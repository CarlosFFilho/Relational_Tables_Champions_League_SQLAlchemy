# 1. IMPORTANDO BIBLIOTECAS

import pandas as pd
import sqlalchemy.orm as sqlAR
import sqlalchemy as sqlA


# 2. CRIANDO TABELAS RELACIONAIS

Base = sqlAR.declarative_base() #Criando a base de dados

engine = sqlA.create_engine('sqlite:///banco.bd') #Criando comunicação entre o SQLAlchemy e o banco de dados


class Jogadores(Base): #Tabela Players contendo id, nome, clube e posição dos jogadores
    __tablename__ = 'Players'
    id = sqlA.Column(sqlA.Integer, primary_key=True, nullable=False) 
    name = sqlA.Column(sqlA.String)
    club = sqlA.Column(sqlA.String)
    position = sqlA.Column(sqlA.String)

    _finalizacao = sqlAR.relationship('Gols_finalizacao', back_populates = '_jogador_finalizacao') #Relacionando a tabela Players com a tabela Gols_finalizacao
    _localizacao = sqlAR.relationship("Gols_localizacao", back_populates = '_jogador_localizacao') #Relacionando a tabela Players com a tabela Gols_localizacao

    def __repr__(self): #Representação da tabela Players
        return f"Jogadores(id={self.id}, name = {self.name}, , club = {self.club} , position = {self.position})"


class Gols_finalizacao(Base): #Tabela Gols_finalizacao contendo id, nome, gols de pé direito, gols de pé esquerdo, gols de cabeça e outros
    __tablename__ = 'Gols_finalizacao'
    id = sqlA.Column(sqlA.Integer, primary_key=True, nullable=False) 
    user_name = sqlA.Column(sqlA.String, sqlA.ForeignKey(Jogadores.name))
    pe_direito = sqlA.Column(sqlA.Integer) 
    pe_esquerdo = sqlA.Column(sqlA.Integer)
    cabeca = sqlA.Column(sqlA.Integer)
    outros = sqlA.Column(sqlA.Integer)
    
    _jogador_finalizacao = sqlAR.relationship('Jogadores', back_populates = '_finalizacao') #Relacionando a tabela Gols_finalizacao com a tabela Players

    def __repr__(self): #Representação da tabela Gols_finalizacao
        return f"Gols_finalizacao(id={self.id} , pe_direito = {self.pe_direito} , pe_esquerdo = {self.pe_esquerdo} , cabeca = {self.cabeca} , outros = {self.outros})"


class Gols_localizacao(Base): #Tabela Gols_localizacao contendo id, nome, gols de dentro da área, gols de fora da área e gols de pênalti
    __tablename__ = 'Gols_localizacao'
    id = sqlA.Column(sqlA.Integer, primary_key=True, nullable=False) 
    user_name = sqlA.Column(sqlA.String, sqlA.ForeignKey(Jogadores.name))
    dentro_area = sqlA.Column(sqlA.Integer) 
    fora_area = sqlA.Column(sqlA.Integer)
    penalti = sqlA.Column(sqlA.Integer)
    
    _jogador_localizacao = sqlAR.relationship('Jogadores', back_populates = '_localizacao') #Relacionando a tabela Gols_localizacao com a tabela Players

    def __repr__(self): #Representação da tabela Gols_localizacao
        return f"Gols_localizacao(id={self.id} , dentro_area = {self.dentro_area} , fora_area = {self.fora_area} , penalti = {self.penalti})"

Base.metadata.create_all(engine) #Usando a base declarativa criada anteriormente para inserir as tabelas criadas no banco de dados


# 3. IMPORTANDO *DATASET* EM CSV

x = pd.read_csv(r"/content/goals.csv" , sep=',')
dados = pd.DataFrame(x) #Criando um quadro de dados


# 4. PREENCHENDO TABELA PRINCIPAL (Players)

session=sqlAR.sessionmaker()(bind=engine) #Relaciona o os objetos implementados no python com o engine

for i in range (10): #Explorando as 10 primeiras linhas do Dataset
        player_champs = Jogadores(name=dados["player_name"][i] , club=dados["club"][i], position=dados["position"][i])
        session.add(player_champs) #Adicionando objeto à tabela Players

session.commit() #Persistindo com as alterações realizadas no banco de dados


# 5. PREENCHENDO TABELA 2 (Gols_finalizacao)

for linha in range(10): #Explorando as 10 primeiras linhas do Dataset

  gol_tipo=Gols_finalizacao(
    user_name=dados["player_name"][linha],
    pe_direito='{0}'.format(dados["right_foot"][linha]),
    pe_esquerdo='{0}'.format(dados["left_foot"][linha]),
    cabeca='{0}'.format(dados["headers"][linha]),
    outros='{0}'.format(dados["others"][linha]))

  session.add(gol_tipo) #Adicionando objeto à tabela Gols_finalizacao
  session.commit() #Persistindo com as alterações realizadas no banco de dados


# 6. PREENCHENDO TABELA 3 (Gols_localizacao)

for linha in range(10): #Explorando as 10 primeiras linhas do Dataset

  gol_lugar=Gols_localizacao(
    user_name=dados["player_name"][linha],
    dentro_area='{0}'.format(dados["inside_area"][linha]),
    fora_area='{0}'.format(dados["outside_areas"][linha]),
    penalti='{0}'.format(dados["penalties"][linha]))

  session.add(gol_lugar) #Adicionando objeto à tabela Gols_localizacao
  session.commit() #Persistindo com as alterações realizadas no banco de dados


# 7. VISUALIZANDO TABELA PRINCIPAL

visualizar = session.query(Jogadores).all() #Filtrando tabela "Players" no banco de dados

quadro1 = []

for elemento in visualizar:
  obj = [elemento.id, elemento.name, elemento.club, elemento.position]
  quadro1.append(obj)
    
QUADRO1 = pd.DataFrame(quadro1, columns=['ID', 'Jogador', 'Clube', 'Posição'])
QUADRO1.set_index('ID', inplace = True)

print(QUADRO1)


# 8. VISUALIZANDO TABELA 2 (Gols_finalizacao)

visualizar = session.query(Gols_finalizacao).all() #Filtrando tabela "Gols_finalizacao" no banco de dados

quadro2 = []

for elemento in visualizar:
  obj = [elemento.id, elemento.user_name, elemento.pe_direito, elemento.pe_esquerdo, elemento.cabeca, elemento.outros]
  quadro2.append(obj)

QUADRO2 = pd.DataFrame(quadro2, columns=['ID', 'Jogador', 'Gols de PÉ DIREITO', 'Gols de PÉ ESQUERDO', 'Gols de CABEÇA', 'Outros'])
QUADRO2.set_index('ID', inplace = True)

print(QUADRO2)


# 9. VIZUALIZANDO TABELA 3 (Gols_localizacao)

visualizar = session.query(Gols_localizacao).all() #Filtrando tabela "Gols_localizacao" no banco de dados

quadro3 = []

for elemento in visualizar:
  obj = [elemento.id, elemento.user_name, elemento.fora_area , elemento.dentro_area , elemento.penalti]
  quadro3.append(obj)
    
QUADRO3 = pd.DataFrame(quadro3, columns=['ID', 'Jogador', 'Gols de FORA DA ÁREA', 'Gols de DENTRO DA ÁREA', 'Gols de PÊNALTI'])
QUADRO3.set_index('ID', inplace = True)

print(QUADRO3)
