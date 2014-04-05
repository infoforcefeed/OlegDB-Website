#!/usr/bin/env python2
from os import listdir
import re

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
            , "What sets OlegDB apart from Leading NoSQL Data Solution X&trade;?"
            , "What other projects do you like?"
            ],
            "answers":
            [ "No. We use this everyday for all of our projects."
            , "\"My goal is to outrank redis with one of the worst OSS products on the free market.\"<p class=\"italic\">Kyle Terry, Senior Developer</p>"
            , "Yeah, sure whatever."
            , "Yes, most definitely."
            , "Well, we're trend-setters. Clearly our way of accomplishing things just hasn't been accepted yet."
            , "We'd rather not be a contributor to the <a href=\"http://en.wikipedia.org/wiki/Year_2038_problem\">Year 2038 problem.</a>"
            , "We were. Never really made it past that."
            , "With our stubborn dedication to quality, C and a lack of experience, we bring a unique perspective to an otherwise ugly and lacking marketplace. Arbitrary decisions, a lack of strong leadership and internal arguments haved turned the project into a double-edged sword, ready to cut into anyone and anything."
            ,
            """ We like every flavor-of-the-week database. Here are a couple:
            <ul>
                <li><a href="http://fallabs.com/kyotocabinet/">Kyoto Cabinet</a></li>
                <li><a href="http://redis.io/">Redis</a></li>
                <li><a href="http://www.postgresql.org/">PostgreSQL</a></li>
                <li><a href="http://sphia.org/">Sophia</a></li>
                <li><a href="http://www.actordb.com/">ActorDB</a></li>
                <li><a href="https://github.com/shuttler/nessDB">NessDB</a></li>
            </ul>
            """
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

    oleg_header.close()

    key_raw_code = [x for x in context['DEFINE'] if x['name'] == 'KEY_SIZE'][0]['raw_code']
    extracted_ks = key_raw_code.split(' ')[2].strip()
    context['EXTRACTED_KEY_SIZE'] = extracted_ks

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
        to_write = to_write[0] + context.get(to_write[1].strip(), '<h1>SOMETHINGWENTWRONG</h1>') + to_write[2]

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
                        beginning = line.split("xXx")[0]
                        end = line.split("xXx")[2]
                        block_name = line.split("xXx")[1].strip()
                        block_data = file_yo['blocks'].get(block_name, "")
                        to_write = beginning + block_data + end

                output.write(to_write if "core" not in to_write else to_write)
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

def _loop_context_interpolate(variable, loop_variable, current_item, i):
    if variable[1] == 'i':
        # i is special, it is an itervar
        muh_list =  context.get(variable[0], None)
        return muh_list[i] if muh_list else ""
    elif variable[1].isdigit():
        # They are trying to index a list
        return context.get(variable[0], None)[int(variable[1])]
    elif variable[0] == loop_variable:
        return current_item[variable[1]]
    # All else fails try to use the dict variable
    return current_item[variable[1]]

def _render_loop(loop_obj):
    loop_list = loop_obj["loop_list"]
    loop_str = loop_obj["loop_str"]
    loop_variable = loop_obj["loop_variable"]
    #outer_loop_variable = loop_obj["outer_loop_variable"]

    temp_loop_str = ""
    regex = re.compile("xXx (?P<variable>[a-zA-Z_0-9\$]+) xXx")
    wombat = re.compile("xXx LOOP (?P<variable>[a-zA-S_]+) (?P<fancy_list>[a-zA-S_\$]+) xXx(?P<subloop>.*)xXx BBL xXx")
    shattered_loops = wombat.split(loop_str)
    if len(shattered_loops) != 1:
        print "BEEP BEEP BEEP SUBLOOP DETECTED"

    i = 0
    for thing in context[loop_list]:
        # Lookit these higher order functions, godDAMN
        def loop_func(x):
            if x == 'i':
                return str(i)
            elif x == "BBL":
                return ""
            elif x == loop_variable:
                return str(thing)
            elif "$" in x and x in regex.findall(loop_str):
                #fUcK
                y = x.split("$")
                if y[0] == loop_variable and y[1].isdigit():
                    return thing[int(y[1])]
                return _loop_context_interpolate(y, loop_variable, thing, i)
            return x
        broken_man = regex.split(shattered_loops[0])
        for chunk in broken_man:
            bro = loop_func(chunk)
            temp_loop_str = temp_loop_str + "".join(bro)
        if len(shattered_loops) != 1:
            # HACKIEST SHIT THAT EVER HACKED
            context[shattered_loops[2]] = thing["params"]
            temp_loop_str = temp_loop_str + _render_loop(loop_obj["loop_subloop"])
            if shattered_loops[4] != "":
                broken_man = regex.split(shattered_loops[4])
                for chunk in broken_man:
                    bro = loop_func(chunk)
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

        loop_stack = None
        active_loops = 0
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
                active_loops = active_loops + 1
                print "We've entered timeskip {}!".format(variables[1])
                if loop_stack is None:
                    loop_stack = {
                        "loop_depth": active_loops,
                        "loop_variable": variables[0],
                        "loop_str": "",
                        "loop_list": variables[1],
                        "loop_subloop": None
                    }
                else:
                    #ThIs WoRkS FoR MoRe ThAn TwO LoOpS
                    def recurse_bro(item):
                        if item is None:
                            loop_stack["loop_subloop"] = {
                                "loop_depth": active_loops,
                                "loop_variable": variables[0],
                                "loop_str": "",
                                "loop_list": variables[1],
                                "loop_subloop": None
                            }
                        else:
                            recurse_bro(item["loop_subloop"])
                    recurse_bro(loop_stack)

            elif "xXx BBL xXx" == stripped:
                active_loops = active_loops - 1
                if active_loops == 0:
                    temp_loop_str = _render_loop(loop_stack)
                    # AsSuMe WeRe In A bLoCk
                    block_str = block_str + temp_loop_str
                    # wE DoNe LoOpIn NoW
                    loop_stack = None
            elif "xXx" in stripped and reading_block is True:
                if '@' in stripped:
                    line = stripped = _interpolate(stripped.replace("@", ""), {})
            elif "xXx" in stripped and reading_block is False:
                reading_block = True
                lstripped = line.split("xXx")
                block_name = lstripped[1].strip()
                block_str = lstripped[0]
                end_str = lstripped[2]
            if active_loops == 0 and reading_block is True and "xXx" not in stripped:
                block_str = block_str + line
            if active_loops > 0:
                def recurse_bro(item):
                    if item is not None:
                        if item["loop_depth"] <= active_loops:
                            if "xXx LOOP" in stripped and item["loop_depth"] != active_loops:
                                item["loop_str"] = item["loop_str"] + stripped
                            elif "xXx LOOP" not in stripped:
                                item["loop_str"] = item["loop_str"] + stripped
                            recurse_bro(item["loop_subloop"])
                recurse_bro(loop_stack)

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

