import pyperclip
import keyboard
import time


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


class Kb:
    def __init__(self):
        self.cbs = {}
        # {
        #     'alt gr': {
        #         'k': lambda: print('k'),
        #         'l': lambda: print('l'),
        #     },
        #     'ctrl': {
        #         'y': lambda: print('y'),
        #     },
        # }

    def add_hotkey(self, hotkey, cb):
        """ keyboard.add_hotkey dosn't handle comma separated hotkeys properly for some reason """
        keys = hotkey.split(', ')
        lvl = self.cbs
        for i, key in enumerate(keys):
            if key not in lvl:
                if i < len(keys) - 1:
                    lvl[key] = {}
                else:
                    lvl[key] = cb
            lvl = lvl[key]

    def resume(self):
        self.level = self.cbs
        keyboard.on_release(lambda key: self._handle_key(key))

    def pause(self):
        keyboard.unhook_all()

    def _handle_key(self, key):
        # print(key.name)
        # print(self.level)
        if key.name in self.level:
            cb = self.level[key.name]
            if callable(cb):
                try:
                    cb()
                except BaseException as err:
                    print(err)
            else:
                self.level = cb
        else:
            self.level = self.cbs

    def write(self, text):
        # With delay <=0.03 vscode sometimes inserts unexpected completions that interfere with input
        # Disable "Editor › Inline Suggest: Enabled" option in vscode for more stable behavior.
        # Without exact=True '{' and '}' cause strange behaviour
        # Without restore_state_after=True it appears that some keys (e.g. 'ctrl') may stay pressed
        ## keyboard.write(text, delay=0.05, restore_state_after=True, exact=True)

        old = pyperclip.paste()
        pyperclip.copy(text)
        time.sleep(0.05) # first insert may get skipped if delay is too short
        keyboard.send('right shift+ins') # seems to be the most reliable way to insert text anywhere
        time.sleep(0.05) # if clipboard content is changed too soon the output may be unstable
        pyperclip.copy(old)

