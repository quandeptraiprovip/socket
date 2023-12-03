from configparser import ConfigParser
import tkinter as tk
from tkinter import *
import socket
import base64
from PIL import Image, ImageTk
from io import BytesIO
import fitz

config = ConfigParser()
config.read("congfig.ini")

