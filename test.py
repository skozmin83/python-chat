#!/usr/bin/env python3
import sys
import socket
import Logging
from PIL import Image
import tkinter as tk
from tkinter import filedialog
from threading import Event, Thread
import codecs
import io

def test():
    """Simple test program."""
    root = tk.Tk()
    root.withdraw()
    fd = LoadFileDialog(root)
    loadfile = fd.go(key="test")
    fd = SaveFileDialog(root)
    savefile = fd.go(key="test")
    print(loadfile, savefile)