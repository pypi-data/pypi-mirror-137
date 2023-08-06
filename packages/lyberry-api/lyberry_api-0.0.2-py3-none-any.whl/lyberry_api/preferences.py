from lbry import lbrynet
import subprocess
import json

prefs = {}

def load():
    lbry_prefs = lbrynet.request('preference_get')
    global prefs
    prefs = lbry_prefs

load()
