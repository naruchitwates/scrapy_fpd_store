from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy import create_engine, Column, Table, ForeignKeyConstraint, UniqueConstraint
from sqlalchemy.orm import relationship

from sqlalchemy.pool import NullPool


from FoodPandaStore.FoodPandaStore.settings import CONNECTION_STRING

Base = declarative_base()

def db_connect():

    # return create_engine(CONNECTION_STRING,
    #                      pool_size=20,
    #                      max_overflow=4,
    #                      pool_recycle=300,
    #                      pool_pre_ping=True,
    #                      pool_use_lifo=True
    #                      )

    return create_engine(CONNECTION_STRING,
                         poolclass=NullPool)


def create_tables(engine):
    Base.metadata.create_all(engine)


class TambonStore(Base):
    __tablename__ = 'scrapy__tambon_store'
    store_id = Column(Integer, ForeignKey('datamart.scrapy__foodpanda_store_info_2.id'), primary_key=True)
    sub_district_id = Column(Integer, primary_key=True)
    district_id = Column(Integer, primary_key=True)
    province_id = Column(Integer, primary_key=True)
    updated_datetime = Column(DateTime, nullable=False)
    __table_args__ = (
        UniqueConstraint('store_id', 'sub_district_id', 'district_id', 'province_id'),
        ForeignKeyConstraint(['sub_district_id',
                              'district_id',
                              'province_id'],
                             ['datamart.tambon_geo_2.sub_district_id',
                              'datamart.tambon_geo_2.district_id',
                              'datamart.tambon_geo_2.province_id']),
                             {"schema": "datamart"}
    )

    def __repr__(self):
        return '<TambonStore {}, {}, {}, {}>'.format(self.store_id,
                                                     self.sub_district_id,
                                                     self.district_id,
                                                     self.province_id)

class TambonGeo2(Base):

    __tablename__ = "tambon_geo_2"
    __table_args__ = (
        UniqueConstraint('sub_district_id', 'district_id', 'province_id'),
        {"schema":"datamart"}
    )
    sub_district_id = Column(Integer, primary_key=True)
    district_id = Column(Integer, primary_key=True)
    province_id = Column(Integer, primary_key=True)
    sub_district_th = Column(String(255), nullable=True)
    sub_district_en = Column(String(255), nullable=True)
    district_th = Column(String(255), nullable=True)
    district_en = Column(String(255), nullable=True)
    province_th = Column(String(255), nullable=True)
    province_en = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    last_updated_dt = Column('last_updated_dt', DateTime, nullable=False)


    def __repr__(self):
        return '<TambonGeo {}, {}, {}>'.format(self.sub_district_id,
                                                self.district_id,
                                                self.province_id)


class FoodPandaStoreInfo2(Base):

    __tablename__ = "scrapy__foodpanda_store_info_2"
    __table_args__ = {"schema": "datamart"}
    id = Column('id', Integer, primary_key=True, unique=True)
    code = Column('code', String(255))
    name = Column('name', String(255))
    category = Column('category', String(255))
    rating = Column('rating', Integer)
    latitude = Column('latitude', Float)
    longitude = Column('longitude', Float)
    address = Column('address', Text)
    url = Column('url', Text)
    is_pickup_available = Column('is_pickup_available', Boolean)
    is_delivery_available = Column('is_delivery_available', Boolean)
    is_active = Column('is_active', Boolean)
    date = Column('date', DateTime)

    tambons_stores = relationship('TambonStore',
                           backref='tambon_store_list'
                           )

    menus = relationship('FoodPandaStoreMenu2', back_populates='store_info',
                         cascade='save-update, delete')

    def __repr__(self):
        return '<FoodPandaStoreInfo2 {}>'.format(self.id)






class FoodPandaStoreMenu2(Base):

    __tablename__ = 'scrapy__foodpanda_store_menu_2'
    __table_args__ = {"schema": "datamart"}
    id = Column(Integer, primary_key=True)
    name = Column('name', String(255))
    type = Column('type', String(64))
    opening_time = Column('opening_time', String(64))
    closing_time = Column('closing_time', String(64))
    store_id = Column(Integer, ForeignKey('datamart.scrapy__foodpanda_store_info_2.id'))
    # Parent
    store_info = relationship('FoodPandaStoreInfo2', back_populates='menus')


    def __repr__(self):
        return '<FoodPandaStoreMenu2 {}, {}>'.format(self.id, self.store_id)










if __name__ == "__main__":

    pass