from git import Repo
import git
import github
import pathlib
from subprocess import Popen, PIPE
import requests
import os
import install_tf as tf

if "INPUT_TERRAFORM_VERSION" in os.environ:
    tf_ver = os.getenv("INPUT_TERRAFORM_VERSION")
else:
    tf_ver = ""

def terraform_check_fmt():
    p = Popen(["./terraform", "fmt", "-check", "-recursive"], stdout=PIPE, stderr=PIPE)
    print(p.communicate())
    return p.returncode

def terraform_fmt():
    p = Popen(["./terraform", "fmt", "-recursive"], stdout=PIPE, stderr=PIPE)
    print(p.communicate())
    return p.returncode

# def create_branch(repo, branch):
#     repo.git.branch(branch)

# def add_commit_to_branch(branch, message):
#     repo.git.checkout(branch)
#     repo.git.add(".")
#     repo.index.commit(message)

# def push_to_origin(branch):
#     origin.push(branch)

# def create_pull_request(api_token, from_branch, into_branch):
#     g = github.Github(api_token)
#     repo = g.get_repo("lowery-me-uk/terraform-dns")
#     repo.create_pull(title="fixing fmt", body='body', head=from_branch, base=into_branch)

if __name__ == "__main__":
    # repo = clone_repo('https://github.com/lowery-me-uk/terraform-dns')
    tf.install(tf_ver)
    if terraform_check_fmt() != 0:
        print('yup')
        # origin = repo.remote()
        # create_branch(repo, branch)
        # terraform_fmt()
        # add_commit_to_branch(branch,'fixing fmt')
        # push_to_origin(branch)
        # create_pull_request(token, branch, 'master')