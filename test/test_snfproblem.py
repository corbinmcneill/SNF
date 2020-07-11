import pytest
import random as rand
from smithnormalform import matrix, snfproblem, z, zi


start_seed = 1000
number_of_seeds = 10

seeds = list(range(start_seed, start_seed + number_of_seeds))
sizes = [(1, 1), (2, 2), (3, 3), (2, 6), (6, 2), (5, 5), (8, 8)]
abslimits = [1, 10, 100, 10000]


@pytest.mark.parametrize("random_seed", seeds)
@pytest.mark.parametrize("size", sizes)
@pytest.mark.parametrize("abslimit", abslimits)
def test_snfproblem_z(random_seed, size, abslimit):
    rand.seed(random_seed)

    h = size[0]
    w = size[1]

    contents = [rand.randint(-abslimit, abslimit) for _ in range(h*w)]
    z_contents = list(map(z.Z, contents))
    m = matrix.Matrix(h, w, z_contents)

    prob = snfproblem.SNFProblem(m)
    prob.computeSNF()

    assert(prob.isValid())


@pytest.mark.parametrize("random_seed", seeds)
@pytest.mark.parametrize("size", sizes)
@pytest.mark.parametrize("abslimit", abslimits)
def test_snfproblem_zi(random_seed, size, abslimit):
    rand.seed(random_seed)

    h = size[0]
    w = size[1]

    contents = [rand.randint(-abslimit, abslimit) for _ in range(h*w*2)]
    zi_contents = [zi.ZI([contents[2*i], contents[2*i+1]]) for i in range(h*w)]

    m = matrix.Matrix(h, w, zi_contents)

    prob = snfproblem.SNFProblem(m)
    prob.computeSNF()

    assert(prob.isValid())
