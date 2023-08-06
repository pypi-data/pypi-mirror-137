"""
https://github.com/asciinema/asciinema/blob/develop/doc/asciicast-v2.md
"""

# from PIL import Image
# from PIL import ImageDraw


# img = Image.new("RGB", (80, 40))
# d = ImageDraw.Draw(img)
# d.text((20, 20), 'Hello', fill=(255, 0, 0))

import os, sys
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageColor
from time import sleep

from core._yaml import load_yaml_from_file
from core.aesthetics import delete_ansi_codes


# sys.stdout.write("s")
# sys.stdout.flush()
# sleep(0.5)
# sys.stdout.write("s")
# sys.stdout.flush()
# sleep(0.5)
# sys.stdout.write("s")
# sys.stdout.flush()
# sleep(0.5)
# sys.stdout.write("s")
# sys.stdout.flush()
# sleep(0.5)
# sys.stdout.write("s")
# sys.stdout.flush()
# sleep(0.5)
# sys.stdout.write("s")
# sys.stdout.flush()
# sleep(0.5)
# sys.stdout.write("s")
# sys.stdout.flush()
# sleep(0.5)
# print("s", end="")
# sleep(0.5)
# print("a", end="")
# sleep(0.5)
# print("l", end="")
# sleep(0.5)
# print("u", end="")
# sleep(0.5)
# print("t", end="")
# sleep(0.5)
# print("a", end="")
# sleep(0.5)
# print("r", end="")
# sleep(0.5)
# print("e", end="")
# sleep(0.5)



frame = ""
frames = []


terminal_lines = 43


class ANSI:
    class endc:
        code = "\x1b[00m"
        name = "endc"

    class backspace:
        code = "\x08\x1b[K"
        name = "backspace"

    class move_cursor_up:
        code = "\x1b[1A"
        name = "move_cursor_up"

    class delete_current_line:
        code = "\x1b[2K"
        name = "delete_current_line"

    # class delete_before:
    #     # ce pui inainte de asta nu se vede
    #     code = "\x1b[?2004l"
    #     name = "delete_before"

# TODO delete all of \x1b[?2004h from strings no matter what

def remove_unseenable(string: str):
    _start = "\x1b"
    _stop = "\x1b\\"
    start = string.find(_start)
    stop = string.find(_stop)
    if start == -1 or stop == -1:
        # abort
        return string

    to_replace = string[start: stop + len(_stop)]
    return string.replace(to_replace, "")

def clean(string: str):
    string = remove_unseenable(string)
    string = string.replace("\x1b[?2004h", "")
    string = string.replace("\x1b[?2004l", "")

    # remove \a which is bell
    string = string.replace("\x07", "")

    # remove \r\n windows CRLF
    string = string.replace("\r\n", "\n")
    string = string.replace("\n\r", "\n")

    return string

from core._string import find_all
from core._string import find_total

operations = []

demo_yml = load_yaml_from_file("demo.yml")
# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
records = demo_yml["records"]
for record in records:
    content = record["content"]
    # print(repr(content))
    delay = record["delay"] / 1000 # miliseconds

    # print(delete_ansi_codes(content))

    content = clean(content)
    # print(content.find("\x1b[1A\x1b[2K"))
    total = find_all(content, "\x1b[1A\x1b[2K")
    print(total)

    if "\n" in content:
        operations.append("newline")
        cont = delete_ansi_codes(content.replace("\n", ""))
        operations.append(cont)

    elif content == ANSI.backspace.code:
        operations.append(ANSI.backspace.name)

    if content.find("\x1b[1A\x1b[2K") != -1:
        # print(repr(content))
        # print(content.find("\x1b[1A\x1b[2K"))
        total = find_total(content, "\x1b[1A\x1b[2K")
        for _ in range(total):
            operations.append("delete last line")

        cont = delete_ansi_codes(content.replace("\x1b[1A\x1b[2K", ""))
        operations.append(cont)
        break
    else:
        operations.append(delete_ansi_codes(content))

    # skip empty content
    if content == "":
        continue

    sys.stdout.write(repr(content) + "\n")
    # sys.stdout.write(content)
    sys.stdout.flush()
    sleep(0.1)
    # print(frame["content"], end="")
    frame += content
    frames.append({
        "content": frame,
        "delay": delay
    })
    # break

for op in operations:
    print(op)
    sleep(0.1)




def getSize(txt, font):
    testImg = Image.new('RGB', (1, 1))
    testDraw = ImageDraw.Draw(testImg)
    return testDraw.textsize(txt, font)

if __name__ == '__main__':

    fontname = "/home/alexzander/.fonts/MonacoB2.otf"
    fontsize = 20

    text = "salutare"
    colorText = "black"
    colorOutline = "red"

    # black: "#1d1f21"
    red_hex = "#d54e53"
    # green: "#b9ca4a"
    yellow_hex = "#e7c547"
    # blue: "#81a2be"
    # magenta: "#c397d8"
    # cyan: "#70c0b1"
    # white: "#eaeaea"

    background_color = ImageColor.getrgb("#282C34")
    red = ImageColor.getrgb(red_hex)
    yellow = ImageColor.getrgb(yellow_hex)


    font = ImageFont.truetype(fontname, fontsize)
    width, height = getSize(text, font)

    img = Image.new('RGB', (1000, 800), background_color)
    d = ImageDraw.Draw(img)
    # (x, y)
    d.text((0, 0), text, fill=red, font=font)
    # img.save("image.png")





    # for index, frame in enumerate(frames):
    #     img = Image.new('RGB', (1000, 800), background_color)
    #     d = ImageDraw.Draw(img)
    #     # (x, y)
    #     d.text((0, 0), frame["content"], fill=red, font=font)
    #     # d.text((100, 0), text, fill=yellow, font=font)
    #     img.save(f"images/frame{index}.png")

