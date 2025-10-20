# Importă modulele necesare pentru program.
import collections  # Pentru structuri de date avansate, cum ar fi defaultdict.
import re  # Pentru a lucra cu expresii regulate (căutare de modele în text).
import sys  # Pentru a interacționa cu sistemul, în special cu setările consolei.
import time  # Pentru a măsura timpul de execuție.

# Reconfigurează consola (stdout) pentru a gestiona corect caracterele UTF-8.
# Acest lucru previne erorile la afișarea diacriticelor românești în consolă.
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')


def read_words(file_path, is_dex=False):
    """
    Citește cuvinte dintr-un fișier, gestionând diferite formate.

    Args:
        file_path (str): Calea către fișierul de citit.
        is_dex (bool): Un flag care indică dacă fișierul este dicționarul (dex.txt).

    Returns:
        list: O listă de cuvinte extrase din fișier.
    """
    words = []
    try:
        # Deschide fișierul cu encodare UTF-8 pentru a citi corect diacriticele.
        with open(file_path, 'r', encoding='utf-8') as f:
            # Parcurge fiecare linie din fișier.
            for line in f:
                # Curăță linia de spații la început și la sfârșit și o convertește la litere mici.
                line = line.strip().lower()
                if not line:
                    continue  # Ignoră liniile goale.

                # Verifică dacă fișierul este dicționarul dex.txt.
                if is_dex:
                    # Dacă linia începe cu '>' sau '<', elimină acest caracter.
                    if line.startswith('>') or line.startswith('<'):
                        line = line[1:].strip()
                    if line:
                        words.append(line)  # Adaugă cuvântul curățat în listă.
                else:  # Altfel, procesează fișierul cuvinte_de_verificat.txt.
                    # Verifică dacă linia are formatul nou (cu punct și virgulă).
                    if ';' in line:
                        parts = line.split(';')
                        # Extrage a treia parte, care este cuvântul.
                        if len(parts) == 3:
                            word = parts[2].strip()
                            if word:
                                words.append(word)
                    else:
                        # Dacă nu are ';', este formatul vechi (un cuvânt pe linie).
                        words.append(line)
        return words
    except FileNotFoundError:
        # Afișează o eroare dacă fișierul nu este găsit.
        print(f"Eroare: Fișierul '{file_path}' nu a fost găsit.")
        return []


def is_valid_word(word):
    """
    Verifică dacă un cuvânt conține doar caractere din alfabetul român sau cratime.
    """
    # Folosește o expresie regulată pentru a valida caracterele.
    return bool(re.match(r'^[a-zăâîșț-]+$', word))


def get_letter_frequencies(words):
    """
    Calculează frecvența de apariție a fiecărei litere într-o listă de cuvinte.
    Aceasta este funcția de bază pentru strategia de ghicire.
    """
    # Expresie regulată pentru a extrage doar literele românești.
    letter_pattern = re.compile(r'[a-zăâîșț]')
    # Un dicționar care nu dă eroare dacă o cheie nu există, ci îi atribuie o valoare implicită (0).
    frequencies = collections.defaultdict(int)
    for word in words:
        # Numără fiecare literă o singură dată per cuvânt.
        for letter in set(letter_pattern.findall(word)):
            frequencies[letter] += 1
    return frequencies


