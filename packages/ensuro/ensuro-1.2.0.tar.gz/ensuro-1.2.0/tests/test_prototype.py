from io import StringIO
from ensuro.utils import load_config
import ensuro.prototype

__author__ = "Guillermo M. Narvaja"
__copyright__ = "Ensuro"
__license__ = "Apache-2.0"


def test_load_yaml_prototype():
    YAML_SETUP = """
    risk_modules:
      - name: Roulette
        scr_percentage: 1
        scr_interest_rate: "0.01"
        ensuro_fee: 0
    currency:
        name: USD
        symbol: $
        initial_supply: 6000
        initial_balances:
        - user: LP1
          amount: 3500
        - user: CUST1
          amount: 100
    etokens:
      - name: eUSD1WEEK
        expiration_period: 604800
      - name: eUSD1MONTH
        expiration_period: 2592000
      - name: eUSD1YEAR
        expiration_period: 31536000
    """

    pool = load_config(StringIO(YAML_SETUP), ensuro.prototype)
    assert "eUSD1WEEK" in pool.etokens
    assert "eUSD1MONTH" in pool.etokens
    assert "eUSD1YEAR" in pool.etokens
    assert "Roulette" in pool.config.risk_modules
