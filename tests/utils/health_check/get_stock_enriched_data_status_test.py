from unittest.mock import MagicMock

from utils.health_check.get_stock_enriched_data_status import (
    get_stock_enriched_data_status,
)


class GetEnrichedDataStatusTest:
    class StockStatusTest:
        def test_should_return_a_dict_with_stock_status(self):
            # Given
            is_enriched_stocks_contains_data = MagicMock(return_value=False)
            is_enriched_stock_data_exists = MagicMock(return_value=False)

            is_enriched_stock_data_exists.return_value = True

            # When
            status = get_stock_enriched_data_status(
                is_enriched_stock_data_exists=is_enriched_stock_data_exists,
                is_enriched_stocks_contains_data=is_enriched_stocks_contains_data,
            )

            # Then
            assert status["is_enriched_stock_datasource_exists"] == True

        def test_should_return_is_stock_ok_as_true_when_table_exists_with_data(self):
            # Given
            is_enriched_stocks_contains_data = MagicMock(return_value=False)
            is_enriched_stock_data_exists = MagicMock(return_value=False)

            is_enriched_stock_data_exists.return_value = True
            is_enriched_stocks_contains_data.return_value = True

            # When
            status = get_stock_enriched_data_status(
                is_enriched_stock_data_exists=is_enriched_stock_data_exists,
                is_enriched_stocks_contains_data=is_enriched_stocks_contains_data,
            )

            # Then
            assert status["is_enriched_stock_datasource_exists"] == True
            assert status["is_stock_ok"] == True

        def test_should_return_is_stock_ok_as_true_when_table_exists_without_data(self):
            # Given
            is_enriched_stocks_contains_data = MagicMock(return_value=False)
            is_enriched_stock_data_exists = MagicMock(return_value=False)

            is_enriched_stock_data_exists.return_value = True
            is_enriched_stocks_contains_data.return_value = False

            # When
            status = get_stock_enriched_data_status(
                is_enriched_stock_data_exists=is_enriched_stock_data_exists,
                is_enriched_stocks_contains_data=is_enriched_stocks_contains_data,
            )

            # Then
            assert status["is_enriched_stock_datasource_exists"] == True
            assert status["is_stock_ok"] == False
