#!/usr/bin/env python3
import os
import subprocess
import sys
import glob
import re
import argparse

HOME = os.path.expanduser('~') + '/'
COMMANDS = HOME + '.config/colorer/commands'


def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'colorscheme', nargs='?', help='Path to the colorscheme file.')
    parser.add_argument(
        'output_dir', nargs='?', default=".config/colorer/out/", help='Where to put the generated config files.')
    parser.add_argument(
        'templates_dir', nargs='?', default=".config/colorer/templates", help='Where the templates are')
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
    if args.colorscheme is None:
        try:
            with open(HOME + ".cache/colorer_colorscheme", "r") as file:
                COLORSCHEME = file.read()
        except:
            raise FileExistsError('Please specify a colorscheme.')
    else:
        COLORSCHEME = args.colorscheme
    with open(COLORSCHEME, "r") as file_flux:
        for line in file_flux:
            key = line.split(" ")[0]
            color = line.split(" ")[1]
            color = color.replace("\n", "")
            colors[key] = color
    # get the 'colorscheme' keyword available
    colors['colorscheme'] = COLORSCHEME

    if args.get is not None:
        if args.get == 'all':
            for i in colors.values():
                print(i)
        else:
            print(colors[args.get])
    else:
        # write files from templates
        print('Writing files to {}'.format(args.output_dir))
        for file in glob.glob(HOME + args.templates_dir + '/*'):
            print(file)
            input_flux = open(file, "r")
            output_flux = open(HOME + args.output_dir + '/' + file.split("/")[-1], "w+")

            for line in input_flux:
                new_line = replace_line(line, colors)
                output_flux.write(new_line)

            input_flux.close()
            output_flux.close()

        with open(HOME + ".cache/colorer_colorscheme", "w+") as file_flux:
            file_flux.write(COLORSCHEME)
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
