import setuptools

with open("README.txt", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vc_hid", # Replace with your own username
    version="2022.2.1",
    author="lorry_rui",
    author_email="lrui@logitech.com",
    description="USB HID command package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Lorrytoolcenter/VC-HID.git",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
