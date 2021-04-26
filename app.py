from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)


class respondent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plec = db.Column(db.String(100))
    wiek = db.Column(db.String(50))
    miejscowosc = db.Column(db.String(200))
    uczelnia = db.Column(db.String(100))
    uslugi = db.Column(db.String(10))
    stany = db.Column(db.String(20))

    def __init__(self, plec, wiek, miejscowosc, uczelnia, uslugi,stany):
        self.plec = plec
        self.wiek = wiek
        self.miejscowosc = miejscowosc
        self.uczelnia = uczelnia
        self.uslugi = uslugi
        self.stany = stany


class wiedza(db.Model):
    id = db.Column( db.Integer, primary_key=True)
    cierp_mez=db.Column(db.String(100))
    znajomosc = db.Column(db.String(100))
    narazony = db.Column(db.String(100))
    objawy_wiek = db.Column(db.String(100))
    cierposob = db.Column(db.Numeric)
    geny = db.Column(db.String(100))

    def __init__(self, cierp_mez, znajomosc, narazony, objawy_wiek, cierposob, geny):
        self.cierp_mez = cierp_mez
        self.znajomosc = znajomosc
        self.narazony = narazony
        self.objawy_wiek = objawy_wiek
        self.cierposob = cierposob
        self.geny = geny


class akceptacja(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alien = db.Column(db.String(100))
    wies = db.Column(db.String(100))
    wspolpraca = db.Column(db.String(100))
    partner = db.Column(db.String(100))
    media = db.Column(db.String(100))

    def __init__(self, alien, wies, wspolpraca, partner, media):
        self.alien = alien
        self.wies = wies
        self.wspolpraca = wspolpraca
        self.partner = partner
        self.media = media




@app.route('/')
def start():
    return render_template('show_all.html', respondents=respondent.query.all())


@app.route('/wynik')
def show_all():
    return render_template('wyniki.html', respondent=respondent.query.all(), wiedza=wiedza.query.all(), akceptacja=akceptacja.query.all())


@app.route('/ankieta', methods=['GET', 'POST'])
def new():
    if request.method == 'POST':
        if not request.form['wiek'] or not request.form['miejscowosc'] or not request.form['uczelnia'] \
                or not request.form['uslugi'] or not request.form['stany'] or not request.form['cierp_mez'] \
                or not request.form['znajomosc'] or not request.form['narazony'] or not request.form['objawywiek'] \
                or not request.form['cierposob'] or not request.form['geny'] or not request.form['alien'] or not request.form['wies'] \
                or not request.form['wspolpraca'] or not request.form['partner'] or not request.form['media']:
            flash('Proszę uzupełnić wszystkie pola', 'error')
        else:
            resp = respondent(request.form['plec'], request.form['wiek'],request.form['miejscowosc'], request.form['uczelnia'], request.form['uslugi'], request.form['stany'])
            wiedz= wiedza(request.form['cierp_mez'], request.form['znajomosc'], request.form['narazony'], request.form['objawywiek'], request.form['cierposob'], request.form['geny'])
            akc = akceptacja(request.form['alien'], request.form['wspolpraca'], request.form['partner'],request.form['wies'], request.form['media'])
            db.session.add(resp)
            db.session.add(wiedz)
            db.session.add(akc)

            db.session.commit()
            #flash('Record was successfully added') -- może być Wynik głosowania został zapisany
            return render_template('koncowa.html')
            #return redirect(url_for('show_all.html'))
    return render_template('pytania.html')


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)