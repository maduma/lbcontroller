import click
from lbcontroller import lbctrl

@click.group()
@click.option('--addr', help='loadbalancer address', required=True)
@click.option('--http', help='force http, default is https', is_flag=True)
@click.pass_context
def cli(ctx, addr, http):
    ctx.obj['ADDR'] = addr
    ctx.obj['PROTO'] = 'http' if http else 'https'
    pass

@cli.command()
@click.argument('group')
@click.pass_context
def status(ctx, group):
    addr = ctx.obj['ADDR']
    proto = ctx.obj['PROTO']
    status = lbctrl.get_group_status(addr, group, proto=proto)
    click.echo(f'Status for {group} on {addr} {proto} loadbalancer: {status}')

@cli.command()
@click.argument('group')
@click.argument('instance', type=int)
@click.pass_context
def disable(ctx, group, instance):
    addr = ctx.obj['ADDR']
    proto = ctx.obj['PROTO']
    click.echo(f'Disable instance {instance} of {group} on {addr} {proto} loadbalancer')
    lbctrl.set_worker(addr, group, instance, disable=True, proto=proto)

@cli.command()
@click.argument('group')
@click.argument('instance', type=int)
@click.pass_context
def enable(ctx, group, instance):
    addr = ctx.obj['ADDR']
    proto = ctx.obj['PROTO']
    click.echo(f'enable instance {instance} of {group} on {addr} {proto} loadbalancer')
    lbctrl.set_worker(addr, group, instance, disable=False, proto=proto)

def main():
    cli(obj={})
