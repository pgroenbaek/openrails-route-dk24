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

import re
import os
import math
import json
import numpy as np
import trackshapeutils as tsu


GLOBAL_TSECTION = "../GLOBAL/tsection.dat"
GLOBAL_TSECTIONEXT = "../ROUTES/OR_DK24/OPENRAILS/tsection.dat" # Set to None if not used.
LOCAL_TSECTION = "../ROUTES/OR_DK24/tsection.dat"

TIT_FILE = "../ROUTES/OR_DK24/dk24.tit"
TDB_FILE = "../ROUTES/OR_DK24/DK24.tdb"
WORLD_FOLDER = "../ROUTES/OR_DK24/WORLD"
OUTPUT_FOLDER = "../DATA/trackcenters"

STATION_NAME = "DKEmb_Bred_181_8"
TRIM_TRVECTORS_TO_PLATFORMS = True
DYNTRACK_SECTIONIDX_START = 50000
TILE_SIZE = 2048
NUM_POINTS_PER_METER = 0.3

# Optional manual reference point override
REFERENCE_TILE_X = None
REFERENCE_TILE_Y = None
REFERENCE_LOCAL_X = None
REFERENCE_LOCAL_Y = None
REFERENCE_LOCAL_Z = None


def read_file(path, encoding='utf-16-le'):
    with open(path, 'r', encoding=encoding) as f:
        return f.read()


def extract_block(lines, start_index):
    block_lines = []
    parenthesis_count = lines[start_index].count("(") - lines[start_index].count(")")
    block_lines.append(lines[start_index][lines[start_index].find("(")+1:])
    i = start_index + 1

    while parenthesis_count > 0 and i < len(lines):
        line = lines[i]
        parenthesis_count += line.count("(") - line.count(")")
        block_lines.append(line.strip())
        i += 1

    block = "\n".join(block_lines)
    return block, i


def load_tsection_files():
    global_text = read_file(GLOBAL_TSECTION)
    if GLOBAL_TSECTIONEXT:
        global_text += "\n" + read_file(GLOBAL_TSECTIONEXT)
    local_text = read_file(LOCAL_TSECTION)
    return global_text, local_text


def load_tit_and_tdb():
    return read_file(TIT_FILE), read_file(TDB_FILE)


def parse_station_tit_items(tit_text):
    station_items = {}
    lines = tit_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("PlatformItem ("):
            block, i = extract_block(lines, i)
            station_match = re.search(r'Station\s*\(\s*"([^"]+)"\s*\)', block)
            if not station_match or station_match.group(1) != STATION_NAME:
                continue

            tritemid_match = re.search(r'TrItemId\s*\(\s*(\d+)\s*\)', block)
            rdata_match = re.search(r'TrItemRData\s*\(\s*([^)]+)\)', block)
            platform_tr_match = re.search(r'PlatformTrItemData\s*\(\s*([^)]+)\)', block)
            pname_match = re.search(r'PlatformName\s*\(\s*"([^"]+)"\s*\)', block)

            rdata_tokens = rdata_match.group(1).split()
            rdata = [float(rdata_tokens[0]), float(rdata_tokens[1]), float(rdata_tokens[2]),
                     int(rdata_tokens[3]), int(rdata_tokens[4])]
            tritem_id = int(tritemid_match.group(1))

            station_items[tritem_id] = {
                "TrItemRData": rdata,
                "PlatformTrItemData": platform_tr_match.group(1).split(),
                "PlatformName": pname_match.group(1),
                "Station": station_match.group(1)
            }
        else:
            i += 1
    return station_items


def parse_world_files(station_tit_items):
    platforms = []
    processed_world_files = set()
    for _, tit_item in station_tit_items.items():
        tile_x, tile_y = tit_item["TrItemRData"][3], tit_item["TrItemRData"][4]
        world_file_name = f"w{('-' if tile_x < 0 else '+')}{abs(int(tile_x)):06d}{('-' if tile_y < 0 else '+')}{abs(int(tile_y)):06d}.w"
        if world_file_name in processed_world_files:
            continue

        world_text = read_file(f"{WORLD_FOLDER}/{world_file_name}")
        lines = world_text.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line.startswith("Platform ("):
                block, i = extract_block(lines, i)
                pdata_match = re.search(r'PlatformData\s*\(\s*([^)]+)\)', block)
                if not pdata_match:
                    continue
                platform_data = int(pdata_match.group(1), 16)
                tr_ids = [int(m.group(1)) for m in re.finditer(r'TrItemId\s*\(\s*\d+\s+(\d+)\s*\)', block)]
                platforms.append({"PlatformData": platform_data, "TrItemIds": tr_ids})
            else:
                i += 1
        processed_world_files.add(world_file_name)
    return platforms


