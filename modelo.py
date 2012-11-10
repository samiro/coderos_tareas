from google.appengine.ext import db

class Tarea(db.Model):
	titulo = db.StringProperty(required=True)
	descripcion = db.StringProperty(required=True)
	creado = db.DateTimeProperty(auto_now_add=True)
	estado = db.CategoryProperty(default='pendiente', choices=['realizado', 'pendiente'])