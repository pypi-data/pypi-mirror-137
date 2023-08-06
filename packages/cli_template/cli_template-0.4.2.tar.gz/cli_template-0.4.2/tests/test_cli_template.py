from click.testing import CliRunner

from cli_template import cli


def test_cli():
    runner = CliRunner()
    result = runner.invoke(cli, ["initdb"])
    assert result.exit_code == 0
    assert result.output == "Initialized the database\n"
