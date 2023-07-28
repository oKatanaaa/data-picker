import typer
from typing_extensions import Annotated

import pandas as pd
import numpy as np
import glob
import os


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def main(
    folder: Annotated[str, typer.Argument(help="Folder containing filtered datasets.")]
):
    files = glob.glob(os.path.join(folder, "*.csv"))

    accepted_dfs = {}
    rejected_dfs = {}
    for file in files:
        df = pd.read_csv(file)
        dataset_name = os.path.basename(file).split(".")[0]
        if 'rejected' in dataset_name:
            rejected_dfs[dataset_name] = len(df)
        else:
            accepted_dfs[dataset_name] = len(df)
        
    print(f"{bcolors.OKBLUE}### Accepted samples {bcolors.ENDC}")
    for name, count in accepted_dfs.items():
        print(f"{name}: {bcolors.OKGREEN}{count}{bcolors.ENDC}")
    print('\n')
    
    print(f"{bcolors.FAIL}### Rejected samples {bcolors.ENDC}")
    for name, count in rejected_dfs.items():
        print(f"{name}: {bcolors.OKGREEN}{count}{bcolors.ENDC}")
    
    print('\n')
    print(f'{bcolors.OKBLUE}Total accepted samples: {bcolors.OKGREEN}{sum(accepted_dfs.values())}')
    print(f'{bcolors.FAIL}Total rejected samples: {bcolors.OKGREEN}{sum(rejected_dfs.values())}{bcolors.ENDC}')


if __name__ == "__main__":
    typer.run(main)