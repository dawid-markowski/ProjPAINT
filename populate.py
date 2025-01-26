from app import db, app
from app.models import User, Part
from config import Config

### KOD SLUZACY DO ZAPELNIENIA LOKALNEJ BAZY DANYCH PRZYKLADOWYMI DANYMI W CELU OBEJRZENIA I PRACY PRZY STRONIE ###

def populate_db():
    # Tworzenie użytkowników
    users_data = [
        {'username': 'admin1', 'email': 'admin@example.com', 'is_admin': True, 'password': 'admin'},
        {'username': 'user1', 'email': 'user1@example.com', 'password': 'password'},
        {'username': 'user2', 'email': 'user2@example.com', 'password': 'password'}
    ]

    for user_info in users_data:
        user = User.query.filter_by(username=user_info['username']).first()
        if user is None:  # Sprawdź, czy użytkownik istnieje
            user = User(username=user_info['username'], email=user_info['email'], is_admin=user_info.get('is_admin', False))
            user.set_password(user_info['password'])
            db.session.add(user)
            print(f"Dodano użytkownika: {user_info['username']}")
        else:
            print(f"Użytkownik {user_info['username']} już istnieje.")

    # Tworzenie części
    parts_data = [
        {'part_name': 'Tlumik sportowy', 'description': 'bardzo dobrze tlumi', 'group': 'tlumik', 'price': 299.99},
        {'part_name': 'Akumulator 620A 74aH', 'description': 'kopie pradem', 'group': 'akumulator', 'price': 699.99},
        {'part_name': 'Wycieraczka Axmo 600mm 400mm', 'description': 'wszystko zetrze', 'group': 'wycieraczka', 'price': 89.99},
        {'part_name': 'Lampa cofania', 'description': 'wszystko z nia widac', 'group': 'lampy', 'price': 119.99},
        {'part_name': 'Swiece zaplonowe x4', 'description': 'zawsze odpali', 'group': 'swiece', 'price': 149.99}
    ]

    for part_info in parts_data:
        part = Part.query.filter_by(part_name=part_info['part_name']).first()
        if part is None:  # Sprawdź, czy część istnieje
            part = Part(part_name=part_info['part_name'], description=part_info['description'], group=part_info['group'], price=part_info['price'])
            db.session.add(part)
            print(f"Dodano część: {part_info['part_name']}")
        else:
            print(f"Część {part_info['part_name']} już istnieje.")

    # Zatwierdzanie zmian w bazie danych
    db.session.commit()


if __name__ == "__main__":
    with app.app_context():
        print("Populating the database...")
        populate_db()
        print("Database populated successfully!")