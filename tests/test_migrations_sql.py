import io

from django.core.management import call_command
from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase


class SqlMigrationTests(TestCase):
    def test_models_match_the_migration_state(self):
        call_command("makemigrations", "--check", "--dry-run", stdout=io.StringIO())

    def test_reverse_sql_drops_the_tables(self):
        executor = MigrationExecutor(connection)
        self.assertTrue(executor.loader.graph.leaf_nodes("inventory"))
        migration = executor.loader.get_migration("inventory", "0001_initial")
        ops = [op for op in migration.operations]
        self.assertEqual(type(ops[0]).__name__, "SeparateDatabaseAndState")
        reverse = ops[0].database_operations[0].reverse_sql
        self.assertTrue(any("DROP TABLE inv_lot" in s for s in reverse))
