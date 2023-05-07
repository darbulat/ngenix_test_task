import pytest

from src.generator import XMLGenerator


def test_archiver(mock_archiver):
    archive_path = mock_archiver.make_archive()
    assert archive_path.exists()


@pytest.mark.parametrize("count, expected", [(-10, 0), (0, 0), (1, 1), (100, 100)])
def test_many_archives(mock_archiver, count, expected):
    work_dir = mock_archiver.make_many_archives(count)
    assert work_dir.exists()
    assert len(list(work_dir.glob("*.zip"))) == expected


def test_xml_generator():
    generator = XMLGenerator()
    data = generator.generate_data()

    assert data.startswith("<root>")
    assert data.endswith("</root>")
