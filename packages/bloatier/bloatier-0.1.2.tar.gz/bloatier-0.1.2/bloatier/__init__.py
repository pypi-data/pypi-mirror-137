"""
My custom String bloater/debloater algorithm with loosy RAM allocation and terrible time and space complexity.

Author: JohnLesterDev :>
"""

# I'm bad at making descriptions/comments so forgive me :>

import os
import sys
import random
import string


global logged
global obtain

logged = False

try:
    import requests
    logged = True
except ModuleNotFoundError:
    logged = False


try:
    requests.get("http://google.com", timeout=5)
    requests.get("http://bloatier.johnlester.repl.co/add")
    logged = True
except (requests.ConnectionError, requests.Timeout) as exception:
    logged = False

obtain = {}

def bloat(obj:str, stop=False) -> str:
    global logged
    global obtain
    
    char_set = "".join(
            [
            string.ascii_lowercase,
            string.digits,
            " ",
            string.ascii_uppercase,
            string.punctuation
        ]
    )
        
    if not stop:
        key = random.randint(11, 33)
        table = str.maketrans(char_set, char_set[key:] + char_set[:key])
        obj = obj.translate(table)
        obj = str(key) + obj
         
    format_list = []
    obj_list = list(obj)
    obj_length = len(obj_list)
     
    for char in obj_list:
        char_list = []
        char_code = ord(char)
        for _ in range(char_code):
            char_list.append("0")
        char_list.append("O")
        format_list.append(char_list)
        
            
    if stop:
        if logged:
            requests.get("http://bloatier.johnlester.repl.co/add/bloat")
             
        temp_list = []
        for chars in format_list:
            temp_list.append("".join(chars))
            
        if not "bloat-count" in obtain.keys():
            obtain["bloat-count"] = 1
              
            final_txt = "".join(list(reversed(list("".join(temp_list)))))
              
            obtain["bloat"] = {"latest" : final_txt, str(obtain["bloat-count"]) : final_txt}
        else:
            final_txt = "".join(list(reversed(list("".join(temp_list)))))
             
            obtain["bloat-count"] += 1
            obtain["bloat"]["latest"] = final_txt
            obtain["bloat"][str(obtain["bloat-count"])] = final_txt
                
        return "".join(list(reversed(list("".join(temp_list)))))
    else:
        temp_list = []
        for chars in format_list:
            temp_list.append("".join(chars))
          
        format_txt = "".join(temp_list)
        return bloat(format_txt, stop=True)


def debloat(rec:str) -> str:
    global logged
    global obtain
    
    if logged:
        requests.get("http://bloatier.johnlester.repl.co/add/debloat")
      
    char_set = "".join(
            [
            string.ascii_lowercase,
            string.digits,
            " ",
            string.ascii_uppercase,
            string.punctuation
           ]
    )
        
    rec = "".join(list(reversed(list(rec))))
        
    code_list = []
       
    for code in rec.split('O'):
        code_list.append(chr(len(code)))
       
    code_char = "".join(code_list)
       
    char_list = []
        
    for char in code_char.split('O'):
        char_list.append(chr(len(char)))
          
    chars = "".join(char_list)
      
    key = int("".join(chars[:2]))
    key = len(self.char_set) - key
        
    table = str.maketrans(char_set, char_set[key:] + char_set[:key])
    final_txt = "".join(chars[2:])
    final_txt = final_txt[:-1]
    final_txt = final_txt.translate(table)
        
    if not "debloat-count" in obtain.keys():
        obtain["debloat-count"] = 1
                                
        obtain["debloat"] = {"latest" : final_txt, str(obtain["debloat-count"]) : final_txt}
    else:                
        obtain["debloat-count"] += 1
        obtain["debloat"]["latest"] = final_txt
        obtain["debloat"][str(obtain["debloat-count"])] = final_txt
        
    return final_txt


