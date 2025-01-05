import logging
import sublime_plugin

from ..events.install import InstallEvent
from ..lib.icons_themes import ZukanTheme

logger = logging.getLogger(__name__)


class RebuildFilesCommand(sublime_plugin.ApplicationCommand):
    """
    Sublime command to rebuild sublime-themes and sublime-syntaxes.
    """

    def run(self):
        """
        Try move folders if installed trough Package Control. Then install
        sublime-theme and sublime-syntax files.
        """
        try:
            # Syntax getting deleted in 'build_icons_preferences' which
            # is used by 'new_install_manually'
            # ZukanPreference.delete_icons_preferences()
            ZukanTheme.delete_icons_themes()
            # Syntax getting deleted in 'build_icons_syntaxes' which
            # is used by 'new_install_manually'
            # ZukanSyntax.delete_icons_syntaxes()
        finally:
            InstallEvent.new_install_manually()
