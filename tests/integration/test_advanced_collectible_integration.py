from scripts.helpful_scripts import (
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
)
from brownie import network
import pytest
import time
from scripts.advanced_collectible.deploy_and_create import deploy_and_create


def test_can_create_simple_collectible_integration():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
    # Act
    advanced_collectible, create_tx = deploy_and_create()
    time.sleep(90)
    # requestId = create_tx.events["requestedCollectible"]["requestId"]
    # random_number = 777
    # get_contract("vrf_coordinator").callBackWithRandomness(
    #     requestId, random_number, advanced_collectible.address, {"from": get_account()}
    # )
    # Assert
    assert advanced_collectible.tokenCounter() == 1
    # assert advanced_collectible.tokenIdToBreed(0) == random_number % 3
