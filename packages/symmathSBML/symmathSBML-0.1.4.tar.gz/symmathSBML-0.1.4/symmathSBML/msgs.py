"""Generate messages for the application."""

import sys

def error(text):
  print("***Error. %s" % text)
  sys.exit()

def warn(text):
  print("***Warning. %s" % text)
