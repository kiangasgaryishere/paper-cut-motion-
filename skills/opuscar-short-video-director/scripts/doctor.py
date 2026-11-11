#!/usr/bin/env python3
"""Read-only dependency report. Does not certify rendering or listening."""
import argparse,json,os,re,shutil,subprocess,sys
from pathlib import Path

def run(args,cwd=None):
    try:
        p=subprocess.run(args,cwd=cwd,text=True,capture_output=True,timeout=15)
        return p.returncode,(p.stdout or p.stderr).strip()
    except (OSError,subprocess.TimeoutExpired) as e:return 127,str(e)

def inspect(lib=None,sfx=None):
    checks={};missing=[]
    for name,minimum in [('git',None),('node',20),('npm',None),('ffmpeg',7),('ffprobe',None)]:
        exe=shutil.which(name);code,out=run([exe,'-version' if name.startswith('ff') else '--version']) if exe else (127,'not found')
        match=re.search(r'(?:ffmpeg version\s+n?|v)?(\d+)\.',out)
        okay=code==0 and (minimum is None or bool(match and int(match.group(1))>=minimum))
        checks[name]={'ready':okay,'path':exe,'version':out.splitlines()[0] if out else ''}
        if not okay:missing.append(name+(f'>={minimum}' if minimum else ''))
    checks['python']={'ready':sys.version_info>=(3,11),'path':sys.executable,'version':sys.version.split()[0]}
    if not checks['python']['ready']:missing.append('Python>=3.11')
    library=Path(lib).expanduser().resolve() if lib else None
    library_ok=bool(library and (library/'AGENTS.md').is_file() and (library/'core/render/video.mjs').is_file())
    checks['lemo_library']={'ready':library_ok,'path':str(library) if library else None}
    if not library_ok:missing.append('Lemo library')
    if library_ok:
        code,commit=run(['git','rev-parse','HEAD'],library);checks['lemo_library']['commit']=commit if code==0 else 'unavailable'
        py=library/('.venv/Scripts/python.exe' if os.name=='nt' else '.venv/bin/python')
        code,out=run([str(py),'-c','import numpy,scipy,soundfile,soxr,PIL,fontTools'])
        checks['python_core']={'ready':code==0,'path':str(py),'details':out}
        if code:missing.append('Opuscar Python core tier')
        node=shutil.which('node')
        code,out=run([node,'-e',"require.resolve('playwright-core');require.resolve('three')"],library) if node else (127,'Node missing')
        checks['node_core']={'ready':code==0,'details':out}
        if code:missing.append('Opuscar Node core tier')
    browser=os.environ.get('PLAYWRIGHT_CHROME') or next((shutil.which(n) for n in ['chromium','chromium-browser','google-chrome','chrome'] if shutil.which(n)),None)
    if not browser:
        caches=[Path(os.environ.get('PLAYWRIGHT_BROWSERS_PATH','')).expanduser()] if os.environ.get('PLAYWRIGHT_BROWSERS_PATH') else []
        caches += [Path(os.environ.get('XDG_CACHE_HOME',str(Path.home()/'.cache')))/'ms-playwright',Path.home()/'Library/Caches/ms-playwright']
        for cache in caches:
            if not cache.is_dir():continue
            for pattern in ['*/**/headless_shell','*/**/chrome-headless-shell','*/**/chrome','*/**/chrome.exe']:
                candidates=[x for x in cache.glob(pattern) if x.is_file()]
                if candidates:browser=str(candidates[0]);break
            if browser:break
    browser_ok=bool(browser and Path(browser).is_file() and os.access(browser,os.X_OK))
    checks['browser_executable']={'ready':browser_ok,'path':browser,'launch_test':'not performed'}
    if not browser_ok:missing.append('Chromium executable / Playwright browser')
    sound=Path(sfx).expanduser().resolve() if sfx else None
    sound_ok=bool(sound and all((sound/f).is_file() for f in ['sounds.json','GUIDE.md','LICENSE']) and (sound/'sounds').is_dir())
    checks['sfx_kit']={'ready':sound_ok,'path':str(sound) if sound else None}
    if not sound_ok:missing.append('SFX Kit')
    return {'ready':not missing,'checks':checks,'missing':missing,'scope':'Dependency discovery only; run a real style smoke render/export and media checks.'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--lib-dir');p.add_argument('--sfx-dir');a=p.parse_args()
    report=inspect(a.lib_dir,a.sfx_dir);print(json.dumps(report,indent=2));return 0 if report['ready'] else 2
if __name__=='__main__':sys.exit(main())
