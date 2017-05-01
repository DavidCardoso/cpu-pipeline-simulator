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
#	@sa 		http://projetos.imd.ufrn.br/davidcardoso-ti/imd0703/blob/master/hmac/guard.py

import os, sys			# os, sys 		- recursos de sistema
import shutil 			# shutil 		- operações avançadas de sistema
import mmap 			# mmap 			- suporte à arquivo em memória

from collections import OrderedDict		# OrderedDict 	- dicionário ordenado
from datetime import datetime			# datetime 		- data e tempo
from string import split 				# split 		- separar strings de acordo com separador

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
## separador CSV	
SEP 		= ";" 
## dicionário
MATCHES 	= {}
## opção de ação do programa (-i, -t ou -x)		
ARG_OPTION  = ""
## diretório a ser aplicado a ação	
ARG_PATH 	= ""
## nome do arquivo de rastreamento
TMP 		= datetime.now().strftime('%Y%m%d%H%M%S')
## extensão do arquivo de rastreamento
EXT 		= ""


## 	@brief 		Função para limpar console
def clearConsole():
	os.system('cls' if os.name == 'nt' else 'reset')


## 	@brief 		Função printExampleArgs()
# 	@details 	Imprimir explicação dos argumentos via linha de comando
def printExampleArgs():
	print '%sGive an option and a folder:%s' 				% (ENDL, ENDL)
	print '-i %sto start folder guard%s' 					% (TAB, ENDL)
	print '-t %sto track the folder%s' 						% (TAB, ENDL)
	print '-x %sto stop folder guard%s' 					% (TAB, ENDL)
	print 'Example: ./guard.py <option> <folder_path> %s' 	% (ENDL)
	print 'Ending... %s' 									% (ENDL)


## 	@brief 		Função checkArgs()
# 	@details 	Validação dos argumentos passados via linha de comando
def checkArgs():
	global ARG_OPTION, ARG_PATH
	if sys.argv.__len__() == 3:
		ARG_OPTION 	= str(sys.argv[1])
		ARG_PATH 	= str(sys.argv[2])
		if ARG_OPTION not in ('-i', '-t', '-x'):
			print 'Invalid option!%s' % (ENDL)
			printExampleArgs()
			sys.exit()
	else:
		print 'Expected 2 arguments but %i was given!%s' % (sys.argv.__len__()-1, ENDL)
		printExampleArgs()
		sys.exit()


## 	@brief 		Função genHMAC()
# 	@details 	Gera HMAC dos arquivos do diretório de forma recursiva
# 	@param 		dir - caminho do diretório
def genHMAC(dir):
	global MATCHES
	# mudando diretorio
	os.chdir(dir)
	# caminho absoluto para diretorio
	dir = os.getcwd()

	# se existe pasta oculta
	if HIDDEN in os.listdir(dir):
		# percorre recursivamente todos os subdiretórios
		for root, dirnames, filenames in os.walk(dir):
			# percore todos os arquivos dos subdiretórios
			for filename in filenames:
				# ignora a pasta oculta
				if root[-len(HIDDEN):] != HIDDEN:
					# caminho completo
					fullpath_filename = os.path.join(root, filename)
					# abre arquivo e lê conteúdo
					f = open(fullpath_filename, "r")
					if f:
						content = f.read()
						f.close()
						# objeto HMAC - submete CAMINHO + CONTEUDO
						h = HMAC_OBJ.hmac(fullpath_filename+content)
						# h = HMAC_OBJ.hmac(content)
						# adiciona caminho absoluto do arquivo e seu respectivo HMAC ao dicionário
						MATCHES.update( {fullpath_filename : h.hexdigest()} )
					else:
						MATCHES.update( {fullpath_filename : 'Error trying to open file!'} )

		# ordenar dicionário por chave (fullpath_filename)
		MATCHES = OrderedDict(sorted(MATCHES.items(), key=lambda t: t[0]))

		# Diretório inválido ou arquivos inexistentes
		if MATCHES.__len__() == 0:
			print 'Invalid folder or there are no files in the folder!%s' % (ENDL)
			printExampleArgs()
			sys.exit()
	else:
		print "%sFolder '%s' not found! You need to start folder guard: %s" % (ENDL, HIDDEN, os.getcwd())
		printExampleArgs()
		sys.exit()
		

## 	@brief		Função createTrackFile()
# 	@details 	Criar arquivo de rastreio contendo os arquivos e os respectivos HMACs
# 	@param 		dir - caminho do diretório
def createTrackFile(dir):
	
	# se existe pasta oculta
	if HIDDEN in os.listdir(dir):
		# mudando para pasta oculta
		os.chdir(dir+'/'+HIDDEN)
		print "%sGenerating new tracking file: %s" % ( ENDL, TMP+EXT )
		# salva dados do dicionário no arquivo de rastreio
		track_file = open(TMP+EXT, "w+")
		if track_file:
			for filename, hash in MATCHES.iteritems():
				track_file.write( str(hash+SEP+filename+ENDL) )
			track_file.close()
			print "%sTracking file saved in: %s" % ( ENDL, os.getcwd() )
		else:
			print "%sError trying to generate tracking file!" % (ENDL)
	else:
		print "%sFolder '%s' not found! You need to start folder guard: %s" % (ENDL, HIDDEN, os.getcwd())
		printExampleArgs()



# BLOCO PRINCIPAL DO PROGRAMA
if __name__ == "__main__":

	# limpar console
	clearConsole()

	print "%s==> Simulador Pipeline" % (WHITE)
	print "    Harvard's Arquitecture.%s%s" % (ENDL, NORMAL)

	# validar argumentos
	checkArgs()

	sys.exit()