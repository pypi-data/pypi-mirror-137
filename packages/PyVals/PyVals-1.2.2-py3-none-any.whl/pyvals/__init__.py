import re
from types import FunctionType, ModuleType
import inspect

glob = {}


def vals_from(content: str):
    global glob
    for i in content.split("\n"):
        var = None
        try:
            match i:
                case "":
                    pass
                case i if re.search(r"^[a-zA-Z_]+( *)=( *)[-+]?\d+(\.\d+)?$", i):
                    i = re.sub(r'\s*', '', i)
                    var_name = i.split("=")[0]
                    glob[var_name] = eval(i.split("=")[1])
                case i if re.search('^[a-zA-Z_]+( *)=( *)("[^"]*"|\'[^\']*\')$', i):
                    i = re.sub(r'\s*=\s*"', '="', i)
                    var_name = i.split("=")[0]
                    glob[var_name] = eval(i.split("=")[1])
                case i if re.search(r"^[a-zA-Z_]+( *)=( *)[a-zA-Z_]+$", i):
                    i = re.sub(r'\s*', '', i)
                    var_name = i.split("=")[0]
                    glob[var_name] = glob[i.split("=")[1]]
                case i if re.search(r"^[a-zA-Z_]+( *)=( *)%math\((.*)\)$", i):
                    i = re.sub(r'\s*', '', i)
                    var_name = i.split("=")[0]
                    i = i.replace("^", "**")
                    statement = re.search(r"^[a-zA-Z_]+( *)=( *)%math\((.*)\)$", i).group(3)
                    glob[var_name] = eval(statement)
                case i if re.search(r"^[a-zA-Z_]+( *)=( *)\[(.*)]$", i):
                    i = re.sub(r"\s*=\s*\[", '=[', i)
                    var_name = i.split("=")[0]
                    statement = i.split("=")[1]
                    glob[var_name] = eval(statement)
            globals().update(glob)
        except Exception:
            print(f"Error in statement: {i}")


def register(globs):
    global glob
    glob.update(globs)


def save() -> str:
    string = ""
    for i in glob:
        if not i.startswith("__") and not isinstance(glob[i], FunctionType) and i != "glob" \
                and not isinstance(glob[i], ModuleType) and not inspect.isclass(glob[i]):
            match i:
                case i if isinstance(glob[i], str):
                    string += i + " = '" + str(glob[i]) + "'\n"
                case _:
                    string += i + " = " + str(glob[i]) + "\n"
    return string
