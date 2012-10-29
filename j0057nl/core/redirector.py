import webob
import webob.dec

import j0057nl.core.resource 

class Redirector(j0057nl.core.resource.Resource):
	def __init__(self, target):
		self.target = target
	def GET(self, request):
		raise webob.exc.HTTPFound(location=self.target)