def parse_tr_vector_sections(platforms, tdb_text):
    tr_vector_sections = {}
    lines = tdb_text.splitlines()
    n = len(lines)

    for platform in platforms:
        target_ids = platform["TrItemIds"]
        i = 0
        while i < n:
            line = lines[i].strip()
            if line.startswith("TrackNode ("):
                tn_block, i = extract_block(lines, i)
                tritemrefs = [int(x) for x in re.findall(r'TrItemRef\s*\(\s*(\d+)\s*\)', tn_block)]
                matching_ids = [tid for tid in tritemrefs if tid in target_ids]
                if not matching_ids:
                    continue
                tn_lines = tn_block.splitlines()
                j = 0
                while j < len(tn_lines):
                    if tn_lines[j].strip().startswith("TrVectorSections ("):
                        vs_block, j = extract_block(tn_lines, j)
                        numbers = [
                            float(n) if any(c in n for c in ".eE") else int(n)
                            for n in re.findall(r'-?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?', vs_block)
                        ][1:]
                        sections = [numbers[k:k + 16] for k in range(0, len(numbers), 16)]
                        for tid in matching_ids:
                            if tid not in tr_vector_sections:
                                tr_vector_sections[tid] = sections
                    else:
                        j += 1
            else:
                i += 1

    return tr_vector_sections


def generate_platform_trackcenters(platforms, tr_vector_sections, station_tit_items, global_tsection_text, local_tsection_text):
    platform_trackcenters = []
    ref_tritemid = platforms[0]["TrItemIds"][0]
    if REFERENCE_TILE_X is not None:
        ref_tile_x = REFERENCE_TILE_X
        ref_tile_y = REFERENCE_TILE_Y
        ref_local_x = REFERENCE_LOCAL_X
        ref_local_y = REFERENCE_LOCAL_Y
        ref_local_z = REFERENCE_LOCAL_Z
    else:
        ref_tritemid = tr_item_ids[0][0]
        ref_local_x, ref_local_y, ref_local_z = carspawner_rit_items[ref_tritemid]["TrItemRData"][:3]
        ref_tile_x, ref_tile_y = carspawner_rit_items[ref_tritemid]["TrItemRData"][3:5]

    for platform in platforms:
        tr_itemid = platform["TrItemIds"][0]
        sections = tr_vector_sections[tr_itemid]
        trackcenter = tsu.generate_empty_centerpoints()

        for section in sections:
            section_idx, shape_idx = section[0], section[1]
            tile_x, tile_y = section[8], section[9]
            local_x, local_y, local_z = section[10], section[11], section[12]
            elevation_promille = -section[13]
            compass_degrees = ((section[14] + math.pi) * 180 / math.pi) % 360
            start_angle = (180 - compass_degrees) % 360
            start_point = np.array([
                (tile_x - ref_tile_x) * TILE_SIZE + (local_x - ref_local_x),
                local_y - ref_local_y,
                (tile_y - ref_tile_y) * TILE_SIZE + (local_z - ref_local_z)
            ])

            # Generate section points
            if section_idx >= DYNTRACK_SECTIONIDX_START:
                sectioncurve_pattern = re.compile(
                    rf'SectionCurve\s*\(\s*\d+\s*\)\s+{section_idx}\s+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s+([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)'
                )
                m = re.search(sectioncurve_pattern, local_tsection_text)
                if not m:
                    raise ValueError(f"Unable to find local section idx '{section_idx}'")
                val1, val2 = float(m.group(1)), float(m.group(2))
                if val2 == 0:
                    length = val1
                    num_points = max(int(length * NUM_POINTS_PER_METER), 1)
                    section_trackcenter = tsu.generate_straight_centerpoints(length, num_points)
                else:
                    angle, radius = math.degrees(val1), val2
                    length = tsu.distance_along_curve(angle, radius)
                    num_points = max(int(length * NUM_POINTS_PER_METER), 1)
                    section_trackcenter = tsu.generate_curve_centerpoints(radius, angle, num_points)
            else:
                tracksection_pattern = re.compile(
                    rf"TrackSection\s*\(\s*({section_idx})\s*\n"
                    r"\s*SectionSize\s*\(\s*([\d.]+)\s+([\d.]+)\s*\)\s*\n"
                    r"(\s*SectionCurve\s*\(\s*([\d.-]+)\s+([\d.-]+)\s*\)\s*\n)?"
                    r"\s*\)", re.MULTILINE | re.DOTALL
                )
                m = tracksection_pattern.search(global_tsection_text)
                if not m:
                    raise ValueError(f"Unable to find global section idx '{section_idx}'")
                length = float(m.group(3))
                radius = float(m.group(5)) if m.group(5) else None
                angle = float(m.group(6)) if m.group(6) else None
                if radius and angle:
                    length_curve = tsu.distance_along_curve(angle, radius)
                    num_points = max(int(length_curve * NUM_POINTS_PER_METER), 1)
                    section_trackcenter = tsu.generate_curve_centerpoints(radius, angle, num_points)
                else:
                    num_points = max(int(length * NUM_POINTS_PER_METER), 1)
                    section_trackcenter = tsu.generate_straight_centerpoints(length, num_points)

            # Rotate, translate
            theta = math.radians(start_angle)
            rotation_matrix = np.array([
                [math.cos(theta), 0, -math.sin(theta)],
                [0, 1, 0],
                [math.sin(theta), 0, math.cos(theta)]
            ])
            rotated_points = (rotation_matrix @ section_trackcenter.centerpoints.T).T
            section_trackcenter.centerpoints = rotated_points + start_point
            
            # Elevation
            forward = section_trackcenter.centerpoints[:, [0, 2]] - section_trackcenter.centerpoints[0, [0, 2]]
            distances = np.linalg.norm(forward, axis=1)
            section_trackcenter.centerpoints[:, 1] = start_point[1] + distances * elevation_promille

            trackcenter += section_trackcenter

        platform_trackcenters.append(trackcenter)

    return platform_trackcenters, ref_local_x, ref_local_y, ref_local_z, ref_tile_x, ref_tile_y


