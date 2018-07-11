#!/usr/bin/env python

from __future__ import print_function

import sys
import pprint
import argparse
import inspect
from jira.client import JIRA

from lib import subissues
# from lib import google_calendar
from utils.smart_argparse_formatter import SmartFormatter

import jiraconfig as conf

# helpers

def _make_jql_argument_parser(parser):
    parser.add_argument("jql", help="the JQL query used in the command")
    return parser

# commands

def list_projects(jira, args):
    """List available JIRA projects"""
    projects = jira.projects()
    print("Available JIRA projects:")
    pprint.pprint([project.name for project in projects])

def list_fields(jira, args):
    """List available JIRA field names and IDs"""
    print("Available JIRA fields (name, id):")
    pprint.pprint([(field['name'], field['id']) for field in jira.fields()])

def export_from_jql(jira, args):
    """Prints a Markdown-compatible tree of epics, 
    stories, subtasks, bugs, issues that match the given JQL query"""
    results = subissues.list_epics_stories_and_tasks(jira, args.jql)
    print("ok")

export_from_jql.argparser = _make_jql_argument_parser

# main

def _main():
    command_name, command = _get_command()
    args = _parse_command_specific_arguments(command_name, command)
    jira = JIRA({'server': conf.JIRA['server']}, # add 'verify': False if HTTPS cert is untrusted
                basic_auth=(conf.JIRA['user'], conf.JIRA['password']))
    command(jira, args)

# helpers

def _make_main_argument_parser():
    parser = argparse.ArgumentParser(formatter_class=SmartFormatter)
    parser.add_argument("command", help="R|the command to run, available " +
            "commands:\n{0}".format(_list_local_commands()))
    return parser

def _get_command():
    argparser = _make_main_argument_parser()
    def print_help_and_exit():
        argparser.print_help()
        sys.exit(1)
    if len(sys.argv) < 2:
        print_help_and_exit()
    command_name = sys.argv[1]
    if not command_name[0].isalpha():
        print_help_and_exit()
    if command_name not in globals():
        print("Invalid command: {0}\n".format(command_name), file=sys.stderr)
        print_help_and_exit()
    command = globals()[command_name]
    return command_name, command

def _list_local_commands():
    sorted_globals = list(globals().items())
    sorted_globals.sort()
    commands = [(var, obj.__doc__) for var, obj in sorted_globals
        if not var.startswith('_')
           and inspect.isfunction(obj)]
    return "\n".join("'{0}': {1}".format(name, doc) for name, doc in commands)

def _parse_command_specific_arguments(command_name, command):
    if not hasattr(command, 'argparser'):
        return None
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help=command_name)
    command_argparser = command.argparser(parser)
    return command_argparser.parse_args()

if __name__ == "__main__":
    _main()
