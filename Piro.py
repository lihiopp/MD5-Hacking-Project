import screen_brightness_control as sbc
from playsound import playsound


def brighten_screen():
    sbc.set_brightness(100)


def fade_screen():
    sbc.set_brightness(0)


def screen_brightness():
    original_brightness = sbc.get_brightness()
    for i in range(15):
        brighten_screen()
        fade_screen()
    sbc.set_brightness(original_brightness)


def sound_effect():
    playsound('C:\\Users\\amitw\\Desktop\\sound_effect_wav.wav')


def main():
    screen_brightness()
    sound_effect()


if __name__ == "__main__":
    main()
