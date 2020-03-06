#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BabyNames python coding exercise.

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import sys
import re
import argparse

__author__ = """https://stackoverflow.com/questions/38093326/
                whats-the-difference-between-rb-and-ru-in-the-open-function-for-csv
                Watched Babynames demo by Piero and Chris W.
                """


"""
Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration.

Here's what the html looks like in the baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 - Extract the year and print it
 - Extract the names and rank numbers and just print them
 - Get the names data into a dict and print it
 - Build the [year, 'name rank', ... ] list and print it
 - Fix main() to use the extract_names list
"""


def extract_names(filename):
    """
    Given a single file name for babyXXXX.html, returns a single list starting
    with the year string followed by the name-rank strings
    in alphabetical order.
    ['2006', 'Aaliyah 91', Aaron 57', 'Abagail 895', ' ...]
    """
    names = []
    with open(filename) as file:
        text = file.read()

    year_matches = re.search(r'Popularity\sin\s(\d{4})', text)
    if not year_matches:
        sys.stderr("Couldn't find the year.\n")
        sys.exit(1)
    year = year_matches.group(1)
    names.append(year)

    tuples = re.findall(r'<td>(\d+)</td><td>(\w+)</td>\<td>(\w+)</td>', text)
    names_dict = {}
    for rank_tuple in tuples:
        (rank, boy_name, girl_name) = rank_tuple
        if boy_name not in names_dict:
            names_dict[boy_name] = rank
        if girl_name not in names_dict:
            names_dict[girl_name] = rank
    sorted_names = sorted(names_dict.keys())

    for name in sorted_names:
        names.append(name + " " + names_dict[name])
    print(names)
    return names


def create_parser():
    """Create a cmd line parser object with 2 argument definitions"""
    parser = argparse.ArgumentParser(
        description="Extracts and alphabetizes baby names from html.")
    parser.add_argument(
        '--summaryfile', help='creates a summary file', action='store_true')
    # The nargs option instructs the parser to expect 1 or more filenames.
    # It will also expand wildcards just like the shell,
    # e.g. 'baby*.html' will work.
    parser.add_argument('files', help='filename(s) to parse', nargs='+')
    return parser


def main(args):
    # Create a command-line parser object with parsing rules
    parser = create_parser()
    # Run the parser to collect command-line arguments
    # into a NAMESPACE called 'ns'
    ns = parser.parse_args(args)

    if not ns:
        parser.print_usage()
        sys.exit(1)

    file_list = ns.files

    for filename in file_list:
        print(f'Working on file: {filename}')
        names = extract_names(filename)

    text = '\n'.join(names)

    create_summary = ns.summaryfile

    if create_summary:
        with open(filename + '.summary', 'w') as rf:
            rf.write(text + '\n')
    else:
        print(text)

    # For each filename, call `extract_names` with that single file.
    # Format the resulting list a vertical list (separated by newline \n)
    # Use the create_summary flag to decide whether to print the list,
    # or to write the list to a summary file e.g. `baby1990.html.summary`


if __name__ == '__main__':
    main(sys.argv[1:])
