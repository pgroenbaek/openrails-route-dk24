"""
Copyright (C) 2025 Peter Grønbæk Andersen <peter@grnbk.io>

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
import re
import sys
import fnmatch
import datetime
import zipfile
import trackshapeutils as tsu


RELEASE_VERSION = "v0.1.001"
FFEDITC_PATH = "./ffeditc_unicode.exe"
SEARCH_PATH = ".."
ROUTE_PATH = "ROUTES/OR_DK24"
EXPORT_PATH = ".."
EXPORT_FILENAME = f"DK24_{RELEASE_VERSION}.zip"
EXPORT_FILE = f"{EXPORT_PATH}/{EXPORT_FILENAME}"
SHAPE_FOLDERS = ["GLOBAL/SHAPES", f"{ROUTE_PATH}/SHAPES"]
TEXTURE_FOLDERS = [f"{ROUTE_PATH}/TEXTURES"]

FILE_MATCHES = [
    ("", "LICENSE"),
    ("", "README.md"),
    ("", "CONTRIBUTING.md"),
    ("GLOBAL", "tsection.dat"),
    (ROUTE_PATH, "*.haz"),
    (ROUTE_PATH, "carspawn.dat"),
    (ROUTE_PATH, "DK24_small.png"),
    (ROUTE_PATH, "DK24.png"),
    (ROUTE_PATH, "DK24.rdb"),
    (ROUTE_PATH, "DK24.ref"),
    (ROUTE_PATH, "dk24.rit"),
    (ROUTE_PATH, "DK24.tdb"),
    (ROUTE_PATH, "dk24.tit"),
    (ROUTE_PATH, "DK24.trk"),
    (ROUTE_PATH, "forests.dat"),
    (ROUTE_PATH, "graphic.ace"),
    (ROUTE_PATH, "load.ace"),
    (ROUTE_PATH, "Map_whitebg.png"),
    (ROUTE_PATH, "Map.png"),
    (ROUTE_PATH, "MirelDb.xml"),
    (ROUTE_PATH, "MirelDbVersion.ini"),
    (ROUTE_PATH, "PowerSupplyStations.xml"),
    (ROUTE_PATH, "PowerSupplyStationsDbVersion.ini"),
    (ROUTE_PATH, "sigcfg.dat"),
    (ROUTE_PATH, "sigscr.dat"),
    (ROUTE_PATH, "speedpost.dat"),
    (ROUTE_PATH, "ssource.dat"),
    (ROUTE_PATH, "telepole.dat"),
    (ROUTE_PATH, "tsection.dat"),
    (ROUTE_PATH, "ttype.dat"),
    (ROUTE_PATH, "VoltageChangeMarkers.xml"),
    (ROUTE_PATH, "VoltageChangeMarkersDbVersion.ini"),
    (f"{ROUTE_PATH}/ENVFILES", "*.ace"),
    (f"{ROUTE_PATH}/ENVFILES", "*.env"),
    (f"{ROUTE_PATH}/OPENRAILS", "tsection.dat"),
    (f"{ROUTE_PATH}/PATHS", "*.pat"),
    (f"{ROUTE_PATH}/TD", "*.dat"),
    (f"{ROUTE_PATH}/TD", "*.td"),
    (f"{ROUTE_PATH}/SOUND", "*.sms"),
    (f"{ROUTE_PATH}/SOUND", "*.wav"),
    (f"{ROUTE_PATH}/TERRTEX", "*.ace"),
    (f"{ROUTE_PATH}/TERRTEX", "*.dds"),
    (f"{ROUTE_PATH}/TILES", "*.t"),
    (f"{ROUTE_PATH}/TILES", "*.raw"),
    (f"{ROUTE_PATH}/TRACKPROFILES", "*.stf"),
    (f"{ROUTE_PATH}/WORLD", "*.w"),
    (f"{ROUTE_PATH}/WORLD", "*.ws"),
    ("SOUND", "*.sms"),
    ("SOUND", "*.wav"),
    ("TRAINS/CONSISTS", "*.con"),
]

TEXTURE_PATTERN = re.compile(r'[\w./-]+\.(ace|dds)\b', re.IGNORECASE)
SHAPEFILE_PATTERN = re.compile(r'[\w./-]+\.s\b', re.IGNORECASE)


def find_files(search_directory, match_files):
    files = []

    for file_name in os.listdir(search_directory):
        if fnmatch.fnmatch(file_name, match_files):
            files.append(f"{search_directory}/{file_name}")

    return files


def find_matches_within_text(text, pattern):
    matches = [match.group(0) for match in pattern.finditer(text)]

    return matches


def find_matches_within_file(file_path, pattern):
    with open(file_path, 'r', encoding='utf-16-le') as f:
        text = f.read()

    return find_matches_within_text(text, pattern)


def find_files_to_pack(search_path, file_matches):
    pack_files = []

    for file_path, file_match in file_matches:
        for directory in [x[0] for x in os.walk(f"{search_path}/{file_path}")]:
            for file_name in os.listdir(directory):
                if fnmatch.fnmatch(file_name, file_match):
                    source_file = f"{directory}/{file_name}"
                    destination_file = f"{directory}/{file_name}".replace(f"{search_path}/", "")
                    pack_files.append((source_file, destination_file))
                    print(f"Found {len(pack_files)} files.", end='\r')
    
    return pack_files


def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def remove_file_if_exists(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)


def pack_files(files_to_pack):
    files_to_pack = list(set(files_to_pack))

    with zipfile.ZipFile(export_file, "a", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
        for idx, (source_file, destination_file) in enumerate(files_to_pack):
            print(f"Packed {idx + 1} of {len(files_to_pack)} files.", end='\r')
            try:
                zipf.write(source_file, destination_file)
            except FileNotFoundError:
                print(f"File not found: {source_file}")



if __name__ == "__main__":
    ensure_directory_exists(EXPORT_PATH)
    remove_file_if_exists(EXPORT_FILE)

    # Find files other than textures and shapes.
    files_to_pack = find_files_to_pack(SEARCH_PATH, FILE_MATCHES)
    
    # Find shapes that are used in the route.
    referenced_shapes = []
    referenced_shapes += find_matches_within_file(f"{SEARCH_PATH}/{ROUTE_PATH}/carspawn.dat", SHAPEFILE_PATTERN)
    referenced_shapes += find_matches_within_file(f"{SEARCH_PATH}/{ROUTE_PATH}/forests.dat", SHAPEFILE_PATTERN)
    referenced_shapes += find_matches_within_file(f"{SEARCH_PATH}/{ROUTE_PATH}/sigcfg.dat", SHAPEFILE_PATTERN)
    referenced_shapes += find_matches_within_file(f"{SEARCH_PATH}/{ROUTE_PATH}/speedpost.dat", SHAPEFILE_PATTERN)
    referenced_shapes += find_matches_within_file(f"{SEARCH_PATH}/{ROUTE_PATH}/telepole.dat", SHAPEFILE_PATTERN)

    for hazard_file in find_files(f"{SEARCH_PATH}/{ROUTE_PATH}", "*.haz"):
        referenced_shapes += find_matches_within_file(hazard_file, SHAPEFILE_PATTERN)
    
    for world_file in find_files(f"{SEARCH_PATH}/{ROUTE_PATH}/WORLD", "*.w"):
        referenced_shapes += find_matches_within_file(world_file, SHAPEFILE_PATTERN)
    
    referenced_shapes = [os.path.split(s)[1] for s in referenced_shapes]
    referenced_shapes = list(set(referenced_shapes))
    
    print(f"Found {len(referenced_shapes)} shapes used in the route.")

    for shape in referenced_shapes:
        if not any([os.path.exists(f"{SEARCH_PATH}/{folder}/{shape}") for folder in SHAPE_FOLDERS]):
            print(f"\tWarning: Shape '{shape}' was not found in any shape folder.")
            continue
        
        for shape_folder in SHAPE_FOLDERS:
            if os.path.exists(f"{SEARCH_PATH}/{shape_folder}/{shape}"):
                source_file = f"{SEARCH_PATH}/{shape_folder}/{shape}"
                destination_file = f"{shape_folder}/{shape}"
                files_to_pack.append((source_file, destination_file))

    # Find textures that are used in the route.
    referenced_textures = []
    referenced_textures += find_matches_within_file(f"{SEARCH_PATH}/{ROUTE_PATH}/forests.dat", TEXTURE_PATTERN)
    referenced_textures += find_matches_within_file(f"{SEARCH_PATH}/{ROUTE_PATH}/sigcfg.dat", TEXTURE_PATTERN)
    referenced_textures += find_matches_within_file(f"{SEARCH_PATH}/{ROUTE_PATH}/speedpost.dat", TEXTURE_PATTERN)

    for world_file in find_files(f"{SEARCH_PATH}/{ROUTE_PATH}/WORLD", "*.w"):
        referenced_textures += find_matches_within_file(world_file, TEXTURE_PATTERN)

    # Find textures that are referenced by shapes used in the route.
    for idx, shape in enumerate(referenced_shapes):
        print(f"Finding textures in shape {idx + 1} of {len(referenced_shapes)}.", end='\r')

        for shape_folder in SHAPE_FOLDERS:
            if os.path.exists(f"{SEARCH_PATH}/{shape_folder}/{shape}"):
                shape = tsu.load_shape(shape, f"{SEARCH_PATH}/{shape_folder}")
                shape.decompress(FFEDITC_PATH)

                referenced_textures += find_matches_within_text("\n".join(shape.lines), TEXTURE_PATTERN)
                
                shape.compress(FFEDITC_PATH)

    referenced_textures = list(set(referenced_textures))

    print(f"Found {len(referenced_textures)} textures used in the route.")

    for texture in referenced_textures:
        if not any([os.path.exists(f"{SEARCH_PATH}/{folder}/{texture}") for folder in TEXTURE_FOLDERS]):
            print(f"\tWarning: Texture '{texture}' was not found in any texture folder.")
    
    for texture_folder in TEXTURE_FOLDERS:
        textures_to_find = [(texture_folder, item) for item in referenced_textures]
        files_to_pack += find_files_to_pack(SEARCH_PATH, textures_to_find)

    pack_files(files_to_pack)