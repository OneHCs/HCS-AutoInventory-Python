from dataclasses import dataclass

@dataclass
class StoreDTO:
    stores: dict
    zone: int
    