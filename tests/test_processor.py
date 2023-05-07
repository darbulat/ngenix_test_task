from pathlib import Path

import pytest

from src.parser import XMLParser
from src.processor import ArchiveProcessor


class TestProcessor:
    def test_processor(self, mock_archiver):
        work_dir = mock_archiver.make_many_archives()
        processor = ArchiveProcessor(XMLParser(), output_dir=work_dir)
        levels_path, objects_path = map(
            Path, processor.process_archives_from_dir(work_dir)
        )
        assert levels_path.exists()
        assert objects_path.exists()

    @pytest.mark.parametrize("param_work_dir", ["not_exists", "main.py"])
    def test_processor_wrong_dir(self, param_work_dir):
        work_dir = Path(param_work_dir)
        with pytest.raises(NotADirectoryError):
            processor = ArchiveProcessor(XMLParser(), output_dir=work_dir)
            processor.process_archives_from_dir(work_dir)

    def test_processor_empty_dir(self):
        work_dir = Path("src")
        with pytest.raises(ValueError):
            processor = ArchiveProcessor(XMLParser(), output_dir=work_dir)
            processor.process_archives_from_dir(work_dir)
