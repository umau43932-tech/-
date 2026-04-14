# Python ファイル整理アプリ

フォルダ内のファイルを拡張子ベースで自動振り分けするCLIアプリです。

## 機能
- 画像 / 動画 / 音声 / ドキュメント / 圧縮ファイル / コード / その他 に分類
- 同名ファイルがある場合は `*_1`, `*_2` のようにリネームして保存
- `--dry-run` で移動せずに実行結果を確認
- `--recursive` でサブフォルダ配下も対象に整理

## 使い方
```bash
python3 file_organizer.py /path/to/target
```

### オプション
```bash
python3 file_organizer.py /path/to/target --dry-run
python3 file_organizer.py /path/to/target --recursive
```

## 分類先フォルダ
- `images`
- `videos`
- `audio`
- `documents`
- `archives`
- `code`
- `others`
- `no_extension`
