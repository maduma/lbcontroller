import click
import sys
import os
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
    auth = basic_auth()
    status = lbctrl.get_group_status(addr, group, proto=proto, auth=auth)
    click.echo(f'Status for {group} on {addr} {proto} loadbalancer: {status}')
    error_code = status[0]
    if error_code == 'ok':
        sys.exit(0)
    else:
        sys.exit(1)

@cli.command()
@click.argument('group')
@click.argument('instance', type=int)
@click.pass_context
def enable(ctx, group, instance):
    set_status(ctx, group, instance, disable=False)

@cli.command()
@click.argument('group')
@click.argument('instance', type=int)
@click.pass_context
def disable(ctx, group, instance):
    set_status(ctx, group, instance, disable=True)

def set_status(ctx, group, instance, disable):
    addr = ctx.obj['ADDR']
    proto = ctx.obj['PROTO']
    action = 'disable' if disable else 'enable'
    click.echo(f'{action} instance {instance} of {group} on {addr} {proto} loadbalancer')
    auth = basic_auth()
    success = lbctrl.set_worker(addr, group, instance, disable=disable, proto=proto, auth=auth)
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

def basic_auth():
    if 'LB_USER' in os.environ and 'LB_PASSWORD' in os.environ:
        return os.environ['LB_USER'], os.environ['LB_PASSWORD']
    return None

def main():
    cli(obj={})
