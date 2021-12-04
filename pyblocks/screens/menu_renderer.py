from pygame.font import Font
from pygame.draw import rect


class MenuRenderer(object):
    BG_COLOR = (0, 0, 0, 0)
    BANNER_TEXT = "BLOCKS"
    BANNER_COLORS = [(255, 0, 0), (0, 0, 255), (255, 255, 0), (0, 255, 0), (0, 242, 255), (191, 0, 179)]

    def __init__(self, screen, title_font_file):
        self.screen = screen
        self.banner = self._render_banner(MenuRenderer.BANNER_TEXT, MenuRenderer.BANNER_COLORS, title_font_file)

    def _render_banner(self, banner_text, banner_colors, title_font_file):
        banner = []
        font = Font(title_font_file, 120)
        font_size = font.size(banner_text)

        # Get the upper left corner of where the text should go
        screen_size = self.screen.get_size()
        x = screen_size[0] // 2 - font_size[0] // 2
        y = screen_size[1] // 4 - font_size[1] // 2

        letters = list(banner_text)
        for letter, color in zip(letters, banner_colors):
            rendered = font.render(letter, True, color)
            banner.append((rendered, (x, y)))
            x += rendered.get_size()[0]

        return banner

    def render(self, active_menu_context):
        self._fill_background()
        self._highlight_selection(active_menu_context)
        self._draw_banner()
        self._draw_text(active_menu_context)

    def _draw_banner(self):
        for letter in self.banner:
            self.screen.blit(letter[0], letter[1])

    def _fill_background(self):
        self.screen.fill(MenuRenderer.BG_COLOR)

    def _highlight_selection(self, active_menu_context):
        overhang_horiz_px = 20
        overhang_vert_px = 5
        item = active_menu_context.get_render_info().get_text_renderer().get_rendered_item(
            active_menu_context.get_selected_index())
        left = item.get_x() - overhang_horiz_px
        top = item.get_y() - overhang_vert_px
        width = item.get_width() + (2 * overhang_horiz_px)
        height = item.get_height() + (2 * overhang_vert_px)
        color = active_menu_context.get_render_info().get_highlight_color()
        rect(self.screen, color, (left, top, width, height), 0)

    def _draw_text(self, active_menu_context):
        for item in active_menu_context.get_render_info().get_text_renderer().get_rendered_items().values():
            self.screen.blit(item.get_item_content(), (item.get_x(), item.get_y()))


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

        self.item_content = font.render(label, 1, RenderableMenuItem.TEXT_COLOR)
        self.width = text_size[0]
        self.height = text_size[1]
        self.x_coord = xpos
        self.y_coord = ypos

    def get_item_content(self):
        return self.item_content

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_x(self):
        return self.x_coord

    def get_y(self):
        return self.y_coord


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

    def get_labels(self):
        return self.label_provider()

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

    def get_rendered_item(self, label_index):
        label = self.get_labels()[label_index]
        return self.get_rendered_items()[label]


# Renders all the menu options up front
class StandardTextRenderer(object):
    def __init__(self, font_file, screen_size, labels):
        self.font = Font(font_file, 50)
        self.screen_size = screen_size
        self.labels = labels
        self.text = {}
        self.rendered = self._render_text()

    def get_labels(self):
        return self.labels

    def _render_text(self):
        rendered = {}
        center_x = self.screen_size[0] // 2
        center_y = self.screen_size[1] // 2

        itemindex = 0
        for label in self.labels:
            item = RenderableMenuItem(label, itemindex, center_x, center_y, self.font)
            rendered[label] = item
            itemindex += 1
        return rendered

    # The items are in the following format:
    #   {"item name": (renderedText, textWidth, textHeight, xPos, yPos), ...}
    def get_rendered_items(self):
        return self.rendered

    def get_rendered_item(self, label_index):
        label = self.get_labels()[label_index]
        return self.get_rendered_items()[label]


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