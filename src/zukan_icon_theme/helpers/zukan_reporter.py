import cProfile
import io
import logging
import os
import pstats
import sublime
import sublime_plugin
import sys

from datetime import datetime
from ..core.listeners import SchemeTheme
from ..core.zukan_pref_settings import SettingsEvent
from ..lib.icons_preferences import ZukanPreference
from ..lib.icons_syntaxes import ZukanSyntax
from ..utils.zukan_paths import ZUKAN_PKG_SUBLIME_PATH
from ..utils.zukan_reports_options import ZUKAN_REPORTS_OPTIONS

logger = logging.getLogger(__name__)

# ZUKAN_REPORTS_OPTIONS = [
#     { 'get_user_theme': (lambda: SchemeTheme().get_user_theme()) },
#     { 'build_preferences': (lambda: ZukanPreference().build_icons_preferences()) },
#     { 'build_syntaxes': (lambda: ZukanSyntax().build_icons_syntaxes()) },
# ]


class Reporter:
    def __init__(self, view):
        self.view = view
        self.profile_file_path = os.path.join(
            ZUKAN_PKG_SUBLIME_PATH, 'zukan_reports.txt'
        )

    def _profile_results(self, fname: str, title: str):
        """
        https://docs.python.org/3/library/profile.html#profile.Profile
        """
        pr = cProfile.Profile()
        pr.enable()
        fname()
        pr.disable()

        stream = io.StringIO()

        # Store the default stdout
        og_stdout = sys.stdout
        sys.stdout = stream

        ps = pstats.Stats(pr, stream=stream).strip_dirs().sort_stats('cumulative')
        ps.print_stats(10)

        # Return to normal stdout
        sys.stdout = og_stdout

        result = stream.getvalue()

        self._add_title_time(title, result)
        self._open_report_file()

    def _zukan_preferences_settings(self, title: str):
        result = SettingsEvent.get_user_zukan_preferences()

        self._add_title_time(title, result)
        self._open_report_file()

    def _add_title_time(self, title: str, result):
        get_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Save results to file
        start_line = '\t{t} =====================\n\n'.format(t=title)
        time_line = '\t{g}\n\n'.format(g=get_time)
        # end_line = '\t=======================================\n\n'

        data = start_line + time_line + result
        self.save_file(data)

    def _open_report_file(self):
        # Open file in a new tab
        self.view.window().open_file(self.profile_file_path)

    def save_file(self, output: str):
        if not os.path.exists(self.profile_file_path):
            with open(self.profile_file_path, 'w') as f:
                f.write(output)
        else:
            with open(self.profile_file_path, 'r') as f:
                data = f.read()

            with open(self.profile_file_path, 'w') as f:
                f.write(output + '\n\n' + data)

    def _delete_report_file(self):
        if os.path.exists(self.profile_file_path):
            os.remove(self.profile_file_path)
            logger.info('deleting %s', os.path.basename(self.profile_file_path))

            return self.profile_file_path

    def report_to_file(self, option: str):
        # for d in self.list_profile_options.items():
        #     if d[0] == option:
        #         self._profile_results(d[1])

        if option == 'Clear reports file':
            self._delete_report_file()

        elif option == 'Zukan preferences settings':
            self._zukan_preferences_settings(option)

        else:
            fname = option.split()[-1]

            if fname == 'get_user_theme':
                self._profile_results(lambda: SchemeTheme().get_user_theme(), option)

            elif fname == 'build_preferences':
                self._profile_results(
                    lambda: ZukanPreference().build_icons_preferences(), option
                )

            elif fname == 'build_syntaxes':
                self._profile_results(
                    lambda: ZukanSyntax().build_icons_syntaxes(), option
                )


class ZukanReporterCommand(sublime_plugin.TextCommand):
    """
    Sublime command to open a file with profile results.
    """

    def run(self, edit, report_option: str):
        reporter = Reporter(self.view)
        reporter.report_to_file(report_option)

    def input(self, args: dict):
        return ZukanReporterrOptionsInputHandler()


class ZukanReporterrOptionsInputHandler(sublime_plugin.ListInputHandler):
    """
    Return report_option to ProfileZukan.
    """

    def name(self) -> str:
        return 'report_option'

    def placeholder(self) -> str:
        sublime.status_message(
            'File will be saved in Packages/Zukan Icon Theme/sublime/zukan_reports.txt'
        )
        return 'Select option'

    def list_items(self) -> list:
        profile_opts = ZUKAN_REPORTS_OPTIONS
        return profile_opts
