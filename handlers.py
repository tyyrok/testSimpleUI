from pony.orm import Database,Required,Set,select,commit,Optional,Json
#from pony.orm import *
from pony.orm.core import db_session
import time, datetime
import json
import os

db = Database()
db.bind(provider='sqlite', filename='//data/data/ru.travelfood.simple_ui/databases/SimpleWMS', create_db=True)

class Birds(db.Entity):
    name =  Required(str, unique=True)
    photo = Optional(Json)
    color = Optional(str)
    seen = Optional("BirdsSeen")
    
class BirdsSeen(db.Entity):
    timestamp = Required(datetime.datetime)
    counts = Required(int)
    bird = Required("Birds")
        
def init():
    db.generate_mapping(create_tables=True)  

def init_on_start(hashMap,_files=None,_data=None):
    init()
    hashMap.put("SQLConnectDatabase","test1.DB")
    hashMap.put("SQLExec",json.dumps({"query":"create table IF NOT EXISTS Birds(id integer primary key autoincrement,name text)","params":""}))
    return hashMap

@db_session
def on_start_birds_list(hashMap, _files=None, _data=None):
    hashMap.put("mm_local","")
    hashMap.put("mm_compression","70")
    hashMap.put("mm_size","65")
    
    j = { "customtable": {
                "options":{
                "search_enabled":False,
                "save_position":True
                },
            
            "layout":  {
                "type": "LinearLayout",
                "orientation": "vertical",
                "height": "match_parent",
                "width": "match_parent",
                "weight": "0",
                "Elements": [{
                    "type": "LinearLayout",
                    "orientation": "horizontal",
                    "height": "wrap_content",
                    "width": "match_parent",
                    "weight": "0",
                    "Elements": [{
                        "type": "Picture",
                        "show_by_condition": "",
                        "Value": "@pic1",
                        "NoRefresh": False,
                        "document_type": "",
                        "mask": "",
                        "Variable": "",
                        "TextSize": "16",
                        "TextColor": "#DB7093",
                        "TextBold": True,
                        "TextItalic": False,
                        "BackgroundColor": "",
                        "width": "match_parent",
                        "height": "wrap_content",
                        "weight": 2
                    },
                    {
                        "type": "LinearLayout",
                        "orientation": "vertical",
                        "height": "wrap_content",
                        "width": "match_parent",
                        "weight": "1",
                        "Elements": [{
                            "type": "TextView",
                            "show_by_condition": "",
                            "Value": "@string1",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": "",
                            "TextSize": "16",
                        },
                        {
                            "type": "TextView",
                            "show_by_condition": "",
                            "Value": "@string2",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": "",
                            "TextSize": "16",
                        },
                        {
                            "type": "TextView",
                            "show_by_condition": "",
                            "Value": "@string3",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": "",
                            "TextSize": "16",
             
                        }]
                    
                    },]
                },
                {
                    "type": "LinearLayout",
                    "orientation": "horizontal",
                    "height": "wrap_content",
                    "width": "match_parent",
                    "weight": "1",
                    
                    "Elements": [{
                                "type": "Button",
                                "show_by_condition": "",
                                "Value": "Детали",
                                "Variable": "btn_tst1",
                                "NoRefresh": False,
                                "document_type": "",
                                "mask": ""
                                
                            }]
                }]
            }
        }
    }
    
    query = select(c for c in Birds)
    
   
    j["customtable"]["tabledata"]=[]

    for record in query:
        pic=""
        if 'photo' in record.photo :
        
            p = record.photo['photo']
            
            if len(p)>0:
                
                for jf in _files: #находим путь к файлу по идентификатору
                        if jf['id']==p[0]:
                              if os.path.exists(jf['path']): 
                                    pic ="~"+jf['path']
                              break  
        c =  {
            "string1" : "ID - " + str(record.id),
            "string2": "Имя птицы - " + str(record.name),
            "string3": "Цвет перьев - " + str(record.color),
            "pic1": pic,
            "photo": json.dumps(record.photo)
        }                 
        j["customtable"]["tabledata"].append(c)                      

    hashMap.put("table",json.dumps(j))
    
    return hashMap

def on_input_birds_list(hashMap, _files=None, _data=None):

    if (hashMap.get("listener") == "@btn_add_bird"):
        hashMap.put("ShowScreen","Add bird")
        
    elif hashMap.get("listener")=="LayoutAction":
        hashMap.put("ShowScreen","Bird detail")
        
    elif hashMap.get("listener") == "ON_BACK_PRESSED":
        hashMap.put("FinishProcess","")
        
    return hashMap

@db_session
def on_save_new_bird(hashMap, _files=None, _data=None):
    hashMap.put("mm_local","")
    
    if hashMap.get("listener") == "btn_create_bird":

        if hashMap.get("name") == "":
            hashMap.put("toast", "Введите имя птицы!")
            
            return hashMap
        
        if not hashMap.containsKey("color"):
            hashMap.put("toast", "Выберите цвет перьев!")
            
            return hashMap
        
        photo = {}
        if hashMap.containsKey("photo_gallery"):
            photo['photo'] = json.loads(hashMap.get("photo_gallery"))
            Birds(name=str(hashMap.get("name")), photo=photo, color=hashMap.get("color"))
        else:
            Birds(name=str(hashMap.get("name")), color=hashMap.get("color"))

        hashMap.remove("photo_gallery")
        hashMap.remove("color")
        hashMap.remove("name")
        hashMap.put("ShowScreen","Birds list")
        
    elif hashMap.get("listener") == "photo":
        
        photo = hashMap.get("photo")
        hashMap.put("photo_gallery", json.dumps([photo]))
        
    elif hashMap.get("listener") == "ON_BACK_PRESSED":
        hashMap.put("ShowScreen","Birds list")
        
    return hashMap

