def read(filename):
    with open(filename, "r") as file:
        lines = file.readlines()

    result = {}

    mode = "main"
    result[mode] = {}

    for i in lines:
        i = i.replace("\n", "")

        if i.startswith("    "):
            i = i[4:]

        if i.startswith("  "):
            i = i[2:]

        if "//" in i:
            i = i.split("//")[0]

        if ":" in i:
            mode = i.split(":")[0]
            result[mode] = {}

        elif "=" in i:
            key, value = i.split("=")

            if value.replace(".", "", 1).isdigit():
                if "." in value:
                    value = float(value)

                else:
                    value = int(value)

            elif value == "true":
                value = True

            elif value == "false":
                value = False

            result[mode][key] = value

    return result

def write(filename, data):
    result = ""
    spaces = 0

    if "main" not in data:
        data = {"main" : data}

    for i in data:
        if spaces != 0:
            spaces -= 1
            result += "\n"

        result += i + ":" + "\n"

        for j in data[i]:
            value = data[i][j]

            if not isinstance(value, bool):
                if isinstance(value, int) or isinstance(value, float):
                    value = str(value)

            elif value == True:
                value = "true"

            elif value == False:
                value = "false"

            result += "    " + j + "=" + value + "\n"

        spaces += 1

    with open(filename, "w") as file:
        file.write(result)

def append(filename, data):
    if "main" not in data:
        data = {"main" : data}
        
    temp_data = data
    data = read(filename)
    data.update(temp_data)

    write(filename, data)

def change(filename, key, value):
    append(filename, {key : value})