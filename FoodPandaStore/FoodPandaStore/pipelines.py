# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


from sqlalchemy.orm.session import sessionmaker, query
from FoodPandaStore.FoodPandaStore.model import *
import datetime as dt
from datetime import datetime




class FoodpandastoreInfo2Pipeline:

    def __init__(self):
        engine = db_connect()
        create_tables(engine)
        self.session = sessionmaker(bind=engine)


    def  process_item(self, item, spider):

        session = self.session()
        new_store_info = FoodPandaStoreInfo2(
            id=item['id'],
            code=item['code'],
            category=item['category'],
            name=item['name'],
            url=item['url'],
            rating=item.get('rating', None),
            address=item['address'],
            latitude=item['latitude'],
            longitude=item['longitude'],
            is_pickup_available=item['is_pickup_available'],
            is_delivery_available=item['is_delivery_available'],
            is_active=item['is_active'],
            date=dt.datetime.utcnow()
        )

        new_ts = TambonStore(
            store_id=item['id'],
            sub_district_id=item['sub_district_id'],
            district_id=item['district_id'],
            province_id=item['province_id'],
            updated_datetime=datetime.utcnow())

        existing_tambon = session.query(TambonGeo2).filter_by(sub_district_id = item['sub_district_id'],
                                                                district_id=item['district_id'],
                                                                province_id=item['province_id']).first()

        if existing_tambon:
            ## Store
            existing_store_info = session.query(FoodPandaStoreInfo2).filter_by(id=item['id']).first()
            existing_tambon_store = session.query(TambonStore).filter_by(store_id=item['id'],
                                                                         sub_district_id=item['sub_district_id'],
                                                                         district_id=item['district_id'],
                                                                         province_id=item['province_id']).first()
            if existing_store_info:
                 session.merge(existing_store_info)
                 if existing_tambon_store:
                    session.merge(new_ts)
                 else:
                    session.add(new_ts)
            else:
                session.add(new_store_info)
                session.add(new_ts)

            menus = item.get('menus', [])
            for menu in menus:
                m = FoodPandaStoreMenu2(
                    id=menu['id'],
                    name=menu['name'],
                    type=menu['type'],
                    opening_time=menu['opening_time'],
                    closing_time=menu['closing_time']
                )
                new_store_info.menus.append(m)


        else:
            print('{}, {}, {} is not persisted in TambonGeo'.format(item['sub_district_id'],
                                                                            item['district_id'],
                                                                            item['province_id']))


        session.commit()
        session.close()