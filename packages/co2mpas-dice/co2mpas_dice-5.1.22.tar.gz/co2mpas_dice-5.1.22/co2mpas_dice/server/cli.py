# -*- coding: utf-8 -*-
#
# Copyright 2016-2021 European Commission (JRC);
# Licensed under the EUPL (the 'Licence');
# You may not use this work except in compliance with the Licence.
# You may obtain a copy of the Licence at: http://ec.europa.eu/idabc/eupl
r"""
DICE command line tool.
"""

import os
import click
import logging
import click_log
import os.path as osp
from co2mpas_dice._version import __version__

log = logging.getLogger('co2mpas_dice.cmd')


# noinspection PyMissingOrEmptyDocstring
class Logger(logging.Logger):
    def setLevel(self, level):
        super(Logger, self).setLevel(level)
        frmt = "%(asctime)-15s:%(levelname)5.5s:%(name)s:%(message)s"
        logging.basicConfig(level=level, format=frmt)
        rlog = logging.getLogger()
        # because `basicConfig()` does not reconfig root-logger when re-invoked.
        rlog.level = level
        logging.captureWarnings(True)


logger = Logger('cli')
click_log.basic_config(logger)


@click.group(
    'co2mpas_dice', context_settings=dict(help_option_names=['-h', '--help'])
)
@click.version_option(__version__)
def cli():
    """
    DICE command line tool.

    \b
    Quick start:
    dice server app.ini

    \b
    Using docker:
    docker run --rm -it -v $(pwd):/build -p 5000:80 dice/back-end:vX.X.X co2mpas_dice server
    """
    os.chdir(os.environ.get('CWD', '.'))


@cli.command('example', short_help='Generates sample configuration file.')
@click.argument('ini-file', default='sample_app.ini', required=False)
@click.option('--force', is_flag=True, help='Overwrite configuration files.')
@click.pass_context
def example(ctx, ini_file, force):
    """
    Writes a sample configuration INI_FILE.

    INI_FILE: DICE configuration file. [default: ./sample_app.ini]
    """

    import shutil
    from pkg_resources import resource_filename as res_fn
    if force or not osp.isfile(ini_file):
        os.makedirs(osp.dirname(ini_file) or '.', exist_ok=True)
        shutil.copy2(res_fn('co2mpas_dice.server', 'app.ini'), ini_file)
    ctx.forward(configure, ini_file=ini_file)
    return ini_file


@cli.command('server', short_help='Runs the DICE server.')
@click.argument('ini_file', type=click.Path(), required=False)
@click.option('--flask', is_flag=True,
              help='Run the server as flask instead of gunicorn.')
@click_log.simple_verbosity_option(logger)
@click.pass_context
def server(ctx, ini_file, flask):
    """Runs the DICE server using the configuration file (INI_FILE)."""
    if osp.isfile(ini_file):
        ctx.invoke(configure, ini_file=ini_file, force=False)
    elif ini_file:
        ini_file = ctx.invoke(example, ini_file=ini_file, force=False)
    else:
        ini_file = ctx.invoke(example, force=False)

    import subprocess
    from co2mpas_dice.server.config import conf
    from co2mpas_dice.server.clean import start_cron
    os.environ['DICE_INI'] = osp.abspath(ini_file)

    if flask:
        os.environ['FLASK_APP'] = osp.join(osp.dirname(__file__), 'app.py')
        args = ['flask', 'run']
        args += ['--%s=%s' % v for v in conf['flask'].items()]
    else:
        args = ['gunicorn', 'co2mpas_dice.app:app']
        args += ['--%s=%s' % v for v in conf['gunicorn'].items()]
    try:
        start_cron()
        subprocess.call(' '.join(args), shell=True)
    except KeyboardInterrupt:
        pass


@cli.command('configure', short_help='Configure the DICE server folders.')
@click.argument('ini_file', type=click.Path(exists=True))
@click.option('--force', is_flag=True, help='Overwrite configuration files.')
@click_log.simple_verbosity_option(logger)
def configure(ini_file, force):
    """
    Configure the DICE server folders using the configuration file (INI_FILE).
    """
    import glob
    import shutil
    from co2mpas_dice.server.config import conf
    from pkg_resources import resource_filename as fn

    conf.read(ini_file)
    pn = 'co2mpas_dice.server'
    folders = [
        (fn(pn, 'keys'), conf['dice']['keys_folder'], '*'),
        (fn(pn + '.validate', ''), conf['dice']['validation_folder'], '*.json'),
        (fn(pn, 'templates'), conf['app']['template_folder'], '*'),
        (fn(pn, 'static'), conf['app']['static_folder'], '*'),
        (fn(pn + '.mail', 'templates'), conf['dice']['mail_folder'], '*'),
        (fn(pn, ''), conf['dice']['error_folder'], 'err.yaml'),
    ]

    def _recursive(src, dst, ext):
        for fpath in glob.glob(osp.join(src, ext)):
            fp = osp.join(dst, osp.basename(fpath))
            if osp.isfile(fpath):
                if force or not osp.isfile(fp):
                    os.makedirs(osp.dirname(fp), exist_ok=True)
                    shutil.copy2(fpath, fp)
            elif osp.isdir(fpath):
                _recursive(fpath, fp, ext)

    for v in folders:
        _recursive(*v)


@cli.command('keys', short_help='Generate new DICE keys.')
@click.argument('output_folder', type=click.Path(exists=True))
def keys(output_folder):
    """
    Generate new DICE keys into OUTPUT_FOLDER.
    """
    from co2mpas_dice.crypto import generate_keys
    generate_keys(output_folder)


if __name__ == '__main__':
    cli()
