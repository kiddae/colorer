![banner](banner.png)
![demo](demo.gif)

---

**Because having to change the hex codes manually is annoying,**

`colorer` uses colorscheme files and template configuration files to manage colorschemes and switch between them easily.

## Usage

The colorscheme files are simple text files taking keywords in this format: `key: value`.

In `~∕.config/colorer/templates/`, put the template configuration files. Where you want to use a color from the colorscheme (or any other keyword), put the keyword name in brackets: `{color1}`

You can run `colorer <colorscheme filepath>` to set the colorscheme. Your generated configuration files will be in `~/.config/colorer/out/`. You can now `ln` them or include them into your configs!

Commands to be run after can be added to `~/.config/colorer/commands`; you can also use the same keywords in there.

```
usage: colorer [-h] [-g GET] [-v]
               [colorscheme] [output_dir] [templates_dir] [commands_path]

positional arguments:
  colorscheme        Path to the colorscheme file.
  output_dir         Where to put the generated config files.
  templates_dir      Where the templates are
  commands_path      File containing commands to run at the end.

options:
  -h, --help         show this help message and exit
  -g GET, --get GET  Get a value, don't set a colorscheme.
  -v, --verbose      Print info
```

## Example configuration files

You can find colorschemes in the [dedicated repository](https://github.com/kiddae/colorer-colorschemes); templates for configuration files and commands in my [dotfiles](https://github.com/kiddae/dotfiles)

## Installation

Clone the repo and run `./install.sh` (or run `pip3 install .`)

## Troubleshoot

Any fixes to common errors will be added here.
