from scripts.drop_tables_main_safe import DEFAULT_TABLES, generate_drop_sql


def test_generate_drop_sql_default():
    sql = generate_drop_sql(DEFAULT_TABLES[:3])
    assert "DROP TABLE IF EXISTS" in sql
    assert "`articulos`" in sql or "articulos" in sql


def test_generate_drop_sql_custom():
    tbls = ["foo", "bar"]
    sql = generate_drop_sql(tbls)
    assert "DROP TABLE IF EXISTS `foo`;" in sql
    assert "DROP TABLE IF EXISTS `bar`;" in sql
