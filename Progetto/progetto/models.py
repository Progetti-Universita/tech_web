from progetto import db, login_manager
from flask_login import UserMixin
from bson.objectid import ObjectId

# recupero dei dati dopo l'accesso attraverso l'id
@login_manager.user_loader
def load_user(user_id):
    user_data = db.users.find_one({"_id": ObjectId(user_id)})
    return User(user_data) if user_data else None


class User(UserMixin):
    def __init__(self, user_data): 
        self.id = str(user_data["_id"])
        self.nome = user_data.get("nome")  
        self.cognome = user_data.get("cognome")  
        self.email = user_data.get("email")
        self.password = user_data.get("password")

    @staticmethod
    def get_by_email(email):
        user_data = db.users.find_one({"email": email})
        return User(user_data) if user_data else None

        
    # serve per creare un nuovo utente nel database
    @staticmethod
    def create(nome, cognome, email, password):
        user = {
            "nome": nome,
            "cognome": cognome,
            "email": email,
            "password": password,
        }
        db.users.insert_one(user)

def insurance_calculation(eta, cilindrata, sinistri, chilometri, classe_merito):
    prezzo_base = 100
    if eta > 25:
        eta = 50
    else:
        eta = 100

    cilindrata = cilindrata / 200 * 50
    sinistri = sinistri * 100

    if chilometri > 50000:
        chilometri = 25
    else:
        chilometri = 50
    
    classe_merito *= 20
    calcolo = prezzo_base + eta + cilindrata + sinistri + chilometri + classe_merito

    return calcolo

