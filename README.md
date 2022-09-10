# NanoVisa

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
