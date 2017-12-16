#Basic Load
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#######################################################################
###NESTA FUNÇÃO FOI FEITA A FILTRAGEM DE UMA TURMA DE CALOUROS#########
def calouros(Eletrica):
    Calouros = Eletrica[Eletrica.nome_disciplina == "FISICA EXPERIMENTAL I"] 
    Calouros1 = Eletrica[Eletrica.nome_disciplina == "MATEMATICA PARA ENGENHARIA I"]
    Calouros2 = Eletrica[Eletrica.nome_disciplina == "ALGORITMOS E LOGICA DE PROGRAMACAO"]
    Calouros3 = Eletrica[Eletrica.nome_disciplina == "MECANICA CLASSICA"]
    
    Calouros4 = Calouros1[Calouros1['discente'].isin(Calouros['discente'])]
    Calouros5 = Calouros4[Calouros4['discente'].isin(Calouros2['discente'])]
    
    Turma1 = Calouros5[Calouros5['discente'].isin(Calouros3['discente'])]
    Turma1 = Turma1['discente']
    
    #Limpesa de várias variáveis temporárias
    del Calouros, Calouros1, Calouros2, Calouros3, Calouros4, Calouros5
    
    #Criação do CSV com a matrícula dos alunos de determinado semeste
    Turma1.to_csv("Data/Turma_Final/OMG.csv", header = 'discente')
    print("Arquivo criado!")
#######################################################################
#######################################################################

###############################################
#Nessa função, foi recolhido o dataset com o nome de todas as turmas e seus IDs.
#Seus valores foram alocados para um novo Dataset (17135x2) e salvo em csv.

def Nome_das_Disciplinas():
    Turmas_Temp = pd.read_csv("Data/Turmas/componentes-curriculares-presenciais.csv", error_bad_lines= False, delimiter = ";")
    Turmas_Temp = Turmas_Temp[Turmas_Temp.nivel == "G"] 
    Turmas_Fixo = Turmas_Temp[['id_componente', 'nome']].copy()
    Turmas_Fixo.to_csv("Turmas_Fixo.csv")
###############################################
    
    
#Importando a tabela que relaciona um ID a um nome de matéria
Turmas_Fixo = pd.read_csv("Data/Turmas_Fixo.csv", error_bad_lines= False, encoding = "ISO-8859-1")
Turmas_Fixo.drop('Unnamed: 0', axis= 1, inplace = True)
#Turmas_Fixo['nome'] = Turmas_Fixo['nome'].astype('str') 

Turmas_Fixo.dropna(inplace = True)
#Importando dados da planilha matrícula (Todos os alunos de todos os cursos)
Ingressantes = pd.read_csv("Data/Matriculas/matricula-componente-20171.csv", error_bad_lines= False, delimiter = ";")

#Removendo as linhas que contêm Null na média
Ingressantes = Ingressantes[~Ingressantes['media_final'].isnull()] 


#A planilha mostra unidades 1,2 e 3 (alguns casos 4), Para remover a repetição de unidade foi mantido apenas o 1
Ingressantes = Ingressantes[Ingressantes.unidade == 1] 


#Pegando todos os alunos de elétrica e jogando em uma nova tabela
Eletrica = Ingressantes[Ingressantes.id_curso == 2000030]

#Removendo colunas indesejadas
Ingressantes.drop([ 'faltas_unidade', 'id_curso', 'unidade', 'nota'], axis= 1, inplace = True)
Eletrica.drop([ 'faltas_unidade', 'id_curso', 'unidade', 'nota'], axis= 1, inplace = True)



######################################################
Turmas = pd.read_csv("Data/Turmas/turmas-2017.1.csv", error_bad_lines= False, delimiter = ";")

#Filtragem
Turmas = Turmas[Turmas.campus_turma == "Campus Central"] 

Turmas = Turmas[['id_turma', 'id_componente_curricular', 'ano', 'periodo']]
Turmas.dropna(inplace = True)

# Foi necessário criar um dicionário para iniciar os processos de mesclagens
Turmas_Fixo.set_index('id_componente', inplace = True)
Turmas.index = Turmas.index.map(int)

Dicionario_Turmas = Turmas_Fixo["nome"].to_dict()
# De posse do dicionário foi mapeado a coluna id_disciplina com seu nome
Turmas["nome_disciplina"] = Turmas["id_componente_curricular"].map(Dicionario_Turmas)
Turmas.dropna(inplace = True)
# Naturalmente o próximo passo seria a criação de um dicionário das turmas para aquele semestre
Turmas.set_index('id_turma', inplace = True)
Turmas.index = Turmas.index.map(int)
Dicionario_Turmas_Semestre = Turmas['nome_disciplina'].to_dict()
Dicionario_Ano_Semestre = Turmas["ano"].to_dict()
Dicionario_Periodo_Semestre = Turmas["periodo"].to_dict()


#################################################
#################################################
##MUITO CUIDADO!!!!!!!!! USEI POR CAUSA DE 2015.1
Eletrica.dropna(inplace = True, axis = 1)
#################################################
#################################################

#Adicionando o nome, ano e período das disciplinas a turma
Eletrica["nome_disciplina"] = Eletrica['id_turma'].map(Dicionario_Turmas_Semestre)
Eletrica["ano"] = Eletrica['id_turma'].map(Dicionario_Ano_Semestre)
Eletrica["periodo"] = Eletrica['id_turma'].map(Dicionario_Periodo_Semestre)



# Pega as infos e cria o dataset para o semestre
Turma1 = pd.read_csv("Data/Turma_Final/Matricula_turma_de_2011.1.csv")
Turma1.drop("Unnamed: 0", axis = 1, inplace = True) 
Semestre = pd.read_csv("Data/Turma_Final/Turma_de_2011.1.csv", error_bad_lines= False, encoding = "ISO-8859-1")
Semestre.drop("Unnamed: 0", axis = 1, inplace = True) 

Semestre.dropna(inplace = True)

Semestre_Temp = Eletrica[Eletrica['discente'].isin(Turma1['discente'])]
Semestre_Temp.drop('id_turma', axis = 1, inplace = True)
Semestre_Temp.dropna(inplace = True)

Semestre_Temp['ano'] = Semestre_Temp['ano'].astype('int64', copy=False)
Semestre_Temp['periodo'] = Semestre_Temp['periodo'].astype('int64', copy=False)

Semestre = Semestre.append(Semestre_Temp)

#Semestre.columns = ['ano','descricao','discente','media_final','nome_disciplina', 'numero_total_faltas','periodo','reposicao']

Semestre.to_csv("Data/Turma_Final/Turma_de_2011.1.csv", header = ['ano',
'descricao',
'discente',
'media_final',
'nome_disciplina', 
'numero_total_faltas',
'periodo',
'reposicao'])
################ Á R E A   D E    T E S T E S #########################


#Semestre.to_csv("Data/Turma_Final/Turma_de_2010.1.csv", header = ['ano','descricao','discente','media_final','nome_disciplina', 'numero_total_faltas','periodo','reposicao'])


#######################################################################


