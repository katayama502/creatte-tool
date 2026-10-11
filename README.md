<p align="center">
  <img alt="Creatte Tool" src="assets/brand/creatte-tool-wordmark.svg" width="320">
</p>

<h3 align="center">クリエイティブアプリ12本を、ひとつのランチャーで。</h3>

<p align="center">
  画像編集・イラスト・動画・写真現像・PDF・モーション・レイアウト・文書・スライド・表計算・CAD・音声。<br>
  Creatte Tool は、オープンソースの制作アプリ12本を<b>見つけて・入れて・最新に保つ</b>デスクトップアプリです。
</p>

---

## できること

- **ワンクリックでインストール** — OS と CPU に合ったパッケージ（DMG / MSI / AppImage / .deb / .rpm など）を自動で選び、公開されている SHA-256 チェックサムで検証してからインストールします。
- **アップデートをまとめて管理** — 各アプリの新しいリリースを確認し、インストール済みのアプリを更新します。通知でもお知らせします。
- **いつでもすぐ起動** — 1つのウィンドウ、またはメニューバー / タスクトレイから各アプリを開けます。Rust 製のネイティブアプリ（Electron・WebView 不使用）。
- **日本語 UI** — 日本語・英語・中国語（簡体）・ドイツ語・フランス語・ポルトガル語（ブラジル）・ロシア語。日本語は同梱の M PLUS Rounded 1c で表示するので、追加フォントは不要です。

## 収録アプリ

| Creatte Tool での名前 | 用途 | 元になったオープンソースアプリ |
|---|---|---|
| Creatte Photo | 画像編集 | PhotoCraft |
| Creatte Vector | ベクターイラスト | VectorCraft |
| Creatte Film | 動画編集・カラー・サウンド | FilmCraft |
| Creatte Light | 写真ライブラリと RAW 現像 | LightCraft |
| Creatte PDF | PDF の閲覧・整理・保護 | PdfCraft |
| Creatte Effect | モーショングラフィックスと VFX | EffectCraft |
| Creatte Layout | ページレイアウトと出版 | DesignCraft |
| Creatte Write | 文章作成とドキュメントデザイン | WordCraft |
| Creatte Deck | プレゼンテーション | DeckCraft |
| Creatte Sheet | 表計算とデータ | GridCraft |
| Creatte CAD | CAD 設計・製図 | CADCraft |
| Creatte Sound | 音声の録音・編集・ミックス | SoundCraft |

各アプリの多くは開発初期（アルファ）段階です。アプリ本体は既定で各アップストリームの GitHub Releases から取得するため、起動したアプリ自体には元の名前が表示されます（下の「アプリ本体もリブランドする」を参照）。

## ビルド

Rust 1.90 以上が必要です。

```sh
cargo run -p creatte-tool --release          # デスクトップ版を起動
cargo test --workspace                       # テスト
packaging/macos/package.sh                   # macOS (.app / .dmg)。署名・公証には Apple Developer ID が必要
packaging/windows/package.ps1                # Windows (.msi)
packaging/linux/package.sh                   # Linux (.deb / .rpm / AppImage)
```

アイコンを作り直すときは `packaging/icons.sh`（`pip install fonttools cairosvg` が必要）。

## ブランドと接続先の設定

ブランドに関わる設定は [`crates/core/src/catalog.rs`](crates/core/src/catalog.rs) の **Branding** セクションにまとまっています。

| 定数 | 内容 | 既定値 |
|---|---|---|
| `WEBSITE_URL` | 公式サイト（販売ページ） | GitHub リポジトリ |
| `COMMUNITY_URL` | お問い合わせ先 | GitHub Issues |
| `SOCIAL` | SNS アカウント | なし |
| `apps_owner!()` | アプリ本体のダウンロード元（GitHub の owner） | `storytold`（アップストリーム） |
| `LAUNCHER_REPO` | Creatte Tool 自身の自動アップデート元 | `katayama502/creatte-tool` |

### アプリ本体もリブランドする

12本のアプリ本体も Creatte 名義で配布したい場合は、各リポジトリ（`github.com/storytold/<app>`）をフォークし、名前・アイコン・商標ファイルを差し替えてビルドし、同じアセット名で自分の GitHub Releases に公開してから、`apps_owner!()` を自分の organization に変更します。

### リリースフィード

アップストリームが運営するリリース情報 API は、第三者のサービスなので既定で**無効**にしてあります（GitHub のみを使用）。自前のフィードを用意した場合は `feed::FEED_URL` か環境変数 `CREATTE_TOOL_FEED_URL` で指定できます。

## セキュリティ

- ダウンロード元は各アプリの GitHub Releases に限定し、`SHA256SUMS.txt` で検証してからインストールします。
- ネットワークから受け取るデータはすべて信頼しない前提で扱います（サイズ上限・`unwrap` 禁止・`unsafe` 禁止）。
- 管理者権限が必要な操作は、実行前に必ずユーザーに伝えます。

## ライセンスとクレジット

Creatte Tool は [ArtCraft Launcher](https://github.com/storytold/craft-launcher)（© 2026 ArtCraft Team and contributors）をフォークして改変したもので、同じ **MIT OR Apache-2.0** で配布します。改変内容と第三者素材は [`NOTICE`](NOTICE) と [`ATTRIBUTION.md`](ATTRIBUTION.md) を参照してください。

ArtCraft の名称・ロゴ・「A」マークは ArtCraft Team の商標で、Creatte Tool には含まれていません。Creatte Tool は独立した製品であり、ArtCraft Team とは提携・承認の関係にありません。

<sub>Adobe, Photoshop, Illustrator, Premiere Pro, Lightroom, Acrobat, After Effects and InDesign are either registered trademarks or trademarks of Adobe in the United States and/or other countries. Microsoft, Word, PowerPoint and Excel are trademarks of the Microsoft group of companies. Autodesk and AutoCAD are registered trademarks or trademarks of Autodesk, Inc. Avid and Pro Tools are trademarks or registered trademarks of Avid Technology, Inc. These names are used only to describe what each app is for; Creatte Tool is not affiliated with, sponsored by or endorsed by any of these companies.</sub>
