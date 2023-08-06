#  Copyright 2022 Zeppelin Bend Pty Ltd
#
#  This Source Code Form is subject to the terms of the Mozilla Public
#  License, v. 2.0. If a copy of the MPL was not distributed with this
#  file, You can obtain one at https://mozilla.org/MPL/2.0/.

import os.path
import sys
from typing import List

import aiofiles as aiof
import aiohttp
from zepben.auth import create_authenticator

from zepben.opendss.ewb.load.load_result import LoadResult

__all__ = ["OpenDssLoadShapeWriter", "load_results_from_json"]


# noinspection PyShadowingNames
def load_results_from_json(json) -> List[LoadResult]:
    return [LoadResult.from_json(r) for r in json["results"]]


class OpenDssLoadShapeWriter:
    def __init__(self, output_dir: str, secure: bool = False, username: str = None, password: str = None,
                 client_id: str = None, host: str = None):
        self.secure = secure
        self.out_dir = output_dir
        if secure:
            authenticator = create_authenticator(f"https://{host}/ewb/auth")
            authenticator.token_request_data.update(
                {
                    "grant_type": "password",
                    "username": username,
                    "password": password,
                    "scope": "offline_access openid profile email",
                    "client_id": client_id
                }
            )
            authenticator.refresh_request_data.update({
                "grant_type": "refresh_token",
                "scope": "offline_access openid profile email",
                "client_id": client_id
            })

            self.token = authenticator.fetch_token()
        else:
            self.token = ''

    async def get_load_profile(self, from_asset: str, from_date: str, to_date: str, host: str, port: int) -> List[LoadResult]:
        async with aiohttp.ClientSession(headers={'Authorization': self.token}, json_serialize=ujson.dumps) as session:
            async with session.get(url=
                                   f'{"https" if self.secure else "http"}://{host}:{port}/ewb/energy/profiles/api/v1/range/{from_asset}'
                                   f'/from-date/{from_date}'
                                   f'/to-date/{to_date}'
                                   ) as response:
                return (await response.json())["results"] if response.status == 200 else []

    @staticmethod
    def create_load_shape(load_profile):
        max_value = sys.float_info.min
        load_shape = []
        try:
            for s in load_profile[0]["series"][0]:
                for entry in s["energy"]["readings"]:
                    if abs(entry["values"]["kwNet"]) > max_value:
                        max_value = abs(entry["values"]["kwNet"])

            for s in load_profile[0]["series"][0]:
                for entry in s["energy"]["readings"]:
                    load_shape.append(f'{entry["values"]["kwNet"] / max_value}\n')
        except IndexError:
            # Empty Feeder
            pass
    
        return load_shape, max_value

    async def write_load_shape_to_txt(self, feeder: str, target: str, load_shape: List[str]):
        base_folder = f'{self.out_dir}/{feeder}/base/'
        if not os.path.exists(base_folder):
            os.makedirs(base_folder)

        async with aiof.open(f'{base_folder}{target}.txt', 'w', encoding='ascii') as f:
            # 1 more day will be written out as API call takes half a day previous and half a day after.
            # i.e 1 year of data will also include half a day of 31st of December the year before and half a day of 1st
            # of January the year after
            await f.writelines(load_shape)
            await f.close()
