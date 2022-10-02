import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vwiz",
    version="0.0.2",
    author="Navindu Dananga",
    author_email="navindum@protonmail.com",
    license="MIT",
    description="Video processing library (Split videos into frames, split dataset into train, validate and test sets, create hdf5 datasets)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nzx9/vwiz",
    packages=setuptools.find_packages(),
    scripts=['scripts/vwiz.py'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=["numpy", "Pillow", "h5py", "opencv-python", "tqdm", "colorama"],
)