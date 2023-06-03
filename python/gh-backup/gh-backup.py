import argparse
import json
from getpass import getpass
from pathlib import Path

import httpx
from pygit2 import Keypair, RemoteCallbacks, clone_repository
from tqdm import tqdm


def process_all_pages(url, token):
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    items = []
    page = 1

    while True:
        print(f"  process {page} page ...")
        r = httpx.get(url, params={"page": page}, headers=headers)
        if result := r.json():
            page += 1
            items += result
            continue
        break

    return items


def download_metadata(args):
    if args.token:
        token = args.token.open("r").read().strip()
    else:
        token = getpass("Enter github personal access token: ")

    repos = []
    gists = []

    if args.repos:
        print("Downloading repos metadata...")
        repos = process_all_pages("https://api.github.com/user/repos", token)

    if args.gists:
        print("Downloading gists metadata...")
        gists = process_all_pages("https://api.github.com/gists", token)

    if args.metadata:
        with args.metadata.open("w") as f:
            json.dump({"repos": repos, "gists": gists}, f, indent=1)

    return repos, gists


def clone_repos(items, output, callbacks, repo_name, repo_url):
    pbar = tqdm(items)
    for item in pbar:
        name = repo_name(item)
        url = repo_url(item)
        pbar.set_description(f"  clone {name}")
        path = output / name / ".git"
        if not path.exists():
            path.mkdir(parents=True)
        clone_repository(url, path, bare=True, callbacks=callbacks)


def main():
    parser = argparse.ArgumentParser(description="Github repository backup script")
    parser.add_argument("-s", dest="download", default=True, action="store_false", help="skip clone")
    parser.add_argument("-r", dest="repos", default=False, action="store_true", help="clone repos")
    parser.add_argument("-g", dest="gists", default=False, action="store_true", help="clone gists")
    parser.add_argument("-p", dest="private", type=Path, default=None, help="ssh private key")
    parser.add_argument("-k", dest="public", type=Path, default=None, help="ssh public key")
    parser.add_argument("-t", dest="token", type=Path, default=None, help="load github personal token from file")
    parser.add_argument("-m", dest="metadata", type=Path, default=None, help="write metadata to file")
    parser.add_argument("-o", dest="output", type=Path, default="github-backup", help="clone output directory")
    args = parser.parse_args()

    repos, gists = download_metadata(args)

    if args.download and args.private and args.public:
        password = getpass("Enter passphrase to decrypt ssh key: ")
        credential = Keypair("git", args.public, args.private, password)
        callbacks = RemoteCallbacks(credentials=credential)

        if args.repos:
            print("Start repo clone")
            clone_repos(repos, args.output / "repos", callbacks, lambda i: i["full_name"], lambda i: i["ssh_url"])

        if args.gists:
            print("Start gist clone")
            clone_repos(
                gists,
                args.output / "gists",
                callbacks,
                lambda i: i["id"],
                lambda i: f"git@gist.github.com:{i['id']}.git",
            )


if __name__ == "__main__":
    main()
