import logging
import threading

from ..lib.icons_preferences import ZukanPreference
from ..lib.icons_syntaxes import ZukanSyntax
from ..lib.icons_themes import ZukanTheme
from ..helpers.delete_unused import delete_unused_icons
from ..helpers.load_save_settings import (
    get_theme_settings,
    get_upgraded_version_settings,
    is_zukan_restart_message,
)
from ..helpers.move_folders import MoveFolder
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

    def __init__(self):
        self.move_folder = MoveFolder()
        self.zukan_preference = ZukanPreference()
        self.zukan_syntax = ZukanSyntax()
        self.zukan_theme = ZukanTheme()

    def zukan_restart_message(self):
        return is_zukan_restart_message()

    def pkg_version_setting(self):
        pkg_version, _ = get_upgraded_version_settings()
        return pkg_version

    def install_batch(self):
        """
        Batch build themes, preferences and syntaxes, to use with Thread together
        in new install manually.
        """
        # Check 'auto_install_theme' avoid duplicate create themes when True.
        # Because deleting theme already triggers event to create themes.

        _ , auto_install_theme = get_theme_settings()

        if auto_install_theme is False:
            self.zukan_theme.create_icons_themes()

        self.zukan_syntax.build_icons_syntaxes()
        self.zukan_preference.build_icons_preferences()

        logger.info('Zukan icons v%s has been built.', self.pkg_version_setting())

    def install_syntaxes_preferences(self):
        """
        Batch build preferences and syntaxes, to use with Thread together in
        install_upgrade_thread and rebuild_icon_files_thread.
        """
        # Change build order: syntax then preferences. Notice error Bad XML,
        # when ignoring icon through Command, duplicating create preferences
        # after change from 'add_on_change' to  ViewListener.
        self.zukan_syntax.build_icons_syntaxes()
        self.zukan_preference.build_icons_preferences()

    def install_upgrade_thread(self):
        """
        Using Thread to build upgraded files, to avoid ST freezing.
        """
        try:
            # Copy new icons_data and icons folder
            self.move_folder.move_folders()

        finally:
            if self.zukan_restart_message() is True:
                dialog_message = (
                    'Zukan icons has been upgraded to v{v}.\n\n'
                    'Changelog in Sublime Text > Settings > Package Settings menu.\n\n'
                    'You may have to restart ST, if all icons do not load correct in '
                    'current theme.'.format(v=self.pkg_version_setting())
                )
            if self.zukan_restart_message() is False:
                dialog_message = (
                    'Zukan icons has been upgraded to v{v}.\n\n'
                    'Changelog in Sublime Text > Settings > Package Settings menu.'
                    '\n\n'.format(v=self.pkg_version_setting())
                )

            t = threading.Thread(target=self.install_syntaxes_preferences)
            t.start()
            ThreadProgress(t, 'Upgrading zukan files', 'Upgrade done', dialog_message)

            logger.info('upgrading Zukan icons to v%s.', self.pkg_version_setting())
            logger.info('Changelog in Sublime Text > Settings > Package Settings menu.')

            # Delete unused icons
            delete_unused_icons(ZUKAN_PKG_ICONS_PATH)
            delete_unused_icons(ZUKAN_PKG_ICONS_DATA_PRIMARY_PATH)

    def rebuild_icon_files_thread(self):
        """
        Using Thread to build syntax and preferences files, to avoid ST freezing.
        """

        t = threading.Thread(target=self.install_syntaxes_preferences)
        t.start()
        ThreadProgress(t, 'Building zukan files', 'Build done')

    def new_install(self):
        """
        Using Thread to build new installation files or when 'icons_preferences' or
        'icons_folders' do not exist, to avoid ST freezing.

        Install icons themes, preferences and syntaxes.
        """
        # Creating themes in main thread helps a little with the error not showing all
        # icons during install.
        # 'refresh_folder_list' do not help force reload. But deleting or duplicating a
        # folder with at least 5 files, it will realod file icons.
        # If change themes, the icons is working with no problem.

        if self.zukan_restart_message() is True:
            dialog_message = (
                'Zukan icons v{v} has been built.\n\n'
                'You may have to restart ST, if all icons do not load correct in '
                'current theme.'.format(v=self.pkg_version_setting())
            )
        if self.zukan_restart_message() is False:
            dialog_message = None

        t = threading.Thread(target=self.install_batch)
        t.start()
        ThreadProgress(t, 'Building zukan files', 'Build done', dialog_message)
