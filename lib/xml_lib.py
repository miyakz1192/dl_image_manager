import xml.etree.ElementTree as ET
import argparse


class XMLOperator:
    def __init__(self):
        self.tree = None
        self.root = None

    def read(self,input_file_name):
        self.tree = ET.parse(input_file_name)
        self.root = self.tree.getroot()

    def rewrite(self,tag_name, value):
        for child in self.root.iter(tag_name):
            child.text = value

    def write(self,output_file_name):
        self.tree.write(output_file_name, encoding='UTF-8')

