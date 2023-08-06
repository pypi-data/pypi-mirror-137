#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import logging
from typing import FrozenSet, Tuple, List, Optional, Callable, Dict, Collection

from zepben.evolve import Terminal, NetworkService, AcLineSegment, PowerTransformer, EnergyConsumer, \
    PowerTransformerEnd, ConductingEquipment, PowerElectronicsConnection, BusBranchNetworkCreator, EnergySource, Switch, Junction, BusbarSection, \
    PerLengthSequenceImpedance, BaseVoltage, \
    EquivalentBranch, IdentifiedObject
from zepben.opendss import LineCode, Circuit, Line, Load, Master, Transformer, TransformerWinding, Bus
from zepben.opendss.creators.utils import transformer_end_connection_mapper, id_from_identified_objects, get_bus_nodes

from zepben.opendss import LineCode, Circuit, Line, Load, Master, Monitor, Transformer, TransformerWinding
from zepben.opendss.creators.validators.validator import OpenDssNetworkValidator

__all__ = ["OpenDssNetworkCreator", "id_from_identified_objects"]


# TODO: Should this be used from utils? why is this also here? Only difference is sorting mrids
def id_from_identified_objects(ios: Collection[IdentifiedObject], separator: str = "__"):
    return separator.join(io.mrid for io in ios)


