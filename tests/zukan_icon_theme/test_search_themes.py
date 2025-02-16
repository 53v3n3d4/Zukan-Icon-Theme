import importlib

from unittest import TestCase
from unittest.mock import Mock, patch

constants_icons_themes = importlib.import_module(
    'Zukan Icon Theme.tests.zukan_icon_theme.mocks.constants_icons_themes'
)
search_themes = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_themes'
)


class TestFilterResourcesThemes(TestCase):
    def test_mock_filter_resources_themes(self):
        filter_themes_list = ['a', 'b', 'c']
        mock = Mock()
        mock.search_themes.filter_resources_themes(filter_themes_list)
        mock.search_themes.filter_resources_themes.assert_called_with(
            filter_themes_list
        )

    def test_filter_resources_themes(self):
        result = search_themes.filter_resources_themes(
            constants_icons_themes.TEST_FILTER_THEMES_LIST
        )
        self.assertEqual(
            result, constants_icons_themes.TEST_FILTER_THEMES_LIST_EXPECTED
        )

    def test_filter_resources_themes_params(self):
        search_themes.filter_resources_themes(
            constants_icons_themes.TEST_FILTER_THEMES_LIST
        )
        self.assertIsInstance(constants_icons_themes.TEST_FILTER_THEMES_LIST, list)
        self.assertNotIsInstance(constants_icons_themes.TEST_FILTER_THEMES_LIST, int)
        self.assertNotIsInstance(constants_icons_themes.TEST_FILTER_THEMES_LIST, str)
        self.assertNotIsInstance(constants_icons_themes.TEST_FILTER_THEMES_LIST, bool)
        self.assertNotIsInstance(constants_icons_themes.TEST_FILTER_THEMES_LIST, dict)


class TestSearchResourcesSublimeThemes(TestCase):
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_themes.search_resources_sublime_themes'
    )
    def test_mock_search_resources_sublime_themes(
        self, search_resources_sublime_themes_mock
    ):
        search_resources_sublime_themes_mock.return_value = (
            constants_icons_themes.TEST_FILTER_THEMES_LIST_EXPECTED
        )

        self.assertEqual(
            search_themes.search_resources_sublime_themes(),
            constants_icons_themes.TEST_FILTER_THEMES_LIST_EXPECTED,
        )
        self.assertEqual(search_resources_sublime_themes_mock.call_count, 1)
        search_resources_sublime_themes_mock.assert_called_once()


class TestPackageThemeExists(TestCase):
    def setUp(self):
        self.mock_theme_paths = [
            'Packages/User/Treble Dark.sublime-theme',
            'Packages/Zukan Icon Theme/Theme/Treble Dark.sublime-theme',
            'Packages/Theme - Treble/Treble Dark.sublime-theme',
        ]

    @patch('sublime.find_resources')
    def test_package_theme_exists(self, mock_find_resources):
        mock_find_resources.return_value = self.mock_theme_paths

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_themes.filter_resources_themes'
        ) as mock_filter:
            with patch(
                'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_themes.search_resources_sublime_themes'
            ) as mock_search:
                mock_filter.return_value = [
                    'Packages/Theme - Treble/Treble Dark.sublime-theme'
                ]
                mock_search.return_value = [
                    'Packages/Theme - Treble/Treble Dark.sublime-theme'
                ]

                result = search_themes.package_theme_exists('Treble Dark.sublime-theme')

                self.assertTrue(result)
                mock_find_resources.assert_called_once_with('Treble Dark.sublime-theme')
                mock_filter.assert_called_once_with(self.mock_theme_paths)
                mock_search.assert_called_once()

    @patch('sublime.find_resources')
    def test_package_theme_exists_theme_not_found(self, mock_find_resources):
        mock_find_resources.return_value = self.mock_theme_paths

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_themes.filter_resources_themes'
        ) as mock_filter:
            with patch(
                'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_themes.search_resources_sublime_themes'
            ) as mock_search:
                mock_filter.return_value = ['Packages/Theme/Not Found.sublime-theme']
                mock_search.return_value = [
                    'Packages/Theme - Treble/Treble Dark.sublime-theme'
                ]

                result = search_themes.package_theme_exists('Not Found.sublime-theme')

                self.assertFalse(result)
                mock_find_resources.assert_called_once_with('Not Found.sublime-theme')

    @patch('sublime.find_resources')
    def test_package_theme_exists_empty_result(self, mock_find_resources):
        mock_find_resources.return_value = []

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_themes.filter_resources_themes'
        ) as mock_filter:
            with patch(
                'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_themes.search_resources_sublime_themes'
            ) as mock_search:
                mock_filter.return_value = []
                mock_search.return_value = []

                result = search_themes.package_theme_exists('Not Found.sublime-theme')

                self.assertFalse(result)
                mock_find_resources.assert_called_once_with('Not Found.sublime-theme')


