# export-jira

Python app that uses the JIRA API to export JIRA in markdown format 
that are not possible with filters or gadgets in JIRA web UI.

Heavily based on the `Ask Jira` project from mrts: https://github.com/mrts/ask-jira.git

Features:

* `export_from_jql`: prints a Markdown-compatible tree
  of epics, stories, subtasks, bugs, issues that match the given JQL query

* `list_projects`: List available JIRA projects (mainly for testing)

* `list_fields`: List available JIRA field names and IDs, useful to get the internal names used by JIRA

## Installation

1. Clone this project
1. cd into the project
1. `virtualenv venv`
1. `. venv/scripts/activate`
1. `pip install --requirement=requirements.txt`
1. EDIT `jiraconfig.py` (you can use jiraconfig-sample.py as example)
1. Call `./export-jira.py list_projects` to test your settings are working (this will print available projects)

JIRA server configuration is picked up from `jiraconfig.py`.

## Usage

Run the command with 

    $ ./export-jira.py <command> <command-specific parameters>

Here's the default help:

    $ ./export-jira.py
    usage: export-jira.py [-h] command

    positional arguments:
     command   the command to run, available commands:
               'export_from_jql': prints a Markdown-compatible tree of epics, stories, subtasks, bugs, issues that match the given JQL query
               'list_fields': List available JIRA field names and IDs
               'list_projects': List available JIRA projects
               
    optional arguments:
      -h, --help  show this help message and exit

## Examples

    # export Project PROJ
    ./export-jira.py export_from_jql 'project = PROJ and sprint in openSprints() and status = Closed' > PROJ.MD

    ./export-jira.py export_from_jql 'project = PROJ and type = Epic' > PROJ2.MD
