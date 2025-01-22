# PROJPAINT

Aplikacja internetowa sklepu z częściami samochodowymi.


## Instalacja

1. **Sklonuj repozytorium:**
   ```bash
   git clone https://github.com/dawid-markowski/ProjPAINT.git
   
2.**Utwórz i aktywuj środowisko wirtualne**
   
3. **Zainstaluj wymagane pakiety**
    ```bash
    pip install -r requirements.txt
    
4. **Skonfiguruj baze danych**
    ```bash
    flask db upgrade
    
5. **Uzupelnij baze danych przykladowymi danymi**
    ```bash
    python populate.py

6. **Uruchom aplikacje**
    ```bash
    python stronka.py
