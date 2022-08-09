"""
 # @ Author: Shirsendu Podder
 # @ Create Time: 2020-10-20 23:22:16
 # @ Description: Command line script for data pre-processing for the OPGAR project.
 # @ Modified by: Shirsendu Podder
 # @ Modified time: 2020-11-19 23:27:17
 """

import tarfile
import os
import sys
import shutil
from argparse import ArgumentParser
from pathlib import Path
import tqdm
import logging
from tqdm.contrib.concurrent import process_map
import datetime
from tqdm.contrib.logging import tqdm_logging_redirect
from rich.logging import RichHandler
from rich.progress import track


logging.basicConfig(level=logging.INFO, handlers=[RichHandler()])

ACCEPTABLE_DATA_FORMATS = (".txt", ".csv", ".json", ".yml", ".yaml")

parser = ArgumentParser(
    description="Extract a series of .tar.gz files and organise the resulting output."
)
parser.add_argument(
    "rawdir",
    default=Path(os.getcwd()),
    help="The directory that contains the raw .tar.gz files.",
)
parser.add_argument("tmpdir", help="The destination for all csv files.")
parser.add_argument(
    "--no-parallel",
    "-n",
    default=False,
    action="store_true",
    help="If true, extraction occurs in a singular thread/process, parallel otherwise.",
)
parser.add_argument(
    "-d",
    "--debug",
    help="Print debugging",
    action="store_const",
    dest="loglevel",
    const=logging.DEBUG,
)
parser.add_argument(
    "-v",
    "--verbose",
    help="Be verbose",
    action="store_const",
    dest="loglevel",
    const=logging.INFO,
)
args = parser.parse_args()
no_multiprocessing = vars(args)["no_parallel"]


log = logging.getLogger(__name__)
SOURCE = Path(args.rawdir)
EXP_DIR = SOURCE.parent
DESTINATION = EXP_DIR / "tmp"

if not DESTINATION.exists():
    logging.info(f"Creating {DESTINATION}")
    DESTINATION.mkdir()


def extract_tar(filename):
    log.debug(f"Extracting {filename}")
    try:
        with tarfile.open(filename, mode="r") as tar:
            tar.extractall(path=DESTINATION)
    except Exception as err:
        log.warning(f"{filename} failed")
        return False
    return True


if __name__ == "__main__":
    # ==============================================================================
    # Search for compressed files (.tar.gz only)
    # ==============================================================================

    TAR_FILES = [f for f in SOURCE.glob("*.tar.gz")]
    if len(TAR_FILES) == 0:
        log.info("No .tar.gz files found.")
        log.info("Terminating.")
        sys.exit(0)

    log.info(f"Source dir -> {os.path.abspath(SOURCE)}")
    log.info(f"Output dir -> {os.path.abspath(DESTINATION)}")

    # Find max id so far
    max_id = -1
    for f in TAR_FILES:
        fname = os.path.split(f)[1][:-7]
        try:
            max_id = int(fname) if int(fname) > max_id else max_id
        except ValueError as err:
            print(f"Error with {fname}")
            continue

    log.info(f"{'Total Files:' : <20}{len(TAR_FILES)}")
    log.info(f"{'Maximum File ID: ' : <20}{max_id}")

    # ==============================================================================
    # Final checks before extraction
    # ==============================================================================

    job_ids_found = []  # store as integers
    files_to_export = []

    # scan destination directory to see what json config files have already been exported
    for f in os.listdir(DESTINATION):
        if not os.path.splitext(f)[-1] in ACCEPTABLE_DATA_FORMATS:
            continue
        filename = os.path.split(f)[-1]
        if "README" in filename:
            continue
        try:
            job_id = int(
                filename[:4]
            )  # xxxx_yyy.csv convention (xxxx = jobID, yyy=actions/composition/etc.)
        except ValueError:
            job_id = int(
                filename[1:5]
            )  # jxxxx_yyy.csv convention (xxxx = jobID, yyy=actions/composition/etc.)

        job_ids_found.append(job_id)
        files_to_export.append(f)

    job_ids_found = set(job_ids_found)
    job_ids_to_extract = set(range(1, max_id + 1)).difference(job_ids_found)
    print(f"{'Jobs already found: ': <20}{len(job_ids_found)}")
    print(80 * "=")

    if input("Continue? (Y/N) ").upper() == "N":
        sys.exit()

    # ==============================================================================
    # Extract all/some of the files
    # ==============================================================================
    files_to_export = [
        f.absolute()
        for f in TAR_FILES
        if int(f.name.rstrip(".tar.gz")) in job_ids_to_extract
    ]
    tick = datetime.datetime.now()

    if no_multiprocessing:
        for f in track(files_to_export):
            extract_tar(f)
            tqdm.tqdm.write(f"{f} extracted")
    else:
        with tqdm_logging_redirect():
            r = process_map(extract_tar, files_to_export, chunksize=1)

        if False in r:
            log.warning("Jobs failed!")

    tock = datetime.datetime.now()

    print(f"Time elapsed: {tock-tick}")

    # ==============================================================================
    # Move all files into destination directory (from tmpdir)
    # ==============================================================================
    if len(files_to_export) == 0:
        print("No files exported.")
    elif len(files_to_export) > 0:

        print(f"Moving to {DESTINATION}")
        for root, dirs, files in os.walk(DESTINATION):
            for f in files:
                if "smpd" in f:
                    continue
                src_path = Path(root) / f
                dst_path = Path(DESTINATION) / f
                if src_path == dst_path:
                    continue
                shutil.move(src_path, dst_path)

        print(f"Exported and moved {len(files_to_export)} files. ")
