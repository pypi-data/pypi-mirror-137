import re


def vals_from(content: str):
    global var
    for i in content.split("\n"):
        var = None
        match i:
            case "":
                pass
            case i if re.search(r"^[a-zA-Z_]+=\d+$", i) or re.search(r'^[a-zA-Z_]+="[^"]*"$', i):
                var_name = i.split("=")[0]
                exec(f"global var\n{i}\nvar={var_name}")
                globals()[var_name] = var
            case i if re.search(r"^[a-zA-Z_]+=[a-zA-Z_]+$", i):
                var_name = i.split("=")[0]
                exec(f"global var\n"
                     f"try:\n"
                     f"\t{i}\n"
                     f"\tvar={var_name}\n"
                     f"except NameError:\n"
                     f"\tprint('Error in statement: {i}')")
                globals()[var_name] = var
            case i if re.search(r"^[a-zA-Z_]+=%math\((.*)\)$", i):
                var_name = i.split("=")[0]
                i = i.replace("^", "**")
                statement = re.search(r"^[a-zA-Z_]+=%math\((.*)\)$", i).group(1)
                exec(f"global var\n"
                     f"try:\n"
                     f"\t{var_name}={statement}\n"
                     f"\tvar={var_name}\n"
                     f"except SyntaxError:\n"
                     f"\tprint('Error in statement: {i}')")
                globals()[var_name] = var
                pass
