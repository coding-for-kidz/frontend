"""Compiles css so that it is smaller and takes up less bandwidth"""
from os import listdir, path
from os.path import isfile, join

from services.web.core import path as pathlib


def compile_css(text):
    """Compile css"""
    list_text = text.split("\n")
    text = ""
    for line in list_text:
        stripped_line = line.strip(" ")
        if stripped_line[0:2] != "/*":
            text += line + "\n"
    text.replace("\t", "")
    while "  " in text:
        text = text.replace("  ", " ")
    text = text.replace("\n", "  ")

    return text


def add_and_compile_css(file_list):
    compiled_css = []
    for css_file_name in file_list:
        css_file = open(str(css_path / css_file_name), "r", encoding="UTF-8")
        compiled_css.append(compile_css(css_file.read()))
        css_file.close()
    return combine_compiled_css(compiled_css)


def combine_compiled_css(compiled_files):
    """Combine multiple files that have been compiled"""
    compiled = ""
    for compiled_file in compiled_files:
        compiled += compiled_file + "  "
    return compiled


def get_file_list(directory):
    return [f for f in listdir(directory) if isfile(join(directory, f))]


# file paths
css_path = pathlib.cfk_dir() / "services" / "web" / "frontend" / "css"  # /frontend/css
loose_files_css_path = css_path / "loose_files"  # /css/loose_files/

# file lists
file_list = get_file_list(css_path)
loose_files_list = [
    f for f in listdir(loose_files_css_path) if isfile(join(loose_files_css_path, f))
]

# print file lists
for file in file_list:
    print("Found: " + file)

for file in loose_files_list:
    print("Found Loose File: " + str(file))

# compiled css path
compiled_css_path = (
        pathlib.cfk_dir() / "services" / "web" / "website" / "static" / "css"
)

# compiled css temp storage
compiled_css = add_and_compile_css(file_list)

# loose files
loose_files_compiled = {}

for item in loose_files_list:
    loose_file = open(str(loose_files_css_path / str(item)), "r", encoding="UTF-8")
    loose_files_compiled[str(item)] = compile_css(loose_file.read())
    loose_file.close()

print("\nWriting to bundle.min.css at " + str(compiled_css_path))
bundle_file_w = open(str(compiled_css_path / "bundle.min.css"), "w", encoding="UTF-8")
bundle_file_w.write(compiled_css)
bundle_file_w.close()
print(
    "Bundle Size: "
    + str(path.getsize(str(compiled_css_path / "bundle.min.css")))
    + " bytes\n"
)
print("\n")

for key in loose_files_compiled:
    key = str(key)
    print("Writing to " + key + " at " + str(compiled_css_path))
    loose_file = open(str(compiled_css_path / key), "w", encoding="UTF-8")
    loose_file.write(loose_files_compiled[key])
    loose_file.close()
    print("File Size: " + str(path.getsize(compiled_css_path / key)) + " bytes\n")
