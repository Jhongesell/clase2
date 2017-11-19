# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class profesor(models.Model):
    _rec_name="apellido"
    _name="ga.profesor"
    _description="Profesor"
    _order = "nombre ASC"
    nombre = fields.Char("Nombres",required=True)
    apellido = fields.Char("Apellidos",required=True)
    anioNacimiento = fields.Date("Año de Nacimiento")
    DNI = fields.Char("DNI")
    edad = fields.Integer("Edad (años)")
    sueldo = fields.Float("Sueldo")
    email = fields.Char("Email")

    cursoIds= fields.One2many("ga.curso","profesorId")

    @api.one
    @api.constrains("sueldo")
    def _check_sueldo(self):
        if self.sueldo>10000 or self.sueldo<0:
            raise ValidationError("El sueldo debe estar comprendido entre 0 y 10000")


    @api.one
    @api.constrains("email")
    def validate_email(self):
        regex = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
        if re.match(regex,self.email)==None:
            raise ValidationError("No tiene el formato de un correo")

class curso(models.Model):
    _name="ga.curso"
    _description="Curso"

    profesorId=fields.Many2one("ga.profesor")
    evaluacionId=fields.One2many("ga.evaluacion","cursoId")

    name=fields.Char(string="Nombre del curso")
    descripcion=fields.Html(string="Descripción del curso")
    tiempo=fields.Integer(string="Tiempo(Horas)")
    costo=fields.Monetary(string="Costo",currency_field="currency_id")
    currency_id=fields.Many2one("res.currency",string="Moneda1")

class alumno(models.Model):
    _rec_name = "nombre"
    _name = "ga.alumno"
    _description = "Alumno"
    _order = "nombre ASC"
    nombre = fields.Char("Nombres", required=True)
    apellido = fields.Char("Apellidos")
    anioNacimiento = fields.Date("Fecha de Nacimiento")
    dni = fields.Char("DNI")
    email = fields.Char("Correo")
    phone = fields.Char("Telefono fijo")
    mobile = fields.Char("Teléfono Móbil")
    direccion = fields.Char("Dirección")
    evaluacionIds = fields.One2many("ga.evaluacion", "alumnoId")

class evaluacion(models.Model):
    _name = "ga.evaluacion"
    _description = "Evaluacion"

    pc1 = fields.Integer("PC1")
    pc2 = fields.Integer("PC2")
    pc3 = fields.Integer("PC3")
    pc4 = fields.Integer("PC4")
    exf = fields.Integer("Ex. Final")
    exp = fields.Integer("Ex. Parcial")
    pp = fields.Integer("Promedio Ponderado", compute="_promedio_ponderado")
    estado = fields.Selection(
        [("registrado", "Registrado"), ("matriculado", "Matriculado"), ("retirado", "Retirado")])
    alumnoId = fields.Many2one("ga.alumno", string="Alumno")
    cursoId = fields.Many2one("ga.curso", string="Curso")



        # class gestor_academico2(models.Model):
#     _name = 'gestor_academico2.gestor_academico2'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         self.value2 = float(self.value) / 100