import logging
import sublime_plugin

from ..events.install import InstallEvent
from ..lib.icons_themes import ZukanTheme

logger = logging.getLogger(__name__)


class RebuildFilesCommand(sublime_plugin.ApplicationCommand):
    """
    Sublime command to rebuild sublime-themes and sublime-syntaxes.
    """

    def __init__(self, install_event=None, zukan_theme=None):
        self.install_event = install_event if install_event else InstallEvent()
        self.zukan_theme = zukan_theme if zukan_theme else ZukanTheme()

    def run(self):
        """
        Try move folders if installed trough Package Control. Then install
        sublime-theme and sublime-syntax files.
        """
        try:
            # Syntax getting deleted in 'build_icons_preferences' which
            # is used by 'new_install_manually'
            # ZukanPreference.delete_icons_preferences()
            self.zukan_theme.delete_icons_themes()
            # Syntax getting deleted in 'build_icons_syntaxes' which
            # is used by 'new_install_manually'
            # ZukanSyntax.delete_icons_syntaxes()
        finally:
            self.install_event.new_install_manually()
