# Exports all DK24 assets into a zip file, only those that are used in the route.

import os
import sys
import fnmatch
import datetime
import zipfile

version = "v0_1"
search_path = "D:\\D"
export_path = "D:\\D"
export_filename = "DK24_Assets_" + version + ".zip"
export_file = "%s\\%s" % (export_path, export_filename)

pack_file_regexes = [
    ("ROUTES\\OR_DK24\\SOUND", "*.sms"),
    ("ROUTES\\OR_DK24\\SOUND", "*.wav"),
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
