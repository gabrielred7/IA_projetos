# -*- coding: utf-8 -*-
"""Tarefa de IA - Hill-SA-AG.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1iA7WrJmh525Tz9wCVu5LisNQWVspA657

### **Tarefa - Hill-SA-AG**  
#### Tema: Resolver o problema das N-rainhas
Nome: Gabriel Almeida Mendes  
DRE: 117204959

### **1. Modelagem**

A representação do tabuleiro N×N com N-rainhas pode ser feita de diversas maneiras, mas uma abordagem comum é usar uma N-tupla do conjunto [1, N]^N, onde cada elemento da tupla representa a posição de uma rainha em uma coluna específica.

Como queremos resolver o problema das N-Rainhas, será ignorado os casos onde há mais de uma rainha na mesma linha, logo, cada linha terá uma única rainha.  

Portanto, direi que a i-ésima componente da N-tupla representa a i-ésima linha do tabuleiro, e o número j da i-ésima componente da N-tupla representa a j-ésima coluna da rainha referente à i-ésima linha.

Exemplos:   
a) A 4-tupla [2, 0, 3, 1] representaria um tabuleiro de 4×4 da seguinte forma:

		- Q - -
		- - - Q
		Q - - -
		- - Q -

b) A 8-tupla [6, 4, 7, 1, 8, 2, 5, 3] representaria um tabuleiro 8x8 da seguinte forma:

		+ + + + + Q + +
		+ + + Q + + + +
		+ + + + + + Q +
		Q + + + + + + +
		+ + + + + + + Q
		+ Q + + + + + +
		+ + + + Q + + +
		+ + Q + + + + +

Algumas das razões para justificar tal forma de  representação seriam: Simplicidade e facilidade de entender a estrutura do tabuleiro, facilidade de manipular e atualizar os estados do tabuleiro e compatibilidade com os algoritmos de busca local (como o Hill Climbing) que veremos mais abaixo.

### **2. Implementação Base**

As implementações das funções auxiliares seram dadas nas células abaixo de forma que cada uma possa ser testadas separadamente. As funções seguem a ordem do enunciado:

Gera aleatoriamente Q tabuleiros N × N com N rainhas.

Parâmetros:
- N: Número de rainhas e tamanho do tabuleiro.
- Q: Número de tabuleiros a serem gerados.
    
Retorna:
Uma lista de Q tabuleiros, onde cada tabuleiro é representado como uma N-tupla.
"""

#Bibliotecas
import math
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

"""#### Função tabuleiro()

Entrada : um número N, e Q tabuleiros

Saída : uma lista de N-tuplas aleatórias do conjunto [1, N]^N de tamanho i

"""

def tabuleiro(N, Q):
    tabuleiros = []
    for _ in range(Q):
        tabuleiro_atual = tuple(random.randint(1, N) for _ in range(N))
        tabuleiros.append(tabuleiro_atual)
    return tabuleiros

#Exemplo
tabuleiros_gerados = tabuleiro(4, 2)
for i, tabuleiro_atual in enumerate(tabuleiros_gerados, 1):
    print(tabuleiro_atual)

"""#### Função todosVizinhos()

Entrada: uma N-tupla do conjunto [1, N]^N

Saída: um conjunto de todas as possíveis N-tuplas da entrada modificada de modo que apenas uma das suas componentes é alterada, isso é, um tabuleiro vizinho é o tabuleiro atual, porém apenas uma raínha é mudada de coluna
"""

def todosVizinhos(tabuleiro):
	tamanho		= len(tabuleiro)	# tamanho da N-tupla
	conjunto	= set()						# conjunto de vizinhos

	# percorre todas as linhas e colunas
	for l in range(tamanho):
		for k in range(tamanho):
			c	= k + 1	# coluna nova
			if c != tabuleiro[l]: # se c for uma coluna diferente
				vizinho	= tuple(tabuleiro[i] if i != l else c for i in range(tamanho))
				conjunto.add(vizinho)
	return conjunto

# Exemplo
ts = tabuleiro(4,2)
vizinhos = todosVizinhos(ts[0])
print(vizinhos)

