#!/usr/bin/env python3

import io
import sys
import json

class handler():
    "Makes any JSON compatible with D3's hierarchy or tree chart formats (see https://d3js.org)"
    def __init__(self, input):
        # creates a write buffer
        self.output = io.StringIO()
        # Determine if we are starting with a list, dictionary, or a very small JSON file, then run the appropriate function first.
        if isinstance(input, dict):
            self.enum_dict(input)
        elif isinstance(input, list):
            self.enum_list(input)
        else:
            self.print_value(input)
        # Save the results
        self.results = self.output.getvalue()
        self.output.close()

    def enum_dict(self, input):
        first = True
        # for all key/value pairs in dictionary
        for key in input:
            if first:
                first = False
            else:
                self.output.write(',\n')
            # if item is another dictionary:
            if isinstance(input[key], dict):
                # { 'name': key, 'children': [ enum_dict ] },
                self.output.write('{ "name": "' + key + '", "children": [')
                self.enum_dict(input[key])
                self.output.write('] ')
            # if item is a list:
            elif isinstance(input[key], list):
                self.output.write('{ "name": "' + key + '", "children": ')
                # { 'name': key, 'children': enum_list },
                self.enum_list(input[key])
            # if this is a value:
            else:
                # { 'name': key, 'value': print_value },
                self.output.write('{ "name": "' + key + '",')
                self.print_value(input[key])
            self.output.write('}')

    def enum_list(self, input):
        # [
        self.output.write('[ ')
        first = True
        # for all items in the list
        for value in input:
            if first:
                first = False
            else:
                self.output.write(', ')
            # if item is a dictionary:
            if isinstance(value, dict):
                # enum_dict ,
                self.enum_dict(value)
            # if item is another list:
            elif isinstance(value, list):
                # enum_list ,
                self.enum_list(value)
            # if item is a value
            else:
                # { print_value },
                self.output.write('{ ')
                self.print_value(value)
                self.output.write(' }')
        # ]
        self.output.write(']')

    def print_value(self, input):
        # if the value is not null
        self.output.write('"value": "' + str(input) + '", ')
        self.output.write('"type": "' + str(type(input))[8:-2] + '"')

############# MAIN #################
def print_banner(text):
    print("\033[32m" + text + "\033[00m")

if __name__ == "__main__":
    if 2 <= len(sys.argv) <= 3:
        in_file = open(str(sys.argv[1]),)
        json_file = json.load(in_file)
        in_file.close()
        converter = handler(json_file)

        try:
            if sys.argv[2]:
                out_file = open(sys.argv[2], "w")
                a = out_file.write(converter.results)
                out_file.close()
        except IndexError:
            print(converter.results)

    else:
        banner = "   _                   ___ _                    \n  (_)                 /   | |                   \n   _ ___  ___  _ __  / /| | |_ _ __ ___  ___    \n  | / __|/ _ \| '_ \/ /_| | __| '__/ _ \/ _ \   \n  | \__ | (_) | | | \___  | |_| | |  __|  __/   \n  | |___/\___/|_| |_|   |_/\__|_|  \___|\___|   \n _/ |                                           \n|__/                                            \n"
        help = """DESCRIPTION:  Makes any JSON compatible with D3's hierarchy or tree chart formats (see https://d3js.org)

EXAMPLE: ./json4tree.py input.json
EXAMPLE: ./json4tree.py input.json output.json
        """
        print_banner(banner)
        print(help)
