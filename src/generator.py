import abc
import string
import uuid
import xml.etree.ElementTree as ET
import random


class AbstractGenerator(abc.ABC):
    @abc.abstractmethod
    def generate_data(self) -> str:
        raise NotImplemented


class XMLGenerator(AbstractGenerator):
    def generate_data(self) -> str:
        return self._generate_xml_data()

    def _generate_xml_data(self) -> str:
        root = ET.Element("root")
        ET.SubElement(root, "var", {"name": "id", "value": str(uuid.uuid4())})
        ET.SubElement(
            root, "var", {"name": "level", "value": str(random.randint(1, 100))}
        )
        objects = ET.SubElement(root, "objects")
        num_objects = random.randint(1, 10)
        for i in range(num_objects):
            ET.SubElement(objects, "object", {"name": self._random_string(10)})
        return ET.tostring(root, encoding="unicode")

    @staticmethod
    def _random_string(length):
        letters = string.ascii_lowercase
        return "".join(random.choice(letters) for _ in range(length))
