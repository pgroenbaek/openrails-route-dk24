import os
import fnmatch

"""
Injects the original global tsection.dat with dynatrax super-elevation workaround entries as well as custom trackshape and tracksection entries.

Explanation:
The script reads the local tsection.dat and looks for .w files in the world folder.
Then finds any TrackObj with shape names matching '*Dynatrax-*' in the world files.
Then generates the workaround entries needed to make super-elevation work properly for Dynatrax track sections.
Then reads any custom entries defined in customtrackshapes.txt and customtracksections.txt.
Then reads the original unmodified global tsection.dat.
Then injects the trackshape entries into line 29253.
Then injects the tracksection entries into line 1730.
And finally saves the modified global tsection.dat.

"""

def read_lines(file):
  lines = []

  with open(file, 'r', encoding='utf-16') as f:
    lines = f.read().split("\n")
  
  return lines


def read_local_tsection(local_tsection_file):
  sections = []
  paths = []

  lines = read_lines(local_tsection_file)

  for line_idx in range(0, len(lines)):
    line = lines[line_idx]
    if "TrackSection (" in line:
      from_idx = line_idx + 1
      to_idx = line_idx + 2
      next_lines = lines[from_idx : to_idx]
      
      for next_line in next_lines:
        if "SectionCurve (" in next_line:
          tokens = next_line.split(" ")
          section_type = int(tokens[2])
          section_idx = int(tokens[4])
          length = float(tokens[5])
          radius = float(tokens[6])
          sections.append((section_idx, section_type, length, radius))

    elif "TrackPath (" in line:
      tokens = line.split(" ")
      section_idx = int(tokens[2])
      length = int(tokens[3])
      section_idxs = [int(x) for x in tokens[4 : 4 + length]]
      paths.append((section_idx, section_idxs))

  return sections, paths


def find_world_files(search_directory):
  world_files = []
  for file_name in os.listdir(search_directory):
      if fnmatch.fnmatch(file_name, "*.w"):
          world_files.append("%s\\%s" % (search_directory, file_name))
  return world_files


def find_dynatrax_section_idxs(world_files):
  dynatrax_section_idxs = []
  shape_name_regex = "*Dynatrax-*"

  for world_file in world_files:
    lines = read_lines(world_file)

    for line_idx in range(0, len(lines)):
      line = lines[line_idx]
      if "TrackObj (" in line:
        from_idx = line_idx + 1
        to_idx = line_idx + 8
        next_lines = lines[from_idx : to_idx]

        shape_name = None
        section_idx = 0

        for next_line in next_lines:
          if "FileName (" in next_line:
            name = next_line.split(" ")[2]
            if fnmatch.fnmatch(name, shape_name_regex):
              shape_name = name.split("\\")[-1].replace("\"", "")
          if "SectionIdx (" in next_line:
            section_idx = int(next_line.split(" ")[2])

        if shape_name is not None:
          dynatrax_section_idxs.append((shape_name, section_idx))

  return list(set(dynatrax_section_idxs))


def generate_tracksection_entry(section_idx, section_type, length, radius):
  track_section = []
  track_section.append("TrackSection ( %d" % (section_idx))
  if section_type == 0:
    track_section.append(" SectionSize ( 1.5 %f )" % (length))
  elif section_type == 1:
    track_section.append(" SectionSize ( 1.5 0 )")
    track_section.append(" SectionCurve ( %f %f )" % (radius, length / 0.01745))
  track_section.append(")")
  return track_section


def generate_trackshape_entry(section_idx, shape_name, path_section_idxs):
  track_shape = []
  track_shape.append("TrackShape ( %d" % (section_idx))
  track_shape.append(" FileName ( %s )" % (shape_name))
  track_shape.append(" NumPaths ( 1 )")
  track_shape.append(" SectionIdx ( %d 0 0 0 0 %s )" % (len(path_section_idxs), " ".join(["%d" % (x) for x in path_section_idxs])))
  track_shape.append(")")
  return track_shape


