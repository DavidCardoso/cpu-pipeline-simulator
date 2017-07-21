#!/usr/bin/env python
# -*- coding: utf-8 -*-

##	@file 		pipeline.py
#	@brief 		Programa Simulador Pipeline.
#	@details 	Baseando-se na Arquitetura de Havard, este programa tem a
#				finalidade de simular um pipeline de cinco estágios (IF, ID, EX, MEM, WB).
#	@since		30/04/2017
#	@date		03/05/2017
#	@author		David Cardoso
#	@copyright	2017 - All rights reserveds
#	@sa 		https://github.com/davidcardoso-ti/cpu-pipeline-simulator/blob/master/pipeline.py

import os, sys			# os, sys 		- recursos de sistema
# import shutil 			# shutil 		- operações avançadas de sistema
# import mmap 			# mmap 			- suporte à arquivo em memória
# import collections		# collections 	- estrutura de dados
# import string 			# string 		- string

from datetime import datetime			# datetime 		- data e tempo
from time import sleep 					# sleep 		- pausa a execução da thread atual

"""Variáveis"""
# negrito
BOLD 		= '\033[1m'
# cor padrão para impressões no terminal		
NORMAL 		= '\033[0;0m'		
# cor verde para destacar impressões no terminal
GREEN 		= BOLD+'\033[32m'	
# cor azul para destacar impressões no terminal
BLUE 		= BOLD+'\033[34m'	
# cor branca para destacar impressões no terminal
WHITE 		= BOLD+'\033[37m'	
# cor amarela para destacar impressões no terminal
YELLOW 		= BOLD+'\033[93m'	
# cor vermelha para destacar impressões no terminal
RED 		= BOLD+'\033[91m' 

# quebra de linha
ENDL 		= "\n"
# tabulação	
TAB 		= "\t"
# opção de ação do programa	
ARG_OPTION  = ""
# diretório/arquivo de entrada
ARG_PATH 	= ""
# tamanho máximo do arquivo de entrada (1MB)
MAX_SIZE 	= 1048576
# nome do arquivo de saída
OUTPUT 		= datetime.now().strftime('%Y%m%d%H%M%S')
# extensão do arquivo de saída
EXT 		= ".txt"
# separador	
SEP 		= " " 

# lista de instruções permitidas
INST_ALLOW 	= ['add', 'sub', 'beq', 'bne', 'lw', 'sw', 'j']
# lista de instruções [linha => instrução]
INST_LIST	= ['']
# dicionário de instruções {linha : [label, comando, oper1, oper2, oper3]}
INST_DIC 	= {}
# dicionário de labels {label : linha}
LABEL_DIC	= {}
# lista de registradores em uso
REG_LOCK 	= []
# dicionário de estágios do pipeline
PIPE_STAGES = {'IF' : '0', 'ID' : '0', 'EX' : '0', 'MEM' : '0', 'WB' : '0'}
# dicionário de regras de dependências 
# instrução anterior (parent) é necessária para a seguinte (child) nos operadores 2, 3 e/ou 4
INST_DEP	= {
	'add' 	: {'add':[3,4], 'sub':[3,4], 'lw':[3], 'sw':[2], 'beq':[2,3], 'bne':[2,3],},
	'sub' 	: {'add':[3,4], 'sub':[3,4], 'lw':[3], 'sw':[2], 'beq':[2,3], 'bne':[2,3],},
	'lw'	: {'add':[3,4], 'sub':[3,4], 'beq':[2,3], 'bne':[2,3],},
	}
# instruções de salto (jump)
INST_JUMPS 	= ['beq', 'bne', 'j']
# contador de programa
PC 			= 1
# quantidade de instruções
INST_QTD 	= 0
# quantidade de ciclos (clocks)
CLOCKS 		= 0


## 	@brief 		Função para limpar console
def clearConsole():
	print('Loading...')
	sleep(0.5)
	os.system('cls' if os.name == 'nt' else 'reset')


## 	@brief 		Função printExampleArgs()
# 	@details 	Imprimir explicação dos argumentos via linha de comando
def printExampleArgs():
	print('%sEnter an argument!%s') % (ENDL, ENDL)
	print('Example: ./pipeline.py <folder_path>/<input_file> %s') % (ENDL)
	print('Ending... %s') % (ENDL)


