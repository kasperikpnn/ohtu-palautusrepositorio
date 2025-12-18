Copilot teki koodistani tälläisiä huomioita:
- koodissani luki näin aluksi: ``score_difference = self.player1_score-self.player2_score``. Copilot ehdotti välilyöntien lisäämistä miinuksen ympärille Pythonin tyyliohjenuorien mukaisesti.
- koodissani oli else-lause, jonka jätin kaiken varalta joka johtaa erroriin, ja Copilot ehdotti sen poistamista, mikä on hyvä ajatus sillä aiemmat if-lauseet kattavat jo kaikki mahdolliset tapaukset.
- score_as_tennis_call palauttaa listasta ``["Love, "Fifteen", "Thirty", "Forty"]`` neljännen indeksin arvon (jota ei ole), jos sitä kutsutaan luvulla 4. Tätä ei pitäisi ikinä tapahtua, mutta korjasin virheen joka tapauksessa.
- score_as_tennis_call palautti alunperin "Deuce", jos siltä pyydettiin palauttamaan neljä tai sitä korkeampi indeksi. Tälle ei ole tarvetta, sillä funktion pitäisi käsitellä vain arvoja 0-3 väliltä. Copilot ehdotti tämän korvaamista ValueErrorilla, ja tein niin.

Ehdotetut muutokset olivat erittäin hyviä ja toteutin jokaisen niistä. Koin Copilotin tekemän katselmoinnin erittäin hyödylliseksi: vaikka virheitä ei juurikaan ollut, sen antamat ehdotukset tekivät koodistani enemmän Pythonin tyyliohjeiden ja yleisten käytäntöjen mukaisen.
