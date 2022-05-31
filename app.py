from flask import Flask,render_template,request
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(host="home.marcinkwapisz.pl", port='2137', database='magazyn', user='postgres', password='secretpassword')
cur = conn.cursor()


def get_data(sql):
    cur.execute(sql)
    x = cur.fetchall()
    return x


@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html')


@app.route('/zamowienie')
def zamowienie():
    request.args.get("id")
    x = get_data('SELECT P."id", P."Nazwa", M."Nazwa", K."Nazwa", PZ."Ilosc_produktow" from magazyn."Pozycje_zamowienia" PZ '
                 'join magazyn."Produkty" P on P.id = PZ."ID_Produkt" join magazyn."Kolor" K on K.id = P."ID_Kolor" '
                 'join magazyn."Marka" M on M.id = P."ID_Marka" where PZ."ID_Zamowienia" = '+request.args.get("id"))
    return render_template('zamowienie.html', data=x, headers=['ID', 'Nazwa', 'Producent', 'Kolor', 'Ilość sztuk'])


@app.route('/dostawa')
def dostawa():
    request.args.get("id")
    x = get_data('select P."Nazwa",K."Nazwa", K2."Nazwa", M."Nazwa", magazyn."Dostawy_produkty"."Ilosc_produktow" from magazyn."Dostawy_produkty" join magazyn."Produkty" P on P.id = "Dostawy_produkty"."ID_Produkt" join magazyn."Kolor" K on K.id = P."ID_Kolor" join magazyn."Kategorie" K2 on K2.id = P."ID_Kategoria" join magazyn."Marka" M on M.id = P."ID_Marka" where magazyn."Dostawy_produkty"."id" = '+request.args.get("id"))
    return render_template('dostawa.html', data=x, headers=['Nazwa', 'Kolor', 'Kategoria', 'Producent', 'Ilość sztuk'])


@app.route('/wyslane')
def wyslane():
    request.args.get("id")
    x = get_data('SELECT magazyn."Zamowienia".id,P."Imie",P."Nazwisko",K."Imie",K."Nazwisko",Zs."Status" FROM magazyn."Zamowienia" join magazyn."Klienci" K on K.id = "Zamowienia"."ID_Klient" join magazyn."Pracownicy" P on P.id = "Zamowienia"."ID_Pracownik" join magazyn."Zamowienia_status" Zs on Zs.id = "Zamowienia"."Status" where magazyn."Zamowienia"."Status" = 2;')
    return render_template('wyslane.html', data=x, headers=['ID', 'Pracownik Imie', 'Pracownik Nazwisko', 'Klient Imie', 'Klient Nazwisko', 'Status', 'Szczegóły'])


@app.route('/produkty')
def produkty():
    request.args.get("id")
    x = get_data('SELECT magazyn."Produkty"."id", magazyn."Produkty"."Nazwa", K."Nazwa", '
                 'magazyn."Produkty"."Cena", M."Nazwa", K2."Nazwa", R."Nazwa", magazyn."Produkty"."Ilosc" '
                 'from magazyn."Produkty" join magazyn."Kategorie" K on K.id = "Produkty"."ID_Kategoria" '
                 'join magazyn."Kolor" K2 on K2.id = "Produkty"."ID_Kolor" join magazyn."Marka" M on '
                 'M.id = "Produkty"."ID_Marka" join magazyn."Rozmiar" R on R.id = "Produkty"."ID_Rozmiar"')
    return render_template('produkty.html', data=x, headers=['ID', 'Nazwa',
                                                             'Kategoria','Cena','Marka','Kolor','Rozmiar','Ilość'])


@app.route('/zamowienia')
def zamowienia():
    x = get_data('SELECT magazyn."Zamowienia".id,P."Imie",P."Nazwisko",K."Imie",K."Nazwisko",'
                 'Zs."Status" FROM magazyn."Zamowienia" join magazyn."Klienci" K on K.id = '
                 '"Zamowienia"."ID_Klient" join magazyn."Pracownicy" P on P.id = "Zamowienia"."ID_Pracownik" '
                 'join magazyn."Zamowienia_status" Zs on Zs.id = "Zamowienia"."Status";')
    return render_template('zamowienia.html', data=x, headers=['ID', 'Pracownik Imie',
                                                               'Pracownik Nazwisko', 'Klient Imie',
                                                               'Klient Nazwisko', 'Status', 'Szczegóły'])


@app.route('/wskaznik')
def wskaznik():
    x = get_data('select P.*, count(Z.id)+count(D.id) from magazyn."Pracownicy" P join magazyn."Zamowienia" Z'
                 ' on P.id = Z."ID_Pracownik" join magazyn."Dostawy" D on P.id = D."ID_Pracownik" '
                 'group by P.id')
    return render_template('wskaznik.html', data=x, headers=['ID', 'Pracownik Imie', 'Pracownik Nazwisko', 'Wskaźnik efektywności pracy'])


@app.route('/klienci')
def klienci():
    x = get_data('select K.id, K."Imie", K."Nazwisko", A."Kod_pocztowy", A."Miasto", A."Ulica", A."Numer_dom", K2."Mail", K2."Telefon", count(Z.id) from magazyn."Klienci" K join magazyn."Zamowienia" Z on K.id = Z."ID_Klient" join magazyn."Adres" A on A.id = K."ID_Adres" join magazyn."Kontakt" K2 on K2.id = K."ID_Kontakt" group by K.id')
    return render_template('klienci.html', data=x, headers=['ID', 'Klient Imie', 'Klient Nazwisko', 'Kod pocztowy', 'Miasto', 'Ulica', 'Numer domu', 'Mail', 'Telefon', 'Ilość zamówień'])


@app.route('/dostawy')
def dostawy():
    x = get_data('select magazyn."Dostawy".id, D."Nazwa_dostawcy", P."Imie", P."Nazwisko" from magazyn."Dostawy" join magazyn."Dostawcy" D on D.id = "Dostawy"."ID_Dostawca" join magazyn."Pracownicy" P on P.id = "Dostawy"."ID_Pracownik"')
    return render_template('dostawy.html', data=x, headers=['ID', 'Nazwa dostawcy', 'Pracownik Imię', 'Pracownik Nazwisko'])


if __name__ == '__main__':
    app.run()