class TestFindSidebarBackground(TestCase):
    def setUp(self):
        self.theme_content = {
            'rules': [
                {
                    'class': 'icon_file_type',
                    'parents': [
                        {
                            'class': 'tree_row',
                            'attributes': ['hover', 'selected'],
                            'layer0.opacity': 0.8,
                        }
                    ],
                },
                {'class': 'sidebar_container', 'layer0.tint': 'var(white2)'},
            ],
            'variables': {'white2': '#F0F0F7'},
        }
        self.theme_content_no_rules = [
            {
                'class': 'icon_file_type',
                'parents': [
                    {
                        'class': 'tree_row',
                        'attributes': ['hover', 'selected'],
                        'layer0.opacity': 0.8,
                    }
                ],
            },
            {'class': 'sidebar_container', 'layer0.tint': '#FFFFFF'},
        ]
        self.theme_content_derived_background = {
            'rules': [
                {'class': 'icon_file_type', 'content_margin': [9, 8]},
                {'class': 'sidebar_container', 'layer0.tint': 'var(bgcolor)'},
            ],
            'variables': {'bgcolor': 'var(--background)'},
        }
        self.theme_content_st_color_palette = {
            'rules': [
                {'class': 'icon_file_type', 'content_margin': [9, 8]},
                {'class': 'sidebar_container', 'layer0.tint': 'darkslategray'},
            ],
        }

        self.patcher1 = patch('sublime.load_resource')
        self.patcher2 = patch('sublime.decode_value')
        self.mock_load_resource = self.patcher1.start()
        self.mock_decode_value = self.patcher2.start()

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()

    def test_find_variables_st_default_theme(self):
        target_list = []
        search_themes.find_variables(
            'rgb(115, 125, 240)',
            self.theme_content,
            target_list,
            'Packages/Theme - Default/Default.sublime-theme',
        )
        self.assertEqual(target_list, ['light'])

    def test_find_variables_hex_color(self):
        target_list = []
        search_themes.find_variables(
            '#FFFFFF',
            self.theme_content,
            target_list,
            'Packages/Theme - Treble/Treble Light.sublime-theme',
        )
        self.assertEqual(target_list, ['light'])

    def test_find_variables_rgb_color(self):
        target_list = []
        search_themes.find_variables(
            'rgb(255, 255, 255)',
            self.theme_content,
            target_list,
            'Packages/Theme - Treble/Treble Light.sublime-theme',
        )
        self.assertEqual(target_list, ['light'])

    def test_find_variables_hsl_color(self):
        target_list = []
        search_themes.find_variables(
            'hsl(0, 0%, 100%)',
            self.theme_content,
            target_list,
            'Packages/Theme - Treble/Treble Light.sublime-theme',
        )
        self.assertEqual(target_list, ['light'])

    def test_find_variables_derived_background(self):
        target_list = []
        with patch('os.path.exists') as mock_exists:
            mock_exists.return_value = True
            with patch(
                'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_themes.read_pickle_data'
            ) as mock_read_pickle:
                mock_read_pickle.return_value = [{'background': '#000000'}]
                search_themes.find_variables(
                    'var(--background)',
                    self.theme_content_derived_background,
                    target_list,
                    'Packages/Theme - Treble/Treble Adaptive.sublime-theme',
                )
                self.assertEqual(target_list, ['dark'])

    def test_find_variables_st_color_palette(self):
        target_list = []
        search_themes.find_variables(
            '#2f4f4f',
            self.theme_content_st_color_palette,
            target_list,
            'Packages/Theme - Custom/Custom.sublime-theme',
        )
        self.assertEqual(target_list, ['dark'])

    def test_find_attributes_sidebar_background(self):
        target_list = []
        search_themes.find_attributes(
            'Packages/Theme - Treble/Treble Light.sublime-theme',
            self.theme_content,
            'sidebar_container',
            'layer0.tint',
            target_list,
        )
        self.assertEqual(target_list, ['light'])

    def test_find_attributes_sidebar_background_no_rules(self):
        target_list = []
        search_themes.find_attributes(
            'Packages/Theme - ayu/ayu-light.sublime-theme',
            self.theme_content_no_rules,
            'sidebar_container',
            'layer0.tint',
            target_list,
        )
        self.assertEqual(target_list, ['light'])

    def test_find_attributes_hidden_file_sidebar_background(self):
        hidden_theme_content = {
            'rules': [{'class': 'sidebar_container', 'layer0.tint': 'var(black)'}],
            'variables': {'black': '#000000'},
        }
        self.mock_load_resource.return_value = '{}'
        self.mock_decode_value.return_value = hidden_theme_content

        target_list = []
        with patch('sublime.find_resources') as mock_find_resources:
            mock_find_resources.return_value = ['Nested Base Theme.hidden-theme']
            search_themes.find_attributes_hidden_file(
                'Nested Dark Theme.hidden-theme',
                {'extends': 'Nested Base Theme.hidden-theme'},
                'sidebar_container',
                'layer0.tint',
                target_list,
            )
            self.assertEqual(target_list, ['dark'])

    def test_find_sidebar_background(self):
        self.mock_load_resource.return_value = '{}'
        self.mock_decode_value.return_value = self.theme_content

        result = search_themes.find_sidebar_background(
            'Packages/Theme - Treble/Treble Light.sublime-theme'
        )
        self.assertEqual(result, ['light'])


