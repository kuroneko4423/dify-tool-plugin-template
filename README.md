# Dify Tool Plugin テンプレート

Dify Tool Plugin 開発用のテンプレートプロジェクトです。  
`TODO` コメントの箇所を変更するだけで、独自の Tool Plugin を素早く作成できます。

## クイックスタート

### 1. Dify Plugin CLI のインストール

**macOS（Homebrew）** ※推奨

```bash
brew tap langgenius/dify
brew install dify
dify version
```

**macOS ARM（M系チップ）手動インストール**

```bash
curl -LO https://github.com/langgenius/dify-plugin-daemon/releases/latest/download/dify-plugin-darwin-arm64
chmod +x dify-plugin-darwin-arm64
sudo mv dify-plugin-darwin-arm64 /usr/local/bin/dify
dify version
```

**macOS Intel 手動インストール**

```bash
curl -LO https://github.com/langgenius/dify-plugin-daemon/releases/latest/download/dify-plugin-darwin-amd64
chmod +x dify-plugin-darwin-amd64
sudo mv dify-plugin-darwin-amd64 /usr/local/bin/dify
dify version
```

**Linux（amd64）**

```bash
curl -LO https://github.com/langgenius/dify-plugin-daemon/releases/latest/download/dify-plugin-linux-amd64
chmod +x dify-plugin-linux-amd64
sudo mv dify-plugin-linux-amd64 /usr/local/bin/dify
dify version
```

**Windows**

