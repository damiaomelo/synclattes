# -*- encoding: utf-8 -*-
from __future__ import absolute_import
from sqlalchemy import or_, and_
from sqlalchemy.orm.exc import NoResultFound
import db, util

class PessoaInstituicao(object):
    def __init__(self, entidade):
        self.entidade = entidade
    @staticmethod
    def fromIdentificador(cpfOrNumeroUFSCar):
        try:
            return PessoaInstituicao(db.session.query(db.Pessoa).filter(or_(
                       db.Pessoa.cpf == cpfOrNumeroUFSCar,
                       db.Pessoa.id  == cpfOrNumeroUFSCar
                   )).one())
        except NoResultFound:
            return None
    def getEntidade(self):
        """ Entidade a ser inserida na chave estrangeira de PessoaLattes """
        return self.entidade
    def getCpf(self):
        return self.entidade.cpf
    def getNome(self):
        return self.entidade.nome
    def getNascimento(self):
        return self.entidade.data_nascimento.strftime('%d/%m/%Y')
    def getPessoaLattes(self):
        return self.entidade.pessoa_lattes
    def getRoles(self):
        """ Retorna lista de vínculos ativos da pessoa com a universidade """
        return map(util.firstOrNone,
                   db.session.query(db.TipoVinculo.nome)\
                             .join(db.Vinculo)\
                             .filter(db.Vinculo.pessoa_id == self.entidade.id)\
                             .filter(db.Vinculo.fim_vinculo.is_(None))\
                             .all())
