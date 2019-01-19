import json
import requests
from flask_babel import _
from app import app

def translate(text, source_language, dest_language):
    # this is supposed to be a translation function that uses
    # Microsoft Translator API, but I did not want to make an account and I don't
    # want to use a credit card to register
    # so I just return the text.
    # I will implement it later
    return text
