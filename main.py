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
        self.prompt_start = ''

    def _hotkey(self, keys, fn, args=[]):
        cb = lambda: self._run(fn)
        self.kb.add_hotkey(keys, cb)

    def init(self):
        filepath = sys.argv[1] if len(sys.argv) > 1 else 'prompt.txt'
        self.prompt_start = open(filepath).read()
        self._hotkey('alt gr, alt gr', self._autodetected_action)
        self.kb.resume()

    def _autodetect(self, text):
        """return action, lang, text, suffix/instructions"""
        lang = 'text'

        js_comment_re = '\s*/\*(.*)\*/\s*'
        js_comment = re.search(js_comment_re, text)
        if js_comment is not None:
            lang = 'js'

        py_comment_re = '\s*"""(.*)"""\s*'
        py_comment = re.search(py_comment_re, text)
        if py_comment is not None:
            lang = 'py'

        insert_re = '___'
        insert = re.search(insert_re, text)
        if insert is not None:
            span = insert.span()
            return 'insert', lang, text[:span[0]], text[span[1]:]

        edit_re = '\n(.*)!!![\w\W]*'
        edit = re.search(edit_re, text)
        if edit is not None:
            if edit[1].strip() == '#':
                lang == 'py'
            if edit[1].strip() == '//':
                lang == 'js'
            edit_lines_re = re.compile('.*!!!(.*)', re.M)
            edit_lines = [m.strip() for m in edit_lines_re.findall(text)]
            instruction = '\n'.join(edit_lines)
            clean_text = re.sub(edit[0], '', text)
            return 'edit', lang, clean_text, instruction
        return 'complete', lang, text, None

    def _autodetected_action(self):
        copied = pyperclip.paste()
        action, lang, text, opt = self._autodetect(copied)
        eng = 'text' if lang == 'text' else 'code'
        print(action, lang, eng)
        print('text:', text)
        print('opt:', opt)

        stop = None
        if lang == 'js' and action != 'edit':
            text = self.prompt_start + text
            stop = ['/* ']
        if lang == 'py' and action != 'edit':
            stop = ['"""']

        if action == 'insert':
            return self.ai.complete(eng, text, opt, stop)
        if action == 'complete':
            return self.ai.complete(eng, text, opt, stop)
        if action == 'edit':
            return self.ai.edit(eng, text, opt)

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
