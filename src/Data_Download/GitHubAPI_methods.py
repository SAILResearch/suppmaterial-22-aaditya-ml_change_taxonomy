#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# %% IMPORTS

import time

import requests
from requests.auth import HTTPBasicAuth


# %% GET DATA FROM REQUEST

def get_requests(url, user, passwd):
    r = requests.get(url, auth=HTTPBasicAuth(user, passwd))

    # if timout
    if r.status_code == 403:
        print("LIMIT EXCEEDED")
        print("WAIT AN HOURS")
        i = 0
        while r.status_code != 200:
            r = requests.get(url, auth=HTTPBasicAuth(user, passwd))
            print("{} MINUTES ELAPSED".format(i))
            time.sleep(60)
    elif r.status_code != 200:
        print(r.status_code)
        return []
    # return data
    data = r.json()
    return data


# %% PROG FCT

def progress(current, total):
    print("Currently at {:.2f}%".format(current / total * 100))


# %% GET SOURCE COMMITS
def get_commits(repo_url, user='', passwd=''):
    # auth for 5000 request/h limitprint("\nINPUT GITHUB AUTH TO GET BETTER REQUEST LIMIT")
    if user == '' or passwd == '':
        user = input('username : ')
        passwd = input('passwd :   ')

    # repo url
    github_commit_url = "https://api.github.com/repos/{}/commits?per_page=100&page="
    url = github_commit_url.format(repo_url)

    # fetch all pages
    commits = []
    i = 1
    eop = False
    while not eop:
        print("\n\nFECTHING PAGE {}".format(i))
        data = get_requests(url + str(i), user, passwd)
        commits = commits + data
        i += 1
        if len(data) != 100:
            eop = True

    return commits


# %% GET LIST OF FORKS
def get_forks(repo_url, user='', passwd=''):
    # auth for 5000 request/h limitprint("\nINPUT GITHUB AUTH TO GET BETTER REQUEST LIMIT")
    if user == '' or passwd == '':
        user = input('username : ')
        passwd = input('passwd :   ')

    # repo url
    github_fork_url = "https://api.github.com/repos/{}/forks?sort=stargazers&per_page=100&page="
    url = github_fork_url.format(repo_url)

    # fetch all pages
    forks = []
    i = 1
    eop = False
    while not eop:
        print("\n\nFECTHING PAGE {}".format(i))
        data = get_requests(url + str(i), user, passwd)
        forks = forks + data
        i += 1
        if len(data) != 100:
            eop = True

    # reject private ones
    temp = forks
    for fork in temp:
        if fork['private'] == True:
            forks.remove(fork)
    print("{} private forks".format(len(temp) - len(forks)))

    return forks


# %% GET USEFUL FORKS

def fork_useful(repo_source, repo_fork):
    ''' checking if any of the commit hashs of the repo is the same as the current fork commithash'''
    most_recent_fork_commit_ID = repo_fork.head.commit.binsha
    source_commits = list(repo_source.iter_commits('master'))

    source_commits_IDs = []
    for commit in source_commits:
        source_commits_IDs.append(commit.binsha)

    if most_recent_fork_commit_ID in source_commits_IDs:
        return False
    else:
        return True


# %% GET PULL REQUESTS
def get_pullReq(repo_url, user, passwd):
    # auth for 5000 request/h limitprint("\nINPUT GITHUB AUTH TO GET BETTER REQUEST LIMIT")
    if user == '' or passwd == '':
        user = input('username : ')
        passwd = input('passwd :   ')

    # repo url
    github_pullReq_url = "https://api.github.com/repos/{}/pulls?state=all&per_page=100&page="
    url = github_pullReq_url.format(repo_url)

    # fetch all pages
    pullReq = []
    i = 1
    eop = False
    while not eop:
        print("\n\nFECTHING PAGE {}".format(i))
        data = get_requests(url + str(i), user, passwd)
        pullReq = pullReq + data
        i += 1
        if len(data) != 100:
            eop = True

    return pullReq


# %% GET COMMITS OF PULL REQ

def get_pullReq_commits(pullreq_url, user, passwd):
    # auth for 5000 request/h limitprint("\nINPUT GITHUB AUTH TO GET BETTER REQUEST LIMIT")
    if user == '' or passwd == '':
        user = input('username : ')
        passwd = input('passwd :   ')

    # fetch 250 max commits
    pullReq_commits = get_requests(pullreq_url, user, passwd)

    return pullReq_commits
