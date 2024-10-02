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