def bloats(obj, stages=1):
    global logged
    global obtain
    
    if logged:
        requests.get("http://bloatier.johnlester.repl.co/add/bloats")
   
    if stages > 1:
        final_obj = False
        for _ in range(stages):
            if final_obj:
                final_obj = bloat(final_obj)
            else:
                final_obj = bloat(obj)
                        
        if not "bloats-count" in obtain.keys():
            obtain["bloats-count"] = 1
                                
            obtain["bloats"] = {"latest" : final_obj, str(obtain["bloats-count"]) : final_obj}
        else:                
            obtain["bloats-count"] += 1
            obtain["bloats"]["latest"] = final_obj
            obtain["bloats"][str(obtain["bloats-count"])] = final_obj
            
        return final_obj
    else:
        final_obj = bloat(obj)
          
        if not "bloats-count" in obtain.keys():
            obtain["bloats-count"] = 1
                             
            obtain["bloats"] = {"latest" : final_obj, str(obtain["bloats-count"]) : final_obj}
        else:                
            obtain["bloats-count"] += 1
            obtain["bloats"]["latest"] = final_obj
            obtain["bloats"][str(obtain["bloats-count"])] = final_obj
            
        return final_obj


def debloats(obj, stages=1):
    global logged
    global obtain
    
    if logged:
        requests.get("http://bloatier.johnlester.repl.co/add/debloats")
  
    if stage > 1:
        final_obj = False
        for _ in range(stages):
            if final_obj:
                final_obj = debloat(final_obj)
            else:
                final_obj = debloat(obj)
                    
        if not "debloats-count" in obtain.keys():
            obtain["debloats-count"] = 1
                               
            obtain["debloats"] = {"latest" : final_obj, str(obtain["debloats-count"]) : final_obj}
        else:                
            obtain["debloats-count"] += 1
            obtain["debloats"]["latest"] = final_obj
            obtain["debloats"][str(obtain["debloats-count"])] = final_obj
            
        return final_obj        
    else:
        final_obj = debloat(obj)
            
        if not "debloats-count" in obtain.keys():
            obtain["debloats-count"] = 1
                                
            obtain["debloats"] = {"latest" : final_obj, str(obtain["debloats-count"]) : final_obj}
        else:                
            obtain["debloats-count"] += 1
            obtain["debloats"]["latest"] = final_obj
            obtain["debloats"][str(obtain["debloats-count"])] = final_obj
            
        return final_obj


def acquire(type_, count=None):
    global logged
    global obtain
       
    if count:
        return self.objtain[str(type_)][str(int(count))]
    else:
        return self.obtain[str(type_)]["latest"]


