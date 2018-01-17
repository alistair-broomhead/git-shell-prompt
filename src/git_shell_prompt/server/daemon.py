import itertools
import errno

import click

from git_shell_prompt.server import app
from git_shell_prompt import synchronisation


@click.command()
@click.option('--host', default='127.0.0.1')
@click.option('--sync-file', default=synchronisation.DEFAULT_SYNC_FILE)
@click.option('--workers', default=1)
@click.option('--debug/--production', default=False)
def main(host, sync_file, workers, debug):
    daemon = synchronisation.Daemon(sync_file)

    app_class = app.DebugApplication if debug else app.StandaloneApplication

    for port in itertools.count(9000):
        application = app_class.create(host, port, workers)

        with daemon.lock:
            daemon.port = port

            try:
                return application.run()
            except OSError as ex:
                if ex.errno != errno.EADDRINUSE:
                    raise


if __name__ == "__main__":
    main()
