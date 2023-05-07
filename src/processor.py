import csv
import os
import zipfile
from multiprocessing import Pool
from pathlib import Path
from typing import Tuple

from src.parser import AbstractParser


class ArchiveProcessor:
    """
    Класс `ArchiveProcessor` предназначен для обработки ZIP-архивов,
    содержащих XML-файлы, с помощью объекта класса, реализующего абстрактный
    класс `AbstractParser`.

    Атрибуты
    --------
    parser : AbstractParser
        Объект класса, реализующего абстрактный класс `AbstractParser`.
    output_dir : Path
        Путь к каталогу, в котором будут сохранены CSV-файлы.

    """

    LEVEL_DATA_FILENAME = "id_level_data.csv"
    OBJECTS_DATA_FILENAME = "object_data.csv"

    def __init__(self, parser: AbstractParser, output_dir: Path = Path()):
        self._parser = parser
        self._output_dir = output_dir

    def process_archive(self, archive_path: Path) -> Tuple:
        """
        Обрабатывает ZIP-архив, содержащий XML-файлы.

        :param archive_path: Путь к ZIP-архиву.
        :return: Кортеж:
            - `id_level_data` - список, содержащий uuid и level для каждого
                XML-файла в архиве.
            - `object_data` - список, содержащий идентификатор и имя
             объекта для каждого объекта в каждом XML-файле в архиве.
        """
        id_level_data = []
        object_data = []
        with zipfile.ZipFile(archive_path, "r") as archive:
            for file_name in archive.namelist():
                if file_name.endswith(".xml"):
                    file_path = archive.extract(file_name)
                    id_level, obj = self._parser.parse_file(Path(file_path))
                    id_level_data.append(id_level)
                    object_data.extend(obj)
                    os.remove(file_path)
        return id_level_data, object_data

    def process_archives_from_dir(self, dir_path: Path) -> Tuple[str, str]:
        """
        Обрабатывает все ZIP-архивы в указанном каталоге.

        :param dir_path: Путь к каталогу, содержащему ZIP-архивы.
        :return: Кортеж:
            - `level_data_path` - список, содержащий uuid и level для каждого
                XML-файла в архиве.
            - `object_data_path` - список, содержащий идентификатор и имя
             объекта для каждого объекта в каждом XML-файле архива.
        """
        if not dir_path.exists() or not dir_path.is_dir():
            raise NotADirectoryError
        id_level_data = []
        object_data = []
        with Pool(os.cpu_count()) as p:
            for result in p.map(self.process_archive, dir_path.glob("*.zip")):
                id_level_data.extend(result[0])
                object_data.extend(result[1])

        if not id_level_data or not object_data:
            raise ValueError("Empty folder or wrong file format")
        level_data_path = self._output_dir / self.LEVEL_DATA_FILENAME
        object_data_path = self._output_dir / self.OBJECTS_DATA_FILENAME
        self.write_csv_file(level_data_path, id_level_data)
        self.write_csv_file(object_data_path, object_data)
        return str(level_data_path), str(object_data_path)

    @staticmethod
    def write_csv_file(file_path: Path, data: list):
        """
        Записывает данные в CSV-файл.

        :param file_path: Путь к CSV-файлу.
        :param data: Список, содержащий данные для записи.
        """
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(data)
