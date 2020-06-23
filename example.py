from snf import matrix
from snf import snfproblem
from snf import z
import random as rand


rand.seed(1002)

snfContents = [rand.randrange(-10, 10) for _ in range(4)]
snfMatrix = matrix.Matrix(2, 2, [z.Z(x) for x in snfContents])
snfProb = snfproblem.SNFProblem(snfMatrix, debug=True)
snfProb.computeSNF()

print(f"A:\n{snfProb.A}")
print(f"J:\n{snfProb.J}")
print(f"S:\n{snfProb.S}")
print(f"T:\n{snfProb.T}")

print(f"S.det: {snfProb.S.determinant()}")
print(f"T.det: {snfProb.T.determinant()}")

print(f"S*A*T == J ?: {snfProb.S * snfProb.A * snfProb.T == snfProb.J}")
