import json
import os

JOB = "C:\\Users\\glebo\\PycharmProjects\\donkey\\app\\product"
with open("tools.json", "r") as f:
    tools = json.load(f)
    f.close()
print(tools)

main_width = 450
main_height = 750
panel_thickness = 21
start_code = ["G00G21G17G90G40G49G80", "G71G91.1"]
def finalize_code():
    code.extend(["M5", "G0 Z75", "G01 X300 Y940 F5000"])
    code.extend(["M30"])
    file_text = f"(X = {main_width}, Y = {main_height}, Z = {panel_thickness})\n"
    for row in range(len(code)):
        file_text += f'N{str((row + 1) * 10)} {code[row]}' + '\n'
    return f'{file_text}%'

_type = "N01"
_order = "example"

processes = {}

def create_folder(name):
    if not os.path.exists(name):
        os.mkdir(name)
    os.chdir(name)
    

def make_rectangle(width, height, thickness, offset, depth, corners):
    r_code = [
        f"G00 X{width - offset} Y{height - offset}",
        f"G01 Z{thickness - depth}",
        f"G01 Y{offset}F2000",
    ]
    if corners == "yes":
        r_code.append(f"G01 X{width - offset + depth} Y{offset - depth} Z{thickness}")
        r_code.append(f"G01 X{width - offset} Y{offset} Z{thickness-depth}")
    r_code.append(f"G01 X{offset}")
    if corners == "yes":
        r_code.append(f"G01 X{offset - depth} Y{offset - depth} Z{thickness}")
        r_code.append(f"G01 X{width} Y{offset} Z{thickness-depth}")
    r_code.append(f"G01 Y{height - offset}")
    if corners == "yes":
        r_code.append(f"G01 X{width - depth} Y{height - offset + depth} Z{thickness}")
        r_code.append(f"G01 X{width} Y{height-offset} Z{thickness-depth}")
    r_code.append(f"G01 X{width - offset}")
    if corners == "yes":
        r_code.append(f"G01 X{width - offset + depth} Y{height - offset + depth} Z{thickness}")
    r_code.append(f"G00 Z{thickness + 20}")

    return r_code

with open("front_types.json", "r") as f:
    front_types = json.load(f)
    # print(front_types)
    for front_type, value in front_types.items():
        # print(front_type, value)
        if front_type == _type:
            processes = value["rectangles"]
            break
os.chdir(JOB)
create_folder(_order)

for tool_set in processes:
    create_folder(tool_set["tool"])
    file_name = f"{main_width}x{main_height}-Tool{tool_set['tool']}.txt"
    code = []
    code.extend(start_code)
    code.extend([f"T{tool_set['tool']}M06",
                 f"G00G43Z100.000H{tool_set['tool']}",
                 "S16000M03", "G94"])

    with open(file_name, "w+") as f:
        for rectangle in tool_set["offsets"]:
            code.extend(make_rectangle(main_width, main_height, panel_thickness, 
                                       rectangle[0], rectangle[1], tool_set["corners"]))
        f.write(finalize_code())
    os.chdir('..')
