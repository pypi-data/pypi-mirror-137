import typer

from pathlib import Path

from camt import __app_name__


APP_PATH = Path(typer.get_app_dir(__app_name__))
