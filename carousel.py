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
    child = pexpect.spawn("/usr/bin/omxplayer --no-osd " + muteoption + video)
    while child.isalive():
      # Keyboard Events
      # ESC = quit
      # SPACE = skip
      for event in pygame.event.get():
        if (event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
          raise BlackScreenException()
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
          stopMovie(child)
          return True
        elif (event.type == pygame.KEYDOWN and event.key == pygame.K_m):
          toggleSound(child)

      time.sleep(0.1)
    time.sleep(2)
    return True
  except BlackScreenException:
    stopMovie(child)
    raise BlackScreenException
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
  while True:
    if (args.sequential):
      random.shuffle(videos)
    else
      videos.sort()
    keepPlaying = playVideos(path, videos)
    if not keepPlaying:
      return

def done():
  pygame.display.quit()
  pygame.quit()
  sys.exit(0)

muted = 1
parser = argparse.ArgumentParser(description='Play some videos')
parser.add_argument('--sequential', action='store_true')
parser.add_argument('--path')
args = parser.parse_args()

try:
  while True:
    screen = blackScreen()
    if args.path != None:
      loadVideos(args.path)
    else:
      loadVideos(os.getcwd() + "/videos")
except KeyboardInterrupt:
  done()
except SystemExit:
  done()
