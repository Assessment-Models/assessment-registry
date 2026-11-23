import subprocess,tempfile,unittest
from pathlib import Path
from scripts.validate_release_integrity import IntegrityError,resolve,validate_commit_claim,validate_manifest,validate_repository_standard
def git(p,*a):
 r=subprocess.run(["git","-C",str(p),*a],capture_output=True,text=True)
 if r.returncode:raise AssertionError(r.stderr)
 return r.stdout.strip()
class TestReleaseIntegrity(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.root=Path(self.t.name);self.remote=self.root/"remote.git";self.work=self.root/"work"
  subprocess.run(["git","init","--bare",str(self.remote)],check=True,capture_output=True);subprocess.run(["git","init",str(self.work)],check=True,capture_output=True)
  git(self.work,"config","user.email","test@example.invalid");git(self.work,"config","user.name","Test")
  (self.work/"model.yaml").write_text("id: sample-model\nversion: 1.2.3\n")
  git(self.work,"add","model.yaml");git(self.work,"commit","-m","fixture");self.sha=git(self.work,"rev-parse","HEAD")
  git(self.work,"remote","add","origin",str(self.remote));git(self.work,"push","origin","HEAD:main")
  git(self.work,"tag","v1.2.3");git(self.work,"tag","-a","v1.2.4","-m","annotated");git(self.work,"push","origin","--tags")
 def tearDown(self):self.t.cleanup()
 def target(self):
  p=self.root/("bare"+str(len(list(self.root.glob("bare*")))));subprocess.run(["git","init","--bare",str(p)],check=True,capture_output=True);return p
 def test_sha(self):self.assertEqual(resolve(self.target(),str(self.remote),self.sha),self.sha)
 def test_lightweight_tag(self):self.assertEqual(resolve(self.target(),str(self.remote),"v1.2.3"),self.sha)
 def test_annotated_tag_peels(self):self.assertEqual(resolve(self.target(),str(self.remote),"v1.2.4"),self.sha)
 def test_missing_tag(self):
  with self.assertRaises(IntegrityError):resolve(self.target(),str(self.remote),"v9.9.9")
 def test_unresolvable_sha(self):
  with self.assertRaises(IntegrityError):resolve(self.target(),str(self.remote),"f"*40)
 def test_digest_fails_closed(self):
  with self.assertRaisesRegex(IntegrityError,"reserved but unsupported"):resolve(self.target(),str(self.remote),"sha256:"+"a"*64)
 def test_tag_commit_mismatch_fails(self):
  with self.assertRaises(IntegrityError):validate_commit_claim({"commit":"f"*40},self.sha)
 def test_manifest_id_mismatch(self):
  with self.assertRaises(IntegrityError):validate_manifest("id: other\nversion: 1.2.3\n","model.yaml","sample-model","1.2.3")
 def test_manifest_version_mismatch(self):
  with self.assertRaises(IntegrityError):validate_manifest("id: sample-model\nversion: 9.9.9\n","model.yaml","sample-model","1.2.3")

 def test_repository_standard_snapshot_matches_pinned_declaration(self):
  record={"id":"sample-model","release":{"version":"1.2.3"},"repository_standard":{"id":"AM-MODEL-REPOSITORY-STANDARD","version":"1.0.1","conformance":"structural"}}
  declaration="repository:\n  type: maturity-model\nstandard:\n  id: AM-MODEL-REPOSITORY-STANDARD\n  version: '1.0.1'\n  conformance: structural\nmodel:\n  id: sample-model\n  version: '1.2.3'\n"
  validate_repository_standard(declaration,record)
 def test_repository_standard_version_mismatch_fails(self):
  record={"id":"sample-model","release":{"version":"1.2.3"},"repository_standard":{"id":"AM-MODEL-REPOSITORY-STANDARD","version":"1.0.1","conformance":"structural"}}
  declaration="repository:\n  type: maturity-model\nstandard:\n  id: AM-MODEL-REPOSITORY-STANDARD\n  version: '2.0.0'\n  conformance: structural\nmodel:\n  id: sample-model\n  version: '1.2.3'\n"
  with self.assertRaisesRegex(IntegrityError,"standard.version"):validate_repository_standard(declaration,record)
 def test_repository_standard_model_version_mismatch_fails(self):
  record={"id":"sample-model","release":{"version":"1.2.3"},"repository_standard":{"id":"AM-MODEL-REPOSITORY-STANDARD","version":"1.0.1","conformance":"structural"}}
  declaration="repository:\n  type: maturity-model\nstandard:\n  id: AM-MODEL-REPOSITORY-STANDARD\n  version: '1.0.1'\n  conformance: structural\nmodel:\n  id: sample-model\n  version: '9.9.9'\n"
  with self.assertRaisesRegex(IntegrityError,"model.version"):validate_repository_standard(declaration,record)
if __name__=="__main__":unittest.main()
