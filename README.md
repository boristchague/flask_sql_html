
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Registration</title>
</head>

<body>
    <center> 
        <div class="wrapper"> 
            <div class="card"> 

                {% if error %}
                <p clas="error"> <stront>Erreur : </stront> {{ error }} </p>
                {% endif %}

                <h1> Créer un compte </h1>

                <form title="information" method="POST"> 
                    <label type="text">Prenom 

                    </label>
                    <input type="text"  cols="25" name="prenom"  maxlength="25" required/> <br>

                    <label type="text" for="">Nom </label><input  type="text"  name="nom"  maxlength="35" required/><br>

                    <label type="text" for="e_mail">Email </label> <input  type="text"  name="e_mail" placeholder="@gmail.com" maxlength="50" required/><br>

                    <label type="text" for="mot_de_passe"> Mot de passe </label> <input  type="password"  name="mot_de_passe"  maxlength="50" required/><br>

                    <label type="text">Description </label> <textarea type="text"  name="description"  maxlength="256"> Description... </textarea><br> <br>


                    <p> Adresse</p>

                    <label type="text" for="numero_rue"> N* de Rue </label><input type="text" name="numero_rue" maxlength="4" required/> <br>

                    <label type="text" for="nom_rue"> Nom de rue </label><input type="text" name="nom_rue" maxlength="50" required/> <br>

                    <label type="text" for="ville"> Ville </label><input type="text" name="ville" maxlength="30" required/> <br>

                    <label type="text" for="code_postal"> Code postal </label><input type="text" name="cp" maxlength="6" required/> <br> 


                    <input type="submit" value="S'enregistrer">
                    
                </form>
            </div>

        </div>
    </center>
</body>
</html>




@app.route('/')
def home():
    if "e_mail" in session:
        return redirect(url_for('my_informations'))
    else :
        return render_template("/login.html")
    




