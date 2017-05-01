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
#	@sa 		http://projetos.imd.ufrn.br/davidcardoso-ti/imd0041/blob/master/simulador_pipeline/pipeline.py

import os, sys			# os, sys 		- recursos de sistema
import shutil 			# shutil 		- operações avançadas de sistema
import mmap 			# mmap 			- suporte à arquivo em memória
import collections		# collections 	- estrutura de dados
import string 			# string 		- string

from datetime import datetime			# datetime 		- data e tempo
from time import sleep 					# sleep 		- pausa a execução da thread atual

"""Variáveis"""
## negrito
BOLD 		= '\033[1m'
## cor padrão para impressões no terminal		
NORMAL 		= '\033[0;0m'		
## cor verde para destacar impressões no terminal
GREEN 		= BOLD+'\033[32m'	
## cor azul para destacar impressões no terminal
BLUE 		= BOLD+'\033[34m'	
## cor branca para destacar impressões no terminal
WHITE 		= BOLD+'\033[37m'	
## cor amarela para destacar impressões no terminal
YELLOW 		= BOLD+'\033[93m'	
## cor vermelha para destacar impressões no terminal
RED 		= BOLD+'\033[91m' 

## quebra de linha
ENDL 		= "\n"
## tabulação	
TAB 		= "\t"
## opção de ação do programa	
ARG_OPTION  = ""
## diretório/arquivo de entrada
ARG_PATH 	= ""
## tamanho máximo do arquivo de entrada (1MB)
MAX_SIZE 	= 1048576
## nome do arquivo de saída
OUTPUT 		= datetime.now().strftime('%Y%m%d%H%M%S')
## extensão do arquivo de saída
EXT 		= ".txt"
## separador	
SEP 		= " " 

## lista de instruções permitidas
INST_ALLOW 	= ['add', 'sub', 'beq', 'bne', 'lw', 'sw', 'j']
## lista de instruções [linha => instrução]
INST_LIST	= []
## dicionário de instruções {(linha, [label, comando, oper1, oper2, oper3])}
INST_DIC 	= {}
## dicionário de labels {(label, linha)}
LABEL_DIC	= {}
## lista de registradores em uso
REG_LOCK 	= []

## 	@brief 		Função para limpar console
def clearConsole():
	print 'Loading...'
	sleep(0.5)
	os.system('cls' if os.name == 'nt' else 'reset')


## 	@brief 		Função printExampleArgs()
# 	@details 	Imprimir explicação dos argumentos via linha de comando
def printExampleArgs():
	print '%sEnter an argument!%s' 									% (ENDL, ENDL)
	print 'Example: ./pipeline.py <folder_path>/<input_file> %s' 	% (ENDL)
	print 'Ending... %s' 											% (ENDL)


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
		print 'Expect 1 argument but %i was given!%s' % (sys.argv.__len__()-1, ENDL)
		printExampleArgs()
		sys.exit()


## 	@brief		Função loadInputFile()
# 	@details 	Carrega o arquivo de entrada
# 	@param 		pathfile - arquivo
# 	@return 	boolean
def loadInputFile(pathfile):
	global INST_LIST, INST_DIC, LABEL_DIC
	# dados do arquivo
	stats = os.stat(pathfile)

	# verifica o tamanho, se é arquivo e tenta abrir o arquivo de entrada
	if stats.st_size <= MAX_SIZE and os.path.isfile(pathfile):
		try:
			input_file = open(pathfile, "r")
		except IOError:
			print "%sError trying to load input file!" % (ENDL)
			return False

		# caso abriu o arquivo de entrada
		with input_file:
			for (line, instruction) in enumerate(input_file):
				# testa se a instrução é permitida
				if instruction.split(SEP)[0] in INST_ALLOW or ':' in instruction.split(SEP)[0]:
					line += 1;
					instruction = instruction.replace('\n', '')
					# preenche a lista de instruções
					INST_LIST.insert(line, instruction)
					# preenche o dicionario de instruções
					instruction = instruction.replace(',', '')
					inst_parts = instruction.split(SEP)
					INST_DIC[line] = inst_parts
					# preenche o dicionário de labels
					if ':' in inst_parts[0]:
						LABEL_DIC[inst_parts[0]] = line
				else:
					print 'Instruction/Label not allowed: %s' % (instruction.split(SEP)[0])
					print 'Allowed instructions: %s' % (INST_ALLOW)
					print 'Labels must have collon symbol (:).'
					return False

			print INST_LIST
			print INST_DIC
			print LABEL_DIC
			print len(INST_DIC)

			input_file.close()
			print "%sInput file loaded: %s" % ( ENDL, pathfile )
			return True
	else:
		print "%sError trying to load input file!" % (ENDL)
		return False


# BLOCO PRINCIPAL DO PROGRAMA
if __name__ == "__main__":

	# limpar console
	clearConsole()

	print "%s==> Pipeline Simulator" % (GREEN)
	print "    Harvard Architecture.%s%s" % (ENDL, NORMAL)

	# validar argumentos
	checkArgs()

	sys.exit()