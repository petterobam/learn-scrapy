# -*- coding:utf-8 -*-
import tagui as t
import uuid

def url2png(url):
    t.init()
    t.url(url)
    # t.type('q', 'decentralization[enter]')
    t.snap('page', 'results-' + str(uuid.uuid1()) + '.png')
    t.close()
        
