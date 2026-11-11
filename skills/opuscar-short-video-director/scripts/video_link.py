#!/usr/bin/env python3
"""Make a pinned GitHub video link after commit/push; optionally verify public bytes."""
import argparse,hashlib,json,re,subprocess,sys
from pathlib import Path
from urllib.parse import quote,urlsplit
from urllib.request import urlopen

def git(repo,*args):
    p=subprocess.run(['git','-C',str(repo),*args],text=True,capture_output=True,timeout=30)
    if p.returncode:raise ValueError('Git check failed; inspect repository access/state. No download link is certified.')
    return p.stdout.strip()

def github_repository(remote):
    if remote.startswith('git@github.com:'):path=remote.split(':',1)[1]
    else:
        parsed=urlsplit(remote)
        if parsed.hostname!='github.com' or parsed.scheme not in ['https','ssh']:raise ValueError('This helper supports GitHub remotes only.')
        path=parsed.path.lstrip('/')
    path=path.rstrip('/');path=path[:-4] if path.endswith('.git') else path
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',path):raise ValueError('Unexpected GitHub repository path.')
    return path

def link_for(repository,commit,path,visibility):
    if not re.fullmatch(r'[0-9a-fA-F]{40}|[0-9a-fA-F]{64}',commit):raise ValueError('Use a full immutable video commit SHA.')
    if visibility not in ['public','private']:raise ValueError('Resolve repository visibility first.')
    encoded=quote(path,safe='/')
    if visibility=='public':return f'https://raw.githubusercontent.com/{repository}/{commit}/{encoded}'
    return f'https://github.com/{repository}/blob/{commit}/{encoded}?raw=true'

def digest(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''):h.update(chunk)
    return h.hexdigest()

def inspect_artifact(repo,file,remote='origin'):
    root=Path(git(repo,'rev-parse','--show-toplevel')).resolve();candidate=Path(file).expanduser()
    candidate=candidate if candidate.is_absolute() else root/candidate
    if candidate.is_symlink():raise ValueError('Deliver a real video file, not a symlink.')
    video=candidate.resolve(strict=True)
    if not video.is_file() or not video.is_relative_to(root):raise ValueError('Video must be a file inside the selected repository.')
    relative=video.relative_to(root).as_posix()
    git(root,'ls-files','--error-unmatch','--',relative)
    check=subprocess.run(['git','-C',str(root),'diff','--quiet','HEAD','--',relative],capture_output=True,timeout=30)
    if check.returncode:raise ValueError('Video has uncommitted/staged changes. Commit it before making a download link.')
    commit=git(root,'rev-parse','HEAD');blob=f'{commit}:{relative}';size=int(git(root,'cat-file','-s',blob))
    if size<1024 and git(root,'show',blob).startswith('version https://git-lfs.github.com/spec/v1'):raise ValueError('Committed object is an LFS pointer, not downloadable video bytes. Use a verified LFS/artifact delivery method.')
    if size!=video.stat().st_size:raise ValueError('Committed object differs from local file; inspect filters before linking.')
    repository=github_repository(git(root,'remote','get-url',remote))
    return root,video,dict(repository=repository,video_path=relative,video_commit=commit,bytes=size,sha256=digest(video))

def check_pushed(repo,remote,branch,commit):
    if not branch or branch.startswith('-'):raise ValueError('Select the actual pushed task branch.')
    git(repo,'check-ref-format','refs/heads/'+branch)
    tip=git(repo,'ls-remote','--exit-code',remote,'refs/heads/'+branch)
    if not tip or tip.split()[0]!=commit:raise ValueError('Remote branch tip does not match the video commit. Push/check the correct branch first.')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',required=True);p.add_argument('--file',required=True);p.add_argument('--remote',default='origin');p.add_argument('--branch');p.add_argument('--visibility',required=True,choices=['public','private']);p.add_argument('--verify-download',action='store_true');a=p.parse_args()
    try:
        root,video,result=inspect_artifact(a.repo,a.file,a.remote)
        branch=a.branch or git(root,'symbolic-ref','--quiet','--short','HEAD');check_pushed(root,a.remote,branch,result['video_commit'])
        url=link_for(result['repository'],result['video_commit'],result['video_path'],a.visibility)
        result.update(branch=branch,remote_push_verified=True,download_url=url,download_verified=False,authentication_required=a.visibility=='private')
        if a.verify_download:
            if a.visibility=='private':raise ValueError('Private download verification needs an authenticated connector/browser; no anonymous verification is claimed.')
            h=hashlib.sha256();count=0
            with urlopen(url,timeout=30) as response:
                for chunk in iter(lambda:response.read(1024*1024),b''):
                    count+=len(chunk)
                    if count>result['bytes']:raise ValueError('Download is larger than the committed artifact.')
                    h.update(chunk)
            if count!=result['bytes'] or h.hexdigest()!=result['sha256']:raise ValueError('Downloaded bytes do not match the pushed local video.')
            result['download_verified']=True
        if a.visibility=='private':result['access_note']='Open while signed into the GitHub account with access; authenticated download was not verified by this helper.'
        print(json.dumps(result,indent=2));return 0
    except (OSError,ValueError,subprocess.TimeoutExpired) as e:print(json.dumps({'ready':False,'error':str(e)}),file=sys.stderr);return 2
if __name__=='__main__':sys.exit(main())
