import contextlib
import errno

import click

from git_shell_prompt.server import app
from git_shell_prompt.main import synchronisation


@contextlib.contextmanager
def suppress_os_error(*codes):
    try:
        yield
    except OSError as ex:
        if ex.errno not in codes:
            raise


def inf_range_from(start):
    while True:
        yield start

        start += 1


@click.command()
@click.option('--host', default='127.0.0.1')
@click.option('--sync-file', default=synchronisation.DEFAULT_SYNC_FILE)
def main(host, sync_file):
    daemon = synchronisation.Daemon(sync_file)

    with daemon.lock:
        for port in inf_range_from(9000):
            daemon.port = port

            with suppress_os_error(errno.EADDRINUSE):
                return app.run(host=host, port=port)


if __name__ == "__main__":
    main()
