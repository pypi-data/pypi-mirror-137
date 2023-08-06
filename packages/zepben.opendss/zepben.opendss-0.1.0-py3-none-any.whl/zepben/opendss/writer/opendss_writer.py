#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from math import sqrt
from pathlib import Path
from typing import Callable
from typing import TypeVar, List
import aiofiles as aiof
import os.path

from zepben.opendss import Line, LineCode, Load, Master, Monitor, Transformer, TransformerWinding

__all__ = ["OpenDssWriter"]

from zepben.opendss.model.bus import Bus


class OpenDssWriter:

    @staticmethod
    async def write(dir_path_str: str, master: Master, default_load: int = None):
        model_dir = Path(dir_path_str)

        if not os.path.exists(model_dir):
            os.makedirs(model_dir)

        if not model_dir.is_dir():
            raise ValueError(f"The argument '{dir_path_str}' for the dir_path_str parameter was not a directory")

        await OpenDssWriter.write_lines_file(model_dir, master)
        await OpenDssWriter.write_line_codes_file(model_dir, master)
        await OpenDssWriter.write_loads_file(model_dir, master, default_load)
        await OpenDssWriter.write_transformers_file(model_dir, master)
        await OpenDssWriter.write_monitor_file(model_dir, master)
        await OpenDssWriter.write_master_file(model_dir, master, default_load)

    @staticmethod
    async def write_lines_file(model_dir: Path, master: Master):
        await OpenDssWriter.write_elements_to_file(
            model_dir / 'Lines.dss',
            master,
            lambda m: m.lines.values(),
            OpenDssWriter.line_to_str
        )

    @staticmethod
    async def write_line_codes_file(model_dir: Path, master: Master):
        await OpenDssWriter.write_elements_to_file(
            model_dir / 'LineCodes.dss',
            master,
            lambda m: m.line_codes.values(),
            OpenDssWriter.line_code_to_str
        )

    @staticmethod
    async def write_loads_file(model_dir: Path, master: Master, default_load: int = None):
        await OpenDssWriter.write_elements_to_file(
            model_dir / 'Loads.dss',
            master,
            lambda m: m.loads.values(),
            OpenDssWriter.load_to_str,
            default_load
        )

    @staticmethod
    async def write_monitor_file(model_dir: Path, master: Master):
        await OpenDssWriter.write_elements_to_file(
            model_dir / 'Monitors.dss',
            master,
            lambda m: m.monitors.values(),
            OpenDssWriter.monitor_to_str
        )

    @staticmethod
    async def write_transformers_file(model_dir: Path, master: Master):
        await OpenDssWriter.write_elements_to_file(
            model_dir / 'Transformers.dss',
            master,
            lambda m: m.transformers.values(),
            OpenDssWriter.transformer_to_str
        )

    @staticmethod
    async def write_master_file(model_dir: Path, master: Master, default_load: int = None):
        async with aiof.open((model_dir / 'Master.dss'), 'w') as file:
            await file.write(OpenDssWriter.master_to_str(master, default_load))

    T = TypeVar('T')

    # noinspection PyArgumentList
    @staticmethod
    async def write_elements_to_file(file_path: Path, master: Master, elements_provider: Callable[[Master], List[T]],
                                     to_str: Callable[[T], str], default_load: int = None):
        async with aiof.open(str(file_path), 'w') as file:
            for element in elements_provider(master):
                # Load file and master file can take default_load
                await file.write((to_str(element, default_load) + "\n") if default_load else (to_str(element) + "\n"))
            await file.flush()

    @staticmethod
    def bus_to_str(bus: Bus) -> str:
        return f"{bus.uid}.{'.'.join(sorted(str(n.value) for n in bus.nodes))}"

    @staticmethod
    def line_to_str(line: Line) -> str:
        return f"New Line.{line.uid} " \
               f"Units={line.units} " \
               f"Length={line.length} " \
               f"bus1={OpenDssWriter.bus_to_str(line.bus1)} bus2={OpenDssWriter.bus_to_str(line.bus2)} " \
               f"Linecode={line.line_code_uid}"

    @staticmethod
    def line_code_to_str(line_code: LineCode) -> str:
        return f"New Linecode.{line_code.uid} " \
               f"units={line_code.units} " \
               f"nphases={line_code.nphases} " \
               f"R1={line_code.r1} R0={line_code.r0 or line_code.r1} " \
               f"X1={line_code.x1} X0={line_code.x0 or line_code.x1} " \
               f"C1={line_code.c1} C0={line_code.c0 or line_code.c1}"

    @staticmethod
    def load_to_str(load: Load, default_load: int = None) -> str:
        s = sqrt(load.kw ** 2.0 + load.kvar ** 2.0)
        pf = 1.0 if s == load.kw or s == 0.0 else load.kw / s
        kv = round(load.kv / sqrt(3) if len(load.bus1.nodes) == 1 else load.kv, 3)

        if default_load:
            return f"New Load.{load.uid} bus1={load.bus1} kV={kv} Vminpu={load.v_min_pu} Vmaxpu={load.v_max_pu} model=1 kW={default_load} PF={pf} Phases={load.phases}"
        else:
            # Commenting out PEC entries but keeping them in file
            if 'pec' in load.uid:
                return f"!New Load.{load.uid} bus1={OpenDssWriter.bus_to_str(load.bus1)} kV={kv} Vminpu={load.v_min_pu} Vmaxpu={load.v_max_pu} model=1 kW={load.kw} PF={pf} yearly=LS_{load.uid} Phases={load.phases}"
            else:
                return f"New Load.{load.uid} bus1={OpenDssWriter.bus_to_str(load.bus1)} kV={kv} Vminpu={load.v_min_pu} Vmaxpu={load.v_max_pu} model=1 kW={load.kw} PF={pf} yearly=LS_{load.uid} Phases={load.phases}"

    @staticmethod
    def monitor_to_str(monitor: Monitor) -> str:
        return f"New energymeter.{monitor.uid} element={monitor.element} term={monitor.term} option={monitor.option} action={monitor.action} PhaseVolt={monitor.phasevolt}"

    @staticmethod
    def transformer_to_str(transformer: Transformer) -> str:
        return f"New Transformer.{transformer.uid} phases={transformer.phases} windings={len(transformer.windings)} %loadloss={transformer.load_loss_percent} " \
               + " ".join(OpenDssWriter.t_winding_to_str(tw, index + 1)
                          for index, tw in enumerate(sorted(transformer.windings, key=lambda w: w.kv, reverse=True)))

    @staticmethod
    def t_winding_to_str(t_winding: TransformerWinding, w_number: int) -> str:
        return f"wdg={w_number} conn={t_winding.conn} Kv={t_winding.kv} kva={t_winding.kva} bus={t_winding.bus_uid}"  # TODO PROJ-1785: How do we handle 0.0 kva? this was not a problem with pandapower but causes issues with opendss

    @staticmethod
    def master_to_str(master: Master, default_load: int = None) -> str:
        load_shape = ''
        if not default_load:
            for load in master.loads:
                if 'pec' in load:
                    pass
                else:
                    load_shape = load_shape + f"New Loadshape.LS_{load} npts=17568 interval=0.5 mult=(file={load}.txt) action=normalize\n"
        return (
                "Clear\n" +
                "\n" +
                f"set defaultbasefreq={master.default_base_frequency}\n" +
                "\n" +
                f"New Circuit.{master.circuit.uid}  bus1={master.circuit.bus1_uid} pu={master.circuit.pu} basekV={master.circuit.base_kv} phases={master.circuit.phases}\n" +
                "\n" +
                f"{load_shape}"
                "\n" +
                f"{load_shape}"
                "\n" +
                "Redirect LineCodes.dss\n" +
                "Redirect Lines.dss\n" +
                "Redirect Transformers.dss\n" +
                "Redirect Loads.dss\n" +
                "Redirect Monitors.dss\n" +
                "\n" +
                f"Set Voltagebases=[{master.voltage_bases[0]}, {master.voltage_bases[1]}]\n" +
                "set defaultbasefreq=50\n" +
                "\n" +
                "Calcvoltagebases\n" +
                "\n" +
                "Set overloadreport=true\t! TURN OVERLOAD REPORT ON\n" +
                "Set voltexcept=true\t! voltage exception report\n" +
                "Set demand=true\t! demand interval ON\n" +
                "Set DIVerbose=true\t! verbose mode is ON\n" +
                "set mode=yearly\n"
                "\n" +
                "Solve" +
                "\n" +
                "Export meter !exports a single csv file named _EXP_METERS for all meters with a row per meter per year\n" +
                "Export Voltages\n" +
                "Export Currents\n" +
                "Export Powers\n" +
                "CloseDI\n"
        )
