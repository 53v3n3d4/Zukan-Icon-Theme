import importlib

from unittest import TestCase
from unittest.mock import patch

color_dark_light = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.color_dark_light'
)


class TestColorDarkLight(TestCase):
    # convert_to_rgb
    def test_convert_to_rgb_hex(self):
        list_hex = [
            ('#392E2A', [57, 46, 42]),  # Biohack
            ('#18171B', [24, 23, 27]),  # Blackcomb
            ('#C4E7CE', [196, 231, 206]),  # Bowtruckle
            ('#F9EFDA', [249, 239, 218]),  # DO
            ('#FFFFFF', [255, 255, 255]),  # Fuji
            ('#B2D6FB', [178, 214, 251]),  # Lagoon
            ('#F3EFF2', [243, 239, 242]),  # Nimbus
            ('#3B273D', [59, 39, 61]),  # Roci
            ('#262833', [38, 40, 51]),  # Zora
        ]

        for p1, p2 in list_hex:
            with self.subTest(list_hex):
                result = color_dark_light.convert_to_rgb(p1)
                self.assertEqual(result, p2)

    def test_convert_to_rgb_hsl(self):
        list_hsl = [
            ('hsl(16, 15.15%, 19.41%)', [57, 46, 42]),  # Biohack
            ('hsl(255, 8%, 9.8%)', [24, 23, 27]),  # Blackcomb
            ('hsl(137, 42.17%, 83.73%)', [196, 231, 206]),  # Bowtruckle
            ('hsl(41, 72.09%, 91.57%)', [249, 239, 218]),  # DO
            ('hsl(0, 0%, 100%)', [255, 255, 255]),  # Fuji
            ('hsl(210, 90.1%, 84.1%)', [178, 214, 251]),  # Lagoon
            ('hsl(315, 14.29%, 94.51%)', [243, 239, 242]),  # Nimbus
            ('hsl(294, 22%, 19.61%)', [59, 39, 61]),  # Roci
            ('hsl(231, 14.61%, 17.45%)', [38, 40, 51]),  # Zora
            ('hsla(111, 14%, 14%, 0.5)', [32, 41, 31]),  # Test 1 >= hube > 2 and alpha
        ]

        for p1, p2 in list_hsl:
            with self.subTest(list_hsl):
                list_rgb = color_dark_light.convert_to_rgb(p1)
                result = [round(i, 0) for i in list_rgb]

                self.assertEqual(result, p2)

    def test_convert_to_rgb_rgb(self):
        list_rgb = [
            ('rgb(57, 46, 42)', [57, 46, 42]),  # Biohack
            ('rgb(24, 23, 27)', [24, 23, 27]),  # Blackcomb
            ('rgb(196, 231, 206)', [196, 231, 206]),  # Bowtruckle
            ('rgb(249, 239, 218)', [249, 239, 218]),  # DO
            ('rgb(255, 255, 255)', [255, 255, 255]),  # Fuji
            ('rgb(178, 214, 251)', [178, 214, 251]),  # Lagoon
            ('rgb(243, 239, 242)', [243, 239, 242]),  # Nimbus
            ('rgb(59, 39, 61)', [59, 39, 61]),  # Roci
            ('rgb(38, 40, 51)', [38, 40, 51]),  # Zora
            ('rgba(32, 41, 31, 0.5)', [32, 41, 31]),  # Test alpha
        ]

        for p1, p2 in list_rgb:
            with self.subTest(list_rgb):
                result = color_dark_light.convert_to_rgb(p1)
                self.assertEqual(result, p2)

    def test_invalid_color(self):
        self.assertIsNone(color_dark_light.convert_to_rgb('invalid-color'))
        self.assertEqual(
            color_dark_light.convert_to_rgb('hsl(0, 200%, 50%)'),
            [382.5, -127.5, -127.5],
        )

    # st_colors_to_hex
    def test_st_colors_to_hex(self):
        ST_COLOR_PALETTE = [
            ('primary', '#392E2A'),  # Biohack
            ('secondary', '#F9EFDA'),  # DO
        ]
        with patch.object(
            color_dark_light,
            'ST_COLOR_PALETTE',
            ST_COLOR_PALETTE,
        ):
            self.assertEqual(color_dark_light.st_colors_to_hex('primary'), '#392E2A')
            self.assertEqual(color_dark_light.st_colors_to_hex('secondary'), '#F9EFDA')
            self.assertIsNone(color_dark_light.st_colors_to_hex('not_exist'))

    # extract_numbers_from_hsl
    def test_extract_numbers_from_hsl(self):
        list_extract_hsl = [
            ('hsl(16, 15.15%, 19.41%)', (16, 15.15, 19.41)),  # Biohack
            ('hsl(255, 8%, 9.8%)', (255, 8, 9.8)),  # Blackcomb
            ('hsl(137, 42.17%, 83.73%)', (137, 42.17, 83.73)),  # Bowtruckle
            ('hsl(41, 72.09%, 91.57%)', (41, 72.09, 91.57)),  # DO
            ('hsl(0, 0%, 100%)', (0, 0, 100)),  # Fuji
            ('hsl(210, 90.1%, 84.1%)', (210, 90.1, 84.1)),  # Lagoon
            ('hsl(315, 14.29%, 94.51%)', (315, 14.29, 94.51)),  # Nimbus
            ('hsl(294, 22%, 19.61%)', (294, 22, 19.61)),  # Roci
            ('hsl(231, 14.61%, 17.45%)', (231, 14.61, 17.45)),  # Zora
            (
                'hsla(111, 14%, 14%, 0.5)',
                (111, 14, 14, 0.5),
            ),  # Test 1 >= hube > 2 and alpha
        ]

        for p1, p2 in list_extract_hsl:
            with self.subTest(list_extract_hsl):
                result = color_dark_light.extract_numbers_from_hsl(p1)
                self.assertEqual(result, p2)

        self.assertIsNone(color_dark_light.extract_numbers_from_hsl('invalid-hsl'))

    # extract_numbers_from_rgb
    def test_extract_numbers_from_rgb(self):
        list_rgb = [
            ('rgb(57, 46, 42)', [57, 46, 42]),  # Biohack
            ('rgb(24, 23, 27)', [24, 23, 27]),  # Blackcomb
            ('rgb(196, 231, 206)', [196, 231, 206]),  # Bowtruckle
            ('rgb(249, 239, 218)', [249, 239, 218]),  # DO
            ('rgb(255, 255, 255)', [255, 255, 255]),  # Fuji
            ('rgb(178, 214, 251)', [178, 214, 251]),  # Lagoon
            ('rgb(243, 239, 242)', [243, 239, 242]),  # Nimbus
            ('rgb(59, 39, 61)', [59, 39, 61]),  # Roci
            ('rgb(38, 40, 51)', [38, 40, 51]),  # Zora
            ('rgba(32, 41, 31, 0.5)', [32, 41, 31]),  # Test alpha
        ]

        for p1, p2 in list_rgb:
            with self.subTest(list_rgb):
                result = color_dark_light.convert_to_rgb(p1)
                self.assertEqual(result, p2)

        self.assertIsNone(color_dark_light.extract_numbers_from_rgb('invalid-rgb'))

    # rgb_dark_light
    def test_rgb_dark_light(self):
        list_rgb = [
            ([57, 46, 42], 'dark'),  # Biohack
            ([24, 23, 27], 'dark'),  # Blackcomb
            ([196, 231, 206], 'light'),  # Bowtruckle
            ([249, 239, 218], 'light'),  # DO
            ([255, 255, 255], 'light'),  # Fuji
            ([178, 214, 251], 'light'),  # Lagoon
            ([243, 239, 242], 'light'),  # Nimbus
            ([59, 39, 61], 'dark'),  # Roci
            ([38, 40, 51], 'dark'),  # Zora
            ([115, 125, 140], 'dark'),  # Sublime base_ui variable, sidebar background
        ]

        for p1, p2 in list_rgb:
            with self.subTest(list_rgb):
                result = color_dark_light.rgb_dark_light(p1)
                self.assertEqual(result, p2)

    # get_icon_dark_light
    def test_get_icon_dark_light(self):
        list_bgcolor = [
            ('dark', 'light'),
            ('light', 'dark'),
            ('', 'dark'),
            ('not_valid', 'dark'),
            ('DARK', 'dark'),
            ('LIGHT', 'dark'),
            ('lighten', 'dark'),
        ]

        for p1, p2 in list_bgcolor:
            with self.subTest(list_bgcolor):
                result = color_dark_light.get_icon_dark_light(p1)
                self.assertEqual(result, p2)

    # hex_dark_light
    def test_hex_dark_light(self):
        list_hex = [
            ('#392E2A', 'dark'),  # Biohack
            ('#18171B', 'dark'),  # Blackcomb
            ('#C4E7CE', 'light'),  # Bowtruckle
            ('#F9EFDA', 'light'),  # DO
            ('#FFFFFF', 'light'),  # Fuji
            ('#B2D6FB', 'light'),  # Lagoon
            ('#F3EFF2', 'light'),  # Nimbus
            ('#3B273D', 'dark'),  # Roci
            ('#262833', 'dark'),  # Zora
        ]

        for p1, p2 in list_hex:
            with self.subTest(list_hex):
                result = color_dark_light.hex_dark_light(p1)
                self.assertEqual(result, p2)

    # Biohack colors
    # #392E2A, hsl(16, 15.15%, 19.41%), rgb(57, 46, 42)
    def test_extract_base_color(self):
        list_colors = [
            ('#392E2A', '#392E2A'),  # Hex
            ('rgb(57,46,42)', 'rgb(57,46,42)'),  # RGB
            ('hsl(16, 15.15%, 19.41%)', 'hsl(16, 15.15%, 19.41%)'),  # HSL
            ('color(#392E2A)', '#392E2A'),  # color with Hex
            ('color(rgb(57, 46, 42))', 'rgb(57, 46, 42)'),  # color with RGB
            (
                'color(hsl(16, 15.15%, 19.41%))',
                'hsl(16, 15.15%, 19.41%)',
            ),  # color with HSL
            ('color(#392E2A l(+ 2%))', '#392E2A'),  # color with modifier
            (
                'color(hsl(16, 15.15%, 19.41%) l(-10%) a(0.8))',
                'hsl(16, 15.15%, 19.41%)',
            ),  # color with modifiers
            ('color(  rgb(57, 46, 42) s(0.2))', 'rgb(57, 46, 42)'),  # color with spaces
            ('', ''),  # empty
        ]

        for p1, p2 in list_colors:
            with self.subTest(list_colors):
                result = color_dark_light.extract_base_color(p1)
                self.assertEqual(result, p2)

    def test_extract_base_color_return(self):
        self.assertIsNone(color_dark_light.extract_base_color('color('))

    def test_extract_base_color_not_valid(self):
        self.assertIsNone(color_dark_light.extract_base_color('color(foo bar)'))
