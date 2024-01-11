import numpy as np


class Tableau:

	#inicialização das variáveis utilziadas no tableau
	def __init__(self, funçaoObjetivo):
		self.funçaoObjetivo = [-1] + funçaoObjetivo
		self.linhas = [] # linhas da tabela 
		self.constantes = [] # restrições ou variaveis de custo
		self.numVariaveis = len(self.funçaoObjetivo)-1
		self.numVariavesFolga = 0
		self.varBasicas = [] 
		self.varNaoBasicas = [i for i in range(1, self.numVariaveis+1)]
		self.numRestriçoes = -1 
		self.restriçoesIguais = []
		self.indexMaiorRestriçao = []
		self.varMaiorRestriçao = []
		self.bigM = 10000
		self.indexFolga = []
		self.funçaoObjetivo = [i * -1 for i in self.funçaoObjetivo]

		# if(sinal == "Max" or sinal == "max"):
		# 	self.funçaoObjetivo = [i * -1 for i in self.funçaoObjetivo]
		# elif (sinal != "min" or sinal != "Min"):
		# 	print("Erro")


	#representação da string de forma orgazinada e de tabela a f.objetivo, varBasica e linhas
	def __str__(self):

		s = "VB | Z"
		for e in self.funçaoObjetivo[1:]:
			s += (" %8.2f |" % e)
		s += ("\n")
		s += ("_"*len(s))
		s += ("\n")
		k = 0
		for l in self.linhas[0:]:
			s += (" x%d |" % self.varBasicas[k])
			k += 1
			for e in l[1:]: #linha
				s += (" %8.2f |" % e)
			s += ("\n")
		return s
	
		# adiciona as restriçoes para as lista de coeficientes
	def restriçoes(self, listaCoeficientes, folga, sinal):
		self.numRestriçoes += 1
		self.linhas.append([0] + listaCoeficientes)
		self.constantes.append(folga)
		self.numVariavesFolga += 1

		if (sinal == '<='):
			self.funçaoObjetivo.append(0)
			self.varBasicas.append(self.numVariaveis+self.numVariavesFolga)
			self.indexFolga.append((self.numVariaveis+self.numVariavesFolga))
		elif (sinal == '='):
			self.funçaoObjetivo.append(self.bigM)
			self.restriçoesIguais.append(self.numRestriçoes)
			self.varBasicas.append(self.numVariaveis+self.numVariavesFolga)
			self.indexFolga.append((self.numVariaveis+self.numVariavesFolga))
		elif (sinal == '>='):
			self.funçaoObjetivo.append(0)
			self.funçaoObjetivo.append(self.bigM)
			self.varMaiorRestriçao.append((self.numVariaveis + self.numVariavesFolga, self.numVariaveis + self.numVariavesFolga+1)) 
			self.indexFolga.append((self.numVariaveis+self.numVariavesFolga))
			self.numVariavesFolga += 1
			self.varBasicas.append((self.numVariaveis+self.numVariavesFolga))



	# construção da tabela do método do tableau simplex
	def constroiTableau(self):
		identidade = np.identity(self.numRestriçoes+1)
		aux1 = np.concatenate( (np.array(self.linhas, dtype=float), identidade), axis=1)
		aux2 = np.array([self.constantes], dtype=float)
		self.linhas = np.concatenate( (aux1,aux2.T), axis=1 )
		self.funçaoObjetivo.append(0)
		self.funçaoObjetivo = np.array(self.funçaoObjetivo, dtype=float)

		for i in self.varMaiorRestriçao:
			self.linhas = np.insert(self.linhas,i[0], self.linhas[:,i[0]],axis = 1)
			for j in range(len(self.linhas[:,i[0]])):
				if self.linhas[j][i[0]] == 1.0:
					self.linhas[j][i[0]] = -1
					self.indexMaiorRestriçao.append(j)

	# BigM aplicada a função objetivo
		for i in self.restriçoesIguais:
			self.funçaoObjetivo -= self.bigM * self.linhas[i]
		for i in self.indexMaiorRestriçao:
			self.funçaoObjetivo -= self.bigM * self.linhas[i]



	#testar se a solução é ótima
	def ehNaoOtimo(self):
		if min(self.funçaoObjetivo[1:-1]) < 0:
			return 1
		else:
			return 0
		

	#seleciona a coluna pivô 
	def pivoColuna(self):
		menorValor = 0
		menorIndex = 0
		for i in range(1, len(self.funçaoObjetivo)-1):
			if self.funçaoObjetivo[i] < menorValor:
				menorValor = self.funçaoObjetivo[i]
				menorIndex= i

		return menorIndex


	# seleciona o pivô da linha baseado no teste da razão minima
	def pivoLinha(self, colunaIndex):
		coluna = self.linhas[:,colunaIndex]
		values = self.linhas[:,-1]
		ratio = []
		#teste da razão minima
		for i in range(len(values)):
			if coluna[i] <= 0:
				ratio.append(99999 * abs(max(coluna)))
			elif values[i] == 0:
				ratio.append(9999)			
			else:
				ratio.append(values[i]/coluna[i])

		return np.argmin(ratio)


	#operação algebrica de pivotamento nas linhas da tabela
	def OperaçaoMatrix(self, linha, coluna):
		pivo = self.linhas[linha][coluna]
		print('\nPivo: %s' %(pivo))
		self.linhas[linha] /= pivo
		for i in range(len(self.linhas)):
			if i != linha:
				self.linhas[i] -= self.linhas[i][coluna] * self.linhas[linha]

		self.funçaoObjetivo = self.funçaoObjetivo - self.funçaoObjetivo[coluna] * self.linhas[linha]


	# atualização da tabela do simplex enquanto não encontra solução ótima
	def atualizaTabela(self):
		qtde = 1
		while self.ehNaoOtimo():
			print("Qtde de  iteração = " + str(qtde))
			print("\n")
			pColuna = self.pivoColuna()
			pLinha = self.pivoLinha(pColuna)
			self.OperaçaoMatrix(pLinha,pColuna)
			print ('\nPivô coluna: %s\nPivô linha: %s'%(pColuna,pLinha+2))
			
			print ('\nX%s entra \nX%s sai'%(pColuna, self.varBasicas[pLinha]))
			print()
			for i in range(len(self.varNaoBasicas)):
				if self.varNaoBasicas[i] == pColuna:
					self.varNaoBasicas[i], self.varBasicas[pLinha] = self.varBasicas[pLinha], self.varNaoBasicas[i]
			print(self)
			qtde += 1


	#mostrar a solução final
	def soluçao(self):
		
		self.constroiTableau()
		print(f"Tabela Inicial:")
		print(self)
		self.atualizaTabela()
		print(f"Tabela Final:")
		print(self)
		print("Variáveis Básicas:")
		s = ""
		for b in range(len(self.varBasicas)):
			s += ("x" + str(self.varBasicas[b]) + " = " + str(self.linhas[b][-1]) + " ")
		print(s)
		print("\n")
		print(f"Soluçao Ótima = " + str(self.funçaoObjetivo[-1]))
		self.rangeDual()
	

	def rangeDual(self):		
		limite = []
		for col in self.indexFolga:
			var_limite = [float('-inf'), float('inf')]
			for linha in range(len(self.linhas)):
				if (self.linhas[linha][col] != 0):
					novoLimite = -self.linhas[linha][-1] / self.linhas[linha][col]
					if (self.linhas[linha][col] > 0):
						if(novoLimite > var_limite[0]):
							var_limite[0] =  novoLimite
					if (self.linhas[linha][col] < 0):
						if(novoLimite < var_limite[1]):
							var_limite[1] =  novoLimite
			limite.append(var_limite)
		print("\n \n Os Limites da variação são:")
		for i in range(len(limite)):
			
			print ("\t{} <= delta_b{} <= {}, assim ".format(limite[i][0], i+1, limite[i][1]), end="")
			print ("{} <= b{} <= {}".format(self.constantes[i] + limite[i][0], i+1, self.constantes[i] + limite[i][1]))	


	def dualProblema(self,listaSinal,const,funObjetivo,lin):
		print("\n\n Problema Dual:")
		print("\tMin z = ", end="")
		for i in range(len(const)):
			print("{}y{} ".format(const[i], i+1), end="")
		print("\n\t st")
		
		for i in range (self.numVariaveis):
			print("\t", end="")
			for j in range(self.numRestriçoes):
				print("{} Y{} ".format(lin[j][i], j+1), end="")
			print(">=", end=" ")
			print("{}".format(funObjetivo[i]))

		for i in range(self.numRestriçoes):
			if(listaSinal[i] == "="):
				print("\t\tY{}, ".format(i+1))
			if(listaSinal[i] == "<="):
				print("\t\tY{} >= 0".format(i+1, listaSinal[i]))
			if(listaSinal[i] == ">="):
				print("\t\tY{} <= 0".format(i+1, listaSinal[i]))
	
		

