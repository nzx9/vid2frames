from ast import Index
import os
from pathlib import Path
import cv2
import numpy as np
import csv

FPS = 37


class Vid2Frames:
    def __init__(
        self,
        root_dir,
        no_of_frames,
        input_file_extension,
        csv_path,
        output_root_dir_name="outputs",
    ):
        self.root_dir = root_dir
        self.fps = no_of_frames
        self.input_file_extension = input_file_extension
        self.csv_path = csv_path
        self.output_root_dir_name = output_root_dir_name
        self.csv_data = []
        self.csv_header = []

    def folders_in_root(self):
        folders = os.listdir(self.root_dir)
        return folders

    def files_in_folder(self, folder):
        files = list(
            Path("{}/{}".format(self.root_dir, folder)).glob(
                "*.{}".format(self.input_file_extension)
            )
        )
        return files

    def get_split_at_list(self, video, fps):
        duration = self.get_duration(video)
        output = [i for i in np.arange(0, duration, (0 + duration) / fps)]
        return output

    def split(self, file, video_id):
        print("Processing:: {}".format(str(file)))
        i = 0
        _frames = 0
        video = self.read_video(file)
        video_fps = video.get(cv2.CAP_PROP_FPS)

        # fps = min(self.fps, video_fps)
        fps = self.fps
        splits = self.get_split_at_list(video, fps)

        filename = str(file).split("/")[-2]
        output_dir = "{}/{}".format(self.output_root_dir_name, video_id)
        duration = self.get_duration(video)
        if not os.path.isdir(output_dir):
            os.mkdir(output_dir)
        while 1:
            is_read, frame = video.read()
            if not is_read:
                print("No Frames")
                break

            frame_due = i * (duration / fps)
            try:
                if frame_due >= splits[0]:
                    print("Writing Frame {} at {}".format(i, splits[0]))
                    cv2.imwrite("{}/{}.jpg".format(output_dir, i), frame)
                    _frames += 1
                if len(splits) > 0:
                    splits.pop(0)
            except IndexError:
                break
            i += 1
        self.csv_write([video_id, filename, _frames])
        print("\n")
        self.csv_flush()

    def csv_flush(self):
        with open(self.csv_path, "w") as csvfile:
            filewriter = csv.writer(
                csvfile, delimiter=",", quotechar="|", quoting=csv.QUOTE_MINIMAL
            )
            filewriter.writerow(self.csv_header)
            filewriter.writerows(self.csv_data)

    def csv_write(self, row):
        self.csv_data.append(row)

    def set_csv_header(self, row):
        self.csv_header = row

    def read_video(self, file):
        return cv2.VideoCapture(str(file))

    def get_duration(self, video):
        return video.get(cv2.CAP_PROP_FRAME_COUNT) / video.get(cv2.CAP_PROP_FPS)