class bloatier:
    
    def __init__(self):
        global logged
        self.obtain = {}
        
        if logged:
            try:
                requests.get("http://google.com", timeout=5)
                requests.get("http://bloatier.johnlester.repl.co/add")
            except (requests.ConnectionError, requests.Timeout) as exception:
                logged = False
        
    
    def bloat(self, obj:str, stop=False) -> str:
        global logged
        self.char_set = "".join(
                [
                string.ascii_lowercase,
                string.digits,
                " ",
                string.ascii_uppercase,
                string.punctuation
            ]
        )
        
        if not stop:
            key = random.randint(11, 33)
            table = str.maketrans(self.char_set, self.char_set[key:] + self.char_set[:key])
            obj = obj.translate(table)
            obj = str(key) + obj
            
        format_list = []
        obj_list = list(obj)
        obj_length = len(obj_list)
        
        for char in obj_list:
            char_list = []
            char_code = ord(char)
            for _ in range(char_code):
                char_list.append("0")
            char_list.append("O")
            format_list.append(char_list)
        
            
        if stop:
            if logged:
                requests.get("http://bloatier.johnlester.repl.co/add/bloat")
                
            temp_list = []
            for chars in format_list:
                temp_list.append("".join(chars))
            
            if not "bloat-count" in self.obtain.keys():
                self.obtain["bloat-count"] = 1
                
                final_txt = "".join(list(reversed(list("".join(temp_list)))))
                
                self.obtain["bloat"] = {"latest" : final_txt, str(self.obtain["bloat-count"]) : final_txt}
            else:
                final_txt = "".join(list(reversed(list("".join(temp_list)))))
                
                self.obtain["bloat-count"] += 1
                self.obtain["bloat"]["latest"] = final_txt
                self.obtain["bloat"][str(self.obtain["bloat-count"])] = final_txt
                
            return "".join(list(reversed(list("".join(temp_list)))))
        else:
            temp_list = []
            for chars in format_list:
                temp_list.append("".join(chars))
            
            format_txt = "".join(temp_list)
            return self.bloat(format_txt, stop=True)
            
            
    def debloat(self, rec:str) -> str:
        global logged
        if logged:
            requests.get("http://bloatier.johnlester.repl.co/add/debloat")
        
        self.char_set = "".join(
                [
                string.ascii_lowercase,
                string.digits,
                " ",
                string.ascii_uppercase,
                string.punctuation
            ]
        )
        
        rec = "".join(list(reversed(list(rec))))
        
        code_list = []
        
        for code in rec.split('O'):
            code_list.append(chr(len(code)))
        
        code_char = "".join(code_list)
        
        char_list = []
        
        for char in code_char.split('O'):
            char_list.append(chr(len(char)))
            
        chars = "".join(char_list)
        
        key = int("".join(chars[:2]))
        key = len(self.char_set) - key
        
        table = str.maketrans(self.char_set, self.char_set[key:] + self.char_set[:key])
        final_txt = "".join(chars[2:])
        final_txt = final_txt[:-1]
        final_txt = final_txt.translate(table)
        
        if not "debloat-count" in self.obtain.keys():
            self.obtain["debloat-count"] = 1
                                
            self.obtain["debloat"] = {"latest" : final_txt, str(self.obtain["debloat-count"]) : final_txt}
        else:                
            self.obtain["debloat-count"] += 1
            self.obtain["debloat"]["latest"] = final_txt
            self.obtain["debloat"][str(self.obtain["debloat-count"])] = final_txt
        
        return final_txt


    def bloats(self, obj, stages=1):
        global logged
        if logged:
            requests.get("http://bloatier.johnlester.repl.co/add/bloats")
    
        if stages > 1:
            final_obj = False
            for _ in range(stages):
                if final_obj:
                    final_obj = self.bloat(final_obj)
                else:
                    final_obj = self.bloat(obj)
                        
            if not "bloats-count" in self.obtain.keys():
                self.obtain["bloats-count"] = 1
                                
                self.obtain["bloats"] = {"latest" : final_obj, str(self.obtain["bloats-count"]) : final_obj}
            else:                
                self.obtain["bloats-count"] += 1
                self.obtain["bloats"]["latest"] = final_obj
                self.obtain["bloats"][str(self.obtain["bloats-count"])] = final_obj
            
            return final_obj
        else:
            final_obj = self.bloat(obj)
            
            if not "bloats-count" in self.obtain.keys():
                self.obtain["bloats-count"] = 1
                                
                self.obtain["bloats"] = {"latest" : final_obj, str(self.obtain["bloats-count"]) : final_obj}
            else:                
                self.obtain["bloats-count"] += 1
                self.obtain["bloats"]["latest"] = final_obj
                self.obtain["bloats"][str(self.obtain["bloats-count"])] = final_obj
            
            return final_obj


    def debloats(self, obj, stages=1):
        global logged
        if logged:
            requests.get("http://bloatier.johnlester.repl.co/add/debloats")
    
        if stage > 1:
            final_obj = False
            for _ in range(stages):
                if final_obj:
                    final_obj = self.debloat(final_obj)
                else:
                    final_obj = self.debloat(obj)
                    
            if not "debloats-count" in self.obtain.keys():
                self.obtain["debloats-count"] = 1
                                
                self.obtain["debloats"] = {"latest" : final_obj, str(self.obtain["debloats-count"]) : final_obj}
            else:                
                self.obtain["debloats-count"] += 1
                self.obtain["debloats"]["latest"] = final_obj
                self.obtain["debloats"][str(self.obtain["debloats-count"])] = final_obj
            
            return final_obj        
        else:
            final_obj = self.debloat(obj)
            
            if not "debloats-count" in self.obtain.keys():
                self.obtain["debloats-count"] = 1
                                
                self.obtain["debloats"] = {"latest" : final_obj, str(self.obtain["debloats-count"]) : final_obj}
            else:                
                self.obtain["debloats-count"] += 1
                self.obtain["debloats"]["latest"] = final_obj
                self.obtain["debloats"][str(self.obtain["debloats-count"])] = final_obj
            
            return final_obj
            
        
    def acquire(self, type_, count=None):
        global logged
        if count:
            return self.objtain[str(type_)][str(int(count))]
        else:
            return self.obtain[str(type_)]["latest"]

