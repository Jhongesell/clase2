# -*- coding: utf-8 -*-

from odoo import models, fields, api


class profesor(models.Model):
    _rec_name="apellido"
    _name="ga.profesor"
    _description="Profesor"
    nombre = fields.Char("Nombres",required=True)
    apellido = fields.Char("Apellidos",required=True)
    anioNacimiento = fields.Date("Año de Nacimiento")
    DNI = fields.Char("DNI")
    edad = fields.Integer("Edad (años)")
    sueldo = fields.Float("Sueldo")




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