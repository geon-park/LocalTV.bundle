# -*- coding: utf-8 -*-

content_ratings = {
    u'모든 연령 시청가': {u'ORIGINAL': u'모든 연령 시청가', u'KCSC': u'모든 연령 시청가', u'TVPG': u'TV-G'},
    u'7세 이상 시청가': {u'ORIGINAL': u'7세 이상 시청가', u'KCSC': u'7세 이상 시청가', u'TVPG': u'TV-Y7'},
    u'12세 이상 시청가': {u'ORIGINAL': u'12세 이상 시청가', u'KCSC': u'12세 이상 시청가', u'TVPG': u'TV-PG'},
    u'15세 이상 시청가': {u'ORIGINAL': u'15세 이상 시청가', u'KCSC': u'15세 이상 시청가', u'TVPG': u'TV-14'},
    u'19세 이상 시청가': {u'ORIGINAL': u'19세 이상 시청가', u'KCSC': u'19세 이상 시청가', u'TVPG': u'TV-MA'},

    u'TV-Y': {u'ORIGINAL': u'TV-Y', u'KCSC': u'모든 연령 시청가', u'TVPG': u'TV-Y'},
    u'TV-G': {u'ORIGINAL': u'TV-G', u'KCSC': u'모든 연령 시청가', u'TVPG': u'TV-G'},
    u'TV-Y7': {u'ORIGINAL': u'TV-Y7', u'KCSC': u'7세 이상 시청가', u'TVPG': u'TV-Y7'},
    u'TV-PG': {u'ORIGINAL': u'TV-PG', u'KCSC': u'12세 이상 시청가', u'TVPG': u'TV-PG'},
    u'TV-14': {u'ORIGINAL': u'TV-14', u'KCSC': u'15세 이상 시청가', u'TVPG': u'TV-14'},
    u'TV-MA': {u'ORIGINAL': u'TV-MA', u'KCSC': u'19세 이상 시청가', u'TVPG': u'TV-MA'},
}


def get_content_rating(rating, country='KCSC'):
    return content_ratings[rating][country]
