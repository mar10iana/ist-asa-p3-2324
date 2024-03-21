from pulp import LpProblem, LpMaximize, LpVariable, lpSum, PULP_CBC_CMD
import sys

def maximizar_lucro(n, p, max_prod, brinquedos, pacotes):

    prob = LpProblem("Maximizacao_do_Lucro", LpMaximize)

    quant_brinquedos = LpVariable.dicts("Brinquedo", range(1, n + 1), lowBound=0, cat='Integer')
    quant_pacotes = LpVariable.dicts("Pacote", range(1, p + 1), lowBound=0, cat='Integer')

    lucro_total = lpSum([brinquedos[i-1][0] * quant_brinquedos[i] for i in range(1, n + 1)]) + \
                  lpSum([pacotes[i-1][3] * quant_pacotes[i] for i in range(1, p + 1)])
    prob += lucro_total

    brinquedo_em_pacotes = {i: 0 for i in range(1, n + 1)}
    for pacote in pacotes:
        for brinquedo in pacote[:3]:
            brinquedo_em_pacotes[brinquedo] += quant_pacotes[pacotes.index(pacote) + 1]

    for i in range(1, n + 1):
        prob += quant_brinquedos[i] + brinquedo_em_pacotes[i] <= brinquedos[i-1][1], f"Max_Brinquedo_{i}"

    prob += lpSum([quant_brinquedos[i] for i in range(1, n + 1)]) + \
            lpSum([3 * quant_pacotes[i] for i in range(1, p + 1)]) <= max_prod, "Max_Total_Prod"

    prob.solve(PULP_CBC_CMD(msg=False))

    return prob.objective.value()


if __name__ == "__main__":
    
    if len(sys.argv) > 1:
        sys.stdin = open(sys.argv[1], 'r')

    t, p, max_prod = map(int, input().split())
    brinquedos = [tuple(map(int, input().split())) for _ in range(t)]
    pacotes = [tuple(map(int, input().split())) for _ in range(p)]

    lucro_maximo = maximizar_lucro(t, p, max_prod, brinquedos, pacotes)
    print(int(lucro_maximo))
