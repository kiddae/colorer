#!/usr/bin/env python3
import os
import subprocess
import sys
import glob
import re
import argparse

HOME = os.path.expanduser('~') + '/'
CACHE_DIR = HOME + ".cache/colorer/"
TEMPLATES = glob.glob(HOME + ".config/colorer/templates/*")
COMMANDS = HOME + '.config/colorer/commands'
with open(CACHE_DIR + "colorscheme") as file:
    CURRENT = os.path.basename(os.path.normpath(file.read()))


def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'colorscheme', nargs='?', default=CURRENT, help='Name of the colorscheme (which is the same as the filename of the colorscheme)')
    parser.add_argument(
        '-g', '--get', help='Get a value, don\'t set a colorscheme.')
    return parser.parse_args()


def replace_line(string, dictionnary):
    # Replace keywords with values in a string
    for color in dictionnary.items():
        if re.search("{" + color[0] + "}", string) != None:
            string = re.sub("{" + color[0] + "}", color[1], string)
    return string


def main():
    args = init_parser()
    # load colors
    colors = {}
    with open(HOME + ".config/colorer/colorschemes/" + args.colorscheme, "r") as file_flux:
        for line in file_flux:
            key = line.split(" ")[0]
            color = line.split(" ")[1]
            color = color.replace("\n", "")
            colors[key] = color
    # get the 'colorscheme' keyword available
    colors['colorscheme'] = args.colorscheme

    if args.get is not None:
        if args.get == 'all':
            for i in colors.values():
                print(i)
        else:
            print(colors[args.get])
    else:
        # write files from templates
        print('Writing files to {}'.format(CACHE_DIR))
        for file in TEMPLATES:
            input_flux = open(file, "r")
            output_flux = open(CACHE_DIR + file.split("/")[-1], "w")

            for line in input_flux:
                new_line = replace_line(line, colors)
                output_flux.write(new_line)

            input_flux.close()
            output_flux.close()

        with open(CACHE_DIR + "colorscheme", "w") as file_flux:
            file_flux.write(
                HOME + ".config/colorer/colorschemes/" + args.colorscheme)
        # Run commands written in COMMAND, can use keywords
        print('Run commands in {}'.format(COMMANDS))
        commands = ''
        with open(COMMANDS, 'r') as file_flux:
            for line in file_flux:
                command = replace_line(line, colors)
                commands += command
        subprocess.Popen(commands, shell=True)


'''Program'''
if __name__ == '__main__':
    main()
