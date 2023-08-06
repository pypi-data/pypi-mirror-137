from setuptools import setup

descricao_longa = """
    # EcotrustAPI - Python3
Biblioteca que interage com a api do Ecotrust e normaliza alguns retornos da plataforma.


# Ações possíveis pela lib

 - Criar scan parametrizado e executá-lo
 - Cadastrar ativo
 - Obter detalhes do ativo
 - Obter relatório
 - Executar scans 
 - Executar scan de forma rápida

## Exemplo execução de scan rápido
```py
def main():
    token = \'<token>\'

    api = EcotrustAPI(token, \"https://instancia.ecotrust.io/\")

    \"\"\"
       Se pular_execucao_com_erro=True, não será feito raise da exceção APIError se não for possível executar o scan 
       usando um sensor específico, e portanto será retornado os ID's dos scans que foram executados com sucesso,
       então há possibilidade de ser retornado um dict vazio \"{}\" caso todos falhem. 
       
       Retorna um dicionário com: 
         {'NET-SCAN': 96, 'DNS-SCAN': 97, 'MALWARE': 98, 'WEBAPP-OWASP': 99}
         
        Na forma: 
          {
             'SENSOR NOME': ID DO SCAN INICIADO
          }
          
        O único valor volátil é o ID do scan, o nome do sensor é IMUTÁVEL.
    \"\"\"
    scans_ids = api.fast_scan("pudim.com.br", pular_execucao_com_erro=False)

    # scans_ids[SENSOR] = ID DO SCAN INICIADO MAPEADO PELO SENSOR

    # Com o id do scan é possível verificar se foi finalizado ou se aconteceu algum erro
    req_st = requests.get(f'https://instancia.ecotrust.io/scans/api/v1/by-id/{scans_ids["NET-SCAN"]}', headers={
        'Authorization': 'Token {}'.format(token)
    })

    # Se o status estiver FINISHED, o scan finalizou com êxito e o relatório do mesmo já está disponível
    if req_st.json()['status'] == 'finished':

        # Obtém relatório CSV especificando ID do Scan que finalizou
        requests.get(f'https://instancia.ecotrust.io/scans/api/v1/report/csv/{scans_ids["NET-SCAN"]}', headers={
            'Authorization': 'Token {}'.format(token)
        })

        # Obtém relatório HTML espcificando ID do Scan que finalizou
        requests.get(f'https://instancia.ecotrust.io/scans/api/v1/report/html/{scans_ids["NET-SCAN"]}', headers={
            'Authorization': 'Token {}'.format(token)
        })

        # Obtém relatório JSON espcificando ID do Scan que finalizou
        requests.get(f'https://instancia.ecotrust.io/scans/api/v1/report/json/{scans_ids["NET-SCAN"]}', headers={
            'Authorization': 'Token {}'.format(token)
        })


if __name__ == "__main__":
    main()
```
"""

setup(
    name="EcotrustAPI",
    version="1.3.0",
    install_requires=[
        'requests', 'urllib3', 'rand-string'
    ],
    description="Biblioteca para interação com API do EcotrustET",
    long_description=descricao_longa,
    long_description_content_type='text/markdown',
    author="EcoIT - Dev Team",
    author_email="pablo.viana@ecoit.com.br",
    py_modules=['ecotrust_api'],
    python_requires='>=3.9',
)