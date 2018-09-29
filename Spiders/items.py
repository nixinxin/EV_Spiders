# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose, Join


def split_processor(values):
    result = None
    if "：" in values:
        result = values.split("：")[1]
    elif ":" in values:
        result = values.split(":")[1]
    if result == '' or result is None:
        return 'null'
    return result


class ElevatorLoader(ItemLoader):
    default_input_processor = MapCompose(split_processor, )
    default_output_processor = TakeFirst()


class SpidersItem(scrapy.Item):
    # define the fields for your item here like:
    identity_code = scrapy.Field()
    reg_code = scrapy.Field()
    equipment_name_num = scrapy.Field()
    customer_addr = scrapy.Field()
    customer_name = scrapy.Field()
    expired_date = scrapy.Field()
    manufacture_unit = scrapy.Field()
    manufacture_name = scrapy.Field()
    manufacture_product_id = scrapy.Field()
    use_id = scrapy.Field()

    def get_sql(self):
        sql = '''INSERT INTO `elevator`.`elev_info_najing_increase`(`id`, `identity_code`, `reg_code`, \
        `equipment_name_num`, `customer_addr`, `customer_name`, `expired_date`, `manufacture_unit`, 
        `manufacture_name`, `manufacture_product_id`, `use_id`) 
        VALUES ({0}, "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", "{8}", "{9}", "{10}") 
        ON duplicate KEY UPDATE `id`= VALUES(`id`)'''

        sql = sql.format(int(self['identity_code']), self['identity_code'], self['reg_code'],
                         self['equipment_name_num'], self['customer_addr'],
                         self['customer_name'], self['expired_date'], self['manufacture_unit'],
                         self['manufacture_name'],
                         self['manufacture_product_id'], self['use_id'])
        return sql


class OthersItem(scrapy.Item):
    # define the fields for your item here like:
    identity_code = scrapy.Field()
    reg_code = scrapy.Field()
    equipment_name_num = scrapy.Field()
    customer_addr = scrapy.Field()
    customer_name = scrapy.Field()
    equipment_parameter = scrapy.Field()
    expired_date = scrapy.Field()
    manufacture_unit = scrapy.Field()
    maintain_unit = scrapy.Field()
    phone = scrapy.Field()

    def get_sql(self):
        sql = '''INSERT INTO `elevator`.`elev_info_najing_increase_other`(`id`, `identity_code`, `reg_code`, 
        `equipment_name_num`, `customer_addr`, `customer_name`, `equipment_parameter`, `expired_date`, `manufacture_unit`, 
        `maintain_unit`, `phone`) 
        VALUES ({0}, "{1}", "{2}", "{3}", "{4}", "{5}", "{6}", "{7}", "{8}", "{9}", "{10}") 
        ON duplicate KEY UPDATE `id`= VALUES(`id`)'''
        if self['identity_code']:
            sql = sql.format(int(self['identity_code']), self['identity_code'], self['reg_code'],
                             self['equipment_name_num'], self['customer_addr'],
                             self['customer_name'], self['equipment_parameter'], self['expired_date'],
                             self['manufacture_unit'],
                             self['maintain_unit'], self['phone'])
            return sql
