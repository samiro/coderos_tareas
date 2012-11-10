import webapp2
import jinja2
import os
import json

from google.appengine.api import users
from modelo import *

tpl_jinja = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__))
	)


class Principal(webapp2.RequestHandler):
	def get(self):
		if users.is_current_user_admin():
			self.redirect('/tareas')
		else:
			link_logueo = users.create_login_url()
			tpl = tpl_jinja.get_template('templates/bienvenido.html')
			variables = {
				'link_logueo':link_logueo
			}
			self.response.out.write(tpl.render(variables))

class Tareas(webapp2.RequestHandler):
	def get(self, accion=None, key_tarea=None):
		if users.is_current_user_admin():
			
			variables = {
				'usuario': users.get_current_user(),
				'link_cerrar':users.create_logout_url('/'),
				'tpl_include': '',
				'titulo': ''
			}

			if accion == "nuevo":
				variables['tpl_include'] = 'templates/nueva_tarea.html'
				variables['titulo'] = 'Nueva Tarea'
			elif accion == "todas":
				variables['tpl_include'] = 'templates/tareas_lista.html'
				variables['titulo'] = 'Todas las tareas'
				variables['tareas'] = Tarea.all()
			elif accion == "editar":
				variables['tpl_include'] = 'templates/editar_tarea.html'
				variables['titulo'] = 'Editar una tarea'
				variables['tarea'] = db.get(key_tarea)
			else:
				variables['tpl_include'] = 'templates/admin.html'
				variables['titulo'] = 'Inicio'
			
			tpl = tpl_jinja.get_template('templates/tpl_global.html')
			self.response.out.write(tpl.render(variables))
		else:
			self.redirect('/')

	def post(self, accion=None, key_tarea=None):
		if users.is_current_user_admin():
			if accion == "nueva":
				inp_titulo = self.request.get('titulo')
				inp_descripcion = self.request.get('descripcion')
				ntarea = Tarea(titulo=inp_titulo,descripcion=inp_descripcion)
				ntarea.put()
				
			elif accion == "editar":
				tarea = db.get(key_tarea)
				tarea.titulo = self.request.get('titulo')
				tarea.descripcion = self.request.get('descripcion')
				tarea.estado = self.request.get('estado')
				tarea.put()

			self.redirect('/tareas')
		else:
			self.redirect('/')

class Ajax(webapp2.RequestHandler):
	def get(self, accion=None, key_tarea=None):
		if users.is_current_user_admin():
			if accion == "delete" and key_tarea != None:
				tarea = db.get(key_tarea)
				tarea.delete()
				respuesta = {
					'eliminado': True
				}
				self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
				self.response.out.write(json.dumps(respuesta))
			else:
				respuesta = {
					'eliminado': False
				}
				self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
				self.response.out.write(json.dumps(respuesta))
		else:
			respuesta = {
				'eliminado': False
			}
			self.response.headers.add_header('content-type', 'application/json', charset='utf-8')
			self.response.out.write(json.dumps(respuesta))

#regex python
#tareas/
#tareas/nuevo -> nueva_tarea.html
#tareas/todas -> todas_tareas.html
#tareas/pendientes -> ...
app = webapp2.WSGIApplication([
	('/', Principal),
	(r'/tareas', Tareas),
	(r'/tareas/(\w+)', Tareas),
	(r'/tareas/(\w+)/(\w*\-*\w*)', Tareas),
	(r'/ajax/(delete)/(\w*\-*\w*)', Ajax)
], debug=True)