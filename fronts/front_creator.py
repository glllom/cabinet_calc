import json
import os

JOB = "C:\\Users\\Gleb\\PycharmProjects\\donkey\\app\\product"
with open("tools.json", "r") as f:
    tools = json.load(f)
    f.close()

main_width = 300
main_height = 342
panel_thickness = 18.8
_type = "N04"
_order = "example_N04"

start_code = ["G00G21G17G90G40G49G80", "G71G91.1"]
processes = {}


def g1(x='', y='', z=''):  # Returns regular g-code G01
    return f"G01 {f'X{x}' if x != "" else ''}{f'Y{y}' if y != "" else ''}{f'Z{z}' if z != "" else ''}"


def rect(x1, y1, x2, y2, z):
    return [g1(x=(x2 + x1) / 2, y=y2, z=z),
            g1(x=x2), g1(y=y1), g1(x=x1), g1(y=y2), g1(x=(x2 + x1) / 2)]


def make_panel(x1, y1, x2, y2, thickness, dep, rc):
    if x2 - x1 <= rc or y2 - y1 <= rc:
        panel_code = [g1((x2 + x1)/2 - 15, (y2 + y1)/2, thickness+1), g1((x2 + x1)/2, (y2 + y1)/2, thickness - dep)]
    else:
        panel_code = make_panel(x1 + rc/2, y1 + rc/2, x2 - rc/2, y2 - rc/2, thickness, dep, rc)
    panel_code.extend(rect(x1, y1, x2, y2, thickness-dep))
    return panel_code


def finalize_code():
    code.extend(["M5", "G0 Z75", "G01 Y940 F4000"])
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


def make_rectangle(width, height, thickness, rect_elem, feed=3000):
    offset = rect_elem['offset']
    depth = rect_elem['depth']
    corners = int(rect_elem['corners'])
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
            r_code.append(f"G01 X{width - (offset + 3)} Y{offset + 3}")
            r_code.append(f"G01 X{width - offset} Y{offset}")
    r_code.append(f"G01 X{offset}")
    if corners > 0:  # corner 2
        r_code.append(f"G01 X{offset - depth} Y{offset - depth} Z{thickness}")
        r_code.append(f"G01 X{offset} Y{offset} Z{thickness - depth}")
        if corners == 2:
            r_code.append(f"G01 X{offset + 3} Y{offset + 3}")
            r_code.append(f"G01 X{offset} Y{offset}")
    r_code.append(f"G01 Y{height - offset}")
    if corners > 0:  # corner 3
        r_code.append(f"G01 X{offset - depth} Y{height - (offset - depth)} Z{thickness}")
        r_code.append(f"G01 X{offset} Y{height - offset} Z{thickness - depth}")
        if corners == 2:
            r_code.append(f"G01 X{offset + 3} Y{height - (offset + 3)}")
            r_code.append(f"G01 X{offset} Y{height - offset}")
    r_code.append(f"G01 X{width - offset}")
    if corners > 0:  # corner 3
        r_code.append(f"G01 X{width - (offset - depth)} Y{height - (offset - depth)} Z{thickness}")
        r_code.append(f"G01 X{width - offset} Y{height - offset} Z{thickness - depth}")
        if corners == 2:
            r_code.append(f"G01 X{width - (offset + 3)} Y{height - (offset + 3)}")
            r_code.append(f"G01 X{width - offset} Y{height - offset}")
    r_code.append(f"G01 Y{height - offset - 50}")
    r_code.append(f"G00 Z{thickness + 20}")

    return r_code


with open("front_types.json", "r") as f:
    front_types = json.load(f)
    for front_type, value in front_types.items():
        if front_type == _type:
            processes = value["rectangles"]
            if "panels" in value:
                panels = value["panels"]
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
            code.extend(make_rectangle(main_width, main_height, panel_thickness, rectangle, feed=current_tool['feed']))
        f.write(finalize_code())
    os.chdir('..')


for tool_set in panels:
    current_tool = tools[tool_set['tool']]
    create_folder(tool_set["tool"])
    file_name = f"{main_width}x{main_height}-Tool{tool_set['tool']}.txt"
    code = []
    code.extend(start_code)
    code.extend([f"T{tool_set['tool']}M06",
                 f"G00G43Z100.000H{tool_set['tool']}",
                 f"S{current_tool['rpm']}M03", "G94"])

    with open(file_name, "w+") as f:
        for offset in tool_set["offsets"]:
            code.extend(make_panel(offset["offset"], offset["offset"],
                                   main_width-offset["offset"], main_height-offset["offset"],
                                   panel_thickness, offset['depth'], 6))  #6 temp
        f.write(finalize_code())
    os.chdir('..')
