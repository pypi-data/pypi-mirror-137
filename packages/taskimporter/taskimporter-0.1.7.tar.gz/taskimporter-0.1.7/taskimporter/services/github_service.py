# SPDX-FileCopyrightText: 2022 Joshua Mulliken <joshua@mulliken.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List

from github import Github

from taskimporter import Task
from taskimporter.services.base_service import BaseService


class GithubService(BaseService):
    service_type = "github"
    config_keys = ["repo", "api_token"]

    def __init__(self, repo, api_token, project_key):
        """
        GithubService constructor. Reads the config from the keys defined in config_keys.
        Any other implementations of BaseService should include the project_key as the last argument.

        :param repo:
        :param api_token:
        :param project_key:
        """
        self._github = Github(api_token)
        self._repo_name = repo
        self._repo = self._github.get_repo(repo)

        self.name = "GitHub: %s" % repo
        self.project_key = project_key

    def get_tasks(self) -> List[Task]:
        issues = self._repo.get_issues(state='open')
        pull_requests = self._repo.get_pulls(state='open')

        tasks = []
        for issue in issues:
            task = Task()
            task.name = "[Issue] %s" % issue.title
            task.url = issue.html_url

            tasks.append(task)

        for pull_request in pull_requests:
            task = Task()
            task.name = "[Pull Request] %s" % pull_request.title
            task.url = pull_request.html_url

            tasks.append(task)

        return tasks
