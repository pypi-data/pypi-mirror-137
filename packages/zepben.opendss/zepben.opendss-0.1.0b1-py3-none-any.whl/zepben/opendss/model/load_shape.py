#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

__all__ = ["LoadShape"]


class LoadShape:
    values: List[float] = []

    def __init__(self, values: List[float] = None):
        if values is None:
            values = []
        self.values = values
