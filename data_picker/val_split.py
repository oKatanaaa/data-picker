import typer
from typing_extensions import Annotated

import pandas as pd
import numpy as np
import os


def main(
    dataset_folder: Annotated[str, typer.Argument(help="Name of the huggingface dataset.")],
    val_split: Annotated[float, typer.Option(help="Percentage of the dataset to use for validation.")] = 0.25
):  
    accepted_name = os.path.join(dataset_folder, 'train_accepted.csv')
    df = pd.read_csv(accepted_name)
    train_split_ind = len(df) - int(len(df) * val_split)
    train_df = df[:train_split_ind]
    val_df = df[train_split_ind:]

    pd.DataFrame(train_df).to_csv(accepted_name, index=False)
    
    val_name = os.path.join(dataset_folder, 'val_accepted.csv')
    pd.DataFrame(val_df).to_csv(val_name, index=False)
    

if __name__ == "__main__":
    typer.run(main)