#!/usr/bin/python3

import random
import subprocess
import os
import sys
import time
import glob
import pygame
import re
import pexpect
import argparse
import pprint

class BlackScreenException(Exception):
  pass

def blackScreen():
  pygame.display.init();
  black = 0, 0, 0
  screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
  screen.fill(black)
  pygame.mouse.set_visible(0)
  return screen

def toggleSound(child):
  global muted
  if muted:
    playSound(child)
    muted = 0
  else:
    muteMovie(child)
    muted = 1


def muteMovie(child):
  for i in range(1,20):
    child.write("-")
    child.expect("Current Volume:")

def playSound(child):
  for i in range(1,20):
    child.write("=")
    child.expect("Current Volume:")

def stopMovie(child):
  child.write("q")

def playVideo(video):
  print('Playing ' + video)
  try:
    muteoption = ""
    if muted:
      muteoption = "--vol -6000 "
    child = pexpect.spawn("/usr/bin/omxplayer --no-osd --aspect-mode fill " + muteoption + video)
    while child.isalive():
      # Keyboard Events
      # ESC = quit
      # SPACE = skip
      time.sleep(0.1)
    time.sleep(2)
    return True
  except BlackScreenException:
    stopMovie(child)
    raise BlackScreenException
  except pexpect.ExceptionPexpect:
    return True

def playScript(script, duration):
  print("playing " + script + " for " + str(duration))
  try:
    child = pexpect.spawn("./" + script + ".sh")
    child.logfile = sys.stdout
    endTime = time.time() + duration
    while child.isalive():
      time.sleep(1.0)
      if time.time() >= endTime:
        child.close()
        return True
  except pexpect.ExceptionPexpect:
    return True
  

def playVideos(path, videos):
  for video in videos:
    video = video.replace(" ", "\ ")
    isMp4 = re.match(".*\.mp4$", video)
    isMkv = re.match(".*\.mkv$", video)
    if isMp4 or isMkv:
      playNext = playVideo(path + "/" + video)
      if not playNext:
        return False
  return True

def loadVideos(path):
  videos = os.listdir(path)
  if (args.sequential):
    videos.sort()
  else:
    random.shuffle(videos)
  return videos

def done():
  pygame.display.quit()
  pygame.quit()
  sys.exit(0)

muted = 1
parser = argparse.ArgumentParser(description='Play some videos')
parser.add_argument('--sequential', action='store_true')
parser.add_argument('--unmuted', action='store_true')
parser.add_argument('--path')
args = parser.parse_args()

try:
  while True:
    try:
      screen = blackScreen()
    except:
      print("could not start pygame")
    if args.unmuted:
      muted = 0;

    videos = []
    if args.path != None:
      videos = loadVideos(args.path)
    else:
      videos = loadVideos(os.getcwd() + "/videos")

    while True:
      for video in videos:
        video = video.replace(" ", "\ ")
        isMp4 = re.match(".*\.mp4$", video)
        isMkv = re.match(".*\.mkv$", video)
        if isMp4 or isMkv:
          playVideo("/home/alice/barsandtone.mp4")
          playScript("webcam", 3 * 60.0)
          playScript("garage", 3 * 60.0)
          playScript("desk", 3 * 60.0)
          playVideo("/home/alice/barsandtone.mp4")
          playVideo(args.path + "/" + video)

except KeyboardInterrupt:
  done()
except SystemExit:
  done()