## 	@brief 		Função checkArgs()
# 	@details 	Validação dos argumentos passados via linha de comando
def checkArgs():
	global ARG_OPTION, ARG_PATH
	if sys.argv.__len__() == 2:
		ARG_PATH 	= str(sys.argv[1])
		if not loadInputFile(ARG_PATH):
			printExampleArgs()
			sys.exit()
	else:
		print('Expect 1 argument but %i was given!%s') % (sys.argv.__len__()-1, ENDL)
		printExampleArgs()
		sys.exit()


## 	@brief		Função loadInputFile()
# 	@details 	Carrega o arquivo de entrada
# 	@param 		pathfile - arquivo
# 	@return 	boolean
def loadInputFile(pathfile):
	global INST_LIST, INST_DIC, LABEL_DIC, INST_QTD
	# dados do arquivo
	stats = os.stat(pathfile)

	# verifica o tamanho, se é arquivo e tenta abrir o arquivo de entrada
	if stats.st_size <= MAX_SIZE and os.path.isfile(pathfile):
		try:
			input_file = open(pathfile, "r")
		except IOError:
			print("%sError trying to load input file!") % (ENDL)
			return False

		# caso abriu o arquivo de entrada
		with input_file:
			line = 1
			for (index, instruction) in enumerate(input_file):
				# testa se a instrução é permitida
				if instruction.split(SEP)[0] in INST_ALLOW or ':' in instruction.split(SEP)[0]:
					instruction = instruction.replace('\n', '')
					# preenche a lista de instruções
					INST_LIST.insert(line, instruction)
					# preenche o dicionario de instruções
					instruction = instruction.replace('$zero', '$00')
					instruction = instruction.replace(',', '')
					inst_parts = instruction.split(SEP)
					if inst_parts[0] in ['lw', 'sw']:
						inst_parts[2] = str(inst_parts[2])[-4:-1]
					# preenche o dicionário de labels
					if ':' in inst_parts[0]:
						label = inst_parts[0].replace(':','')
						LABEL_DIC[label] = line
						# INST_DIC[line] = [label]
					else:
						INST_DIC[line] = ['']+inst_parts
						line += 1
						INST_QTD += 1
				else:
					print('Instruction/Label not allowed: %s') % (instruction.split(SEP)[0])
					print('Allowed instructions: %s') % (INST_ALLOW)
					print('Labels must have collon symbol (:).')
					return False

			print(INST_LIST)
			print(INST_DIC)
			print(LABEL_DIC)

			input_file.close()

			if INST_QTD == 0:
				print('Input file has no instructions to be processed!')
				return False
			else:
				print("%sInput file loaded: %s%s") % ( ENDL, pathfile, ENDL )
				return True
	else:
		print("%sError trying to load input file!") % (ENDL)
		return False

## 	@brief 		Função identifyDeps()
# 	@details 	Identifica as dependências
# 	@param 		reg - registrador base para verificação de dependência
# 	@return 	dicionário com as dependências
def identifyDeps(reg):
	hasDep = {}
	for (line, parent) in INST_DIC.iteritems():
		if parent[1] in INST_DEP:
			for (key, child) in INST_DIC.iteritems():
				if key > line:
					deps = INST_DEP.get(parent[1], 0)
					opers = deps.get(child[1], 0)
					if type(opers) == list:
						for i in opers:
							if child[i] == parent[reg]:
								# print("linha %s depende da linha %s" % (key, line)
								if key in hasDep:
									hasDep[key].append(line)
								else:
									hasDep[key] = [line]
	return hasDep


## 	@brief 		Função checkJump()
# 	@details 	Verifica se há jump para configurar corretamente o próximo PC
# 	@param 		pc - program counter atual
# 	@return 	próximo PC
def checkJump(pc):
	jump = INST_DIC[pc][1]
	if jump in INST_JUMPS:
		label = INST_DIC[pc][-1]
		return LABEL_DIC[label]
	else:
		return pc + 1


## 	@brief 		Função printPipelineClock()
#	@details	Imprime as instruções que estão nos estágios do pipeline em determinado clock
#	@param 		clocks - número do clock atual
#	@param 		stages - estágios do pipeline
def printPipelineClock(clocks, stages):
	print('--------------------------------------------')
	print('Clock #%s:') % (clocks)
	print('IF:%s%s') % (TAB, INST_LIST[int(stages['IF'])] if type(stages['IF']) == int else stages['IF'].replace('end','0'))
	print('ID:%s%s') % (TAB, INST_LIST[int(stages['ID'])] if type(stages['ID']) == int else stages['ID'].replace('end','0'))
	print('EX:%s%s') % (TAB, INST_LIST[int(stages['EX'])] if type(stages['EX']) == int else stages['EX'].replace('end','0'))
	print('MEM:%s%s') % (TAB, INST_LIST[int(stages['MEM'])] if type(stages['MEM']) == int else stages['MEM'].replace('end','0'))
	print('WB:%s%s') % (TAB, INST_LIST[int(stages['WB'])] if type(stages['WB']) == int else stages['WB'].replace('end','0'))


