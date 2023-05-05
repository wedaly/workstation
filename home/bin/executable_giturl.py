#!/usr/bin/env python3

from contextlib import contextmanager
import os
import sys
import subprocess
import re


def main():
    if len(sys.argv) < 2:
        print("USAGE: {} FILE".format(sys.argv[0]))
        sys.exit(1)

    filepath = sys.argv[1]
    url = url_for_file(filepath)
    print(url)


def url_for_file(filepath):
    dirpath = os.path.dirname(filepath) or "."
    with chdir(dirpath):
        repo_url = git_cmd(["remote", "get-url", "origin"])
        repo_root = git_cmd(["rev-parse", "--show-toplevel"])
        git_commit = git_cmd(["rev-parse", "HEAD"])

    relpath = os.path.relpath(filepath, start=repo_root)

    if "github.com" in repo_url:
        return github_url(repo_url, git_commit, relpath)
    else:
        raise Exception("Cannot construct file URL for git repository {}".format(repo_url))


def github_url(repo_url, git_commit, relpath):
    repo_org, repo_name = github_repo_org_and_name(repo_url)
    return "https://github.com/{}/{}/blob/{}/{}".format(
        repo_org,
        repo_name,
        git_commit,
        relpath,
    )


def github_repo_org_and_name(repo_url):
    m = re.match("git@github.com:([^/]+)/([^.]+)", repo_url)
    if m is None:
        raise Exception("Could not extract GitHub repo org and name from {}".format(repo_url))
    return m.group(1), m.group(2)


def git_cmd(args):
    result = subprocess.run(["git"] + args, capture_output=True)
    result.check_returncode()
    return result.stdout.decode("utf-8").strip()


@contextmanager
def chdir(path):
    wd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(wd)


if __name__ == "__main__":
    main()

