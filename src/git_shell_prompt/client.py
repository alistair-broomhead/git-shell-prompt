import os
import urllib.parse
import urllib.request

import click

from git_shell_prompt import synchronisation


def url_for(netloc, path, query, scheme='http', fragment=''):
    if query is None or isinstance(query, str):
        pass
    else:
        query = urllib.parse.urlencode(query)

    return urllib.parse.urlunsplit((scheme, netloc, path, query, fragment))


def get(url):
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')


class Client(synchronisation.Client):

    @staticmethod
    def query(output_format):
        out = []

        if output_format:
            out.append(('fmt', output_format))

        return out

    def get(self, host='127.0.0.1', path='.', output_format='json'):
        url = url_for(
            netloc=f'{host}:{self.port}',
            path=path,
            query=self.query(output_format)
        )

        return get(url)


@click.command()
@click.option('--host', default='127.0.0.1')
@click.option('--sync-file', default=synchronisation.DEFAULT_SYNC_FILE)
@click.option('--output-format', type=click.Choice(('json', 'bash')))
def main(host, sync_file, output_format):
    print(Client(sync_file).get(host, os.getcwd(), output_format))


if __name__ == '__main__':
    main()
