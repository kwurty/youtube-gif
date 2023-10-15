# Filename: conversion.py
from pytube import YouTube
from moviepy.editor import *

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

    def find720p(self):
        self.youtube720pStream = self.video.streams.filter(file_extension="mp4").filter(resolution="720p").first()

    def find1080p(self):
        self.youtube1080pStream = self.video.streams.filter(file_extension="mp4").filter(resolution="1080p").first()

    def downloadVideo(self):
        self.videoLocation = self.youtube720pStream.download();

    def setExport(self):
        pass

    def setClipLocation(self):
        self.moviePyFile = VideoFileClip(self.videoLocation, audio=False)

    def exportGif(self):
        print(self.startTime, self.clipLength)
        self.clip = self.moviePyFile.subclip(self.startTime, self.startTime + self.clipLength).resize(0.3)
        self.clip.write_gif("output.gif")