def solve_hangman(secret_word, dictionary):
    """
    Rezolvă automat un puzzle Hangman pentru un cuvânt dat.

    Returns:
        (int, bool): O pereche conținând (numărul de litere încercate, dacă a fost ghicit cu succes).
    """
    word_len = len(secret_word)

    # Filtrare inițială: păstrează din dicționar doar cuvintele de aceeași lungime și valide.
    possible_words = [word for word in dictionary if len(word) == word_len and is_valid_word(word)]

    # Dacă nu găsim niciun cuvânt potrivit în dicționar, nu putem rezolva.
    if not possible_words:
        return 0, False

    guessed_letters = set()  # Un set pentru a stoca toate literele încercate.
    incorrect_letters = set()  # Un set pentru a stoca literele greșite.
    max_incorrect_guesses = 6  # Numărul standard de vieți la Hangman.

    # Creează cuvântul afișat, înlocuind literele cu '_'.
    display_word = ['_' if c != '-' else '-' for c in secret_word]

    # Bucla principală a jocului: continuă cât timp mai sunt litere de ghicit și mai sunt vieți.
    while '_' in display_word and len(incorrect_letters) < max_incorrect_guesses:
        # Dacă lista de cuvinte posibile devine goală, algoritmul se oprește.
        if not possible_words:
            break

        # Calculează frecvența literelor pentru cuvintele rămase.
        frequencies = get_letter_frequencies(possible_words)

        guess = ''
        # Sortează literele descrescător după frecvență pentru a alege cea mai probabilă literă.
        sorted_freq = sorted(frequencies.items(), key=lambda x: (-x[1], x[0]))

        # Găsește prima literă din topul frecvențelor care nu a mai fost încercată.
        for letter, freq in sorted_freq:
            if letter not in guessed_letters:
                guess = letter
                break

        # Dacă nu mai sunt litere de ghicit, oprește.
        if not guess:
            break

        guessed_letters.add(guess)

        # Verifică dacă litera ghicită este în cuvântul secret.
        if guess in secret_word:
            # Dacă da, actualizează cuvântul afișat.
            for i, letter in enumerate(secret_word):
                if letter == guess:
                    display_word[i] = guess
        else:
            # Dacă nu, adaugă la greșeli.
            incorrect_letters.add(guess)

        # Rafinează (filtrează) lista de cuvinte posibile pe baza ultimei încercări.
        temp_possible_words = []
        for word in possible_words:
            match = True
            # Regula 1: Un cuvânt posibil nu trebuie să conțină nicio literă ghicită greșit.
            if any(incorrect_letter in word for incorrect_letter in incorrect_letters):
                match = False

            # Regula 2: Un cuvânt posibil trebuie să se potrivească cu starea curentă a cuvântului afișat.
            if match:
                for i in range(word_len):
                    if display_word[i] != '_' and display_word[i] != word[i]:
                        match = False
                        break

            if match:
                temp_possible_words.append(word)

        possible_words = temp_possible_words

    # Verifică dacă jocul s-a terminat cu succes.
    was_successful = '_' not in display_word
    return len(guessed_letters), was_successful


def main():
    """
    Funcția principală care orchestrează întregul proces de rezolvare și raportare.
    """
    # Citește cuvintele de ghicit și dicționarul.
    words_to_guess = read_words('cuvinte_de_verificat.txt')
    dictionary = read_words('dex.txt', is_dex=True)

    # Verifică dacă fișierele au fost citite corect.
    if not words_to_guess or not dictionary:
        print("Nu s-a putut continua. Verificați mesajele de eroare anterioare.")
        return

    # Adaugă cuvintele de ghicit în dicționar pentru a garanta că pot fi găsite.
    for word in words_to_guess:
        if word not in dictionary:
            dictionary.append(word)

    # Pornește cronometrul și inițializează contoarele pentru statistici.
    start_time = time.time()
    total_guesses = 0
    successful_solves = 0
    num_words = len(words_to_guess)

    # Parcurge fiecare cuvânt și încearcă să-l rezolve.
    for word in words_to_guess:
        guesses, was_successful = solve_hangman(word, dictionary)
        total_guesses += guesses  # Adună numărul de litere încercate.
        if was_successful:
            successful_solves += 1  # Incrementează contorul de succese.

    # Oprește cronometrul și calculează statisticile finale.
    end_time = time.time()
    total_time = end_time - start_time
    average_time = total_time / num_words if num_words > 0 else 0

    # Afișează rezultatele finale.
    print(f"Timp total pentru a încerca rezolvarea a {num_words} de cuvinte: {total_time:.2f} secunde.")
    print(f"Media de timp per cuvânt: {average_time:.4f} secunde.")
    print(f"Numărul total de litere încercate: {total_guesses}.")
    print(f"Cuvinte ghicite cu succes: {successful_solves}/{num_words}.")


# Punctul de intrare în program: dacă scriptul este rulat direct, se execută funcția main.
if __name__ == "__main__":
    main()
