"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -mspihole` python will execute
    ``__main__.py`` as a script. That means there won't be any
    ``spihole.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there's no ``spihole.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""
import functools
import logging
import os
import signal
import sys
import threading

import click

from .capture import Capture
from .display import Display
from .hub import Hub
from .keypad import KeyPad


def signal_handler(stop_event: threading.Event, received_signal, _frame):
    logging.info('Signal received: %s', received_signal)
    stop_event.set()


def install_handlers(stop_event: threading.Event):
    handler = functools.partial(signal_handler, stop_event)
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)


@click.command()
@click.option("-c", "--configuration", type=click.Path(readable=True),
              default=os.path.join(os.path.sep, 'etc', 'spihole.conf'))
def main(configuration):
    # configuration_file = click.format_filename(configuration)
    logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    hub = Hub()
    capture = Capture(hub)
    display = Display(hub)
    keypad = KeyPad(hub)

    startables = [hub, display, capture, keypad]
    for startable in startables:
        startable.start()

    stop_evt = threading.Event()
    logging.debug('Starting main loop')
    while not stop_evt.is_set():
        try:
            signal.pause()  # interruptible idle
        except KeyboardInterrupt:
            stop_evt.set()
    logging.debug('Main loop completed, closing threads')
    for startable in startables:
        startable.stop()

    for startable in startables:
        startable.join()