class OpenDssNetworkCreator(
    BusBranchNetworkCreator[Master, Bus, Line, Line, Transformer, Circuit, Load, Load, OpenDssNetworkValidator]
):

    def __init__(
            self, *,
            logger: logging.Logger,
            vm_pu: float = 1.0,
            load_provider: Callable[[ConductingEquipment], Tuple[float, float]] = lambda x: (0, 0),
            pec_load_provider: Callable[[ConductingEquipment], Tuple[float, float]] = lambda x: (0, 0),
            min_line_r_ohm: float = 0.001,
            min_line_x_ohm: float = 0.001
    ):
        # -- input --
        self.vm_pu = vm_pu
        self.logger = logger
        self.load_provider = load_provider
        self.pec_load_provider = pec_load_provider
        self.min_line_r_ohm = min_line_r_ohm
        self.min_line_x_ohm = min_line_x_ohm

    def bus_branch_network_creator(self, node_breaker_network: NetworkService) -> Master:
        nominal_voltages = [bv.nominal_voltage for bv in node_breaker_network.objects(BaseVoltage) if bv.nominal_voltage != 0]
        network = Master(default_base_frequency=50, voltage_bases=(min(nominal_voltages) / 1000.0, max(nominal_voltages) / 1000.0))
        return network

    def topological_node_creator(
            self,
            bus_branch_network: Master,
            base_voltage: Optional[int],
            collapsed_conducting_equipment: FrozenSet[ConductingEquipment],
            border_terminals: FrozenSet[Terminal],
            inner_terminals: FrozenSet[Terminal],
            node_breaker_network: NetworkService
    ) -> Tuple[str, Bus]:
        uid = id_from_identified_objects(border_terminals)
        bus = Bus(uid=uid, nodes=get_bus_nodes(next(iter(border_terminals))))
        bus_branch_network.add_bus(bus)
        return uid, bus

    def topological_branch_creator(
            self,
            bus_branch_network: Master,
            connected_topological_nodes: Tuple[Bus, Bus],
            length: Optional[float],
            collapsed_ac_line_segments: FrozenSet[AcLineSegment],
            border_terminals: FrozenSet[Terminal],
            inner_terminals: FrozenSet[Terminal],
            node_breaker_network: NetworkService
    ) -> Tuple[str, Line]:
        ac_line = next(iter(collapsed_ac_line_segments))
        nphases = len(connected_topological_nodes[0].nodes)
        line_code = self._get_create_line_code(bus_branch_network, ac_line.per_length_sequence_impedance, nphases)
        uid = id_from_identified_objects(collapsed_ac_line_segments)
        line = Line(
            uid=uid,
            units="m",
            length=0.5 if length is None else length,
            bus1=connected_topological_nodes[0],
            bus2=connected_topological_nodes[1],
            line_code_uid=line_code.uid
        )
        bus_branch_network.add_line(line)
        return uid, line

    @staticmethod
    def _get_create_line_code(bus_branch_network: Master, per_length_sequence_impedance: PerLengthSequenceImpedance, nphases: int) -> LineCode:
        uid = f"{per_length_sequence_impedance.mrid}-{nphases}W"
        line_code = bus_branch_network.line_codes.get(uid)
        if line_code is not None:
            return line_code

        line_code = LineCode(
            uid=uid,
            units="m",
            nphases=nphases,
            r1=per_length_sequence_impedance.r,
            r0=per_length_sequence_impedance.r0,
            x1=per_length_sequence_impedance.x,
            x0=per_length_sequence_impedance.x0,
            c1=0.0,
            c0=0.0
        )
        bus_branch_network.add_line_code(line_code)
        return line_code

    def equivalent_branch_creator(self, bus_branch_network: Master, connected_topological_nodes: List[Bus], equivalent_branch: EquivalentBranch,
                                  node_breaker_network: NetworkService) -> Tuple[str, Line]:
        raise RuntimeError(
            f"The creation of EquivalentBranches is not supported by the OpenDssNetworkCreator."
            f" Tried to create EquivalentBranches {equivalent_branch.mrid}.")

    def power_transformer_creator(
            self,
            bus_branch_network: Master,
            power_transformer: PowerTransformer,
            ends_to_topological_nodes: List[Tuple[PowerTransformerEnd, Optional[Bus]]],
            node_breaker_network: NetworkService
    ) -> Dict[str, Transformer]:
        uid = power_transformer.mrid
        num_phases = max([len(get_bus_nodes(end.terminal)) for end, t in ends_to_topological_nodes if end.terminal is not None])
        transformer = Transformer(
            uid=uid,
            phases=num_phases,
            # TODO: What to do when no transformer-end-info
            # load_loss_percent=upstream_end.star_impedance.transformer_end_info.energised_end_short_circuit_tests.voltage_ohmic_part,
            load_loss_percent=0.0,
            # xhl=upstream_end.star_impedance.transformer_end_info.energised_end_short_circuit_tests.voltage, TODO: Investigate how this is represented in output file
            windings=
            [
                TransformerWinding(
                    conn=transformer_end_connection_mapper(end),
                    kv=end.rated_u / 1000.0,
                    kva=(end.rated_s or 234) / 1000.0,
                    bus_uid=f"{power_transformer.mrid}-disc-end-{end.end_number}" if bus is None else bus.uid
                ) for end, bus in ends_to_topological_nodes]
        )

        bus_branch_network.add_transformer(transformer)
        return {uid: transformer}

    def energy_source_creator(
            self,
            bus_branch_network: Master,
            energy_source: EnergySource,
            connected_topological_node: Bus,
            node_breaker_network: NetworkService
    ) -> Dict[str, Circuit]:
        if bus_branch_network.circuit is not None:
            raise RuntimeError("Found multiple EnergySources while trying to create OpenDss model. Only one energy source is supported.")

        uid = energy_source.mrid
        circuit = Circuit(
            uid=uid,
            bus1_uid=connected_topological_node.uid,
            pu=self.vm_pu,
            base_kv=energy_source.base_voltage.nominal_voltage / 1000.0,
            phases=len(connected_topological_node.nodes)
        )

        bus_branch_network.set_circuit(circuit)
        return {uid: circuit}

    def energy_consumer_creator(
            self, bus_branch_network: Master,
            energy_consumer: EnergyConsumer,
            connected_topological_node: Bus,
            node_breaker_network: NetworkService
    ) -> Dict[str, Load]:
        p, q = self.load_provider(energy_consumer)
        uid = energy_consumer.mrid
        load = Load(
            uid=uid,
            bus1=connected_topological_node,
            kv=energy_consumer.base_voltage.nominal_voltage / 1000.0,
            kw=p / 1000.0,
            kvar=q / 1000.0,
            phases=len(connected_topological_node.nodes)
        )

        bus_branch_network.add_load(load)
        return {uid: load}

    def power_electronics_connection_creator(
            self,
            bus_branch_network: Master,
            power_electronics_connection: PowerElectronicsConnection,
            connected_topological_node: Bus,
            node_breaker_network: NetworkService,
    ) -> Dict[str, Load]:
        p, q = self.pec_load_provider(power_electronics_connection)
        uid = power_electronics_connection.mrid
        load = Load(
            uid=uid,
            bus1=connected_topological_node,
            kv=power_electronics_connection.base_voltage.nominal_voltage / 1000.0,
            kw=p / 1000.0,
            kvar=q / 1000.0,
            phases=len(connected_topological_node.nodes)
        )
        bus_branch_network.add_load(load)
        return {uid: load}

    def has_negligible_impedance(self, ce: ConductingEquipment) -> bool:
        if isinstance(ce, AcLineSegment):
            if ce.length == 0 or ce.per_length_sequence_impedance.r == 0:
                return True

            if ce.length * ce.per_length_sequence_impedance.r < self.min_line_r_ohm \
                    or ce.length * ce.per_length_sequence_impedance.x < self.min_line_x_ohm:
                return True

            return False
        if isinstance(ce, Switch):
            return not ce.is_open()
        if isinstance(ce, Junction) or isinstance(ce, BusbarSection) or isinstance(ce, EquivalentBranch):
            return True
        return False

    def validator_creator(self) -> OpenDssNetworkValidator:
        return OpenDssNetworkValidator(logger=self.logger)

    def monitors_creator(self, master: Master):
        for transformer in master.transformers.values():
            for winding in transformer.windings:
                if winding.kv == 0.415:
                    monitor = Monitor(uid=f"{transformer.uid}_em", element=f"Transformer.{transformer.uid}")
                    master.monitors[monitor.uid] = monitor
        return master
