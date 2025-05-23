# Packs a DK24 release into a zip file, with only assets that are actually used in the route.

import os
import sys
import fnmatch
import datetime
import zipfile
import trackshapeutils as tsu

# TODO create a list of shape files:
#   Search world files
#   Search carspawn.dat
#   Search *.haz
#   Search sigcfg.dat
#   Search telepole.dat

# TODO create a list of textures:
#   Search forests.dat
#   Search sigcfg.dat
#   Search speedpost.dat
#   Find in the following folders, whereever it exists:
#       - GLOBAL/SHAPES
#       - ROUTES/OR_DK24/SHAPES

# TODO Look for textures in shapes (use FFEDITC)
#   Add them to textures list

# TODO Find shapes in the following folders, whereever it exists:
#       - GLOBAL/SHAPES
#       - ROUTES/OR_DK24/SHAPES
#   Warn if anything is missing

# TODO Find textures in the following folders, whereever it exists:
#       - GLOBAL/SHAPES
#       - ROUTES/OR_DK24/SHAPES
#   Also copy the texture from all environmant subfolders
#   Warn if anything is missing
def find_files_to_pack(search_path, file_matches):
    pack_files = []
    for file_path, file_match in file_matches:
        for directory in [x[0] for x in os.walk(f"{search_path}/{file_path}")]:
            for file_name in os.listdir(directory):
                if fnmatch.fnmatch(file_name, file_match):
                    source_file = f"{directory}/{file_name}"
                    destination_file = f"{directory}/{file_name}".replace(f"{search_path}/", "")
                    pack_assets.append((source_file, destination_file))
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
    version = "v0.1"
    search_path = ".."
    export_path = ".."
    export_filename = f"DK24_{version}.zip"
    export_file = f"{export_path}/{export_filename}"

    file_matches = [
        ("", "LICENSE"),
        ("", "README.md"),
        ("", "CONTRIBUTING.md"),
        ("GLOBAL", "tsection.dat"),
        ("ROUTES/OR_DK24", "carspawn.dat"),
        ("ROUTES/OR_DK24", "deer.haz"),
        ("ROUTES/OR_DK24", "DK24_small.png"),
        ("ROUTES/OR_DK24", "DK24.png"),
        ("ROUTES/OR_DK24", "DK24.rdb"),
        ("ROUTES/OR_DK24", "DK24.ref"),
        ("ROUTES/OR_DK24", "dk24.rit"),
        ("ROUTES/OR_DK24", "DK24.tdb"),
        ("ROUTES/OR_DK24", "dk24.tit"),
        ("ROUTES/OR_DK24", "DK24.trk"),
        ("ROUTES/OR_DK24", "forests.dat"),
        ("ROUTES/OR_DK24", "graphic.ace"),
        ("ROUTES/OR_DK24", "load.ace"),
        ("ROUTES/OR_DK24", "Map_whitebg.png"),
        ("ROUTES/OR_DK24", "Map.png"),
        ("ROUTES/OR_DK24", "MirelDb.xml"),
        ("ROUTES/OR_DK24", "MirelDbVersion.ini"),
        ("ROUTES/OR_DK24", "PowerSupplyStations.xml"),
        ("ROUTES/OR_DK24", "PowerSupplyStationsDbVersion.ini"),
        ("ROUTES/OR_DK24", "sigcfg.dat"),
        ("ROUTES/OR_DK24", "sigscr.dat"),
        ("ROUTES/OR_DK24", "speedpost.dat"),
        ("ROUTES/OR_DK24", "spotter.haz"),
        ("ROUTES/OR_DK24", "ssource.dat"),
        ("ROUTES/OR_DK24", "telepole.dat"),
        ("ROUTES/OR_DK24", "tsection.dat"),
        ("ROUTES/OR_DK24", "ttype.dat"),
        ("ROUTES/OR_DK24", "VoltageChangeMarkers.xml"),
        ("ROUTES/OR_DK24", "VoltageChangeMarkersDbVersion.ini"),
        ("ROUTES/OR_DK24/ENVFILES", "*.ace"),
        ("ROUTES/OR_DK24/ENVFILES", "*.env"),
        ("ROUTES/OR_DK24/OPENRAILS", "tsection.dat"),
        ("ROUTES/OR_DK24/PATHS", "*.pat"),
        ("ROUTES/OR_DK24/TD", "*.dat"),
        ("ROUTES/OR_DK24/TD", "*.td"),
        ("ROUTES/OR_DK24/SOUND", "*.sms"),
        ("ROUTES/OR_DK24/SOUND", "*.wav"),
        ("ROUTES/OR_DK24/TERRTEX", "*.ace"),
        ("ROUTES/OR_DK24/TERRTEX", "*.dds"),
        ("ROUTES/OR_DK24/TILES", "*.t"),
        ("ROUTES/OR_DK24/TILES", "*.raw"),
        ("ROUTES/OR_DK24/TRACKPROFILES", "*.stf"),
        ("ROUTES/OR_DK24/WORLD", "*.w"),
        ("ROUTES/OR_DK24/WORLD", "*.ws"),
        ("SOUND", "*.sms"),
        ("SOUND", "*.wav"),
        ("TRAINS/CONSISTS", "*.con"),
    ]
    
    ensure_directory_exists(export_path)
    remove_file_if_exists(export_file)
    
    files_to_pack = find_files_to_pack(search_path, file_matches)
    pack_files(files_to_pack)