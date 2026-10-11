# Creatte Tool — セキュリティレビュー（リブランド時）

対象: ArtCraft Launcher v0.2.1 からのフォークと、Creatte Tool としての改変一式。観点: OWASP Top 10、認証・認可、入力検証、機密情報の管理。

| 観点 | 状態 | 内容 |
|---|---|---|
| A08 ソフトウェアとデータの整合性 | OK | アプリは `github.com/<APPS_OWNER>/<app>/releases` からのみ取得し、`SHA256SUMS.txt` と照合してからインストール（上流の仕組みをそのまま維持）。 |
| A10 SSRF／外部接続先 | 改善 | 上流企業のリリースフィード API（第三者サービス）を既定で無効化し、GitHub のみに。`CREATTE_TOOL_FEED_URL` は `https://` かループバックだけを受け付ける。 |
| A03 インジェクション／入力検証 | OK | ネットワーク入力はサイズ上限つきで扱い、本番コードで `unwrap`・`panic` を禁止、`unsafe` 禁止（clippy で強制、警告 0）。 |
| A01 アクセス制御／権限 | OK | 管理者権限が必要な操作は事前に表示（Windows はユーザー単位インストールで昇格不要）。 |
| A05 設定ミス | 改善 | MSI の UpgradeCode とコンポーネント GUID を新規発行し、上流製品と取り違えて上書きしないようにした。アプリ ID は `jp.creatte.creatte-tool`。 |
| 機密情報 | OK | リポジトリにトークン・鍵・パスワードなし（スキャン済み）。署名鍵は GitHub Secrets 経由のみ。未設定時は未署名ビルドになる。 |
| 自己アップデート元 | 要対応 | `katayama502/creatte-tool` のリリースを参照。リポジトリ作成前は更新確認が失敗するだけで、他人のバイナリは取得しない。 |
| 販売サイト | OK | 静的ページ。フォームなし、外部スクリプトなし（Google Fonts のみ）、外部リンクは `rel="noopener"`。 |

テスト: `cargo test --workspace` で 1 件を除きすべて成功。失敗する `process::tests::running_paths_are_matched_literally` は、改変前の上流でも同じ環境で失敗する、コンテナ環境依存のテスト。
