import machine
import time

# Funkcja read_impulses przyjmuje argument input_pin (GPIO ustawiony jako wejście)
def read_impulses(input_pin):
    print("Program czyta ramkę danych DCF77")
    bits = []  # Inicjalizacja listy bits do przechowywania odczytanych bitów
    sync_detected = False  # Zmienna do śledzenia stanu synchronizacji, w momencie synchronizacji zmienia stan na True

    # Funkcja do pomiaru długości impulsu
    # do start_time zapisywany jest czas początkowy stanu wysokiego
    # do end_time zapisywany jest czas końcowy stanu wysokiego
    def read_pulse():
        start_time = time.ticks_ms()
        while input_pin.value() == 1:
            pass
        end_time = time.ticks_ms()
        return time.ticks_diff(end_time, start_time)  # Funkca time.ticks_diff od czasu końcowego odejmuje czas początkowy i zwraca wartośc w ms

    while True:
        # try except wyświetli komunikat o błędzie
        try:
            # Sprawdzenie stanu pinu GPIO
            # w momencie pojawieniu się stanu wysokiego na GPIO wywoływana jest funkca do pomiru długości impulsu
            # jeżeli impuks mieści się w granicach 80-120ms interpretowany jest jako 0 logiczne
            # jeżeli impuls mieści się w granicach 170-230ms interpretowany jest jako 1 logiczne
            # impuls w przedziale 970-1030ms interpretowany jest jako impuls końca ramki i synchronizacji
            
            # Jeżeli został wykryty impuls synchronizacji a wcześniej był ustawiony jako False to sync_detect ustawiany jest na True i wyświetlany jest komunikat
            # o synchronizacji ramki danych w kolejnym obiegu pętli jeżeli poprzednio sync_detect ustawiony był jako true to teraz przestawiany jest na Fase
            # i funkcja input_pin.value zwraca ramke danych w liście bits
            if input_pin.value() == 1:
                duration = read_pulse()

                if 80 <= duration <= 120:  # Odczyt impulsu 100ms
                    if sync_detected:
                        bits.append(0)
                        machine.idle()  # Metoda przenosi procesor w stan niskiego zużycia energii
                elif 170 <= duration <= 230:  # Odczyt impulsu 200ms
                    if sync_detected:
                        bits.append(1)
                        machine.idle()  # Metoda przenosi procesor w stan niskiego zużycia energii
                elif 970 <= duration <= 1030:  # Odczyt synchronizacji ramki
                    if sync_detected:
                        sync_detected = False
                        return bits
                    else:
                        sync_detected = True
                    print("Synchronizacja OK... Impuls 970-1030ms")

            machine.idle()  # Metoda przenosi procesor w stan niskiego zużycia energii 
        except Exception as e:
            print(f"Błąd: {e}")
            break
