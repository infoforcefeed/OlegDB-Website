#!/usr/bin/env python3
from os import listdir
from json import dumps

TEMPLATE_DIR = "templates/"
BUILD_DIR = "built/"

def _parse_variable(variable_variables):
    split = variable_variables.strip().split("xXx")[1].strip()
    var_name = split.split("=")[0]
    value = split.split("=")[1]
    return (var_name, value)

def _parse_variable(variable_variables):
    split = variable_variables.strip().split("xXx")[1].strip()
    var_name = split.split("=")[0]
    value = split.split("=")[1]
    return (var_name, value)

def _interpolate(line, file_meta):
    to_write = line
    to_write = to_write.strip().split("xXx")
    if "=" in to_write:
        # We FoUnD a LiNe tHaT hAs a vArIaBlE iN iT
        varname = to_write.strip().split("=")[0]
        if file_meta['vars'].get(varname):
            var = file_meta['vars'][varname]
            to_write = to_write[0] + var + to_write[2]
        else:
            to_write = to_write[0] + to_write[2]
    else:
        to_write = to_write[0] + to_write[2]

    return to_write

def _render_file(file_yo):
    if file_yo.get("children"):
        # We DoNt ReNdEr FiLeS wItH cHiLdReN
        for base_file in file_yo["children"]:
            _render_file(base_file)
    else:
        output = open(BUILD_DIR + file_yo["filename"], "w+")
        parent_file = None

        if file_yo['vars'].get("PARENT"):
            parent_file = open(file_yo['vars']['PARENT'], "r")

        in_file = open(file_yo['file'], "r")

        if parent_file:
            for line in parent_file:
                to_write = line
                if 'xXx' in line:
                    if '=' in line:
                        to_write = _interpolate(line, file_yo)
                    else:
                        # ChIlD BloCk oR SoMeThIng, Yo
                        beginning = line.strip().split("xXx")[0]
                        end = line.strip().split("xXx")[2]
                        block_name = line.strip().split("xXx")[1].strip()
                        block_data = file_yo['blocks'].get(block_name, "")
                        to_write = beginning + block_data + end

                output.write(to_write.strip())
        else:
            for line in in_file:
                to_write = line
                if 'xXx' in line:
                    to_write = _interpolate(line, file_yo)

                output.write(to_write)

        if parent_file:
            parent_file.close()
        in_file.close()
        output.close()

def main():
    all_templates = []
    for radical_file in listdir(TEMPLATE_DIR):
        if not radical_file.endswith(".html"):
            continue

        tfile = open(TEMPLATE_DIR + radical_file, "r")
        file_meta = {}
        file_meta['file'] = TEMPLATE_DIR + radical_file
        file_meta['filename'] = radical_file
        file_meta['vars'] = {}
        file_meta['blocks'] = {}

        reading_block = False
        block_str = ""
        end_str = ""
        block_name = ""
        for line in tfile:
            stripped = line.strip()
            if "xXx" in stripped and "=" in stripped:
                var = _parse_variable(line)
                file_meta['vars'][var[0]] = var[1]
            elif "xXx TTYL xXx" == stripped:
                file_meta['blocks'][block_name] = block_str + end_str
                reading_block = False
                block_str = ""
                block_name = ""
                end_str = ""
            elif "xXx" in stripped:
                reading_block = True
                lstripped = stripped.split("xXx")
                block_name = lstripped[1].strip()
                block_str = lstripped[0]
                end_str = lstripped[2]
            if reading_block is True and "xXx" not in stripped:
                block_str = block_str + stripped



        all_templates.append(file_meta)

    # BuIlD a SiCk TrEe oF TeMpLaTeS yO
    tree = {}
    for tfile in all_templates:
        if tfile['vars'].get('PARENT'):
            parent = tfile['vars']['PARENT']
            if tree.get(parent):
                tree[parent]['children'].append(tfile)
            else:
                tree[parent] = {
                        'children': [tfile]
                    }

    for base_file in tree:
        _render_file(tree[base_file])

    # BeCaUsE WhY NoT
    return 0
if __name__ == '__main__':
    main()
