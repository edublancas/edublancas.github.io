all: templates resume cv move clean

templates:
	python build.py

resume: templates
	pandoc --standalone --template style.tex \
	--from markdown --to context \
	-o resume.tex tmp_resume.md; \
	context resume.tex

cv: templates
	pandoc --standalone --template style.tex \
	--from markdown --to context \
	-o cv.tex tmp_cv.md; \
	context cv.tex

move: resume cv
	mv resume.pdf ../files/resume.pdf; mv cv.pdf ../files/cv.pdf

clean:
	rm -f tmp_resume.md
	rm -f resume.tuc
	rm -f resume.tex
	rm -f resume.log
	rm -f tmp_cv.md
	rm -f cv.tuc
	rm -f cv.tex
	rm -f cv.log
