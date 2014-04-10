# Heres a joke for you:
# Q: Whats the difference between interpolate and parse_variable?
# A: Militant confusion.

def parse_variable(variable_variables):
    split = variable_variables.strip().split("xXx")[1].strip()
    kill_splitter = split.split("=", 1)
    var_name = kill_splitter[0]
    value = kill_splitter[1]
    return (var_name, value)

def interpolate(line, file_meta, context):
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

