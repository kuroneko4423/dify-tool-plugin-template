"""
Tool Provider — 認証情報の検証ロジック

このクラスは、ユーザーがDifyのプラグイン設定画面で認証情報を保存する際に呼ばれます。
外部APIにテストリクエストを送り、認証情報が有効かどうかを検証してください。

TODO:
  1. クラス名を変更（例: MyToolProvider → GoogleSearchProvider）
  2. _validate_credentials メソッド内の検証ロジックを実装
"""

from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError

import requests


class MyToolProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        プロバイダーの認証情報を検証する。

        :param credentials: provider YAML の credentials_for_provider で定義した認証情報
        :raises ToolProviderCredentialValidationError: 検証失敗時
        """
        api_key = credentials.get("api_key", "")
        if not api_key:
            raise ToolProviderCredentialValidationError(
                "API Key is required."
            )

        try:
            # =================================================================
            # TODO: 外部APIにテストリクエストを送って認証情報を検証する
            # =================================================================
            # 例: 軽量なエンドポイントにリクエストして 200 が返るか確認
            #
            # response = requests.get(
            #     "https://api.example.com/v1/health",
            #     headers={"Authorization": f"Bearer {api_key}"},
            #     timeout=10,
            # )
            # if response.status_code in (401, 403):
            #     raise ToolProviderCredentialValidationError(
            #         "Invalid API Key."
            #     )
            # response.raise_for_status()
            pass

        except ToolProviderCredentialValidationError:
            raise
        except requests.ConnectionError:
            raise ToolProviderCredentialValidationError(
                "Failed to connect to the API. Please check your network."
            )
        except Exception as e:
            raise ToolProviderCredentialValidationError(
                f"Credential validation failed: {str(e)}"
            )
