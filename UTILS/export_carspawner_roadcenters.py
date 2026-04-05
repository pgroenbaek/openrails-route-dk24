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

RIT_FILE = "../ROUTES/OR_DK24/dk24.rit"
RDB_FILE = "../ROUTES/OR_DK24/DK24.rdb"
OUTPUT_FOLDER = "../DATA/roadcenters"

ROADCENTERS_OUTPUT_NAME = "DKEmb_Bred_181_8"
CARSPAWNER_TRITEM_IDS = [0, 2] # Only need to put a single TrItem ID from each carspawner.
TRIM_TRVECTORS_TO_CARSPAWNERS = True
TILE_SIZE = 2048
NUM_POINTS_PER_METER = 0.3

# Optional manual reference point override
REFERENCE_TILE_X = -5666
REFERENCE_TILE_Y = 15118
REFERENCE_LOCAL_X = 702.968
REFERENCE_LOCAL_Y = 50.62607
REFERENCE_LOCAL_Z = -552.1223


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
    return global_text


def load_rit_and_rdb():
    return read_file(RIT_FILE), read_file(RDB_FILE)


def parse_carspawner_rit_items(rit_text):
    carspawner_items = {}
    lines = rit_text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("CarSpawnerItem ("):
            block, i = extract_block(lines, i)
            
            tritemid_match = re.search(r'TrItemId\s*\(\s*(\d+)\s*\)', block)
            rdata_match = re.search(r'TrItemRData\s*\(\s*([^)]+)\)', block)

            rdata_tokens = rdata_match.group(1).split()
            rdata = [float(rdata_tokens[0]), float(rdata_tokens[1]), float(rdata_tokens[2]),
                     int(rdata_tokens[3]), int(rdata_tokens[4])]
            tritem_id = int(tritemid_match.group(1))

            carspawner_items[tritem_id] = {
                "TrItemRData": rdata,
            }
        else:
            i += 1
    return carspawner_items


def parse_tr_vector_sections(carspawner_tr_ids, tdb_text):
    tr_vector_sections = []
    tr_item_ids = []
    lines = tdb_text.splitlines()
    n = len(lines)

    i = 0
    while i < n:
        line = lines[i].strip()
        if line.startswith("TrackNode ("):
            tn_block, i = extract_block(lines, i)
            tritemrefs = [int(x) for x in re.findall(r'TrItemRef\s*\(\s*(\d+)\s*\)', tn_block)]
            matching_ids = [tid for tid in tritemrefs if tid in carspawner_tr_ids]
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
                    tr_vector_sections.append(sections)
                    tr_item_ids.append(tritemrefs)
                else:
                    j += 1
        else:
            i += 1

    return tr_item_ids, tr_vector_sections


def generate_carspawner_roadcenters(tr_item_ids, tr_vector_sections, carspawner_rit_items, global_tsection_text):
    carspawner_roadcenters = []
    ref_tritemid = tr_item_ids[0][0]
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

    for sections in tr_vector_sections:
        roadcenter = tsu.generate_empty_centerpoints()

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
                section_roadcenter = tsu.generate_curve_centerpoints(radius, angle, num_points)
            else:
                num_points = max(int(length * NUM_POINTS_PER_METER), 1)
                section_roadcenter = tsu.generate_straight_centerpoints(length, num_points)

            # Rotate, translate
            theta = math.radians(start_angle)
            rotation_matrix = np.array([
                [math.cos(theta), 0, -math.sin(theta)],
                [0, 1, 0],
                [math.sin(theta), 0, math.cos(theta)]
            ])
            rotated_points = (rotation_matrix @ section_roadcenter.centerpoints.T).T
            section_roadcenter.centerpoints = rotated_points + start_point
            
            # Elevation
            forward = section_roadcenter.centerpoints[:, [0, 2]] - section_roadcenter.centerpoints[0, [0, 2]]
            distances = np.linalg.norm(forward, axis=1)
            section_roadcenter.centerpoints[:, 1] = start_point[1] + distances * elevation_promille

            roadcenter += section_roadcenter

        carspawner_roadcenters.append(roadcenter)

    return carspawner_roadcenters, ref_local_x, ref_local_y, ref_local_z, ref_tile_x, ref_tile_y


def trim_carspawner_roadcenters(tr_item_ids, carspawner_roadcenters, carspawner_rit_items, ref_local_x, ref_local_y, ref_local_z, ref_tile_x, ref_tile_y):
    if not TRIM_TRVECTORS_TO_CARSPAWNERS:
        return
    for tr_item_id, roadcenter in zip(tr_item_ids, carspawner_roadcenters):
        points = roadcenter.centerpoints
        start_tr = carspawner_rit_items[tr_item_id[0]]
        end_tr = carspawner_rit_items[tr_item_id[1]]
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
        roadcenter.centerpoints = points[start_idx:end_idx + 1]


def save_roadcenters_json(tr_item_ids, carspawner_roadcenters, carspawner_rit_items, ref_local_x, ref_local_y, ref_local_z, ref_tile_x, ref_tile_y):
    output = {
        "reference_x": ref_local_x,
        "reference_y": ref_local_y,
        "reference_z": ref_local_z,
        "reference_tile_x": ref_tile_x,
        "reference_tile_y": ref_tile_y,
        "carspawners": []
    }
    for tr_item_id, roadcenter in zip(tr_item_ids, carspawner_roadcenters):
        carspawner_data = {
            "carspawner_name": f"Carspawner{tr_item_id[0]}_{tr_item_id[1]}",
            "carspawner_coords": roadcenter.centerpoints[:, [0, 2, 1]].tolist()
        }
        output["carspawners"].append(carspawner_data)

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    with open(f"{OUTPUT_FOLDER}/{ROADCENTERS_OUTPUT_NAME}.json", "w") as f:
        json.dump(output, f, indent=2)

    print(f"{len(tr_item_ids)} roadcenters exported.")


if __name__ == "__main__":
    print(f"Exporting roadcenters from carspawners containing TrItem id's: {CARSPAWNER_TRITEM_IDS}")
    global_text = load_tsection_files()
    rit_text, rdb_text = load_rit_and_rdb()

    carspawner_rit_items = parse_carspawner_rit_items(rit_text)
    if not carspawner_rit_items:
        raise RuntimeError(f"No carspawners found.")

    tr_item_ids, tr_vector_sections = parse_tr_vector_sections(CARSPAWNER_TRITEM_IDS, rdb_text)

    carspawner_roadcenters, ref_local_x, ref_local_y, ref_local_z, ref_tile_x, ref_tile_y = generate_carspawner_roadcenters(
        tr_item_ids, tr_vector_sections, carspawner_rit_items, global_text
    )

    trim_carspawner_roadcenters(tr_item_ids, carspawner_roadcenters, carspawner_rit_items,
        ref_local_x, ref_local_y, ref_local_z, ref_tile_x, ref_tile_y)

    save_roadcenters_json(tr_item_ids, carspawner_roadcenters, carspawner_rit_items,
        ref_local_x, ref_local_y, ref_local_z, ref_tile_x, ref_tile_y)