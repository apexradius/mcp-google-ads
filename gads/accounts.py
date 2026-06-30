import json
import os
from pathlib import Path
from typing import Optional

from google.ads.googleads.client import GoogleAdsClient

_DEFAULT_CONFIG = Path.home() / ".config" / "mcp-google-ads" / "accounts.json"


class AccountError(Exception):
    pass


class AccountManager:
    def __init__(self):
        config_path = os.environ.get("GOOGLE_ADS_ACCOUNTS_CONFIG", str(_DEFAULT_CONFIG))
        path = Path(os.path.expanduser(config_path))
        if not path.exists():
            raise AccountError(
                f"Accounts config not found at {path}. "
                "Set GOOGLE_ADS_ACCOUNTS_CONFIG or create ~/.config/mcp-google-ads/accounts.json"
            )
        self._config = json.loads(path.read_text())
        self._path = path
        self._clients: dict[str, GoogleAdsClient] = {}

    def _account_name(self, account: Optional[str]) -> str:
        name = account or self._config.get("default")
        if not name:
            raise AccountError("No account specified and no default set in config.")
        if name not in self._config.get("accounts", {}):
            available = list(self._config.get("accounts", {}).keys())
            raise AccountError(f"Account '{name}' not found. Available: {available}")
        return name

    def get_client(self, account: Optional[str] = None) -> GoogleAdsClient:
        name = self._account_name(account)
        if name not in self._clients:
            self._clients[name] = self._build_client(name)
        return self._clients[name]

    def _build_client(self, name: str) -> GoogleAdsClient:
        cfg = self._config["accounts"][name]
        developer_token = os.environ.get("GOOGLE_ADS_DEVELOPER_TOKEN", "")
        account_type = cfg.get("type", "oauth")

        if account_type == "service_account":
            return GoogleAdsClient.load_from_dict({
                "developer_token": developer_token,
                "json_key_file_path": os.path.expanduser(cfg["credentials_file"]),
                "impersonated_email": cfg.get("impersonated_email", ""),
                "use_proto_plus": True,
            })
        else:
            # OAuth — requires client_secrets + refresh_token
            token_path = Path(os.path.expanduser(cfg["token_file"]))
            if not token_path.exists():
                raise AccountError(
                    f"Token file not found for account '{name}': {token_path}. "
                    "Run: mcp-google-ads auth <account-name>"
                )
            token_data = json.loads(token_path.read_text())
            return GoogleAdsClient.load_from_dict({
                "developer_token": developer_token,
                "client_id": token_data["client_id"],
                "client_secret": token_data["client_secret"],
                "refresh_token": token_data["refresh_token"],
                "use_proto_plus": True,
            })

    def list_accounts(self) -> list[dict]:
        default = self._config.get("default")
        return [
            {
                "name": name,
                "type": cfg.get("type", "oauth"),
                "is_default": name == default,
            }
            for name, cfg in self._config.get("accounts", {}).items()
        ]

    def set_default(self, account: str) -> None:
        name = self._account_name(account)
        self._config["default"] = name
        self._path.write_text(json.dumps(self._config, indent=2))

    def invalidate(self, account: Optional[str] = None) -> None:
        name = self._account_name(account)
        self._clients.pop(name, None)
