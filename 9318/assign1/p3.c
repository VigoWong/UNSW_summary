Data: D is a dataset of n d-dimensional points; k is the number of clusters. 
Initialize k centers C = [c_1, c_2, ..., c_k]; 
canStop <- false; 
while canStop = false do
    Initialize k empty clusters G = [g_1, g_2, ..., g_k]; 
    for each data point p ∈ D do:
        c_x <- NearestCenter(p, C); 
        g_cx.append(p); 
    for each group g ∈ G do:
        c_i <- ComputeCenter(g);

return G;