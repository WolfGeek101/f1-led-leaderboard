from data.standings import StandingsItem
from renderer.renderer import Renderer
from utils import Color, align_text, Position


class ConstructorStandings(Renderer):
    """
    Render constructor standings

    Arguments:
        data (api.Data):                        Data instance

    Attributes:
        standings (list[StandingsItem]):        Constructor standings
        text_color (tuple):                     Text color
        offset (int):                           Row y-coord offset
        coords (dict):                          Coordinates dictionary
        text_y (int):                           Constructor's name & points y-coord
    """

    def __init__(self, matrix, canvas, draw, layout, data):
        super().__init__(matrix, canvas, draw, layout)
        self.data = data
        self.standings = self.data.constructor_standings.items
        self.text_color = Color.WHITE
        self.offset = self.font_height + 2
        self.coords = self.layout.coords['standings']['constructors']
        self.text_y = self.coords['name']['y']

    def render(self):
        self.new_canvas(self.matrix.width, self.coords['row_height'] * (len(self.standings) + 1) + 1)
        self.render_header()
        for constructor in self.standings:
            self.render_row(constructor)
        self.scroll_up(self.canvas)
        self.text_y = self.coords['name']['y']  # Reset

    def render_header(self):
        x, y = align_text(self.font.getsize('Constructors'),
                          self.matrix.width,
                          self.matrix.height,
                          Position.CENTER,
                          Position.TOP)
        y += self.coords['header']['offset']['y']

        self.draw.rectangle(((0, 0), (self.matrix.width, y + self.font_height - 1)), fill=Color.GRAY)
        self.draw.text((x, y), 'Constructors', fill=Color.WHITE, font=self.font)

    def render_row(self, constructor: StandingsItem):
        bg_color, self.text_color = constructor.item.colors

        self.render_background(bg_color)
        self.render_name(constructor.item.name)
        self.render_points(f'{constructor.points:g}')

        self.text_y += self.offset

    def render_background(self, color: tuple):
        self.draw.rectangle(((0, self.text_y - 1),
                             (self.matrix.width, self.text_y + self.font_height - 1)),
                            fill=color)

    def render_name(self, name: str):
        x = self.coords['name']['x']
        self.draw.text((x, self.text_y), name, fill=self.text_color, font=self.font)

    def render_points(self, points: str):
        x = align_text(self.font.getsize(points),
                       col_width=self.matrix.width,
                       x=Position.RIGHT)[0]
        self.draw.text((x, self.text_y), points, fill=self.text_color, font=self.font)
