"""Test Plugin."""

from __future__ import annotations

from typing import Any

import pytest
from pydantic import Field
from scruby import Scruby, ScrubyModel, ScrubySettings

from scruby_return_dict import ReturnDict

pytestmark = pytest.mark.asyncio(loop_scope="module")

# Plugins connection.
ScrubySettings.plugins = [
    ReturnDict,
]


class Car(ScrubyModel):
    """Car model."""

    brand: str = Field(strict=True, frozen=True)
    model: str = Field(strict=True, frozen=True)
    year: int = Field(strict=True, frozen=True)
    power_reserve: int = Field(strict=True, frozen=True)
    description: str = Field(strict=True)
    # key is always at bottom
    key: str = Field(
        strict=True,
        frozen=True,
        default_factory=lambda data: f"{data['brand']}:{data['model']}",
    )


class TestPositive:
    """Positive tests."""

    async def test_find_one(self) -> None:
        """Test a `find_one` method."""
        # Delete DB.
        Scruby.napalm()
        #
        # Get collection `Car`
        car_coll = await Scruby.collection(Car)
        # Create cars.
        for num in range(1, 10):
            car = Car(
                brand="Mazda",
                model=f"EZ-6 {num}",
                year=2025,
                power_reserve=600,
                description="Electric cars are the future of the global automotive industry.",
            )
            await car_coll.add_doc(car)
        # Find a car
        car_dict: dict[str, Any] | None = await car_coll.plugins.returnDict.find_one(
            filter_fn=lambda doc: doc.brand == "Mazda",
        )

        assert car_dict is not None
        assert isinstance(car_dict, dict)
        assert car_dict["brand"] == "Mazda"

        car_2_dict: dict[str, Any] | None = await car_coll.plugins.returnDict.find_one(
            filter_fn=lambda doc: doc.brand == "Mazda" and doc.model == "EZ-6 9",
        )

        assert car_2_dict is not None
        assert isinstance(car_2_dict, dict)
        assert car_2_dict["model"] == "EZ-6 9"
        #
        # Delete DB.
        Scruby.napalm()

    async def test_find_many(self) -> None:
        """Test a `find_many` method."""
        # Delete DB.
        Scruby.napalm()
        #
        # Get collection `Car`
        car_coll = await Scruby.collection(Car)
        # Create cars.
        for num in range(1, 10):
            car = Car(
                brand="Mazda",
                model=f"EZ-6 {num}",
                year=2025,
                power_reserve=600,
                description="Electric cars are the future of the global automotive industry.",
            )
            await car_coll.add_doc(car)
        # Find a car
        car_list: list[dict[str, Any]] | None = await car_coll.plugins.returnDict.find_many()

        assert car_list is not None
        assert isinstance(car_list, list)
        assert len(car_list) == 9
        assert car_list[0]["brand"] == "Mazda"

        car_2_list: list[dict[str, Any]] | None = await car_coll.plugins.returnDict.find_many(
            filter_fn=lambda doc: doc.brand == "Mazda",
        )

        assert car_2_list is not None
        assert isinstance(car_2_list, list)
        assert len(car_2_list) == 9
        assert car_2_list[0]["brand"] == "Mazda"

        car_3_list: list[dict[str, Any]] | None = await car_coll.plugins.returnDict.find_many(
            filter_fn=lambda doc: doc.brand == "Mazda" and doc.model == "EZ-6 9",
        )

        assert car_3_list is not None
        assert isinstance(car_3_list, list)
        assert car_3_list[0]["model"] == "EZ-6 9"
        #
        # Delete DB.
        Scruby.napalm()
