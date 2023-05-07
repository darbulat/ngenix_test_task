import uuid
from multiprocessing import Pool
from os import cpu_count
from pathlib import Path
from zipfile import ZipFile

from src.generator import AbstractGenerator


class Archiver:
    def __init__(
        self,
        generator: AbstractGenerator,
        work_dir: Path,
        files_per_archive: int = 100,
    ):
        self._generator = generator
        self._work_dir = work_dir
        self._files_per_archive = files_per_archive

    def make_archive(self, *args):
        uuid_ = str(uuid.uuid4())
        zip_file = Path(uuid_).with_suffix(".zip")
        self._work_dir.mkdir(exist_ok=True)
        zip_path = self._work_dir / zip_file
        with ZipFile(zip_path, "w") as archive:
            [
                archive.writestr(f"{i}_{uuid_}.xml", self._generator.generate_data())
                for i in range(self._files_per_archive)
            ]
        return zip_path

    def make_many_archives(self, count: int = 50) -> Path:
        with Pool(cpu_count()) as p:
            p.map(self.make_archive, range(count))

        return self._work_dir
