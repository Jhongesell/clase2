# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request

class home(http.Controller):

    @http.route("/alumnos",auth="user")
    def index(self):
        Alumnos=request.env["ga.alumno"].search([])
        """
        str="<ul>"
        for alumno in alumnos:
            str=str+"<li>"+alumno.nombre+" "+alumno.apellido+"</li>"
        str=str+"</ul>"
        """

        return request.render("gestor_academico2.listaAlumnos",{"alumnos":Alumnos})

    @http.route("/alumno/<model('ga.alumno'):alumno>",auth="user")
    def detalleAlumno(self,alumno):
        return request.render("gestor_academico2.detalleAlumno",{"alumno":alumno})


    @http.route("/api/alumnos",auth="user",type="json")
    def getAlumnos(self):
        data=request.env["ga.alumno"].search([])
        alumnos=[]
        for alumno in data:
            alumnos.append({"id":alumno.id,"nombre":alumno.nombre,"email":alumno.email})
        return {"data":alumnos}

    @http.route("/api2/alumnos", auth="user", type="json",methods=["POST"])
    def getAlumnos(self):
        data = request.env["ga.alumno"].search([])
        return {"data": data.read(["nombre","evaluacionIds"])}

# class GestorAcademico2(http.Controller):
#     @http.route('/gestor_academico2/gestor_academico2/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestor_academico2/gestor_academico2/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestor_academico2.listing', {
#             'root': '/gestor_academico2/gestor_academico2',
#             'objects': http.request.env['gestor_academico2.gestor_academico2'].search([]),
#         })

#     @http.route('/gestor_academico2/gestor_academico2/objects/<model("gestor_academico2.gestor_academico2"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestor_academico2.object', {
#             'object': obj
#         })