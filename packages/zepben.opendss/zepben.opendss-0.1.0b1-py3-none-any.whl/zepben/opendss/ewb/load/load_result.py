#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass
from typing import List

__all__ = [
    "LoadValues",
    "LoadReading",
    "EnergyObject",
    "SeriesObject",
    "LoadAsset",
    "LoadResult",
]


@dataclass
class LoadValues:
    kw_in: float
    kw_out: float
    kw_net: float
    pf: float
    kva_net: float

    @staticmethod
    def from_json(json) -> 'LoadValues':
        return LoadValues(
            kw_in=json["kwIn"],
            kw_out=json["kwOut"],
            kw_net=json["kwNet"],
            pf=json["pf"],
            kva_net=json["kvaNet"]
        )


@dataclass
class LoadReading:
    time: str
    values: LoadValues

    @staticmethod
    def from_json(json) -> 'LoadReading':
        return LoadReading(
            time=json["time"],
            values=LoadValues.from_json(json["values"])
        )


@dataclass
class EnergyObject:
    date: str
    missing_load_ids: List[str]
    maximums: LoadValues
    readings: List[LoadReading]

    @staticmethod
    def from_json(json) -> 'EnergyObject':
        return EnergyObject(
            date=json["date"],
            missing_load_ids=json["missingLoadIds"],
            maximums=LoadValues.from_json(json["maximums"]),
            readings=[LoadReading.from_json(r) for r in json["readings"]]
        )


@dataclass
class SeriesObject:
    energy: EnergyObject

    @staticmethod
    def from_json(json) -> 'EnergyObject':
        return EnergyObject.from_json(json["energy"])


@dataclass
class LoadAsset:
    id: str
    name: str
    system_tag: str

    @staticmethod
    def from_json(json) -> 'LoadAsset':
        return LoadAsset(
            id=json["id"],
            name=json["name"],
            system_tag=json["systemTag"]
        )


@dataclass
class LoadResult:
    system_tag: str
    from_asset: LoadAsset
    to_asset: LoadAsset
    load_ids: List[str]
    voltage: int
    rating: float
    series: List[List[EnergyObject]]

    @staticmethod
    def from_json(json) -> 'LoadResult':
        return LoadResult(
            system_tag=json["systemTag"],
            from_asset=LoadAsset.from_json(json["fromAsset"]),
            to_asset=LoadAsset.from_json(json["toAsset"]),
            load_ids=json["loadIds"],
            voltage=json["voltage"],
            rating=json["rating"],
            series=[[SeriesObject.from_json(si) for si in s] for s in json["series"]]
        )
