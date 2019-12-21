#!/usr/bin/python3

import random
import subprocess
import os
import sys
import time
import glob
import pygame
import re

muted = False

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
    muted = True
  else:
    muteMovie(child)
    muted = False


def muteMovie(child):
  child.communicate(input=b"---")[0]

def playSound(child):
  child.communicate(input=b"+++")[0]

def stopMovie(child):
  child.communicate(input=b"q")[0]

def playVideo(video):
  print('Playing ' + video)
  try:
    child = subprocess.Popen(['/usr/bin/omxplayer', '--no-osd', video], stdin = subprocess.PIPE)
    while child.poll() is None:
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
  except subprocess.CalledProcessError:
    print ("omxplayer output:", e.output)
    return False


def playVideos(path, videos):
  for video in videos:
    isMp4 = re.match(".*\.mp4$", video)
    isMkv = re.match(".*\.mkv$", video)
    if isMp4 or isMkv:
      playNext = playVideo(path + "/" + video)
      if not playNext:
        return False
  return True

def loadVideos(path):
  videos = os.listdir(path)
  random.shuffle(videos)
  while True:
    keepPlaying = playVideos(path, videos)
    if not keepPlaying:
      return

def done():
  pygame.display.quit()
  pygame.quit()
  sys.exit(0)

try:
  while True:
    screen = blackScreen()
    if len(sys.argv) > 1:
      loadVideos(sys.argv[1])
    else:
      loadVideos(os.getcwd() + "/videos")
except KeyboardInterrupt:
  done()
except SystemExit:
  done()
