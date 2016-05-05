import factory
from django.db.models import signals

from django.core.management.base import BaseCommand

from config import settings
from core.db.manager import DataHubManager


class Command(BaseCommand):
    help = ("Creates the public policy schema and table "
            "necessary for creating row level security policies.")

    def handle(self, *args, **options):
        print('Creating the public policy schema')
        create_policy_schema(None, None)

        print('Creating the public policy table')
        create_policy_table(None, None)


@factory.django.mute_signals(signals.pre_save)
def create_policy_schema(apps, schema_editor):
    # create the dh_public schema if it doesn't exist
    public_username = settings.PUBLIC_ROLE
    datahub_manager = DataHubManager(public_username)

    create_schema_query = ('CREATE SCHEMA IF NOT EXISTS dh_public')
    datahub_manager.execute_sql(create_schema_query)


@factory.django.mute_signals(signals.pre_save)
def create_policy_table(apps, schema_editor):
    # create the policy table inside dh_public if it doesn't exist
    public_username = settings.PUBLIC_ROLE
    datahub_manager = DataHubManager(public_username)

    create_table_query = ('CREATE TABLE IF NOT EXISTS dh_public.policy'
                          '('
                          'policy_id serial primary key,'
                          'policy VARCHAR(80) NOT NULL,'
                          'policy_type VARCHAR(80) NOT NULL,'
                          'grantee VARCHAR(80) NOT NULL,'
                          'grantor VARCHAR(80) NOT NULL,'
                          'table_name VARCHAR(80) NOT NULL,'
                          'repo VARCHAR(80) NOT NULL,'
                          'repo_base VARCHAR(80) NOT NULL'
                          ');')
    datahub_manager.execute_sql(create_table_query)