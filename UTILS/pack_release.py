# Packs a DK24 release into a zip file, with only assets that are actually used in the route.

import os
import re
import sys
import fnmatch
import datetime
import zipfile
import trackshapeutils as tsu


ace_dds_pattern = re.compile(r'[\w./-]+\.(ace|dds)\b', re.IGNORECASE)
s_file_pattern = re.compile(r'[\w./-]+\.s\b', re.IGNORECASE)


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
    version = "v0.1.001"
    ffeditc_path = "./ffeditc_unicode.exe"
    search_path = ".."
    route_path = "ROUTES/OR_DK24"
    export_path = ".."
    export_filename = f"DK24_{version}.zip"
    export_file = f"{export_path}/{export_filename}"
    shape_folders = ["GLOBAL/SHAPES", f"{route_path}/SHAPES"]
    texture_folders = [f"{route_path}/TEXTURES"]

    file_matches = [
        ("", "LICENSE"),
        ("", "README.md"),
        ("", "CONTRIBUTING.md"),
        ("GLOBAL", "tsection.dat"),
        (route_path, "*.haz"),
        (route_path, "carspawn.dat"),
        (route_path, "DK24_small.png"),
        (route_path, "DK24.png"),
        (route_path, "DK24.rdb"),
        (route_path, "DK24.ref"),
        (route_path, "dk24.rit"),
        (route_path, "DK24.tdb"),
        (route_path, "dk24.tit"),
        (route_path, "DK24.trk"),
        (route_path, "forests.dat"),
        (route_path, "graphic.ace"),
        (route_path, "load.ace"),
        (route_path, "Map_whitebg.png"),
        (route_path, "Map.png"),
        (route_path, "MirelDb.xml"),
        (route_path, "MirelDbVersion.ini"),
        (route_path, "PowerSupplyStations.xml"),
        (route_path, "PowerSupplyStationsDbVersion.ini"),
        (route_path, "sigcfg.dat"),
        (route_path, "sigscr.dat"),
        (route_path, "speedpost.dat"),
        (route_path, "ssource.dat"),
        (route_path, "telepole.dat"),
        (route_path, "tsection.dat"),
        (route_path, "ttype.dat"),
        (route_path, "VoltageChangeMarkers.xml"),
        (route_path, "VoltageChangeMarkersDbVersion.ini"),
        (f"{route_path}/ENVFILES", "*.ace"),
        (f"{route_path}/ENVFILES", "*.env"),
        (f"{route_path}/OPENRAILS", "tsection.dat"),
        (f"{route_path}/PATHS", "*.pat"),
        (f"{route_path}/TD", "*.dat"),
        (f"{route_path}/TD", "*.td"),
        (f"{route_path}/SOUND", "*.sms"),
        (f"{route_path}/SOUND", "*.wav"),
        (f"{route_path}/TERRTEX", "*.ace"),
        (f"{route_path}/TERRTEX", "*.dds"),
        (f"{route_path}/TILES", "*.t"),
        (f"{route_path}/TILES", "*.raw"),
        (f"{route_path}/TRACKPROFILES", "*.stf"),
        (f"{route_path}/WORLD", "*.w"),
        (f"{route_path}/WORLD", "*.ws"),
        ("SOUND", "*.sms"),
        ("SOUND", "*.wav"),
        ("TRAINS/CONSISTS", "*.con"),
    ]
    
    ensure_directory_exists(export_path)
    remove_file_if_exists(export_file)

    # Find files other than textures and shapes.
    files_to_pack = find_files_to_pack(search_path, file_matches)
    
    # Find shapes that are used in the route.
    referenced_shapes = []
    referenced_shapes += find_matches_within_file(f"{search_path}/{route_path}/carspawn.dat", s_file_pattern)
    referenced_shapes += find_matches_within_file(f"{search_path}/{route_path}/forests.dat", s_file_pattern)
    referenced_shapes += find_matches_within_file(f"{search_path}/{route_path}/sigcfg.dat", s_file_pattern)
    referenced_shapes += find_matches_within_file(f"{search_path}/{route_path}/speedpost.dat", s_file_pattern)
    referenced_shapes += find_matches_within_file(f"{search_path}/{route_path}/telepole.dat", s_file_pattern)

    for hazard_file in find_files(f"{search_path}/{route_path}", "*.haz"):
        referenced_shapes += find_matches_within_file(hazard_file, s_file_pattern)
    
    for world_file in find_files(f"{search_path}/{route_path}/WORLD", "*.w"):
        referenced_shapes += find_matches_within_file(world_file, s_file_pattern)
    
    referenced_shapes = [os.path.split(s)[1] for s in referenced_shapes]
    referenced_shapes = list(set(referenced_shapes))
    
    print(f"Found {len(referenced_shapes)} shapes used in the route.")

    for shape in referenced_shapes:
        if not any([os.path.exists(f"{search_path}/{folder}/{shape}") for folder in shape_folders]):
            print(f"\tWarning: Shape '{shape}' was not found in any shape folder.")
            continue
        
        for shape_folder in shape_folders:
            if os.path.exists(f"{search_path}/{shape_folder}/{shape}"):
                source_file = f"{search_path}/{shape_folder}/{shape}"
                destination_file = f"{shape_folder}/{shape}"
                files_to_pack.append((source_file, destination_file))

    # Find textures that are used in the route.
    referenced_textures = []
    referenced_textures += find_matches_within_file(f"{search_path}/{route_path}/forests.dat", ace_dds_pattern)
    referenced_textures += find_matches_within_file(f"{search_path}/{route_path}/sigcfg.dat", ace_dds_pattern)
    referenced_textures += find_matches_within_file(f"{search_path}/{route_path}/speedpost.dat", ace_dds_pattern)

    for world_file in find_files(f"{search_path}/{route_path}/WORLD", "*.w"):
        referenced_textures += find_matches_within_file(world_file, ace_dds_pattern)

    # Find textures that are referenced by shapes used in the route.
    for idx, shape in enumerate(referenced_shapes):
        print(f"Finding textures in shape {idx + 1} of {len(referenced_shapes)}.", end='\r')

        for shape_folder in shape_folders:
            if os.path.exists(f"{search_path}/{shape_folder}/{shape}"):
                shape = tsu.load_shape(shape, f"{search_path}/{shape_folder}")
                shape.decompress(ffeditc_path)

                referenced_textures += find_matches_within_text("\n".join(shape.lines), ace_dds_pattern)
                
                shape.compress(ffeditc_path)

    referenced_textures = list(set(referenced_textures))

    print(f"Found {len(referenced_textures)} textures used in the route.")

    for texture in referenced_textures:
        if not any([os.path.exists(f"{search_path}/{folder}/{texture}") for folder in texture_folders]):
            print(f"\tWarning: Texture '{texture}' was not found in any texture folder.")
    
    for texture_folder in texture_folders:
        textures_to_find = [(texture_folder, item) for item in referenced_textures]
        files_to_pack += find_files_to_pack(search_path, textures_to_find)

    files_to_pack = list(set(files_to_pack))
    pack_files(files_to_pack)