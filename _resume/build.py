"""
Build resume and cv from resume.md and cv.md
"""
import subprocess
import os.path
from jinja2 import Environment, FileSystemLoader
from datetime import date


def get_commit_hash():
    out = subprocess.check_output('git show --oneline -s', shell=True)
    return out.decode('utf-8') .replace('\n', '').split(' ')[0]


path = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(path))

git_hash = get_commit_hash()
now = '{}. {}'.format(date.today().strftime('%b %d, %Y'), git_hash)

# this will remove the jinja2 tags
resume = env.get_template('resume.md').render(referral=True, now=now)

# this will fill the blocks in cv.md in the corresponding parts in resume.md
# also, do not include referral since cv contains all sections
cv = env.get_template('cv.md').render(referral=False, now=now)


with open(os.path.join(path, 'tmp_resume.md'), 'w') as f:
    f.write(resume)


with open(os.path.join(path, 'tmp_cv.md'), 'w') as f:
    f.write(cv)
