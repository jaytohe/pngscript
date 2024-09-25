# pngscript
A small Python script which utilizes the [efsw python bindings I wrote](https://github.com/jaytohe/efsw) to watch for automatically convert webp and avif images to png.

# Requirements
1. [pyefsw](https://github.com/jaytohe/efsw)
2. Latest [Pillow](https://pypi.org/project/pillow/) lib
3. [Pillow AVIF plugin](https://pypi.org/project/pillow-avif-plugin/)

# How to Use
1. Open up the script in a text editor
2. Modify the `WEBP_DIRS` variable with the directory paths you want to monitor
3. Run the Python script
4. Add a webp file to the watched directory to test it
