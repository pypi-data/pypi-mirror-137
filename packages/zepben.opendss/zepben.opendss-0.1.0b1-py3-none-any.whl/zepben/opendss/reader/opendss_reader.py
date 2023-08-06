#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
from typing import Dict, Any, TextIO

from dataclassy import dataclass

from zepben.opendss import Circuit, DssType, Line, LineCode, Load, Master, Transformer, TransformerWinding

logger = logging.getLogger(__name__)

__all__ = ["BaseDSSReader"]


def line(fields: Dict[str, Any]) -> Line:
    return Line(fields["id"],
                fields["units"],
                float(fields["length"]),
                fields["bus1"],
                fields["bus2"],
                int(fields["phases"]),
                fields["linecode"])


def line_code(fields: Dict[str, Any]) -> LineCode:
    r0 = convert_val(fields["r0"])
    x0 = convert_val(fields["x0"])
    r1 = convert_val(fields["r1"])
    x1 = convert_val(fields["x1"])
    return LineCode(fields["id"],
                    fields["units"],
                    r1,
                    r0,
                    x1,
                    x0)


def convert_val(val: str) -> float:
    # TODO: Fix this to do the right thing for values like: 4 0.102 *
    try:
        return float(val)
    except:
        s = val.split()
        return float(s[0]) * float(s[1])


def load(fields: Dict[str, Any]) -> Load:
    return Load(fields["id"],
                fields["bus1"],
                float(fields["kv"]),
                float(fields["kw"]),
                float(fields["kvar"]),
                int(fields["phases"]),
                float(fields["vminpu"]),
                float(fields["vmaxpu"]))


def transformer(fields: Dict[str, Any], windings: Dict[int, Dict[str, Any]]) -> Transformer:
    transformer_windings = []
    for i, winding in windings.items():
        transformer_windings.append(TransformerWinding(winding["conn"], winding["kv"], winding["kva"], winding["bus"]))

    return Transformer(fields["id"],
                       fields["phases"],
                       fields["%loadloss"],
                       transformer_windings)


def circuit(fields: Dict[str, Any]) -> Circuit:
    return Circuit(fields["id"],
                   fields["bus1"],
                   fields["pu"],
                   fields["base_kv"])


type_map = {
    DssType.line: line,
    DssType.linecode: line_code,
    DssType.load: load,
    DssType.transformer: transformer,
    DssType.circuit: circuit,
}


@dataclass(slots=True)
class BaseDSSReader(object):
    master: Master = Master()

    def read_file(self, file: TextIO):
        for line in file:
            self.process_line(line)

    def process_line(self, line: str):
        keyed_values = line.split()

        if not line or line.startswith('!'):
            return

        fields = dict()
        windings = dict()

        reader = None
        dss_type = None
        winding = None
        grouped_vals = []
        grouped_key = None
        stop_processing_group = False
        for kv in keyed_values:
            s = kv.split(sep='=', maxsplit=1)

            # If we've started a group process it.
            if grouped_vals:
                if not stop_processing_group:
                    grouped_vals.append(kv)
                    if kv.endswith(')'):
                        stop_processing_group = True
                        grouped = ' '.join(grouped_vals).lstrip('(').rstrip(')')
                        fields[grouped_key.casefold()] = grouped
                        grouped_key = None
                        grouped_vals = []
                        stop_processing_group = False
                        continue
                    continue

            if s[0].casefold() == 'wdg':
                winding = s[1]
                windings[winding] = dict()
            elif len(s) > 1:
                # Deal with parenthesis grouped results e.g (3.02 4.75 *)
                if s[1].startswith('('):
                    grouped_key = s[0]
                    grouped_vals.append(s[1])
                    continue

                if winding is not None:
                    windings[winding][s[0].casefold()] = s[1]
                else:
                    # lowercase all keys
                    fields[s[0].casefold()] = s[1]
            else:
                if s[0].casefold() == 'new':
                    continue  # TODO: Are other things required here?
                s2 = s[0].split(sep='.', maxsplit=1)
                # Skip fields with no . or = seperators
                if len(s2) < 2:
                    continue
                try:
                    dss_type = DssType[s2[0].casefold()]
                except KeyError as ke:
                    logger.debug(f"Could not process type {s2[0]} - line in file was: {line}")
                    continue
                reader = type_map[dss_type]
                fields["id"] = s2[1]

        if dss_type is None:
            logger.warning(f"No type was detected for line: {line}")
            return

        if reader is None:
            logger.warning(f"Could not handle line: {line}")
            return

        if not fields:
            logger.warning(f"Fields could not be processed for line: {line}")
            return

        try:
            if dss_type == DssType.line:
                self.master.add_line(reader(fields))
            elif dss_type == DssType.load:
                self.master.add_load(reader(fields))
            elif dss_type == DssType.linecode:
                self.master.add_line_code(reader(fields))
            elif dss_type == DssType.transformer:
                # noinspection PyTypeChecker
                self.master.add_transformer(reader(fields, windings))
            elif dss_type == DssType.circuit:
                self.master.set_circuit(reader(fields))
            else:
                raise ValueError(f"Unhandled type {dss_type}")

        except Exception as e:
            raise e

    def read_line(self) -> Line:
        pass
