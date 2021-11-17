# TODO: this could just be a named tuple
class GameParams:
    def __init__(self):
        self.screen = None
        self.geo = None

    def set_screen(self, screen):
        self.screen = screen

    def get_screen(self):
        return self.screen

    def set_geometry(self, geometry):
        self.geo = geometry

    def get_geometry(self):
        return self.geo

    def set_jukebox(self, jukebox):
        self.jukebox = jukebox

    def get_jukebox(self):
        return self.jukebox

    def set_key_change_publisher(self, publisher):
        self.key_change_publisher = publisher

    def get_key_change_publisher(self):
        return self.key_change_publisher

    def set_key_mapper(self, key_mapper):
        self.key_mapper = key_mapper

    def get_key_mapper(self):
        return self.key_mapper
