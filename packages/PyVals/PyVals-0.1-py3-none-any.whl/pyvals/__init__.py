import re


def vals_from(content: str):
    for i in content.split("\n"):
        match i:
            case "":
                pass
            case i if re.search(r"^[a-zA-Z]+=\d+$", i):
                var_name = i.split("=")[0]
                global var
                var = None
                exec(f"global var\n{i}\nvar={var_name}")
                globals()[var_name] = var
