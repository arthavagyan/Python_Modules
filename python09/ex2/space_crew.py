from enum import Enum
from typing import List
from datetime import datetime
from pydantic import BaseModel, Field, model_validator, ValidationError


class Rank(str, Enum):
    cadet = "cadet"
    officer = "officer"
    lieutenant = "lieutenant"
    captain = "captain"
    commander = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: List[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def validate_mission(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        has_lead = any(
            member.rank in (Rank.commander, Rank.captain)
            for member in self.crew
        )
        if not has_lead:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
                )

        if self.duration_days > 365:
            total = len(self.crew)
            experienced = sum(
                1 for member in self.crew
                if member.years_experience >= 5
            )
            if experienced < total / 2:
                raise ValueError(
                    "Long missions require at least "
                    "50% experienced crew (5+ years)"
                )

        if any(not member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")

        return self


def demonstrate() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")

    print("Valid mission created:")
    try:
        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            crew=[
                CrewMember(
                    member_id="C01",
                    name="Sarah Connor",
                    rank=Rank.commander,
                    age=40,
                    specialization="Mission Command",
                    years_experience=10,
                ),
                CrewMember(
                    member_id="C02",
                    name="John Smith",
                    rank=Rank.lieutenant,
                    age=35,
                    specialization="Navigation",
                    years_experience=6,
                ),
                CrewMember(
                    member_id="C03",
                    name="Alice Johnson",
                    rank=Rank.officer,
                    age=30,
                    specialization="Engineering",
                    years_experience=5,
                ),
            ],
            budget_millions=2500.0,
        )

        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crew size: {len(mission.crew)}")
        print("Crew members:")

        for member in mission.crew:
            print(f"- {member.name} ({member.rank.value}) - "
                  f"{member.specialization}")

    except ValidationError as e:
        print(e)

    print()
    print("=========================================")
    print("Expected validation error:")

    try:
        SpaceMission(
            mission_id="X999",
            mission_name="Faulty Mission",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=100,
            crew=[
                CrewMember(
                    member_id="C01",
                    name="Test User",
                    rank=Rank.officer,
                    age=30,
                    specialization="Test",
                    years_experience=2,
                )
            ],
            budget_millions=100.0,
        )
    except ValidationError:
        print("Mission must have at least one Commander or Captain")


if __name__ == "__main__":
    demonstrate()
