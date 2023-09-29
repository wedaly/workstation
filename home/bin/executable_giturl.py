#!/usr/bin/env python3

from contextlib import contextmanager
import os
import sys
import subprocess
import urllib.parse
import re


def main():
    if len(sys.argv) < 2:
        print("USAGE: {} FILE [LINE]".format(sys.argv[0]))
        sys.exit(1)

    filepath = sys.argv[1]
    line = int(sys.argv[2]) if len(sys.argv) >= 2 else None

    url = url_for_file(filepath, line)
    print(url)


def url_for_file(filepath, line):
    dirpath = os.path.dirname(filepath) or "."
    with chdir(dirpath):
        repo_url = git_cmd(["remote", "get-url", "origin"])
        repo_root = git_cmd(["rev-parse", "--show-toplevel"])
        git_commit = git_cmd(["rev-parse", "HEAD"])

    relpath = os.path.relpath(filepath, start=repo_root)

    if "github.com" in repo_url:
        return github_url(repo_url, git_commit, relpath, line)
    elif "visualstudio.com" in repo_url or "dev.azure.com" in repo_url:
        return ado_url(repo_url, git_commit, relpath, line)
    else:
        raise Exception("Cannot construct file URL for git repository {}".format(repo_url))


def github_url(repo_url, git_commit, relpath, line):
    repo_org, repo_name = github_repo_org_and_name(repo_url)
    url = "https://github.com/{}/{}/blob/{}/{}".format(
        repo_org,
        repo_name,
        git_commit,
        relpath,
    )

    if line is not None:
        url += "#L{}".format(line)

    return url


def github_repo_org_and_name(repo_url):
    patterns = [
        "git@github.com:([^/]+)/(.+).git$",
        "git@github.com:([^/]+)/(.+)$",
        "https://github.com/([^/]+)/(.+).git$",
        "https://github.com/([^/]+)/(.+)$",
    ]

    for p in patterns:
        m = re.match(p, repo_url)
        if m is not None:
            return m.group(1), m.group(2)

    raise Exception("Could not extract GitHub repo org and name from {}".format(repo_url))


def ado_url(repo_url, git_commit, relpath, line):
    repo_org, repo_project, repo_name = ado_repo_org_project_and_name(repo_url)
    url = "https://{}.visualstudio.com/{}/_git/{}?path={}&version=GC{}&_a=contents".format(
        repo_org,
        repo_project,
        repo_name,
        urllib.parse.quote_plus("/" + relpath),
        git_commit,
    )

    if line is not None:
        url += "&line={}&lineStartColumn=1&lineEndColumn=1&lineStyle=plain".format(line)

    return url


def ado_repo_org_project_and_name(repo_url):
    patterns = [
        "[^@]+@.+\.com:[^/]+/([^/]+)/([^.]+)/(.+)",
    ]

    for p in patterns:
        m = re.match(p, repo_url)
        if m is not None:
            return m.group(1), m.group(2), m.group(3)

    raise Exception("Could not extract ADO repo org, project, and name from {}".format(repo_url))


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

