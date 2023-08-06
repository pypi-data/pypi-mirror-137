# flake8: noqa: F401
# noreorder
"""
Pytube: a very serious Python library for downloading YouTube Videos.
"""
__title__ = "pytube"
__author__ = "Ronnie Ghose, Taylor Fox Dahlin, Nick Ficano"
__license__ = "The Unlicense (Unlicense)"
__js__ = None
__js_url__ = None

from ytspace.pytube.version import __version__
from ytspace.pytube.streams import Stream
from ytspace.pytube.captions import Caption
from ytspace.pytube.query import CaptionQuery, StreamQuery
from ytspace.pytube.__main__ import YouTube
# from ytspace.pytube.contrib.playlist import Playlist
# from ytspace.pytube.contrib.channel import Channel
# from ytspace.pytube.contrib.search import Search
