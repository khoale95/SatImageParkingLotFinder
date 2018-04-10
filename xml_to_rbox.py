'''
To run this: $ python3 xml_to_rbox.py foo.xml
    parses foo.xml
OR: $ python3 xml_to_rbox.py
    parses all XML files found in the current directory
    
The script will parse a roLabelImg XML file and output the .rbox of the file.

Compatible with Python 3; changing the print statements should make this 
compatible with Python 2.
'''

import sys
import math
import os
# http://docs.python.org/library/xml.etree.elementtree.html
from xml.etree import ElementTree
string = ''

def print_values(node):
    '''
        Concatenates the value of the current node.
        
        @param node - current node in the XML
    '''
    global string
    
    if node.tag == "cx":
        string += node.text + " "
    elif node.tag == "cy":
        string += node.text + " "
    elif node.tag == "w":
        string += node.text + " "
    elif node.tag == "h":
        string += node.text + " 1 "
    elif node.tag == "angle":
        string += str(round(180 - math.degrees(float(node.text)),6)) + "\n"
        
def recur_node(node, f):
    '''
        Applies function f on given node and goes down recursively to its 
        children.
        
        @param node - the root node
        @param f - function to be applied on node and its children
    '''
    if node != None:
        f(node)
        for item in node.getchildren():
            recur_node(item, f)
    else:
        return 0
        
def walkThrough ():
    '''
        Walks through the current directory and subdirectories, and converts any XML files found to
        the .rbox file format.
    '''

    root = '.'
    for dirpath, dirnames, filenames in os.walk (root):
        for file in filenames:
            if file.endswith (".xml"):
                try:
                    node_root = ElementTree.parse(file).getroot()
                except:
                    print("Could not open xml file:" + file)
                    continue
                global string
                string = ''
                recur_node(node_root, print_values)
                file = open(os.path.splitext(file)[0] + ".rbox", "w")
                file.write(string)
                file.close

def main(fileName: str = None) -> None:
    '''
        Parses the inputted file (optional), or walks through the current directory and parses
        all XML files.
        
        @param fileName - name of XML file to be parsed (optional)
    '''
    if fileName is None:
        walkThrough()
    else:
        try:
            node_root = ElementTree.parse(fileName).getroot()
        except:
            print("Could not open xml file:" + fileName)
            return -1
        global string
        string = ''
        recur_node(node_root, print_values)
        file = open(os.path.splitext(fileName)[0] + ".rbox", "w")
        file.write(string)
        file.close
    

if __name__ == "__main__":
    if len(sys.argv) == 1:
        sys.exit(main())
    else:
        sys.exit(main(sys.argv[1]))