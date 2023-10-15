from pytube import YouTube
from moviepy.editor import *
from conversion import Conversions
import tempfile

def main():

    url = ""
    time = ""
    length = ""

    while url=="":
        print("Enter your youtube link: ")
        url = input()

    youtube = YouTube(url)

    while time=="":
        print("Enter your start time (HH:MM:SS): ")
        time = input()
        time = time.split(":")
        if len(time) != 3:
            print("Please enter a correct time format (HH:MM:SS)")
            time = ""
        
        hours = time[0]
        minutes = time[1]
        seconds = time[2]
        startTime = (int(hours) * 60 * 60) + (int(minutes) * 60) + int(seconds)

        if(startTime > youtube.length):
            print(f"The time entered is longer than the actual video ")
            time=""

    while length=="":
        print("Enter your length in seconds (1-5): ")
        length = int(input())
        if(length > 5 or length < 1):
            print("Time must be between 1-5 seconds")
            length = ""

    conversion = Conversions(youtube, "/", startTime, length)
    conversion.find720p()
    conversion.downloadVideo()
    conversion.setClipLocation()
    conversion.exportGif()

    

    # local = VideoFileClip(downloaded)

    # clip = local.subclip(startTime, length)

    # clip.write_gif("output.gif", fps=25)

if __name__ == "__main__":
    main()