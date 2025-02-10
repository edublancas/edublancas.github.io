---
layout: post
title: "How do AI agents work, anyway?"
comments: false
---

At [work](https://ploomber.io/), we've initiated several projects incorporating
AI agents into our operations and product, which sparked my interest in better understanding
the technology. While exploring resources, I noticed a significant gap
between the concepts and  implementations so I chose to examine one
framework (`smolagents`) in detail to understand how it works.

In this post, I'll provide a brief conceptual introduction to AI agents and analyze
the implementation of the `smolagents` library by examining its OpenAI API calls using
`mitmproxy` and DuckDB.

# What are agents?

An AI agent is a program that performs actions through a set of tools. For example,
ChatGPT is an agent that can search the web via a tool. Agents use Large Language Models
(LLMs) to break down tasks into smaller ones (planning), choose which tools to use at
each step, and determine when the task is complete.

Tools are typically functions (like Python functions) that the agent calls to
retrieve results or perform actions (such as writing to a database).

The plan is the series of steps that the agent will perform. Not all plans are created
equal: shorter plans and less computationally expensive plans are desirable.

To learn more about AI agents, check out
[Chip Huyen's blog post](https://huyenchip.com/2025/01/07/agents.html#planning)
and the [smolagents](https://huggingface.co/blog/smolagents) blog post.

# Code agents

Since the LLM decides which tools to run at each step, we need a way to represent
tool calling (aka function calling). Code agents represent their tool calls using
actual code (e.g., Python code), in contrast to other agents which represent tool
calls with JSON. [Research has shown](https://arxiv.org/abs/2402.01030) that code-based tool
calling produces more effective agents.

We'll be using the [smolagents](https://github.com/huggingface/smolagents) framework
to understand how agents work with the code agent configuration (though you can
also use the JSON configuration).

# Setup

First, let's install the required dependencies:

- [smolagents](https://github.com/huggingface/smolagents) for running the agent
- [mitmproxy](https://mitmproxy.org/) for intercepting OpenAI API requests
- [DuckDB](https://duckdb.org/) for querying the OpenAI API logs 
- [rich](https://github.com/Textualize/rich) for prettier terminal output

~~~sh
# Install packages (including litellm for OpenAI model support)
pip install 'smolagents[litellm]' mitmproxy duckdb rich
~~~

Download the code:

~~~sh
git clone --depth 1 https://github.com/edublancas/posts
cd smolagents/
~~~

Next, start the reverse proxy to intercept OpenAI requests and log them to a `.jsonl` file that we'll query later with DuckDB:

~~~sh
mitmdump -s proxy_logger.py --mode reverse:https://api.openai.com --listen-port 8080
~~~

# Basic example (multiplication, no tools)

Let's start with a basic example: asking the model to perform a simple multiplication without providing any tools.

~~~python
from smolagents import CodeAgent, OpenAIServerModel

# Initialize the model with our reverse proxy
model = OpenAIServerModel(
    model_id="gpt-4o-mini",
    api_base="http://localhost:8080/v1",
)

# Create an agent with no tools
agent = CodeAgent(tools=[], model=model, add_base_tools=False)

# Run the agent with a simple multiplication task
agent.run("How much is 2 * 21?")
~~~

After running the code, we can view the execution logs by running `python print.py`, which displays all logs from the `.jsonl` file.

## Prompt

Here's the prompt for the API call, I removed several parts to make it shorter (several
parts are redundant to deal with the stuborrness of LLMs), but kept the overall message the
same. You can see the complete logs in the `openai_logs_no_base_tools.jsonl` file.

### System

The system prompt indicates the model what their purpose is and the rules it must abide
to. It essentially tells the LLM that its job is to solve tasks with tools, and
that solving the tasks involves three steps: `Thought`, `Code`, and `Observation`:

~~~md
You are an expert assistant who can solve any task using code blobs. You have been
given access to a list of tools: these tools are Python functions.

To solve the task, you must plan forward to proceed in a series of steps, in a cycle
of 'Thought:', 'Code:', and 'Observation:' sequences.

'Thought:' sequence, you should explain your reasoning and the tools that you want to use.

'Code:' sequence, you should write the code in Python.

During each intermediate step, use `print()` to save important information.
These `print` outputs will then appear in the 'Observation:' field, which will be
available as input for the next step.

In the end you have to return a final answer using the `final_answer` tool.

Here are a few examples:

---

Task: "What is the result of the following operation: 5 + 3 + 2"

Thought: I will use python code to compute the result of the operation and then return
the final answer using the `final_answer` tool

Code:
```py
result = 5 + 3 + 2
final_answer(result)
```
<end_code>
---

[...MORE EXAMPLES HERE]
~~~


After listing a few more examples, the system prompt includes the available tools (we
only have the `final_answer` tool) and the rules it must abide by:

~~~md
You only have access to these tools:


- final_answer: Provides a final answer to the given problem.
    Takes inputs: {'answer': {'type': 'any', 'description': 'The final answer to the problem'}}
    Returns an output of type: any
[... MORE TOOLS ARE ADDED HERE, IF ANY]


Here are the rules you should always follow to solve your task:

1. Always provide a 'Thought:' sequence, and a 'Code:
```py' sequence ending with '```<end_code>' sequence, else you will fail.
[...MORE RULES HERE]
~~~

### User

The next message has `{"role": "user"}`, and it contains the task to perform:

> New task:
> How much is 2 * 21?

## Response

Remember that one of the rules in the system prompt says:

>  Always provide a 'Thought:' sequence, and a 'Code:' sequence

Hence, the model proceeds to return `Thought:` and `Code:`

~~~md
Thought: This is a simple multiplication task. I will multiply 2 by 21 and return the
result using the `final_answer` tool.

Code:

```py
result = 2 * 21
final_answer(result)
```
~~~

The agent then runs the Python code, and since the `Code:` portion already uses
`final_answer`, it knows it has finished.

## Output

Here's the output that `agent.run` displays:

```
╭──────────── New run ────────────╮
│                                 │
│ How much is 2 * 21?             │
│                                 │
╰─ OpenAIServerModel - gpt-4o-mini╯
━━━━━━━━━━━━━━━━ Step 1 ━━━━━━━━━━━━━━━━
 ─ Executing parsed code: ─────────────
  result = 2 * 21
  final_answer(result)
 ──────────────────────────────────────
Out - Final answer: 42
[Step 0: Duration 1.08 seconds| Input tokens: 1,956 | Output tokens: 52]
```

# Multi-step example (fibonacci series, no tools)

The previous task was trivial (no tools required, besides the `final_answer` tool). The
true potential of AI agents lies in performing complex tasks by using tools. Let's look
at another agent whose plan involves two steps.

```python
from smolagents import CodeAgent, OpenAIServerModel

model = OpenAIServerModel(
    model_id="gpt-4o-mini",
    api_base="http://localhost:8080/v1",
)

agent = CodeAgent(tools=[], model=model, add_base_tools=False)

agent.run(
    "Could you give me the 118th number in the Fibonacci sequence?",
)
```

## Prompt (1st step)

### System

The system prompt is the same as in the previous example.

### User

> New task:
> Could you give me the 118th number in the Fibonacci sequence?

## Response (1st step)

Unlike the first example, this response doesn't use `final_answer`:

~~~md
Thought: To find the 118th number in the Fibonacci sequence, I can use a simple
iterative approach to compute Fibonacci numbers until the 118th index. This will be
efficient and easy to implement. I'll create two variables to hold the last two
Fibonacci numbers and iteratively compute the next Fibonacci number until I reach
the 118th one.

Code:
```py
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

fibonacci_118 = fibonacci(118)
print(fibonacci_118)
```
~~~

This example highlights one of the key challenges in agent systems: planning efficiency.
While a task can often be solved in multiple ways, some plans are more efficient than
others. Longer plans require more computational steps and time to execute, but current
models don't necessarily optimize for the shortest possible solution.

In this case, the model chose a two-step approach when a single step would have
sufficed: it could have directly called `final_answer(fibonacci_118)` instead of
using `print(fibonacci_118)`.

Since the model didn't use `final_answer` to conclude the task, we need to proceed
with an additional step.


## Prompt (2nd step)

### System

The system prompt is the same as in the previous example.

### User

> New task:
> Could you give me the 118th number in the Fibonacci sequence?

### Assistant

Unlike the first example where we had a single step, this time we have an assistant message.
This message includes the output from the previous step (`Thought:` and `Code:`) along
with information about the tools that were called (`Calling tools:`).

~~~md
Thought: To find the 118th number in the Fibonacci sequence, I can use a simple iterative approach to compute Fibonacci
numbers until the 118th index. This will be efficient and easy to implement. I'll create two variables to hold the last
two Fibonacci numbers and iteratively compute the next Fibonacci number until I reach the 118th one.

Code:
```py
def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

fibonacci_118 = fibonacci(118)
print(fibonacci_118)
```
Calling tools:
[{'id': 'call_1', 'type': 'function', 'function': {'name': 'python_interpreter', 'arguments': 'def fibonacci(n):\n    a,
b = 0, 1\n    for _ in range(n):\n        a, b = b, a + b\n    return a\n\nfibonacci_118 =
fibonacci(118)\nprint(fibonacci_118)'}}]
~~~

### User

To generate the final message, the agent runs the Python code, and prints the output:

~~~md
Call id: call_1
Observation:
Execution logs:
2046711111473984623691759
Last output from code snippet:
None
~~~


## Response

The response from the second API call shows that the model has already identified the
final output and produces a new code snippet that just uses `final_answer`, which
finishes the agent execution.

~~~
Thought: The 118th number in the Fibonacci sequence is 2046711111473984623691759. Now I will provide this as the final
answer using the `final_answer` tool.

Code:
```py
final_answer(2046711111473984623691759)
```
~~~

# Output

This is the output we see in the terminal.

```
╭──────────── New run ────────────╮
│                                 │
│ Could you give me the 118th     │
│ number in the Fibonacci         │
│ sequence?                       │
│                                 │
╰─ OpenAIServerModel - gpt-4o-mini╯
━━━━━━━━━━━━━━━━ Step 1 ━━━━━━━━━━━━━━━━
 ─ Executing parsed code: ─────────────
  def fibonacci(n):
      a, b = 0, 1
      for _ in range(n):
          a, b = b, a + b
      return a

  fibonacci_118 = fibonacci(118)
  print(fibonacci_118)
 ──────────────────────────────────────
Execution logs:
2046711111473984623691759

Out: None
[Step 0: Duration 2.70 seconds| Input tokens: 1,961 | Output tokens: 127]
━━━━━━━━━━━━━━━━ Step 2 ━━━━━━━━━━━━━━━━
 ─ Executing parsed code: ─────────────
  final_answer(2046711111473984623691759)
 ──────────────────────────────────────
Out - Final answer: 2046711111473984623691759
[Step 1: Duration 1.55 seconds| Input tokens: 4,179 | Output tokens: 186]
```

# Final thoughts

The concept of AI agents is rapidly evolving. Encouragingly, a consensus is emerging
around their core concepts: agents plan and use tools to accomplish tasks.
However, research in this field is still a work in progress. As new research emerges
and more powerful models are developed, many existing frameworks will likely become
outdated. This is why I believe it's crucial to understand what's happening behind the
scenes; specifically, what API calls are being made to the LLM. This understanding
allows us to grasp their strengths and weaknesses, customize their behavior, or
even develop our own solutions when existing options don't meet our needs.

A significant limitation of current frameworks is their reliance on hardcoded prompts,
as there's no guarantee these prompts will perform optimally for specific tasks.
I predict that future agent frameworks will evolve into meta-frameworks, offering
greater flexibility to customize prompts and choose between different planning
strategies (such as defining a complete plan upfront versus incrementally adding steps
until reaching a stopping condition, like `smolagents` does).