def generate_dynatrax_entries(world_files, dyntrack_sections, dyntrack_paths):
  track_sections = []
  track_shapes = []
  section_idxs_created = []
  shape_idxs_created = []

  dynatrax_sections_idxs = find_dynatrax_section_idxs(world_files)

  for shape_name, section_idx in dynatrax_sections_idxs:
    dyntrack_section = next((t for t in dyntrack_sections if t[0] == section_idx), None)
    dyntrack_path = next((t for t in dyntrack_paths if t[0] == section_idx), None)
    for path_section_idx in dyntrack_path[1]:
      dyntrack_path_section = next((t for t in dyntrack_sections if t[0] == path_section_idx), None)
      section_type = dyntrack_path_section[1]
      length = dyntrack_path_section[2]
      radius = dyntrack_path_section[3]

      if path_section_idx not in section_idxs_created:
        track_sections.extend(generate_tracksection_entry(path_section_idx, section_type, length, radius))
        section_idxs_created.append(path_section_idx)

    if path_section_idx not in section_idxs_created:
      track_sections.extend(generate_tracksection_entry(section_idx, section_type, length, radius))
      section_idxs_created.append(section_idx)

    if section_idx not in shape_idxs_created:
      track_shapes.extend(generate_trackshape_entry(section_idx, shape_name, dyntrack_path[1]))
      shape_idxs_created.append(section_idx)
  
  return track_sections, track_shapes


def get_max_idx(track_sections, track_shapes):
  section_idxs = [int(x.split(" ")[2]) for x in track_sections if "TrackSection (" in x]
  shape_idxs = [int(x.split(" ")[2]) for x in track_shapes if "TrackShape (" in x]
  
  max_section_idx = max(section_idxs + [40000])
  max_shape_idx = max(shape_idxs + [40000])

  return max_section_idx, max_shape_idx


def write_modified_global_tsection(output_tsection_file, original_tsection_file, track_sections, track_shapes):
  lines = read_lines(original_tsection_file)

  # Disable this, TSRE5 will try to increase section indexes of dyntrack in the local tsection.dat if these numbers are increased. And if so, the workaround will not work.
  #max_section_idx, max_shape_idx = get_max_idx(track_sections, track_shapes)
  
  #lines = [x.replace("TrackSections ( 40000", "TrackSections ( %d" % (max_section_idx)) for x in lines]
  #lines = [x.replace("TrackShapes ( 40000", "TrackShapes ( %d" % (max_shape_idx)) for x in lines]

  shapes_injection_line = 29253
  lines[shapes_injection_line : shapes_injection_line] = [' ']
  lines[shapes_injection_line : shapes_injection_line] = track_shapes
  lines[shapes_injection_line : shapes_injection_line] = [' ']
  lines[shapes_injection_line : shapes_injection_line] = ['_INFO(Custom DK24 shapes)']

  sections_injection_line = 1730
  lines[sections_injection_line : sections_injection_line] = [' ']
  lines[sections_injection_line : sections_injection_line] = track_sections
  lines[sections_injection_line : sections_injection_line] = [' ']
  lines[sections_injection_line : sections_injection_line] = ['_INFO(Custom DK24 track sections)']

  output_text = "\n".join(lines)
  
  with open(output_tsection_file, 'w', encoding='utf-16') as file:
    file.write(output_text)


if __name__ == "__main__":
    local_tsection_file = "D:\\Games\\Open Rails\\Content\\Denmark\\ROUTES\\OR_DK24\\tsection.dat"
    original_tsection_file = "D:\\Games\\Open Rails\\Content\\Denmark\\GLOBAL\\tsection_v38.dat"
    output_tsection_file = "D:\\Games\\Open Rails\\Content\\Denmark\\GLOBAL\\tsection.dat"
    custom_shapes_file = "D:\\Games\\Open Rails\\Content\\Denmark\\GLOBAL\\customtrackshapes.txt"
    custom_sections_file = "D:\\Games\\Open Rails\\Content\\Denmark\\GLOBAL\\customtracksections.txt"
    world_file_path = "D:\\Games\\Open Rails\\Content\\Denmark\\ROUTES\\OR_DK24\\WORLD"

    dsections, dpaths = read_local_tsection(local_tsection_file)
    world_files = find_world_files(world_file_path)

    dynatrax_sections, dynatrax_shapes = generate_dynatrax_entries(world_files, dsections, dpaths)

    print("Writing %d dynatrax sections..." % (sum('TrackSection' in s for s in dynatrax_sections)))
    print("Writing %d dynatrax shapes..." % (sum('TrackShape' in s for s in dynatrax_shapes)))

    custom_shapes = read_lines(custom_shapes_file)
    custom_sections = read_lines(custom_sections_file)

    print("Writing %d custom sections..." % (sum('TrackSection' in s for s in custom_sections)))
    print("Writing %d custom shapes..." % (sum('TrackShape' in s for s in custom_shapes)))

    custom_sections = custom_sections + dynatrax_sections
    custom_shapes = custom_shapes + dynatrax_shapes

    write_modified_global_tsection(output_tsection_file, original_tsection_file, custom_sections, custom_shapes)
