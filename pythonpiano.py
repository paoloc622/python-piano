from pynput import keyboard
import AudioMixer.Mixer as mixer
import time
import wave
import traceback
pianomixer = mixer.Mixer()

isFlat = False

keymap = {}


keys=[  "1234567",
        "890qwer",
        "tyuiopa",
        "sdfghjk",
        "lzxcvbnm"]

notes = "CDEFGAB"
numbers = 1
note = 2

for octave in keys:
    for n in octave:
        keymap[n] = notes[note] + str(numbers)
        note += 1
        if note > 6:
            note = 0
            numbers += 1

for key, value in keymap.items():
    print('Keymap:', key, value)

class notemaker:

    def __init__(self, sound_mixer):
        self.notelist = []
        self.wavlist = {}
        for key in keymap.values():
            key_sound = wave.open(f"samples/{key}.wav")
            setattr(self, f"{key}", key_sound)
            self.notelist.append(key)
            self.wavlist[key] = (key_sound)
            print("Created sound for  key", key)

        for fkey in keymap.values():
            flat = f"{fkey}"
            flat = flat[0] + 'b' + flat[1]
            if flat[0:2] in ['Fb', 'Cb']:
                continue

            key_sound = wave.open(f"samples/{flat}.wav")
            setattr(self, f"{flat}", key_sound)
            self.notelist.append(flat)
            self.wavlist[flat] = (key_sound)
            print("Created sound for fkey", flat)
        sound_mixer.register(self.notelist, self.wavlist)



notes = notemaker(pianomixer)



def on_press(key):
    global isFlat

    try:
        if isFlat == True:
            flat = f'{keymap[key.char]}'
            flat = flat[0] + 'b' + flat[1]
            pianomixer.Sound(flat, getattr(notes, flat))
            print(f'{flat} pressed')
        else:
            pianomixer.Sound(keymap[key.char], getattr(notes, f'{keymap[key.char]}'))
            print(f'{keymap[key.char]} pressed')
    except Exception as E:
        print(f'special key {key} pressed')
        #print(traceback.format_exc())
    if key == keyboard.Key.shift:
        isFlat = True
def on_release(key):
    global isFlat
    if key == keyboard.Key.shift:
        isFlat = False
    try:
        print(f'{keymap[key.char]} released')
    except Exception as E:
        print(f'special key {key} released')
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start() #Until on_release returns false

pianomixer.playStream()
#while True:
#    print('sdsfsdfsdfs')
