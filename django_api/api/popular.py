from .models import States

states = {
    "AC": 'Acre',
    "AL": 'Alagoas',
    "AP": 'Amapa',
    "AM": 'Amazonas',
    "BA": 'Bahia',
    "CE": 'Ceara',
    "DF": 'Distrito Federal',
    "ES": 'Espirito Santo',
    "GO": 'Goias',
    "MA": 'Maranhao',
    "MT": 'Mato Grosso',
    "MS": 'Mato Grosso do Sul',
    "MG": 'Minas Gerais',
    "PR": 'Parana',
    "PB": 'Paraiba', "PA": 'Para', "PE": 'Pernambuco', "PI": 'Piaui',
    "RJ": 'Rio de Janeiro', "RN": 'Rio Grande do Norte', "RS": 'Rio Grande do Sul',
    "RO": 'Rondonia', "RR": 'Roraima', "SC": 'Santa Catarina', "SE": 'Sergipe',
    "SP": 'Sao Paulo', "TO": 'Tocatins'
}


def create_comment():
    for key in states:
        States.objects.create(uf=key, state=states[key])


if __name__ == "__main__":
    create_comment()