"""#### Função umVizinho()

Entrada	: uma N-tupla do conjunto [1, N]^N

Saída	: a N-tupla da entrada modificada de modo que apenas uma das componentes é alterada com um número aleatório de [1, 8] \ {o valor da componente}
"""

def umVizinho(tabuleiro):
	tamanho	= len(tabuleiro)					    # tamanho de uma N-tupla
	linha	= random.randrange(tamanho)	    # uma linha aleatória
	coluna	= tabuleiro[linha]				    # uma coluna da rainha da linha escolhida
	c	= random.randrange(tamanho - 1) + 1 # uma coluna nova
	if coluna <= c:
		c + 1
	return tuple(tabuleiro[i] if i != linha else c for i in range(tamanho))

# Exemplo
ts = tabuleiro(4, 1)
vizinho = umVizinho(ts[0])
print(vizinho)

"""#### Função numeroAtaques()

Entrada	: uma N-tupla do conjunto [1, N]^N

Saída	: quantidade de conjuntos de duas rainhas que se atacam
"""

def numeroAtaques(tabuleiro):
	tamanho	= len(tabuleiro)	# tamanho de uma N-tupla
	contador = 0							# contador para quantos conjuntos de duas rainhas que se atacam
	for i in range(tamanho): # forma de evitar repetições de conjuntos de duas rainhas
		for j in range(i):
			rainhaA	= (i, tabuleiro[i])
			rainhaB	= (j, tabuleiro[j])
			if ( # no caso de duas rainhas se atacarem, incremente o contador
				rainhaA[0] == rainhaB[0] or
				rainhaA[1] == rainhaB[1] or
				abs(rainhaA[0] - rainhaB[0]) == abs(rainhaA[1] - rainhaB[1])
			):
				contador += 1
	return contador

# Exemplo
ts = tabuleiro(4, 1)
nAtaques = numeroAtaques(ts[0])
print(nAtaques)

"""### **3. Hill Climbing**

As implementações das funções principais seram dadas nas células abaixo de forma que cada uma possa ser testadas separadamente. As funções são:   
```
hcPrimeiraEscolha()  
Entrada: uma N-tupla do conjunto [1, N]^N
Saída: uma N-tupla do conjunto [1, N]^N que é mínimo local de numeroAtaques

hcMelhorEscolha()
Entrada: uma N-tupla do conjunto [1, N]^N
Saída: uma N-tupla do conjunto [1, N]^N que é mínimo local de numeroAtaques
```
As analises serão fornecidas no fim.

"""

def hcPrimeiraEscolha(tabuleiro):
	minimoLocal	= False															# check do while loop da função
	tabuleiroAtual = tabuleiro
	funcaoObjetivo = numeroAtaques(tabuleiroAtual)
	contador = 0																	  # total de tabuleiros correntes já gerados
	ListafuncaoObjetivo = []
	ListafuncaoObjetivo.append(numeroAtaques(tabuleiroAtual))

	# enquanto um mínimo local não foi encontrado
	while minimoLocal == False:
		contador += 1				# vai ser gerado um tabuleito corrente no loop
		minimoLocal	= True	# se inicia como True em cada loop. No encontro de um vizinho melhor, troca para False

		vizinhosConjunto = set()
		v	= umVizinho(tabuleiroAtual)
		f	= numeroAtaques(v)						# função objetivo de v

		# se o vizinho aleatório já não apareceu antes
		while v not in vizinhosConjunto:
			# se esse vizinho for melhor que o tabuleiroAtual, substitui
			if f < funcaoObjetivo:
				minimoLocal	= False		# garante a repetição do loop
				tabuleiroAtual = v
				funcaoObjetivo = f
				break
			else:
				vizinhosConjunto.add(v)				# adiciona o vizinho já testado no conjunto de vizinhos
				v	= umVizinho(tabuleiroAtual)
				f	= numeroAtaques(v)

		# no caso de um vizinho melhor ter sido encontrado, pula o loop atual e inicia um novo
		if minimoLocal == False:
			continue

		vizinhosConjunto = todosVizinhos(tabuleiroAtual)	# conjunto de todos os vizinhos de tabuleiroAtual possíveis

		# busca o primeiro vizinho melhor
		for v in vizinhosConjunto:
			f	= numeroAtaques(v)
			# se o vizinho for melhor que o tabuleiroAtual, substitui pelo vizinho
			if f < funcaoObjetivo:
				minimoLocal	= False
				tabuleiroAtual = v
				funcaoObjetivo = f		# substitui a função objetivo do tabuleiroAtual pelo do vizinho
				break
		ListafuncaoObjetivo.append(funcaoObjetivo)

	if len(ListafuncaoObjetivo) > 1 and ListafuncaoObjetivo[len(ListafuncaoObjetivo)-1] == ListafuncaoObjetivo[len(ListafuncaoObjetivo)-2]:
		ListafuncaoObjetivo.pop()
	return tabuleiroAtual, funcaoObjetivo, contador, ListafuncaoObjetivo

