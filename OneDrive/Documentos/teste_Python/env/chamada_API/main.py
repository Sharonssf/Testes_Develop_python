import requests
import json
import sqlite3
import pandas as pd
from chamada_API.database import Data_base

# Função para realizar consulta ao CNPJ via API
def consulta_cnpj(cnpj):
    url = f"https://publica.cnpj.ws/cnpj/{cnpj}"  
    response = requests.get(url)
    
    if response.status_code == 200:
        resp = json.loads(response.text)
        
        if 'razao_social' in resp:
            return resp 
        else:
            print("Chave 'razao_social' não encontrada na resposta.")
            return None
    else:
        print(f"Erro ao consultar o CNPJ. Status code: {response.status_code}")
        return None

# Função para conectar ao banco SQLite e pegar os CNPJs
def consultar_cnpjs_banco():
    conn = sqlite3.connect("system.db")
    cursor = conn.cursor()
    cursor.execute("SELECT CNPJ FROM Empresa")  
    cnpjs = cursor.fetchall()  
    conn.close()
    return cnpjs

# Função para atualizar o banco com as respostas da API
def salvar_no_banco(cnpj, razao_social):
    conn = sqlite3.connect('system.db')
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE Empresa SET Razao_Social = ? WHERE CNPJ = ?",
        (razao_social, cnpj)
    )
    
    conn.commit()
    conn.close()

# Exportação dos dados para uma planilha
def exportar_para_planilha(dados):
    df = pd.DataFrame(dados)

    arquivo_excel = 'empresas_registradas.xlsx'
    df.to_excel(arquivo_excel, index=False)

    print(f"Dados exportados para {arquivo_excel} com sucesso.")

# Realizando a integração
def integrar_com_api(cnpj):
    razao_social = consulta_cnpj(cnpj)  
    
    if razao_social:
        company_data = {
            'estabelecimento': {'cnpj': cnpj},
            'razao_social': razao_social['razao_social'],
            'capital_social': razao_social.get('capital_social', '0'),  
            'responsavel_federativo': razao_social.get('responsavel_federativo', 'Não especificado'),
            'atualizado_em': '2024-09-26',
            'porte': {'descricao': razao_social.get('porte', {}).get('descricao', 'Não especificado')},
            'natureza_juridica': {'descricao': razao_social.get('natureza_juridica', {}).get('descricao', 'Não especificado')},
            'qualificacao_do_responsavel': {'descricao': razao_social.get('qualificacao_do_responsavel', {}).get('descricao', 'Não especificado')}
        }
        
        socios_data = [] 

        # Registrando a empresa
        db = Data_base()
        db.connect()
        result = db.register_company(company_data, socios_data)
        db.close_connection()
        
        print(result)  
        return company_data  

# Main
if __name__ == "__main__":
    #Conexão com o banco
    db = Data_base()
    db.connect()
    db.create_table_company()
    db.close_connection()

    
    cnpj_usuario = input("Digite o CNPJ da empresa a ser buscada e incluída no banco: ")

    dados_empresa = integrar_com_api(cnpj_usuario)

    if dados_empresa:
        exportar_para_planilha([dados_empresa])  

    db.connect()
    companies = db.select_all_companies()
    print("Empresas registradas:", companies)
    db.close_connection()
