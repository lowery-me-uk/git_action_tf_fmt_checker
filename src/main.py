from git import Repo
import git
import github
from pathlib import Path
from subprocess import Popen, PIPE
import requests
import os
import time
import sys
import install_tf as tf

if "INPUT_TERRAFORM_VERSION" in os.environ:
    tf_ver = os.getenv("INPUT_TERRAFORM_VERSION")
else:
    tf_ver = ""

if "INPUT_REPO_TOKEN" in os.environ:
    print("set: github token")
    github_token = os.getenv("INPUT_REPO_TOKEN")
else:
    print("unable to set: github token")
    github_token = ""

if "GITHUB_REPOSITORY" in os.environ:
    github_repo = os.getenv("GITHUB_REPOSITORY")
else:
    github_repo = ""

if "INPUT_BRANCH" in os.environ:
    github_branch = os.getenv("INPUT_BRANCH")
else:
    github_branch = "master"

def terraform_check_fmt():
    p = Popen(["../terraform", "fmt", "-check", "-recursive"], stdout=PIPE, stderr=PIPE)
    p.communicate()
    print(f"INFO: fmt check output - {p.returncode}")
    return p.returncode

def terraform_fmt():
    p = Popen(["../terraform", "fmt", "-recursive"], stdout=PIPE, stderr=PIPE)
    p.communicate()
    print(f"INFO: fmt output {p.returncode}")
    return p.returncode

def create_branch(repo, branch):
    repo.git.branch(branch)

def add_commit_to_branch(branch, message):
    repo.git.checkout(branch)
    repo.git.add(".")
    repo.index.commit(message)

def push_to_origin(branch):
    origin.push(branch)

def create_pull_request(github_repo, api_token, from_branch, into_branch):
    g = github.Github(api_token)
    repo = g.get_repo(github_repo)
    repo.create_pull(title="fixing fmt", body='body', head=from_branch, base=into_branch)

if __name__ == "__main__":
    tf.install(tf_ver)
    repo = Repo(Path.cwd())
    if terraform_check_fmt() != 0:
        origin = repo.remote()
        print(repo.active_branch.name)
        branch = f"{repo.active_branch.name}_fmt_{int(time.time())}"
        create_branch(repo, branch)
        terraform_fmt()
        add_commit_to_branch(branch,'fixing fmt')
        push_to_origin(branch)
        create_pull_request(github_repo, github_token, branch, github_branch)
        sys.exit(1)