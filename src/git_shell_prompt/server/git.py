import collections
import contextlib
import pathlib

import dulwich.errors
import dulwich.porcelain
import dulwich.repo


def non_repo_info():
    return {
        'is_git': False,
    }


def repo_info(repo):
    root = pathlib.Path(repo.path)

    with contextlib.closing(repo):
        staged, unstaged, untracked = dulwich.porcelain.status(repo)

        return {
            'is_git': True,

            'repo': {
                'root': repo.path,
                'name': root.name,
            },

            'local': {
                'has_untracked': bool(untracked),
                'has_additions': bool(staged['add']),
                'has_deletions': bool(staged['delete']),
                'has_modifications': bool(staged['modify']),
                'has_cached_modifications': bool(staged['modify']),
                'ready_to_commit': staged and not (unstaged or untracked),
                # 'is_on_tag': None,
                # 'detached': None,
            },

            'upstream': {
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


async def get_info(path):
    common = {
        'path': str(pathlib.Path(path).resolve()),
    }

    try:
        repo = dulwich.repo.Repo.discover(path)
    except dulwich.errors.NotGitRepository:
        return collections.ChainMap(non_repo_info(), common)
    else:
        return collections.ChainMap(repo_info(repo), common)