class TestThemeOpacity(TestCase):
    def setUp(self):
        self.theme_content_with_opacity = {
            'rules': [
                {
                    'class': 'icon_file_type',
                    'layer0.tint': None,
                    'layer0.opacity': 0.8,
                    'content_margin': [9, 8],
                },
                {
                    'class': 'icon_file_type',
                    'parents': [{'class': 'tree_row', 'attributes': ['hover']}],
                    'layer0.opacity': 1.0,
                },
                {
                    'class': 'icon_file_type',
                    'parents': [{'class': 'tree_row', 'attributes': ['selected']}],
                    'layer0.opacity': 1.0,
                },
                {'class': 'sidebar_container', 'layer0.tint': '#FFFFFF'},
            ],
            'variables': {'background': 'var(--background)'},
        }
        self.theme_content_without_opacity = {
            'rules': [
                {'class': 'icon_file_type', 'content_margin': [9, 8]},
                {'class': 'sidebar_container', 'layer0.tint': 'var(bgcolor)'},
            ],
            'variables': {'bgcolor': 'var(--background)'},
        }
        self.theme_content_with_opacity_no_rules = [
            {
                'class': 'icon_file_type',
                'parents': [
                    {
                        'class': 'tree_row',
                        'attributes': ['hover', 'selected'],
                        'layer0.opacity': 0.8,
                    }
                ],
            },
            {
                'class': 'icon_file_type',
                'parents': [{'class': 'tree_row', 'attributes': ['hover']}],
                'layer0.opacity': 1.0,
            },
            {
                'class': 'icon_file_type',
                'parents': [{'class': 'tree_row', 'attributes': ['selected']}],
                'layer0.opacity': 1.0,
            },
            {'class': 'sidebar_container', 'layer0.tint': '#FFFFFF'},
        ]
        self.theme_content_without_opacity_no_rules = {
            'rules': [
                {'class': 'icon_file_type', 'content_margin': [9, 8]},
                {'class': 'sidebar_container', 'layer0.tint': '#fcfcfc'},
            ],
        }

        self.patcher1 = patch('sublime.load_resource')
        self.patcher2 = patch('sublime.decode_value')
        self.mock_load_resource = self.patcher1.start()
        self.mock_decode_value = self.patcher2.start()

    def tearDown(self):
        self.patcher1.stop()
        self.patcher2.stop()

    def test_find_attributes_opacity(self):
        target_list = [True]
        search_themes.find_attributes(
            'Packages/Theme - Treble/Treble Adaptive.sublime-theme',
            self.theme_content_with_opacity,
            'icon_file_type',
            'tree_row',
            target_list,
            ['hover', 'selected'],
            'parents',
        )
        self.assertEqual(target_list, [True, True])

    def test_theme_with_opacity_return_false(self):
        self.mock_load_resource.return_value = self.theme_content_without_opacity
        self.mock_decode_value.side_effect = lambda x: x

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_themes.is_cached_theme_info'
        ) as mock_cached:
            mock_cached.return_value = False
            result = search_themes.theme_with_opacity('Default.sublime-theme')
            self.assertFalse(result)

    def test_theme_with_opacity_no_rules_return_false(self):
        self.mock_load_resource.return_value = (
            self.theme_content_without_opacity_no_rules
        )
        self.mock_decode_value.side_effect = lambda x: x

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_themes.is_cached_theme_info'
        ) as mock_cached:
            mock_cached.return_value = False
            result = search_themes.theme_with_opacity('ayu-light.sublime-theme')
            self.assertFalse(result)

    def test_theme_with_opacity_return_true(self):
        self.mock_load_resource.return_value = self.theme_content_with_opacity
        self.mock_decode_value.side_effect = lambda x: x

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_themes.is_cached_theme_info'
        ) as mock_cached:
            mock_cached.return_value = False
            result = search_themes.theme_with_opacity(
                'Packages/Theme - Treble/Treble Dark.sublime-theme'
            )
            self.assertTrue(result)

    def test_theme_with_opacity_no_rules_return_true(self):
        self.mock_load_resource.return_value = self.theme_content_with_opacity_no_rules
        self.mock_decode_value.side_effect = lambda x: x

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_themes.is_cached_theme_info'
        ) as mock_cached:
            mock_cached.return_value = False
            result = search_themes.theme_with_opacity(
                'Packages/Theme - Custom/Custom.sublime-theme'
            )
            self.assertTrue(result)


