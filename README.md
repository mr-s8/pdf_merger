<div align="center">
  <p>
    <a href="https://github.com/mr-s8/merger_gui/blob/main/images/pdf-4919559_1280.png"><img src="https://github.com/mr-s8/merger_gui/blob/main/images/pdf-4919559_1280.png" width="200" alt="pytube logo" /></a>
  </p>
</div>



# pdf_merger
A GUI made with Tkinter, that allows the user to merge pdf and image files together to a pdf file.

# How to install:
1. download the python skript and the requirements.txt file
2. install python from: https://www.python.org/
3. In the folder where the requirements.txt file is located, open a terminal and install the dependencies with:
```bash
pip install -r requirements.txt
```
4. Download and install ffmpeg from: https://ffmpeg.org/download.html
5. If not already done, add ffmpeg to PATH
6. In the folder where the python skript is located, open a terminal and start the app with:
```bash
python youtube_downloader.py
```


# ToDo
Features to add:
- get links from textfile
- download playlist all at once
- use multithreading (one thread for gui and one for each download)                             ✓
- show thumbnail when adding video
- show progressbar
- add other formats than mp4 and mp3
- allow user to choose resolution
- show debug messages to a textbox in the gui (also because multithreading spams the console)  ✓
- check Linux compatibility

To fix:
- with the ANDROID_CREATOR client, in some cases, there is no 1080p stream, even though there should be one,
    using the ADROID client could fix this, it fixes a loop bug with age restricted videos, but leads to 403 errors
    very often; how can I eliminate all these bugs?

## Pictures
<div align="center">
  <p>
    <a href="https://github.com/mr-s8/merger_gui/blob/main/images/pdf_merger_gui.png"><img src="https://github.com/mr-s8/merger_gui/blob/main/images/pdf_merger_gui.png" width="800" alt="pytube logo" /></a>
  </p>
</div>
