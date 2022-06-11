import os
import h5py
import numpy as np
from tqdm import tqdm
from PIL import Image
import io


class HDF5_PRE_PROCESS_CORE:
    dataset_path = None
    dataset = None

    def __init__(self, dataset_path, groups):
        if not os.path.exists(dataset_path):
            raise FileNotFoundError
        self.dataset_path = dataset_path
        self.groups = groups.split(",")
        self.error_files = []

    def read_bytes(self, path):
        with open(path, "rb") as inp:  # open files as python binary
            return inp.read()

    def to_numpy(self):
        return None

    def __create__(
        self,
        output_path: str,
        group: str,
        miss_frames_from: dict = {"start": 0, "end": 0},
        output_name: str = "hdf5_dataset",
    ):
        output_file = os.path.join(output_path, "{}.hdf5".format(output_name))
        print("Writing to: {}".format(output_file))

        flag = "a" if os.path.exists(output_file) else "w"

        if flag == "a":
            print("File Exist! Appending... (Mode = {})".format(flag))
        elif flag == "w":
            print("File Not Exist! Creating New File... (Mode = {})".format(flag))

        with h5py.File(output_file, flag) as hdf:
            grp = hdf.create_group(group)
            _path = os.path.join(self.dataset_path, group)
            print(_path)
            if not os.path.exists(_path):
                raise FileNotFoundError("Group {} not found".format(group))
            for vid in tqdm(os.listdir(_path)):
                try:
                    vid_abs_path = os.path.join(_path, vid)
                    # print("Processing: {}".format(vid_abs_path))
                    frames = os.listdir(vid_abs_path)
                    if miss_frames_from["end"] == 0:
                        frames = frames[miss_frames_from["start"] :]
                    else:
                        frames = frames[
                            miss_frames_from["start"] : miss_frames_from["end"] * -1
                        ]
                    frame_byte_array = []
                    for frame in frames:
                        frame_bytes = self.read_bytes(os.path.join(vid_abs_path, frame))
                        frame_byte_array.append(frame_bytes)
                    frame_binary_data_np = np.array(frame_byte_array)
                    grp.create_dataset(vid, data=frame_binary_data_np)
                except:
                    self.error_files.append(vid_abs_path)
                    pass

    def create(
        self,
        output_path: str,
        miss_frames_from: dict = {"start": 0, "end": 0},
        output_name: str = "hdf5_dataset",
    ):
        for group in self.groups:
            print("Group: {}".format(group))
            print("=" * 20)
            self.__create__(output_path, group, miss_frames_from, output_name)

        print("\n\n\nError Files: \n {}".format(self.error_files))

    def read_frame(self, bytes):
        return Image.open(io.BytesIO(bytes))

    def show_frame(self, bytes):
        frame = Image.open(io.BytesIO(bytes))
        frame.show()
