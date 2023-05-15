#!/usr/bin/env python
import os


DEFAULT_EXTENSIONS = [
    ".txt",
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".mp4",
    ".mkv",
    ".m2ts",
    ".ts",
    ".webm",
]


def int_or_none(value: str):
    try:
        return int(value)
    except ValueError:
        # 不正な数値文字列
        return None


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="連番ファイルの欠けを見つけるためのプログラム",
    )
    parser.add_argument(
        "path",
        type=str,
        help="検索対象のディレクトリ",
    )
    parser.add_argument(
        "-x",
        "--extensions",
        type=str,
        nargs="*",
        default=DEFAULT_EXTENSIONS,
        help='許可される拡張子（いずれかに一致）. ".jpg", ".png"のようにドットを含める',
    )
    parser.add_argument(
        "-s",
        "--start",
        type=int,
        default=0,
        help="連番の開始番号（inclusive）",
    )
    parser.add_argument(
        "-t",
        "--step",
        type=int,
        default=1,
        help="連番のステップ数（番号飛ばし）",
    )
    parser.add_argument(
        "-e",
        "--end",
        type=int,
        default=100,
        help="連番の終了番号（inclusive）",
    )
    # parser.add_argument(
    #     '-z',
    #     '--zfill',
    #     type=int,
    #     help='左ゼロ埋めの桁数',
    # )
    args = parser.parse_args()

    path: str = args.path
    extensions: list[str] = args.extensions
    start: int = args.start
    step: int = args.step
    end: int = args.end
    # zfill: int = args.zfill

    if step < 1:
        raise Exception("ステップ数は1以上を指定してください")

    if end < start:
        raise Exception("終了番号は開始番号以上の値を指定してください")

    extension_set = set(map(lambda s: s.lower(), extensions))
    unfound_number_set = set(range(start, end + 1, step))

    files = os.listdir(path)
    for file in files:
        file_path = os.path.join(path, file)

        # ディレクトリは無視
        if not os.path.isfile(file_path):
            continue

        stem, extension = os.path.splitext(file)
        if extension.lower() not in extension_set:
            continue

        stem_int = int_or_none(stem)
        if stem_int is None:
            # 不正な数値文字列
            continue

        if stem_int in unfound_number_set:
            unfound_number_set.remove(stem_int)

    sorted_unfound_number_list = sorted(unfound_number_set)
    print("\n".join(map(str, sorted_unfound_number_list)))


if __name__ == "__main__":
    main()
