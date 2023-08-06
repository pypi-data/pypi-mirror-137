#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

__all__ = ["transformer_end_connection_mapper", "id_from_identified_objects", "get_bus_nodes"]

from typing import TypeVar, Collection, Set

from zepben.evolve import PowerTransformerEnd, SinglePhaseKind, WindingConnection, IdentifiedObject, Terminal

from zepben.opendss import Node

T = TypeVar("T")


def transformer_end_connection_mapper(transformer_end: PowerTransformerEnd):
    if transformer_end.connection_kind == WindingConnection.D:
        return "delta"
    elif transformer_end.connection_kind == WindingConnection.Y:
        return "wye"
    else:
        # TODO: There are tons of windings missing here, if we throw for anything other than D and Y then this won't run on anywhere
        return "delta" if transformer_end.end_number == 1 else "wye"
        # raise Exception(f'WindingConnection {transformer_end.connection_kind} is not supported for '
        #                 f'TransformerEnd: {transformer_end.mrid}')


def id_from_identified_objects(ios: Collection[IdentifiedObject], separator: str = "__"):
    return separator.join(sorted(io.mrid for io in ios))


spk_to_node = {
    SinglePhaseKind.A: Node.A,
    SinglePhaseKind.B: Node.B,
    SinglePhaseKind.C: Node.C
}


def get_bus_nodes(t: Terminal) -> Set[Node]:
    return {n for n in {spk_to_node.get(t.traced_phases.phase_normal(sp)) for sp in t.phases.single_phases} if n is not None}
