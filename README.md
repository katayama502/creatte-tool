<p align="center"><img alt="Creatte Film" src="assets/brand/creatte-film-wordmark.svg" width="300"></p>

<h3 align="center">Creatte Film — 動画編集ソフト</h3>

Creatte Film は、カット編集・カラー調整・テロップ・字幕・音声ミックスまでこなすノンリニア動画編集ソフトです。Creatte Tool に含まれる動画編集アプリを、単体でも使えるようにしたものです。画面は日本語に対応しています。

- 対応：macOS 11 以降（Apple シリコン / Intel）、Windows 10 / 11（64 ビット / ARM）
- 配布ファイル：`creatte-film-<version>-macos-universal.dmg`、`creatte-film-<version>-windows-x64.msi` ほか
- インストール手順：配布 ZIP に同梱の「インストール手順.html」

## ビルド

GitHub Actions の「Build Creatte Film」（`.github/workflows/build.yml`）が、`creatte-film` ブランチへの push のたびに Mac と Windows のインストーラーを作ります。ローカルでは Rust 1.95 以上で `cargo run -p filmcraft --release`。

## ライセンスとクレジット

Creatte Film は [FilmCraft](https://github.com/storytold/filmcraft)（© 2026 ArtCraft Team and the FilmCraft contributors）を改変したもので、同じ **MIT OR Apache-2.0** で配布します。改変内容と第三者素材は [`NOTICE`](NOTICE) と [`ATTRIBUTION.md`](ATTRIBUTION.md) を参照してください。ArtCraft の名称・ロゴは ArtCraft Team の商標で、Creatte Film には含まれていません。
