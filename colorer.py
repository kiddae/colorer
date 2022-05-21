#!/usr/bin/env python3
import os
import subprocess
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
    parser.add_argument(
        '-s', '--silent', action='store_true', help='Do not print anything')
    return parser.parse_args()

def load_colorscheme(colorscheme_path, dictionary):
    if colorscheme_path is None:
        try:
            with open(HOME + ".cache/colorer_colorscheme", "r") as file:
                COLORSCHEME = file.read()
        except:
            raise FileExistsError('Please specify a colorscheme.')
    else:
        COLORSCHEME = colorscheme_path
    with open(COLORSCHEME, "r") as file_flux:
        for line in file_flux:
            key = line.split(" ")[0]
            color = line.split(" ")[1]
            color = color.replace("\n", "")
            dictionary[key] = color
    # get the 'colorscheme' keyword available
    dictionary['colorscheme'] = COLORSCHEME

def print_value(key, dictionary):
    if key == 'all':
        for i in dictionary.values():
            print(i)
    else:
        print(dictionary[key])

def replace_line(string, dictionary):
    keyword_search = re.search('{(.+?)}', string)
    if keyword_search and keyword_search.group(1) in dictionary.keys:
        return re.sub('{(.+?)}', dictionary[keyword_search.group(1)], string)
    else:
        return string

    # Replace keywords with values in a string
    # for color in dictionnary.items():
    #     if re.search("{" + color[0] + "}", string) != None:
    #         string = re.sub("{" + color[0] + "}", color[1], string)
    # return string
    
def write_to_files(dictionary, templates_directory, output_directory, silent):
    # write files from templates
    if not silent:
        print('Writing files to {}'.format(output_directory))
    for file in glob.glob(HOME + templates_directory + '/*'):
        if not silent:
            print(file)
        input_flux = open(file, "r")
        output_flux = open(HOME + output_directory + '/' + file.split("/")[-1], "w+")

        for line in input_flux:
            new_line = replace_line(line, dictionary)
            output_flux.write(new_line)

        input_flux.close()
        output_flux.close()

    with open(HOME + ".cache/colorer_colorscheme", "w+") as file_flux:
        file_flux.write(os.path.abspath(dictionary['colorscheme']))

def run_commands(dictionary, silent):
    global COMMANDS
    if not silent:
        print('Run commands in {}'.format(COMMANDS))
    commands = ''
    with open(COMMANDS, 'r') as file_flux:
        for line in file_flux:
            command = replace_line(line, dictionary)
            commands += command
    if silent:
        subprocess.Popen(commands, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
    else:
        subprocess.Popen(commands, shell=True)


def main():
    args = init_parser()
    # load colors
    colors = {}
    load_colorscheme(args.colorscheme, colors)

    if args.get is not None:
        print_value(args.get, colors)
    else:
        write_to_files(colors, args.templates_dir, args.output_directory, args.silent)
        run_commands(colors,args.silent)


'''Program'''
if __name__ == '__main__':
    main()