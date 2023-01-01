import os
import subprocess
import glob
import re
import argparse

HOME = os.path.expanduser('~') + '/'
CONFIG_DIR = os.getenv('XDG_CONFIG_HOME') + '/'
CACHE_DIR = os.getenv('XDG_CACHE_HOME') + '/'


def init_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'colorscheme', nargs='?', help='Path to the colorscheme file.')
    parser.add_argument(
        'output_dir', nargs='?', default=CONFIG_DIR + "colorer/out/", help='Where to put the generated config files.')
    parser.add_argument(
        'templates_dir', nargs='?', default=CONFIG_DIR + "colorer/templates", help='Where the templates are')
    parser.add_argument(
        'commands_path', nargs='?', default=CONFIG_DIR + "colorer/commands", help='File containing commands to run at the end.')
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
            with open(CACHE_DIR + "colorer_colorscheme", "r") as file:
                COLORSCHEME = file.read()
        except:
            raise FileExistsError('Please specify a colorscheme.')
    else:
        COLORSCHEME = os.path.abspath(os.path.expanduser(colorscheme_path))
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


def replace_line(string, dictionary, comment_if_undef=False, verbose=False):
    # Replaces line with corresponding keys
    # comment_if_undef: comments (with #) the line if some keys were found but not defined in the colorscheme
    # This is used in the commands part to avoid that weird bash commands are runned.
    pattern = re.compile(r'{(.+?)}')
    search = re.findall(pattern, string)
    for i in search:
        if i in dictionary.keys():
            string = re.sub("{"+i+"}", dictionary[i], string)
        elif comment_if_undef:
            if verbose:
                print(f"{string} was commented out.")
            return "# " + string
    return string


def write_to_files(dictionary, templates_directory, output_directory, verbose):
    # write files from templates
    if verbose:
        print('Writing files to {}'.format(output_directory))
    for file in glob.iglob(templates_directory + '/*'):
        if verbose:
            print(file)
        with open(file, 'r') as input_flux:
            with open(output_directory + '/' + file.split('/')[-1], "w+") as output_flux:
                for line in input_flux:
                    new_line = replace_line(line, dictionary)
                    output_flux.write(new_line)

    with open(CACHE_DIR + "colorer_colorscheme", "w+") as file_flux:
        file_flux.write(dictionary['colorscheme'])


def run_commands(dictionary, output_path, verbose):
    # Run the commands given
    commands = ''
    with open(output_path, 'r') as file_flux:
        for line in file_flux:
            command = replace_line(line, dictionary, True)
            commands += command
    with open(CACHE_DIR + "colorer_commands", "w+") as file_flux:
        file_flux.write(commands)

    if verbose:
        print('Run commands in {}'.format(output_path))
        print(commands)
        subprocess.Popen(CACHE_DIR + "colorer_commands")
    else:
        subprocess.Popen(CACHE_DIR + "colorer_commands",
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    args = init_parser()
    # load colors
    dictionary = load_colorscheme(args.colorscheme)

    if args.get is not None:
        print_value(args.get, dictionary)
    else:
        write_to_files(dictionary, args.templates_dir,
                       args.output_dir, args.verbose)
        run_commands(dictionary, args.commands_path, args.verbose)


if __name__ == '__main__':
    main()
