
"""
    core/aesthetics.py

    useful and fancy design in terminal

    here you can
        - asciify text
        - color asciified text
        - color normal text

    author: @alexzander
"""


impressive_fonts = [
    "bell",
    "big",
    "broadway",
    "bubble",
    "chunky",
    "contessa",
    "cursive",
    "cyberlarge",
    "cybermedun",
    "cybersmall",
    "digital",
    "doh",
    "doom",
    "double",
    "drpepper",
    "epic",
    "fender",
    "kban",
    "l4me",
    "larry3d",
    "ogre",
    "rectangles",
    "shadow",
    "slant",
    "small",
    "smkeyboard",
    "speed",
    "standard",
    "weird"
]


def asciify(text, font=None):
    """ puts 2 lines of spaces
         after the modified text. """


    if type(text) != str:
        text = str(text)
    if font and font not in impressive_fonts:
        raise FileNotFoundError

    text = "+".join(text.split())

    if font:
        url_parameters = f"/make?text={text}&font={font}"
    else:
        url_parameters = f"/make?text={text}"

    url = "http://artii.herokuapp.com"
    import requests
    response = requests.get(url + url_parameters)
    if response.status_code != 200:
        raise ConnectionError("status code: {}".format(response.status_code))

    ascii_art = response.text
    items = ascii_art.split("\n")

    # deleting last 2 lines from the big text
    items = items[:len(items) - 2]
    # inserting "\n" because in original text it didnt exist
    items[len(items) - 1] += "\n"
    # reconstructing
    ascii_art = "\n".join(items)
    return ascii_art


def shift_left_ascii(ascii_text, size):
    """ left shift the big text with specified
        before:
        BIG_TEXT
        after:
        --------->(size) BIG_TEXT
    """
    if type(size) != int:
        raise TypeError

    if type(ascii_text) != str:
        raise TypeError

    if not "\n" in ascii_text:
        raise ValueError

    lines = ascii_text.split("\n")
    lines = [" " * size + line for line in lines]
    lines = "\n".join(lines)
    return lines


def shift_right_ascii(ascii_text, size):
    if type(size) != int:
        raise TypeError

    if type(ascii_text) != str:
        raise TypeError

    if not "\n" in ascii_text:
        raise ValueError

    lines = ascii_text.split("\n")
    lines = [line[size:] for line in lines]
    lines = "\n".join(lines)
    return lines


# text effects
endc_effect = "\033[0m"
bold_effect = "\033[1m"
underlined_effect = "\033[4m"
reversed_effect = "\u001b[7m"


