#!/usr/bin/env python3
"""CR-AR-06: resolve all registered Git releases and verify pinned manifest identity."""
from __future__ import annotations
import re, subprocess, sys, tempfile
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parent.parent
TAG=re.compile(r"^v\d+\.\d+\.\d+(-[a-z0-9.-]+)?$")
SHA=re.compile(r"^[0-9a-f]{40}$")
DIGEST=re.compile(r"^sha256:[0-9a-f]{64}$")
DEFAULT_MANIFESTS={"maturity-model":"model.yaml","assessment-model":"model.yaml","component":"model.yaml"}
class IntegrityError(Exception): pass
def git(repo:Path,*args:str,check:bool=True)->str:
 r=subprocess.run(["git","-C",str(repo),*args],capture_output=True,text=True)
 if check and r.returncode: raise IntegrityError(r.stderr.strip() or r.stdout.strip() or "git command failed")
 return r.stdout.strip()
def manifest_path(record:dict)->str|None:
 rel=record.get("release") or {}
 p=rel["manifest"] if "manifest" in rel else DEFAULT_MANIFESTS.get(record.get("type"))
 if p is None:return None
 if not isinstance(p,str) or not p.strip():raise IntegrityError("release.manifest must be a non-empty relative path or null")
 q=Path(p)
 if q.is_absolute() or ".." in q.parts or p.startswith("./"):raise IntegrityError(f"unsafe release.manifest path: {p!r}")
 return p
def resolve(repo:Path,url:str,ref:str)->str:
 if TAG.fullmatch(ref):
  git(repo,"fetch","--quiet","--no-tags","--depth=1",url,f"refs/tags/{ref}:refs/tags/{ref}")
  return git(repo,"rev-parse","--verify",f"refs/tags/{ref}^{{commit}}").lower()
 if SHA.fullmatch(ref):
  git(repo,"fetch","--quiet","--no-tags","--depth=1",url,ref)
  sha=git(repo,"rev-parse","--verify","FETCH_HEAD^{commit}").lower()
  if sha!=ref:raise IntegrityError(f"requested SHA {ref} resolved to {sha}")
  return sha
 if DIGEST.fullmatch(ref):raise IntegrityError("sha256 digest references are reserved but unsupported: no content-addressed artifact resolver exists")
 raise IntegrityError(f"unsupported reference {ref!r}; expected vX.Y.Z tag or 40-character commit SHA")
def validate_commit_claim(release:dict,resolved_commit:str)->None:
 claim=release.get("commit")
 if claim and claim.lower()!=resolved_commit.lower():
  raise IntegrityError(f"release.commit {claim} != resolved commit {resolved_commit}")
def validate_manifest(text:str,path:str,asset_id:str,version:str)->None:
 try:d=yaml.safe_load(text)
 except yaml.YAMLError as e:raise IntegrityError(f"invalid YAML in pinned {path}: {e}") from e
 if not isinstance(d,dict):raise IntegrityError(f"pinned {path} is not a YAML mapping")
 if d.get("id")!=asset_id:raise IntegrityError(f"pinned {path} id {d.get('id')!r} != registry id {asset_id!r}")
 if str(d.get("version"))!=str(version):raise IntegrityError(f"pinned {path} version {d.get('version')!r} != release.version {version!r}")
def validate_repository_standard(text:str,record:dict)->None:
 try:d=yaml.safe_load(text)
 except yaml.YAMLError as e:raise IntegrityError(f"invalid YAML in pinned standard.yaml: {e}") from e
 if not isinstance(d,dict):raise IntegrityError("pinned standard.yaml is not a YAML mapping")
 expected=record.get("repository_standard")
 if not isinstance(expected,dict):raise IntegrityError("repository_standard adoption snapshot is required for this maturity-model registration")
 repository=d.get("repository") or {}; standard=d.get("standard") or {}; model=d.get("model") or {}
 checks=[
  ("repository.type",repository.get("type"),"maturity-model"),
  ("standard.id",standard.get("id"),expected.get("id")),
  ("standard.version",str(standard.get("version")),str(expected.get("version"))),
  ("standard.conformance",standard.get("conformance"),expected.get("conformance")),
  ("model.id",model.get("id"),record.get("id")),
  ("model.version",str(model.get("version")),str((record.get("release") or {}).get("version"))),
 ]
 for field,actual,wanted in checks:
  if actual!=wanted:raise IntegrityError(f"pinned standard.yaml {field} {actual!r} != expected {wanted!r}")
def validate(record:dict)->tuple[str,str]:
 src,rel=record.get("source") or {},record.get("release") or {}
 org,repo_name,ref,version=src.get("organization"),src.get("repository"),rel.get("reference"),rel.get("version")
 if not all((org,repo_name,ref,version)):raise IntegrityError("source organization/repository and release version/reference are required")
 path=manifest_path(record);url=f"https://github.com/{org}/{repo_name}.git"
 with tempfile.TemporaryDirectory(prefix="assessment-registry-") as tmp:
  bare=Path(tmp)/"source.git"
  r=subprocess.run(["git","init","--bare",str(bare)],capture_output=True,text=True)
  if r.returncode:raise IntegrityError(r.stderr.strip() or "could not initialize temporary Git repository")
  commit=resolve(bare,url,ref)
  validate_commit_claim(rel,commit)
  if path:
   text=git(bare,"show",f"{commit}:{path}",check=False)
   if not text:raise IntegrityError(f"pinned commit {commit} does not contain authoritative manifest {path}")
   validate_manifest(text,path,record.get("id","<unknown>"),version)
  if record.get("type")=="maturity-model" and record.get("status")!="legacy":
   declaration=git(bare,"show",f"{commit}:standard.yaml",check=False)
   if not declaration:raise IntegrityError(f"pinned commit {commit} does not contain required repository-standard declaration standard.yaml")
   validate_repository_standard(declaration,record)
 return commit,path or "not-applicable"
def main()->int:
 errors=[];count=0
 for p in sorted((ROOT/"registry").rglob("*.yaml")):
  d={}
  try:
   d=yaml.safe_load(p.read_text())
   if not isinstance(d,dict):raise IntegrityError("record is not a YAML mapping")
   commit,manifest=validate(d);count+=1
   s,r=d["source"],d["release"]
   print(f"OK — {d['id']} | {s['organization']}/{s['repository']} | {r['reference']} -> {commit} | manifest={manifest}")
  except (IntegrityError,OSError,KeyError,TypeError) as e:
   s,r=d.get("source") or {},d.get("release") or {}
   errors.append(f"{p.relative_to(ROOT)} [{d.get('id',p.stem)}] {s.get('organization','?')}/{s.get('repository','?')} ref={r.get('reference','?')}: {e}")
 if errors:
  print(f"FAIL — {len(errors)} release-integrity error(s):",file=sys.stderr)
  for e in errors:print("  - "+e,file=sys.stderr)
  return 1
 print(f"OK — {count} registry releases resolved; commit claims and applicable pinned manifests verified")
 return 0
if __name__=="__main__":sys.exit(main())
