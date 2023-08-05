from matplotlib.testing.decorators import cleanup

from unittest import TestCase
from parameterized import parameterized

import os

from linefolio.quantrocket_moonshot import from_moonshot_csv
from linefolio.utils import (to_utc, to_series)
from linefolio.tears import (create_full_tear_sheet,
                             create_simple_tear_sheet,
                             create_returns_tear_sheet,
                             create_position_tear_sheet,
                             create_txn_tear_sheet,
                             create_round_trip_tear_sheet,
                             create_interesting_times_tear_sheet,)


class PositionsTestCase(TestCase):
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))

    @parameterized.expand([({},),
                           ({'slippage': 1},),
                           ({'round_trips': True},),
                           ({'hide_positions': True},),
                           ({'cone_std': 1},),
                           ({'bootstrap': True},),
                           ])
    @cleanup
    def test_create_full_tear_sheet_breakdown(self, kwargs):
        from_moonshot_csv(self.__location__ + "/test_data/moonline-tearsheet.csv", **kwargs)
