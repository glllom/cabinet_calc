import json
import os

JOB = "C:\\Users\\glebo\\PycharmProjects\\donkey\\app\\product"
with open("tools.json", "r") as f:
    tools = json.load(f)
    f.close()

main_width = 340
main_height = 400
panel_thickness = 19
_type = "N02"
_order = "example_N02"

start_code = ["G00G21G17G90G40G49G80", "G71G91.1"]
processes = {}


def finalize_code():
    code.extend(["M5", "G0 Z75", "G01 Y940 F3000"])
    code.extend(["M30"])
    file_text = f"(X = {main_width}, Y = {main_height}, Z = {panel_thickness})\n"
    file_text += f"(Front {_type})\n"
    for row in range(len(code)):
        file_text += f'N{str((row + 1) * 10)} {code[row]}' + '\n'
    return f'{file_text}%'


def create_folder(name):
    if not os.path.exists(name):
        os.mkdir(name)
    os.chdir(name)


def make_rectangle(width, height, thickness, rect, feed=3000):
    offset = rect['offset']
    depth = rect['depth']
    corners = int(rect['corners'])
    r_code = [
        f"G00 X{width - offset} Y{height - offset}F{feed}",
        f"G01 Z{thickness}F{feed}",
        f"G01 Y{height - offset - 50} Z{thickness - depth}",
        f"G01 Y{offset}",
    ]
    if corners > 0:  # corner 1
        r_code.append(f"G01 X{width - (offset - depth)} Y{offset - depth} Z{thickness}")
        r_code.append(f"G01 X{width - offset} Y{offset} Z{thickness - depth}")
        if corners == 2:
            r_code.append(f"G01 X{width - (offset+3)} Y{offset+3}")
            r_code.append(f"G01 X{width - offset} Y{offset}")
    r_code.append(f"G01 X{offset}")
    if corners > 0:  # corner 2
        r_code.append(f"G01 X{offset - depth} Y{offset - depth} Z{thickness}")
        r_code.append(f"G01 X{offset} Y{offset} Z{thickness - depth}")
        if corners == 2:
            r_code.append(f"G01 X{offset+3} Y{offset+3}")
            r_code.append(f"G01 X{offset} Y{offset}")
    r_code.append(f"G01 Y{height - offset}")
    if corners > 0:  # corner 3
        r_code.append(f"G01 X{offset - depth} Y{height - (offset - depth)} Z{thickness}")
        r_code.append(f"G01 X{offset} Y{height - offset} Z{thickness - depth}")
        if corners == 2:
            r_code.append(f"G01 X{offset+3} Y{height - (offset+3)}")
            r_code.append(f"G01 X{offset} Y{height - offset}")
    r_code.append(f"G01 X{width - offset}")
    if corners > 0:  # corner 3
        r_code.append(f"G01 X{width - (offset - depth)} Y{height - (offset - depth)} Z{thickness}")
        r_code.append(f"G01 X{width - offset} Y{height - offset} Z{thickness - depth}")
        if corners == 2:
            r_code.append(f"G01 X{width - (offset+3)} Y{height - (offset+3)}")
            r_code.append(f"G01 X{width - offset} Y{height - offset}")
    r_code.append(f"G01 Y{height - offset - 50}")
    r_code.append(f"G00 Z{thickness + 20}")

    return r_code


with open("front_types.json", "r") as f:
    front_types = json.load(f)
    for front_type, value in front_types.items():
        if front_type == _type:
            processes = value["rectangles"]
            break
os.chdir(JOB)
create_folder(_order)

for tool_set in processes:
    current_tool = tools[tool_set['tool']]
    create_folder(tool_set["tool"])
    file_name = f"{main_width}x{main_height}-Tool{tool_set['tool']}.txt"
    code = []
    code.extend(start_code)
    code.extend([f"T{tool_set['tool']}M06",
                 f"G00G43Z100.000H{tool_set['tool']}",
                 f"S{current_tool['rpm']}M03", "G94"])

    with open(file_name, "w+") as f:
        for rectangle in tool_set["offsets"]:
            if 'r_thickness' in rectangle:
                print(rectangle)
            code.extend(make_rectangle(main_width, main_height, panel_thickness, rectangle, feed=current_tool['feed']))
            # print(rectangle)
        f.write(finalize_code())
    os.chdir('..')
