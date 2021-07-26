"""
This file aims to address the downloading of all resources required by stanza and nltk
"""
import stanza
import nltk

stanza.download("fr")
nltk.download("stopwords")
