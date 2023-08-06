#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["Monitor"]


class Monitor:

    def __init__(
            self,
            uid: str,
            element: str,
            term: int = 1,
            option: str = 'R',
            action: str = 'C',
            phasevolt: str = 'Yes'

    ):
        self.uid = uid
        self.element = element
        self.term = term
        self.option = option
        self.action = action
        self.phasevolt = phasevolt

