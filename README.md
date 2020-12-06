# Basecamp3 CLI

A CLI interface for interacting with Basecamp. Built using
[basecampy3](https://github.com/phistrom/basecampy3) to interact with Basecamp3 API,
[Typer](https://github.com/tiangolo/typer) to parse CLI options, and [simple-term-menu](https://github.com/IngoMeyer441/simple-term-menu) for terminal menus.

## Installation
1. `source ./install.sh`  
A bit hacky, but works on linux.  
Installs requirements in a virtualenv, creates an executable app.py,
and adds an alias to ~/.bashrc


1. `$ bc3 configure`  
Requires `client_id` and `client_secret` for a Basecamp app  
*(SharpestMinds team: see 1Password)*


## Usage
After installation, should be available via `sm` alias.

`$ sm`  
Lists projects and lets user navigate TODOs with keyboard

`$ sm -p <project-name>`  
Jump to a specific project by name

#### Navigating menus
- Navigate menus with arrow keys (or `j/k`) and `enter`
- Exit with `q` or `<Ctrl>-c`
- Use `/` to search/filter menu with regex

## Roadmap
- edit tasks
- move tasks
- flag to jump to specific task-list
- browse messages and docs
