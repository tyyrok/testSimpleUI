from pony.orm import Database,Required,Set,select,commit,Optional,Json
import json
import os

db = Database()
db.bind(provider='sqlite', filename='//data/data/ru.travelfood.simple_ui/databases/SimpleWMS', create_db=True)

class Birds(db.Entity):
    name =  Required(str, unique=True)
    photo = Optional(Json)
        
def init():
    db.generate_mapping(create_tables=True)  

def init_on_start(hashMap,_files=None,_data=None):
    init()
    hashMap.put("SQLConnectDatabase","test1.DB")
    hashMap.put("SQLExec",json.dumps({"query":"create table IF NOT EXISTS Birds(id integer primary key autoincrement,name text)","params":""}))
    return hashMap

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
                            "Variable": ""
                        },
                        {
                            "type": "TextView",
                            "show_by_condition": "",
                            "Value": "@string2",
                            "NoRefresh": False,
                            "document_type": "",
                            "mask": "",
                            "Variable": ""
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

def on_save_new_bird(hashMap, _files=None, _data=None):
    hashMap.put("mm_local","")
    
    if hashMap.get("listener") == "btn_create_bird":

        photo = {}
        photo['photo'] = json.loads(hashMap.get("photo_gallery"))
        
        Birds(name=str(hashMap.get("name")), photo=photo)
        commit()
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
    
    return hashMap
    

def on_start_detail_view(hashMap, _files=None, _data=None):
    hashMap.put("mm_local","")
    bird = json.loads(hashMap.get("card_data"))
    
    id = int(bird["string1"].split("- ")[1])
    
    bird = Birds.get(id=id)
    name = bird.name
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
    
    
    return hashMap

def on_input_detail_view(hashMap, _files=None, _data=None):
    if  hashMap.get("listener")=='ON_BACK_PRESSED': 
        hashMap.put("ShowScreen","Birds list")
        
    return hashMap