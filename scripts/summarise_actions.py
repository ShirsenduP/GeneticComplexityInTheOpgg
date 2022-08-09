from argparse import ArgumentParser
from datetime import datetime
from pathlib import Path

import pandas as pd
from gopgar import average_actions, load_config, load_df
from rich.progress import track
from rich.logging import RichHandler
import logging


def summarise_data(data_dir: str, num_jobs: int):
    failures = set()
    dfs = []

    for job_id in track(range(1, num_jobs + 1)):
        tmp_df = load_df(job_id, "actions", True, data_dir)

        if tmp_df is None:
            print(f"Job {job_id} is missing")
            failures.add(job_id)
            continue

        tmp_config = pd.Series(load_config(job_id, data_dir))
        means = average_actions(tmp_df)
        means["uid"] = job_id
        df = pd.concat([means, tmp_config])
        dfs.append(df)

    results = pd.concat(dfs, axis=1).T
    try:
        results.set_index("uid")
    except KeyError:
        logging.warning(f"Can't set 'uid' as index. ")

    return results, failures


def main():
    parser = ArgumentParser("Summarise the actions from an experiment.")
    parser.add_argument(
        "data_path", help="The location of the csv files to summarise.", type=str
    )
    parser.add_argument(
        "output_path", help="The destination for the summary file.", type=str
    )
    parser.add_argument(
        "jobs", type=int, help="The max number of jobs to be summarised."
    )
    parser.add_argument("debug", action="store_true", help="Show log messages.")
    args = parser.parse_args()

    log_level = logging.DEBUG if args.debug else logging.INFO
    logging.basicConfig(level=log_level, handlers=[RichHandler()])

    data_dir_path = Path(args.data_path).absolute()
    summary_data_dir_path = Path(args.output_path).absolute()
    output_file = summary_data_dir_path / "actions.csv"
    if output_file.exists():
        invalid_name = output_file
        newname = datetime.strftime(datetime.now(), format="%Y%m%d_%H%M")
        output_file = output_file.with_name(f"actions_{newname}.csv")
        logging.warning(
            f"File {invalid_name.name} already exists. Renaming to {output_file.name}"
        )

    logging.info(f"{'Source: ':<20}{args.data_path}")
    logging.info(f"{'Destination: ':<20}{output_file}")
    logging.info(f"{'Jobs found: ':<20}{args.jobs}")

    if input("Confirm? Y/N ").upper() == "N":
        print("Cancelled.")
        return

    df, failures = summarise_data(str(data_dir_path), args.jobs)

    df.to_csv(output_file)
    print("Exported file", end="")
    if len(failures) > 0:
        print(f"but, there are {len(failures)} jobs missing.")


if __name__ == "__main__":
    main()
