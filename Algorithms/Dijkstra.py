#------------------------------------------------------------------------------
# Name : Dijkstra
# Author: paroxyste
#------------------------------------------------------------------------------

def initial_graph() :

    return {
        'A' : {'B' :  1, 'C' :  4, 'D' : 2},
        'B' : {'A' :  9, 'E' :  5},
        'C' : {'A' :  4, 'F' : 15},
        'D' : {'A' : 10, 'F' :  7},
        'E' : {'B' :  3, 'J' :  7},
        'F' : {'C' : 11, 'D' : 14, 'K' : 3, 'G' : 9},
        'G' : {'F' : 12, 'I' :  4},
        'H' : {'J' : 13},
        'I' : {'G' :  6, 'J' :  7},
        'J' : {'H' :  2, 'I' :  4},
        'K' : {'F' :  6}
    }


start = 'A'
step = '<-'

path = {}
adj_node = {}

queue = []

graph = initial_graph()

for node in graph:
    path[node] = float('inf')
    adj_node[node] = None
    queue.append(node)

path[start] = 0

while queue:
    key_min = queue[0]
    min_val = path[key_min]

    for n in range(1, len(queue)) :
        if path[queue[n]] < min_val :
            key_min = queue[n]
            min_val = path[key_min]

    cur = key_min
    queue.remove(cur)


    for i in graph[cur]:
        alternate = graph[cur][i] + path[cur]

        if path[i] > alternate :
            path[i] = alternate
            adj_node[i] = cur

finish = 'I'

print('Start :', start, ' >>> ', 'Finish :', finish)
print('--------------------------')

while 1:
    finish = adj_node[finish]

    if finish is None:
        break

    print('\nNodes :', finish)
