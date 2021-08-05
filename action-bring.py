#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import configparser
import importlib
from BringApi.BringApi import BringApi
from rhasspyhermes.nlu import NluIntent
from importlib import reload
from rhasspyhermes_app import EndSession, HermesApp
import io
import random
import sys
import json

app = HermesApp("BringApp")

CONFIGURATION_ENCODING_FORMAT = "utf-8"
# Your Path..
CONFIG_INI = "/home/pi/skills-server/skills/bring-shopping/config.ini"
i18n = importlib.import_module("translations." + "de")

class SnipsConfigParser(configparser.ConfigParser):
    def to_dict(self):
        return {section : {option_name : option for option_name, option in self.items(section)} for section in self.sections()}

def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.read_file(f)
            return conf_parser.to_dict()
    except (IOError, configparser.Error) as e:
        return dict()

def get_bring(conf):
    return BringApi(conf['secret']['uuid'],conf['secret']['bringlistuuid'])

def add_item_int(bring, items):
    list = bring.get_items()['purchase']

    added = []
    exist = []
    for item in items:
        if not any(entr['name'] == item for entr in list):
            bring.purchase_item(item, "")
            added.append(item)
            print(added)
        else:
            exist.append(item)
    return added, exist

def delete_item_int(bring, items):
    list = bring.get_items()['purchase']
    removed = []
    exist = []
    for item in items:
        if any(entr['name'] == item for entr in list):
            bring.recent_item(item)
            removed.append(item)
        else:
            exist.append(item)
    return removed, exist

def check_list_int(bring,check):
    list = bring.get_items()['purchase']
    found = []
    missing = []
    for c in check:
        if any(c == entr['name'] for entr in list):
            found.append(c)
        else:
            missing.append(c)
    return found, missing


### INTENTS ###
## Add item to list
def add_item(intentMessage,conf):
    itemsList = []
    for slot in intentMessage.slots:
        if slot.slot_name == "Items":
            itemsList.append(slot.raw_value)

    if len(itemsList) > 0:
        added, exist = add_item_int(get_bring(conf), itemsList)
        return combine_lists(i18n.ADD, i18n.ADD_CONN, i18n.ADD_END, i18n.ADD_F, added, exist)
    else:
        return random.choice(i18n.ADD_WHAT)

## Delete items from list
def delete_item(intentMessage,conf):
    itemsList = []
    for slot in intentMessage.slots:
        if slot.slot_name == "Items":
            itemsList.append(slot.raw_value)

    if len(itemsList) > 0:
        removed, failed = delete_item_int(get_bring(conf), itemsList)
        return combine_lists(i18n.REM, i18n.REM_CONN, i18n.REM_END, i18n.REM_F, removed, failed)
    else:
        return random.choice(i18n.REM_WHAT)

## check if item is in list
def check_list(intentMessage,conf):
    itemsList = []
    for slot in intentMessage.slots:
        if slot.slot_name == "Items":
            itemsList.append(slot.raw_value)

    if len(itemsList) > 0:
        found, missing = check_list_int(get_bring(conf), itemsList)
        return combine_lists(i18n.CHK, i18n.CHK_CONN, i18n.CHK_END, i18n.CHK_F, found, missing)
    else:
        return random.choice(i18n.CHK_WHAT)

# Du hast xxx, xxx und xxx auf deiner Einkaufsliste
def read_list(conf):
    items = get_bring(conf).get_items()['purchase']
    itemlist = [ l['name'] for l in items ]
    print(itemlist)
    return get_text_for_list(i18n.READ, itemlist)


#### List/Text operations
### Combines two lists(if filled)
# first+CONN+second
# first+END
# second
def combine_lists(str_first, str_conn, str_end, str_second, first, second):
    strout = ""
    if first:
        strout = get_text_for_list(str_first, first)
    if second:
        backup = strout # don't overwrite added list... even if empty!
        strout = get_text_for_list(str_second,second)
    else:
        strout += random.choice(str_end)
    
    if first and second:
        strout = random.choice(str_conn).format(backup,strout)
    return strout

### Combine entries of list into wrapper sentence
def get_text_for_list(str,list):
    category, strout = get_default_list(list)
    print(str)
    print(category)
    return random.choice(str[category]).format(strout)

### Return if MULTI or ONE entry and creates list for multi ( XXX, XXX and XXX )
def get_default_list(items):
    if len(items) > 1:
        return "MULTI", random.choice(i18n.GENERAL_LIST).format(first=", ".join(items[:-1]), last=items[-1])
    elif len(items) == 1:
        return "ONE", items[0]
    else:
        return "NONE", ""


@app.on_intent(i18n.INTENT_ADD_ITEM)
async def addItem(intent: NluIntent):
    """Add Item"""
    return EndSession(add_item(intent,conf))

@app.on_intent(i18n.INTENT_DEL_ITEM)
async def delItem(intent: NluIntent):
    """del item"""
    return EndSession(delete_item(intent,conf))

@app.on_intent(i18n.INTENT_READ_LIST)
async def readList(intent: NluIntent):
    """Read list"""
    return EndSession(read_list(conf))

@app.on_intent(i18n.INTENT_CHECK_LIST)
async def checkList(intent: NluIntent):
    """Check List"""
    return EndSession(check_list(intent,conf))

if __name__ == "__main__":
   # reload(sys)
   # sys.setdefaultencoding('utf-8')
    conf = read_configuration_file(CONFIG_INI)
    i18n = importlib.import_module("translations." + "de")
    app.run()
