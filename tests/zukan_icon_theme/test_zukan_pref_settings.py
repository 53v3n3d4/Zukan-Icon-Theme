import importlib

from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

zukan_pref_settings = importlib.import_module(
    'Zukan Icon Theme.src.zukan_icon_theme.core.zukan_pref_settings'
)


class TestEventBus(TestCase):
    def setUp(self):
        self.event_bus = zukan_pref_settings.EventBus()

    def test_event_bus_subscribe(self):
        mock_listener = Mock()
        self.event_bus.subscribe('upgrade_started', mock_listener)
        self.assertIn('upgrade_started', self.event_bus.listeners)
        self.assertIn(mock_listener, self.event_bus.listeners['upgrade_started'])

    def test_event_bus_subscribe_multiple(self):
        mock_listener1 = Mock()
        mock_listener2 = Mock()
        self.event_bus.subscribe('upgrade_started', mock_listener1)
        self.event_bus.subscribe('upgrade_started', mock_listener2)
        self.assertEqual(len(self.event_bus.listeners['upgrade_started']), 2)

    def test_event_bus_publish(self):
        mock_listener1 = Mock()
        mock_listener2 = Mock()
        self.event_bus.subscribe('upgrade_started', mock_listener1)
        self.event_bus.subscribe('upgrade_started', mock_listener2)

        self.event_bus.publish('upgrade_started')

        mock_listener1.assert_called_once()
        mock_listener2.assert_called_once()

    def test_event_bus_publish_not_exist(self):
        self.event_bus.publish('event_not_exists')


