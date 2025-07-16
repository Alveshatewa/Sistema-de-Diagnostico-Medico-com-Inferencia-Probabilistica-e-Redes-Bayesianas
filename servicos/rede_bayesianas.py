from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

def criar_rede_bayesiana():
    # Criar o grafo da rede
    model = DiscreteBayesianNetwork([
        ('Febre', 'Tifoide'),
        ('Diarreia', 'Tifoide'),
        ('Fadiga', 'Tifoide'),
        ('Vomito', 'Gastroenterite'),
        ('DorUrinaria', 'Gastroenterite'),
        ('Febre', 'Malaria'),
        ('Fadiga', 'Malaria'),
        ('DorUrinaria', 'InfeccaoUrinaria'),
        ('Febre', 'InfeccaoUrinaria'),
    ])

    # CPDs para sintomas
    cpd_febre = TabularCPD('Febre', 2, [[0.7], [0.3]], state_names={'Febre': [0, 1]})
    cpd_diarreia = TabularCPD('Diarreia', 2, [[0.6], [0.4]], state_names={'Diarreia': [0, 1]})
    cpd_fadiga = TabularCPD('Fadiga', 2, [[0.5], [0.5]], state_names={'Fadiga': [0, 1]})
    cpd_vomito = TabularCPD('Vomito', 2, [[0.8], [0.2]], state_names={'Vomito': [0, 1]})
    cpd_dor_urinaria = TabularCPD('DorUrinaria', 2, [[0.9], [0.1]], state_names={'DorUrinaria': [0, 1]})

    # CPD para Tifoide
    cpd_tifoide = TabularCPD(
        variable='Tifoide',
        variable_card=2,
        values=[
            [0.95, 0.9, 0.85, 0.8, 0.9, 0.85, 0.8, 0.7],
            [0.05, 0.1, 0.15, 0.2, 0.1, 0.15, 0.2, 0.3]
        ],
        evidence=['Febre', 'Diarreia', 'Fadiga'],
        evidence_card=[2, 2, 2],
        state_names={'Tifoide': [0, 1], 'Febre': [0, 1], 'Diarreia': [0, 1], 'Fadiga': [0, 1]}
    )

    # CPD para Gastroenterite
    cpd_gastroenterite = TabularCPD(
        variable='Gastroenterite',
        variable_card=2,
        values=[
            [0.95, 0.9, 0.85, 0.8],
            [0.05, 0.1, 0.15, 0.2]
        ],
        evidence=['Vomito', 'DorUrinaria'],
        evidence_card=[2, 2],
        state_names={'Gastroenterite': [0, 1], 'Vomito': [0, 1], 'DorUrinaria': [0, 1]}
    )

    # CPD para Malaria
    cpd_malaria = TabularCPD(
        variable='Malaria',
        variable_card=2,
        values=[
            [0.9, 0.7, 0.6, 0.4],
            [0.1, 0.3, 0.4, 0.6]
        ],
        evidence=['Febre', 'Fadiga'],
        evidence_card=[2, 2],
        state_names={'Malaria': [0, 1], 'Febre': [0, 1], 'Fadiga': [0, 1]}
    )

    # CPD para Infecção Urinária
    cpd_infeccao = TabularCPD(
        variable='InfeccaoUrinaria',
        variable_card=2,
        values=[
            [0.9, 0.6, 0.7, 0.4],
            [0.1, 0.4, 0.3, 0.6]
        ],
        evidence=['DorUrinaria', 'Febre'],
        evidence_card=[2, 2],
        state_names={'InfeccaoUrinaria': [0, 1], 'DorUrinaria': [0, 1], 'Febre': [0, 1]}
    )

    # Associar os CPDs ao modelo
    model.add_cpds(
        cpd_febre,
        cpd_diarreia,
        cpd_fadiga,
        cpd_vomito,
        cpd_dor_urinaria,
        cpd_tifoide,
        cpd_gastroenterite,
        cpd_malaria,
        cpd_infeccao
    )

    # Verificar a consistência da rede
    try:
        model.check_model()
        print("Modelo bayesiano válido!")
    except Exception as e:
        print(f"Erro na validação do modelo: {str(e)}")
        raise

    return model
