from os import listdir
from os.path import isfile, join, splitext
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from xml.etree.ElementTree import Element
from typing import List
from pathlib import Path


@dataclass
class Card():
    name: str = ''
    age: int = 0
    displayunitcount: int = 0
    icon: str = ''
    strings: List[str] = field(default=lambda: [])


class AORXMLParser():
    def __init__(self):
        pass

    def load_all(self, directory_path: str):
        self.xml_files = self.get_all_xml_files(directory_path)
        self.load_all_xml()

    def load_all_recursive(self, directory_path: str, filename: str = ''):
        self.xml_files = [
            str(filename)
            for filename in list(Path(directory_path).rglob(filename))
        ]
        self.load_all_xml()

    def get_all_xml_files(self, directory_path: str):
        return [
            join(directory_path, f) for f in listdir(directory_path)
            if isfile(join(directory_path, f))
            and splitext(join(directory_path, f))[1] == '.xml'
        ]

    @staticmethod
    def get_element(obj, property: str):
        all_xml = obj.findall(property)
        if all_xml:
            return all_xml[0].text
        else:
            return None

    def load_xml(self, file: str):
        return ET.parse(file).getroot()

    def load_all_xml(self):
        self.roots = {}
        for file in self.xml_files:
            self.roots[file] = self.load_xml(file)


class AORTechParser(AORXMLParser):
    def __init__(self, path: str):
        AORXMLParser.__init__(self)
        self.xml = self.load_xml(path)
        self.techs = self.get_techs()

    def get_techs(self):
        return {
            child.attrib['name']: child
            for child in self.xml if child.tag == 'tech'
        }

    def get_tech(self, name: str):
        try:
            return self.techs[name]
        except KeyError:
            print(name)
            return Element('tech')


class AORStringsParser(AORXMLParser):
    def __init__(self, directory_path: str):
        AORXMLParser.__init__(self)
        self.load_all_recursive(directory_path, 'stringtabley.xml')
        self.load_strings()

    def load_strings(self):
        self.strings = {}
        for file in self.xml_files:
            language_element = self.roots[file].findall('language')[0]
            if language_element:
                for string in language_element:
                    if string.attrib['_locid'] in self.strings:
                        self.strings[string.attrib['_locid']] \
                            .append(string.text)
                    else:
                        self.strings[string.attrib['_locid']] = []
                        self.strings[string.attrib['_locid']] \
                            .append(string.text)

    def get_string(self, string_id: str):
        return self.strings[string_id]


class AORCardParser(AORXMLParser):
    def __init__(
        self,
        directory_path: str,
        tech_parser: AORTechParser,
        strings_parser: AORStringsParser
    ):
        AORXMLParser.__init__(self)
        self.tech_parser = tech_parser
        self.strings_parser = strings_parser
        self.load_all(directory_path)
        self.get_cards()

    def get_cards(self):
        self.cards_xml = {}
        self.cards = {}
        for file in self.xml_files:
            self.get_cards_element(file)
            self.cards[self.get_nation(file)] = []
            self.get_cards_cards(file)

    def get_cards_element(self, file: str):
        for child in self.roots[file]:
            if child.tag == 'cards':
                self.cards_xml[file] = child
                break

    def get_nation(self, file):
        return AORXMLParser.get_element(self.roots[file], 'civ')

    def get_cards_cards(self, file: str):
        for card in self.cards_xml[file]:
            if card.tag == 'card':
                name = AORXMLParser.get_element(card, 'name')
                age = AORXMLParser.get_element(card, 'age')
                displayunitcount = \
                    AORXMLParser.get_element(card, 'displayunitcount')
                tech = self.tech_parser.get_tech(name)
                displaynameid = AORXMLParser.get_element(tech, 'displaynameid')
                strings = \
                    self.strings_parser.get_string(displaynameid) \
                    if displaynameid is not None else []
                self.cards[self.get_nation(file)].append(
                    Card(
                        name=name,
                        age=age,
                        displayunitcount=displayunitcount,
                        icon=AORXMLParser.get_element(tech, 'icon'),
                        strings=strings
                    )
                )
