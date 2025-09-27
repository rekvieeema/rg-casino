"""Lightweight TON client integrations used by the casino."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import httpx


@dataclass(slots=True)
class TonTransferRequest:
    """Parameters required to initiate a TON transfer."""

    wallet_address: str
    amount: float
    payload: Optional[str] = None


@dataclass(slots=True)
class TonTransferResult:
    """Result of a TON transfer attempt."""

    success: bool
    tx_hash: Optional[str] = None
    error: Optional[str] = None


class TonClient:
    """Wrapper around TON Center API (or compatible) for deposits and withdrawals."""

    def __init__(self, api_key: str | None, network: str = "mainnet") -> None:
        self._api_key = api_key
        self._network = network
        self._base_url = "https://toncenter.com/api/v2"
        if network == "testnet":
            self._base_url = "https://testnet.toncenter.com/api/v2"
        self._client = httpx.AsyncClient(base_url=self._base_url, timeout=20.0)

    async def close(self) -> None:
        """Close the underlying HTTP client."""

        await self._client.aclose()

    async def get_wallet_info(self, address: str) -> Dict[str, Any]:
        """Fetch wallet balance and status information from TON Center."""

        params = {"address": address}
        if self._api_key:
            params["api_key"] = self._api_key
        response = await self._client.get("/getAddressInformation", params=params)
        response.raise_for_status()
        payload = response.json()
        if not payload.get("ok"):
            raise RuntimeError(f"TON API error: {payload}")
        return payload["result"]

    async def send_transfer(self, request: TonTransferRequest) -> TonTransferResult:
        """Initiate a transfer using the Highload wallet interface."""

        payload = {
            "to_address": request.wallet_address,
            "amount": int(request.amount * 1_000_000_000),  # convert TON to nanotons
        }
        if request.payload:
            payload["payload"] = request.payload
        if self._api_key:
            payload["api_key"] = self._api_key

        response = await self._client.post("/sendBocReturnHash", json=payload)
        try:
            response.raise_for_status()
            body = response.json()
        except httpx.HTTPError as exc:  # pragma: no cover - network failure
            return TonTransferResult(success=False, error=str(exc))

        if not body.get("ok"):
            return TonTransferResult(success=False, error=str(body))
        return TonTransferResult(success=True, tx_hash=body.get("result"))


__all__ = ["TonClient", "TonTransferRequest", "TonTransferResult"]
