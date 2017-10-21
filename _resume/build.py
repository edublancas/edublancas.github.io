"""
Build resume and cv from resume.md and cv.md
"""
import os.path
from jinja2 import Environment, FileSystemLoader

path = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(path))

# this will remove the jinja2 tags
resume = env.get_template('resume.md').render(referral=True)

# this will fill the blocks in cv.md in the corresponding parts in resume.md
# also, do not include referral since cv contains all sections
cv = env.get_template('cv.md').render(referral=False)


with open(os.path.join(path, 'tmp_resume.md'), 'w') as f:
    f.write(resume)


with open(os.path.join(path, 'tmp_cv.md'), 'w') as f:
    f.write(cv)
