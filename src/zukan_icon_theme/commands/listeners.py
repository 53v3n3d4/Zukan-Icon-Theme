import sublime
import sublime_plugin


class ThemeSettingListener(sublime_plugin.EventListener):
    def on_window_command(self, window, command, args):
        # if command == 'edit_settings':
        if command == 'select_theme' or 'edit_settings':
            theme_name = sublime.load_settings('Preferences.sublime-settings').get(
                'theme'
            )
            print('window command')

    def on_post_window_command(self, window, command, args):
        # if command == 'edit_settings':
        if command == 'select_theme' or 'edit_settings':
            theme_name = sublime.load_settings('Preferences.sublime-settings').get(
                'theme'
            )
            print(theme_name)
