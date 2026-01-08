import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT / "services" / "prefect"))

from compare_utils import should_promote

def test_should_promote_when_better_than_prod_plus_delta():
    assert should_promote(new_auc=0.80, prod_auc=0.78, delta=0.01) is True

def test_should_not_promote_when_not_enough_gain():
    assert should_promote(new_auc=0.785, prod_auc=0.78, delta=0.01) is False

def test_should_promote_if_prod_auc_is_nan():
    import math
    assert should_promote(new_auc=0.75, prod_auc=math.nan, delta=0.01) is True

def test_should_promote_if_prod_auc_is_none():
    assert should_promote(new_auc=0.75, prod_auc=None, delta=0.01) is True