def hcMelhorEscolha(tabuleiro):
	minimoLocal		= False														# check do while loop da função
	tabuleiroAtual = tabuleiro
	funcaoObjetivo  = numeroAtaques(tabuleiroAtual)
	contador = 0																		# total de tabuleiros correntes já gerados
	ListafuncaoObjetivo = []

	# enquanto um mínimo local não foi encontrado
	while minimoLocal == False:
		ListafuncaoObjetivo.append(funcaoObjetivo)			 # adicionando a função objetivo na lista de valores
		contador += 1																     # vai ser gerado um tabuleito corrente no loop
		minimoLocal	= True														   # se inicia como True em cada loop. No encontro de um vizinho melhor, troca para Falsee
		vizinhosConjunto = todosVizinhos(tabuleiroAtual)
		menorVizinho = None
		menorFuncao	= 0

		# procura o vizinho com a menor função objetivo
		for v in vizinhosConjunto:
			f	= numeroAtaques(v)	# função objetivo de v
			# define menorVizinho caso ele não tenha sido definido antes
			if menorVizinho is None:
				menorVizinho = v
				menorFuncao		= f
			# se o vizinho for melhor que o tabuleiroAtual, substitui pelo vizinho
			if f < menorFuncao:
				menorVizinho = v
				menorFuncao	= f
			# se o vizinho for tão bom quanto o menor deles, escolhe aleatoriamente um deles
			if f == menorFuncao:
				menorVizinho = random.choice((v, menorVizinho))

		# se o vizinho for melhor que o tabuleiroAtual, substitui pelo vizinho
		if menorFuncao < funcaoObjetivo:
			minimoLocal	= False
			tabuleiroAtual = menorVizinho
			funcaoObjetivo = menorFuncao

	if len(ListafuncaoObjetivo) > 1 and ListafuncaoObjetivo[len(ListafuncaoObjetivo)-1] == ListafuncaoObjetivo[len(ListafuncaoObjetivo)-2]:
		ListafuncaoObjetivo.pop()
	return tabuleiroAtual, funcaoObjetivo, contador, ListafuncaoObjetivo

"""#### Funções Auxiliares"""

def printTabuleiro(tabuleiro):
	lenght = len(tabuleiro) # quantidade de linhas no tabuleiro
	for i in range(lenght):
		left = tabuleiro[i] - 1
		right	= lenght - tabuleiro[i]
		print('X ' * left + 'Q ' + 'X ' * right)  # printa a linha

def printGrafico(lista, title):
  fig = plt.figure(figsize=(10,7.5)) # define uma nova figura de gráfico e seu tamanho
  fig.tight_layout()
  plt.title(title)

  plt.axis([0, len(lista)+1, 0, max(lista, key=int) + 1]) # define os eixos estéticos do gráfico (Limites da area observada)
  axes = fig.gca() # óbtem o subplot dos eixos do gráfico defindos acima

  # determina que cada tick de intervalo entre os pontos dos eixos são numeros inteiros
  axes.yaxis.set_major_locator(MaxNLocator(integer=True))
  axes.xaxis.set_major_locator(MaxNLocator(integer=True))

  plt.grid(fillstyle='full', dashes=(5,2,1,2)) # exige que exista um grid (Ele passara por cima dos ticks de intervalo)

  # define as legendas de cada eixo
  plt.ylabel('Quantidade de Ataques')
  plt.xlabel('Sequencia de Tabuleiros')
  x = list(range(1,len(lista)+1)) # cria uma lista de numeros inteiros que começa em 1 e vai até o ultimo tabuleiro gerado + 1. O tabuleiro inicial é o 1 e o final é len + 1

  # plota os tabuleiros gerados e suas quantidades de ataques marcando os pontos com uma bolinha
  plt.plot(x, lista, marker="o")

