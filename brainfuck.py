# coding: utf-8
# Python 3.6.2
# ----------------------------------------------------------------------------

import os
import sys


class Instance:

    def __init__(self):

        self.pointer = 0
        self.array = [0] * 30_000

        self.index = 0
        self.tree = []

        self.macros = {}

    def pointer_inc(self):
        ">  incrémente (augmente de 1) le pointeur."
        self.pointer += 1
        self.index += 1

    def pointer_dec(self):
        "<  décrémente (diminue de 1) le pointeur."
        self.pointer -= 1
        self.index += 1

    def byte_inc(self):
        "+   incrémente l'octet du tableau sur lequel est positionné le pointeur (l'octet pointé)."
        self.array[self.pointer] += 1
        if self.array[self.pointer] > 255:
            self.array[self.pointer] = 0
        self.index += 1

    def byte_dec(self):
        "-   décrémente l'octet pointé."
        self.array[self.pointer] -= 1
        if self.array[self.pointer] < 0:
            self.array[self.pointer] = 255
        self.index += 1

    def print(self):
        ".   sortie de l'octet pointé (valeur ASCII)."
        try: value = chr(self.array[self.pointer])
        except:
            value = "?"
        sys.stdout.write(value)
        sys.stdout.flush()
        self.index += 1

    def show(self):
        "!   sortie de la valeur de la case pointé."
        sys.stdout.write(str(self.array[self.pointer]))
        sys.stdout.flush()
        self.index += 1

    def input(self):
        ",   entrée d'un octet dans le tableau à l'endroit où est positionné le pointeur (valeur ASCII)."
        self.array[self.pointer] = ord(max(input(), "\n")[0])
        self.index += 1

    def begin(self):
        "[   saute à l'instruction après le ] correspondant si l'octet pointé est à 0."
        if not self.array[self.pointer]:
            for value in self.tree[self.index:]:
                self.index += 1
                if value == self.end:
                    return
        self.index += 1

    def end(self):
        "]   retourne à l'instruction après le [ si l'octet pointé est différent de 0."
        if self.array[self.pointer]:
            for value in self.tree[self.index::-1]:
                if value == self.begin:
                    return
                self.index -= 1
        self.index += 1

    @property
    def finish(self):
        return len(self.tree) <= self.index

    def run(self):
        while not self.finish:
            self.tree[self.index]()


def parse(data:str, parent:Instance = None):

    i = parent if parent else Instance()

    in_comment = False
    name_macro = ""
    history_names_macro = []

    in_macro = False
    data_macro = ""

    for char in data + " ":

        if in_comment:
            if char == "\n":
                in_comment = False
            continue

        if name_macro:
            if char in (
                "abcdefghijklmnopqrstuvwxyz"
                + "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                + "0123456789"
                + "_"
            ):
                name_macro += char
                continue
            else:
                macro = i.macros.get(name_macro[1:])
                if macro:
                    parse(macro, parent=i)
                else:
                    history_names_macro.append(name_macro[1:])
                name_macro = ""

        if in_macro:
            if char == "}":
                in_macro = False
                i.macros[history_names_macro.pop()] : str = data_macro
                data_macro = ""
            else:
                data_macro += char
                continue

        if char == ";":
            in_comment = True
        elif char == "<":
            i.tree.append(i.pointer_dec)
        elif char == ">":
            i.tree.append(i.pointer_inc)
        elif char == "+":
            i.tree.append(i.byte_inc)
        elif char == "-":
            i.tree.append(i.byte_dec)
        elif char == ".":
            i.tree.append(i.print)
        elif char == "!":
            i.tree.append(i.show)
        elif char == ",":
            i.tree.append(i.input)
        elif char == "[":
            i.tree.append(i.begin)
        elif char == "]":
            i.tree.append(i.end)
        elif char == "{":
            in_macro = True
        elif char == ":":
            name_macro = ":"

    if not parent:
        i.run()


def term_title(t):
    if os.name == "nt":
        # Windows
        os.system("title " + t)
    else:
        # Linux, Darwin (macOS, iOS, ...), *BSD
        print('\33]0;' + t + '\a', end='', flush=True)


args = sys.argv

term_title("Brainfuck")

if len(args) == 1:
    # Si l'user a juste ouvert l'executable à la main
    # args[0] = Emplacement de l'executable


    print(
         f"Interpreteur Brainfuck"
        + "\n\nEcrivez ``` pour ouvrir et fermer un bloc de texte."
    )

    data = ""
    is_multiline = False

    while True:

        if is_multiline:
            try: text = input('... ')
            except KeyboardInterrupt:
                # CTRL + C
                data = ""
                text = ""
                is_multiline = False
                pass
            except EOFError:
                # CTRL + D
                data = ""
                text = ""
                is_multiline = False
                pass
        else:
            try: text = input('\n>>> ')
            except KeyboardInterrupt:
                # CTRL + C
                print("KeyboardInterrupt")
                sys.exit()
            except EOFError:
                # CTRL + D
                sys.exit()

        if text == '```':
            is_multiline = not is_multiline

        else:
            data += (text + '\n')

        if is_multiline:
            continue

        result = parse(data)
        if result is not None:
            print(result)

        data = ""

else:
    # Si l'user a ouvert l'executable avec un fichier

    path_exe = args[0]
    path_file = args[1]

    term_title("Brainfuck - %s" % path_file)

    with open(path_file, encoding='utf-8-sig') as f:
        data = f.read()

    path_file = path_file.replace('\\', '/')
    path_exe = path_exe.replace('\\', '/')

    parse(data)

print()