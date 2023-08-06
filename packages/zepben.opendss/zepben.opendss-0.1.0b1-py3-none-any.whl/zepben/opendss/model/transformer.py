#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import List

__all__ = ["TransformerWinding", "Transformer"]


class TransformerWinding:

    def __init__(
            self,
            conn: str,
            kv: float,
            kva: float,
            bus_uid: str
    ):
        self.conn = conn
        self.kv = kv
        self.kva = kva
        self.bus_uid = bus_uid


class Transformer:

    def __init__(
            self,
            uid: str,
            phases: int,
            load_loss_percent: float,
            windings: List[TransformerWinding]
    ):
        self.uid = uid
        self.phases = phases
        self.load_loss_percent = load_loss_percent
        self.windings = windings
