import copy as c
import decimal as d

class Matrice:
	def __init__(self, n, m = -1):
		if m == -1:
			m = n
		self.carre = n == m
		self.n = n
		self.m = m
		self.value = [[d.Decimal(0) for _ in range(n)] for _ in range(m)]

	def __str__(self):
		res = ""
		for i in self.value:
			res += "|"
			for j in i:
				res += "{:<10}".format(j.quantize(d.Decimal("0.01")))
			res += "|\n"
		return res

	def __getitem__(self, pos):
		return self.value[pos[0] - 1][pos[1] - 1]

	def __setitem__(self, pos, value):
		self.value[pos[0] - 1][pos[1] - 1] = d.Decimal(value)

	def __mul__(self, facteur):
		res = c.copy(self)
		for i in range(1, self.n + 1):
			for j in range(1, self.m + 1):
				res[i, j] *= d.Decimal(facteur)
		return res

	def __rmul__(self, facteur):
		return self.__mul__(facteur)

	def getTransposee(self):
		if self.carre:
			res = Matrice(self.n)
			for i in range(self.n):
				for j in range(self.m):
					res[j, i] = self[i, j]
		else:
			pass
		return res

	def getSousMatrice(self, pos):
		res = Matrice(self.n - 1, self.m - 1)
		p = 1
		q = 1
		for i in range(1, self.n + 1):
			if i != pos[0]:
				for j in range(1, self.m + 1):
					if j != pos[1]:
						res[q, p] = self[i, j]
						p += 1
				p = 1
				q += 1
		return res

	def getDet(self):
		if self.carre:
			if self.n == 1:
				return self[1, 1]
			elif self.n == 2:
				return self[1, 1] * self[2, 2] - self[1, 2] * self[2, 1]
			else:
				res = d.Decimal(0)
				for j in range(1, self.m + 1):
					sousMatriceij = self.getSousMatrice((1, j))
					res += d.Decimal(self[1, j] * ((-1) ** (1 + j)) * sousMatriceij.getDet())
				return res

	def getCofacteur(self, pos):
		return (-1) ** (pos[0] + pos[1]) * self.getSousMatrice(pos).getDet()

	def getComatrice(self):
		if self.carre:
			res = Matrice(self.n)
			for i in range(1, self.m + 1):
				for j in range(1, self.m + 1):
					res[i, j] = self.getCofacteur((i, j))
			return res

	def getInverse(self):
		return (1 / self.getDet()) * self.getComatrice().getTransposee()

	def getTrace(self):
		if self.carre:
			res = d.Decimal(0)
			for i in range(1, self.n + 1):
				res += self[i, i]
			return res

	def somme(self, matrice):
		if self.n == matrice.n and self.m == matrice.n:
			res = Matrice(self.n, self.m)
			for i in range(1, self.n + 1):
				for j in range(1, self.m):
					res[i, j] = self[i, j] + matrice[i, j]
			return res

	def produit(self, matrice):
		if self.carre:
			if matrice == self.getInverse():
				return __class__.matriceUnite(self.n)
		if self.m == matrice.n:
			res = Matrice(self.n, matrice.m)
			for i in range(1, self.n + 1):
				for j in range(1, self.n + 1):
					somme = 0
					for k in range(1, matrice.m + 1):
						somme += round(self[i, k] * matrice[k, j], 4)
					res[i, j] = somme
		return res

	def matriceUnite(n):
		res = Matrice(n)
		for i in range(1, n + 1):
			res[i, i] = 1
		return res


if __name__ == "__main__":
	matriceTest = Matrice(3)
	matriceTest[1, 1] = 1
	matriceTest[1, 2] = 6
	matriceTest[1, 3] = 0
	matriceTest[2, 1] = 0
	matriceTest[2, 2] = 4
	matriceTest[2, 3] = -2
	matriceTest[3, 1] = 3
	matriceTest[3, 2] = 2
	matriceTest[3, 3] = 5
	print(matriceTest)
	print(matriceTest.getDet())
	print(matriceTest.getComatrice())
	print(matriceTest.getInverse().getInverse())
	print(matriceTest.getInverse().produit(matriceTest))
