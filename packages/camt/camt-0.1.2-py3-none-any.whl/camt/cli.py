from typing import Optional

import typer

from camt import __app_name__, __version__
from camt.camt import archive, _copy, get_labeled_files

app = typer.Typer()


@app.command()
def compress(
    dest_dir: str = typer.Option(
        "--dest-dir",
        help="Zip file name"
    ),
    src_dir: str = typer.Option(
        "--src-dir",
        help="Dir where the labeled images are"
    ),
    format: str = typer.Option(
        "--format",
        help="Compression format. Ex. zip, tar, gztar, bztar, or xztar",
    )
) -> None:
    files = get_labeled_files(src_dir)

    _copy(files, dest_dir)

    archive(dest_dir, src_dir, _format=format)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    _ = version
    return
