from click.testing import CliRunner
import ringsome


def test_get_countries():
    runner = CliRunner()
    result = runner.invoke(ringsome.cli, ["get", "countries"])
    assert result.exit_code == 0
    assert "United States of America" in result.output