"""### Análise -> Hill Climb Primeira Escolha

Resultados:

tabuleiro 4x4   
  vezes executado: 1  
  média de estados gerados: 4.0

tabuleiro 8x8   
  vezes executado: 15.5   
  média de estados gerados: 6.39   

tabuleiro 16x16   
  vezes executado: 27.6   
  média de estados gerados: 15.7   

tabuleiro 32x32   
  vezes executado: 108   
  média de estados gerados: 25.37

#### Tamanho 4x4
"""

### Tamanho 4x4
quantidade = 10
ts = tabuleiro(4,quantidade)

for x in range(quantidade):
  t = ts[x]

  print('Inicial \n')
  printTabuleiro(t)
  hc = hcPrimeiraEscolha(t)
  print()
  print('Tabuleiro Primeira Execução\n')
  printTabuleiro(hc[0])
  print()
  printGrafico(hc[3], 'Primeira Execução')
  print()
  solucao = hc[1] == 0
  print('Solução: ' + str(solucao) + '; Quantidade de Ataques: ' + str(hc[1]))
  print()

  if not solucao:
    i = 1
    g = hc[2]
    while 0 < hc[1]:
      i += 1
      hc = hcPrimeiraEscolha(t)
      g += hc[2]

    print('Tabuleiro Solução')
    printTabuleiro(hc[0])
    print()
    print('Quantidade de Execuções: ' + str(i))
    printGrafico(hc[3], 'Solução')

"""#### Tamanho 8x8

"""

quantidade = 1
ts = tabuleiro(8,quantidade)

for x in range(quantidade):
  t = ts[x]
  print('Tabuleiro Padrão Inicial')
  printTabuleiro(t)
  print()
  hc = hcPrimeiraEscolha(t)
  print('Tabuleiro Primeira Execução')
  printTabuleiro(hc[0])
  print()
  printGrafico(hc[3], 'Primeira Execução')
  print()
  solucao = hc[1] == 0
  print('Solução: ' + str(solucao) + '; Quantidade de Ataques: ' + str(hc[1]))
  print()

  if not solucao:
    i = 1
    g = hc[2]
    while 0 < hc[1]:
      i += 1
      hc = hcPrimeiraEscolha(t)
      g += hc[2]

    print('Tabuleiro Solução')
    printTabuleiro(hc[0])
    print()
    print('Quantidade de Execuções: ' + str(i))
    printGrafico(hc[3], 'Solução')

"""#### Tamanho 16x16"""

quantidade = 1
ts = tabuleiro(16, quantidade)

for x in range(quantidade):
  t = ts[x]

  print('Tabuleiro Padrão Inicial')
  printTabuleiro(t)
  print()
  hc = hcPrimeiraEscolha(t)
  print('Tabuleiro Primeira Execução')
  printTabuleiro(hc[0])
  print()
  printGrafico(hc[3], 'Primeira Execução')
  print()
  solucao = hc[1] == 0
  print('Solução: ' + str(solucao) + '; Quantidade de Ataques: ' + str(hc[1]))
  print()

  if not solucao:
    i = 1
    g = hc[2]
    while 0 < hc[1]:
      i += 1
      hc = hcPrimeiraEscolha(t)
      g += hc[2]

    print('Tabuleiro Solução')
    printTabuleiro(hc[0])
    print()
    print('Quantidade de Execuções: ' + str(i))
    printGrafico(hc[3], 'Solução')

"""#### Tamanho 32x32"""

quantidade = 1
ts = tabuleiro(32,quantidade)

