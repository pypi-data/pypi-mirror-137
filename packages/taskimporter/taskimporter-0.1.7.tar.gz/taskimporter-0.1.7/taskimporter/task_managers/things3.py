# SPDX-FileCopyrightText: 2022 Joshua Mulliken <joshua@mulliken.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from subprocess import Popen, PIPE

from taskimporter import Task
from taskimporter.const import JINJA_TEMPLATE_ENV
from taskimporter.task_managers import BaseTaskManager

THINGS_PROJECT = "Default Project"
THINGS_TEMPLATE = JINJA_TEMPLATE_ENV.get_template("things3_add_todo.applescript")


class Things3(BaseTaskManager):
    name = "things3"

    @staticmethod
    def add_task(task: Task, project=THINGS_PROJECT):
        things_script = THINGS_TEMPLATE.render(
            todo_name=task.name,
            todo_url=task.url,
            things_project=project,
            todo_due_date=task.due_date)

        with Popen(['osascript', '-'], stdin=PIPE) as proc:
            proc.stdin.write(things_script.encode('utf-8'))
            proc.stdin.close()
            proc.wait()
