import heapq
def dijkstra(g, src):
    dist = {n: float("inf") for n in g}; prev = {}
    dist[src] = 0; pq = [(0, src)]; order = []
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]: continue
        order.append((u, d))
        for v, w in g[u].items():
            if d + w < dist[v]:
                dist[v] = d + w; prev[v] = u; heapq.heappush(pq, (dist[v], v))
    return dist, prev, order
links = [("R1","R2",10),("R1","R3",100),("R2","R3",10),("R2","R4",100),
         ("R3","R5",10),("R4","R5",10),("R4","R6",100),("R5","R6",10)]
def build(f):
    g = {f"R{i}": {} for i in range(1,7)}
    for a,b,w in links: g[a][b]=g[b][a]=f(w)
    return g
for label,f in (("new ref (100 Gbps)",lambda w:w),("default ref",lambda w:1 if w<=100 else 10)):
    pass
g = build(lambda w: w)
dist, prev, order = dijkstra(g, "R1")
print(order); print(dist)
for n in dist:
    p=[n]
    while p[-1]!="R1": p.append(prev[p[-1]])
    print(n, dist[n], "->".join(reversed(p)))
# default-reference costs: 10G and 1G both 1
g2 = build(lambda w: 1)
d2,p2,_ = dijkstra(g2,"R1"); print(d2)
