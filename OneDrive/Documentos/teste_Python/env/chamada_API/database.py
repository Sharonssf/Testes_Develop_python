import sqlite3

# Criação e manipulação dos dados no Banco (sqlite)
class Data_base:
    def __init__(self, name="system.db") -> None:
        self.name = name

    def connect(self):
        self.connection = sqlite3.connect(self.name)

    def close_connection(self):
        try:
            self.connection.close()
        except:
            pass

    # Criação da tabela 'Empresa' para armazenar as informações do CNPJ e Razão Social
    def create_table_company(self):
        cursor = self.connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Empresa (
                CNPJ TEXT PRIMARY KEY,
                Inscricao_Estadual TEXT,  -- Novo campo
                Razao_Social TEXT,
                Nome_Fantasia TEXT,  -- Novo campo
                CEP TEXT,  -- Novo campo
                UF TEXT,  -- Novo campo
                Capital_Social TEXT,
                Responsavel_Federativo TEXT,
                Atualizado_Em TEXT,
                Porte_Descricao TEXT,
                Natureza_Juridica_Descricao TEXT,
                Qualificacao_Responsavel TEXT
            )
        ''')
        
        # Criação da tabela 'Socios' para armazenar informações dos sócios
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Socios (
                CNPJ_Empresa TEXT,
                CPF_CNPJ_Socio TEXT,
                Nome TEXT,
                Tipo TEXT,
                Data_Entrada TEXT,
                Faixa_Etaria TEXT,
                Pais_ID TEXT,
                Qualificacao_Descricao TEXT,
                PRIMARY KEY (CPF_CNPJ_Socio, CNPJ_Empresa),
                FOREIGN KEY (CNPJ_Empresa) REFERENCES Empresa(CNPJ)
            )
        ''')

    # Registro das informações da empresa
    def register_company(self, company_data, socios_data):
        cursor = self.connection.cursor()

        # Dados da empresa
        empresa_dados = (
            company_data['estabelecimento']['cnpj'],
            company_data.get('inscricao_estadual', ''),  
            company_data['razao_social'],
            company_data.get('nome_fantasia', ''),  
            company_data.get('cep', ''), 
            company_data.get('uf', ''),  
            company_data.get('capital_social', ''),  
            company_data.get('responsavel_federativo', ''),
            company_data.get('atualizado_em', ''),
            company_data['porte']['descricao'],
            company_data['natureza_juridica']['descricao'],
            company_data['qualificacao_do_responsavel']['descricao']
        )

        try:
            cursor.execute('''
                INSERT INTO Empresa (CNPJ, Inscricao_Estadual, Razao_Social, Nome_Fantasia, CEP, UF, Capital_Social, Responsavel_Federativo, Atualizado_Em, Porte_Descricao, Natureza_Juridica_Descricao, Qualificacao_Responsavel)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', empresa_dados)
        except sqlite3.IntegrityError:
            return "Empresa já registrada."

        # Dados dos sócios
        for socio in socios_data:
            socio_dados = (
                company_data['estabelecimento']['cnpj'],
                socio['cpf_cnpj_socio'],
                socio['nome'],
                socio['tipo'],
                socio['data_entrada'],
                socio['faixa_etaria'],
                socio['pais_id'],
                socio['qualificacao_socio']['descricao']
            )

            # Inserção dos sócios no banco de dados
            try:
                cursor.execute('''
                    INSERT INTO Socios (CNPJ_Empresa, CPF_CNPJ_Socio, Nome, Tipo, Data_Entrada, Faixa_Etaria, Pais_ID, Qualificacao_Descricao)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', socio_dados)
            except sqlite3.IntegrityError:
                return f"Sócio {socio['nome']} já registrado."

        self.connection.commit()
        return "Registro de empresa e sócios realizado com sucesso."

    
    def select_all_companies(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Empresa ORDER BY Razao_Social")
        empresas = cursor.fetchall()
        
        # Função para imprimir os dados da empresa e ver se está tudo certo
        for empresa in empresas:
            print(empresa)
         
        return empresas

    # Selecionar todos os sócios de uma empresa
    def select_company_socios(self, cnpj_empresa):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM Socios WHERE CNPJ_Empresa = ?", (cnpj_empresa,))
        socios = cursor.fetchall()
        return socios

    # Deletar uma empresa
    def delete_companie(self, cnpj):
        try:
            cursor = self.connection.cursor()
            cursor.execute("DELETE FROM Empresa WHERE CNPJ = ?", (cnpj,))
            self.connection.commit()
            return "Cadastro de empresa excluído com sucesso!"
        except sqlite3.Error as e:
            return f"Erro ao excluir a empresa: {e}"


    # Atualização dos dados
    def update_company(self, fullDataSet):
        cursor = self.connection.cursor()
        cursor.execute('''
            UPDATE Empresa SET
                Razao_Social = ?,
                Capital_Social = ?,
                Responsavel_Federativo = ?,
                Atualizado_Em = ?,
                Porte_Descricao = ?,
                Natureza_Juridica_Descricao = ?,
                Qualificacao_Responsavel = ?
            WHERE CNPJ = ?
        ''', (
            fullDataSet[1],  # Razao_Social
            fullDataSet[2],  # Capital_Social
            fullDataSet[3],  # Responsavel_Federativo
            fullDataSet[4],  # Atualizado_Em
            fullDataSet[5],  # Porte_Descricao
            fullDataSet[6],  # Natureza_Juridica_Descricao
            fullDataSet[7],  # Qualificacao_Responsavel
            fullDataSet[0]   # CNPJ
        ))
        self.connection.commit()
        return "Empresa atualizada com sucesso."

if __name__ == "__main__":
    db = Data_base()
    db.connect()
    db.create_table_company()
    db.close_connection()
    print("Banco de dados criado e tabelas configuradas com sucesso.")
