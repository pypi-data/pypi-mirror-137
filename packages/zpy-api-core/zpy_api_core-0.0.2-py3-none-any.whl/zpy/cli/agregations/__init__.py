import logging

from .agregations import adds


def get_last_import(lines):
    index = 0
    for i in range(0, len(lines)):
        if "import" in lines[i] or "from" in lines[i]:
            index = i
    return index + 1


def add_config(db):
    print("Add database configuration...")
    di_path = "./src/di.py"
    print("Searching for dependencies file...")

    try:
        with open(di_path, "r+") as f:
            lines = f.readlines()
            codes = adds.get("di.py").get("code")
            imports_to_add = []
            for line_toad in codes["imports"]:
                to_add = True
                for line in lines:
                    if line.strip("\n\r\t") == line_toad.strip("\n\r\t"):
                        to_add = False
                        break
                if to_add is True:
                    imports_to_add.append(line_toad)
            final_lines = codes.get("blocks")
            final_lines = imports_to_add + final_lines
            index = get_last_import(lines)
            old1 = lines[:index]
            old = lines[index + 1:]
            f.seek(0)
            f.truncate(0)
            f.writelines(old1)
            f.writelines(final_lines)
            f.writelines(old)
        print("Configuration added into di.py...")
        print(
            "Execute: \n\n\tvirtualenv venv\n\t./venv/Scripts/activate\n\tpip install -r requirements.txt\n\tConfigure environment variables\n\tpython ./src/local_deploy.py")
    except Exception as e:
        logging.exception(e)
