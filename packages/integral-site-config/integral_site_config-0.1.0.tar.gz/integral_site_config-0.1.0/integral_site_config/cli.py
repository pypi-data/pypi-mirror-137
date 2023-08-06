"""Console script for integral_site_config."""
import sys
import click
import integral_site_config


@click.group()
def cli():
    pass

@cli.command()
def show():
    for k, v in dict(integral_site_config.settings).items():
        click.echo(f"{k:50s}: {str(v):50}")


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
