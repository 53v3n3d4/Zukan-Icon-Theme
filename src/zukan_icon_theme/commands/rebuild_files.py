import logging
import sublime_plugin

from ..events.install import InstallEventE2
from ..lib.icons_themes import ZukanThemeT2

logger = logging.getLogger(__name__)


class RebuildFilesCommand(
    sublime_plugin.ApplicationCommand, InstallEventE2, ZukanThemeT2
):
    """
    Sublime command to rebuild sublime-themes and sublime-syntaxes.
    """

    def __init__(self):
        InstallEventE2.__init__(self)
        ZukanThemeT2.__init__(self)

    def run(self):
        """
        Try move folders if installed trough Package Control. Then install
        sublime-theme and sublime-syntax files.
        """
        try:
            # Syntax getting deleted in 'build_icons_preferences' which
            # is used by 'new_install_manually'
            # ZukanPreference.delete_icons_preferences()
            self.delete_icons_themes()
            # Syntax getting deleted in 'build_icons_syntaxes' which
            # is used by 'new_install_manually'
            # ZukanSyntax.delete_icons_syntaxes()
        finally:
            self.new_install_manually()


# class RebuildFilesCommand(sublime_plugin.ApplicationCommand):
#     """
#     Sublime command to rebuild sublime-themes and sublime-syntaxes.
#     """

#     def run(self):
#         """
#         Try move folders if installed trough Package Control. Then install
#         sublime-theme and sublime-syntax files.
#         """
#         try:
#             # Syntax getting deleted in 'build_icons_preferences' which
#             # is used by 'new_install_manually'
#             # ZukanPreference.delete_icons_preferences()
#             ZukanTheme.delete_icons_themes()
#             # Syntax getting deleted in 'build_icons_syntaxes' which
#             # is used by 'new_install_manually'
#             # ZukanSyntax.delete_icons_syntaxes()
#         finally:
#             InstallEvent.new_install_manually()
