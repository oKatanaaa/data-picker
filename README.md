## Data Picker

A simple console utility for manually selecting data samples from huggingface datasets.

### Installation

1. `git clone https://github.com/oKatanaaa/data-picker.git`
2. `cd data-picker`
3. `pip install -e .`

### Usage

To start data selection, run: `python -m data_picker.pick dataset_name`
Parameters:
- `--dataset-config`. If a dataset has configurations, you can supply one using this parameter.
- `--save-rejected`. Whether to save rejected (not picked) data samples.
- `--save-folder`. Path to the folder where to save the selected samples. By default a new folder with the dataset name
will be created in the current working directory.

During data selection you can do the following:
- hit enter - skip current sample.
- type *y* - accept current sample.
- type *back* - revert previous action, go to previous sample.
- type *stop* - finish data selection process.

Once data have been selected, there will be two files in the saving folder:
1. `train_accepted.csv` - selected samples.
2. `test_rejected.csv` - rejected samples.
The files have *train* and *test* prefixes so that huggingface does not merge them into single train split.