for x in range(quantidade):
  t = ts[x]
  print('Tabuleiro Padrão Inicial')
  printTabuleiro(t)
  print()
  hc = hcPrimeiraEscolha(t)
  print('Tabuleiro Primeira Execução')
  printTabuleiro(hc[0])
  print()
  printGrafico(hc[3], 'Primeira Execução')
  print()
  solucao = hc[1] == 0
  print('Solução: ' + str(solucao) + '; Quantidade de Ataques: ' + str(hc[1]))
  print()

  if not solucao:
    i = 1
    g = hc[2]
    while 0 < hc[1]:
      i += 1
      hc = hcPrimeiraEscolha(t)
      g += hc[2]
    print('Tabuleiro Solução')
    printTabuleiro(hc[0])
    print()
    print('Quantidade de Execuções: ' + str(i))
    printGrafico(hc[3], 'Solução')

"""### Análise -> Hill Climb Melhor Escolha

Resultados:

tabuleiro 4x4   
vezes executado: 1   
média de estados gerados: 3.0   

tabuleiro 8x8   
vezes executado: 7.5   
média de estados gerados: 4.44   

tabuleiro 16x16   
vezes executado: 32.5   
média de estados gerados: 8.39   

tabuleiro 32x32   
vezes executado: 50.3   
média de estados gerados: 14.4

#### Tamanho 4x4
"""

quantidade = 1
ts = tabuleiro(4,quantidade)

for x in range(quantidade):
  t = ts[x]
  print('Tabuleiro Padrão Inicial')
  printTabuleiro(t)
  print()
  hc = hcMelhorEscolha(t)
  print('Tabuleiro Primeira Execução')
  printTabuleiro(hc[0])
  print()
  printGrafico(hc[3], 'Primeira Execução')
  print()
  i = 1
  g = hc[2]
  solucao = hc[1] == 0
  print('Solução: ' + str(solucao) + '; Quantidade de Ataques: ' + str(hc[1]))
  print()

  if not solucao:
    while 0 < hc[1]:
      i += 1
      hc = hcMelhorEscolha(t)
      g += hc[2]
    print('Tabuleiro Solução')
    printTabuleiro(hc[0])
    print()
    print('Quantidade de Execuções: ' + str(i))
    printGrafico(hc[3], 'Solução')

"""#### Tamanho 8x8

"""

quantidade = 1
ts = tabuleiro(8, quantidade)

for x in range(quantidade):
  t = ts[x]
  print('Tabuleiro Padrão Inicial')
  printTabuleiro(t)
  print()
  hc = hcMelhorEscolha(t)
  print('Tabuleiro Primeira Execução')
  printTabuleiro(hc[0])
  print()
  printGrafico(hc[3], 'Primeira Execução')
  print()
  i = 1
  g = hc[2]
  solucao = hc[1] == 0
  print('Solução: ' + str(solucao) + '; Quantidade de Ataques: ' + str(hc[1]))
  print()

  if not solucao:
    while 0 < hc[1]:
      i += 1
      hc = hcMelhorEscolha(t)
      g += hc[2]
    print('Tabuleiro Solução')
    printTabuleiro(hc[0])
    print()
    print('Quantidade de Execuções: ' + str(i))
    printGrafico(hc[3], 'Solução')

"""#### Tamanho 16x16

"""

quantidade = 1
ts = tabuleiro(16,quantidade)

for x in range(quantidade):
  t = ts[x]
  print('Tabuleiro Padrão Inicial')
  printTabuleiro(t)
  print()
  hc = hcMelhorEscolha(t)
  print('Tabuleiro Primeira Execução')
  printTabuleiro(hc[0])
  print()
  printGrafico(hc[3], 'Primeira Execução')
  print()
  i = 1
  g = hc[2]
  solucao = hc[1] == 0
  print('Solução: ' + str(solucao) + '; Quantidade de Ataques: ' + str(hc[1]))
  print()

  if not solucao:
    while 0 < hc[1]:
      i += 1
      hc = hcMelhorEscolha(t)
      g += hc[2]
    print('Tabuleiro Solução')
    printTabuleiro(hc[0])
    print()
    print('Quantidade de Execuções: ' + str(i))
    printGrafico(hc[3], 'Solução')

"""#### Tamanho 32x32

"""

quantidade = 1
ts = tabuleiro(32,quantidade)

