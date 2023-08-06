#! /usr/bin/env python

import click
import os
import logging
import sys

plugin_folder = os.path.join(os.path.dirname(__file__), 'subcommands')

class MyCLI(click.MultiCommand):

    def list_commands(self, ctx):
        rv = []
        for filename in os.listdir(plugin_folder):
            if filename.endswith('.py') and filename != '__init__.py': #,'validations.py','exceptions.py','utils.py'
                rv.append(filename[:-3])
        rv.sort()
        return rv

    def get_command(self, ctx, name):
        try:
            ns = {}
            fn = os.path.join(plugin_folder, name + '.py')
            with open(fn) as f:
                code = compile(f.read(), fn, 'exec')
                eval(code, ns, ns)
            return ns['cli']
        except Exception as err:
            logging.error(err)

@click.command(cls=MyCLI)
def cli():
    '''Command-line tool for ease the execution of batch jobs with Spark.'''
    pass

if __name__ == '__main__':
    try:
        cli()
    except Exception as err:
        logging.error(f"    {err}")