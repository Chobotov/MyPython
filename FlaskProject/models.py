from flask_login import login_required,login_user,logout_user,LoginManager,UserMixin

NumberOfUser = 0
Dict = dict()

class User(UserMixin):
    def __init__(self,id):
        self.id = id
    def set_info(self,name,password):
        self.name = name
        self.password = password
        addNewUser(name,password)
    def get_info(self):
        return "%d %s %s" % (self.id,self.name,self.password)

def addNewUser(name,password):
    Dict[password] = name