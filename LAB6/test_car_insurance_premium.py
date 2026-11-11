import pytest
from car_insurance_premium import (
    annual_premium,
    no_claim_bonus,
    claim_payout,
)


# Annual premium tests

def test_sedan_no_claims():
    assert annual_premium("sedan", 30, 0, False) == 9600


def test_all_car_types():
    assert annual_premium("hatchback", 30, 1, False) == 8000
    assert annual_premium("suv", 30, 1, False) == 15000


def test_unknown_car_type():
    with pytest.raises(ValueError):
        annual_premium("truck", 30, 0, False)


def test_driver_too_young():
    with pytest.raises(ValueError):
        annual_premium("sedan", 17, 0, False)


def test_young_driver():
    assert annual_premium("sedan", 24, 1, False) == 16000


def test_senior_driver():
    assert annual_premium("sedan", 60, 1, False) == 14000


def test_middle_age_driver():
    assert annual_premium("sedan", 40, 1, False) == 12000


def test_claim_history():
    assert annual_premium("sedan", 30, 1, False) == 12000
    assert annual_premium("sedan", 30, 2, False) == 12000
    assert annual_premium("sedan", 30, 3, False) == 24000


def test_anti_theft_discount():
    assert annual_premium("sedan", 30, 1, True) == 11500


# No-claim bonus tests

def test_negative_claim_free_years():
    with pytest.raises(ValueError):
        no_claim_bonus(-1)


def test_no_bonus():
    assert no_claim_bonus(0) == 0


def test_small_bonus():
    assert no_claim_bonus(1) == 20
    assert no_claim_bonus(2) == 20


def test_medium_bonus():
    assert no_claim_bonus(3) == 35
    assert no_claim_bonus(4) == 35


def test_maximum_bonus():
    assert no_claim_bonus(5) == 50
    assert no_claim_bonus(6) == 50


# Claim payout tests

def test_invalid_damage_cost():
    with pytest.raises(ValueError):
        claim_payout(-1, 10000, 500, False)


def test_invalid_deductible():
    with pytest.raises(ValueError):
        claim_payout(1000, 10000, -1, False)


def test_total_loss():
    assert claim_payout(8000, 10000, 500, True) == 10000


def test_damage_below_deductible():
    assert claim_payout(400, 10000, 500, False) == 0


def test_damage_equal_to_deductible():
    assert claim_payout(500, 10000, 500, False) == 0


def test_normal_claim_payout():
    assert claim_payout(3000, 10000, 500, False) == 2500


def test_payout_capped_at_insured_value():
    assert claim_payout(15000, 10000, 500, False) == 10000