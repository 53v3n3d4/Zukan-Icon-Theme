import logging
import sublime
import threading

from ..lib.icons_preferences import ZukanPreference
from ..lib.icons_syntaxes import ZukanSyntax
from ..lib.icons_themes import ZukanTheme
from ..lib.move_folders import MoveFolder
from ..helpers.thread_progress import ThreadProgress

logger = logging.getLogger(__name__)


class InstallEvent:
    """
    Install actions like 'first install' and upgrade package. And also
    syntaxes installation that is using Thread.
    """

    def install_syntax(file_name: str, syntax_name: str):
        ts = threading.Thread(
            target=ZukanSyntax.build_icon_syntax, args=(file_name, syntax_name)
        )
        ts.start()
        ThreadProgress(ts, 'Building zukan syntaxes', 'Build done')

    def install_syntaxes():
        ts = threading.Thread(target=ZukanSyntax.build_icons_syntaxes)
        ts.start()
        ThreadProgress(ts, 'Building zukan syntaxes', 'Build done')

    def install_batch():
        # ZukanTheme.create_icons_themes()
        ZukanPreference.build_icons_preferences()
        ZukanSyntax.build_icons_syntaxes()

    def install_upgrade():
        ZukanPreference.build_icons_preferences()
        ZukanSyntax.build_icons_syntaxes()

    def install_upgrade_thread():
        ZUKAN_RESTART_MESSAGE = sublime.load_settings(
            'Zukan Icon Theme.sublime-settings'
        ).get('zukan_restart_message')

        if ZUKAN_RESTART_MESSAGE is True:
            dialog_message = (
                'Zukan icons has been upgraded.\n\n'
                'You may have to restart ST if all icons do not load correct in current theme.'
            )
        if ZUKAN_RESTART_MESSAGE is False:
            dialog_message = None

        t = threading.Thread(target=InstallEvent.install_upgrade)
        t.start()
        ThreadProgress(t, 'Upgrading zukan files', 'Upgrade done', dialog_message)

    def new_install_manually():
        # Creating themes in main thread helps a little with the error not showing all
        # building file icons when ST start.
        # 'refresh_folder_list' do not help force reload. But deleting or duplicating a
        # folder with at least 5 files, it will realod file icons.
        # If change themes, the icons is working with no problem.

        # ZukanTheme.create_icons_themes()
        # InstallEvent.install_syntaxes()

        # threading.Thread(target=ZukanTheme.create_icons_themes).start()
        # threading.Thread(target=ZukanPreference.build_icons_preferences).start()

        try:
            ZUKAN_RESTART_MESSAGE = sublime.load_settings(
                'Zukan Icon Theme.sublime-settings'
            ).get('zukan_restart_message')

            if ZUKAN_RESTART_MESSAGE is True:
                dialog_message = (
                    'Zukan icons has been built.\n\n'
                    'You may have to restart ST if all icons do not load correct in current theme.'
                )
            if ZUKAN_RESTART_MESSAGE is False:
                dialog_message = None

            t = threading.Thread(target=InstallEvent.install_batch)
            t.start()
            ThreadProgress(t, 'Building zukan files', 'Build done', dialog_message)
        finally:
            # Testing if order helps prompt show icons. Building themes last.
            ZukanTheme.create_icons_themes()

    def new_install_pkg_control():
        """
        Try move folders if installed trough Package Control. Then install
        sublime-theme and sublime-syntax files.
        """
        try:
            MoveFolder.move_folders()
        finally:
            InstallEvent.new_install_manually()
