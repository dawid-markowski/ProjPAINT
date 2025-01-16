from app import db, app
from app.models import User, Part
from config import Config
### KOD SLUZACY DO ZAPELNIENIA LOKALNEJ BAZY DANYCH PRZYKLADOWYMI DANYMI W CELU OBEJRZENIA I PRACY PRZY STRONIE ###

def populate_db():
    # Tworzenie użytkowników
    users = [
        User(username='admin1', email='admin@example.com', is_admin=True),
        User(username='user1', email='user1@example.com'),
        User(username='user2', email='user2@example.com')
    ]

    # Ustawianie haseł
    users[0].set_password('admin')
    users[1].set_password('password')
    users[2].set_password('password')

    # Dodawanie użytkowników do sesji
    for user in users:
        db.session.add(user)

    # Tworzenie części
    parts = [
        Part(part_name='Tlumik sportowy', description='bardzo dobrze tlumi', group='tlumik', price=299.99),
        Part(part_name='Akumulator 620A 74aH', description='kopie pradem', group='akumulator', price=699.99),
        Part(part_name='Wycieraczka Axmo 600mm 400mm', description='wszystko zetrze', group='wycieraczka', price=89.99),
        Part(part_name='Lampa cofania', description='wszystko z nia widac', group='lampy', price=119.99),
        Part(part_name='Swiece zaplonowe x4', description='zawsze odpali', group='swiece', price=149.99)
    ]

    # Dodawanie części do sesji
    for part in parts:
        db.session.add(part)

    # Zatwierdzanie zmian w bazie danych
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        print("Populating the database...")
        populate_db()
        print("Database populated successfully!")
