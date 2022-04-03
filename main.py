#!/usr/bin/env python3

import argparse
import os
import sys
import pyperclip
import keyboard
import beepy
# import pygame as pg
import openai
import json
import time
from kb import Kb

# def wait_all_released():
#     time.sleep(1)
#     keyboard.release(100)
#     keyboard.release(31)
#     time.sleep(1)
#     while True:
#         state = keyboard.stash_state()
#         print(state)
#         if len(state) == 0: return
#         time.sleep(0.1)

def copy_text():
    old = pyperclip.paste()
    time.sleep(0.5)
    keyboard.send('ctrl+a')
    time.sleep(0.5)
    keyboard.send('ctrl+c')
    text = pyperclip.paste()
    time.sleep(0.1)
    pyperclip.copy(old)
    return text

def paste_text(text):
    old = pyperclip.paste()
    pyperclip.copy(text)
    keyboard.send('ctrl+a')
    keyboard.send('ctrl+v')
    # time.sleep(0.1)
    pyperclip.copy(old)
    return

def beep_start():
    keyboard.call_later(lambda: beepy.beep(sound=1), delay=0)

def beep_success():
    keyboard.call_later(lambda: beepy.beep(sound=0), delay=0)

def beep_cancel():
    keyboard.call_later(lambda: beepy.beep(sound=3), delay=0)

class Ai:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if (openai.api_key is None or openai.api_key == ''):
            raise BaseException('no OPENAI_API_KEY')

    def complete_code(self, code):
        response = openai.Completion.create(
            engine="code-davinci-002",
            prompt="<|endoftext|>" + code,
            temperature=0,
            max_tokens=1000,
            # top_p=1,
            # frequency_penalty=0,
            # presence_penalty=0
            stop=["/* Command:"],
            stream=True
        )
        for part in response:
            if part["choices"][0]["finish_reason"] is not None: return
            yield part["choices"][0]["text"]

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
        # self._hotkey('alt gr, i', self._complete_codex_js_sandbox)
        self._hotkey('alt gr, alt gr', self._complete_codex_js_sandbox)
        self.kb.resume()

    def _complete_codex_js_sandbox(self):
        copied = pyperclip.paste()
        print('-' * 40, 'Copied:')
        print(f'{copied[0:100]}...')

        code = self.prompt_start + copied
        response = self.ai.complete_code(code)

        return response

    def _complete_all_codex_js_sandbox(self):
        copied = copy_text()
        print('-' * 40, 'Copied:')
        print(f'{copied[0:60]}...')

        code = self.prompt_start + copied
        response = self.ai.complete_code(code)

        keyboard.send('i')
        time.sleep(0.1)
        return response

    def _run(self, fn):
        """unhook, run fn, handle errors, handle cancel, type, hook"""
        self.kb.pause()
        try:
            print('=' * 60)
            res = fn()
            parts = []
            print('-' * 40, 'Response:')
            for part in res:
                if keyboard.is_pressed('esc'):
                    print('CANCELED')
                    beep_cancel()
                    self.kb.resume()
                    return
                parts.append(part)
                print(part, end='')
                self.kb.write(part)
            print('OK')
        except BaseException as err:
            print('ERROR')
            print(err)
            beep_cancel()
        self.kb.resume()

ai = Ai()
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
