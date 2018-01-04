import json
import os.path
import pathlib
import typing

DEFAULT_SYNC_FILE = os.path.expanduser('~/.git-sh-prompt-sync')

Callback = typing.Optional[typing.Callable]


class NotSet(ValueError):
    pass


class Locked(ValueError):
    pass


class Reader:

    def __init__(self, sync_file_path):
        self.path = pathlib.Path(sync_file_path)

    @property
    def exists(self):
        return self.path.exists()

    def read(self):
        try:
            with self.path.open() as handle:
                return json.load(handle)
        except (FileNotFoundError, json.JSONDecodeError):
            raise NotSet(str(self.path))


class Writer(Reader):

    def safe_write(self, data):
        """
        Ensure reads never get corrupted data

        By writing to a temporary directory and then moving
        that file over the sync-file path, the write is
        guaranteed to be atomic, and so it is impossible to
        have a read of a file in a half-written state.
        """
        suffix = self.path.suffix
        suffix = f'{suffix}~swp' if suffix else '.swp'

        temp_path = self.path.with_suffix(suffix)

        with temp_path.open('w') as handle:
            json.dump(data, handle)

        temp_path.replace(self.path)

    def clear(self):
        if self.exists:
            self.path.unlink()


class FileLock:
    def __init__(self, writer: Writer):
        self.accessor = writer

    def __enter__(self):
        if self.accessor.exists:
            raise Locked

        self.accessor.safe_write({})

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.accessor.clear()


def read_accessor(**accessors):
    def inner(cls):
        for reader_name, keys in accessors.items():
            for key in keys:
                setattr(cls, key, _read_accessor(reader_name, key))
        return cls
    return inner


def _read_accessor(reader_name, key):
    @property
    def getter(self):
        accessor = getattr(self, reader_name)
        data = accessor.read()
        return data[key]

    return getter


def write_accessor(**accessors):
    def inner(cls):
        for reader_name, keys in accessors.items():
            for key in keys:
                setattr(cls, key, _write_accessor(reader_name, key))

        return cls
    return inner


def _write_accessor(reader_name, key):
    getter = _read_accessor(reader_name, key)

    def read(self):
        accessor = getattr(self, reader_name)
        return accessor.read()

    def write(self, value):
        accessor = getattr(self, reader_name)
        return accessor.safe_write(value)

    @getter.setter
    def setter(self, value):
        data = read(self)

        if data.get(key) != value:
            data[key] = value
            write(self, data)

    @setter.deleter
    def deleter(self):
        data = read(self)

        if key in data:
            del data[key]
            write(self, data)

    return deleter


@read_accessor(sync=['port'])
class Client:
    def __init__(self, sync_file_path):
        self.sync = Reader(sync_file_path)


@write_accessor(sync=['port'])
class Daemon:
    def __init__(self, sync_file_path):
        self.sync = Writer(sync_file_path)

    @property
    def lock(self):
        return FileLock(self.sync)
