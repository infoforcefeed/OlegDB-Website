#!/usr/bin/env python3
from os import listdir
from json import dumps
from collections import deque
import re, argparse

TEMPLATE_DIR = "templates/"
BUILD_DIR = "built/"

# Question: Hey qpfiffer, why is this indented all weird?
# Man I don't know leave me alone.
context = { "questions":
            [ "Is this a joke?"
            , "Why are you doing this?"
            , "Can I use this in production?"
            , "Should I use this in production?"
            , "Why did you make X the way it is? Other people do Y."
            , "Why isn't there a 32-bit version?"
            , "Are you guys CS 100 students?"
            ],
            "answers": 
            [ "No. We use this everyday for all of our projects."
            , "\"My goal is to outrank redis with one of the worst OSS products on the free market.\"<p class=\"italic\">Kyle Terry, Senior Developer</p>"
            , "Yeah, sure whatever."
            , "Yes, most definitely."
            , "Well, we're trend-setters. Clearly our way of accomplishing things just hasn't been accepted yet."
            , "We'd rather not be a contributor to the <a href=\"http://en.wikipedia.org/wiki/Year_2038_problem\">Year 2038 problem.</a>"
            , "We were. Never really made it past that."
            ],
        }

def build_doc_context(include_dir):
    oleg_header = open("{}/oleg.h".format(include_dir))
    docstring_special = ["DEFINE", "ENUM", "STRUCT", "DESCRIPTION",
            "RETURNS", "TYPEDEF"]

    reading_docs = False
    raw_code = ""
    doc_object = {}
    prev_stripped = None
    for line in oleg_header:
        docline = False
        stripped = line.strip()
        if stripped == '*/':
            continue

        # ThIs iS sOmE wEiRd FaLlThRouGh BuLlShIt
        if reading_docs and stripped.startswith("/*"):
            raise Exception("Yo I think you messed up your formatting. Read too far.")
        if "xXx" in line and "*" in stripped[:2]:
            (variable, value) = _parse_variable(stripped)

            docline = True
            if not reading_docs:
                doc_object["name"] = value
                doc_object["type"] = variable
                doc_object["params"] = []
                reading_docs = True
            else:
                if variable in docstring_special:
                    # SpEcIaL
                    doc_object[variable] = value
                else:
                    doc_object["params"].append((variable, value))
        if reading_docs and not docline and stripped != "":
            raw_code = raw_code + line
        if stripped == "" and reading_docs:
            reading_docs = False
            doc_object["raw_code"] = raw_code
            if context.get(doc_object["type"], False):
                context[doc_object["type"]].append(doc_object)
            else:
                context[doc_object["type"]] = [doc_object]
            doc_object = {}
            raw_code = ""
        prev_stripped = stripped

    oleg_header.close()

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

                output.write(to_write.strip() if "core" not in to_write else to_write)
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

def _render_loop(loop_obj):
    loop_list = loop_obj["loop_list"]
    loop_str = loop_obj["loop_str"]
    loop_variable = loop_obj["loop_variable"]
    outer_loop_variable = loop_obj["outer_loop_variable"]

    temp_loop_str = ""
    regex = re.compile("xXx (?P<variable>[a-zA-Z_\$]+) xXx")
    broken_man = regex.split(loop_str)

    i = 0
    if not context.get(loop_list):
        import ipdb; ipdb.set_trace()
    for thing in context[loop_list]:
        # Lookit these higher order functions, godDAMN
        def loop_func(x):
            if x == 'i':
                return str(i)
            elif x == loop_variable:
                return str(thing)
            elif "$" in x and x in regex.findall(loop_str):
                #fUcK
                y = x.split("$")
                if y[1] == 'i':
                    # i is special, it is an itervar
                    muh_list =  context.get(y[0], None)
                    return muh_list[i] if muh_list else ""
                elif y[1].isdigit():
                    # They are trying to index a list
                    return context.get(y[0], None)[int(y[1])]
                elif y[0] == loop_variable:
                    return thing[y[1]]
                # All else fails try to use the dict variable
                return thing[y[1]]
            return x
        # Why doesn't Python's map return a new list?
        bro = [loop_func(x) for x in broken_man]
        temp_loop_str = temp_loop_str + "".join(bro)
        i = i + 1

    return temp_loop_str

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
        file_meta['loops'] = []

        reading_block = False
        block_str = ""
        end_str = ""
        block_name = ""

        loop_stack = deque([])
        for line in tfile:
            stripped = line.strip()
            if "xXx" in stripped and "=" in stripped.split("xXx")[1]:
                var = _parse_variable(line)
                file_meta['vars'][var[0]] = var[1]
            elif "xXx TTYL xXx" == stripped:
                file_meta['blocks'][block_name] = block_str + end_str
                reading_block = False
                block_str = ""
                block_name = ""
                end_str = ""
            # We LoOpIn BaBy
            elif "xXx LOOP " in stripped:
                variables = stripped.split("xXx")[1].strip().replace("LOOP ", "").split(" ")
                print("We've entered timeskip {}!".format(variables[1]))
                loop_stack.append({
                    "loop_variable": variables[0],
                    "loop_str": "",
                    "loop_list": variables[1]
                })

            elif "xXx BBL xXx" == stripped:
                loop = loop_stack.popleft()
                print("We're leaving timeskip {}!".format(loop["loop_list"]))
                temp_loop_str = _render_loop(loop)
                # AsSuMe WeRe In A bLoCk
                block_str = block_str + temp_loop_str
                # wE DoNe LoOpIn NoW
            elif "xXx" in stripped and reading_block is False:
                reading_block = True
                lstripped = stripped.split("xXx")
                block_name = lstripped[1].strip()
                block_str = lstripped[0]
                end_str = lstripped[2]
            if len(loop_stack) is 0 and reading_block is True and "xXx" not in stripped:
                block_str = block_str + stripped
            if len(loop_stack) > 0 and "xXx LOOP" not in stripped and "xXx BBL xXx" != stripped:
                loop_stack[-1]["loop_str"] = loop_stack[-1]["loop_str"] + stripped

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
    parser = argparse.ArgumentParser(description='Build the OlegDB website.')
    parser.add_argument('include_dir', type=str,
        help='The location of the OlegDB header files.')
    args = parser.parse_args()
    build_doc_context(args.include_dir)
    main()
