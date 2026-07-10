import subprocess

from settings import MODE


def get_current_branch():
    result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        capture_output=True, text=True
    )
    return result.stdout.strip()


def test_mode_matches_branch():
    branch = get_current_branch()
    expected = {
        "main": "prod",
        "dev": "dev",
    }
    if branch in expected:
        assert MODE == expected[branch], (
            f"Ветка '{branch}' требует MODE='{expected[branch]}', "
            f"а сейчас MODE='{MODE}'"
        )