for x in range(quantidade):
  t = ts[x]
  print('Tabuleiro Padrão Inicial')
  printTabuleiro(t)
  print()
  hc = hcMelhorEscolha(t)
  print('Tabuleiro Primeira Execução')
  printTabuleiro(hc[0])
  print()
  printGrafico(hc[3], 'Primeira Execução')
  print()
  i = 1
  g = hc[2]
  solucao = hc[1] == 0
  print('Solução: ' + str(solucao) + '; Quantidade de Ataques: ' + str(hc[1]))
  print()

  if not solucao:
    while 0 < hc[1]:
      i += 1
      hc = hcMelhorEscolha(t)
      g += hc[2]
    print('Tabuleiro Solução')
    printTabuleiro(hc[0])
    print()
    print('Quantidade de Execuções: ' + str(i))
    printGrafico(hc[3], 'Solução')

"""####Conclusões

Em geral, o hcPrimeiraEscolha, aquele que testa todos os vizinhos e escolhe o melhor, costuma demandar metade das vezes a ser executado comparado com o hcMelhorEscolha, aquele que pega o primeiro vizinho que melhore a função objetivo.

Além disso, o hcPrimeiraEscolha gera metade dos estados em média, comparado com o hcMelhorEscolha.

### **4. Simulated Annealing**

O algoritmo SA é implementado na célula abaixo, onde:   

Entrada: dois números inteiros n, maxIt e dois números reais tempInicial, alpha      

Saída: uma N-tupla do conjunto [1, N]^N   

A questões restantes serão respondidas logo em seguida:
"""

def simulatedAnnealing(n, maxIt, tempInicial, alpha):
	tabuleiroAtual = tabuleiro(n)
	tempAtual	= tempInicial
	melhorTabuleiro	= tabuleiroAtual						    # variável auxiliar na busca do melhor tabuleiro
	funcaoObjetivo = numeroAtaques(tabuleiroAtual)
	melhorFuncao	= funcaoObjetivo
	contador = 1										                # quantidade de tabuleiros correntes gerados

	# faz maxIt iterações
	for _ in range(maxIt):
		v	= vizinho(tabuleiroAtual)	# vizinho aleatório
		f	= numeroAtaques(v)

		# se o vizinho for melhor que o tabuleiroAtual, substitui tabuleiroAtual pelo vizinho
		if f < funcaoObjetivo:
			contador += 1
			tabuleiroAtual = v
			funcaoObjetivo = f

			# se o vizinho for o melhor tabuleiro até então, substitui melhorTabuleiro pelo vizinho
			if f < melhorFuncao:
				melhorTabuleiro	= v
				melhorFuncao = f
		else:
      # se não, substitui tabuleiroAtual pelo vizinho se tiver chance
			if random.random() < math.exp(float(funcaoObjetivo - f)/tempAtual):
				contador += 1
				tabuleiroAtual = v
				funcaoObjetivo = f
		tempAtual *= alpha	# aumenta a temperatura

	print(tempAtual)
	return melhorTabuleiro, melhorFuncao, contador

def tabuleiroNovo(n):
	return tuple(random.randrange(n) + 1 for _ in range(n))

tabuleiros = []
tabuleiros.append(tabuleiroNovo(4))
tabuleiros.append(tabuleiroNovo(8))
tabuleiros.append(tabuleiroNovo(16))
tabuleiros.append(tabuleiroNovo(32))

for t, maxIt, tempInit, alpha in tabuleiros:
	l = len(t)
	print('tabuleiro ' + str(len(t)) + 'x' + str(len(t)) + ' : ' + str(t)) # printa t
	printTabuleiro(t) # printa o tabuleiro t
	print()
	print()
	print()

	sa = simulatedAnnealing(l, maxIt, tempInit, alpha)
	while 0 < sa[2]:
		sa = simulatedAnnealing(l, maxIt, tempInit, alpha)
	print('simulatedAnnealing : ' + str(sa[0])) # printa o resultado do simulatedAnnealing
	print('com ' + str(sa[1]) + ' quantidade de ataques')
	print('e ' + str(sa[2]) + ' tabuleiros correntes gerados')
	print()
	print()
	print()

	print('-' * 32)
	print('+' * 32)
	print('-' * 32)
	print()
	print()
	print()

