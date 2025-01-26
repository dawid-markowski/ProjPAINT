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

## Instalacja 

###  Używając Dockera 

1.  **Sklonuj repozytorium:**

    ```bash
    git clone https://github.com/dawid-markowski/ProjPAINT.git

2.  **Pobierz obraz Dockerowy:**

    ```bash
    docker pull ghcr.io/dawid-markowski/samo:latest

3.  **Uruchom kontener:**

    ```bash
    docker run -d -p 5000:5000 --name samochodoza ghcr.io/dawid-markowski/projpaint/samo:latest

4. **Dostęp do aplikacji:**
    * Otwórz przeglądarkę i przejdź do adresu: `http://localhost:5000`
    
## Konta testowe

Do przetestowania funkcjonalności strony możesz użyć następujących kont:

*   **Użytkownik:**
    *   **Login:** test
    *   **Hasło:** test
*   **Administrator:**
    *   **Login:** admin
    *   **Hasło:** admin
