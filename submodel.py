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

from ai import Ai

class Submodel:
    def __init__(self, ai):
        self.ai = ai
        self.options = None
        self.prefix = None

    def loads(self, conf):
        h_end, p_start = re.search('\n\n', conf).span()
        header, prefix = conf[:h_end], conf[p_start:]
        options = json.loads(header)
        if 'pattern' not in options:
            raise Exception(f'No pattern in config')
        if 'model' not in options:
            raise Exception(f'No model in config')
        self.options = options
        self.prefix = prefix

    def match(self, prompt):
        found = re.search(self.options['pattern'], prompt)
        return found is not None

    def process(self, prompt, **kwargs):
        params = {
            **kwargs,
            **self.options['model'],
            'prompt': self.prefix + prompt,
        }
        print(params['prompt'])
        return self.ai.complete(params)
