# `colorer`: a tool to manage colorschemes and template config files

`colorer` uses colorscheme files and template configuration files to manage colorschemes and switch between them easily.

## Usage

In `~/.config/colorer/colorschemes/`, put the colorscheme files, which are simply text files

In ``~∕.config/colorer/templates/``, put the template configuration files. Where you want to use a color from the colorscheme (or any other keyword), put the keyword name in brackets: `{color1}`

You can run `colorer <colorscheme name>` to set the colorscheme. Your generated configuration files will be in `~/.cache/colorer`. You can now `ln` them or include them into your configs!

Commands to be run after can be added to `~/.config/colorer/commands`; you can also use the same keywords in there.

## Example configuration files

You can find colorschemes, templates for configuration files and commands [here](https://github.com/ngynLk/colorer-files)

## Troubleshoot

Any fixes to common errors will be added here.
