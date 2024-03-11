import logging
import os
import sys

from auto_generate_a_summary_from_long_youtube_videos import get_text_from_audio, read_file, split_text_into_chunks, \
    create_summarizer, get_summary_bart, save_summary_to_file, get_text


def parse_arguments():
    import argparse
    parser = argparse.ArgumentParser("simple_example")
    parser.add_argument("video_name", help="Arbitrary name of the video or name of your local MP3 file that you want to transcribe.", type=str)
    parser.add_argument("-u", "--url", help="YouTube url of the video. If not provided an MP3 file of VIDEO_NAME will be searched.", type=str)
    return vars(parser.parse_args())


"""
*
*
*
*
*
*
*
*
*
*
MAIN FUNCTION
*
*
*
*
*
*
*
*
*
*
"""
if __name__ == '__main__':
    logging.basicConfig(filename='demo.log', encoding='utf-8', level=logging.ERROR)

    args = parse_arguments()
    VIDEO_NAME = args["video_name"]
    print("\n\n- Name of the video: ", VIDEO_NAME)

    """# Downloading the YouTube video in MP3 Format"""
    """# Transcribe the audio with Wisper"""
    try:
        URL = args["url"]
        print("- YouTube url: ", URL)
        get_text(url=URL, video_name=VIDEO_NAME)
    except Exception as e:
        print(e)
        try:
            print("\n\nNo URL. Getting text from local .mp3 file\n")
            get_text_from_audio(audio_path=os.path.join("results", f"{VIDEO_NAME}.mp3"), video_name=VIDEO_NAME)
        except Exception as e1:
            print(e1)
            exit()

    print(f"\nAudio transcription completed and saved in file {VIDEO_NAME}.txt\n")


    """# Summarize the generated text
    ## Divide the large text into chunks
    """
    print("\n\nSummarizing the text...")
    long_text = read_file(VIDEO_NAME)
    if long_text:
        text_chunks = split_text_into_chunks(long_text, max_tokens=4000)
        logging.info(f"Text chunks: {text_chunks}")
    else:
        logging.error("Error: Unable to process the text.")


    """## Text Summarization with BART"""
    bart_params = {
        "max_length": 124,
        "min_length": 30,
        "do_sample": False,
        "truncation": True,
        "repetition_penalty": 2.0,
    }

    # Assume text_chunks is already defined and contains the chunks of text from the previous steps
    summarizer = create_summarizer("facebook/bart-large-cnn")
    summary = get_summary_bart(text_chunks, summarizer, bart_params)
    save_summary_to_file(summary, f"summary_{VIDEO_NAME}")

    print(f"\n\nSummary saved in the file summary_{VIDEO_NAME}.txt")

    if len(summary) > 5000:
        # If the summary is to long we can reapply the summarization function
        text_chunks = split_text_into_chunks(summary, max_tokens=1000)
        short_summary = get_summary_bart(text_chunks, summarizer, bart_params)
        save_summary_to_file(short_summary, f"short_summary_{VIDEO_NAME}")
        logging.info("Summary saved to file.")
        print(f"\n\nShort summary saved in the file short_summary_{VIDEO_NAME}.txt")
    else:
        logging.error("Error: Unable to generate summary.")


    print("\n\nEND\n\n")