class TestZukanIconFiles(TestCase):
    def setUp(self):
        self.event_bus = Mock()
        self.clean_comments = Mock()
        self.install_event = Mock()
        self.zukan_preference = Mock()
        self.zukan_syntax = Mock()

        self.mock_settings = {
            'ignored_icon': ['Ignored-1', 'Ignored-2'],
            'change_icon': {'Atest': 'atest'},
            'change_icon_file_extension': ['txt', 'md'],
            'create_custom_icon': ['ATest-1', 'ATest-2'],
            'prefer_icon': {'Treble Dark.sublime-theme': 'light'},
        }

        patch_config = [
            ('os.path.exists', {'return_value': True}),
            ('builtins.open', {'return_value': MagicMock()}),
            ('os.makedirs', {'return_value': MagicMock()}),
            (
                zukan_pref_settings,
                'read_pickle_data',
                {'return_value': [self.mock_settings]},
            ),
            (
                zukan_pref_settings,
                'get_settings',
                {'return_value': True},
            ),
            (
                zukan_pref_settings,
                'get_prefer_icon_settings',
                {'return_value': (True, {'Treble Dark.sublime-theme': 'light'})},
            ),
            (
                zukan_pref_settings,
                'get_change_icon_settings',
                {'return_value': ({'ATest': 'atest'}, ['txt', 'md'])},
            ),
            (
                zukan_pref_settings,
                'get_ignored_icon_settings',
                {'return_value': ['Ignored-1', 'Ignored-2']},
            ),
            (
                zukan_pref_settings,
                'get_create_custom_icon_settings',
                {'return_value': ['ATest-1', 'ATest-2']},
            ),
            (
                zukan_pref_settings,
                'read_current_settings',
                {'return_value': self.mock_settings},
            ),
            (
                zukan_pref_settings,
                'save_current_settings',
                {'return_value': MagicMock()},
            ),
        ]

        self.patches = []

        for item in patch_config:
            if isinstance(item[0], str):
                target, kwargs = item
                patcher = patch(target, **kwargs)
            else:
                module, attr, kwargs = item
                patcher = patch.object(module, attr, **kwargs)

            self.patches.append(patcher)

        self.mocks = [p.start() for p in self.patches]

        self.zukan = zukan_pref_settings.ZukanIconFiles(
            event_bus=self.event_bus,
            clean_comments=self.clean_comments,
            install_event=self.install_event,
            zukan_preference=self.zukan_preference,
            zukan_syntax=self.zukan_syntax,
        )

    def tearDown(self):
        for patcher in self.patches:
            patcher.stop()

    def test_zukan_icon_files_init(self):
        self.event_bus.subscribe.assert_any_call(
            'upgrade_started', self.zukan.on_upgrade_started
        )
        self.event_bus.subscribe.assert_any_call(
            'upgrade_finished', self.zukan.on_upgrade_finished
        )

        self.assertFalse(self.zukan.is_upgrading)
        self.assertEqual(
            self.zukan.rebuild_functions,
            {
                'rebuild_icon_files_thread': False,
                'build_icons_preferences': False,
                'install_syntaxes': False,
            },
        )

    def test_on_upgraded_started_finished(self):
        self.zukan.on_upgrade_started()
        self.assertTrue(self.zukan.is_upgrading)

        self.zukan.on_upgrade_finished()
        self.assertFalse(self.zukan.is_upgrading)

    def test_rebuild_icons_files(self):
        self.zukan.rebuild_icons_files(self.event_bus)

        self.assertFalse(self.zukan.rebuild_functions['rebuild_icon_files_thread'])
        self.assertFalse(self.zukan.rebuild_functions['build_icons_preferences'])
        self.assertFalse(self.zukan.rebuild_functions['install_syntaxes'])

    def test_rebuild_icons_files_with_changes(self):
        self.zukan.ignored_icon = ['Ignored-1', 'Ignored-3']
        self.zukan.prefer_icon = {'Treble Light.sublime-theme': 'dark'}
        self.zukan.change_icon_file_extension = ['txt', 'py']

        with patch.object(zukan_pref_settings, 'save_current_settings'):
            self.zukan.rebuild_icons_files(self.event_bus)

        self.assertTrue(any(self.zukan.rebuild_functions.values()))

    def test_execute_rebuilds(self):
        self.zukan.rebuild_functions['build_icons_preferences'] = True
        self.zukan.rebuild_functions['install_syntaxes'] = True

        self.zukan.zukan_preference.build_icons_preferences = Mock()
        self.zukan.clean_comments.clean_comments = Mock()
        self.zukan.zukan_syntax.install_syntaxes = Mock()

        self.zukan.execute_rebuilds()

        self.zukan.zukan_preference.build_icons_preferences.assert_called_once()
        self.zukan.clean_comments.clean_comments.assert_called_once()
        self.zukan.zukan_syntax.install_syntaxes.assert_called_once()

        self.assertFalse(self.zukan.rebuild_functions['build_icons_preferences'])
        self.assertFalse(self.zukan.rebuild_functions['install_syntaxes'])

    def test_execute_rebuilds_icon_files_thread(self):
        self.zukan.rebuild_functions['rebuild_icon_files_thread'] = True

        self.zukan.execute_rebuilds()

        self.install_event.rebuild_icon_files_thread.assert_called_once()
        self.clean_comments.clean_comments.assert_called_once()

        self.assertFalse(self.zukan.rebuild_functions['rebuild_icon_files_thread'])


