import logging
import threading

from ..lib.icons_preferences import ZukanPreference
from ..lib.icons_syntaxes import ZukanSyntax
from ..lib.icons_themes import ZukanTheme
from ..lib.move_folders import MoveFolder
from ..helpers.load_save_settings import get_settings
from ..helpers.thread_progress import ThreadProgress
from ..utils.file_settings import (
    ZUKAN_SETTINGS,
)

logger = logging.getLogger(__name__)


class InstallEvent:
    """
    Install actions like 'first install' and upgrade package. And also
    syntaxes installation that is using Thread.
    """

    def install_syntax(file_name: str, syntax_name: str):
        """
        Using Thread to install syntax to avoid freezing ST to build syntax.

        Parameters:
        file_name (str) -- syntax file name, without extension.
        syntax_name (str) -- syntax name, file name and extension.
        """
        ts = threading.Thread(
            target=ZukanSyntax.build_icon_syntax, args=(file_name, syntax_name)
        )
        ts.start()
        ThreadProgress(ts, 'Building zukan syntaxes', 'Build done')

    def install_syntaxes():
        """
        Using Thread to install syntax to avoid freezing ST to build syntaxes.
        """
        # Deleting syntax for 'change_icon_file_extension'
        ZukanSyntax.delete_icons_syntaxes()

        ts = threading.Thread(target=ZukanSyntax.build_icons_syntaxes)
        ts.start()
        ThreadProgress(ts, 'Building zukan syntaxes', 'Build done')

    def install_batch():
        """
        Batch build themes, preferences and syntaxes, to use with Thread together
        in new install manually.
        """
        # Check 'auto_install_theme' avoid duplicate create themes when True.
        # Because deleting theme already triggers event to create themes.
        auto_install_theme = get_settings(ZUKAN_SETTINGS, 'auto_install_theme')
        if auto_install_theme is False:
            ZukanTheme.create_icons_themes()

        ZukanPreference.build_icons_preferences()
        ZukanSyntax.build_icons_syntaxes()

        version = get_settings(ZUKAN_SETTINGS, 'version')
        logger.info('Zukan icons v%s has been built.', version)

    def install_syntaxes_preferences():
        """
        Batch build preferences and syntaxes, to use with Thread together in
        install_upgrade_thread and rebuild_icon_files_thread.
        """
        # Deleting syntax for 'change_icon_file_extension'
        ZukanSyntax.delete_icons_syntaxes()

        ZukanPreference.build_icons_preferences()
        ZukanSyntax.build_icons_syntaxes()

    def install_upgrade_thread():
        """
        Using Thread to build upgraded files, to avoid ST freezing.
        """
        version = get_settings(ZUKAN_SETTINGS, 'version')
        zukan_restart_message = get_settings(ZUKAN_SETTINGS, 'zukan_restart_message')

        if zukan_restart_message is True:
            dialog_message = (
                'Zukan icons has been upgraded to v{v}.\n\n'
                'Changelog in Sublime Text > Settings > Package Settings menu.\n\n'
                'You may have to restart ST, if all icons do not load correct in '
                'current theme.'.format(v=version)
            )
        if zukan_restart_message is False:
            dialog_message = (
                'Zukan icons has been upgraded to v{v}.\n\n'
                'Changelog in Sublime Text > Settings > Package Settings menu.'
                '\n\n'.format(v=version)
            )

        t = threading.Thread(target=InstallEvent.install_syntaxes_preferences)
        t.start()
        ThreadProgress(t, 'Upgrading zukan files', 'Upgrade done', dialog_message)

        logger.info('upgrading Zukan icons to v%s.', version)
        logger.info('Changelog in Sublime Text > Settings > Package Settings menu.')

    def rebuild_icon_files_thread():
        """
        Using Thread to build syntax and preferences files, to avoid ST freezing.
        """

        t = threading.Thread(target=InstallEvent.install_syntaxes_preferences)
        t.start()
        ThreadProgress(t, 'Building zukan files', 'Build done')

    def new_install_manually():
        """
        Using Thread to build new installation files via clone repo, to avoid ST freezing.

        Install icons themes, preferences and syntaxes.
        """
        # Creating themes in main thread helps a little with the error not showing all
        # building file icons when ST start.
        # 'refresh_folder_list' do not help force reload. But deleting or duplicating a
        # folder with at least 5 files, it will realod file icons.
        # If change themes, the icons is working with no problem.
        version = get_settings(ZUKAN_SETTINGS, 'version')
        zukan_restart_message = get_settings(ZUKAN_SETTINGS, 'zukan_restart_message')

        if zukan_restart_message is True:
            dialog_message = (
                'Zukan icons v{v} has been built.\n\n'
                'You may have to restart ST, if all icons do not load correct in '
                'current theme.'.format(v=version)
            )
        if zukan_restart_message is False:
            dialog_message = None

        t = threading.Thread(target=InstallEvent.install_batch)
        t.start()
        ThreadProgress(t, 'Building zukan files', 'Build done', dialog_message)

    def new_install_pkg_control():
        """
        Using Thread to build new installation files via sublime-package file,
        to avoid ST freezing.

        Try move folders if installed trough Package Control. Folders contain icons
        PNGs, preferences and syntaxes data files.

        Then install icons themes, preferences and syntaxes.
        """
        try:
            MoveFolder.move_folders()
        finally:
            InstallEvent.new_install_manually()
