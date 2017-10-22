# https://github.com/jgm/pandoc-templates
# https://github.com/jgm/doctemplates
all: templates resume cv move clean

templates:
	python build.py

resume: templates
	pandoc -o resume.pdf --template template.tex \
	--latex-engine=xelatex tmp_resume.md

cv: templates
	pandoc -o cv.pdf --template template.tex \
	--latex-engine=xelatex tmp_cv.md

move: resume cv
	mv resume.pdf ../files/resume.pdf; mv cv.pdf ../files/cv.pdf

clean:
	rm -f tmp_resume.md
	rm -f tmp_cv.md
