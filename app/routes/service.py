import os
import json
import requests
import time
from flask import current_app
from app.models import Projects, Posts
from app import db
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip

