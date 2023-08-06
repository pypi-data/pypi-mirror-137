# SPDX-FileCopyrightText: 2022 Joshua Mulliken <joshua@mulliken.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from datetime import date

from jira import JIRA
from jira.resources import Issue as JiraIssue

from taskimporter import Task
from taskimporter.services.base_service import BaseService


class JiraService(BaseService):
    service_type = "jira"
    config_keys = ["server", "api_token"]

    def __init__(self, server, api_token, project_key):
        """
        JiraService constructor. Reads the config from the keys defined in config_keys.
        Any other implementations of BaseService should include the project_key as the last argument.

        :param server:
        :param api_token:
        :param project_key:
        """

        self._server = server
        self._jira = JIRA(server=self._server, token_auth=api_token)
        self.name = "Jira: %s" % self._server
        self.project_key = project_key

    def get_tasks(self):
        issues = self._jira.search_issues('assignee = currentUser() AND resolution = Unresolved')

        tasks = []
        issue: JiraIssue
        for issue in issues:
            task = Task()
            task.name = "[%s] %s" % (issue.key, issue.fields.summary)
            task.url = "%s/browse/%s" % (self._server, issue.key)

            if issue.fields.duedate:
                task.due_date = date.fromisoformat(issue.fields.duedate)
                print("We got a due date and it is %s" % task.due_date)

            tasks.append(task)

        return tasks
