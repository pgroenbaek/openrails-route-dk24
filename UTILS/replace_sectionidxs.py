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
import fnmatch


def replace_sectionidx(world_file: str, replace_greater_than: int = 49999, replace_with: int = 0) -> None:
    pattern = r"(SectionIdx\s*\(\s*)(\d+)(\s*\))"

    print(f"Processing {world_file}")

    with open(world_file, 'r', encoding='utf-16-le') as file:
        text = file.read()
    
    def replace_match(match):
        value = int(match.group(2))
        if value > replace_greater_than:
            print(f"Found match in {world_file}")
            return f"{match.group(1)}{replace_with}{match.group(3)}"
        else:
            return match.group(0)

    text = re.sub(pattern, replace_match, text)

    with open(world_file, 'w', encoding='utf-16-le') as file:
      file.write(text)


def find_world_files(search_directory: str) -> List[str]:
    world_files = []
    for file_name in os.listdir(search_directory):
        if fnmatch.fnmatch(file_name, "*.w"):
            world_files.append(f"{search_directory}\{file_name}")
    return world_files


if __name__ == "__main__":
    search_path = "../ROUTES/OR_DK24/WORLD"
    replace_greater_than = 49999
    replace_with = 0
    
    world_files = find_world_files(search_path)

    for world_file in world_files:
      replace_sectionidx(world_file, replace_greater_than, replace_with)