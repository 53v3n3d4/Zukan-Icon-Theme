import logging
import threading

from ..lib.icons_preferences import ZukanPreference, ZukanPreferenceP2
from ..lib.icons_syntaxes import ZukanSyntax, ZukanSyntaxS2
from ..lib.icons_themes import ZukanTheme, ZukanThemeT2
from ..lib.move_folders import MoveFolder, MoveFolderF2
from ..helpers.delete_unused import delete_unused_icons
from ..helpers.load_save_settings import (
    get_theme_settings,
    get_upgraded_version_settings,
    is_zukan_restart_message,
)
from ..helpers.thread_progress import ThreadProgress
from ..utils.zukan_paths import (
    ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH,
    ZUKAN_PKG_ICONS_PATH,
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
        ignored_theme, auto_install_theme = get_theme_settings()
        pkg_version, _ = get_upgraded_version_settings()

        if auto_install_theme is False:
            ZukanTheme.create_icons_themes()

        ZukanSyntax.build_icons_syntaxes()
        ZukanPreference.build_icons_preferences()

        logger.info('Zukan icons v%s has been built.', pkg_version)

    def install_syntaxes_preferences():
        """
        Batch build preferences and syntaxes, to use with Thread together in
        install_upgrade_thread and rebuild_icon_files_thread.
        """
        # Change build order: syntax then preferences. Notice error Bad XML,
        # when ignoring icon through Command, duplicating create preferences
        # after change from 'add_on_change' to  ViewListener.
        ZukanSyntax.build_icons_syntaxes()
        ZukanPreference.build_icons_preferences()

    def install_upgrade_thread():
        """
        Using Thread to build upgraded files, to avoid ST freezing.
        """
        try:
            # Copy new icons_data and icons folder
            MoveFolder.move_folders()

        finally:
            pkg_version, _ = get_upgraded_version_settings()
            zukan_restart_message = is_zukan_restart_message()

            if zukan_restart_message is True:
                dialog_message = (
                    'Zukan icons has been upgraded to v{v}.\n\n'
                    'Changelog in Sublime Text > Settings > Package Settings menu.\n\n'
                    'You may have to restart ST, if all icons do not load correct in '
                    'current theme.'.format(v=pkg_version)
                )
            if zukan_restart_message is False:
                dialog_message = (
                    'Zukan icons has been upgraded to v{v}.\n\n'
                    'Changelog in Sublime Text > Settings > Package Settings menu.'
                    '\n\n'.format(v=pkg_version)
                )

            # Delete unused icons
            delete_unused_icons(ZUKAN_PKG_ICONS_PATH)
            delete_unused_icons(ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH)

            t = threading.Thread(target=InstallEvent.install_syntaxes_preferences)
            t.start()
            ThreadProgress(t, 'Upgrading zukan files', 'Upgrade done', dialog_message)

            logger.info('upgrading Zukan icons to v%s.', pkg_version)
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
        # icons during install.
        # 'refresh_folder_list' do not help force reload. But deleting or duplicating a
        # folder with at least 5 files, it will realod file icons.
        # If change themes, the icons is working with no problem.
        pkg_version, _ = get_upgraded_version_settings()
        zukan_restart_message = is_zukan_restart_message()

        if zukan_restart_message is True:
            dialog_message = (
                'Zukan icons v{v} has been built.\n\n'
                'You may have to restart ST, if all icons do not load correct in '
                'current theme.'.format(v=pkg_version)
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
        PNGs and zukan icons data files.

        Then install icons themes, preferences and syntaxes.
        """
        try:
            MoveFolder.move_folders()
        finally:
            InstallEvent.new_install_manually()


class InstallEventE2(MoveFolderF2, ZukanPreferenceP2, ZukanSyntaxS2, ZukanThemeT2):
    """
    Install actions like 'first install' and upgrade package. And also
    syntaxes installation that is using Thread.
    """

    def __init__(self):
        MoveFolderF2.__init__(self)
        ZukanPreferenceP2.__init__(self)
        ZukanSyntaxS2.__init__(self)
        ZukanThemeT2.__init__(self)

        self.pkg_version, self.auto_upgraded = get_upgraded_version_settings()
        self.zukan_restart_message = is_zukan_restart_message()

    def install_syntax(self, file_name: str, syntax_name: str):
        """
        Using Thread to install syntax to avoid freezing ST to build syntax.

        Parameters:
        file_name (str) -- syntax file name, without extension.
        syntax_name (str) -- syntax name, file name and extension.
        """
        ts = threading.Thread(
            target=self.build_icon_syntax, args=(file_name, syntax_name)
        )
        ts.start()
        ThreadProgress(ts, 'Building zukan syntaxes', 'Build done')

    def install_syntaxes(self):
        """
        Using Thread to install syntax to avoid freezing ST to build syntaxes.
        """
        ts = threading.Thread(target=self.build_icons_syntaxes)
        ts.start()
        ThreadProgress(ts, 'Building zukan syntaxes', 'Build done')

    def install_batch(self):
        """
        Batch build themes, preferences and syntaxes, to use with Thread together
        in new install manually.
        """
        # Check 'auto_install_theme' avoid duplicate create themes when True.
        # Because deleting theme already triggers event to create themes.

        # ignored_theme, auto_install_theme = get_theme_settings()
        # pkg_version, _ = get_upgraded_version_settings()

        if self.auto_install_theme is False:
            self.create_icons_themes()

        self.build_icons_syntaxes()
        self.build_icons_preferences()

        logger.info('Zukan icons v%s has been built.', self.pkg_version)

    def install_syntaxes_preferences(self):
        """
        Batch build preferences and syntaxes, to use with Thread together in
        install_upgrade_thread and rebuild_icon_files_thread.
        """
        # Change build order: syntax then preferences. Notice error Bad XML,
        # when ignoring icon through Command, duplicating create preferences
        # after change from 'add_on_change' to  ViewListener.
        self.build_icons_syntaxes()
        self.build_icons_preferences()

    def install_upgrade_thread(self):
        """
        Using Thread to build upgraded files, to avoid ST freezing.
        """
        try:
            # Copy new icons_data and icons folder
            self.move_folders()

        finally:
            # pkg_version, _ = get_upgraded_version_settings()
            # zukan_restart_message = is_zukan_restart_message()

            if self.zukan_restart_message is True:
                dialog_message = (
                    'Zukan icons has been upgraded to v{v}.\n\n'
                    'Changelog in Sublime Text > Settings > Package Settings menu.\n\n'
                    'You may have to restart ST, if all icons do not load correct in '
                    'current theme.'.format(v=self.pkg_version)
                )
            if self.zukan_restart_message is False:
                dialog_message = (
                    'Zukan icons has been upgraded to v{v}.\n\n'
                    'Changelog in Sublime Text > Settings > Package Settings menu.'
                    '\n\n'.format(v=self.pkg_version)
                )

            # Delete unused icons
            delete_unused_icons(ZUKAN_PKG_ICONS_PATH)
            delete_unused_icons(ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH)

            t = threading.Thread(target=self.install_syntaxes_preferences)
            t.start()
            ThreadProgress(t, 'Upgrading zukan files', 'Upgrade done', dialog_message)

            logger.info('upgrading Zukan icons to v%s.', self.pkg_version)
            logger.info('Changelog in Sublime Text > Settings > Package Settings menu.')

    def rebuild_icon_files_thread(self):
        """
        Using Thread to build syntax and preferences files, to avoid ST freezing.
        """

        t = threading.Thread(target=self.install_syntaxes_preferences)
        t.start()
        ThreadProgress(t, 'Building zukan files', 'Build done')

    def new_install_manually(self):
        """
        Using Thread to build new installation files via clone repo, to avoid ST freezing.

        Install icons themes, preferences and syntaxes.
        """
        # Creating themes in main thread helps a little with the error not showing all
        # icons during install.
        # 'refresh_folder_list' do not help force reload. But deleting or duplicating a
        # folder with at least 5 files, it will realod file icons.
        # If change themes, the icons is working with no problem.

        # pkg_version, _ = get_upgraded_version_settings()
        # zukan_restart_message = is_zukan_restart_message()

        if self.zukan_restart_message is True:
            dialog_message = (
                'Zukan icons v{v} has been built.\n\n'
                'You may have to restart ST, if all icons do not load correct in '
                'current theme.'.format(v=self.pkg_version)
            )
        if self.zukan_restart_message is False:
            dialog_message = None

        t = threading.Thread(target=self.install_batch)
        t.start()
        ThreadProgress(t, 'Building zukan files', 'Build done', dialog_message)

    def new_install_pkg_control(self):
        """
        Using Thread to build new installation files via sublime-package file,
        to avoid ST freezing.

        Try move folders if installed trough Package Control. Folders contain icons
        PNGs and zukan icons data files.

        Then install icons themes, preferences and syntaxes.
        """
        try:
            self.move_folders()
        finally:
            self.new_install_manually()
