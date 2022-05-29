import argparse
from tqdm import tqdm

cmd_parser = argparse.ArgumentParser()

cmd_sub_parser = cmd_parser.add_subparsers(
    help="vid2frames commands", dest="command", required=True
)

v2f = cmd_sub_parser.add_parser("v2f", help="Convert videos to frames")
h5 = cmd_sub_parser.add_parser(
    "h5", help="Create hdf5 datasets from the converted frames"
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
    help="Path to create csv file",
)

v2f.add_argument(
    "-V",
    "--verbose",
    required=False,
    nargs="?",
    const=True,
    help="Print verbose data",
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

args = cmd_parser.parse_args()

if __name__ == "__main__":
    if args.command == "v2f":
        from src.vid2frames import Vid2Frames

        root_dir = args.root_dir
        frames = args.frames
        ext = args.extension
        csv = args.csv

        v2f = Vid2Frames(
            root_dir=root_dir,
            no_of_frames=frames,
            input_file_extension=ext,
            csv_path=csv,
        )

        folders = v2f.folders_in_root()
        v2f.set_csv_header(["video_id", "label", "frames"])
        video_id = 0
        if args.verbose:
            for folder in folders:
                files = v2f.files_in_folder(folder=folder)
                for file in files:
                    v2f.split(file, video_id)
                    video_id += 1
        else:
            for folder in tqdm(folders):
                files = v2f.files_in_folder(folder=folder)
                for file in files:
                    v2f.split(file, video_id)
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

        def pre_process_hdf5(
            dataset_path, groups, miss_frames_from, output_path, output_name
        ):
            pre_process_core = HDF5_PRE_PROCESS_CORE(
                dataset_path=dataset_path, groups=groups
            )
            pre_process_core.create(
                output_path=output_path,
                output_name=output_name,
                miss_frames_from=miss_frames_from,
            )

    else:
        print("Invalid Command selected")
