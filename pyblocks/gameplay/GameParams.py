

class GameParams(object):
    def __init__(self):
        self.screen = None
        self.geometry = None
        self.jukebox = None
        self.keys = None
        self.key_change_publisher = None
        self.key_mapper = None
        self.high_score_reader = None
        self.high_score_writer = None

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, val):
        self._screen = val

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, val):
        self._geometry = val

    @property
    def jukebox(self):
        return self._jukebox

    @jukebox.setter
    def jukebox(self, val):
        self._jukebox = val

    @property
    def keys(self):
        return self._keys

    @keys.setter
    def keys(self, val):
        self._keys = val

    @property
    def key_change_publisher(self):
        return self._screen

    @key_change_publisher.setter
    def key_change_publisher(self, val):
        self._key_change_publisher = val

    @property
    def key_mapper(self):
        return self._key_mapper

    @key_mapper.setter
    def key_mapper(self, val):
        self._key_mapper = val

    @property
    def high_score_reader(self):
        return self._high_score_reader

    @high_score_reader.setter
    def high_score_reader(self, val):
        self._high_score_reader = val

    @property
    def high_score_writer(self):
        return self._high_score_writer

    @high_score_writer.setter
    def high_score_writer(self, val):
        self._high_score_writer = val
