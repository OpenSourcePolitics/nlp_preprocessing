"""
This file aims to address the downloading of all resources required by stanza and nltk
"""
import stanza
import nltk

stanza.download("fr", "./cache/stanza_resources")
nltk.download("stopwords", "./cache/nltk_resources")
