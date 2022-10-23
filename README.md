# NanoVisa

NanoVisa on tietokilpailusovellus jossa käyttäjät voivat itse luoda kysymyksiä ja vastata toistensa kysymyksiin. Kysymyksistä voi luoda haluamansa pituisen setin ja avainsanoilla voi rajata kysymysvalikoimaa koskemaan tiettyjä aihealueita.

Sovellus on testattavissa Herokussa
Herokuun on luotu testi käyttäjä, sekä testi admin. Voit toki myös luoda oman käyttäjän, se on jopa suositeltavaa. Uutta admin-käyttäjää ei voi luoda sovelluksessa suoraan. Ylläpitäjä voi lisätä toiselle käyttäjälle ylläpito-oikeudet (tai poistaa ne). Tämä tapahtuu käyttäjän ID:n avulla. 

### HUOM! 
### testikäyttäjä: nimi testi, salasana testi
### testi ylläpitäjä: nimi testiadmin, salasana testiadmin 
 
testikäyttäjän ID on 1.

testiadmin ID on 9, älä poista ylläpitäjän oikeuksia tältä käyttäjältä, ellet ole ensin lisännyt niitä jollekkin toiselle. Muutoin ainoa tapa luoda uusi ylläpitäjä on suoraan tietokantaa muokkaamalla.

