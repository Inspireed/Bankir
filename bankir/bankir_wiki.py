import copy
import networkx as nx

def main():
    processes = 4
    resources = 4
    max_resources = [1, 1, 1, 1]
    label = 'Безопасная последовательность:'
    sequence = ""

    print("\n-- maximum resources for each process --")
    max_need = [[int(i) for i in input(f"process {j + 1} : ").split()] for j in range(processes)]

    print("\n-- allocated resources for each process --")
    currently_allocated = [[int(i) for i in input(f"process {j + 1} : ").split()] for j in range(processes)]


    print("\n-- request resources for each process --")
    currently_request = [[int(i) for i in input(f"process {j + 1} : ").split()] for j in range(processes)]

    allocated = [0] * resources
    for i in range(processes):
        for j in range(resources):
            allocated[j] += currently_allocated[i][j]
    available = [max_resources[i] - allocated[i] for i in range(resources)]

    bankir(processes, resources, max_resources, max_need, currently_allocated, currently_request, available, allocated, sequence, label)


def bankir(processes, resources, max_resources, max_need, currently_allocated, currently_request, available, allocated, sequence, label):
    rest = 1
    draw_req = []
    draw_all = []
    draw_req.append(copy.deepcopy(currently_request))
    draw_all.append(copy.deepcopy(currently_allocated))
    if_not_safe1 = copy.deepcopy(currently_request)
    if_not_safe2 = copy.deepcopy(currently_allocated)

    null_lst = []
    running = [True] * processes
    safe = False
    count = processes
    while count != 0:
        for i in range(processes):
            if running[i]:
                executing = True
                for j in range(resources):
                    if currently_request[i][j] - currently_allocated[i][j] > available[j]:
                        executing = False
                        break
                if executing: # выделение ресурсов и запуск проверки
                    available1 = copy.copy(available)
                    currently_allocated1 = copy.copy(currently_allocated)
                    currently_request1 = copy.copy(currently_request)
                    for j in range(resources):
                        available[j] += currently_allocated[i][j]
                    for j in range(resources):
                        currently_allocated[i][j] = 0
                    for j in range(resources):
                        currently_request[i][j] = 0
                    draw_req.append(copy.deepcopy(currently_request))
                    draw_all.append(copy.deepcopy(currently_allocated))
                    # проверка на безопасность
                    work = copy.copy(available)
                    finish = [0]*processes
                    is_end = True
                    while is_end:
                        for j in range(resources):
                            if currently_request[finish.index(0)][j] > work[j] and finish.count(0) == 1:
                                is_end = False
                                break
                        is_ok = True
                        for k in range(processes):
                            for j in range(resources):
                                if currently_request[k][j] > work[j]:
                                    is_ok = False
                                    break
                            if is_ok:
                                finish[k] = 1
                                for j in range(resources):
                                    work[j] += currently_allocated[k][j]
                        is_end = False

                    if 0 in finish:
                        #count = 0
                        currently_request = currently_request1
                        currently_allocated = currently_allocated1
                        available = available1
                        print(f"Запрос процесса {i + 1} не выполнен, система не в безопасном состоянии\n")
                    else:
                        rest += 1
                        null_lst.append(i)
                        count -= 1
                        print(f"Процесс {i + 1} выполнен")
                        print("выделено ресурсов:")
                        [print(*currently_allocated[i]) for i in range(4)]
                        print("запрос на ресурсы:")
                        [print(*currently_request[i]) for i in range(4)]

                        if count:
                            sequence += f"{i + 1} -> "
                        else:
                            sequence += f"{i + 1}"
                        running[i] = False
                        safe = True
                        break
        if not safe:
            label = "Система в небезопасном состоянии\n"
            print(label)
            print(draw_all)
            print(draw_req)
            draw_req = [if_not_safe1]
            draw_all = [if_not_safe2]
            print(len(draw_all))
            rest = 1
            # transponir
            trans_matrix = list(zip(*draw_all[0]))
            draw_all[0] = [list(row) for row in trans_matrix]

            adj_matrix = {
                'R1': [],
                'R2': [],
                'R3': [],
                'R4': [],
                'P1': [],
                'P2': [],
                'P3': [],
                'P4': []
            }
            for i in range(4):
                for j in range(4):
                    if draw_all[0][i][j] == 1:
                        adj_matrix[f'R{i + 1}'].append(f'P{j + 1}')
                    if draw_req[0][i][j] == 1:
                        adj_matrix[f'P{i + 1}'].append(f'R{j + 1}')

            # удаляем ключи
            to_remove = [key for key, value in adj_matrix.items() if value == []]
            for key in to_remove:
                del adj_matrix[key]
            # print(adj_matrix)

            graph = nx.DiGraph(adj_matrix)

            cycles = nx.simple_cycles(graph)
            cyc = []

            # ['P2', 'R1', 'P1', 'R3']
            for cycle in cycles:
                cyc += cycle

            # [['P2', 'R1'], ['R1', 'P1'], ['P1', 'R3'], ['R3', 'P2']]
            cyc.append(cyc[0])
            cycle_res = [[cyc[i], cyc[i + 1]] for i in range(len(cyc) - 1)]
            # print(cycle_res)

            for cycl in range(len(cycle_res)):
                for i in range(4):
                    if f'R{i + 1}' in cycle_res[cycl][0]:
                        for j in range(4):
                            if f'P{j + 1}' in cycle_res[cycl][1]:
                                draw_all[0][i][j] = -1
                    if f'P{i + 1}' in cycle_res[cycl][0]:
                        for k in range(4):
                            if f'R{k + 1}' in cycle_res[cycl][1]:
                                draw_req[0][i][k] = -1
            return null_lst, label, sequence, draw_req, draw_all, rest

    if safe:

        #print(draw_req)
        #print(draw_all)
        rest = 5

        # transponir
        trans_matrix = list(zip(*draw_all))
        draw_all = [list(row) for row in trans_matrix]

        adj_matrix = {
            'R1': [],
            'R2': [],
            'R3': [],
            'R4': [],
            'P1': [],
            'P2': [],
            'P3': [],
            'P4': []
        }
        for i in range(4):
            for j in range(4):
                if draw_all[i][j] == 1:
                    adj_matrix[f'R{i + 1}'].append(f'P{j + 1}')
                if draw_req[i][j] == 1:
                    adj_matrix[f'P{i + 1}'].append(f'R{j + 1}')

        # удаляем ключи
        to_remove = [key for key, value in adj_matrix.items() if value == []]
        for key in to_remove:
            del adj_matrix[key]
        # print(adj_matrix)

        graph = nx.DiGraph(adj_matrix)

        cycles = nx.simple_cycles(graph)
        cyc = []

        # ['P2', 'R1', 'P1', 'R3']
        for cycle in cycles:
            cyc += cycle

        # [['P2', 'R1'], ['R1', 'P1'], ['P1', 'R3'], ['R3', 'P2']]
        cyc.append(cyc[0])
        cycle_res = [[cyc[i], cyc[i + 1]] for i in range(len(cyc) - 1)]
        #print(cycle_res)

        for cycl in range(len(cycle_res)):
            for i in range(4):
                if f'R{i + 1}' in cycle_res[cycl][0]:
                    for j in range(4):
                        if f'P{j + 1}' in cycle_res[cycl][1]:
                            draw_all[i][j] = -1
                if f'P{i + 1}' in cycle_res[cycl][0]:
                    for k in range(4):
                        if f'R{k + 1}' in cycle_res[cycl][1]:
                            draw_req[i][k] = -1
        print(draw_all)
        print(draw_req)
        return null_lst, label, sequence, draw_req, draw_all, rest


if __name__ == "__main__":
    main()
