import pandas
import pytest

from db import db
from utils.database_cleaners import clean_database, clean_tables
from write.offerer_view.create_cultural_activity import _create_table_offerer_cultural_activity


class CreateTableOffererCulturalActivityTest:
    def teardown_method(self):
        clean_database()
        clean_tables()

    def test_should_create_table(self, app):
        # Given
        offerer_cultural_activity_dataframe = pandas.DataFrame()

        # When
        with app.app_context():
            _create_table_offerer_cultural_activity(offerer_cultural_activity_dataframe)

        # Then
        query = '''SELECT * FROM information_schema.tables WHERE table_name = 'offerer_cultural_activity';'''
        results = db.session.execute(query).fetchall()
        assert len(results) == 1
