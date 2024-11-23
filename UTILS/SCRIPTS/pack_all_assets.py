# Exports all DK24 assets into a zip file, even those that are not used.

import os
import sys
import fnmatch
import datetime
import zipfile

search_path = "D:\\D"
export_path = "D:\\D"
export_filename = "DK24_Assets_" + datetime.date.today().strftime("%Y-%m-%d") + ".zip"
export_file = "%s\\%s" % (export_path, export_filename)

pack_file_regexes = [
    ("GLOBAL\\SHAPES", "*.s"),
    ("GLOBAL\\SHAPES", "*.sd"),
    ("GLOBAL\\TEXTURES", "*.ace"),
    ("GLOBAL\\TEXTURES", "*.dds"),
    ("ROUTES\\OR_DK24\\SHAPES", "*.s"),
    ("ROUTES\\OR_DK24\\SHAPES", "*.sd"),
    ("ROUTES\\OR_DK24\\SOUND", "*.sms"),
    ("ROUTES\\OR_DK24\\SOUND", "*.wav"),
    ("ROUTES\\OR_DK24\\TEXTURES", "*.ace"),
    ("ROUTES\\OR_DK24\\TEXTURES", "*.dds"),
    ("ROUTES\\OR_DK24\\TERRAIN_MAPS", "*.png"),
    ("ROUTES\\OR_DK24\\TERRTEX", "*.ace"),
    ("ROUTES\\OR_DK24\\TERRTEX", "*.dds"),
    ("ROUTES\\OR_DK24\\TILES", "*.t"),
    ("ROUTES\\OR_DK24\\TILES", "*.raw"),
    ("SOUND", "*.sms"),
    ("SOUND", "*.wav"),
]

pack_files = []

for file_path, file_regex in pack_file_regexes:
    for directory in [x[0] for x in os.walk("%s\\%s" % (search_path, file_path))]:
        for file_name in os.listdir(directory):
            if fnmatch.fnmatch(file_name, file_regex):
                pack_files.append((file_path, file_name))
                print('Found %d assets.' % (len(pack_files)), end='\r')

if not os.path.exists(export_path): 
    os.makedirs(export_path)

if os.path.exists(export_file): 
    os.remove(export_file)

pack_files = list(set(pack_files))

with zipfile.ZipFile(export_file, "a", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
    for file_path, file_name in pack_files:
        print('Packed %d of %d assets.' % (pack_files.index((file_path, file_name)) + 1, len(pack_files)), end='\r')
        source_file = "%s\\%s\\%s" % (search_path, file_path, file_name)
        destination_file = "%s\\%s" % (file_path, file_name)
        try:
            zipf.write(source_file, destination_file)
        except FileNotFoundError:
            print("File not found: %s" % (source_file))
