# -*- coding: utf-8 -*- 

from flask import Flask, request, render_template, flash, redirect, url_for, session

import hashlib, uuid, os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/mnt/c/Users'
ALLOWED_EXTENSIONS = set(['txt', 'png', 'pdf', 'jpg', 'jpeg', 'gif'])

import mysql.connector as MS 
connection = MS.connect(user ='root', password ='Justine93@', host='127.0.0.1', buffered=True)
cursor = connection.cursor()

utiliser_bd = "USE colisvip"
cursor.execute(utiliser_bd)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMAGES_PATH'] = UPLOAD_FOLDER

app.config.update(
    DEBUG = True, 
    SECRET_KEY = 'secret_XXX'
)

@app.route('/')
def home():
    if "e_mail" in session:
        return redirect(url_for('my_informations'))
    else :
        return render_template("/login.html")


@app.route('/registration', methods=["GET", "POST"])
def registration ():
    
    error = None 

    if "e_mail" in session:
        return redirect(url_for('my_informations'))


    if request.method == "GET":
        return render_template("enregister.html")
    
    if request.method == "POST":

        """User informations"""

        id_user = int(uuid.uuid4())
        prenom = request.form["prenom"]
        nom = request.form["nom"]
        e_mail = request.form["e_mail"]
        mot_de_passe = request.form["mot_de_passe"]
        mot_de_passe_hash = hashlib.sha3_256(str(mot_de_passe).encode("utf-8")).hexdigest()
        description = request.form["description"]


        """User Adresse Informations"""
        id_adresse = str(uuid.uuid4())
        numero_rue = request.form["numero_rue"]
        nom_rue = request.form["nom_rue"]
        ville = request.form["ville"]
        Code_postal = request.form["cp"]



        """verify if e-mail doesn't yet exist"""

        check_user_exist = "SELECT * FROM USER WHERE Email = '%s' "
        
        cursor.execute(check_user_exist % e_mail)
        check_user_exist_result = cursor.fetchall()
        print(check_user_exist_result)

        '''If we have an e-mail with this adress, we return the following information'''

        if len(check_user_exist_result) > 0 :
            error = 'Cette adresse courriel est déjà utilisee, veuillez utiliser une autre adresse'

            return render_template("enregister.html", error=error)


            """If not we register user information in Data base"""

        else:
            req_enregister_user = "INSERT INTO USER (idUser, firstName, lastName, Email, hashPassword, userDescription) VALUES(%s, %s, %s, %s, %s, %s)"
            cursor.execute(req_enregister_user, (id_user, prenom, nom, e_mail, mot_de_passe_hash, description))
            connection.commit()


            req_enregister_user_adress = "INSERT INTO ADRESS(idAdress, streetNumber, streetName, city, zipCode, idUser) VALUES(%, %s, %s, %s, %s, %s, %s)"
            cursor.execute(req_enregister_user_adress, (id_adresse, numero_rue, nom_rue, ville, Code_postal, id_user))
            connection.commit()
            session["e_mail"] = request.form["e_mail"]


            """Insert image of user by default"""

            req_inserer_image = "INSERT INTO USERPICTURE (idImage, imageDescription, idUser) VALUES (%s, %s, %s)"

            id_image = str(uuid.uuid4())
            image_description = "default.jpg"
            cursor.execute(req_inserer_image % (id_image, image_description, id_user))

            connection.commit()

            return redirect(url_for('my_informations'))



@app.route("/login", methods = ["POST", "GET"])
def authentification():
    error = None
    if request.method == "POST":
        e_mail = request.form["e_mail"]
        mot_de_passe = request.form["mot_de_passe"]
        mot_de_passe_hash = hashlib.sha256(str(mot_de_passe).encode("utf-8")).hexdigest()

        req_user_connection = "SELECT * FROM USER WHERE Email = '%s' AND hashPassWord = '%s'"
        cursor.execute(req_user_connection % (e_mail, mot_de_passe_hash))

        user_connection_result = cursor.fetchall()

        if len(user_connection_result) == 0:
            session['e_mail'] = None
            error = "Cette adresse ou mot de passe ne sont pas valides, veuillez créer un compte "

            return render_template("login.html", error=error)
        
        else :
            

            session['e_mail'] = request.form['e_mail']
            return redirect(url_for("my_informations"))

    elif  request.method == "GET":
        return render_template("login.html")



@app.route("/my_informations", methods =["GET", "POST"])
def informations():

    if request.method =="GET" and 'e_mail' in session :
        e_mail = session["e_mail"]
        req_idUser = "SELECT idUser FORM USER WHERE Email = '%s' "
        cursor.execute(req_idUser % e_mail)

        id_user = cursor.fetchone()
 

        req_user_informations = "SELECT U.firstName, U.lastName, U.Email, A.streetName, A.streetNumber, A.City, A.z ipCode, U.userDescription FROM USER as U, Adress as A WHERE U.idUser = A.idUser AND C.Email = '%s' "
        cursor.execute(req_user_informations % id_user)
        result_req_user_informations = cursor.fetchall()

        req_image = "SELECT U.imgDescription FROM USERPICTURE as U WHERE U.idUser = '%s' "
        cursor.execute(req_image % id_user)
        display_image = cursor.fetchone()
        display_image = display_image[0]
        lieu_image = os.path.join(app.config['UPLOAD_FOLDER'], display_image)

        lieu_image = str(lieu_image)
        print(lieu_image)

        print(result_req_user_informations)
        return render_template("/my_informations.html", result_req_user_informations = result_req_user_informations, lieu_image = lieu_image)

    if request.method =="POST" :
        e_mail = session["e_mail"]


        """ USER Picture """
        req_id_user = "SELECT idUser FROM USER WHERE EMAIL= '%s' "
        cursor.execute(req_id_user % e_mail )
        id_user = cursor.fetchone()
        image = request.files["image"]

        id_image = str(uuid.uuid4())
        image_description = secure_filename(image.filename)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], image_description))

        req_insert_image = "INSERT INTO USERPICTURE (idImage, imageDescription, idUser) VALUES ('%s', '%s', '%s')"
        cursor.execute(req_insert_image % (id_image, image_description, id_user[0]))

        connection.commit()
        flash("votre image est enregistree")

        return redirect(url_for('my_informations'))
    else:
        return redirect(url_for('login'))
    
app.run(port="4040")
app.config["DEBUG"] = True



