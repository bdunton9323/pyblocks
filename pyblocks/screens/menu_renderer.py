from pygame.font import Font


class MenuRenderer(object):

    def __init__(self, menu_info):
        pass


class RenderableMenuItem(object):
    # pixels to put between each menu item
    PADDING = 50
    # color to draw the menu text
    TEXT_COLOR = (128, 255, 255)

    # label - the actual text to render
    # item_index - indicates which item within the menu options this is. Determines the vertical position.
    # center_x - the x-coordinate of the center of the display area
    # center_y - the y-coordinate of the center of the display area
    def __init__(self, label, item_index, center_x, center_y, font):
        text_size = font.size(label)
        xpos = center_x - (text_size[0] // 2)
        ypos = center_y - (text_size[1] // 2) + (RenderableMenuItem.PADDING * item_index)
        self.rendered_menu_item = (
            font.render(label, 1, RenderableMenuItem.TEXT_COLOR),
            # width of text
            text_size[0],
            # height of text
            text_size[1],
            # x position on screen of text
            xpos,
            # y position on screen of text
            ypos
        )

    def get_rendered_item(self):
        return self.rendered_menu_item


# Renders the labels each time they are needed. This allows the menu labels
# to be dynamic (e.g. text that changes as options are toggled)
class LazyTextRenderer(object):
    def __init__(self, label_provider, font_file, screen_size):
        self.label_provider = label_provider
        self.font = Font(font_file, 50)
        self.screen_size = screen_size
        self.center_x = screen_size[0] // 2
        self.center_y = screen_size[1] // 2
        # cache the RenderableMenuItems by their label because rendering is expensive.
        self.rendered = {}

    # We will generate our own labels, so this is a no-op
    def init_text(self):
        pass

    def get_labels(self):
        return self.label_provider.get_labels()

    def render_labels(self, labels):
        index = 0
        updated = {}
        for label in labels:
            # cache the labels because rendering is expensive
            if label in self.rendered:
                updated[label] = self.rendered[label]
            else:
                updated[label] = RenderableMenuItem(label, index, self.center_x, self.center_y, self.font)
            index += 1

        self.rendered = updated
        return self.rendered

    # The items are in the following format:
    #   {"item name": (renderedText, textWidth, textHeight, xPos, yPos), ...}
    def get_rendered_items(self):
        return self.render_labels(self.get_labels())


# Renders all the menu options up front
class StandardTextRenderer(object):
    def __init__(self, font_file, screen_size, labels):
        self.font = Font(font_file, 50)
        self.screen_size = screen_size
        self.labels = labels
        self.rendered = {}
        self.text = {}

    def get_labels(self):
        return self.labels

    def init_text(self):
        self.rendered = {}
        center_x = self.screen_size[0] // 2
        center_y = self.screen_size[1] // 2

        itemindex = 0
        self.text = {}
        for label in self.labels:
            item = RenderableMenuItem(label, itemindex, center_x, center_y, self.font)
            self.rendered[label] = item
            itemindex += 1

    # The items are in the following format:
    #   {"item name": (renderedText, textWidth, textHeight, xPos, yPos), ...}
    def get_rendered_items(self):
        return self.rendered


# A simple highlight strategy where the highlight color is always the same
# regardless of mode
class HighlightStrategyNormal(object):
    HIGHLIGHT_COLOR = (0, 0, 255)

    def __init__(self):
        pass

    def get_highlight_color(self):
        return HighlightStrategyNormal.HIGHLIGHT_COLOR


# This highlight strategy highlights a different color if the menu option is waiting for input.
class HighlightStrategyInputField(object):
    SPECIAL_HIGHLIGHT = (128, 0, 0)
    NORMAL_HIGHLIGHT = (0, 0, 255)

    def __init__(self, listening_status_provider):
        self.listening_status_provider = listening_status_provider

    def get_highlight_color(self):
        if self.listening_status_provider():
            return HighlightStrategyInputField.SPECIAL_HIGHLIGHT
        else:
            return HighlightStrategyInputField.NORMAL_HIGHLIGHT