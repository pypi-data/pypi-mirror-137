# SPDX-FileCopyrightText: 2022 Joshua Mulliken <joshua@mulliken.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later

from abc import abstractmethod, ABC
from typing import List

from taskimporter import Task


class BaseService(ABC):
    service_type: str
    name: str
    project_key: str

    @property
    @abstractmethod
    def service_type(self) -> str:
        pass

    @property
    @abstractmethod
    def config_keys(self) -> List[str]:
        pass

    @abstractmethod
    def get_tasks(self) -> List[Task]:
        pass