class TestSettingsEvent(TestCase):
    def settings_side_effect(self, _, option=None):
        if option is None:
            return self.zukan_settings_mock

        settings_values = {
            'option1': 'value1',
            'option2': 'value2',
            'user_opt1': 'user_val1',
            'user_opt2': 'user_val2',
            'log_level': 'DEBUG',
        }
        return settings_values.get(option, 'default')

    def setUp(self):
        self.event_bus_mock = MagicMock()
        self.zukan_settings_mock = MagicMock()

        self.patches = [
            patch.object(
                zukan_pref_settings,
                'get_settings',
                side_effect=self.settings_side_effect,
            ),
            patch.object(
                zukan_pref_settings,
                'get_folder_size',
                return_value=1024,
            ),
            patch.object(
                zukan_pref_settings,
                'get_file_size',
                return_value=2048,
            ),
            patch.object(
                zukan_pref_settings,
                'bytes_to_readable_size',
                side_effect=lambda x: f'{x}B',
            ),
            patch.object(
                zukan_pref_settings,
                'ZUKAN_SETTINGS_OPTIONS',
                ['option1', 'option2'],
            ),
            patch.object(
                zukan_pref_settings,
                'USER_SETTINGS_OPTIONS',
                ['user_opt1', 'user_opt2'],
            ),
            patch.object(
                zukan_pref_settings,
                'EventBus',
                return_value=self.event_bus_mock,
            ),
            patch.object(zukan_pref_settings, 'UpgradePlugin'),
            patch.object(zukan_pref_settings, 'ZukanIconFiles'),
            patch.object(
                zukan_pref_settings,
                'ZUKAN_SETTINGS',
                'Zukan Icon Theme',
            ),
            patch.object(
                zukan_pref_settings,
                'USER_SETTINGS',
                'USER_SETTINGS',
            ),
        ]

        for p in self.patches:
            p.start()

        self.zukan_settings_mock.add_on_change = MagicMock()
        self.zukan_settings_mock.clear_on_change = MagicMock()

    def tearDown(self):
        for p in self.patches:
            p.stop()

    def test_get_user_zukan_preferences(self):
        result = zukan_pref_settings.SettingsEvent.get_user_zukan_preferences()

        expected_elements = [
            '==== Zukan Icon Theme settings ====',
            'Zukan folder size: 1024B',
            'sublime-package size: 2048B',
            'option1: value1',
            'option2: value2',
            '==== User ST settings ==============',
            'user_opt1: user_val1',
            'user_opt2: user_val2',
            '------------------------------------',
        ]

        for element in expected_elements:
            self.assertIn(element, result)

    @patch('builtins.print')
    def test_output_to_console_zukan_pref_settings(self, mock_print):
        zukan_pref_settings.SettingsEvent.output_to_console_zukan_pref_settings()
        mock_print.assert_called_once()

    @patch('builtins.print')
    def test_output_to_console_zukan_pref_settings_not_debug(self, mock_print):
        with patch.object(
            zukan_pref_settings,
            'get_settings',
            return_value='INFO',
        ):
            zukan_pref_settings.SettingsEvent.output_to_console_zukan_pref_settings()
            mock_print.assert_not_called()

    def test_zukan_options_settings(self):
        upgrade_plugin_mock = MagicMock()
        zukan_files_mock = MagicMock()

        # fmt: off
        with patch.object(
                zukan_pref_settings,
                'UpgradePlugin',
                return_value=upgrade_plugin_mock,
             ) as upgrade_mock, \
             patch.object(
                zukan_pref_settings,
                'ZukanIconFiles',
                return_value=zukan_files_mock,
             ) as files_mock:
             # fmt: on

            zukan_pref_settings.SettingsEvent.zukan_options_settings()

            self.assertTrue(self.event_bus_mock)

            upgrade_mock.assert_called_once_with(self.event_bus_mock)
            upgrade_plugin_mock.start_upgrade.assert_called_once()

            files_mock.assert_called_once_with(self.event_bus_mock)
            zukan_files_mock.rebuild_icons_files.assert_called_once_with(
                self.event_bus_mock
            )

    def test_zukan_preferences_clear(self):
        zukan_pref_settings.SettingsEvent.zukan_preferences_clear()
        self.zukan_settings_mock.clear_on_change.assert_called_once_with(
            'Zukan Icon Theme'
        )

    def test_zukan_preferences_changed(self):
        zukan_pref_settings.SettingsEvent.zukan_preferences_changed()
        self.zukan_settings_mock.add_on_change.assert_called_once_with(
            'Zukan Icon Theme', zukan_pref_settings.SettingsEvent.zukan_options_settings
        )


