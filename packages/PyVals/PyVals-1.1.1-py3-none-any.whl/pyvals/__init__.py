import re

glob = {}


def vals_from(content: str):
    global glob
    for i in content.split("\n"):
        var = None
        match i:
            case "":
                pass
            case i if re.search(r"^[a-zA-Z_]+( *)=( *)[-+]?\d+(\.\d+)?$", i):
                i = re.sub(r'\s*', '', i)
                var_name = i.split("=")[0]
                glob[var_name] = eval(i.split("=")[1])
            case i if re.search(r'^[a-zA-Z_]+( *)=( *)"[^"]*"$', i):
                i = re.sub(r'\s*=\s*"', '="', i)
                var_name = i.split("=")[0]
                glob[var_name] = eval(i.split("=")[1])
            case i if re.search(r"^[a-zA-Z_]+( *)=( *)[a-zA-Z_]+$", i):
                i = re.sub(r'\s*', '', i)
                var_name = i.split("=")[0]
                try:
                    glob[var_name] = glob[i.split("=")[1]]
                except KeyError:
                    print(f"Error in statement: {i}")
            case i if re.search(r"^[a-zA-Z_]+( *)=( *)%math\((.*)\)$", i):
                i = re.sub(r'\s*', '', i)
                var_name = i.split("=")[0]
                i = i.replace("^", "**")
                statement = re.search(r"^[a-zA-Z_]+( *)=( *)%math\((.*)\)$", i).group(3)
                try:
                    glob[var_name] = eval(statement)
                except SyntaxError:
                    print(f"Error in statement: {i}")


def register(globs):
    global glob
    glob = globs
