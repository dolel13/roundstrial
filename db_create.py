# db_create.py


from rounds import db, Item

db.create_all()

db.session.commit()