# SPDX-FileCopyrightText: 2022 Joshua Mulliken <joshua@mulliken.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import configparser
import os
import argparse
from appdirs import user_data_dir

from taskimporter import const
from taskimporter.task import Task
from taskimporter.services import services
from taskimporter.task_managers import task_managers


def configure_services(config, user_services):
    s_list = []

    for service in user_services:
        service_name = config[service]['service']
        if service_name in services:
            service_cls = services[service_name]

            service_config = {}

            for key in service_cls.config_keys:
                if key in config[service]:
                    service_config[key] = config[service][key]

            service_config["project_key"] = config[service]['project']

            print(service_config)

            s_list.append(service_cls(**service_config))
        else:
            print("Invalid service: %s" % service_name)

    return s_list


def main():
    parser = argparse.ArgumentParser(description='Import tasks from various services')
    parser.add_argument('-c', '--config', help='Path to configuration file')
    parser.add_argument('-w', '--write', help='Write default config', action='store_true')
    args = parser.parse_args()

    config_path = user_data_dir('taskimporter', 'Joshua Mulliken') + '/config.ini'

    if args.config:
        config_path = args.config

    os.makedirs(os.path.dirname(config_path), exist_ok=True)

    if args.write:
        with open(config_path, 'w') as f:
            f.write(const.DEFAULT_CONFIG)

            print('Default config written to \"{}\"'.format(config_path))
            print('Please edit the config file and run again')
            exit(0)

    config = configparser.ConfigParser()

    task_manager = ""
    user_services = []

    try:
        config.read(config_path)
        task_manager = config['DEFAULT']['task_manager']
        user_services = [section for section in config.sections() if section != 'DEFAULT']
    except KeyError:
        print('Invalid config file')
        print('Please run with --write to create a default config file')
        print('Config file path: \"{}\"'.format(config_path))
        exit(1)

    if len(user_services) == 0:
        print("No services configured. Please add a service to the config file and run again")
        print("Config location: \"{}\"".format(config_path))
        exit(0)

    for service in configure_services(config, user_services):
        print("Refreshing tasks from %s" % service.name)
        for tsk in service.get_tasks():
            print("Adding task: %s" % tsk.name)
            if task_manager in task_managers:
                task_managers[task_manager].add_task(tsk, project=service.project_key)


if __name__ == "__main__":
    main()
