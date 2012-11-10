import webapp2
import jinja2
import os

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
	def get(self, accion=None):
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
			else:
				variables['tpl_include'] = 'templates/admin.html'
				variables['titulo'] = 'Inicio'
			
			tpl = tpl_jinja.get_template('templates/tpl_global.html')
			self.response.out.write(tpl.render(variables))
		else:
			self.redirect('/')

	def post(self, accion=None):
		if users.is_current_user_admin():
			inp_titulo = self.request.get('titulo')
			inp_descripcion = self.request.get('descripcion')
			ntarea = Tarea(titulo=inp_titulo,descripcion=inp_descripcion)
			ntarea.put()
			self.redirect('/tareas')
		else:
			self.redirect('/')

#regex python
#tareas/
#tareas/nuevo -> nueva_tarea.html
#tareas/todas -> todas_tareas.html
#tareas/pendientes -> ...
app = webapp2.WSGIApplication([
	('/', Principal),
	(r'/tareas', Tareas),
	(r'/tareas/(\w+)', Tareas)
], debug=True)