class TestUpgradePlugin(TestCase):
    @patch.object(zukan_pref_settings, 'get_upgraded_version_settings')
    @patch.object(zukan_pref_settings, 'get_settings')
    def setUp(self, mock_get_settings, mock_get_upgraded_settings):
        self.event_bus = zukan_pref_settings.EventBus()
        self.install_event = Mock(spec=zukan_pref_settings.InstallEvent)

        mock_get_upgraded_settings.return_value = ('0.4.8', True)
        mock_get_settings.return_value = '0.4.7'

        self.upgrade_plugin = zukan_pref_settings.UpgradePlugin(
            event_bus=self.event_bus, install_event=self.install_event
        )

    @patch.object(zukan_pref_settings, 'get_upgraded_version_settings')
    @patch.object(zukan_pref_settings, 'get_settings')
    def test_upgrade_plugin_init(self, mock_get_settings, mock_get_upgraded_settings):
        mock_get_upgraded_settings.return_value = ('0.4.8', True)
        mock_get_settings.return_value = '0.4.8'

        plugin = zukan_pref_settings.UpgradePlugin(self.event_bus)

        self.assertFalse(plugin.is_upgrading)
        self.assertEqual(plugin.pkg_version, '0.4.8')
        self.assertTrue(plugin.auto_upgraded)

    def test_start_upgrade(self):
        upgrade_started = Mock()
        upgrade_finished = Mock()
        self.event_bus.subscribe('upgrade_started', upgrade_started)
        self.event_bus.subscribe('upgrade_finished', upgrade_finished)

        with patch.object(self.upgrade_plugin, 'upgrade_zukan_files') as mock_upgrade:
            self.upgrade_plugin.start_upgrade()

            self.assertFalse(self.upgrade_plugin.is_upgrading)
            mock_upgrade.assert_called_once()
            upgrade_started.assert_called_once()
            upgrade_finished.assert_called_once()

    def exists_side_effect(self, path):
        if path == zukan_pref_settings.ZUKAN_CURRENT_SETTINGS_FILE:
            return True
        if path == zukan_pref_settings.ZUKAN_PKG_SUBLIME_PATH:
            return True
        return False

    @patch('os.path.exists')
    @patch.object(zukan_pref_settings, 'read_pickle_data')
    @patch.object(zukan_pref_settings, 'save_current_settings')
    @patch('os.makedirs')
    def test_upgrade_zukan_files(
        self, mock_makedirs, mock_save_settings, mock_read_pickle, mock_exists
    ):
        mock_exists.side_effect = self.exists_side_effect
        mock_read_pickle.return_value = [{'version': '0.4.7'}]

        self.upgrade_plugin.upgrade_zukan_files()

        self.install_event.install_upgrade_thread.assert_called_once()
        mock_save_settings.assert_called_once()

        mock_makedirs.assert_not_called()

    @patch('os.path.exists')
    @patch.object(zukan_pref_settings, 'read_pickle_data')
    @patch.object(zukan_pref_settings, 'save_current_settings')
    def test_upgrade_zukan_files_same_version(
        self, mock_save_settings, mock_read_pickle, mock_exists
    ):
        mock_exists.return_value = True
        mock_read_pickle.return_value = [{'version': '0.4.8'}]
        self.upgrade_plugin.pkg_version = '0.4.8'
        self.upgrade_plugin.auto_upgraded = True

        self.upgrade_plugin.upgrade_zukan_files()

        self.install_event.install_upgrade_thread.assert_not_called()

    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch.object(zukan_pref_settings, 'save_current_settings')
    def test_upgrade_zukan_files_no_zukan_current_settings_file(
        self, mock_save_settings, mock_makedirs, mock_exists
    ):
        mock_exists.side_effect = lambda x: False

        self.upgrade_plugin.upgrade_zukan_files()

        mock_makedirs.assert_called_once_with(
            zukan_pref_settings.ZUKAN_PKG_SUBLIME_PATH
        )
        mock_save_settings.assert_called_once()

    @patch('os.path.exists')
    @patch('os.remove')
    def test_upgrade_zukan_files_deprecated_version(self, mock_remove, mock_exists):
        mock_exists.return_value = True
        self.upgrade_plugin.version_json_file = '0.3.0'
        self.upgrade_plugin.pkg_version = '0.3.1'
        self.upgrade_plugin.auto_upgraded = True

        self.upgrade_plugin.upgrade_zukan_files()

        mock_remove.assert_called_once_with(zukan_pref_settings.ZUKAN_VERSION_FILE)
        self.install_event.install_upgrade_thread.assert_called_once()
