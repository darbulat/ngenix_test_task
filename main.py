import argparse
import shutil
from pathlib import Path

from src.archiver import Archiver
from src.generator import XMLGenerator
from src.parser import XMLParser
from src.processor import ArchiveProcessor


def main(num_archives: int, files_per_archive: int, work_dir: str):
    archiver = Archiver(
        generator=XMLGenerator(),
        work_dir=Path("data"),
        files_per_archive=files_per_archive,
    )
    dest_dir = archiver.make_many_archives(num_archives)
    path_work_dir = Path(work_dir)
    path_work_dir.mkdir(exist_ok=True)
    processor = ArchiveProcessor(parser=XMLParser(), output_dir=path_work_dir)
    levels_path, objects_path = processor.process_archives_from_dir(dest_dir)
    print(f'{levels_path=}')
    print(f'{objects_path=}')
    shutil.rmtree(dest_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--num_archives", type=int, default=50, help="Количество архивов"
    )
    parser.add_argument(
        "--num_files", type=int, default=100, help="Количество файлов в архиве"
    )
    parser.add_argument(
        "--work_dir", type=str, default="results", help="Количество файлов в архиве"
    )

    args = parser.parse_args()

    main(args.num_archives, args.num_files, args.work_dir)
