from dataclasses import dataclass


@dataclass(frozen=True)
class HudsonHousekeeperQuery:
    id: int
    name: str


@dataclass(frozen=True)
class HudsonHousekeeperResponse:
    id: int
    name: str


MrsHudsonHousekeeperQuery = HudsonHousekeeperQuery
MrsHudsonHousekeeperResponse = HudsonHousekeeperResponse
