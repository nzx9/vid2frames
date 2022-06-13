# vidworks

Python tool to work with video datasets.

- Convert videos to frames and create the relevant csv files
- Create hdf5 datasets
- Split datasets into train, validate and test

## Installation

- [x] Clone the vid2frame repo from Github and navigate to the cloned directory

```bash
git clone https://github.com/nzx9/vid2frames.git
cd vid2frames
```

- [x] Create virtual environment

```bash
python -m venv venv # For Windows

python3 -m venv venv # For Linux/ OSx
```

- [x] Activate venv

```bash
venv\Script\activate # For Windows

source venv/bin/activate # For Linux/ OSx
```

- [x] Install requirements

```bash
python -m pip install -r requirements.txt
```

- [x] Run

```
python app.py --help
```

## Usage

```no-format
positional arguments:
  {v2f,h5,split}  vid2frames commands
    v2f           Convert videos to frames
    h5            Create hdf5 datasets from the converted frames
    split         Split CSV file into train, test, and val sets

options:
  -h, --help      show this help message and exit
```

### v2f

v2f can be used to split video files into frames

### h5

h5 can be used create hdf5 datasets

### split

split can be used to split datasets into train, validation and test datasets
