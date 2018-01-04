import itertools
import errno

import click

from git_shell_prompt.server import app
from git_shell_prompt import synchronisation


@click.command()
@click.option('--host', default='127.0.0.1')
@click.option('--sync-file', default=synchronisation.DEFAULT_SYNC_FILE)
@click.option('--workers', default=1)
def main(host, sync_file, workers):
    daemon = synchronisation.Daemon(sync_file)

    for port in itertools.count(9000):
        application = app.StandaloneApplication.create(host, port, workers)

        with daemon.lock:
            daemon.port = port

            try:
                return application.run()
            except OSError as ex:
                if ex.errno != errno.EADDRINUSE:
                    raise


if __name__ == "__main__":
    main()
