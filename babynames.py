#!/usr/bin/env python
# -*- coding: utf-8 -*-

# BabyNames python coding exercise.

# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# GitHub user:  DJJD2150
# Helped out by Jordan Davidson, Janelle Kuhns, Doug Enas, Daniel Lomelino, Kano Marvel,
# Janell Huyck, Devon Middleton, Tiffany McLean

"""
Define the extract_names() function below and change main()
to call it.

For writing regex, it's nice to include a copy of the target
text for inspiration. Here's what the HTML looks like in the
baby.html files:
...
<h3 align="center">Popularity in 1990</h3>
....
<tr align="right"><td>1</td><td>Michael</td><td>Jessica</td>
<tr align="right"><td>2</td><td>Christopher</td><td>Ashley</td>
<tr align="right"><td>3</td><td>Matthew</td><td>Brittany</td>
...

Suggested milestones for incremental development:
 - Extract all the text from the file and print it
 - Find and extract the year and print it
 - Extract the names and rank numbers and print them
 - Get the names data into a dict and print it
 - Build the [year, 'name rank', ... ] list and print it
 - Fix main() to use the extracted_names list
"""

import sys
import re
import argparse

__author__ = "helped by referencing Jackson D. later down the line."


def extract_names(filename):
    """
    Given a single file name for babyXXXX.html, returns a
    single list starting with the year string followed by
    the name-rank strings in alphabetical order.
    ['2006', 'Aaliyah 91', 'Aaron 57', 'Abagail 895', ...]
    """
    names = []
    with open(filename, "r") as f:
        # creates a variable with a list of everything in the file,
        # separated into lines
        file_lines = f.readlines()
    # adds the year to the front of the list
    # year_line = file_lines[40]
    # print(year_line)
    year = re.compile(r'Popularity\sin\s(\d\d\d\d)')
    name = re.compile(r'<td>(\d+)</td><td>(\w+)</td><td>(\w+)</td>')
    name_dict = {}
    for file_line in reversed(file_lines):
        if 'Popularity in ' in file_line:
            extracted_year = year.search(file_line)
            # print(dir(extracted_year))
            # names.insert(0, extracted_year.group(1))
        else:
            extracted_name = name.findall(file_line)
            if extracted_name:
                name_dict[extracted_name[0][1]] = extracted_name[0][0]
                name_dict[extracted_name[0][2]] = extracted_name[0][0]
                names.append(extracted_name)
    names = [x + " " + name_dict[x] for x in name_dict]
    names = sorted(names)
    names.insert(0, extracted_year.group(0)[14:18])
    # print(names)
    return names


def create_parser():
    """Create a command line parser object with 2 argument definitions."""
    parser = argparse.ArgumentParser(
        description="Extracts and alphabetizes baby names from html.")
    parser.add_argument(
        '--summaryfile', help='creates a summary file', action='store_true')
    # The nargs option instructs the parser to expect 1 or more
    # filenames. It will also expand wildcards just like the shell.
    # e.g. 'baby*.html' will work.
    parser.add_argument('files', help='filename(s) to parse', nargs='+')
    return parser


def create_summary_file(filename):
    with open(filename + ".summary", "w") as summary_file:
        text = '\n'.join(extract_names(filename)) + '\n'
        summary_file.write(text)


def main(args):
    # Create a command line parser object with parsing rules
    parser = create_parser()
    # Run the parser to collect command line arguments into a
    # NAMESPACE called 'ns'
    ns = parser.parse_args(args)

    file_list = ns.files

    # option flag
    create_summary = ns.summaryfile

    if not ns:
        parser.print_usage()
        sys.exit(1)
    elif create_summary:
        for each_file in file_list:
            create_summary_file(each_file)
    else:
        for each_file in file_list:
            print_names = '\n'.join(extract_names(each_file))
            print(print_names)

    # For each filename, call `extract_names()` with that single file.
    # Format the resulting list as a vertical list (separated by newline \n).
    # Use the create_summary flag to decide whether to print the list
    # or to write the list to a summary file (e.g. `baby1990.html.summary`).


if __name__ == '__main__':
    main(sys.argv[1:])
