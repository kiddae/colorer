import os
import subprocess
import glob
import re
import argparse

HOME = os.path.expanduser('~') + '/'

def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'colorscheme', nargs='?', help='Path to the colorscheme file.')
    parser.add_argument(
        'output_dir', nargs='?', default=HOME + ".config/colorer/out/", help='Where to put the generated config files.')
    parser.add_argument(
        'templates_dir', nargs='?', default=HOME + ".config/colorer/templates", help='Where the templates are')
    parser.add_argument(
        'commands_path', nargs='?', default=HOME + ".config/colorer/commands", help='File containing commands to run at the end.')
    parser.add_argument(
        '-g', '--get', help='Get a value, don\'t set a colorscheme.')
    parser.add_argument(
        '-v', '--verbose', action='store_true', help='Print info')
    return parser.parse_args()

def load_colorscheme(colorscheme_path):
    # Returns dict with the keys, from path; if it is empty then load the colorscheme written to ~/.cache/colorer_colorscheme
    dictionary = {}
    if colorscheme_path is None:
        try:
            with open(HOME + ".cache/colorer_colorscheme", "r") as file:
                COLORSCHEME = file.read()
        except:
            raise FileExistsError('Please specify a colorscheme.')
    else:
        COLORSCHEME = os.path.abspath(colorscheme_path)
    with open(COLORSCHEME, "r") as file_flux:
        for line in file_flux:
            key = line.split(" ")[0]
            color = line.split(" ")[1]
            color = color.replace("\n", "")
            dictionary[key] = color
    # make the 'colorscheme' keyword available
    dictionary['colorscheme'] = COLORSCHEME
    return dictionary

def print_value(key, dictionary):
    # Print key from the dict, or all
    if key == 'all':
        for i in dictionary.values():
            print(i)
    else:
        print(dictionary[key])

def replace_line(string, dictionary):
    # Replaces line with corresponding keys
    pattern = re.compile(r'{(.+?)}')
    search = re.findall(pattern, string)
    for i in search:
        if i in dictionary.keys():
            string = re.sub("{"+i+"}", dictionary[i], string)
    return string
    
def write_to_files(dictionary, templates_directory, output_directory, silent):
    # write files from templates
    if not silent:
        print('Writing files to {}'.format(output_directory))
    for file in glob.iglob(templates_directory + '/*'):
        if not silent:
            print(file)
        with open(file, 'r') as input_flux:
            with open(output_directory + '/' + file.split('/')[-1], "w+") as output_flux:
                for line in input_flux:
                    new_line = replace_line(line, dictionary)
                    output_flux.write(new_line)

    with open(HOME + ".cache/colorer_colorscheme", "w+") as file_flux:
        file_flux.write(os.path.abspath(dictionary['colorscheme']))

def run_commands(dictionary, output_path, silent):
    # Run the commands given
    if not silent:
        print('Run commands in {}'.format(output_path))
    commands = ''
    with open(output_path, 'r') as file_flux:
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
    dictionary = {}
    load_colorscheme(args.colorscheme)

    if args.get is not None:
        print_value(args.get, dictionary)
    else:
        write_to_files(dictionary, args.templates_dir, args.output_directory, not args.verbose)
        run_commands(dictionary, args.commands_path, not args.verbose)

if __name__ == '__main__':
    main()