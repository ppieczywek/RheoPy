# RheoPy_1.0.py

## Opis
    RheoPy.py jest skryptem napisanym w języku Python, służącym do analizy danych
    pomiarowych z reometrów TA Instruments. Skrypt odczytuje dane pomiarowe
    zapisane w plikach tekstowych, a wyznaczone parmetery reologiczne zapisuje w
    arkuszu kalkulacyjnym MS Excel.

    Parametry wyznaczane przez skrypt:

    - lepkość przy stałej prędkości ścinania z bloku pomiarowego [peak hold -xx];
      wynikiem analizy jest średnia wartość lepkości, wyliczana z całego bloku
      danych, z pominięciem trzech pierwszych i trzech ostatnich punktów pomiarowych

    - parametry modeli płynięcia, wyznaczane z bloków pomiarowych [Flow sweep - xx],
      zawierających krzywe płynięcia (flow curve) - przebiegi naprężenia ścinającego
      w funkcji prędkości ścinania (shear stress vs. shear rate); analiza polega
      na dopasowaniu modeli płynięcia do punktów pomiarowych.

      Dopasowywane modele reologiczne:

        model Hershel-Buckley'a  - T = G_0 + K * gamma^n
        model Ostwald'a          - T = K * gamma^n

        gdzie:  T     - naprężenie styczne (ścinające)
                gamma - prędkość ścinanina
                G_0   - wstępne naprężenie ścinającego
                K,n   - współczynniki modeli płynięcia

    - pole powierzchni pod krzywymi płynięcia (z narastającą lub malejącą
      prędkością ścinania) z bloków [Flow sweep - xx];

    - granica plastyczności ("yield stress") - minimalne wymagane naprężenie
      ścinające, niezbędne do zainicjowania zjawiska przepływu; wyznaczane z
      bloków [Flow ramp - xx], z rampą naprężenia ścinającego;


[Dane wejściowe]
    Danymi wejściowymi programu są pliki tekstowe wyeksportowane z programu
    TRIOS, zawierające krzywe płynięcia. Eksportu danych do pliku tekstowego można
    dokonać z menu kontesktowego programu TRIOS, po wskazaniu pliku/plików danych
    (prawy przycisk myszy -> Export -> To Plain Text).

    UWAGA!!
    SEPERATOREM kolumn musi być znak tabulacji! Podczas eksportu danych do pliku
    tesktowe należy znanaczyć opcję "Column separator" -> Tab.

    UWAGA!!
    Plik danych musi zawierać kolumny "Stress", "Viscosity" oraz "Shear rate".
    Tylko te dane poddawane są analizie. W przypadku braku tych kolumn blok danych
    nie będzie analizowany.

    Prawidłowy plik z danymi powienien zawierać przynajmniej jeden blok pomiarowy
    np. "Flow sweep - xx". W przypadku analizy pliku, w którym takieglo bloku nie
    ma, program nie generuje żadnych wejściowych.


[Uruchamianie i analiza danych]
    Program uruchamiany jest poprzez dwukrotne kliknięcie lewym przyciskiem myszy
    na jego ikonę, lub wskazanie ikony i wciśnięcie przycisku "Enter" na klawiaturze
    komputera. Po uruchomieniu program wyświetla okno "konsoli" systemu operacyjnego,
    w którym wyświetlane są komunikaty o aktualny stanie analizy.

    Chwilę po wyświetleniu okna konsoli, pojawi się okno dialogowe wyboru plików
    do analizy. Okno pozwala na wybór wielu plików. Po dokonaniu i zatwierdzeniu
    wyboru, program uruchamia analizę danych, wyświetlając komunitakty kontrolne.

    Po przetworzeniu wszystkich plików wejściowych, pojawia się kolejne okno dialogowe,
    umożliwiające wskazanie lokalizacji oraz nazwy pliku wyników. Po wskazaniu pliku
    wyjściowego okno dialogowe zostaje zamknięte, a okno konsoli wyświetla
    komunikat o oczekiwaniu na wciśnięcie przycisku "Enter". Po jego wciśnięciu
    program automatycznie kończy swoje działanie i zamyka okno konsoli.


[Dane wyjściowe]
    Dane wyściowe zapisywane są w pliku Ms Excel o rozszerzeniu *.xlsx. Pierwsza,
    druga i trzecia kolumna danych we wszystkich arkuszach wynikowych zawiera
    kolejno: numer porządkowy pliku, nazwę pliku ("file") oraz nazwę bloku
    pomiarowego ("step").

    Arkusz "Viscosity" zawiera dane z pomiarów lepkości przy stałej prędkości
    ścinania. Nagłówki danych to "shear_rate" oraz "viscosity".

    Arkusz "Ostwald" zawiera parametry modelu płynięcia Ostwald'a (inaczej potęgowego),
    wyznaczane z bloków pomiarowych [Flow sweep - xx], zawierających krzywe płynięcia.
    Nagłówki danych to współczynniki modelu "K" i "n" oraz współczynnik dopasowania
    modelu "R2".

    Arkusz "Hershel-Buckley" zawiera parametry modelu płynięcia Hershel-Buckley'a,
    wyznaczane z bloków pomiarowych [Flow sweep - xx], zawierających krzywe płynięcia.
    Nagłówki danych to współczynniki modelu "G0", "K" i "n" oraz współczynnik
    dopasowania modelu "R2".

    Arkusz "Yield" zawiera dane z pomiarów granicy plastyczności ("yield stress"),
    wyznaczanej na podstawie danych z bloków [Flow ramp - xx]. Nagłówek danych
    nosi nazwę "yield_stress".

    Arkusz "Thixotropy" zawiera dane z pomiarów pola powierzchni pod krzywymi
    płynięcia. Nagłówek danych nosi nazwę "area".

    Powyższe arkusze występują opcjonalnie, w zależności czy dane pomiarowe
    zawierają odpowiednie bloki pomiarowe. Jeżeli danego bloku nie ma w danych,
    plik *.xlsx nie będzie zawierał odpowiadającego mu arkusza.


[Problemy]
    Aby uspwarniać funkcjonowanie programu, należy zawsze zgłaszać problemy z jego
    działaniem. Należy zgłszać problemy, występujące podczas analizy danych
    (np. zawieszanie się programu lub występowanie komunikatów o błędzie), a także
    wszelkie błędy, w arkuszach wyników. Zgłoszenie błędu musi być dokonane
    razem z danymi, na których wystąpił błąd. Tylko w takim przypadku możliwe jest
    szybkie zidentyfikowanie przyczyny błędu.


[Inne wymagania]
    Program wymaga zainstalowania na kompurze interpretera języka Python 3.7, a
    także następujących bibliotek: numpy, pandas, os, scipy, re, wxPython, openpyxl
