# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

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

    cursoIds= fields.One2many("ga.curso","profesorId")

    @api.one
    @api.constrains("sueldo")
    def _check_sueldo(self):
        if self.sueldo>10000 or self.sueldo<0:
            raise ValidationError("El sueldo debe estar comprendido entre 0 y 10000")


class curso(models.Model):
    _name="ga.curso"
    _description="Curso"

    profesorId=fields.Many2one("ga.profesor")

    name=fields.Char(string="Nombre del curso")
    descripcion=fields.Html(string="Descripción del curso")
    tiempo=fields.Integer(string="Tiempo(Horas)")
    costo=fields.Monetary(string="Costo",currency_field="currency_id")
    currency_id=fields.Many2one("res.currency",string="Moneda1")


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