from tests.test_schema.helpers import PytestHelpers


def test_upgrading_to_head_creates_same_schema_as_model(engine):
    helpers = PytestHelpers(engine)
    helpers.add_alembic()
    schema_from_model = helpers.get_schema_str()

    helpers.drop_all()
    helpers.upgrade("head")
    schema_made_by_alembic = helpers.get_schema_str()
    helpers.assert_schema_strs_similar(schema_from_model, schema_made_by_alembic)
