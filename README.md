# vwiz 🧙

> vwiz :: video wizard 🧙

Python tool to work with video datasets.

- Convert videos to frames and create the relevant csv files
- Create hdf5 datasets
- Split datasets into train, validate and test

## Installation

### Using `pip`

```bash
pip install vwiz
```

### Using `git`

- [x] Clone the vid2frame repo from Github and navigate to the cloned directory

```bash
git clone https://github.com/nzx9/vwiz.git
cd vwiz
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

```no-format
usage: app.py v2f [-h] -D ROOT_DIR -F FRAMES -E EXTENSION -C CSV [-O OUT_DIR]
                  [-V [VERBOSE]] [-FF [FORCE]]

options:
  -h, --help            show this help message and exit
  -D ROOT_DIR, --root_dir ROOT_DIR
                        Root directory of the video files
  -F FRAMES, --frames FRAMES
                        No of frames from the video
  -E EXTENSION, --extension EXTENSION
                        File extention of the input video files
  -C CSV, --csv CSV     Path to create csv file
  -O OUT_DIR, --out_dir OUT_DIR
                        Output location to save the frames, default is
                        'outputs'
  -V [VERBOSE], --verbose [VERBOSE]
                        Print verbose data
  -FF [FORCE], --force [FORCE]
                        force frame splitter to use frames given to --frames
                        or else it will use the best fps to automatically
                        decide number of frames. Not setting this will return
                        different number of frames than the given --frames

```

### h5

h5 can be used create hdf5 datasets

```no-format
usage: app.py h5 [-h] -D ROOT_DIR -G GROUPS [-MS MISS_FRAMES_START]
                 [-ME MISS_FRAMES_END] -OP OUTPUT_PATH -ON OUTPUT_NAME

options:
  -h, --help            show this help message and exit
  -D ROOT_DIR, --root_dir ROOT_DIR
                        Path to the converted frames
  -G GROUPS, --groups GROUPS
                        Groups need to create in hdf5 dataset
  -MS MISS_FRAMES_START, --miss_frames_start MISS_FRAMES_START
                        No of frames to miss from start
  -ME MISS_FRAMES_END, --miss_frames_end MISS_FRAMES_END
                        No of frames to miss from end
  -OP OUTPUT_PATH, --output_path OUTPUT_PATH
                        Path to save output
  -ON OUTPUT_NAME, --output_name OUTPUT_NAME
                        Name to save output

```

### split

split can be used to split datasets into train, validation and test datasets

```no-format
usage: app.py split [-h] -C CSV -T TRAIN_RATIO [-V VALIDATE_RATIO]
                    [-S [SHUFFLE]] [-H [INCLUDE_HEADER]] [-D SAVE_DIR]
                    [-P POSTFIX]

options:
  -h, --help            show this help message and exit
  -C CSV, --csv CSV     csv file to split
  -T TRAIN_RATIO, --train_ratio TRAIN_RATIO
                        Ratio to split train set
  -V VALIDATE_RATIO, --validate_ratio VALIDATE_RATIO
                        Ratio to split validation set. if not given, test set
                        will be empty and if --train_ratio is less than 1
                        validate_ratio will be calculate automatically
  -S [SHUFFLE], --shuffle [SHUFFLE]
                        Shuffle the data before splitting
  -H [INCLUDE_HEADER], --include_header [INCLUDE_HEADER]
                        Include header to the splitting process
  -D SAVE_DIR, --save_dir SAVE_DIR
                        Save output csv files to this directory
  -P POSTFIX, --postfix POSTFIX
                        Add postfix text to output csv filename's end

```