[GitHub Releases](https://github.com/langgenius/dify-plugin-daemon/releases) から `dify-plugin-windows-amd64.exe` をダウンロードし、パスの通ったディレクトリに `dify.exe` として配置してください。

```powershell
dify version
```

> `dify version` でバージョンが表示されればインストール成功です。

### 2. テンプレートのカスタマイズ

プロジェクト内の `TODO` コメントを検索して、順に変更してください。

```bash
grep -rn "TODO" --include="*.yaml" --include="*.py" --include="*.md" .
```

**最低限変更が必要なファイル:**

| ファイル | 変更内容 |
|----------|----------|
| `manifest.yaml` | プラグイン名、作者名、説明 |
| `provider/my_tool.yaml` | プロバイダー名、タグ、認証情報の定義 |
| `provider/my_tool.py` | 認証検証ロジックの実装 |
| `tools/my_tool.yaml` | ツール名、パラメータ定義、LLM向け説明 |
| `tools/my_tool.py` | ツールの実装（API呼び出しロジック） |

> **ファイル名の変更**: `my_tool` の部分をプラグイン名に合わせてリネームし、
> YAML 内のパス参照（`source:` や `tools:` セクション）も一致させてください。

### 3. ローカルで実行

```bash
# venv の作成と有効化
python3 -m venv .venv

# macOS / Linux
source .venv/bin/activate

# Windows (PowerShell)
# .venv\Scripts\Activate.ps1

# Windows (コマンドプロンプト)
# .venv\Scripts\activate.bat

# 依存パッケージのインストール
pip install -r requirements.txt

# .env ファイルの設定
cp .env.example .env
# .env を編集してデバッグキー等を設定

# プラグインの起動
python -m main

# 終了後、venv を無効化する場合
deactivate
```

### 4. デバッグ接続

1. Dify の **プラグイン管理** → **プラグインのデバッグ** を開く
2. 表示されるリモートサーバーアドレスとデバッグキーをコピー
3. `.env` ファイルに設定：

```env
INSTALL_METHOD=remote
REMOTE_INSTALL_HOST=<コピーしたアドレス>
REMOTE_INSTALL_PORT=5003
REMOTE_INSTALL_KEY=<コピーしたキー>
```

4. `python -m main` で起動すると、Dify のプラグイン画面に表示されます

### 5. パッケージング

```bash
# プラグインの親ディレクトリで実行
cd ..
dify plugin package ./dify-tool-plugin-template

# → dify-tool-plugin-template.difypkg が生成される
```

生成された `.difypkg` ファイルを Dify のプラグイン管理画面からアップロードしてインストールできます。

### 6. 署名とインストール

Dify はデフォルトで **プラグインの署名検証** が有効になっています。
Marketplace 以外のプラグインをインストールするには、以下のいずれかの対応が必要です。

#### 方法 A: 署名検証を無効化する（開発・テスト向け）

Dify の `/docker/.env` に以下を追加して再起動します。

```env
FORCE_VERIFYING_SIGNATURE=false
```

```bash
cd docker
docker compose down
docker compose up -d
```

> ⚠️ セキュリティ上、本番環境では署名検証を有効にしておくことを推奨します。

#### 方法 B: サードパーティ署名を使う（本番向け・Community Edition のみ）

自前の鍵ペアでプラグインに署名し、Dify 側に公開鍵を登録する方法です。
Marketplace を経由せずに、安全にプラグインを配布・インストールできます。

**1. 鍵ペアの生成**

```bash
openssl genrsa -out my_key.private.pem 2048
openssl rsa -in my_key.private.pem -pubout -out my_key.public.pem
```

**2. プラグインに署名**

```bash
# パッケージング済みの .difypkg に署名
dify signature sign my_plugin.difypkg -p my_key.private.pem

# → my_plugin.signed.difypkg が同じディレクトリに生成される
```

**3. 署名の検証（任意）**

```bash
dify signature verify my_plugin.signed.difypkg -p my_key.public.pem
```

> `-p` を省略すると Marketplace の公開鍵で検証されます。
> Marketplace 以外のプラグインでは必ず自分の公開鍵を指定してください。

**4. Dify 側に公開鍵を登録**

公開鍵ファイルを plugin_daemon のボリュームに配置します。

```bash
# 公開鍵をコピー
mkdir -p docker/volumes/plugin_daemon/public_keys
cp my_key.public.pem docker/volumes/plugin_daemon/public_keys/
```

`docker/.env`（または `docker-compose.yaml`）に以下の環境変数を設定します。

```yaml
# docker-compose.yaml の plugin_daemon サービス
services:
  plugin_daemon:
    environment:
      FORCE_VERIFYING_SIGNATURE: "true"
      THIRD_PARTY_SIGNATURE_VERIFICATION_ENABLED: "true"
      THIRD_PARTY_SIGNATURE_VERIFICATION_PUBLIC_KEYS: /app/storage/public_keys/my_key.public.pem
```

> `docker/volumes/plugin_daemon` はコンテナ内の `/app/storage` にマウントされます。
> パスがコンテナ内のパスと一致していることを確認してください。

Dify を再起動すれば、署名済みプラグイン（`.signed.difypkg`）をインストールできるようになります。

```bash
cd docker
docker compose down
docker compose up -d
```

> ⚠️ この機能は **Dify Community Edition** でのみ利用可能です。Cloud Edition では現在サポートされていません。

#### 方法 C: Marketplace に公開する

[dify-plugins リポジトリ](https://github.com/langgenius/dify-plugins) に PR を提出して
Marketplace に掲載されると、正規の Marketplace 署名が自動的に付与されます。

## ディレクトリ構造

```
dify-tool-plugin-template/
├── _assets/
│   └── icon.svg                 # プラグインアイコン（SVG）
├── provider/
│   ├── my_tool.yaml             # プロバイダー定義（認証情報など）
│   ├── my_tool.py               # プロバイダーの認証検証コード
│   └── __init__.py
├── tools/
│   ├── my_tool.yaml             # ツール定義（パラメータ、説明）
│   ├── my_tool.py               # ツール実行コード
│   └── __init__.py
├── main.py                      # エントリーポイント
├── manifest.yaml                # プラグイン全体の設定
├── requirements.txt             # Python 依存パッケージ
├── .env.example                 # デバッグ設定テンプレート
├── .difyignore                  # パッケージング除外設定
├── .gitignore
└── README.md
```

## ツールの追加方法

ひとつのプロバイダーに複数のツールを追加できます。

1. `tools/` に新しい YAML ファイルと Python ファイルを作成
2. `provider/my_tool.yaml` の `tools:` セクションに YAML パスを追記

```yaml
# provider/my_tool.yaml
tools:
  - tools/my_tool.yaml
  - tools/another_tool.yaml       # ← 追加
```

## 返却メッセージの種類

ツールの `_invoke` メソッドで使える返却メソッド一覧:

| メソッド | 用途 |
|---------|------|
| `self.create_text_message(text)` | テキストを返す |
| `self.create_json_message(data)` | JSON データを返す |
| `self.create_blob_message(blob, meta)` | バイナリデータ（画像等）を返す |
| `self.create_link_message(link)` | リンクを返す |
| `self.create_image_message(url)` | 画像URLを返す |

## パラメータの型一覧

| type | 説明 |
|------|------|
| `string` | テキスト |
| `number` | 数値（min / max 指定可） |
| `boolean` | 真偽値 |
| `select` | ドロップダウン選択（options で選択肢定義） |
| `secret-input` | 暗号化入力（APIキー等の機密情報） |
| `file` | 単一ファイル |
| `files` | 複数ファイル |
| `model-selector` | モデル選択 |
| `app-selector` | アプリケーション選択 |

## 利用可能なタグ

`search`, `image`, `videos`, `weather`, `finance`, `design`, `travel`,
`social`, `news`, `medical`, `productivity`, `education`, `business`,
`entertainment`, `utilities`, `other`

## トラブルシューティング

### 署名検証エラー

```
PluginDaemonBadRequestError: plugin verification has been enabled, and the plugin you want to install has a bad signature
```

「6. 署名とインストール」セクションを参照してください。開発時は `FORCE_VERIFYING_SIGNATURE=false` が最も手軽です。

### プラグイン起動時に FileNotFoundError

```
FileNotFoundError: [Errno 2] No such file or directory: '.../<name>.py'
```

各 YAML ファイルの `extra.python.source` が **プラグインルートからの相対パス** になっているか確認してください。

```yaml
# ❌ NG — ファイル名のみ
extra:
  python:
    source: my_tool.py

# ✅ OK — ディレクトリを含むパス
extra:
  python:
    source: provider/my_tool.py    # プロバイダーの場合
    source: tools/my_tool.py       # ツールの場合
```

> 本テンプレートでは正しいパスを設定済みですが、ファイルをリネーム・移動した際は YAML 側も忘れずに更新してください。

### maximum recursion depth exceeded

```
ValueError: Error loading plugin configuration: Failed to load YAML file manifest.yaml: maximum recursion depth exceeded
```

エントリーポイント（`manifest.yaml` の `entrypoint`）と、プロバイダー/ツールの `extra.python.source` で指定するファイル名が **衝突** すると再帰ロードが発生します。

- エントリーポイントは `main` （= `main.py`）のまま変更しない
- `source` パスには必ずディレクトリを含める（例: `provider/my_tool.py`）

### パッケージサイズ超過

```
ERROR failed to package plugin error="Plugin package size is too large."
```

`.difyignore` に `venv/` や不要ファイルを追加してください。本テンプレートにはデフォルトの `.difyignore` が含まれています。

```
.venv/
venv/
__pycache__/
*.pyc
*.difypkg
.env
.git/
```

### デバッグ接続が切れる / handshake failed

```
handshake failed, invalid key
```

Dify のデバッグキー（`REMOTE_INSTALL_KEY`）は定期的に更新されます。Dify のプラグインデバッグ画面から最新のキーをコピーし、`.env` を更新してください。

### pip install で dify_plugin が見つからない

```
ERROR: No matching distribution found for dify_plugin
```

Python 3.12 以上が必要です。バージョンを確認してください。

```bash
python3 --version  # 3.12 以上であること
```

また、venv を有効化してからインストールしているか確認してください。

### バイナリファイルアップロード時の接続エラー

`Upload File (File Variable)` ツールで接続エラーが発生する場合、Dify の Docker 環境における内部ネットワーク設定が原因です。

#### `[Errno 110] Connection timed out`

**原因**: プラグインコンテナから Dify の外部 URL（`FILES_URL` に設定された IP アドレス）に到達できません。

**対処法**: Dify の `.env` に `INTERNAL_FILES_URL` を設定してください。

```bash
# Dify の docker/.env に追加
INTERNAL_FILES_URL=http://api:5001
```

設定後、Dify を再起動してください。

```bash
docker compose down && docker compose up -d
```

> **背景**: Dify はファイルの URL を `FILES_URL`（例: `http://192.168.1.101:8082`）から生成しますが、プラグインコンテナからこの外部 IP には到達できません。本プラグインは `INTERNAL_FILES_URL` 環境変数を読み取り、ファイル取得先を Docker 内部ネットワークのサービス名（`api:5001`）に自動書き換えします。

#### `Server error '503 Service Unavailable'`

**原因**: SSRF プロキシ経由でプライベート IP（`192.168.x.x` 等）にアクセスしようとして、プロキシにブロックされています。

**対処法**: 上記の `INTERNAL_FILES_URL` を設定してください。本プラグインは Dify 内部ファイルのダウンロード時に SSRF プロキシをバイパスする設計になっています。

#### `[Errno 111] Connection refused`

**原因**: `INTERNAL_FILES_URL` に設定したホスト/ポートが正しくありません。

**対処法**: 以下の値を試してください。

| 設定値 | 説明 |
|--------|------|
| `http://api:5001` | Dify API サーバー直接（推奨） |
| `http://nginx:80` | nginx 経由（環境によってはポートが異なる場合あり） |

API サーバーが port 5001 でリッスンしていることは、Dify のログで確認できます。

```
api-1 | Listening at: http://0.0.0.0:5001
```

#### `storageQuotaExceeded` (403)

**原因**: サービスアカウントにはストレージクォータがないため、個人ドライブへのアップロードが拒否されています。

**対処法**: Google Workspace の共有ドライブ（Shared Drive）のフォルダを使用してください。

1. [Google Workspace](https://workspace.google.com/) のアカウントで [Google Drive](https://drive.google.com) にアクセス
2. 左メニューの「共有ドライブ」→「新しい共有ドライブ」を作成
3. 作成した共有ドライブで「メンバーを管理」を開き、サービスアカウントのメールアドレス（`xxx@xxx.iam.gserviceaccount.com`）を**コンテンツ管理者**以上の権限で追加
4. 共有ドライブ内にアップロード先フォルダを作成
5. フォルダの URL（`https://drive.google.com/drive/folders/<FOLDER_ID>`）から **フォルダ ID** を取得
6. Dify のプラグイン設定で `Default Folder ID` に設定、またはワークフローのツールパラメータ `folder_id` に指定

> **注意**: 無料の Google アカウントでは共有ドライブを作成できません。Google Workspace（Business Starter 以上）が必要です。

### 認証エラー

```
Failed to validate Google Drive credentials: ...
```

- Google Cloud Console で **Google Drive API** が有効になっているか確認
- JSON キーファイルの内容が正しくコピーされているか確認（先頭の `{` から末尾の `}` まで）
- サービスアカウントのキーが失効していないか確認

### 権限エラー

```
The caller does not have permission
```

- 操作対象のフォルダがサービスアカウントのメールアドレスに共有されているか確認
- 共有権限が「閲覧者」ではなく「**編集者**」になっているか確認
- 共有ドライブの場合、サービスアカウントがメンバーとして追加されているか確認

### Google Workspace ファイルの読み取りが期待通りにならない

Google Workspace ファイルは自動的にエクスポートされます:

| Google Workspace タイプ | エクスポート形式 |
|-------------------------|------------------|
| Google ドキュメント | プレーンテキスト |
| Google スプレッドシート | CSV |
| Google スライド | プレーンテキスト |
| Google 図形描画 | PNG（バイナリとして返却） |

- 書式やレイアウト情報はエクスポート時に失われます
- Google スプレッドシートは最初のシートのみがエクスポートされます

### プロキシ関連の接続エラー

```
Error uploading file: ... | Proxy env vars: {...}
```

- Dify の Docker 環境でプロキシが設定されている場合、プラグインは自動的にプロキシを検出します
- プロキシ検出の対象環境変数: `HTTPS_PROXY`, `HTTP_PROXY`, `SSRF_PROXY_HTTPS_URL`, `SSRF_PROXY_HTTP_URL`, `SANDBOX_HTTPS_PROXY`, `SANDBOX_HTTP_PROXY`
- エラーメッセージに含まれる `Proxy env vars` の内容を確認し、プロキシ設定が正しいか確認してください
- プロキシサーバーが `https://www.googleapis.com` へのアクセスを許可しているか確認してください

## 参考リンク

- [Dify Plugin 公式ドキュメント](https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/cheatsheet)
- [Tool Plugin 開発ガイド](https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/tool-plugin)
- [プラグイン署名ガイド](https://docs.dify.ai/en/plugins/publish-plugins/signing-plugins-for-third-party-signature-verification)
- [Dify Plugin SDK (Python)](https://github.com/langgenius/dify-plugin-sdks)
- [Dify 公式プラグイン集](https://github.com/langgenius/dify-official-plugins)
- [Plugin CLI Releases](https://github.com/langgenius/dify-plugin-daemon/releases)
- [Dify Marketplace](https://marketplace.dify.ai/)
