<img width="996" height="178" alt="image" src="https://github.com/user-attachments/assets/e3ef4e9a-837d-4bfb-b1e0-8ee1d0bf6905" />
1. Inițializare și Citirea Datelor:
       * Scriptul începe prin a citi două fișiere: dex.txt, care servește ca dicționar de referință, și cuvinte_de_verificat.txt, care conține cuvintele ce trebuie ghicite.
       * Funcția read_words este capabilă să proceseze diferite formate de text și curăță cuvintele, aducându-le la o formă standard (litere mici, fără spații extra).

   2. Strategia de Rezolvare (Funcția `solve_hangman`):
       * Pentru fiecare cuvânt secret, algoritmul filtrează inițial dicționarul pentru a păstra doar cuvintele care au aceeași lungime.
       * Intră într-o buclă de ghicire care continuă până când cuvântul este complet descoperit sau se atinge numărul maxim de greșeli (6).
       * Mecanismul de Ghicire:
           1. La fiecare pas, calculează frecvența de apariție a literelor în lista de cuvinte posibile rămase.
           2. Alege ca următoare literă de încercat pe cea mai frecventă care nu a mai fost ghicită până acum. Aceasta este cea mai probabilă literă corectă.
       * Actualizare și Filtrare:
           * Dacă litera este corectă, starea cuvântului de ghicit este actualizată (de ex: _ a _ a).
           * Dacă este greșită, este adăugată la o listă de litere incorecte.
           * După fiecare ghicire, lista de cuvinte posibile este rafinată: sunt eliminate cuvintele care conțin litere ghicite greșit sau care nu se potrivesc cu starea curentă a cuvântului parțial descoperit.

   3. Execuția Principală și Raportarea (Funcția `main`):
       * Funcția main orchestrează întregul proces: citește datele, iterează prin fiecare cuvânt de ghicit și apelează solve_hangman.
       * Monitorizează performanța, măsurând timpul total de execuție.
       * La final, afișează un raport detaliat care include:
           * Timpul total și mediu de rezolvare per cuvânt.
           * Numărul total de litere încercate.
           * Rata de succes (câte cuvinte au fost ghicite corect din total).

  Scriptul folosește expresii regulate pentru a valida cuvintele conform alfabetului român și structuri de date eficiente precum collections.defaultdict pentru a număra frecvențele.