## 	@brief 		Função writePipelineOutput()
#	@details	Escreve as instruções que estão nos estágios do pipeline em um arquivo de saída
#	@param 		clocks - número do clock atual
#	@param 		stages - estágios do pipeline
def writePipelineOutput(clocks, stages):
	file = open(OUTPUT+EXT, 'a')
	out = '--------------------------------------------\n'
	out += 'Clock #%s:\n' % (clocks)
	out += 'IF:%s%s%s\n' % (TAB, INST_LIST[int(stages['IF'])] if type(stages['IF']) == int else stages['IF'].replace('end','0'), ('\t(PC='+str(stages['IF'])+')') if type(stages['IF']) == int else '')
	out += 'ID:%s%s%s\n' % (TAB, INST_LIST[int(stages['ID'])] if type(stages['ID']) == int else stages['ID'].replace('end','0'), ('\t(PC='+str(stages['ID'])+')') if type(stages['ID']) == int else '')
	out += 'EX:%s%s%s\n' % (TAB, INST_LIST[int(stages['EX'])] if type(stages['EX']) == int else stages['EX'].replace('end','0'), ('\t(PC='+str(stages['EX'])+')') if type(stages['EX']) == int else '')
	out += 'MEM:%s%s%s\n' % (TAB, INST_LIST[int(stages['MEM'])] if type(stages['MEM']) == int else stages['MEM'].replace('end','0'), ('\t(PC='+str(stages['MEM'])+')') if type(stages['MEM']) == int else '')
	out += 'WB:%s%s%s\n' % (TAB, INST_LIST[int(stages['WB'])] if type(stages['WB']) == int else stages['WB'].replace('end','0'), ('\t(PC='+str(stages['WB'])+')') if type(stages['WB']) == int else '')
	file.write(out)
	file.close()


# BLOCO PRINCIPAL DO PROGRAMA
if __name__ == "__main__":

	# limpar console
	clearConsole()

	print("%s==> Pipeline Simulator") % (GREEN)
	print("    Harvard Architecture%s") % (ENDL)
	print("    Stages: IF, ID, EX, MEM, WB%s%s") % (ENDL, NORMAL)

	# validar argumentos passados via linha de comando
	checkArgs()

	# identificar dependências
	hasDep = identifyDeps(2)
	# print hasDep

	# processamento das instruções
	while PIPE_STAGES['MEM'] != 'end':
		# contador de clocks
		CLOCKS += 1

		# segue o processamento das instruções através dos estágios do pipeline
		PIPE_STAGES['WB'] = PIPE_STAGES['MEM']
		PIPE_STAGES['MEM'] = PIPE_STAGES['EX']
		PIPE_STAGES['EX'] = PIPE_STAGES['ID']
		PIPE_STAGES['ID'] = PIPE_STAGES['IF']

		# verifica se ainda tem mais instruções a serem executadas
		if PC <= INST_QTD:
			depend = False
			# verifica se a instrução atual tem dependência no pipeline
			if PC in hasDep:
				for dep in hasDep[PC]:
					if depend:
						break
					for (stage, line) in PIPE_STAGES.iteritems():
						# insere bolha, se alguma instrução parent estiver sendo processada
						if stage != 'WB' and dep == line:
							PIPE_STAGES['IF'] = 'NOP'
							depend = True
							break
						else:
						# insere a instrução PC no pipeline, se a instrução parent estiver no estágio WB
							if stage == 'WB' and dep == line:
								depend = False
			if not depend:
				PIPE_STAGES['IF'] = PC
				PC = checkJump(PC)
		else:
			PIPE_STAGES['IF'] = 'end'

		# situação atual do pipeline
		# printPipelineClock(CLOCKS, PIPE_STAGES)
		writePipelineOutput(CLOCKS, PIPE_STAGES)

	# impressão do total de ciclos
	print("Total clocks: %s") % (CLOCKS)

 	# impressão das situações de cada ciclo do pipeline
	file = open(OUTPUT+EXT, 'r')
	print(file.read())
	file.close()

	# fim do programa
	sys.exit()