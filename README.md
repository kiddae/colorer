# `colorer`: a tool to manage colorschemes and template config files

`colorer` uses colorscheme files and template configuration files to manage colorschemes and switch between them easily.

## Usage

In `~/.config/colorer/colorschemes/`, put the colorscheme files, which are simply text files

In ``~∕.config/colorer/templates/``, put the template configuration files. Where you want to use a color from the colorscheme (or any other keyword), put the keyword name in brackets: `{color1}`

You can run `colorer <colorscheme name>` to set the colorscheme. Your generated configuration files will be in `~/.cache/colorer`. You can now `ln` them or include them into your configs!

You can add commands to be run with `colorer` by modifying the script.

## Example configuration files

You can find colorschemes [here](https://github.com/ngynLk/colorer-colorschemes) and template configuration files [here](https://github.com/ngynLk/colorer-templates) (it includes `sequences` which can be used to update all the terminal colorschemes automatically by writing it to `/dev/pts/[0-9]`)

## Troubleshoot

Any fixes to common errors will be added here.
