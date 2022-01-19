import pytest
import sys
import logging
import PIL
import rgbmatrix
import utils
from utils import Position


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason='Requires Linux')
class TestUtils:
    def test_read_json(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.ERROR):
            utils.read_json('invalid.json')
        assert "Couldn't find file at invalid.json" in caplog.text

    def test_load_font(self):
        font = utils.load_font('rpi-rgb-led-matrix/fonts/5x7.bdf')
        assert isinstance(font, rgbmatrix.graphics.Font)

    def test_load_font_2(self):
        font = utils.load_font('rpi-rgb-led-matrix/fonts/5x7.bdf')
        assert font.baseline, 6

    def test_load_font_3(self):
        font = utils.load_font('rpi-rgb-led-matrix/fonts/5x7.bdf')
        assert font.height, 7

    def test_load_font_4(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.WARNING):
            utils.load_font('invalid.bdf')
        assert f"Couldn't find font invalid.bdf. Setting font to default 4x6." in caplog.text

    def test_load_font_5(self):
        font = utils.load_font('invalid.bdf')
        assert isinstance(font, rgbmatrix.graphics.Font)

    def test_load_font_6(self):
        font = utils.load_font('invalid.bdf')
        assert font.baseline == 5

    def test_load_font_7(self):
        font = utils.load_font('invalid.bdf')
        assert font.height == 6

    def test_load_image(self):
        image = utils.load_image('assets/img/error.png', (15, 15))
        assert isinstance(image, PIL.Image.Image)

    def test_load_image_2(self):
        image = utils.load_image('assets/img/error.png', (15, 15))
        assert image.size <= (15, 15)

    def test_load_image_3(self):
        image = utils.load_image('assets/img/error.png')
        assert isinstance(image, PIL.Image.Image)

    def test_load_image_4(self):
        image = utils.load_image('assets/img/error.png')
        assert image.size <= (64, 32)

    def test_load_image_5(self, caplog):
        caplog.clear()
        with caplog.at_level(logging.ERROR):
            utils.load_image('invalid.jpg')
        assert f"Couldn't find image invalid.jpg" in caplog.text

    def test_load_image_6(self):
        image = utils.load_image('invalid.jpg')
        assert image is None

    def test_align_text(self):
        x, y = utils.align_text('Lorem ipsum', Position.CENTER, Position.CENTER, 64, 32, 4, 6)
        assert (x, y) == (10, 19)

    def test_align_text_2(self):
        x = utils.align_text('Lorem ipsum', x=Position.CENTER, col_width=64, font_width=4)
        assert x == 10

    def test_align_text_3(self):
        y = utils.align_text('Lorem ipsum', y=Position.CENTER, col_height=32, font_height=6)
        assert y == 19

    def test_align_text_4(self):
        x = utils.align_text('Lorem ipsum', x=Position.RIGHT, col_width=64, font_width=4)
        assert x == 20

    def test_align_text_5(self):
        x = utils.align_text('Lorem ipsum', y=Position.BOTTOM, col_height=32)
        assert x == 32

    def test_align_image(self):
        img = utils.load_image('assets/img/error.png', (15, 15))
        x, y = utils.align_image(img, Position.CENTER, Position.CENTER, 64, 32)
        assert (x, y) == (25, 10)

    def test_align_image_2(self):
        img = utils.load_image('assets/img/error.png', (15, 15))
        x = utils.align_image(img, x=Position.CENTER, col_width=64)
        assert x == 25

    def test_align_image_3(self):
        img = utils.load_image('assets/img/error.png', (15, 15))
        y = utils.align_image(img, y=Position.CENTER, col_height=32)
        assert y == 10

    def test_split_into_pages(self):
        lst = [0, 1, 2, 5, 7, 9, 13]
        n = 2
        pages = utils.split_into_pages(lst, n)
        assert len(pages) == 4
