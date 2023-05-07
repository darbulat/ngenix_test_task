import abc
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Tuple, List, Any


class AbstractParser(abc.ABC):
    @abc.abstractmethod
    def parse_file(self, file_path: Path):
        raise NotImplemented


class XMLParser(AbstractParser):
    def parse_file(self, file_path: Path) -> Tuple:
        return self._process_xml_file(file_path)

    @staticmethod
    def _process_xml_file(file_path: Path) -> Tuple:
        xml_data = file_path.read_text()
        root = ET.fromstring(xml_data)
        id_value: Any = root.find('.//var[@name="id"]')
        level_value: Any = root.find('.//var[@name="level"]')
        objects: Any = root.find(".//objects")
        id_level_data: Tuple = (id_value.attrib["value"], level_value.attrib["value"])
        object_data: List[Tuple] = [
            (id_value.attrib["value"], obj.attrib["name"])
            for obj in objects.findall("object")
        ]
        return id_level_data, object_data
