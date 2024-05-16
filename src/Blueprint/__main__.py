"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Blueprint."""


if __name__ == "__main__":
    main(prog_name="Blueprint")  # pragma: no cover
