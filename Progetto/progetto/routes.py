from flask import render_template, url_for, flash, redirect, request
from progetto import app, bcrypt, db
from progetto.forms import RegistrationForm, LoginForm, UpdateAccountForm, InsuranceForm
from progetto.models import User, insurance_calculation
from flask_login import login_user, current_user, logout_user, login_required
from bson.objectid import ObjectId

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/area_clienti", methods=['GET', 'POST'])
def area_clienti():
    if current_user.is_authenticated: # se l'utente è già loggato
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit(): # verifica se il modulo è stato inviato correttamente e se i dati inseriti sono validi.
        user = User.get_by_email(form.email.data) 
        if user and bcrypt.check_password_hash(user.password, form.password.data): ## verifica se  viene l'email e la password è corretta 
            login_user(user, remember=form.remember.data)
            return redirect(url_for('account'))
        else:
            flash('Accesso non riuscito. Controlla e-mail e password', 'danger')
    return render_template('AreaClienti.html', form=form)


@app.route("/registrazione", methods=['GET', 'POST'])
def registrazione():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = RegistrationForm()    
    if form.validate_on_submit():
        # genera un hash che serve per crittografare la password dell'utente prima di salvarla nel database.
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        User.create(nome=form.nome.data, cognome=form.cognome.data, email=form.email.data, password=hashed_password)
        flash('Il tuo account è stato creato! Ora puoi fare il login', 'success')
        return redirect(url_for('area_clienti'))
    return render_template('Registrazione.html', form=form)

@app.route("/logout")
def logout():
    logout_user() # comando di flask-login per disconnessione
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required  # Questo decoratore protegge la pagina da utenti non autenticati
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.nome = form.nome.data
        current_user.cognome = form.cognome.data
        current_user.email = form.email.data
        db.users.update_one( {"_id": ObjectId(current_user.id)},
        {"$set": { "nome": form.nome.data, "cognome": form.cognome.data, "email": form.email.data }}
        ) 
        flash('Aggiornamento effettuato!', 'success')  
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.nome.data = current_user.nome
        form.cognome.data = current_user.cognome
        form.email.data = current_user.email
        return render_template('account.html', form=form)

@app.route("/calcolo", methods=['GET', 'POST'])
def calcolo():
    form = InsuranceForm()
    calcolo = 0
    if form.validate_on_submit():
        eta = form.eta.data
        cilindrata = form.cilindrata.data
        sinistri = form.sinistri.data
        chilometri = form.chilometri.data
        classe_merito = form.classe_merito.data
        calcolo = insurance_calculation(eta, cilindrata, sinistri, chilometri, classe_merito)

        insurance = {
            "user_id": current_user.id, # id dell'utente utenticato
            "eta": eta,
            "cilindrata": cilindrata,
            "sinistri": sinistri,
            "chilometri": chilometri,
            "classe_merito": classe_merito,
            "calcolo": calcolo,
        }
        user_insurance = db.insurance.find_one({"user_id": current_user.id})
        if user_insurance:
            db.insurance.update_one({"user_id": current_user.id},
            {"$set": {
                        "eta": form.eta.data, 
                        "cilindrata": form.cilindrata.data,
                        "sinistri": form.sinistri.data,
                        "chilometri": form.chilometri.data,
                        "classe_merito": form.classe_merito.data,
                        "calcolo": calcolo,
                     }}) 
            flash('Calcolo aggiornato correttamente!', 'success')
        else:
            db.insurance.insert_one(insurance)
        flash('Calcolo nuovo inserito correttamente!', 'success')
        return redirect(url_for('insurance_results'))  
    return render_template('calcolo.html', form=form, calcolo=calcolo)



@app.route("/insurance_results")
@login_required  # Questo decoratore assicura che l'utente sia autenticato
def insurance_results():
    # recupera i dati di utente e calcolo preventivo
    user_data = db.users.find_one({"_id": ObjectId(current_user.id)})
    user_insurance = db.insurance.find_one({"user_id": current_user.id})

    print("Dati utente:", user_data)
    print("Dati assicurazione:", user_insurance)

    if user_insurance and user_data:
        return render_template("account.html", user=user_data, insurance=user_insurance)
    else:
        flash("Nessun calcolo trovato per l'utente", 'danger')
        return redirect(url_for("account"))
