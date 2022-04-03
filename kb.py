import pyperclip
import keyboard

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
        """
        with delay <=0.03 vscode sometimes inserts unexpected completions that interfere with input
        Disable "Editor › Inline Suggest: Enabled" option in vscode for more stable behavior.
        without exact=True '{' and '}' cause strange behaviour
        without restore_state_after=True it appears that some keys (e.g. 'ctrl') may stay pressed
        """
        keyboard.write(text, delay=0.05, restore_state_after=True, exact=True)
