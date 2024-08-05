from click.testing import CliRunner

import ringsome


def test_get_countries():
    runner = CliRunner()
    result = runner.invoke(ringsome.cli, ["get", "countries"])
    assert result.exit_code == 0
    assert "United States of America" in result.output


def test_get_nodes():
    runner = CliRunner()
    result = runner.invoke(ringsome.cli, ["get", "nodes"])
    assert result.exit_code == 0
    assert "linode" in result.output


def test_get_nodes_for_country():
    runner = CliRunner()
    result = runner.invoke(ringsome.cli, ["get", "nodes", "--country", "PT"])
    assert result.exit_code == 0
    for line in result.output.splitlines():
        # Get only the lines in the table with the hostnames, which all end in nlnog.net
        if "nlnog.net" in line:
            assert "PT" in line
        else:
            continue
