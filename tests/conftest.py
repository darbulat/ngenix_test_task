import shutil

import pytest

from src.archiver import AbstractGenerator, Archiver


class FakeGenerator(AbstractGenerator):
    def __init__(self, mock_data=None):
        self._data = mock_data

    def generate_data(self) -> str:
        return self._data


@pytest.fixture
def mock_generator(xml_data):
    return FakeGenerator(xml_data)


@pytest.fixture
def mock_archiver(mock_generator, tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("data")

    yield Archiver(mock_generator, tmp_path)

    shutil.rmtree(tmp_path)


@pytest.fixture
def xml_file(xml_data, tmp_path_factory):
    dir_path = tmp_path_factory.mktemp("data")
    xml_path = dir_path / "temp.xml"
    xml_path.write_text(xml_data)

    yield xml_path

    shutil.rmtree(dir_path)


@pytest.fixture
def xml_data():
    return """
    <root>
    <var name="id" value="693b7b63-8cc5-4a06-9eec-df80638159a0" />
    <var name="level" value="24" />
    <objects>
    <object name="gcrjuoewqn" />
    <object name="afwfwjfirn" />
    <object name="bnrnfweofw" />
    </objects></root>
    """
