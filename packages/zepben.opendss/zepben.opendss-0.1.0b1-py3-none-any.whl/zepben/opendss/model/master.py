#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from typing import Tuple, Optional, Dict

from zepben.opendss import Circuit, Line, LineCode, Transformer, Load
from zepben.opendss.model.bus import Bus
from zepben.opendss.model.monitor import Monitor

__all__ = ["Master"]


class Master:

    def __init__(
            self,
            default_base_frequency: int = 50,
            voltage_bases: Tuple[float, float] = None,
            circuit: Optional[Circuit] = None,
            buses: Dict[str, Bus] = None,
            lines: Dict[str, Line] = None,
            line_codes: Dict[str, LineCode] = None,
            transformers: Dict[str, Transformer] = None,
            loads: Dict[str, Load] = None,
            monitors: Dict[str, Monitor] = None
    ):
        self.default_base_frequency = default_base_frequency
        self.voltage_bases = voltage_bases
        self.circuit = circuit
        self.buses = {} if buses is None else buses
        self.lines = {} if lines is None else lines
        self.line_codes = {} if line_codes is None else line_codes
        self.transformers = {} if transformers is None else transformers
        self.loads = {} if loads is None else loads
        self.monitors = {} if monitors is None else monitors

    def set_default_base_frequency(self, default_base_frequency: int):
        self.default_base_frequency = default_base_frequency

    def set_voltage_bases(self, voltage_bases: Tuple[float, float]):
        self.voltage_bases = voltage_bases

    def set_circuit(self, circuit: Optional[Circuit] = None):
        self.circuit = circuit

    def add_bus(self, bus: Bus):
        self.buses[bus.uid] = bus

    def add_line(self, line: Line):
        self.lines[line.uid] = line

    def add_line_code(self, line_code: LineCode):
        self.line_codes[line_code.uid] = line_code

    def add_transformer(self, transformer: Transformer):
        self.transformers[transformer.uid] = transformer

    def add_load(self, load: Load):
        self.loads[load.uid] = load

    def remove_line(self, uid: str):
        del self.lines[uid]

    def remove_line_code(self, uid: str):
        del self.line_codes[uid]

    def remove_transformer(self, uid: str):
        del self.transformers[uid]

    def remove_load(self, uid: str):
        del self.loads[uid]

    def copy(self):
        raise NotImplementedError("Copy method is not implemented")
