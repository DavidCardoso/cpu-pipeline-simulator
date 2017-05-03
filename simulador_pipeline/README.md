README
--

@brief _Informações gerais sobre o projeto_

**Projeto** da disciplina **IMD0041 IOAC**, ministrada pelo Prof. Kayo Gonçalves no curso BTI da UFRN.

Programa
--

_Pipeline Simulator_

Objetivo
--

- O objetivo deste trabalho é **implementar um simulador de pipeline** com cinco estágios (IF, ID, EX, MEM, WB) baseado na arquitura de Harvard.

Informações sobre o programa
--

- O programa foi implementado utilizando a linguagem de programação _Python_.
- Orientações sobre a execução do programa:
	- Via linha de comando, navegue até o diretório onde se localiza o arquivo **pipeline.py**.
	- Pode-ser utilizar **./pipeline.py** ou **python pipeline.py** para executar o programa.
	- É necessário passar um arquivo de entrada como argumento, por exemplo: ./pipeline.py input.txt
	- O arquivo de entrada deve conter um programa escrito em Assembly no formato:
		beq $s0, $s1, DENTRO
		add $t1, $t2, $t3
		lw $t0, 128($t1)
		DENTRO: 
		sub $t1, $t2, $t3
		add $s5, $t1, $t4
	- Apenas as instruções ADD, SUB, BEQ, BNE, LW, SW e J são permitidas.
	- A instrução após algum LABEL deve vir na linha seguinte.
	- Arquivos de entrada vazios, com instruções não permitidas ou maiores do que 1MB serão rejeitados.