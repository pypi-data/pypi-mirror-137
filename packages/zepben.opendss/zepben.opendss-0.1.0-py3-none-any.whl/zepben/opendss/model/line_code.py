#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["LineCode"]

class LineCode:

    def __init__(
            self,
            uid: str,
            units: str,
            nphases: int,
            r1: float,
            r0: float,
            x1: float,
            x0: float,
            c1: float,
            c0: float
    ):
        self.uid = uid
        self.units = units
        self.nphases = nphases
        self.r1 = r1
        self.r0 = r0
        self.x1 = x1
        self.x0 = x0
        self.c1 = c1
        self.c0 = c0
