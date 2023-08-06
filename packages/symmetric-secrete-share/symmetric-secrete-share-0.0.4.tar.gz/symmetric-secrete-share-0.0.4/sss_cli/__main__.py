import typer

from sss_cli import __version__
from sss_cli._string_template import EXAMPLE_KEYCHAIN
from sss_cli.helper import get_keychain
from sss_cli.inject import inject
from sss_cli.share import share

app = typer.Typer()


@app.command("key")
def set_key(
    clear: bool = typer.Option(
        False, "-c", "--clear", help="Clear all keys in keychain"
    ),
    force: bool = typer.Option(
        False, "-f", "--force", help="Force clear all keys in keychain"
    ),
):
    """Edit keys in keychain."""
    keychain = get_keychain()
    if clear:
        if not force:
            typer.confirm("Are you sure you want to delete it?", abort=True)
        if keychain.is_file():
            keychain.unlink()
            typer.secho("Cleared keychain.", fg="green")
        return
    if not keychain.is_file():
        keychain.write_text(EXAMPLE_KEYCHAIN)
    typer.secho("Please edit keychain config file.", fg="green")
    typer.launch(str(keychain))


@app.command("share")
def cmd_share(
    config_path: str = typer.Argument(..., help="Path to your repo"),
    key: str = typer.Option("", "-k", "--key", help="Password as plaintext"),
):
    """Update the cypher file by encrypting the secret file."""
    share(config_path, key)


@app.command(name="inject")
def cmd_inject(
    config_path: str = typer.Argument(..., help="Path to your repo"),
    key: str = typer.Option("", "-k", "--key", help="Password as plaintext"),
):
    """Inject the decrypted cypher to correct path in repo."""
    inject(config_path, key)
