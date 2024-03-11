# Generate_Summary_from_Videos

This Python script uses Whisper and BERT to automatically generate a summary from a local mp3 file or a YouTube video.

> Note: it has been tested on Windows only.

----

## How to install
1. Clone this repo on your local machine.
2. Install the needed packages:
    * Open your local project
    * Open your terminal
    * run `pip install -r requirements.txt`

## How to use
**FIRST METHOD: summarize a local mp3 file**
1. Create a new folder under the root of your local project and name it `results`
2. Add the mp3 file to the `results` folder
3. In your terminal, run the command `python run main.py VIDEO_NAME`
4. The generated summary will be stored in the `results` folder.

> In this case `VIDEO_NAME` is the name of your local mp3 file. Do not include the file extension!


**SECOND METHOD: summarize a YouTube video**
1. Create a new folder under the root of your local project and name it `results`
2. In your terminal, run the command `python run main.py VIDEO_NAME -u YOUTUBE_URL`
3. The generated summary will be stored in the `results` folder.

> In this case `VIDEO_NAME` is just the name for the generated file that contains the summary.