def on_start_new_bird(hashMap,_files=None,_data=None):
    hashMap.put("mm_local","")
    hashMap.put("mm_compression","70")
    hashMap.put("mm_size","65")
    
    if hashMap.get("name") == None:
        hashMap.put("name","")
    
    return hashMap
    
@db_session
def on_start_detail_view(hashMap, _files=None, _data=None):
    hashMap.put("mm_local","")
    bird = json.loads(hashMap.get("card_data"))
    
    id = int(bird["string1"].split("- ")[1])
    
    bird = Birds.get(id=id)
    name = bird.name
    color = bird.color
    pic = ""
    if 'photo' in bird.photo:
        
        photo = bird.photo["photo"]
        
        if len(photo) > 0:
            for jf in _files: #находим путь к файлу по идентификатору
                
                if jf['id']==photo[0]:
                    if os.path.exists(jf['path']): 
                        pic ="~"+jf['path']
                        break 
    #hashMap.put("toast", str(pic))
    hashMap.put("name", name)
    hashMap.put("photo", pic)
    hashMap.put("color", color)
    
    
    return hashMap

def on_input_detail_view(hashMap, _files=None, _data=None):
    if  hashMap.get("listener")=='ON_BACK_PRESSED': 
        hashMap.put("ShowScreen","Birds list")
        
    elif hashMap.get("listener")=="btn_seen_bird":
        bird = json.loads(hashMap.get("card_data"))
        global global_bird_id 
        global_bird_id = bird['string1'].split("- ")[1]
        hashMap.put("_global_bird_id", global_bird_id)
        hashMap.put("ShowScreen","Birds list")
        
    return hashMap

@db_session
def on_start_birds_seen_list(hashMap, _files=None, _data=None):
    hashMap.put("mm_local","")
    hashMap.put("mm_compression","70")
    hashMap.put("mm_size","65")
    
    j = { "customtable": {
                "options":{
                "search_enabled":False,
                "save_position":True
                },
            
            "layout":  {
                "type": "LinearLayout",
                "orientation": "vertical",
                "height": "match_parent",
                "width": "match_parent",
                "weight": "0",
                "Elements": [{
                    "type": "LinearLayout",
                    "orientation": "horizontal",
                    "height": "wrap_content",
                    "width": "match_parent",
                    "weight": "0",
                    "Elements": [{
                        "type": "Picture",
                        "show_by_condition": "",
                        "Value": "@pic1",
                        "NoRefresh": False,
                        "document_type": "",
                        "mask": "",
                        "Variable": "",
                        "TextSize": "16",
                        "TextColor": "#DB7093",
                        "TextBold": True,
                        "TextItalic": False,
                        "BackgroundColor": "",
                        "width": "match_parent",
                        "height": "wrap_content",
                        "weight": 2
                    },
                    {
                        "type": "LinearLayout",
                        "orientation": "vertical",
                        "height": "wrap_content",
                        "width": "match_parent",
                        "weight": "1",
                        "Elements": [{
                            "type": "TextView",
                            "show_by_condition": "",
                            "Value": "@name",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": ""
                        },
                        {
                            "type": "TextView",
                            "show_by_condition": "",
                            "Value": "@datetime",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": ""
                        },
                        {
                            "type": "TextView",
                            "show_by_condition": "",
                            "Value": "@counts",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": ""
                        }]
                    
                    },]
                }]
            }
        }
    }
    query = select(c for c in BirdsSeen)
    
   
    j["customtable"]["tabledata"]=[]

    for record in query:
        pic=""
        if 'photo' in record.bird.photo :
        
            p = record.bird.photo['photo']
            
            if len(p)>0:
                
                for jf in _files: #находим путь к файлу по идентификатору
                        if jf['id']==p[0]:
                              if os.path.exists(jf['path']): 
                                    pic ="~"+jf['path']
                              break  
        c =  {
            "name" : "Имя птицы - " + str(record.bird.name),
            "datetime": "Время наблюдения - " + str(record.timestamp),
            "counts": "Кол-во наблюдений - " + str(record.counts),
            "pic1": pic,
            "photo": json.dumps(record.bird.photo)
        }                 
        j["customtable"]["tabledata"].append(c)                      

    hashMap.put("table",json.dumps(j))
    
    return hashMap

@db_session
def on_input_birds_seen_list(hashMap, _files=None, _data=None):
    
    if hashMap.get("listener") == "ON_BACK_PRESSED":
        hashMap.put("FinishProcess","")
        
    elif hashMap.get("listener") == "btn_add_seen_bird":
        
        if not hashMap.containsKey("_global_bird_id"):
            hashMap.put("toast", "Вы не указали увиденную птицу")
            
        else:
            id = int(hashMap.get("_global_bird_id"))
            bird = Birds.get(id=id)
            birdseen = BirdsSeen.get(bird=bird)

            if birdseen is not None:
                count = birdseen.counts
                birdseen.timestamp = datetime.datetime.now()
                birdseen.counts = count + 1
                
            else:
                BirdsSeen(timestamp=datetime.datetime.now(), counts=1, bird=bird)
    
    return hashMap