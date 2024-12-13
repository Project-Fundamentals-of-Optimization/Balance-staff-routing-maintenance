import copy
# n,k = [int(_) for _ in input().split()]

# work_time = [0]+[int(_) for _ in input().split()]
# distance = [[int(_) for _ in input().split()] for _ in range(n+1)]

with open("input0.txt", "r") as file:
    n, k = map(int, file.readline().split())
    work_time = [0] + list(map(int, file.readline().split()))
    distance = [list(map(int, file.readline().split())) for _ in range(n+1)]

# print(n, k)
# print(work_time)
# print(distance)


# print(work_time)
# print(distance)

l,r = 0, int(1e5)
bit_mask = [0 for _ in range(n+1)]
max_branch = 2
max_num_state = 10
full_limit = None
origin = None
def wraper(max_time, bit_mask):
    stack_of_paths = []
    cur_path = []
    stop_bruteforce = 0
    def find_a_route(u,max_time = max_time):
        nonlocal stop_bruteforce
        if stop_bruteforce:return
        #check phần của các worker khác bằng số việc còn lại >= số worker còn lại
        """
        find a route 
        calculate cost of 0-> ... ->0
        """
        # print(f"full lm {full_limit} - {n-sum(bit_mask)} - {bit_mask}")
        going_to_go_to_zero = True
        if n-sum(bit_mask)>full_limit:
            for i in range(1,n+1):
                if bit_mask[i]==0 and max_time+distance[u][0]-distance[u][i]-work_time[i]-distance[i][0]>=0:
                    bit_mask[i]=1
                    cur_path.append(i)
                    # print(f"from {u} to {i} cost {distance[u][i]-work_time[i]-distance[i][0]}")
                    find_a_route(i, max_time+distance[u][0]-distance[u][i]-work_time[i]-distance[i][0])
                    cur_path.pop()
                    bit_mask[i]=0
                    going_to_go_to_zero = False
        if going_to_go_to_zero: 
            if len(cur_path)>0:
                stack_of_paths.append([bit_mask[:],cur_path[:]])
                # print(f"cheecccckkkk {cur_path} - {max_time} - max {origin}")
            if len(stack_of_paths)>max_num_state: stop_bruteforce = 1
    for start_point in range(1,n+1):
        if bit_mask[start_point]==0 and distance[0][start_point]+work_time[start_point]+distance[start_point][0]<max_time:
            bit_mask[start_point] = 1
            cur_path = [start_point]
            find_a_route(start_point,max_time-(distance[0][start_point]+work_time[start_point]+distance[start_point][0]))
            bit_mask[start_point] = 0
    return stack_of_paths

max_great_num_state = 1000
def check(max_length):
    worker = [[] for i in range(k+1)]
    worker[-1] = [[bit_mask[:],]]
    """
    worker[i] is list of [bit_mask,[worker[0] path],[worker[1] path],.... worker[i]path]
    """
    global full_limit, origin
    origin = max_length
    for id in range(k):
        full_limit = k-id-1
        cnt = 0
        for senario in worker[id-1]:
            cur_bit_mask = senario[0]
            potential_moves = wraper(max_length,cur_bit_mask)
            if len(potential_moves) ==0:
                # print(senario,id-1)
                return None
            # print(f"potential move:{potential_moves} at id {id} in max_length {max_length}")
            for move in potential_moves:
                tmp = copy.deepcopy(senario)
                tmp[0] = move[0]
                tmp.append(move[1])
                worker[id].append(tmp)
    # if max_length != 505:
    # print(worker[k-1])
    worker[k-1] = [state for state in worker[k-1] if set(state[0][1:]) == set([1])]
    
    if len(worker[k-1])==0:return None

    # lst = worker[k-1][0][0][1:]
    # # print(lst)
    # lst = set(lst)
    # # print(lst)
    # if lst != set([1]):return None
    # print(f"at length {max_length}: {worker[k-1]}")
    return worker[k-1][0]

from time import perf_counter
while r-l>1:
    tin=perf_counter()
    m = (l+r)//2
    new_state = check(m)
    if new_state: 
        r = m
        last_state = new_state
    else: l = m
    print(f"{l},{m},{r}: {perf_counter()-tin:.2f}s")

for i in range(1,k+1):
    u = [0] + last_state[i]+[0]
    print(len(u))
    print(*u) 