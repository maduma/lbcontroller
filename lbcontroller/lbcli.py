import click

@click.group()
@click.option('--addr', help='loadbalancer address', required=True)
@click.option('--proto', help='http|https, default to https', default='https')
@click.pass_context
def cli(ctx, addr, proto):
    ctx.obj['ADDR'] = addr
    ctx.obj['PROTO'] = proto
    pass

@cli.command()
@click.argument('group')
@click.pass_context
def status(ctx, group):
    addr = ctx.obj['ADDR']
    proto = ctx.obj['PROTO']
    click.echo(f'Status for {group} on {addr} {proto} loadbalancer')

@cli.command()
@click.argument('group')
@click.argument('instance')
@click.pass_context
def disable(ctx, group, instance):
    addr = ctx.obj['ADDR']
    proto = ctx.obj['PROTO']
    click.echo(f'Disable instance {instance} of {group} on {addr} {proto} loadbalancer')

@cli.command()
@click.argument('group')
@click.argument('instance')
@click.pass_context
def enable(ctx, group, instance):
    addr = ctx.obj['ADDR']
    proto = ctx.obj['PROTO']
    click.echo(f'enable instance {instance} of {group} on {addr} {proto} loadbalancer')

def main():
    cli(obj={})
