import codecs
import os.path
import setuptools


class FileReader:
    here = os.path.abspath(os.path.dirname(__file__))

    def __init__(self, path, default=None):
        self.path = os.path.join(self.here, path)
        self.default = default

    def __call__(self, handler):
        return self.then(handler)

    @classmethod
    def get(cls, path, default=None):
        return cls(path, default)

    def then(self, handler):
        result = self.default

        if callable(result):
            result = result()

        if os.path.exists(self.path):
            with codecs.open(self.path) as handle:
                try:
                    result = handler(handle)
                except Exception as ex:
                    print(ex)

        return result

    def then_read(self):
        return self.then(self._read)

    @staticmethod
    def _read(handle):
        return handle.read()


setuptools.setup(
    name="GitShellPrompt",
    version="0.1",
    description="A better prompt for git repositories",
    long_description=FileReader.get('README.rst', default="").then_read(),
    url="https://github.com/alistair-broomhead/GitShellPrompt",
    package_dir={'': 'src'},
    packages=setuptools.find_packages('src'),
    install_requires=[
        'aiohttp',
        'click',
    ],
    extra_requires={
        'dev': [
            'twine',
        ],
    },
    entry_points={
        'console_scripts': [
            'git-shell-prompt-daemon=git_shell_prompt.server.daemon:main'
        ],
    },
)