class TestGetSidebarBgColor(TestCase):
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_themes.sublime.find_resources'
    )
    @patch(
        'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_themes.find_sidebar_background'
    )
    def test_get_sidebar_bgcolor(
        self, mock_find_sidebar_background, mock_find_resources
    ):
        mock_theme_name = 'Treble Adaptive.sublime-theme'
        mock_resources = ['Packages/Zukan Icon Theme', 'Packages/Theme Treble']
        mock_bgcolor = ('dark',)
        mock_find_resources.return_value = mock_resources
        mock_find_sidebar_background.return_value = mock_bgcolor

        result = search_themes.get_sidebar_bgcolor(mock_theme_name)

        mock_find_resources.assert_called_with(mock_theme_name)
        mock_find_sidebar_background.assert_called_with('Packages/Theme Treble')
        self.assertEqual(result, 'dark')

    @patch('sublime.find_resources')
    def test_get_sidebar_bgcolor_user_theme(self, mock_find_resources):
        mock_find_resources.return_value = ['Packages/User/Treble Dark.sublime-theme']

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_themes.find_sidebar_background'
        ) as mock_find_bg:
            mock_find_bg.return_value = ['dark']

            result = search_themes.get_sidebar_bgcolor('Treble Dark.sublime-theme')

            self.assertEqual(result, 'dark')
            mock_find_resources.assert_called_once_with('Treble Dark.sublime-theme')
            mock_find_bg.assert_called_once_with(
                'Packages/User/Treble Dark.sublime-theme'
            )

    @patch('sublime.find_resources')
    def test_get_sidebar_bgcolor_first_install(self, mock_find_resources):
        # Setup
        mock_find_resources.return_value = [
            'Packages/Theme - Treble/Treble Dark.sublime-theme'
        ]

        with patch(
            'Zukan Icon Theme.src.zukan_icon_theme.helpers.search_themes.find_sidebar_background'
        ) as mock_find_bg:
            mock_find_bg.return_value = ['light']

            result = search_themes.get_sidebar_bgcolor('Treble Dark.sublime-theme')

            self.assertEqual(result, 'light')
            mock_find_resources.assert_called_once_with('Treble Dark.sublime-theme')
            mock_find_bg.assert_called_once_with(
                'Packages/Theme - Treble/Treble Dark.sublime-theme'
            )

    @patch('sublime.find_resources')
    def test_get_sidebar_bgcolor_no_theme_found(self, mock_find_resources):
        mock_find_resources.return_value = []

        with self.assertRaises(UnboundLocalError):
            search_themes.get_sidebar_bgcolor('Not Found.sublime-theme')

        mock_find_resources.assert_called_once_with('Not Found.sublime-theme')
