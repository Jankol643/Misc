import os
import subprocess
import git
import time
from datetime import datetime, timedelta

FOLDER = os.path.dirname(os.path.abspath(__file__))
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
REPO_PATH = 'https://github.com/Jankol643/exercises'

repo = git.Repo(REPO_PATH)
untracked_files = repo.untracked_files # list of untracked files

def get_commits(repo):
    """
    Get commits from specified repo

    :param repo: repository to get commits from
    :type repo: Repo
    :return: list of commits
    :rtype: list
    """
    
    # get all commits reachable from "HEAD"
    commits = list(repo.iter_commits('HEAD'))
    return commits

def commit_per_period(repo, period):
    """
    Calculate number of commits for a repository in a period

    :param repo: repository to analyze
    :type repo: Repo
    :param period: period to calculate commits from
    :type period: string
    :return: number of commits in given period
    :rtype: float
    """
    date_list = list()
    commits = get_commits(repo)
    for commit in commits:
        date = commit.commited_date
        date = datetime.fromtimestamp(date)
        date = datetime.strftime(DATETIME_FORMAT, date)
        date = datetime.strptime(date, DATETIME_FORMAT)
        date_list.append(date)
    print(date_list)
    first_commit = date_list[0]
    first_commit = datetime.strptime(first_commit, DATETIME_FORMAT)
    last_commit = date_list[-1]
    last_commit = datetime.strptime(last_commit, DATETIME_FORMAT)
    now = datetime.now()
    no_commits = len(commits)

    if period == 'week':
        monday1 = (first_commit - timedelta(days=first_commit.weekday()))
        monday2 = (now - timedelta(days=now.weekday()))
        weeks = (monday2 - monday1).days / 7
        commits_per_weeks = weeks/no_commits
        return commits_per_weeks
    if period == 'month':
        months = (now.year - first_commit.year) * 12 + (now.month - first_commit.month)
        commits_per_month = months/no_commits
        return commits_per_month

result = commit_per_period(repo, 'week')
print(result)