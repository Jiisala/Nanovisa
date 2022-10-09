# NanoVisa

NanoVisa on tietokilpailusovellus jossa käyttäjät voivat itse luoda kysymyksiä ja vastata toistensa kysymyksiin. Kysymyksistä voi luoda haluamansa pituisen setin ja avainsanoilla voi rajata kysymysvalikoimaa koskemaan tiettyjä aihealueita.

Sovellus on testattavissa Herokussa
[https://nanovisa.herokuapp.com/](https://nanovisa.herokuapp.com/)

Tämän hetkinen tila:

Projektin toiminnallisuus on toteutettu suurimmaksi osaksi, ulkoasun siistimistä ei ole vielä edes aloitettu

- Käyttäjän lisääminen ja sisäsisäänkirjautuminenänkirjautuminen toimivat. Ne noudattelevat esimerkkisovelluksen logiikkaa, mutta oletan ettei ole tarkoitus keksiä pyörää uudestaan.
- Kysymyksiä voi lisätä.
- Kysymys-settejä voi muodostaa ja niihin voi vastata.
- Pistelasku toimii melkein, bugi jonka olen jo yksilöinyt vaivaa vielä.
  (yritin tallettaa session dataan liikaa tietoa, ratkaisuksi ajattelin server side sessiota, mutta sen toteuttaminen jää myöhemmäksi).
- kysymyksiä voi ilmiantaa ylläpidolle tarkistettaviksi
- ylläpitäjä voi tarkistaa kysymyksiä ja poistaa niitä.

Seuraavat askeleet:

- loput admin toiminnallisuudet
- käyttäjän profiilisivu
- ulkoasu
- tällä hetkellä moni syötekenttä validoidaan vain selaimessa, olisi varmaan syytä validoida ne myös bäkkärin puolella
- monesta kohdasta puuttuu vielä käyttäjälle annettu palaute toiminnasta
- ja tietysti bugien korjaus

### -- Tästä alaspäin alkuperäinen suunnitelma --

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
