#!/usr/bin/env python3

import argparse
import os
import sys
import pyperclip
import keyboard
import beepy
import json
import time
import re

from kb import Kb
from ai import Ai
from submodel import Submodel

def beep_start():
    keyboard.call_later(lambda: beepy.beep(sound=1), delay=0)

def beep_success():
    keyboard.call_later(lambda: beepy.beep(sound=0), delay=0)

def beep_cancel():
    keyboard.call_later(lambda: beepy.beep(sound=3), delay=0)

class App:
    def __init__(self, ai, kb):
        self.ai = ai
        self.kb = kb
        self.models = []

    def _hotkey(self, keys, fn, args=[]):
        cb = lambda: self._run(fn)
        self.kb.add_hotkey(keys, cb)

    def _read_prompts(self):
        """read prompts from files in ./prompts to a dict"""
        for filename in sorted(os.listdir('prompts')):
            s = open('prompts/' + filename).read()
            model = Submodel(ai)
            try:
                model.loads(s)
                model.filename = filename
                self.models.append(model)
                print(f'Loaded {filename}', f"'{model.options['pattern']}'")
            except BaseException as err:
                print(f'Skipped {filename}', err)

    def init(self):
        self._read_prompts()
        self._hotkey('alt gr, alt gr', self._autodetected_action)
        self.kb.resume()

    def _find_model(self, text):
        for model in self.models:
            does_match = model.match(text)
            if does_match: return model

    def _autodetected_action(self):
        copied = pyperclip.paste()
        print('text:', copied)

        model = self._find_model(copied)
        if model is None:
            print('Could not find matching pattern')
            return

        print('model:', model.filename, model.options['pattern'])
        return model.process(copied)

    def _run(self, fn):
        """unhook, run fn, handle errors, handle cancel, type, hook"""
        self.kb.pause()
        try:
            print('=' * 60)
            res = fn()
            print('-' * 40, 'Response:')
            for part in res:
                if keyboard.is_pressed('esc'):
                    print('CANCELED')
                    beep_cancel()
                    self.kb.resume()
                    return
                print(part, end='')
                self.kb.write(part)
            print('OK')
        except BaseException as err:
            print('ERROR')
            print(err)
            beep_cancel()
        self.kb.resume()

openai_api_key = os.getenv("OPENAI_API_KEY")
ai = Ai(openai_api_key)
kb = Kb()
app = App(ai, kb)

def main():
    app.init()
    print("Started")

    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print('\nDone')

main()
