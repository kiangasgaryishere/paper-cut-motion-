#!/usr/bin/env python3
"""Create project memory from a required existing UTF-8 script. Never overwrite."""
import argparse,json,shutil,sys
from pathlib import Path

def initialize(project,script,title=''):
    project=Path(project).expanduser().resolve();script=Path(script).expanduser().resolve()
    if not script.is_file():raise ValueError('An existing script file is required; this skill does not write scripts.')
    text=script.read_text(encoding='utf-8-sig')
    if not text.strip():raise ValueError('The supplied script is empty.')
    if project.exists() and (not project.is_dir() or any(project.iterdir())):raise ValueError('Project is not empty; refusing to overwrite it.')
    templates=Path(__file__).resolve().parents[1]/'templates'
    project.mkdir(parents=True,exist_ok=True)
    for source in templates.iterdir():
        if source.is_file() and source.name!='README.md':shutil.copyfile(source,project/source.name)
    (project/'script.md').write_text(text,encoding='utf-8')
    brief=json.loads((project/'brief.json').read_text());brief['title']=title or project.name
    (project/'brief.json').write_text(json.dumps(brief,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    (project/'README.md').write_text('# '+brief['title']+'\n\nSupplied script: script.md. Fill the brief, art direction, storyboard, sound plan and shared timeline before production.\n\nThis initialized project is a draft, not an approved production plan.\n',encoding='utf-8')
    return project

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--project',required=True);p.add_argument('--script-file',required=True);p.add_argument('--title',default='');a=p.parse_args()
    try:print(initialize(a.project,a.script_file,a.title));return 0
    except (ValueError,OSError,UnicodeError) as e:print(str(e),file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
