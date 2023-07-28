import typer
from typing_extensions import Annotated

import pandas as pd
import numpy as np
import os
from datasets import load_dataset


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

NO_ACTION = -1
REJECT = 0
ACCEPT = 1

def main(
    dataset_name: Annotated[str, typer.Argument(help="Name of the huggingface dataset.")],
    dataset_config: Annotated[str, typer.Option(help="Dataset config if needed.")] = None,
    save_rejected: Annotated[bool, typer.Option(help="Save rejected data.")] = True,
    save_folder: Annotated[bool, typer.Option(help="Where to save selected data.")] = None
):
    dataset = load_dataset(dataset_name, name=dataset_config)
    df = dataset['train'].to_pandas()
    n_entries = len(df)
    indices = np.random.choice(n_entries, size=n_entries, replace=False)
    
    keep = []
    rejected = []
    last_action = NO_ACTION
    i = 0
    while True:
        if i == n_entries:
            break

        ind = indices[i]
        data = df.iloc[ind].to_dict()
        for k, v in data.items():
            print(f'{bcolors.WARNING}{k}{bcolors.ENDC}')
            print(v, end='\n\n')

        response = input(f'{bcolors.OKGREEN}Gathered {bcolors.OKCYAN}{len(keep)}{bcolors.OKGREEN} samples. Keep it?{bcolors.ENDC} ')
        if len(response) == 0:
            last_action = REJECT
            rejected.append(data)
        if response.lower() == 'y':
            last_action = ACCEPT
            keep.append(data)
        if response == 'stop':
            break
        if response == 'back':
            i -= 1
            if last_action == ACCEPT:
                keep.pop()
            if last_action == REJECT:
                rejected.pop()
            continue

        i += 1
    
    dataset_name = dataset_name.replace('/', '__')
    if save_folder is None:
        save_folder_path = dataset_name
    else:
        save_folder_path = save_folder
    os.makedirs(save_folder_path, exist_ok=True)
    
    smart_save(save_folder_path, 'train_accepted.csv', pd.DataFrame(keep))

    if save_rejected:
        smart_save(save_folder_path, 'train_rejected.csv', pd.DataFrame(rejected))


def smart_save(save_folder: str, basefilename: str, df: pd.DataFrame):
    filename = os.path.join(save_folder, basefilename)
    if os.path.exists(filename):
        print(f'{bcolors.WARNING}File {filename} already exists. Adding new content at the end.{bcolors.ENDC}')
        old_df = pd.read_csv(filename)
        df = pd.concat([old_df, df])
    
    df.to_csv(filename, index=False)
    
    
if __name__ == "__main__":
    typer.run(main)