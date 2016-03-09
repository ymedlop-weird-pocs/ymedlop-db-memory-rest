# -*- coding: utf-8 -*-

import logging
import urllib

from models.offices import Offices
from numpy import genfromtxt
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event, create_engine, MetaData

from geoalchemy import WKTSpatialElement
from geoalchemy.functions import functions

# Using a Memory Database in Multiple Threads
# http://docs.sqlalchemy.org/en/rel_0_7/dialects/sqlite.html#using-a-memory-database-in-multiple-threads

engine = create_engine(
    'sqlite://',
    connect_args={'check_same_thread':False},
    poolclass=StaticPool
)

# this enables the libspatialite extension on each connection
@event.listens_for(engine, "connect")
def connect(dbapi_connection, notused):
    logging.info ("Loading Spatialite Ext!!")
    dbapi_connection.enable_load_extension(True)
    dbapi_connection.execute("SELECT load_extension('libspatialite.so');")


def init_db():

    logging.info ("Downloading data!!")
    urllib.urlretrieve ("https://storage.googleapis.com/ymedlop-memory-db-demo/mocks/oficinas.csv", "oficinas.csv")

    logging.info ("Initializating the application!!")

    engine.execute("SELECT InitSpatialMetaData();")

    session = sessionmaker(bind=engine)()

    logging.info("Creating Table Offices")
    Offices.__table__.create(engine)

    logging.info("Loading values in Offices file")
    data = genfromtxt(
        'oficinas.csv',
        delimiter=',',
        dtype= None,
        converters={0: lambda s: str(s)} # Problem Encoding es_ES
    )

    logging.info("Mapping values in Offices")

    for item in data.tolist():
        office = Offices(
            desc = item[0],
            address = item[1],
            location = 'POINT({0} {1})'.format(item[2], item[3]),
            beautiful_location = 'POINT({0} {1})'.format(item[2], item[3])
        )
        session.add(office)

    logging.info("Inserting values in Offices")
    session.commit()


def get_all():

    session = sessionmaker(bind=engine)()

    list = []

    # TODO: https://marshmallow.readthedocs.org/en/latest/nesting.html
    for office in session.query(Offices):
        list.append({
            "desc": office.desc,
            "address": office.address,
            "location": office.beautiful_location
        })

    return list


def near(lat, lng, radius):

    list = []
    point = WKTSpatialElement('POINT({0} {1})'.format(lng, lat), 4326)

    logging.info("Doing search with %s" % 'POINT({0} {1})'.format(lng, lat))
    logging.info("And Radius %s" % radius)

    session = sessionmaker(bind=engine)()
    query = session.query(Offices).filter(functions._within_distance(Offices.location, point, radius))

    # TODO: https://marshmallow.readthedocs.org/en/latest/nesting.html
    for office in query:
        list.append({
            "desc": office.desc,
            "address": office.address,
            "location": office.beautiful_location
        })

    return list
