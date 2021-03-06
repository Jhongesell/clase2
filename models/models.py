# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
import re

class cliente(models.Model):
    _inherit="res.partner"
    ruc = fields.Char("RUC")

    def _puntos_default(self):
        return "soltero"

    estadocivil= fields.Selection([("casado","1. Casado"),
                                   ("soltero", "2. Soltero"),
                                   ("viudo","3. Viudo")],
                                  required=True,
                                  default=_puntos_default,)


    puntos=fields.Integer(string="Puntos Bonus",
                          compute="calculodepuntos",
                          help="Puntos Bonus, se calcula en base a las compras realizadas por el cliente")


    @api.one
    def calculodepuntos(self):
        amount_total=self.puntos
        for invoice in self.invoice_ids:
            if invoice.state=="paid":
                amount_total=amount_total+invoice.amount_total
        self.puntos=amount_total*15


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
    evaluacionIds=fields.One2many("ga.evaluacion","cursoId")

    name=fields.Char(string="Nombre del curso")
    descripcion=fields.Html(string="Descripción del curso")
    tiempo=fields.Integer(string="Tiempo(Horas)")
    costo=fields.Monetary(string="Costo",currency_field="currency_id")
    currency_id=fields.Many2one("res.currency",string="Moneda1")

    promedioPc1=fields.Float("Promedio de PC1",store=True)
    promedioPc2 = fields.Float("Promedio de PC2", store=True,compute="promedio_pc2")


    @api.onchange("evaluacionIds")
    def promedio_pc1(self):
        pc1=0
        for pc in self.evaluacionIds:
            pc1=pc1+pc.pc1
        n=len(self.evaluacionIds)
        if len(self.evaluacionIds)==0:
            n=1
        pc1=pc1/n

        self.promedioPc1=pc1

    @api.depends("evaluacionIds.pc2")
    def promedio_pc2(self):
        pc2 = 0
        for pc in self.evaluacionIds:
            pc2 = pc2 + pc.pc2
        n = len(self.evaluacionIds)
        if len(self.evaluacionIds) == 0:
            n = 1
        pc2 = pc2 / n

        self.promedioPc2 = pc2

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
    state = fields.Selection(
        [("registrado", "Registrado"),
         ("matriculado", "Matriculado"),
         ("retirado", "Retirado")])
    evaluacionIds = fields.One2many("ga.evaluacion", "alumnoId")



    @api.model
    def todosalumnos(self):
        data=self.env["ga.alumno"].search([["state","=","matriculado"]])
        alumnos={}
        for alumno in data:
            nombre=alumno.nombre
            evaluaciones=self.env["ga.evaluacion"].search([ ["alumnoId","=",alumno.id] ])
            arrEval=[]
            for eval in evaluaciones:
                arrEval.append({"curso":eval.cursoId.name,"Prom. pond":eval.pp})
            evaluaciones=arrEval
            alumnos[alumno.id]={
                "nombre":nombre,
                "evaluaciones":evaluaciones
            }
        return {"alumnos": alumnos}

    @api.model
    def suma(self,paramx,paramy,param1=0,param2=10,param3=0):
        return {"resultado":param1+param2+param3}



class evaluacion(models.Model):
    _name = "ga.evaluacion"
    _description = "Evaluacion"
    _order = "pp"
    pc1 = fields.Integer("PC1")
    pc2 = fields.Integer("PC2")
    pc3 = fields.Integer("PC3")
    pc4 = fields.Integer("PC4")
    exf = fields.Integer("Ex. Final")
    exp = fields.Integer("Ex. Parcial")
    pp = fields.Integer("Promedio Ponderado",compute="calcular_promedio",store=True)

    alumnoId = fields.Many2one("ga.alumno", string="Alumno")

    cursoId = fields.Many2one("ga.curso", string="Curso")


    @api.one
    @api.depends("pc1","pc2","pc3","pc4","exp","exf")
    def calcular_promedio(self):
        record=self
        promedio = ((record.pc1+record.pc2+record.pc3+record.pc4)/4+ record.exp+record.exf)/3
        self.pp = promedio


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