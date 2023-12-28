% PF 22.2 - Questão 1 - Escreva a função retira(ListaInicial, ListaFinal) que recebe uma lista em ListaInicial e retorne em ListaFinal a lista sem repetições dos elementos. 
Exemplo: ? − retira([1, 2, 1, 3, 2, 1, 3, 4],L). L = [1, 2, 3, 4]

retira(ListaInicial, ListaFinal) :-
    sem_repeticao(ListaInicial, ListaFinal).

sem_repeticao([], []).
% Se o elemento X está presente no restante da lista (RestoI), ele é removido usando member. Em seguida, a recursão é feita para o restante da lista (RestoI) para continuar removendo elementos repetidos.
sem_repeticao([X|RestoI], LF) :-
    member(X, RestoI), !, 
    sem_repeticao(RestoI, LF).

sem_repeticao([X|RestoI], [X|RestoF]) :-
    sem_repeticao(RestoI, RestoF).

-----------------------------------------------------------------------------------------------------------------
% P1 22.2 - Questão 4 - Faça em prolog uma função paridade que, dada uma lista L e dois inteiros P e I, percorra a lista uma vez e retorne nas variáveis a quantidade de números pares e ímpares.
? − paridade([1, 2, 3, 4, 5, 8, 3, 5], P, I). P = 3, I = 5

paridade(L, P, I) :-
	quantidade(L, Pares, Impares),
	P is Pares,
	I is Impares.

quantidade([], 0, 0). % Caso base: lista vazia

quantidade([X|Resto], Pares, Impares) :-
	Z is X mod 2, Z = 1, !, % Caso em que o número é ímpar
	quantidade(Resto, Pares, RestoImpares),
	Impares is RestoImpares + 1;
    
	Z is X mod 2, Z = 0, !, % Caso em que o número é par
	quantidade(Resto, RestoPares, Impares),
	Pares is RestoPares + 1.

-----------------------------------------------------------------------------------------------------------------
% P1 23.1 / P1 22.2 - Questão 2 - Defina o predicado maiorsoma(L1, L2, S, L3) que recebe como entrada as lista de números L1 e L2 e um limite S, e retorna a lista L3 formada por valores maiores que S obtidos pela soma de um elemento X de L1 com um elemento Y de L2.
Exemplos: 
?- maiorsoma([1,2,3],[6,1,1],5,L). L = [7, 8, 9]
?- maiorsoma([1,2,3],[6,1,1],10,L). L = []

maiorsoma(L1, L2, S, L3) :-
    soma(L1, L2, S, L3).

soma([], _, _, []).
% Caso em que a soma de elementos de L1 e L2 é maior que Limite
soma([X | RestoL1], L2, Limite, [Soma | RestoL3]) :-  
    member(Y, L2),  					% Seleciona um elemento Y de L2
    Soma is X + Y,  					% Calcula a soma
    Soma > Limite,  					% Verifica se a soma é maior que Limite
    soma(RestoL1, L2, Limite, RestoL3). % Chama recursivamente para o restante das listas, mantendo as somas que excedem o limite.

% Caso em que a soma de elementos de L1 e L2 não é maior que Limite
soma([_ | RestoL1], L2, Limite, L3) :-   
    soma(RestoL1, L2, Limite, L3).     

-----------------------------------------------------------------------------------------------------------------
% P1 23.1 - Questão 1 - Escreva um programa Prolog que, dada uma lista de números inteiros L1, retorna o valor obtido pela soma dos elementos ímpares menos a soma dos elementos pares. O programa deve percorrer a lista L1 uma única vez. 
Exemplo: ?- resposta([5,3,2,4],X). X = -2

resposta(Lista, Resultado) :-
    somar_impares_pares(Lista, SomaImpares, SomaPares),
    Resultado is SomaImpares - SomaPares.

somar_impares_pares([], 0, 0).  % Caso base: listas vazias

somar_impares_pares([X | Resto], SomaImpares, SomaPares) :-
        Y is X mod 2, Y = 1, !,  % Se X é ímpar
		% Se verdadeiro, chama recursivamente para o restante da lista e obtém a soma de ímpares
        somar_impares_pares(Resto, RestoImpares, SomaPares), 
        SomaImpares is X + RestoImpares; 
      	
    	Y is X mod 2, Y = 0, !,  % Se X é par
        somar_impares_pares(Resto, SomaImpares, RestoPares),
        SomaPares is X + RestoPares.
-----------------------------------------------------------------------------------------------------------------
% PF 23.1 - Questão 1 - Faça um programa prolog que dada uma lista L1 de números inteiros maiores ou iguais a zero, retorna a lista L2 formada por X cópias de cada número X pertencente a L1. 
Por exemplo: ?- multi([2,1,3,4,0], L). L = [2,2,1,3,3,3,4,4,4,4].”

multi(L1, L2) :-
    repeticao(L1, L2).

repeticao([], []).
% Define a regra recursiva para a multiplicação.
repeticao([X|Resto1], L2) :- 
    N is X,
    geracao(X, N, Copias), 				% Gerar uma lista Copias contendo N cópias do elemento X.   
	repeticao(Resto1, RestoCopias), 	% Chama recursivamente para o restante da lista Resto1.	
	append(Copias, RestoCopias, L2). 	% Concatena as cópias geradas (Copias) com o restante da lista resultante (RestoCopias) para formar a lista final L2

geracao(_, 0, []).   					% Essa funçãoo trata cada elemento de cada vez
geracao(X, N, [X|Resto2]) :-
    N > 0,
    Z is N - 1,
    geracao(X, Z, Resto2).
