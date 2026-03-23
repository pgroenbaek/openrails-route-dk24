"""
Copyright (C) 2026 Peter Grønbæk Andersen <peter@grnbk.io>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import os
import struct
import math

HGT_DIR = "D:\Games\Open Rails\HGST"
OUTPUT_DIR = "D:\Games\Open Rails\HGST_OFFSET"

OFFSET_METERS = 1
VOID_VALUE = -32768

EXPECTED_SAMPLES = 1201 * 1201
EXPECTED_BYTES = EXPECTED_SAMPLES * 2

os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_hgt(path_in, path_out):
    with open(path_in, "rb") as f:
        data = f.read()

    if len(data) != EXPECTED_BYTES:
        raise ValueError(f"Unexpected file size: {len(data)} bytes")

    values = struct.unpack(f">{EXPECTED_SAMPLES}h", data)

    out = []
    for v in values:
        if v == VOID_VALUE:
            out.append(v)
        else:
            out.append(v + OFFSET_METERS)

    packed = struct.pack(f">{EXPECTED_SAMPLES}h", *out)

    with open(path_out, "wb") as f:
        f.write(packed)

for name in os.listdir(HGT_DIR):
    if not name.lower().endswith(".hgt"):
        continue

    src = os.path.join(HGT_DIR, name)
    dst = os.path.join(OUTPUT_DIR, name)

    process_hgt(src, dst)
    print(f"OK: {name}")

print("Done.")
