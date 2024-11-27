from src.build.scripts import create_parser, main
from src.build.utils.scripts_args import COMMANDS
from tests.mocks.constants_scripts import (
    # COMMANDS_ARGS_PATH_P2,
    # COMMANDS_ARGS_PATH_P3,
    COMMANDS_ARGS_PATH_P4,
    COMMANDS_ARGS_PATH_P5,
    COMMANDS_ARGS_PATH_P6,
    COMMANDS_ARGS_PATH_P10,
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
        for p1, p2, p3, p4, p5, p6, p7, p8, p9, p10 in COMMANDS_ARGS_PATH_P10:
            with patch(p1) as mock_command:
                # Simulate command-line arguments
                with patch('sys.argv', ['script_name'] + p2):
                    main()

                mock_command.assert_called_once_with(p3, p4, p5, p6, p7, p8, p9, p10)
