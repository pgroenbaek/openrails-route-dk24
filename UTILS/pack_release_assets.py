# Exports all DK24 assets into a zip file, only those that are used in the route.

import os
import sys
import fnmatch
import datetime
import zipfile
import 

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
def find_assets_to_pack(file_matches):
    pack_assets = []
    for file_path, file_match in file_matches:
        for directory in [x[0] for x in os.walk(f"{search_path}}/{file_path}")]:
            for file_name in os.listdir(directory):
                if fnmatch.fnmatch(file_name, file_match):
                    pack_assets.append((file_path, file_name))
                    print(f"Found {len(pack_assets)} assets.", end='\r')
    return pack_assets


def ensure_directory_exists(directory_path):
    if not os.path.exists(directory_path): 
        os.makedirs(directory_path)


def remove_file_if_exists(file_path):
    if os.path.exists(file_path): 
        os.remove(file_path)


def pack_assets(assets_to_pack):
    assets_to_pack = list(set(assets_to_pack))

    with zipfile.ZipFile(export_file, "a", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
        for idx, (file_path, file_name) in enumerate(assets_to_pack):
            print(f"Packed {idx + 1} of {len(assets_to_pack)} assets.", end='\r')
            source_file = f"{search_path}/{file_path}/{file_name}")
            destination_file = f"{file_path}/{file_name}")
            try:
                zipf.write(source_file, destination_file)
            except FileNotFoundError:
                print(f"File not found: {source_file}")



if __name__ == "__main__":
    version = "v0.1"
    search_path = "../"
    export_path = "../"
    export_filename = f"DK24_Assets_{version}.zip"
    export_file = f"{export_path}/{export_filename}"

    file_matches = [
        ("ROUTES/OR_DK24/SOUND", "*.sms"),
        ("ROUTES/OR_DK24/SOUND", "*.wav"),
        ("ROUTES/OR_DK24/TERRTEX", "*.ace"),
        ("ROUTES/OR_DK24/TERRTEX", "*.dds"),
        ("ROUTES/OR_DK24/TILES", "*.t"),
        ("ROUTES/OR_DK24/TILES", "*.raw"),
        ("ROUTES/OR_DK24/TRACKPROFILES", "*.stf"),
        ("SOUND", "*.sms"),
        ("SOUND", "*.wav"),
    ]
    
    ensure_directory_exists(export_path)
    remove_file_if_exists(export_file)
    
    assets_to_pack = find_assets_to_pack(file_matches)
    pack_assets(assets_to_pack)