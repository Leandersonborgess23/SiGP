from app import db
from app.models.secretaria import Secretaria
from app.models.prefeitura import Prefeitura


class SecretariaController:

    @staticmethod
    def criar(form):
        try:
            sec = Secretaria()
            form.populate_obj(sec)
            prefeitura = Prefeitura.query.first()
            if not prefeitura:
                prefeitura = Prefeitura(
                    nome="Prefeitura Municipal de Pureza-RN",
                    cnpj="08.290.223/0001-42",
                    endereco="Praça 5 de Abril, 180",
                    telefone="(84) 99461-6390",
                    email="prefeitura@pureza.rn.gov.br"
                )
                db.session.add(prefeitura)
                db.session.commit()

            # Associa a secretaria à prefeitura
            sec.prefeitura_id = prefeitura.id

            db.session.add(sec)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            print("Erro criar secretaria:", e)
            return False

    @staticmethod
    def listar():
        return Secretaria.query.all()
