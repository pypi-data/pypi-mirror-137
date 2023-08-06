#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from zepben.opendss.model.bus import Bus

__all__ = ["Load"]


class Load:

    def __init__(
            self,
            uid: str,
            bus1: Bus,
            kv: float,
            kw: float,
            kvar: float,
            phases: int,
            # Minimum per unit voltage for which the MODEL is assumed to apply.
            # Below this value, the load model reverts to a constant impedance model.
            v_min_pu: float = 0.95,
            # Maximum per unit voltage for which the MODEL is assumed to apply.
            # Above this value, the load model reverts to a constant impedance model.
            v_max_pu: float = 1.05,
    ):
        self.uid = uid
        self.bus1 = bus1
        self.kv = kv
        self.kw = kw
        self.kvar = kvar
        self.phases = phases
        self.v_min_pu = v_min_pu
        self.v_max_pu = v_max_pu
