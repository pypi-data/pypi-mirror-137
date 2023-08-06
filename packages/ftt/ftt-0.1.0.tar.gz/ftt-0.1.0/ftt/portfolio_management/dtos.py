from dataclasses import dataclass
from typing import Optional

import pandas as pd


@dataclass
class PortfolioAllocationDTO:
    weights: Optional[dict[str, float]] = None
    allocation: Optional[dict[str, float]] = None
    leftover: Optional[float] = None
    expected_annual_return: Optional[float] = None
    annual_volatility: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    cov_matrix: Optional[pd.DataFrame] = None
