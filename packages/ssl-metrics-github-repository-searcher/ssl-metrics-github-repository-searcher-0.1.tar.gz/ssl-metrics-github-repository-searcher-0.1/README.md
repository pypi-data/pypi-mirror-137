# Software Systems Laboratory GitHub Repository Searcher

> A utility to perform advanced searching on GitHub using both the REST and GraphQL APIs

![[https://img.shields.io/badge/python-3.9.6%20%7C%203.10-blue](https://img.shields.io/badge/python-3.9.6%20%7C%203.10-blue)](https://img.shields.io/badge/python-3.9.6%20%7C%203.10-blue)
![[https://img.shields.io/badge/DOI-Example-red](https://img.shields.io/badge/DOI-Example-red)](https://img.shields.io/badge/DOI-Example-red)
![[https://img.shields.io/badge/build-Example-red](https://img.shields.io/badge/build-Example-red)](https://img.shields.io/badge/build-Example-red)
![[https://img.shields.io/badge/license-BSD--3-yellow](https://img.shields.io/badge/license-BSD--3-yellow)](https://img.shields.io/badge/license-BSD--3-yellow)

## Table of Contents

- [Software Systems Laboratory GitHub Repository Searcher](#software-systems-laboratory-github-repository-searcher)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [Developer Tooling](#developer-tooling)
    - [Operating System](#operating-system)
    - [Python Software](#python-software)
  - [How To Use](#how-to-use)
    - [Installation](#installation)
    - [Command Line Arguements](#command-line-arguements)

## About

The Software Systems Laboratory (SSL) GitHub Repository Searcher is an installable Python project that utilizes both the GitHub REST and GraphQL APIs to allow for the advanced searching of repositories hosted on GitHub.

This project is licensed under the BSD-3-Clause. See the [LICENSE](LICENSE) for more information.

## Developer Tooling

To maximize the utility of this project the following software packages are **required**:

### Operating System

This tool **targets** Mac OS and Linux. SSL Metrics software is not supported or recommended to run on Windows *but can be modified to do so at your own risk*.

It is recomendded to run this tool on Mac OS or Linux. However, if you are on a Windows machine, you can use WSL to develop as well.

### Python Software

> The software listed in this section is meant for developing tools

All listed Python software assumes that you have downloaded and installed **Python 3.9.6** or greater.

- `pandas`
- `progress`
- `requests`

You can install all of the Python software with one of the following one-liners:

- `pip install --upgrade pandas pip progress requests`
- `pip install --upgrade pip -r requirements.txt`

## How To Use

### Installation

You can install the tool from PyPi with one of the following one liners:

- `pip install ssl-metrics-meta`
- `pip install ssl-metrics-github-repository-searcher`

### Command Line Arguements

`ssl-metrics-github-repository-searcher-search -h`

```shell
options:
  -h, --help            show this help message and exit
  -r REPOSITORY, --repository REPOSITORY
                        A specific repository to be analyzed. Must be in format OWNER/REPO
  --topic TOPIC         Topic to scrape (up to) the top 1000 repositories from
  -o OUTPUT, --output OUTPUT
                        JSON file to dump data to
  -t TOKEN, --token TOKEN
                        GitHub personal access token
  --min-stars MIN_STARS
                        Minimum number of stars a repository must have
  --max-stars MAX_STARS
                        Maximum number of stars a repository must have
  --min-commits MIN_COMMITS
                        Minimum number of commits a repository must have
  --max-commits MAX_COMMITS
                        Maximum number of commits a repository must have
  --min-issues MIN_ISSUES
                        Minimum number of issues a repository must have
  --max-issues MAX_ISSUES
                        Maximum number of issues a repository must have
  --min-pull-requests MIN_PULL_REQUESTS
                        Minimum number of pull requests a repository must have
  --max-pull-requests MAX_PULL_REQUESTS
                        Maximum number of pull requests a repository must have
  --min-forks MIN_FORKS
                        Minimum number of forks a repository must have
  --max-forks MAX_FORKS
                        Maximum number of forks a repository must have
  --min-watchers MIN_WATCHERS
                        Minimum number of watchers a repository must have
  --max-watchers MAX_WATCHERS
                        Maximum number of watchers a repository must have
  --min-created-date MIN_CREATED_DATE
                        Minimum date of creation a repository must have
  --max-created-date MAX_CREATED_DATE
                        Maximum date of creation a repository must have
  --min-pushed-date MIN_PUSHED_DATE
                        Minimum date of the latest push a repository must have
  --max-pushed-date MAX_PUSHED_DATE
                        Maximum date of the latest push a repository must have
```
