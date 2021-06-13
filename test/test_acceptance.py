import csv
import os
import subprocess

import pytest

from spotify_backup import OAUTH_TOKEN_ENV_VAR


@pytest.fixture(scope="module", autouse=True)
def test_make_sure_api_key_is_defined_for_acceptance_tests():
    assert os.getenv(OAUTH_TOKEN_ENV_VAR), f"Env variable {OAUTH_TOKEN_ENV_VAR} must be defined " \
                                           f"for acceptance tests to work"


def test_should_call_for_results(tmpdir: str):
    test_csv_path = os.path.join(tmpdir, f"test.csv")
    test_cmd = f"spotify-backup {test_csv_path} --dump playlists"
    completed_process = subprocess.run(test_cmd.split(), timeout=10., capture_output=True)
    process_logs = f"\nstdout: {completed_process.stdout.decode()}" \
                   f"\nstderr: {completed_process.stderr.decode()}"

    assert completed_process.returncode == 0, f"Command returned non-zero exit code: {completed_process.returncode} {process_logs}"
    assert os.path.isfile(test_csv_path), f"Expected output file does not exist: {test_csv_path}; {process_logs}"

    with open(test_csv_path, "r") as _actual_csv:
        first_row = _actual_csv.readline()
    assert first_row == 'test,spotify:track:4u3cJaAUcmp4qPKUUcxXZv,UNKLE,War Stories,Mistress (feat Alicia Temple)\n', \
        f"First row: {first_row} differs from expected"

    with open(test_csv_path, "r") as _actual_csv:
        csv_reader = csv.reader(_actual_csv, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in csv_reader:
            assert row, f"Found empty row in result file"
            assert len(row) == 5, f"Unexpected values count in row: {row}"
