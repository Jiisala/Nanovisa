# NanoVisa

Alustava hahmotelma sovelluksesta
- Roolit: Käyttäjä, Moderaattori

- Tietovisasovellus monivalintakysmyksillä. 
- Jokainen käyttäjä voi sekä pelata visaa, että lisätä omia kysmyksiä.
- Kysymykset luokitellaan avainsanoin lisäämisen yhteydessä
- Käyttäjä luo itselleen visan antamalla hakuehdot
   - esim: 
   määrä: 10 
   aiheet: limasienet, laamat, 80-luku
   vaikeusaste: 5/5 (tämä määritellään sen mukaan kuinka suuri osa edellisistä vastaajista on vastannut oikein)
   täytä puttuvat satunnaisilla: Kyllä (jos siis ei löydy tarvittamaa määrää annetuilla ehdoilla peli joko antaa vähemmän kysymyksiä tai arpoo loput)
   
- Oletuksena peli ei valitse käyttäjän itsensä lisäämiä kysymyksiä, mutta tämän voi ehkä muuttaa asetuksissa.
- Peli pitää highscore listaa kaikista käyttäjistä, omiin kysymyksiin vastaamisesta ei saa pisteitä.
- Peli pitää kirjaa siitä mihin kysmyksiin käyttäjä on jo vastannut, samaan kysymykseen uudestaan vastaaminen ei tuo pisteitä
- Käyttäjä voi merkitä kysymyksen virheelliseksi/loukkaavaksi jolloin kysymys piilotetaan.
- Käyttäjä voi nähdä tilastoja omasta pelaamisestaam (näiden tarkempi sisältö tarkentuu kunhan kerkiän miettiä asiaa enemmän)

- Moderaattori voi tarkistaa piilotetut kysymyksent ja joko poistaa ne tai tuoda takaisin peliin. 
- Moderaattori voi myös poistaa käyttäjän
- Moderaattori voi tarkastella ja muokata muitakin lisättyjä kysymyksiä (esim. lisätä avainsanoja)
- MOderaattori ei voi saada pisteitä pelaamisesta eikä päästä highscore listalle
