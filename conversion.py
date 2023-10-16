# Filename: conversion.py
from pytube import YouTube
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip


class Conversions:

    def __init__(self, video: YouTube, export: str, startTime: int, clipLength: int):
      self.video = video
      self.export = export
      self.startTime = startTime
      self.clipLength = clipLength
      self.videoLocation = None
      self.youtube720pStream = None
      self.youtube1080pStream = None
      self.moviePyFile = None
      self.gifLocation = None
    def find720p(self):
        self.youtube720pStream = self.video.streams.filter(file_extension="mp4").filter(resolution="720p").first()

    def find1080p(self):
        self.youtube1080pStream = self.video.streams.filter(file_extension="mp4").filter(resolution="1080p").first()

    def downloadVideo(self):
        self.videoLocation = self.youtube720pStream.download();

    def setExport(self):
        pass

    def addText(self, message):
        # Load the video clip
        print(f"movie clip: ")
        print(self.moviePyFile)
        video_clip = self.videoLocation

        # Extract a subclip if needed (optional)
        # You can specify the start and end time in seconds
        # ffmpeg_extract_subclip("input_video.mp4", start_time, end_time, targetname="subclip.mp4")
        # video_clip = VideoFileClip("subclip.mp4")

        # Create a TextClip with the desired text
        txt_clip = TextClip(message, fontsize=30, color='white')

        # Set the duration of the text clip to match the video duration
        txt_clip = txt_clip.set_duration(video_clip.duration)

        # Position the text on the video (you can adjust the x, y coordinates)
        txt_clip = txt_clip.set_position(('center', 'bottom'))

        # Overlay the text clip on top of the video clip
        final_clip = video_clip.set_duration(video_clip.duration).set_audio(video_clip.audio)
        final_clip = final_clip.set_end(txt_clip.end)
        final_clip = final_clip.set_duration(video_clip.duration)
        final_clip = final_clip.set_audio(video_clip.audio)
        final_clip = final_clip.set_duration(video_clip.duration)

        # Write the final video with text to a file
        self.moviePyFile = final_clip

    def setClipLocation(self):
        self.moviePyFile = VideoFileClip(self.videoLocation, audio=False)

    def exportGif(self):
        self.clip = self.moviePyFile.subclip(self.startTime, self.startTime + self.clipLength).resize(0.3)
        self.clip.write_gif(f"E:\Programming\youtube-gif\gifs\{self.video.video_id}.gif", program='ffmpeg')
        self.gifLocation = f"E:\Programming\youtube-gif\gifs\{self.video.video_id}.gif"