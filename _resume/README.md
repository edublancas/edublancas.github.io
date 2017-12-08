# Markdown resume

* Resume are CV are generated from `resume.md` and `cv.md`
* A Python script does some templating to merge the files
* Then I use `pandoc` and a custom template to convert them to pdf using latex
* Requires latex packages `titlesec` and `enumitem`: `tlmgr install titlesec enumitem`