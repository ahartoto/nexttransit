# Filename: utils.py

"""
BART Utility Module
"""

# Standard libraries
from xml.dom import minidom


def print_xml_response(response):
    """
    Print the XML response to the stdout
    """
    xml_str = response.content.decode()
    print(minidom.parseString(xml_str).toprettyxml(indent="  "))
