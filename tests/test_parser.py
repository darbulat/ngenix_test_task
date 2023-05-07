from src.parser import XMLParser


def test_parser(xml_file):
    parser = XMLParser()
    a, b = parser.parse_file(xml_file)
    assert isinstance(a, tuple)
    assert isinstance(b, list)
    assert len(b) == 3
