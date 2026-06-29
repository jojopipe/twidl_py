#!/usr/bin/env python3
# coding: utf-8

import argparse
import os
import yt_dlp

def download_urls(urls: list, target: str):
    ydl_opts = {
        "cookiesfrombrowser": ("firefox",),
        "outtmpl": f"{target}/%(id)s.%(ext)s",
    }
    info_file = target + "/info.txt"
    print(info_file)
    ydl = yt_dlp.YoutubeDL(ydl_opts)
    for url in urls:
        if not url:
            continue
        try:
            ydl.download([url])
            info = ydl.extract_info(url, download = False)
            with open(info_file, "a+") as f:
                f.write(str(info) + "\n")
        except Exception as e:
            if isinstance(e, yt_dlp.utils.ExtractorError):
                continue
    # TODO: add post info to seperate file (use extractor)
    ydl.close()

    return

def create_target(target: str):
    target_dir = target + ".d"
    os.makedirs(target_dir, mode = 511, exist_ok = True)
    # _ = open(target_dir + "/info.txt", "w+") # create file
    return target_dir

def urls_from_file(file: str) -> list:
    urls = []
    with open(file, "r") as f:
        urls = f.read().splitlines()
    return urls

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()

    urls = urls_from_file(args.file)
    target = create_target(args.file)
    download_urls(urls, target)

if __name__ == "__main__":
    main()
