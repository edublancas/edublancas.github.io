---
layout: post
title: Using GPT-4o for web scraping
comments: false
---

tl;dr; show me the [demo!](#conclusions-and-demo)

![app](/assets/images/ai-web-scraper/app.png)

I'm pretty excited about the new [structured outputs](https://platform.openai.com/docs/guides/structured-outputs)
feature in OpenAI's API so I took it for a spin and developed an AI-assisted web scraper. This post summarizes my learnings.

## Asking GPT-4o to scrape data

The first experiment was to straight ask GPT-4o to extract the data from an HTML
string, so I used the new structured outputs feature with the following [Pydantic](https://docs.pydantic.dev/latest/) models:

```python
from typing import List, Dict

class ParsedColumn(BaseModel):
    name: str
    values: List[str]


class ParsedTable(BaseModel):
    name: str
    columns: List[ParsedColumn]
```

The system prompt is:

> You're an expert web scraper. You're given the HTML contents of a table and you have to extract structured data from it.

Here are some interesting things I found when parsing different tables.

*Note:* I also tried GPT-4o mini but yielded significantly worse results so I just continued my experiments with GPT-4o.

## Parsing complex tables

![alt text](/assets/images/ai-web-scraper/image.png)

After experimenting with some simple tables, I wanted to see how the model would do with a more complex ones, so I passed a 10-day [weather](https://weather.com) forecast from Weather.com. The table
contains a big row for at the top and smaller rows for the other 9
days. Interestingly, GPT-4o was able to parse this correctly:

![alt text](/assets/images/ai-web-scraper/image-1.png)

For the 9 remaining days, the table shows a day and a night forecast (see screenshot above). The model correctly parsed such data and added a `Day/Night` column. Here's how it looks like in the browser (note that to display this, we need to click on the button to the right of each row):

![alt text](/assets/images/ai-web-scraper/image-2.png)

At first, I thought that the parsed `Condition` column was a hallucination since I did not see that in the website, however, upon inspecting the source code, I realized that those tags exist but are invisible in the table.

## Combined rows break the model

When thinking where to find *easy tables*, my first thought was *Wikipedia*. Turns out, a *simple* table from Wikipedia ([Human development index](https://en.wikipedia.org/wiki/Human_Development_Index)) breaks the model because rows with repeated values are merged:

![alt text](/assets/images/ai-web-scraper/image-3.png)

And while the model is able to retrieve individual columns (as instructed by the system prompt), they don't have the same size, hence, I'm unable to represent the data as a table.

I tried modifying the system prompt with the following:

> Tables might collapse rows into a single row. If that's the case, extract the collapsed row as multiple JSON values to ensure all columns contain the same number of rows.

But it didn't work. I have yet to try modifying the system prompt
to tell the model to extract rows instead of columns.

## Asking GPT-4o to return XPaths

Running an OpenAI API call every time can become very expensive, so I figured I'd ask the model to return [XPaths](https://developer.mozilla.org/en-US/docs/Web/XPath) instead of
the parsed data. This would allow me to scrape the same page (e.g., to fetch updated data) without breaking the bank.

After some tweaks, I came up with this prompt:

> You're an expert web scraper.
>
> The user will provide the HTML content and the extracted values in JSON format. 
> Your job is to come up with an XPath that will return all elements of that column.
>
> The XPath should be a string that can be evaluated by Selenium's
> `driver.find_elements(By.XPATH, xpath)` method.
>
> Return the full matching element, not just the text.

Unfortunately, this didn't work well. Sometimes, the model would return invalid XPaths (although
this was alleviated with the sentence that mentions Selenium) or XPaths that would
return incorrect data or no data at all.

## Combining the two approaches

My next attempt was to combine both approaches: once the model extracted the data,
we could use it as a reference to ask the model for the XPath. *This worked much better than straight asking for XPaths!*

I noticed that sometimes the generated XPath would return no data at all so I added
some dumb retry logic: if the XPath returns no results, try again. This did the trick for
the tables I tested.

However, I noticed a new issue: sometimes the first step (extract data) converted images into text (e.g. an arrow pointing upwards might appear in the
extracted data as "arrow-upwards"), this caused the second step to fail since it'd look for data that wasn't there. I did not attempt to fix this problem.

## GPT-4o is very expensive

![alt text](/assets/images/ai-web-scraper/image-4.png)

Scraping with GPT-4o can become very expensive since even small HTML tables can contain lots of characters. I've been experimenting for two days and I've already spent $24!

To reduce the cost, I added some clean up logic to remove unnecessary data from the HTML string before passing it to the model. A simple function that removes all properties except `class`, `id`, and `data-testid` (which are the ones I noticed the generated XPaths were using) trimmed the number of characters in the table by half.

I didn't see any performance degradations and my suspicion is that the results would actually improve extraction quality.

Currently, the second step (generate XPaths) makes one model call per column in
the table, another improvement could be to generate more than one XPath, I have yet
to try this approach and evaluate performance.


## Conclusions and demo

I was surprised by the extraction quality of GPT-4o (but then sadly surprised when I looked at how much I'd have to pay OpenAI!). Nonetheless, this was a fun experiment and I definitely see potential for AI-assisted web scraping tools.

I did a quick demo using Streamlit, you can check it out here:

Some stuff I'd like to try if I had more time: [https://orange-resonance-9766.ploomberapp.io](https://orange-resonance-9766.ploomberapp.io)

1. Capture browser events: the current demo is a one-off process: users enter the URL and an initial XPath. This isn't great UX as it'd be better to ask the user to click on the table they want to extract, and to provide some sample rows so the model can understand the structure a bit better.
2. In complex tables, a single XPath might not be enough to extract a full column, I'd like to see if asking the LLM to return a program (e.g. Python) would work.
3. More experimenting with the HTML clean up is needed. It's very expensive to use GPT-4o and I feel like I'm passing a lot of unnecessary data to the model
