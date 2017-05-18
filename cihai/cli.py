# -*- coding: utf8 - *-
from __future__ import (absolute_import, division, print_function,
                        with_statement)

import logging

import click

from .__about__ import __version__
from ._compat import PY2
from .core import Cihai


@click.group(context_settings={'obj': {}})
@click.version_option(
    __version__, '-V', '--version', message='%(prog)s %(version)s'
)
@click.option('-c', '--config', type=click.Path(exists=True))
@click.option('--log_level', default='INFO',
              help='Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
@click.pass_context
def cli(ctx, config, log_level):
    """For help and example usage, see documentation:
    https://cihai.git-pull.com"""
    setup_logger(
        level=log_level.upper()
    )
    if config:
        c = Cihai.from_file(config)
    else:
        c = Cihai()

    if not c.is_bootstrapped:
        from .bootstrap import bootstrap_unihan
        click.echo("Bootstrapping Unihan database")
        bootstrap_unihan(c.metadata, c.config.get('unihan_options', {}))
        c.reflect_db()

    ctx.obj['c'] = c  # pass Cihai object down to other commands


@cli.command(name='info', short_help='Get details on a CJK character')
@click.argument('char')
@click.pass_context
def command_info(ctx, char):
    c = ctx.obj['c']
    Unihan = c.base.classes.Unihan
    query = c.session.query(Unihan).filter_by(char=char).first()
    for c in query.__table__.columns._data.keys():
        value = getattr(query, c)
        if value:
            if PY2:
                value = value.encode('utf-8')

            print('{:>30} {:>60}'.format(c, value))


def setup_logger(logger=None, level='INFO'):
    """Setup logging for CLI use.

    :param logger: instance of logger
    :type logger: :py:class:`Logger`

    """
    if not logger:
        logger = logging.getLogger()
    if not logger.handlers:
        channel = logging.StreamHandler()

        logger.setLevel(level)
        logger.addHandler(channel)