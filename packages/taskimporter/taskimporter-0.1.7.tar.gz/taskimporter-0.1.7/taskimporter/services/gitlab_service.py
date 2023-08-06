# SPDX-FileCopyrightText: 2022 Joshua Mulliken <joshua@mulliken.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from typing import List

from taskimporter import Task
from taskimporter.services.base_service import BaseService
from gitlab import Gitlab


class GitlabService(BaseService):
    service_type = "gitlab"
    config_keys = ["gitlab_instance", "repo", "api_token"]

    def __init__(self, gitlab_instance, repo, api_token, project_key):
        """
        GitlabService constructor. Reads the config from the keys defined in config_keys.
        Any other implementations of BaseService should include the project_key as the last argument.

        :param gitlab_instance: The gitlab instance to use.
        :param repo:
        :param api_token:
        :param project_key:
        """

        self._gitlab = Gitlab(gitlab_instance, private_token=api_token)
        self._gitlab.auth()
        self._repo_name = repo
        self._repo = self._gitlab.projects.get(repo)

        self.name = "GitLab: %s" % repo
        self.project_key = project_key

    def get_tasks(self) -> List[Task]:
        issues = self._repo.issues.list(state='opened')
        merge_requests = self._repo.mergerequests.list(state='opened')

        tasks = []
        for issue in issues:
            task = Task()
            task.name = "[Issue] %s" % issue.title
            task.url = issue.web_url

            tasks.append(task)

        for merge_request in merge_requests:
            task = Task()
            task.name = "[Pull Request] %s" % merge_request.title
            task.url = merge_request.web_url

            tasks.append(task)

        return tasks
