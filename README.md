# `colorer`: a tool to manage colorschemes and template config files

`colorer` uses colorscheme files and template configuration files to manage colorschemes and switch between them easily.

## Usage

In `~/.config/colorer/colorschemes/`, put the colorscheme files, which are simply text files

In `~∕.config/colorer/templates/`, put the template configuration files. Where you want to use a color from the colorscheme (or any other keyword), put the keyword name in brackets: `{color1}`

You can run `colorer <colorscheme name>` to set the colorscheme. Your generated configuration files will be in `~/.config/colorer/out/`. You can now `ln` them or include them into your configs!

Commands to be run after can be added to `~/.config/colorer/commands`; you can also use the same keywords in there.

```
usage: colorer [-h] [-g GET] colorscheme [output_dir] [templates_dir]

positional arguments:
  colorscheme        Name of the colorscheme (which is the same as the
                     filename of the colorscheme)
  output_dir         Where to put the generated config files.
  templates_dir      Where the templates are

optional arguments:
  -h, --help         show this help message and exit
  -g GET, --get GET  Get a value, don't set a colorscheme.
```

## Example configuration files

You can find colorschemes, templates for configuration files and commands in my [dotfiles](https://github.com/kiddae/dotfiles)

## Installation

Clone the repo and run `./install.sh` (or run `pip3 install .`)

## Troubleshoot

Any fixes to common errors will be added here.
