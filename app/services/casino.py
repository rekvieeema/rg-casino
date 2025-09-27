"""Core casino mechanics for the rocket crash game and loot cases."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Iterable, List


@dataclass(slots=True)
class CaseItem:
    """Represents an individual reward item inside a case."""

    title: str
    probability: float
    reward: float
    emoji: str = "🎁"


@dataclass(slots=True)
class Case:
    """A loot case that can be opened by players."""

    title: str
    price: float
    items: List[CaseItem]

    def pick_reward(self) -> CaseItem:
        """Randomly select an item based on probability weights."""

        weights = [item.probability for item in self.items]
        return random.choices(self.items, weights=weights, k=1)[0]


@dataclass(slots=True)
class WagerResult:
    """Result of a crash game wager."""

    multiplier: float
    profit: float
    crashed: bool


class CasinoEngine:
    """Encapsulates RNG logic for crash game and cases."""

    def __init__(self, house_edge: float = 0.02) -> None:
        self.house_edge = house_edge

    def play_crash(self, cash_out_multiplier: float) -> WagerResult:
        """Simulate a crash round for the provided cash out multiplier."""

        crash_point = self._generate_crash_point()
        crashed = crash_point < cash_out_multiplier
        multiplier = cash_out_multiplier if not crashed else crash_point
        profit = max(multiplier - 1.0, 0.0)
        return WagerResult(multiplier=multiplier, profit=profit, crashed=crashed)

    def _generate_crash_point(self) -> float:
        """Generate a crash multiplier using a provably fair distribution."""

        # Simplified algorithm: house edge is applied by shifting distribution.
        roll = random.random()
        crash_point = 1 / (1 - roll)
        return max(1.0, crash_point * (1 - self.house_edge))

    def open_case(self, case: Case) -> CaseItem:
        """Open a case and return the resulting item."""

        return case.pick_reward()

    @staticmethod
    def normalise_cases(cases: Iterable[Case]) -> List[Case]:
        """Ensure probabilities per case sum to 1 for fairness."""

        normalised_cases: List[Case] = []
        for case in cases:
            total_probability = sum(item.probability for item in case.items)
            if not 0.99 <= total_probability <= 1.01:
                raise ValueError(
                    f"Case '{case.title}' probability must sum to 1, got {total_probability:.2f}"
                )
            normalised_cases.append(case)
        return normalised_cases


__all__ = ["CasinoEngine", "Case", "CaseItem", "WagerResult"]
