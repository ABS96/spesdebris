import macpy
import itertools

WHITESPACE_CHARS = " \r"

def handle_hotstring(e):
    print(e)

    if e.trigger is None:
        # Can trigger inside word
        kbd.keypress(keys.KEY_LEFTSHIFT, keystates.PRESSED)
        for _ in itertools.repeat(None, len(e.string)):
            kbd.keypress(keys.KEY_LEFT)
        kbd.keypress(keys.KEY_LEFTSHIFT, keystates.RELEASED)
    else:
        # A trigger character was used
        for _ in itertools.repeat(None, len(e.string) + len(e.trigger)):
            kbd.keypress(keys.KEY_BACKSPACE)


    kbd.type("macska" + (e.trigger or ''))

def handle_keyboard_event(e):
    #print(e)
    pass

def keyboard_cleanup():
    kbd.uninstall_keyboard_hook()

kbd = macpy.Keyboard()
keys = macpy.key.Key
keystates = macpy.key.KeyState

kbd.install_keyboard_hook(handle_keyboard_event)
kbd.register_hotstring("cica", '', handle_hotstring)