from src.build.scripts import create_parser, main
from src.build.utils.scripts_args import COMMANDS
from tests.mocks.constants_scripts import (
    # COMMANDS_ARGS_PATH_P2,
    # COMMANDS_ARGS_PATH_P3,
    COMMANDS_ARGS_PATH_P4,
    COMMANDS_ARGS_PATH_P5,
    COMMANDS_ARGS_PATH_P6,
    COMMANDS_ARGS_PATH_P9,
)
from unittest.mock import patch


class TestScripts:
    def test_create_parser(self):
        parser = create_parser(COMMANDS)
        assert parser  # Ensure parser is created

        # Check if help is available
        help_message = parser.format_help()
        assert '--help' in help_message

    def test_error_message_no_args(self, capsys):
        args = ['clean']
        with patch('sys.argv', ['script_name'] + args):
            main()
        captured = capsys.readouterr()
        assert 'Error' in captured.out
        assert 'You need pass an argument. Use --help to see options.' in captured.out

    # Giving a Fixture Error of cli_cmd_path not found
    # def test_cli(self, cli_cmd_path):
    #     """
    #     Generic test function to handle multiple command scenarios.

    #     Parameters:
    #     cli_cmd_path (list) - A list of tuples with parameters for each command.
    #     """
    #     for args in cli_cmd_path:
    #         command_path, command_args, *expected_args = args

    #         with patch(command_path) as mock_command:
    #             # Simulate command-line arguments
    #             with patch('sys.argv', ['script_name'] + command_args):
    #                 main()

    #             mock_command.assert_called_once_with(*expected_args)

    # def test_scripts_p2(self):
    #     TestScripts.test_scripts(self, COMMANDS_ARGS_PATH_P2)

    # def test_scripts_p3(self):
    #     TestScripts.test_scripts(self, COMMANDS_ARGS_PATH_P3)

    # def test_scripts_p4(self):
    #     TestScripts.test_cli(self, COMMANDS_ARGS_PATH_P4)

    # def test_scripts_p5(self):
    #     TestScripts.test_cli(self, COMMANDS_ARGS_PATH_P5)

    # def test_scripts_p7(self):
    #     TestScripts.test_cli(self, COMMANDS_ARGS_PATH_P5)

    # def test_scripts_p9(self):
    #     TestScripts.test_cli(self, COMMANDS_ARGS_PATH_P9)

    # def test_scripts_p2(self):
    #     for p1, p2 in COMMANDS_ARGS_PATH_P2:
    #         with patch(p1) as mock_command:
    #             # Simulate command-line arguments
    #             with patch('sys.argv', ['script_name'] + p2):
    #                 main()

    #             mock_command.assert_called_once()

    # def test_scripts_p3(self):
    #     for p1, p2, p3 in COMMANDS_ARGS_PATH_P3:
    #         with patch(p1) as mock_command:
    #             # Simulate command-line arguments
    #             with patch('sys.argv', ['script_name'] + p2):
    #                 main()

    #             mock_command.assert_called_once_with(p3)
    #             # assert isinstance(mock_command.call_args.args[p2], str)

    def test_scripts_p4(self):
        for p1, p2, p3, p4 in COMMANDS_ARGS_PATH_P4:
            with patch(p1) as mock_command:
                # Simulate command-line arguments
                with patch('sys.argv', ['script_name'] + p2):
                    main()

                mock_command.assert_called_once_with(p3, p4)

    def test_scripts_p5(self):
        for p1, p2, p3, p4, p5 in COMMANDS_ARGS_PATH_P5:
            with patch(p1) as mock_command:
                # Simulate command-line arguments
                with patch('sys.argv', ['script_name'] + p2):
                    main()

                mock_command.assert_called_once_with(p3, p4, p5)

    def test_scripts_p6(self):
        for p1, p2, p3, p4, p5, p6 in COMMANDS_ARGS_PATH_P6:
            with patch(p1) as mock_command:
                # Simulate command-line arguments
                with patch('sys.argv', ['script_name'] + p2):
                    main()

                mock_command.assert_called_once_with(p3, p4, p5, p6)

    def test_scripts_p9(self):
        for p1, p2, p3, p4, p5, p6, p7, p8, p9 in COMMANDS_ARGS_PATH_P9:
            with patch(p1) as mock_command:
                # Simulate command-line arguments
                with patch('sys.argv', ['script_name'] + p2):
                    main()

                mock_command.assert_called_once_with(p3, p4, p5, p6, p7, p8, p9)


# class TestCreateParser(TestCase):
#     def test_parser_has_subparsers(self):
#         self.parser = create_parser(commands_args)
#         subparsers = self.parser._subparsers
#         assert isinstance(subparsers, argparse._SubParsersAction)

# def test_command_parsers_created(self):
#     # Check if subparsers for each command exist
#     subparsers = self.parser._subparsers._actions[0].choices
#     self.assertIn('clean', subparsers)
#     self.assertIn('concat', subparsers)

# def test_clean_parser_arguments(self):
#     clean_parser = self.parser._subparsers._actions[0].choices['clean']
#     expected_args = [
#         ('-a', '--all', {'action': 'store_true'}, False, 'Clean all SVGs from src/icons folder.', False),
#         ('-d', '--directory', {'type': str}, None, 'Path to SVGs folder.', False),
#         ('-f', '--file', {'type': str}, None, 'Path to SVG file.', False),
#         ('-l', '--list', {'default': 'unused_list'}, None, 'List of unused tags to be removed.', False)
#     ]
#     for arg in expected_args:
#         self._assert_argument(clean_parser, *arg)

# def test_concat_parser_arguments(self):
#     concat_parser = self.parser._subparsers._actions[0].choices['concat']
#     expected_args = [
#         ('-a', '--all', {'action': 'store_true'}, False, 'Concat SVG file with all icons.', False),
#         ('-cf', '--concatfile', {'type': str}, None, 'Path to concat SVG file.', False),
#         ('-d', '--data', {'type': str}, None, 'Path to folder data.', False),
#         ('-i', '--icon', {'type': str}, 'icons_svg_path', 'Path to icons SVGs folder.', False),
#         ('-ipr', '--iconsperrow', {'type': int, 'default': 5}, None, 'Icons per row in concat SVG.', False),
#         ('-mh', '--maxheight', {'type': int, 'default': 2000}, None, 'Max height of concat SVG file.', False),
#         ('-sa', '--sample', {'action': 'store_true'}, False, 'Concat SVG file from random selection.', False),
#         ('-sano', '--samplenumbers', {'type': int, 'default': 30}, None, 'Number of icons in random sample.', False)
#     ]
#     for arg in expected_args:
#         self._assert_argument(concat_parser, *arg)


#     def _assert_argument(self, parser, flag, option, action=None, default=None, help_text=None, required=False, type=None):
#         for action_item in parser._actions:
#             if action_item.dest == option.replace('-', '').replace('--', ''):
#                 self.assertEqual(action_item.option_strings, [flag, option])
#                 self.assertEqual(action_item.help, help_text)
#                 self.assertEqual(action_item.required, required)
#                 self.assertEqual(action_item.default, default)
#                 if type:
#                     self.assertEqual(action_item.type, type)
#                 self.assertEqual(action_item.action, action)
#                 return
#         self.fail(f'Argument {flag} not found in parser {parser.prog}')