if __name__ == '__main__':

	# t = Tableau([3,5])
	# t.restriçoes([1, 0], 4, "<=")
	# t.restriçoes([0, 2], 12, "<=")
	# t.restriçoes([3, 2], 18, "=")
	# t.soluçao()
	# listaSinal = ["<=","<=","="]
	# const = [4,12,18]
	# funObjetivo = [3,5]
	# lin = [
	# 	[1,0],
	# 	[0,2],
	# 	[3,2]
	# ]
	# t.dualProblema(listaSinal,const,funObjetivo,lin)	
	

	# t = Tableau([2,3,2],"Max")
	# t.restriçoes([2, 1, 1], 4, "<=")
	# t.restriçoes([1, 2, 1], 7, "<=")
	# t.restriçoes([0, 0, 1], 5, "<=")
	# t.soluçao()
	# listaSinal = ["<=","<=","<="]
	# const = [4,7,5]
	# funObjetivo = [2,3,2]
	# lin = [
	# 	[2,1,1],
	# 	[1,2,1],
	# 	[0,0,1]
	# ]
	# t.dualProblema(listaSinal,const,funObjetivo,lin)


	t = Tableau([0.4, 0.5])
	t.restriçoes([0.3, 0.1], 2.7, "<=")
	t.restriçoes([0.5, 0.5], 6, "=")
	t.restriçoes([0.6, 0.4], 6, ">=")
	t.soluçao()
	listaSinal = ["<=","=",">="]
	const = [2.7, 6, 6]
	funObjetivo = [0.4, 0.5]
	lin = [
		[0.3,0.1],
		[0.5, 0.5],
		[0.6, 0.4]
	]
	t.dualProblema(listaSinal,const,funObjetivo,lin)

	

	# t = Tableau([1,1, 1],"Max")
	# t.restriçoes([1, 1, 0], 1, "<=")
	# t.restriçoes([0,-1, 1], 0, "<=")
	# t.soluçao()
	# listaSinal = ["<=","<=","<="]
	# const = [1,0]
	# funObjetivo = [1,1,1]
	# lin = [
	# 	[1,1,0],
	# 	[0,-1,1],
	# ]
	# t.dualProblema(listaSinal,const,funObjetivo,lin)

	# t = Tableau([3,4,1],"Max")
	# t.restriçoes([1, 2, 1], 6, "<=")
	# t.restriçoes([2, 0, 2], 4, "<=")
	# t.restriçoes([3, 1, 1], 9, "<=")
	# t.soluçao()
	# listaSinal = ["<=","<=","<="]
	# const = [3,4,1]
	# funObjetivo = [6,4,9]
	# lin = [
	# 	[1,2,1],
	# 	[2,0,2],
	# 	[3,1,1]
	# ]
	# t.dualProblema(listaSinal,const,funObjetivo,lin)


	# t = Tableau([5,5,3],"Max")
	# t.restriçoes([1,3,1],3, "<=")
	# t.restriçoes([-1,0,3],2, "<=")
	# t.restriçoes([2,-1,2],4, "<=")
	# t.restriçoes([2,3,-1],2, "<=")
	# t.soluçao()
	# listaSinal = ["<=","<=","<=","<="]
	# const = [3,2,4,2]
	# funObjetivo = [5,5,3]
	# lin = [
	# 	[1,3,1],
	# 	[-1,0,3],
	# 	[2,-1,2],
	# 	[2, 3,-1]
	# ]
	# t.dualProblema(listaSinal,const,funObjetivo ,lin)


	# t = Tableau([2, 10, 1, 4 ],"Min")
	# t.restriçoes([3, 6, 0, 4], 100, "<=")
	# t.restriçoes([1,0, 0, 10], 50, ">=")
	# t.restriçoes([3, 1, 6 , 0], 30, ">=")
	# t.soluçao()
	# listaSinal = ["<=",">=",">="]
	# const = [100, 50, 30]
	# funObjetivo = [2, 10, 1, 4 ]
	# lin = [
	# 	[3, 6, 0, 4],
	# 	[1,0, 0, 10],
	# 	[3, 1, 6 , 0]
	# ]
	# t.dualProblema(listaSinal,const,funObjetivo,lin)