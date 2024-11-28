import os
import fnmatch

def find_world_files(search_directory):
  world_files = []
  for file_name in os.listdir(search_directory):
      if fnmatch.fnmatch(file_name, "*.w"):
          world_files.append("%s\\%s" % (search_directory, file_name))
  return world_files

def translate_heights(world_file, shape_name_regex, delta_height):
  file_text = ""
  was_changed = False

  with open(world_file, 'r', encoding='utf-16') as file:
    file_text = file.read()

  lines = file_text.split("\n")

  for line_idx in range(0, len(lines)):
    line = lines[line_idx]
    if "Static (" in line:
      from_idx = line_idx + 1
      to_idx = line_idx + 5
      next_lines = lines[from_idx:to_idx]

      should_replace = False
      original_height = 0.0

      for next_line in next_lines:
        if "FileName (" in next_line:
          if fnmatch.fnmatch(next_line.split(" ")[2], shape_name_regex):
            should_replace = True
        if "Position (" in next_line:
          original_height = float(next_line.split(" ")[3])

      if should_replace:
        was_changed = True
        for next_line in next_lines:
          if "Position (" in next_line:
            replace_line_idx = line_idx + next_lines.index(next_line) + 1
            tokens = lines[replace_line_idx].split(" ")
            tokens[3] = str(original_height + delta_height)
            lines[replace_line_idx] = " ".join(tokens)

  if was_changed:
    changed_file_text = '\n'.join(lines)

    with open(world_file, 'w', encoding='utf-16') as file:
      file.write(changed_file_text)



if __name__ == "__main__":
    search_path = "D:\\Games\\Open Rails\\Content\\Denmark\\ROUTES\\OR_DK24\\WORLD"
    shape_name_regex = "NR_*"
    delta_height = -0.07
    
    world_files = find_world_files(search_path)

    for world_file in world_files:
      translate_heights(world_file, shape_name_regex, delta_height)