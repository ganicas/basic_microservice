from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import generate_relationship, automap_base
from sqlalchemy.orm import interfaces

from common.urls.urls_file import master_app_database_connection

"""
    master_app_database_connection tables only for Importer data.
    This is main include to robot_micro service and by this setup robot service works with master_app_database_connection
    tables. Relationships generate, and reflect data included.

"""


def _gen_relationship(base, direction, return_fn, attrname, local_cls, referred_cls, **kw):
    if direction is interfaces.ONETOMANY:
        kw['cascade'] = 'all, delete-orphan'
        kw['passive_deletes'] = True
    return generate_relationship(base, direction, return_fn,
                                 attrname, local_cls, referred_cls, **kw)


metadata = MetaData()

master_app_database_engine = create_engine(
    '{}'.format(master_app_database_connection), convert_unicode=True, echo=False)

metadata.reflect(master_app_database_engine,
                 only=['administration_companies',
                       'administration_company_access',
                       'administration_userroletemplates',
                       'administration_customuser',
                       'administration_device',
                       'administration_product', 'robots_machine', 'administration_rescan_robot_machine',
                       'administration_notification']
                 )
Base = automap_base(metadata=metadata)
Base.prepare(generate_relationship=_gen_relationship)
