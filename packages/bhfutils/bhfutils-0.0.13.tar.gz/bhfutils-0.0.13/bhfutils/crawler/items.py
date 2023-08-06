# -*- coding: utf-8 -*-

# Define here the models for your scraped items

from scrapy import Item, Field


class RawResponseItem(Item):
    appid = Field()
    crawlid = Field()
    url = Field()
    responseUrl = Field()
    statusCode = Field()
    success = Field()
    exception = Field()
    encoding = Field()
    playgroundId = Field()
    attrs = Field()


class MenuResponseItem(RawResponseItem):
    groupCategoryName = Field()
    groupName = Field()
    groupUrl = Field()


class ProductResponseItem(RawResponseItem):
    productUrl = Field()
    groupId = Field()
    imageUrl = Field()
    name = Field()
    details = Field()
    price = Field()


class ProductDetailsResponseItem(RawResponseItem):
    productUrl = Field()
    groupId = Field()
    imageUrl = Field()
    name = Field()
    details = Field()
