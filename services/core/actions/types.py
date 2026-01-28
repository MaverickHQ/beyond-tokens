from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PlaceBuy:
    symbol: str
    quantity: float
    price: float


@dataclass(frozen=True)
class PlaceSell:
    symbol: str
    quantity: float
    price: float
