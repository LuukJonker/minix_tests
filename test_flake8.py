import subprocess


def test_flake8():
    res = subprocess.Popen(
        ["flake8", "--max-line-length=120", "--ignore=E203,W503", "--exclude=minix_tests"],
        stdout=subprocess.PIPE,
    ).stdout.read()
    print(res)
    assert len(res) == 0 and "Flake8 outputted something"
