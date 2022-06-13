import argparse
from tqdm import tqdm
import sys

cmd_parser = argparse.ArgumentParser()

cmd_sub_parser = cmd_parser.add_subparsers(
    help="vid2frames commands", dest="command", required=True
)

v2f = cmd_sub_parser.add_parser("v2f", help="Convert videos to frames")
h5 = cmd_sub_parser.add_parser(
    "h5", help="Create hdf5 datasets from the converted frames"
)
split = cmd_sub_parser.add_parser(
    "split", help="Split CSV file into train, test, and val sets"
)

v2f.add_argument(
    "-D",
    "--root_dir",
    required=True,
    type=str,
    help="Root directory of the video files",
)
v2f.add_argument(
    "-F",
    "--frames",
    required=True,
    type=int,
    help="No of frames from the video",
)
v2f.add_argument(
    "-E",
    "--extension",
    required=True,
    type=str,
    help="File extention of the input video files",
)

v2f.add_argument(
    "-C",
    "--csv",
    required=True,
    type=str,
    default="Outputs",
    help="Path to create csv file",
)

v2f.add_argument(
    "-O",
    "--out_dir",
    required=False,
    type=str,
    help="Output location to save the frames, default is 'outputs'",
)

v2f.add_argument(
    "-V",
    "--verbose",
    required=False,
    nargs="?",
    const=True,
    help="Print verbose data",
)

v2f.add_argument(
    "-FF",
    "--force",
    required=False,
    nargs="?",
    const=True,
    help="force frame splitter to use frames given to --frames or else it will use the best fps to automatically decide number of frames. Not setting this will return different number of frames than the given --frames",
)

h5.add_argument(
    "-D",
    "--root_dir",
    required=True,
    type=str,
    help="Path to the converted frames",
)
h5.add_argument(
    "-G",
    "--groups",
    required=True,
    type=str,
    help="Groups need to create in hdf5 dataset",
)

h5.add_argument(
    "-MS",
    "--miss_frames_start",
    required=False,
    type=int,
    help="No of frames to miss from start",
)
h5.add_argument(
    "-ME",
    "--miss_frames_end",
    required=False,
    type=int,
    help="No of frames to miss from end",
)

h5.add_argument(
    "-OP",
    "--output_path",
    required=True,
    type=str,
    help="Path to save output",
)

h5.add_argument(
    "-ON",
    "--output_name",
    required=True,
    type=str,
    help="Name to save output",
)

split.add_argument(
    "-C",
    "--csv",
    required=True,
    type=str,
    help="csv file to split",
)
split.add_argument(
    "-T",
    "--train_ratio",
    required=True,
    type=float,
    help="Ratio to split train set",
)
split.add_argument(
    "-V",
    "--validate_ratio",
    required=False,
    type=float,
    help="Ratio to split validation set. if not given, test set will be empty and if --train_ratio is less than 1 validate_ratio will be calculate automatically",
)
split.add_argument(
    "-S",
    "--shuffle",
    required=False,
    nargs="?",
    const=True,
    help="Shuffle the data before splitting",
)

split.add_argument(
    "-H",
    "--include_header",
    required=False,
    nargs="?",
    const=True,
    help="Include header to the splitting process",
)

split.add_argument(
    "-D",
    "--save_dir",
    required=False,
    type=str,
    help="Save output csv files to this directory",
)

split.add_argument(
    "-P",
    "--postfix",
    required=False,
    type=str,
    help="Add postfix text to output csv filename's end",
)


args = cmd_parser.parse_args()

if __name__ == "__main__":
    if args.command == "v2f":
        from src.vid2frames import Vid2Frames

        root_dir = args.root_dir
        frames = args.frames
        ext = args.extension
        csv = args.csv
        force = False if args.force is None else args.force
        verbose = False if args.verbose is None else args.verbose
        out_dir = "outputs" if args.out_dir is None else args.out_dir
        v2f = Vid2Frames(
            root_dir=root_dir,
            no_of_frames=frames,
            input_file_extension=ext,
            csv_path=csv,
            output_root_dir_name=out_dir,
        )

        folders = v2f.folders_in_root()
        v2f.set_csv_header(["video_id", "label", "frames", "height", "width"])
        video_id = 0
        if verbose:
            v2f.set_verbose(True)
            for folder in folders:
                files = v2f.files_in_folder(folder=folder)
                for file in files:
                    v2f.split(file, video_id, force)
                    video_id += 1
        else:
            for folder in tqdm(folders):
                files = v2f.files_in_folder(folder=folder)
                for file in files:
                    v2f.split(file, video_id, force)
                    video_id += 1

    elif args.command == "h5":
        from src.hdf5 import HDF5_PRE_PROCESS_CORE

        dataset_path = args.root_dir
        groups = args.groups
        output_path = args.output_path
        output_name = args.output_name
        miss_frames_from = {}
        miss_frames_from["start"] = (
            0 if args.miss_frames_start is None else args.miss_frames_start
        )

        miss_frames_from["end"] = (
            0 if args.miss_frames_end is None else args.miss_frames_end
        )

        pre_process_core = HDF5_PRE_PROCESS_CORE(
            dataset_path=dataset_path, groups=groups
        )
        pre_process_core.create(
            output_path=output_path,
            output_name=output_name,
            miss_frames_from=miss_frames_from,
        )

    elif args.command == "split":
        from src.split import Split

        splitter = Split(
            args.csv,
            args.train_ratio,
            args.validate_ratio,
            args.shuffle,
            not args.include_header,
        )
        splitter.csv_write(args.save_dir, args.postfix)
    else:
        cmd_parser.print_help(sys.stderr)
