from smithnormalform import matrix, snfproblem, z
import random as rand


rand.seed(1001)

snfContents = [rand.randrange(-10000, 10000) for _ in range(100)]
snfMatrix = matrix.Matrix(10, 10, [z.Z(x) for x in snfContents])
snfProb = snfproblem.SNFProblem(snfMatrix)
snfProb.computeSNF()

print(f"A:\n{snfProb.A}")
print()
print(f"J:\n{snfProb.J}")
print()
print(f"S:\n{snfProb.S}")
print()
print(f"T:\n{snfProb.T}")
print()

print(f"S.det: {snfProb.S.determinant()}")
print()
print(f"T.det: {snfProb.T.determinant()}")
print()

print(f"S*A*T == J ?: {snfProb.S * snfProb.A * snfProb.T == snfProb.J}")
