import logging
import sublime_plugin

from .install import InstallEvent
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
            self.zukan_theme.delete_icons_themes()

        finally:
            self.install_event.new_install_manually()
