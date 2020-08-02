import click

@click.group()
def cli():
    pass

@cli.command()
def status():
    click.echo('Initialized the database')

@cli.command()
def disable():
    click.echo('Dropped the database')

@cli.command()
def enable():
    click.echo('Dropped the database')

if __name__ == '__main__':
    cli()