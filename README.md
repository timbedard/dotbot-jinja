# Jinja2 Templates for Dotbot

Generate files from templates.

## Installation

Add this repo as a submodule to your dotfiles repo:

`git submodule add https://github.com/timbedard/dotbot-stow`

Modify your `install` script:

```bash
"${BASEDIR}/${DOTBOT_DIR}/${DOTBOT_BIN}" -d "${BASEDIR}" --plugin-dir dotbot-jinja -c "${CONFIG}" "${@}"
```

## Usage
