#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from enum import Enum
from typing import Set

__all__ = ["Node", "Bus"]


class Node(Enum):
    A = 1
    B = 2
    C = 3
    N = 4


class Bus:
    uid: str
    nodes: Set[Node]

    def __init__(self, uid: str, nodes: Set[Node]):
        self.uid = uid
        self.nodes = nodes
