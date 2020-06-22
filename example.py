from snf import matrix
from snf import snfproblem
from snf import z
from snf import zi

snfMatrix = matrix.Matrix(2, 2, [z.Z(i) for i in range(1,5)])
snfProb = snfproblem.SNFProblem(snfMatrix)
snfProb.computeSNF()

print(f"A:\n{snfProb.A}")
print(f"J:\n{snfProb.J}")
print(f"S:\n{snfProb.S}")
print(f"T:\n{snfProb.T}")

print(f"S*A*T == J ?: {snfProb.S * snfProb.A * snfProb.T == snfProb.J}")
