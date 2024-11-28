import os
import fnmatch

#	Static (
#		UiD ( 307 )
#		FileName ( NR_Emb1t4000r1d.s )
#		Position ( -1002.91 10.1105 46.6427 )
#		QDirection ( 0.002627 0.8786 -0.004832 -0.4776 )
#	)

def find_world_files(search_directory):
  world_files = []
  for file_name in os.listdir(search_directory):
      if fnmatch.fnmatch(file_name, "*.w"):
          world_files.append("%s\\%s" % (search_directory, file_name))
          #print('Found %d world files.' % (len(world_files)), end='\r')
  return world_files

def translate_heights(world_file, shape_name_regex, delta_height):
  file_text = ""
  was_changed = False

  print(world_file)

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
    #print("Changed")
    changed_file_text = '\n'.join(lines)
    #print(changed_file_text)
    with open(world_file, 'w', encoding='utf-16') as file:
      file.write(changed_file_text)

# for each worldfile
#   for each line
#     check if Static
#     get next 4 lines
#     for each next four lines
#       if startswith Position
#         get position
#       if startswith FileName
#         should_replace = true/false
#     if should_replace
#       replace line
#   if was_changed
#     save world file

def replace_text_in_file(file_path, search_exp, replace_exp):
    with open(file_path, 'r', encoding='utf-16') as file:
      file_text = file.read()
    file_text = file_text.replace(search_exp, replace_exp)
    


if __name__ == "__main__":
    search_path = "D:\\Games\\Open Rails\\Content\\Denmark\\ROUTES\\OR_DK24\\WORLD"
    shape_name_regex = "NR_*"
    delta_height = -0.07
    
    world_files = find_world_files(search_path)

    for world_file in world_files:
      translate_heights(world_file, shape_name_regex, delta_height)