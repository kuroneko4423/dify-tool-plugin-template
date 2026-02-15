"""
ツール実装テンプレート

Tool クラスを継承し、_invoke メソッドを実装します。
外部APIを呼び出して結果を返す処理をここに記述してください。

TODO:
  1. クラス名を変更（例: MyTool → GoogleSearchTool）
  2. _invoke メソッド内のロジックを実装
"""

from collections.abc import Generator
from typing import Any

import requests

from dify_plugin import Tool
from dify_plugin.entities.tool import ToolInvokeMessage


class MyTool(Tool):
    """
    ツールのメインクラス。

    _invoke メソッドで外部APIを呼び出し、結果を yield で返します。

    利用可能な返却メソッド:
      self.create_text_message(text)          — テキストを返す
      self.create_json_message(data)          — JSON データを返す
      self.create_blob_message(blob, meta)    — バイナリ（画像等）を返す
      self.create_link_message(link)          — リンクを返す
      self.create_image_message(image_url)    — 画像URLを返す
    """

    def _invoke(
        self, tool_parameters: dict[str, Any]
    ) -> Generator[ToolInvokeMessage]:
        # =====================================================================
        # 1. パラメータの取得
        # =====================================================================
        query = tool_parameters["query"]
        max_results = tool_parameters.get("max_results", 5)

        # =====================================================================
        # 2. 認証情報の取得
        # =====================================================================
        # provider YAML の credentials_for_provider で定義した変数名を使用
        api_key = self.runtime.credentials.get("api_key", "")
        if not api_key:
            yield self.create_text_message("Error: API Key is not configured.")
            return

        # =====================================================================
        # 3. 外部API呼び出し
        # =====================================================================
        try:
            # TODO: 実際のAPI呼び出しに置き換えてください
            #
            # response = requests.get(
            #     "https://api.example.com/v1/search",
            #     params={
            #         "q": query,
            #         "limit": max_results,
            #     },
            #     headers={
            #         "Authorization": f"Bearer {api_key}",
            #     },
            #     timeout=30,
            # )
            # response.raise_for_status()
            # result = response.json()

            # --- サンプル: ダミーレスポンス（実装時に削除） ---
            result = {
                "query": query,
                "max_results": max_results,
                "results": [
                    {
                        "title": "Sample Result",
                        "url": "https://example.com",
                        "snippet": "This is a sample result from the template.",
                    }
                ],
                "message": "TODO: Replace this with actual API response.",
            }

        except requests.Timeout:
            yield self.create_text_message("Error: Request timed out.")
            return
        except requests.ConnectionError:
            yield self.create_text_message("Error: Failed to connect to the API.")
            return
        except requests.HTTPError as e:
            yield self.create_text_message(f"Error: API returned {e.response.status_code}.")
            return
        except Exception as e:
            yield self.create_text_message(f"Error: {str(e)}")
            return

        # =====================================================================
        # 4. 結果を返す
        # =====================================================================
        # JSON で返す場合:
        yield self.create_json_message(result)

        # テキストで返す場合:
        # yield self.create_text_message("結果のテキスト")

        # 画像を返す場合:
        # yield self.create_image_message("https://example.com/image.png")

        # バイナリ（画像等）を返す場合:
        # yield self.create_blob_message(
        #     blob=image_bytes,
        #     meta={"mime_type": "image/png"},
        # )
