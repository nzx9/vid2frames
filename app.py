from src.vid2frames import Vid2Frames

root_dir = "/home/navindu/Downloads/SinhalaSignVideoDataset-50/Videos"
FPS = 37
v2f = Vid2Frames(
    root_dir=root_dir, no_of_frames=FPS, input_file_extension="mp4", csv_path="data.csv"
)

folders = v2f.folders_in_root()
v2f.set_csv_header(["video_id", "label", "frames"])
video_id = 0
for folder in folders:
    files = v2f.files_in_folder(folder=folder)
    for file in files:
        v2f.split(file, video_id)
        video_id += 1
