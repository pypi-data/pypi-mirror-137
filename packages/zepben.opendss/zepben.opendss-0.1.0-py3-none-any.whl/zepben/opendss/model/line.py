#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.opendss.model.bus import Bus

__all__ = ["Line"]


class Line:

    def __init__(
            self,
            uid: str,
            units: str,
            length: float,
            bus1: Bus,
            bus2: Bus,
            line_code_uid: str
    ):
        self.uid = uid
        self.units = units
        self.length = length
        self.bus1 = bus1
        self.bus2 = bus2
        self.line_code_uid = line_code_uid
