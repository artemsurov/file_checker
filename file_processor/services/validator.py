import io
from contextlib import redirect_stdout
from pathlib import Path

from flake8.main import cli


def flake_validator(path_to_file: str):
    file = Path(path_to_file)
    if not file.exists():
        raise FileNotFoundError()
    with redirect_stdout(io.TextIOWrapper(io.BytesIO())) as f:
        cli.main([str(file)])
    f.seek(0)
    return f.readlines()
