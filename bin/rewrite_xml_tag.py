#!/usr/bin/env python3

import xml.etree.ElementTree as ET
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_file_name", type=str)
parser.add_argument("output_file_name", type=str)
parser.add_argument("tag_name", type=str)
parser.add_argument("value", type=str)
args = parser.parse_args()

tree = ET.parse(args.input_file_name)
root = tree.getroot()

for child in root.iter(args.tag_name):
    child.text = args.value

tree.write(args.output_file_name, encoding='UTF-8')

