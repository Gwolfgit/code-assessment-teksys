#!/usr/bin/python3

import re
import sys
import timeit
from typing import TextIO


multi_patterns = (
    r'.+?port\s(\d+).+?',
    r'.+?Port:\s(\d+).+?',
    r'.+?s_port:\"(\d+)\".+?',
    r'.+?service:\"(\d+)\".+?',
)

single_pattern = r'service:\"(\d+)\"|s_port:\"(\d+)\"|Port:\s(\d+)|port\s(\d+)'


def extract_single_multiline_pattern(file: TextIO) -> list:
    """Extract entire file at once using a multiline regex"""
    results = []
    for x in re.findall(single_pattern, file.read(), re.MULTILINE):
        results += [
            match for match in x
            if match
        ]
    return results


def extract_multiple_patterns(file: TextIO) -> list:
    """Extract file line by line using a tuple of regex patterns"""
    results = []
    for line in file.readlines():
        for pattern in multi_patterns:
            regex = re.compile(pattern)
            results += [
                match for match in re.findall(regex, line)
            ]
    return results


def extract_single_pattern(file: TextIO) -> list:
    """Extract file line by line using a single regex pattern"""
    results = []
    regex = re.compile(single_pattern)
    for line in file.readlines():
        for x in re.findall(regex, line):
            results += [
                match for match in x
                if match
            ]
    return results


def main(path: str):
    """Main function"""

    # parses whole file at once using a single regex pattern
    # fast but could be a problem with large files
    with open(path) as file:
        print("extract_single_multiline_pattern")
        start = timeit.default_timer()
        print(extract_single_multiline_pattern(file))
        print(f"Execution took: {timeit.default_timer() - start}s\n")

    # alternatively we can parse the file line by line and
    # match using a single regex pattern
    with open(path) as file:
        print("extract_single_pattern")
        start = timeit.default_timer()
        print(extract_single_pattern(file))
        print(f"Execution took: {timeit.default_timer() - start}s\n")

    # parses file line by line and matches against a tuple of regex patterns
    # might be a useful way to manage our patterns but much slower
    with open(path) as file:
        print("extract_multiple_patterns")
        start = timeit.default_timer()
        print(extract_multiple_patterns(file))
        print(f"Execution took: {timeit.default_timer() - start}s\n")

if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        print(f"Syntax: {sys.argv[0]} ./path/to/file.log")
