# Packs all DK24 assets into a zip file, even those that are not used in the route. Things that are stored in the git repo are not included.

import os
import sys
import fnmatch
import datetime
import zipfile


def find_assets_to_pack(search_path, file_matches):
    pack_assets = []
    for file_path, file_match in file_matches:
        for directory in [x[0] for x in os.walk(f"{search_path}/{file_path}")]:
            for file_name in os.listdir(directory):
                if fnmatch.fnmatch(file_name, file_match):
                    source_file = f"{directory}/{file_name}"
                    destination_file = f"{directory}/{file_name}".replace(f"{search_path}/", "")
                    pack_assets.append((source_file, destination_file))
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
        for idx, (source_file, destination_file) in enumerate(assets_to_pack):
            print(f"Packed {idx + 1} of {len(assets_to_pack)} assets.", end='\r')
            try:
                zipf.write(source_file, destination_file)
            except FileNotFoundError:
                print(f"File not found: {source_file}")



if __name__ == "__main__":
    current_date = datetime.date.today().strftime("%Y-%m-%d")
    search_path = ".."
    export_path = ".."
    export_filename = f"DK24_Assets_{current_date}.zip"
    export_file = f"{export_path}/{export_filename}"

    file_matches = [
        ("", "default.fbk"),
        ("", "train.exe"),
        ("DATA", "*.csv"),
        ("GLOBAL/SHAPES", "*.s"),
        ("GLOBAL/SHAPES", "*.sd"),
        ("GLOBAL/SHAPES", "lightmat.pal"),
        ("GLOBAL/TEXTURES", "*.ace"),
        ("GLOBAL/TEXTURES", "*.dds"),
        ("ROUTES/OR_DK24/SHAPES", "*.s"),
        ("ROUTES/OR_DK24/SHAPES", "*.sd"),
        ("ROUTES/OR_DK24/SOUND", "*.sms"),
        ("ROUTES/OR_DK24/SOUND", "*.wav"),
        ("ROUTES/OR_DK24/TEXTURES", "*.ace"),
        ("ROUTES/OR_DK24/TEXTURES", "*.dds"),
        ("ROUTES/OR_DK24/TERRAIN_MAPS", "*.png"),
        ("ROUTES/OR_DK24/TERRTEX", "*.ace"),
        ("ROUTES/OR_DK24/TERRTEX", "*.dds"),
        ("ROUTES/OR_DK24/TILES", "*.t"),
        ("ROUTES/OR_DK24/TILES", "*.raw"),
        ("ROUTES/OR_DK24/TRACKPROFILES", "*.stf"),
        ("ROUTES/OR_DK24/TRACKPROFILES_TEST", "*.stf"),
        ("ROUTES/OR_DK24/WORLD", "*.dtbak"),
        ("ROUTES/OR_DK24TEST/SHAPES", "*.s"),
        ("ROUTES/OR_DK24TEST/SHAPES", "*.sd"),
        ("ROUTES/OR_DK24TEST/SOUND", "*.sms"),
        ("ROUTES/OR_DK24TEST/SOUND", "*.wav"),
        ("ROUTES/OR_DK24TEST/TEXTURES", "*.ace"),
        ("ROUTES/OR_DK24TEST/TEXTURES", "*.dds"),
        ("ROUTES/OR_DK24TEST/TERRAIN_MAPS", "*.png"),
        ("ROUTES/OR_DK24TEST/TERRTEX", "*.ace"),
        ("ROUTES/OR_DK24TEST/TERRTEX", "*.dds"),
        ("ROUTES/OR_DK24TEST/TILES", "*.t"),
        ("ROUTES/OR_DK24TEST/TILES", "*.raw"),
        ("ROUTES/OR_DK24TEST/TRACKPROFILES", "*.stf"),
        ("ROUTES/OR_DK24TEST/TRACKPROFILES_TEST", "*.stf"),
        ("ROUTES/OR_DK24TEST/WORLD", "*.dtbak"),
        ("SOUND", "*.sms"),
        ("SOUND", "*.wav"),
        ("TRAINS/CONSIST", "*"),
        ("TRAINS/TRAINSET", "*"),
    ]
    
    ensure_directory_exists(export_path)
    remove_file_if_exists(export_file)
    
    assets_to_pack = find_assets_to_pack(search_path, file_matches)
    pack_assets(assets_to_pack)