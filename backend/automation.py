from enum import Enum
class Permission(str, Enum): OBSERVE='observe'; SUGGEST='suggest'; CONFIRM='confirm'; EXECUTE='execute'
class Automation:
    def __init__(self): self.items=[]
    def create(self,name,trigger,action,permission='confirm'):
        item={'id':f'auto-{len(self.items)+1}','name':name,'trigger':trigger,'action':action,'permission':permission,'enabled':True}
        self.items.append(item); return item
    def list(self): return self.items
automations=Automation()