def trim_platform_trackcenters(platforms, platform_trackcenters, station_tit_items, ref_local_x, ref_local_y, ref_local_z, ref_tile_x, ref_tile_y):
    if not TRIM_TRVECTORS_TO_PLATFORMS:
        return
    for platform, trackcenter in zip(platforms, platform_trackcenters):
        points = trackcenter.centerpoints
        start_tr = station_tit_items[platform["TrItemIds"][0]]
        end_tr = station_tit_items[platform["TrItemIds"][1]]
        p1 = np.array([
            (start_tr["TrItemRData"][3] - ref_tile_x) * TILE_SIZE + start_tr["TrItemRData"][0] - ref_local_x,
            start_tr["TrItemRData"][1] - ref_local_y,
            (start_tr["TrItemRData"][4] - ref_tile_y) * TILE_SIZE + start_tr["TrItemRData"][2] - ref_local_z
        ])
        p2 = np.array([
            (end_tr["TrItemRData"][3] - ref_tile_x) * TILE_SIZE + end_tr["TrItemRData"][0] - ref_local_x,
            end_tr["TrItemRData"][1] - ref_local_y,
            (end_tr["TrItemRData"][4] - ref_tile_y) * TILE_SIZE + end_tr["TrItemRData"][2] - ref_local_z
        ])
        d1, d2 = np.linalg.norm(points - p1, axis=1), np.linalg.norm(points - p2, axis=1)
        start_idx, end_idx = sorted([np.argmin(d1), np.argmin(d2)])
        trackcenter.centerpoints = points[start_idx:end_idx + 1]


def save_station_json(platforms, platform_trackcenters, station_tit_items, ref_local_x, ref_local_y, ref_local_z, ref_tile_x, ref_tile_y):
    output = {
        "station_name": STATION_NAME,
        "reference_x": ref_local_x,
        "reference_y": ref_local_y,
        "reference_z": ref_local_z,
        "reference_tile_x": ref_tile_x,
        "reference_tile_y": ref_tile_y,
        "platforms": []
    }
    for platform, trackcenter in zip(platforms, platform_trackcenters):
        platform_data = {
            "platform_name": station_tit_items[platform["TrItemIds"][0]]["PlatformName"],
            "platform_coords": trackcenter.centerpoints[:, [0, 2, 1]].tolist()
        }
        output["platforms"].append(platform_data)

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    with open(f"{OUTPUT_FOLDER}/{STATION_NAME}.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"{len(platforms)} platforms exported for station '{STATION_NAME}'.")


if __name__ == "__main__":
    global_text, local_text = load_tsection_files()
    tit_text, tdb_text = load_tit_and_tdb()

    station_tit_items = parse_station_tit_items(tit_text)
    if not station_tit_items:
        raise RuntimeError(f"No platforms found for station '{STATION_NAME}'.")

    platforms = parse_world_files(station_tit_items)
    tr_vector_sections = parse_tr_vector_sections(platforms, tdb_text)

    platform_trackcenters, ref_local_x, ref_local_y, ref_local_z, ref_tile_x, ref_tile_y = generate_platform_trackcenters(
        platforms, tr_vector_sections, station_tit_items, global_text, local_text
    )

    trim_platform_trackcenters(platforms, platform_trackcenters, station_tit_items,
        ref_local_x, ref_local_y, ref_local_z, ref_tile_x, ref_tile_y)

    save_station_json(platforms, platform_trackcenters, station_tit_items,
        ref_local_x, ref_local_y, ref_local_z, ref_tile_x, ref_tile_y)