ansi_codes = {
    'purple': '\033[95m',
    'blue': '\033[94m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'endc': '\033[0m',
    'bold': '\033[1m',
    'underlined': '\033[4m',
    'white': "\u001b[37;1m",
    "cyan": '\x1b[38;5;44m',
    "darkcyan": '\033[36m',
    "magenta": "\033[35m",
    "black": "\033[30m",
    "grey": "\x1b[38;5;246m",
    "orange": "\x1b[38;5;208m",
    "brown": "\033[94m",
    "italic": "\033[3m",
}


import re
import itertools


class ColorManager:
    def __init__(self):

        self.ESC, self.RESET, self.STYLE, self.END = "\033", "[0", "[", "m"
        self.FOREGROUND, self.BACKGROUND = "[38;5;", "[48;5;"
        self.hex_prefix, self.hex_hash = '0x', '#'
        self.lo_8_colors = ['000000', '800000', '008000', '808000', '000080', '800080', '008080', 'c0c0c0']
        self.hi_8_colors = ['808080', 'ff0000', '00ff00', 'ffff00', '0000ff', 'ff00ff', '00ffff', 'ffffff']
        self.increments = (0x00, 0x5f, 0x87, 0xaf, 0xd7, 0xff)
        self.color_matrix_increments = range(95, 256, 40)

        self.styles_list = ['normal', 'bold', 'dim', 'italic', 'underline', 'blink', 'reverse']
        self.style_values = [value for value in range(8) if value != 6]
        self.styles = dict(zip(self.styles_list, self.style_values))

        self.basic_16 = self.lo_8_colors + self.hi_8_colors
        self.strip_regex = r'(..)(..)(..)'

        self.color_cube = self.color_cube_matrix()
        self.string_color_cube = self.string_color_cube_matrix()
        self.ansi_256 = self.ansi_256_dict()

    def strip_hash(self, rgb_string):
        return rgb_string.lstrip(self.hex_hash) if rgb_string.startswith(self.hex_hash) else rgb_string

    def reset(self):
        return "%s%s%s" % (self.ESC, self.RESET, self.END)

    def style(self, text_style=None):
        _pre = "%s%s" % (self.ESC, self.STYLE)
        if not text_style and text_style != 0:
            return ""
        if isinstance(text_style, int):
            return "%s%s%s" % (_pre, text_style, self.END) if text_style in self.style_values else ""
        elif isinstance(text_style, str) and text_style in self.styles_list:
            try:
                return "%s%s%s" % (_pre, self.styles[text_style], self.END)
            except IndexError:
                return ""
        else:
            return ""

    def color_cube_matrix(self):
        hex_list = ["00"]
        for value in self.color_matrix_increments:
            hex_list.append(hex(value).lstrip(self.hex_prefix))
        rgb_hex_lists = [hex_list] * 3
        return list(itertools.product(*rgb_hex_lists))

    def string_color_cube_matrix(self):
        color_cube_values = list()
        for entry in self.color_cube:
            color_cube_values.append(''.join([hex_value for hex_value in entry]))
        return color_cube_values

    def ansi_16_dict(self):
        ansi_16_colors = dict()
        for index_value in range(16):
            ansi_16_colors.update({str(index_value): self.basic_16[index_value]})
        return ansi_16_colors

    def ansi_216_dict(self):
        ansi_216_colors = dict()
        basic_216 = self.string_color_cube
        for index_value in range(216):
            ansi_216_colors.update({str(index_value + 16): basic_216[index_value]})
        return ansi_216_colors

    def ansi_256_dict(self):
        return {**self.ansi_16_dict(), **self.ansi_216_dict()}

    def closest_rgb(self, rgb_value_string):
        stripped_rgb = re.split(self.strip_regex, self.strip_hash(rgb_value_string))[1:4]
        stripped_rgb = [int(value, 16) for value in stripped_rgb]
        closest_r_g_b = list()
        for _color in stripped_rgb:
            _index = 0
            while _index < len(self.increments) - 1:
                smaller, bigger = self.increments[_index], self.increments[_index + 1]
                if smaller <= _color <= bigger:
                    _smaller, _bigger = abs(smaller - _color), abs(bigger - _color)
                    closest = smaller if _smaller < _bigger else bigger
                    closest_r_g_b.append(closest)
                    break
                _index += 1
        closest_r_g_b = ''.join([('%02.x' % _idx) for _idx in closest_r_g_b])
        return closest_r_g_b

    def closest_ansi(self, rgb_value_string):
        ansi_viable_rgb = self.closest_rgb(rgb_value_string)
        key = next(key for key, value in self.ansi_256.items() if value == ansi_viable_rgb)
        return key

    def rgb_to_ansi(self, fg_rgb, bg_rgb=None):
        fg_rgb = self.closest_ansi(fg_rgb)
        _fg = "%s%s%s%s" % (self.ESC, self.FOREGROUND, fg_rgb, self.END)
        if bg_rgb:
            bg_rgb = self.closest_ansi(bg_rgb)
            _bg = "%s%s%s%s" % (self.ESC, self.BACKGROUND, bg_rgb, self.END)
            return "%s%s" % (_bg, _fg)
        return _fg

    def ansi_to_rgb(self, ansi_value):
        return self.ansi_256[str(ansi_value)]

    def rgb(self, fg, bg=None, style=None):
        ansi_string = self.rgb_to_ansi(fg, bg)
        return self.reset() + self.style(style) + ansi_string

    def ansi(self, ansi_fg, ansi_bg=None, style=None):
        style = self.style(style) if style else ""
        _fg = "%s%s%s%s" % (self.ESC, self.FOREGROUND, str(ansi_fg), self.END)
        if ansi_bg:
            _bg = "%s%s%s%s" % (self.ESC, self.BACKGROUND, str(ansi_bg), self.END)
            return self.reset() + style + "%s%s" % (_bg, _fg)
        return self.reset() + style + _fg

color_manager = ColorManager()

def color(string: str, hex_code: str):
    if hex_code.startswith("#"):
        hex_code = hex_code[1:]
    string = str(string)
    ansi_color = color_manager.rgb(hex_code)
    return ansi_color + string + endc_effect

class AnsiCodes:
    purple = '\x1b[95m'
    blue = '\x1b[94m'

    green = '\x1b[92m'
    green_background = "\u001b[42m"
    lime_green = "\x1b[38;5;184m"

    reversed_effect = "\u001b[7m"

    yellow = '\x1b[93m'
    red = '\x1b[91m'
    red_background = "\x1b[48;5;1m"

    # to reset the pipeline
    endc = '\x1b[0m'
    reset = '\x1b[0m'
    # both are identical

    bold = '\x1b[1m'
    underlined = '\x1b[4m'

    white = '\x1b[37;1m'
    white_yellow = "\x1b[38;5;15m"

    cyan = '\x1b[38;5;44m'
    darkcyan = '\x1b[36m'
    magenta = '\x1b[35m'
    black = '\x1b[30m'
    grey = '\x1b[38;5;246m'
    orange = '\x1b[38;5;208m'

    @staticmethod
    def get_all_color_names():
        return list(ansi_codes.keys())

    @staticmethod
    def get_all_color_values():
        return list(ansi_codes.values())

    @staticmethod
    def get_all_pairs():
        return [ tuple(pair) for pair in ansi_codes.items() ]



def ansi_colored(red, green, blue, string):
    if type(red) != int or \
       type(green) != int or \
       type(blue) != int or \
       type(string) != str:
        raise TypeError(red, green, blue, string)

    return "\x1b[{};{};{}m{}{}".format(red, green, blue, string, endc_effect)


def underlined(string):
    if type(string) != str:
        try:
            string = str(string)
        except:
            raise TypeError
    return ansi_codes["underlined"] + string + endc_effect


def bold(string):
    if type(string) != str:
        try:
            string = str(string)
        except:
            raise TypeError(string)

    return ansi_codes["bold"] + string + endc_effect


def ConsoleColored(string, color, bold=0, underlined=0):
    if type(string) != str:
        try:
            string = str(string)
        except Exception as error:
            print(error)
            message = red + ansi_codes["bold"] + 'type of param @string should be str.' + endc_effect
            raise TypeError(message)
            del message

    # incorrect color
    if color not in ansi_codes and color != 'random':
        message = red + ansi_codes["bold"] + 'this color "{}" is not in ANSICodesDICT.'.format(color) + endc_effect
        raise NotImplementedError(message)
        del message

    # bold == 0 and underlined == 0
    if not bold and not underlined:
        if color == "random":
            from random import choice
            return ansi_codes[choice(list(ansi_codes.keys()))] + string + endc_effect

        return ansi_codes[color] + string + endc_effect

    # bold == 0 and underlined == 1
    elif not bold and underlined:
        if color == "random":
            from random import choice
            return ansi_codes[choice(list(ansi_codes.keys()))] + \
                ansi_codes["underlined"] + string + endc_effect

        return ansi_codes[color] + ansi_codes["underlined"] + string + endc_effect

    # bold == 1 and underlined == 0
    elif bold and not underlined:
        if color == "random":
            from random import choice
            return ansi_codes[choice(list(ansi_codes.keys()))] + \
                ansi_codes["bold"] + string + endc_effect

        return ansi_codes[color] + ansi_codes["bold"] + string + endc_effect

    # bold == 1 and underlined == 1
    if color == "random":
        from random import choice
        return ansi_codes[choice(list(ansi_codes.keys()))] + \
            ansi_codes["bold"] + ansi_codes["underlined"] + string + endc_effect

    return ansi_codes[color] + ansi_codes["bold"] + ansi_codes["underlined"] + string + endc_effect


def print_ansi_table():
    import sys
    print("\n")
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
        print (u"\u001b[0m")
    print("\n")



import re
ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

def delete_ansi_codes(string):
    string = str(string)
    return ansi_escape.sub("", string)


# ---------------------------------------------------------
# printing colored

def print_red(__string):
    print(ConsoleColored(__string, "red"))


def print_blue(__string):
    print(ConsoleColored(__string, "blue"))


def print_yellow(__string):
    print(ConsoleColored(__string, "yellow"))


def print_orange(__string):
    print(ConsoleColored(__string, "orange"))


def print_purple(__string):
    print(ConsoleColored(__string, "purple"))


def print_cyan(__string):
    print(ConsoleColored(__string, "cyan"))


def print_green(__string):
    print(ConsoleColored(__string, "green"))


# ---------------------------------------------------------
# printing colored UNDERLINED

def print_red_underlined(__string):
    print(ConsoleColored(__string, "red", underlined=1))


def print_blue_underlined(__string):
    print(ConsoleColored(__string, "blue", underlined=1))


def print_yellow_underlined(__string):
    print(ConsoleColored(__string, "yellow", underlined=1))


def print_orange_underlined(__string):
    print(ConsoleColored(__string, "orange", underlined=1))


def print_purple_underlined(__string):
    print(ConsoleColored(__string, "purple", underlined=1))


def print_cyan_underlined(__string):
    print(ConsoleColored(__string, "cyan", underlined=1))


def print_green_underlined(__string):
    print(ConsoleColored(__string, "green", underlined=1))


# ---------------------------------------------------------
# printing colored BOLD

def print_red_bold(__string):
    print(ConsoleColored(__string, "red", bold=1))


def print_blue_bold(__string):
    print(ConsoleColored(__string, "blue", bold=1))


def print_yellow_bold(__string):
    print(ConsoleColored(__string, "yellow", bold=1))


def print_orange_bold(__string):
    print(ConsoleColored(__string, "orange", bold=1))


def print_purple_bold(__string):
    print(ConsoleColored(__string, "purple", bold=1))


def print_cyan_bold(__string):
    print(ConsoleColored(__string, "cyan", bold=1))


def print_green_bold(__string):
    print(ConsoleColored(__string, "green", bold=1))


# ---------------------------------------------------------
# printing colored  BOLD + UNDERLINED

def print_red_bold_underlined(__string):
    print(ConsoleColored(__string, "red", bold=1, underlined=1))


def print_blue_bold_underlined(__string):
    print(ConsoleColored(__string, "blue", bold=1, underlined=1))


def print_yellow_bold_underlined(__string):
    print(ConsoleColored(__string, "yellow", bold=1, underlined=1))


def print_orange_bold_underlined(__string):
    print(ConsoleColored(__string, "orange", bold=1, underlined=1))


def print_purple_bold_underlined(__string):
    print(ConsoleColored(__string, "purple", bold=1, underlined=1))


def print_cyan_bold_underlined(__string):
    print(ConsoleColored(__string, "cyan", bold=1, underlined=1))


def print_green_bold_underlined(__string):
    print(ConsoleColored(__string, "green", bold=1, underlined=1))


# ---------------------------------------------------------
# returning colored

def italic(__string: str):
    if not isinstance(__string, str):
        __string = str(__string)

    return ansi_codes["italic"] + __string + ansi_codes["endc"]


def print_italic(__string: str):
    print(italic(__string))


def grey(__string: str):
    return ConsoleColored(__string, "grey")


def yellow(__string):
    return ConsoleColored(__string, "yellow")


def orange(__string):
    return ConsoleColored(__string, "orange")


def purple(__string):
    return ConsoleColored(__string, "purple")


def cyan(__string):
    return ConsoleColored(__string, "cyan")


def green(__string):
    return ConsoleColored(__string, "green")


def red(__string):
    return ConsoleColored(__string, "red")


def blue(__string):
    return ConsoleColored(__string, "blue")


# ---------------------------------------------------------
# returning colored UNDERLINED

def yellow_underlined(__string):
    return ConsoleColored(__string, "yellow", underlined=1)


def orange_underlined(__string):
    return ConsoleColored(__string, "orange", underlined=1)


def purple_underlined(__string):
    return ConsoleColored(__string, "purple", underlined=1)


def cyan_underlined(__string):
    return ConsoleColored(__string, "cyan", underlined=1)


def green_underlined(__string):
    return ConsoleColored(__string, "green", underlined=1)


def red_underlined(__string):
    return ConsoleColored(__string, "red", underlined=1)


def blue_underlined(__string):
    return ConsoleColored(__string, "blue", underlined=1)


# ---------------------------------------------------------
# returning colored BOLD

def yellow_bold(__string):
    return ConsoleColored(__string, "yellow", bold=1)


def orange_bold(__string):
    return ConsoleColored(__string, "orange", bold=1)


def purple_bold(__string):
    return ConsoleColored(__string, "purple", bold=1)


def cyan_bold(__string):
    return ConsoleColored(__string, "cyan", bold=1)


def green_bold(__string):
    return ConsoleColored(__string, "green", bold=1)


def red_bold(__string):
    return ConsoleColored(__string, "red", bold=1)


def blue_bold(__string):
    return ConsoleColored(__string, "blue", bold=1)


# ---------------------------------------------------------
# returning colored BOLD + UNDERLINED

def yellow_bold_underlined(__string):
    return ConsoleColored(__string, "yellow", bold=1, underlined=1)


def orange_bold_underlined(__string):
    return ConsoleColored(__string, "orange", bold=1, underlined=1)


def purple_bold_underlined(__string):
    return ConsoleColored(__string, "purple", bold=1, underlined=1)


def cyan_bold_underlined(__string):
    return ConsoleColored(__string, "cyan", bold=1, underlined=1)


def green_bold_underlined(__string):
    return ConsoleColored(__string, "green", bold=1, underlined=1)


def red_bold_underlined(__string):
    return ConsoleColored(__string, "red", bold=1, underlined=1)


def blue_bold_underlined(__string):
    return ConsoleColored(__string, "blue", bold=1, underlined=1)



def red_background(__string):
    __string = str(__string)
    return AnsiCodes.red_background + __string + AnsiCodes.endc


def white_yellow(__string):
    __string = str(__string)
    return AnsiCodes.white_yellow + __string + AnsiCodes.endc


def lime_green(__string) -> str:
    __string = str(__string)
    return AnsiCodes.lime_green + __string + AnsiCodes.endc


def print_lime_green(__string) -> None:
    __string = str(__string)
    print(lime_green(__string))


def lime_green_bold(__string):
    __string = str(__string)
    return AnsiCodes.lime_green + AnsiCodes.bold + __string + AnsiCodes.endc


def lime_green_bold_underlined(__string):
    __string = str(__string)
    return AnsiCodes.lime_green + AnsiCodes.bold + AnsiCodes.underlined + __string + AnsiCodes.endc


def lime_green_underlined(__string):
    __string = str(__string)
    return AnsiCodes.lime_green + AnsiCodes.underlined + __string + AnsiCodes.endc


def print_lime_green_bold(__string):
    __string = str(__string)
    print(lime_green_bold(__string))


def print_lime_green_bold_underlined(__string):
    __string = str(__string)
    print(lime_green_bold_underlined(__string))


def print_lime_green_underlined(__string):
    __string = str(__string)
    print(lime_green_underlined(__string))


def print_all_ansi_foregrounds():
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            color = u"\u001b[38;5;" + code + "m"
            print(color + repr(color))
        print (u"\u001b[0m")



def print_all_ansi_backgrounds():
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            color = u"\u001b[48;5;" + code + "m"
            print(color + repr(color) + "\033[0m")
        print(u"\u001b[0m")


template = \
"""
[[[[[[[[[[[[[[[|]]]]]]]]]]]]]]]
[::::::::::::::|::::::::::::::]
[::::::::::::::|::::::::::::::]
[::::::[[[[[[[:|:]]]]]]]::::::]
[:::::[        |        ]:::::]
[:::::[        |        ]:::::]
[:::::[        |        ]:::::]
[:::::[        |        ]:::::]
[:::::[        |        ]:::::]
[:::::[        |        ]:::::]
[:::::[        |        ]:::::]
[:::::[        |        ]:::::]
[:::::[        |        ]:::::]
[:::::[        |        ]:::::]
[:::::[        |        ]:::::]
[::::::[[[[[[[:|:]]]]]]]::::::]
[::::::::::::::|::::::::::::::]
[::::::::::::::|::::::::::::::]
[[[[[[[[[[[[[[[|]]]]]]]]]]]]]]]
"""

def text_insertion(text):
    # globals
    format_len = 20
    insertion_index = 9 # middle of drawing


    # index 10 for inserting
    template_lines = template.split("\n")
    template_lines = [line for line in template_lines if line != ""]

    # reducing to 3 spaces between insertion and wall
    right_wall_3_spaces = "[:::::[   "
    left_wall_3_spaces = "   ]:::::]"
    for index in range(len(template_lines)):
        if template_lines[index] == "[:::::[        |        ]:::::]":
            template_lines[index] = "{}|{}".format(right_wall_3_spaces, left_wall_3_spaces)

    # splitting by "|"
    template_lines_sections = []
    for line in template_lines:
        left, right = line.split("|")
        template_lines_sections.append((left, right))


    def FormatText(text):
        """ reads a @text and formats the lines with max @format_len dimension """

        words = text.split()
        text_lines = []
        line = ""
        for word in words:
            if len(line + word + " ") <= format_len:
                line += word + " "
            else:
                text_lines.append(line)
                line = word + " "

        text_lines.append(line)

        # getting rid of spaces
        for i in range(len(text_lines)):
            text_lines[i] = text_lines[i].strip()

        return text_lines

    # shapes
    def CuttedSquareTextInsertion(text):
        """ reads a @text and inserts it in the @template drawing based on its length

            example:

            [[[[[[[[[[[[[[[       ]]]]]]]]]]]]]]]
            [::::::::::::::       ::::::::::::::]
            [::::::::::::::       ::::::::::::::]
            [::::::[[[[[[[:       :]]]]]]]::::::]
            [:::::[                       ]:::::]
            [:::::[                       ]:::::]
            [:::::[                       ]:::::]
            [:::::[                       ]:::::]
            [:::::[                       ]:::::]
            [:::::[   my name is andrew   ]:::::]
            [:::::[                       ]:::::]
            [:::::[                       ]:::::]
            [:::::[                       ]:::::]
            [:::::[                       ]:::::]
            [:::::[                       ]:::::]
            [::::::[[[[[[[:       :]]]]]]]::::::]
            [::::::::::::::       ::::::::::::::]
            [::::::::::::::       ::::::::::::::]
            [[[[[[[[[[[[[[[       ]]]]]]]]]]]]]]]
        """

        text_length = len(text)
        final_result = ""
        if text_length <= format_len:
            for index, line in enumerate(template_lines_sections):
                if index == insertion_index:
                    final_result += line[0] + text + line[1] + "\n"
                else:
                    if line[1] != left_wall_3_spaces:
                        final_result += line[0] + " " * (format_len - 13) + line[1] + "\n"
                    else:
                        final_result += line[0] + " " * (text_length) + line[1] + "\n"
        else:
            text_formated_list = FormatText(text)
            line_max_length = max(map(len, text_formated_list))

            max_possible_len_for_line = len(right_wall_3_spaces * 2) + line_max_length

            for index, line in enumerate(template_lines_sections):
                if index == insertion_index:
                    for formated_line in text_formated_list:
                        formated_line = formated_line.center(line_max_length, " ")
                        final_result += line[0] + formated_line + line[1] + "\n"
                else:
                    space = max_possible_len_for_line - len(line[0] + line[1])
                    space = " " * space
                    final_result += line[0] + space + line[1] + "\n"

        return final_result
    return CuttedSquareTextInsertion(text)

# ================= SYMBOLS SECTION =====================


# ↵
enter_symbol = chr(8629)
# ═
equal_symbol = chr(9552)
# ═┳═
latteral_connection_symbol = chr(9552) + chr(9523) + chr(9552)
# ┗═
down_right_connection_symbol = chr(9495) + chr(9552)
# ⋘
triple_left_shift = chr(8920)
# ⋙
triple_right_shift = chr(8921)


# [
left_bracket_cyan = ConsoleColored("[", "cyan", bold=1)
# ]
right_bracket_cyan = ConsoleColored("]", "cyan", bold=1)


# -
dash_orange = ConsoleColored("-", "red", bold=1)


# <
left_arrow_blue = ConsoleColored("<", "blue", bold=1)
# <
left_arrow_yellow = ConsoleColored("<", "yellow", bold=1)
# >
right_arrow_blue = ConsoleColored(">", "blue", bold=1)
# >
right_arrow_yellow = ConsoleColored(">", "yellow", bold=1)

# >>>
left_arrow_3_green_bold = green_bold(">>>")

thicc_line = "▬"

fancy_line = "▬▬▬▬▬▬▬▬▬ஜ۩۞۩ஜ▬▬▬▬▬▬▬▬▬"
fancy_title = "▬▬▬▬▬▬▬▬▬ஜ۩۞  {title} ۞۩ஜ▬▬▬▬▬▬▬▬▬"


# ================= SYMBOLS SECTION =====================


from ._rich import error
from ._rich import success
from ._rich import warning

# TERMINAL INDEPENDENT COLORS
# colors that are using RGB algo

import re

def hex_to_rgb(hx, hsl=False):
    """Converts a HEX code into RGB or HSL.
    Args:
        hx (str): Takes both short as well as long HEX codes.
        hsl (bool): Converts the given HEX code into HSL value if True.
    Return:
        Tuple of length 3 consisting of either int or float values.
    Raise:
        ValueError: If given value is not a valid HEX code."""
    if re.compile(r'#[a-fA-F0-9]{3}(?:[a-fA-F0-9]{3})?$').match(hx):
        div = 255.0 if hsl else 0
        if len(hx) <= 4:
            return tuple(int(hx[i]*2, 16) / div if div else
                         int(hx[i]*2, 16) for i in (1, 2, 3))
        return tuple(int(hx[i:i+2], 16) / div if div else
                     int(hx[i:i+2], 16) for i in (1, 3, 5))
    raise ValueError(f'"{hx}" is not a valid HEX code.')

class RGBColors:
    # https://stackoverflow.com/a/70599663/12172291
    class DefaultTheme:
        # \u001b == \x1b (they are the same)
        blue_ocean = "\x1b[38;2;38;199;186m"
        yellow_dark = "\u001b[38;2;200;179;1m"
        yellow_bright = "\u001b[38;2;230;186;52m"
        lime_green = "\u001b[38;2;168;230;52m"
        blue_dark = "\x1b[38;2;38;129;199m"
        red = "\u001b[38;2;205;70;77m"
        cyan = "\u001b[38;2;101;200;179m"
        blue = "\u001b[38;2;70;142;205m"
        purple = "\u001b[38;2;186;70;205m"
        magenta = "\u001b[38;2;205;70;164m"
        orange = "\u001b[38;2;230;114;52m"
        green_pine = "\x1b[38;2;38;199;87m"
        gray = "\u001b[38;2;108;108;108m"
        endc = "\u001b[0m"


    # class AtomOneDarkTheme:
    #     yellow = "\u001b[38;2;200;179;1m"
    #     red = "\u001b[38;2;205;70;77m"
    #     cyan = "\u001b[38;2;101;200;179m"
    #     endc = "\u001b[0m"
    #     blue = "\u001b[38;2;70;142;205m"

    # class GruvboxTheme:
    #     yellow = "\u001b[38;2;200;179;1m"
    #     red = "\u001b[38;2;205;70;77m"
    #     cyan = "\u001b[38;2;101;200;179m"
    #     endc = "\u001b[0m"
    #     blue = "\u001b[38;2;70;142;205m"

    _themes = {
        "default": DefaultTheme,
        "onedark": "AtomOneDarkTheme",
        "gruvbox": "GruvboxTheme"
    }

    def __init__(self, theme: str = "default"):
        if theme not in self._themes:
            raise NotImplementedError("theme is not themes list")

        self.theme = self._themes[theme]


    def red(self, _string: str) -> str:
        return self.theme.red + _string + self.theme.endc


    def print_red(self, _string: str):
        print(self.red(_string))


    def yellow_bright(self, _string: str) -> str:
        return self.theme.yellow_bright + _string + self.theme.endc

    def print_yellow_bright(self, _string: str):
        print(self.yellow_bright(_string))




# TESTING
if __name__ == '__main__':
    # print(asciify("hello"))
    print(fancy_title.format(title="Python"))
    # print(thicc_line * 100)
    # print(italic("some string"))
    # print("something")
    print_italic("some_string")

    warning("salutare")
    warning("salutare")

    error("salutare")
    error("salutare")

    success("salutare")
    success("salutare")

