# Personal website

Source for my [personal website](http://edublancas.github.io/).

```
bundle exec jekyll serve --incremental
```


## Add compile script as pre-commit hook

The source is written in Markdown format, before
any commit is done run `compile` to convert .md files
to .html

```bash
ln -s ../../compile .git/hooks/pre-commit
```
