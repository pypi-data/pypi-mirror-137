# SPDX-FileCopyrightText: 2022 Joshua Mulliken <joshua@mulliken.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later
from jinja2 import Environment, DictLoader

DEFAULT_CONFIG = """# This is the default configuration file for the task importer.
# The following settings are required:
[DEFAULT]
# Acceptable values for the 'task_manager' setting are: things3, omnifocus3
task_manager=things3

# The following settings are examples of services that can be imported.
# You can add as many services as you want.
; [Work Jira]
; service=jira
; server=https://jira.example.com
; api_token=<ACCESS_TOKEN>
; project=<PROJECT_KEY>
 
; [Work Github]
; service=github
; repo=<REPO_NAME>
; api_token=<ACCESS_TOKEN>
; project=<PROJECT_KEY>

; [Work Gitlab]
; service=gitlab
; gitlab_instance=<INSTANCE>
; repo=<REPO_NAME>
; api_token=<ACCESS_TOKEN>
; project=<PROJECT_KEY>
"""

JINJA_TEMPLATE_DICT = {
    "things3_add_todo.applescript": """
tell application "Things3"
    if "{{ todo_name }}" is not in (name of every to do in project "{{ things_project }}") then
        set TheTodo to (make to do at project "{{ things_project }}")
        set name of TheTodo to "{{ todo_name }}"
        set notes of TheTodo to "{{ todo_url }}"
        {% if todo_due_date %}
        set due date of TheTodo to date "{{ todo_due_date.strftime('%b %d %Y') }}"
        {% endif %}
    end if
end tell
""",
    "omnifocus3_add_todo.applescript": """
tell front document of application "OmniFocus"
    set ExistingProject to false
    set theProjects to every flattened project where its completed = false
    repeat with a from 1 to length of theProjects
        set currentProj to item a of theProjects
        set nameProj to name of currentProj
        if "{{ omnifocus_project }}" = nameProj then
            set ExistingProject to true
            set UseProject to currentProj
        end if
    end repeat

    if not ExistingProject then
        set UseProject to make new project with properties {{ '{{' }}name:"{{ omnifocus_project }}", singleton action holder:true{{ '}}' }}
    end if
    if "{{ todo_name }}" is not in (name of every flattened task of currentProj where its completed = false) then
        tell UseProject
            set theTask to make new task with properties {{ '{{' }}name:"{{ todo_name }}", note:"{{ todo_url }}"{{ '}}' }}
        end tell
    end if
end tell
"""  # TODO: Add due date to omnifocus3_add_todo.applescript @vincent
}

JINJA_TEMPLATE_ENV = Environment(loader=DictLoader(JINJA_TEMPLATE_DICT))
