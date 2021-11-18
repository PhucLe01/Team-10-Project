from app import myapp_obj, db
db.create_all()
myapp_obj.run(debug=True)
