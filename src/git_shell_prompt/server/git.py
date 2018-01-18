import collections
import contextlib
import pathlib

import dulwich.errors
import dulwich.porcelain
import dulwich.repo


def non_repo_info() -> dict:
    return {
        'is_git': False,
    }


def local_info(repo) -> dict:
    root = pathlib.Path(repo.path).resolve()

    staged, unstaged, untracked = dulwich.porcelain.status(repo)

    modifications = deletions = False

    for path in unstaged:
        if isinstance(path, bytes):
            path = path.decode('utf-8')

        # An addition must be staged to be tracked
        if (root / path).exists():
            modifications = True
        else:
            deletions = True

    ready = any(staged.values()) and not (unstaged or untracked)

    try:
        refs, stash = repo.refs.follow(b'refs/stash')
    except KeyError:
        stash = None

    return {
        'has_stashes': stash is not None,
        'has_untracked': bool(untracked),
        'has_modifications': modifications,
        'has_deletions': deletions,
        'has_additions': bool(staged['add']),
        'has_cached_modifications': bool(staged['modify']),
        'has_cached_deletions': bool(staged['delete']),
        'ready_to_commit': ready,
    }


def repo_info(repo):
    root = pathlib.Path(repo.path)

    with contextlib.closing(repo):
        full = {
            'is_git': True,

            'repo': {
                'root': repo.path,
                'name': root.name,
            },

            'local': local_info(repo),

            'remote': {
                # 'needs_merge': None,
                # 'can_fast_forward': None,
                # 'has_diverged': None,
                # 'not_tracked_branch': None,
                # 'rebase_tracking': None,
                # 'merge_tracking': None,
                # 'should_push': None,
                # 'has_stashes': None,
            },
        }
        return full


def rel_path(root, path):
    pth_root = pathlib.Path(root)
    pth_path = pathlib.Path(path)

    relative = str(
        pth_path.relative_to(pth_root)
    )

    if not relative.startswith('..'):
        return relative

    relative = str(
        pth_path.resolve().relative_to(pth_root.resolve())
    )

    if not relative.startswith('..'):
        return relative

    return path


async def get_info(path):
    common = {
        'path': str(pathlib.Path(path).resolve()),
    }

    try:
        repo = dulwich.repo.Repo.discover(path)
    except dulwich.errors.NotGitRepository:
        maps = [non_repo_info()]
    else:
        maps = [
            repo_info(repo),
            {'rel': rel_path(repo.path, path)},
        ]

    return collections.ChainMap(*maps, common)
