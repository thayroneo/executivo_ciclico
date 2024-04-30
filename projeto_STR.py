import os
from os.path import dirname, realpath, isfile
from json import dump, load


class JsonManager:

    def __init__(self):
        self.path = dirname(realpath(__file__)) + '/'

    
    def read_json(self, file):
        if isfile(self.path + file):
            with open(self.path + file) as f:
                data = load(f)
            return data
        else:
            return False

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a * b // gcd(a, b)

def calculo_MMC():
    data = jmanager.read_json('data/tarefas.json')
    range_tarefas = range(0, len(data))
    periodo = []

    for i in range_tarefas:
        periodo.append(int(data[i]['periodo']))

    # Calcular o MMC dos períodos
    result = periodo[0]
    for num in periodo[1:]:
        result = lcm(result, num)

    return result

def calculo_MDC():
    data = jmanager.read_json('data/tarefas.json')
    range_tarefas = range(0, len(data))
    periodo = []

    for i in range_tarefas:
        periodo.append(int(data[i]['periodo']))
    
    result = periodo[0]
    for num in periodo[1:]:
        result = gcd(result, num)
    
    return result



def taxa_ultiliza():
    data = jmanager.read_json('data/tarefas.json')
    range_tarefas = range(0, len(data))

    taxa_utilizacao = 0

    for i in range_tarefas:
        taxa_utilizacao += (data[i]['tempo_execut'])/(data[i]['periodo'])
    
    return taxa_utilizacao


def selection_sort(lista, lista_2, lista_3, lista_4, lista_5):
    n = len(lista)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if lista[j] < lista[min_idx]:
                min_idx = j
        lista[i], lista[min_idx] = lista[min_idx], lista[i]
        lista_2[i], lista_2[min_idx] = lista_2[min_idx], lista_2[i]
        lista_3[i], lista_3[min_idx] = lista_3[min_idx], lista_3[i]
        lista_4[i], lista_4[min_idx] = lista_4[min_idx], lista_4[i]
        lista_5[i], lista_5[min_idx] = lista_5[min_idx], lista_5[i]
    
    return [lista, lista_2, lista_3, lista_4, lista_5]

def heuristica(ciclo_maior, ciclo_menor):

    data = jmanager.read_json('data/tarefas.json')
    range_tarefas = range(0, len(data))

    prioridade = []
    tempo_execut = []

    periodo_ordenado = []
    periodo_modificado = []

    repeticoes = []
    for i in range_tarefas:
        prioridade.append(data[i]['tarefa'])
        tempo_execut.append(data[i]['tempo_execut'])
        periodo_ordenado.append(data[i]['periodo'])
        periodo_modificado.append(data[i]['periodo'])
        repeticoes.append(ciclo_maior/data[i]['periodo'])

    periodo_ordenado = selection_sort(periodo_ordenado, tempo_execut, periodo_modificado, prioridade, repeticoes)[0]
    tempo_execut = selection_sort(periodo_ordenado, tempo_execut, periodo_modificado, prioridade, repeticoes)[1]
    periodo_modificado = selection_sort(periodo_ordenado, tempo_execut, periodo_modificado, prioridade, repeticoes)[2]
    prioridade = selection_sort(periodo_ordenado, tempo_execut, periodo_modificado, prioridade, repeticoes)[3]
    repeticoes = selection_sort(periodo_ordenado, tempo_execut, periodo_modificado, prioridade, repeticoes)[4]
    

    ciclos = []
    qt_ciclos = ciclo_maior/ciclo_menor
    tempo = 0
    ciclo_atual = []
    for j in range(0, int(qt_ciclos)):
        for i in range_tarefas:
            if (tempo + tempo_execut[i]) <= ciclo_menor and len(ciclos) < qt_ciclos: 
                if periodo_modificado[i] >= periodo_ordenado[i]:
                    ciclo_atual.append(prioridade[i])
                    repeticoes[i] -= 1
                    tempo += tempo_execut[i]
                    periodo_modificado[i] = 0
            if periodo_modificado[i] < periodo_ordenado[i]:
                periodo_modificado[i] += ciclo_menor
            

        ciclos.append(ciclo_atual)  
 
        ciclo_atual = []
        tempo = 0

    aux = 0
    for i in repeticoes:
        if i != 0:
            aux += 1
    if aux != 0:
        return [False, False]

    return [prioridade, ciclos]


# MAIN

os.system('cls')
jmanager = JsonManager()

data = jmanager.read_json('data/tarefas.json')
json_size = len(data)
range_tarefas = range(0, len(data))
print(f'A quantidade de tarefas é: {json_size}')

taxa_utilizacao = taxa_ultiliza()
print(f'A taxa de utilização é {taxa_utilizacao*100}%',end = "\n\n")

if taxa_utilizacao > 1:
    print('Sistema impossível de ser escalonado')
    exit()

else:

    ciclo_maior = calculo_MMC()
    ciclo_menor = calculo_MDC()
 

    tempo_execut = []
    periodo = []

    f = []


    for i in range_tarefas:
        tempo_execut.append(data[i]['tempo_execut'])
        periodo.append(data[i]['periodo'])

    print('Testando possíveis valores de ciclo menor:', end='\n')

    x = 1

    while(x != 0):

        if x > ciclo_maior:
            break

        for i in range_tarefas:
            if x > tempo_execut[i]:
                if (2*x - gcd(periodo[i],x) <= periodo[i] ):
                    if (ciclo_maior % x) == 0:
                        f.append(x)
            x += 1
    
    print(f'{f} \n\n')

    ciclo_menor_correto = 1

    for i in range(len(f)):

        print(f'Testando:  {f[i]}', end='\n\n')
        aux = heuristica(ciclo_maior, f[i])[1]

        if aux != False:
            ciclo_menor_correto = f[i]
            break
        else:
            print(f'O valor {f[i]} é INVÁLIDO', end = '\n\n')
            ciclo_menor_correto = False

    if ciclo_menor_correto == False:
        print('Não ESCALONÁVEL')

        exit()

    ciclo_maior = calculo_MMC()
    print(f'O Ciclo Maior do Executivo Cíclico é: {ciclo_maior} unidades de tempo', end='\n')

    
    print(f'O Ciclo Menor do Executivo Cíclico é: {ciclo_menor_correto} unidades de tempo', end="\n\n")
    

    
    for i in range_tarefas:
        print(f'{data[i]['tarefa']} tem o período: {data[i]['periodo']}')
    
    print('',end = '\n\n')

    for i in range_tarefas:
        print(f'{data[i]['tarefa']} tem tempo de execução: {data[i]['tempo_execut']}')
    
    print('',end = '\n\n')
    
    
  
    print('Heurística escolhida: HRF',end ='\n\n')

    prio = heuristica(ciclo_maior, ciclo_menor_correto)[0]
    ciclo = heuristica(ciclo_maior, ciclo_menor_correto)[1]

    print('As prioridades são: ',f'\n {prio} \n')

    print('Os ciclos menores são: ', end='\n\n')

    try:
        for i in range(0,len(ciclo)):
            print(f'CICLO {i+1}: ', end = '\n')
            print(f'\n {ciclo[i]} \n' )
    except:
        print(ciclo)

