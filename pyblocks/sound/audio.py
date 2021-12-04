from collections import namedtuple


class Jukebox(object):
    DEFAULT_MUSIC_VOLUME = .5
    DEFAULT_SOUND_VOLUME = .8

    DEFAULT_MUSIC = 'Funky Deep'

    def __init__(self, mixer):
        self.mixer = mixer
        self.load_audio()

    def load_audio(self):
        # sound effects
        self.sounds = {}
        self.sounds['menu'] = self.mixer.Sound('audio/kick.ogg')
        self.sounds['piece_land'] = self.mixer.Sound('audio/blockhit.ogg')
        self.sounds['one_row'] = self.mixer.Sound('audio/explosiondebris.ogg')
        self.sounds['multi_row'] = self.mixer.Sound('audio/explosiondebris.ogg')
        self.sounds['typewriter'] = self.mixer.Sound('audio/typewriter.ogg')
        self.current_sound_volume = Jukebox.DEFAULT_SOUND_VOLUME
        self.set_sound_volume(self.current_sound_volume)

        # Music
        self.music = {}
        self.music['Funky Deep'] = 'audio/FunkyDeep.ogg'
        self.music['Solitude of the Soli'] = 'audio/SolitudeOfTheSoli.ogg'
        self.music['Mr. Wozzie'] = 'audio/MrWozzie.ogg'
        self.music['Fever'] = 'audio/Fever.ogg'
        self.mixer.music.load(self.music[Jukebox.DEFAULT_MUSIC])
        self.current_music_volume = Jukebox.DEFAULT_MUSIC_VOLUME
        self.set_music_volume(self.current_music_volume)

    def get_available_song_titles(self):
        return list(self.music)

    def set_song(self, song_title):
        if song_title in self.music:
            self.mixer.music.load(self.music[song_title])
            self.start_game_music()

    # volume - between 0 and 1
    def set_music_volume(self, volume):
        if volume > 1 or volume < 0:
            raise ValueError('volume must be between 0 and 1')
        self.mixer.music.set_volume(volume)

    def set_sound_volume(self, volume):
        if volume > 1 or volume < 0:
            raise ValueError('volume must be between 0 and 1')
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def enable_sound(self, enabled):
        if enabled:
            self.set_sound_volume(self.current_sound_volume)
        else:
            self.set_sound_volume(0)

    def enable_music(self, enabled):
        if enabled:
            self.start_game_music()
            self.set_music_volume(self.current_music_volume)
        else:
            self.stop_music()
            self.set_music_volume(0)

    def start_game_music(self):
        self.mixer.music.play(-1)

    def stop_sfx(self):
        self.menu_sound.stop()
        self.piece_landed.stop()
        self.one_row.stop()
        self.multi_row.stop()

    def stop_music(self):
        self.mixer.music.stop()

    def play_sound_menu_select(self):
        self.sounds['menu'].stop()
        self.sounds['menu'].play()

    def play_typewriter(self):
        self.sounds['typewriter'].stop()
        self.sounds['typewriter'].play()

    def play_sound_piece_landed(self):
        self.sounds['piece_land'].play()

    def play_sound_one_row(self):
        self.sounds['piece_land'].stop()
        self.sounds['one_row'].play()

    def play_sound_multi_row(self):
        self.sounds['piece_land'].stop()
        self.sounds['multi_row'].play()