[https://nanovisa.herokuapp.com/](https://nanovisa.herokuapp.com/)

Loppupalautus:

Projektin tämä versio on valmis.


- Käyttäjän lisääminen ja sisäsisäänkirjautuminen toimivat.
- Kysymyksiä voi lisätä.
- Kysymyksiä lisätessä ja kysymys-settejä luodessa, ohjelma antaa ehdotuksia avainsana kenttiin kun alat kirjoittamaan. Nämä perustuvat tietokantaan jo lisättyihin avainsanoihin.
- Kysymys-settejä voi muodostaa ja niihin voi vastata.
- Pistelasku toimii, pisteitä saa vain muiden lisäämistä kysymyksistä, joihin käyttäjä vastaa ensimmäisen kerran.
- Ylläpitäjät eivät saa pisteitä vaikka pelaisivat.
- Highscore lista toimii.
- Pelin jälkeen näytetään tulos-sivu josta näkee sen kierroksen kysymykset ja ansaitut pisteet.
- Tulos-sivulla voi myös ilmiantaa kysymyksiä ylläpidolle tarkistettaviksi.
- Käyttäjällä on profiilisivu jossa näkee tietoja pelatuista peleistä, sekä käyttäjän itsensä lisäämät kysymykset.
- Käyttäjä voi poistaa ja muokata omia kysymyksiään.
- Käyttäjät voivat lähettää viestejä toisilleen ja ylläpidolle.


- Ylläpitäjä voi tarkistaa kysymyksiä ja poistaa, tai muokata niitä.
- Ylläpitäjä voi vaihtaa käyttäjän roolia ylläpitäjäksi, tai toisin päin. Tämä tapahtuu käyttäjän ID:n avulla. Sen voisi myös tehdä käyttäjän nimellä, toiminnallisuus siihen on luotu samalla kuin viestien lähettäminen, mutta en ehtinyt ottaa sitä käyttöön tässä kohtaa ohjelmaa.


- Ohjelman ulkoasu on toteutettu CSS:llä ilman ulkoisia ulkoasukirjastoja.
- Ohjelmassa ei ole bugeja joista tietäisin, toisaalta sillä testaus ei kuulunut kurssin aihealueisiin, en sitä myöskään toteuttanut. On siis aivan mahdollista että niitä siellä siis lurkkii piiloissaan.


- Ohjelman toimintaa on testattu käsin chrome ja firefox selaimilla. Chromella eivät tavuviivat toimi sanoja jakaessa. Tämä on ilmeisesti tunnettu ongelma jolle en löytänyt järkevää ratkaisua. Ruutu myös välähtää ikävästi kun kysymykseen vastatessa ladataan uutta sivua. Firefoxilla näitä ongelmia ei ole. 
- Ohjelma on myös testattu ja todettu toimivaksi kännykällä (sony/android).


- Vscoden automaattimuotoilu tuntui vihaavan Jinjaa. Pyrin pitämään myös HTML-tiedostot jokseenkin luettavina, mutta ne joissa on enemmän Jinja-koodia ovat ehkä silti hieman vaikeaselkoisia.

Mikäli joskus palaan tämän pariin:

- Kattava testaus
- Ulkoasun hiominen
- Viesti toiminnon parantaminen, tällaisenaan se on hieman torso, viestejä ei esim. ketjuteta järkevästi, eikä niitä voi poistaa. 
- Koodin refaktorointi, toteutin tätä tehdessäni ensimmäisen sovellukseni python/flask/jinja yhdistelmällä ja opin tehdessäni runsaasti siitä kuinka asiat kannattaa toteuttaa. Tästä johtuen, alkupäässä kirjoittamani koodin seassa on joitakin kohtia, joista tiedän jo kuinka tehdä ne fiksummin. Koska kyseessä on aikataulutettu kurssi ja deadline on nyt, se jääköön tulevasuuteen.
- Ja tietysti niiden mahdollisten bugien korjaus.


### -- Tästä alaspäin alkuperäinen suunnitelma, joka on tehty kurssin viikolla 1 --

Alustava hahmotelma sovelluksesta. Tämä tulee varmasti elämään projektin edetessä.

- Roolit: Käyttäjä, Moderaattori

- Tietovisasovellus monivalintakysymyksillä.
- Jokainen käyttäjä voi sekä pelata visaa, että lisätä omia kysymyksiä.
- Kysymykset luokitellaan avainsanoin lisäämisen yhteydessä
- Käyttäjä luo itselleen visan antamalla hakuehdot esim:

  - määrä: 10

  - aiheet: limasienet, laamat, 80-luku

  - vaikeusaste: 3/5 (tämä määritellään sen mukaan kuinka suuri osa edellisistä vastaajista on vastannut oikein)

  - täytä puuttuvat satunnaisilla: Kyllä (jos siis ei löydy tarvittavaa määrää annetuilla ehdoilla peli joko antaa vähemmän kysymyksiä tai arpoo loput)

- Oletuksena peli ei valitse käyttäjän itsensä lisäämiä kysymyksiä, mutta tämän voi ehkä muuttaa asetuksissa.
- Peli pitää highscore listaa kaikista käyttäjistä, omiin kysymyksiin vastaamisesta ei saa pisteitä.
- Peli pitää kirjaa siitä mihin kysymyksiin käyttäjä on jo vastannut, samaan kysymykseen uudestaan vastaaminen ei tuo pisteitä
- Käyttäjä voi merkitä kysymyksen virheelliseksi/loukkaavaksi jolloin kysymys piilotetaan.
- Käyttäjä voi nähdä tilastoja omasta pelaamisestaan (näiden tarkempi sisältö tarkentuu kunhan kerkiän miettiä asiaa enemmän)
- Myös muita hienoja ja hyödyllisiä tilastoja voi tarkastella

- Moderaattori voi tarkistaa piilotetut kysymykset ja joko poistaa ne tai tuoda takaisin peliin.
- Moderaattori voi myös poistaa käyttäjän
- Moderaattori voi tarkastella ja muokata muitakin lisättyjä kysymyksiä (esim. lisätä avainsanoja)
- Moderaattori ei voi saada pisteitä pelaamisesta eikä päästä highscore listalle

- Käyttäjä ja moderaattori voivat keskustella viestein.

- Jos tuntuu että aika on liialti ja ominaisuuksia voi lisätä loputtomiin, lisätään moderaattorille mahdollisuus järjestää pelejä/turnauksia joissa on omat pisteensä.
