from ortools.algorithms import pywrapknapsack_solver
import os
import time
def main():
    # Create the solver.
    solver = pywrapknapsack_solver.KnapsackSolver(
        pywrapknapsack_solver.KnapsackSolver.
        KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample') # declares a specialized solver for knapsack problems
    path = "C:\\Users\\VQ\\VScode\\Knapsack\\kplib-master\\"
    for file in os.listdir(path):
        time_start1 =time.time()
        for file1 in os.listdir(path+file):
            for file2 in os.listdir(path+file+"\\"+file1):
                #creates the data for the problem
                values = [] # A vector containing the values of the items
                weights = [] # A vector containing the weights of the items
                capacities = [] # A vector with just one entry, the capacity of the knapsack
                optimal_solution = False
                time_start2 =time.time()
                # get input
                with open(path+file+"\\"+file1 +"\\"+ file2 +"\\"+"s000.kp",'r') as rf:
                    line = rf.readline()
                    num = rf.readline()
                    capacities = [int(rf.readline())]
                    line = rf.readline()
                    line = rf.readline()
                    while line:
                        v=line.split(" ")
                        values.append(int(v[0]))
                        weights.append(int(v[1]))
                        line = rf.readline()
                weights=[weights]

                solver.set_time_limit(180) # set runtime limit
                solver.Init(values, weights, capacities)
                computed_value = solver.Solve()
                time_end2 =time.time()
                packed_items = []
                packed_weights = []
                total_weight = 0
                # print('Total value =', computed_value)
                for i in range(len(values)):
                    if solver.BestSolutionContains(i):
                        packed_items.append(i)
                        packed_weights.append(weights[0][i])
                        total_weight += weights[0][i]
                # print('Total weight:', total_weight)
                # print('Packed items:', packed_items)
                # print('Packed_weights:', packed_weights)
                Runtime =time_end2-time_start2
                # check the optimal solution
                if Runtime <= 180:
                    optimal_solution = True 
                output=['Num of items: '+ num,
                        'Runtime:{:.5f}'.format(Runtime),
                        'Capacities: '+str(capacities[0]),
                        'Total_value: '+ str(computed_value),
                        'Total_weight: '+ str(total_weight),
                        'Is_optimal: '+ str(optimal_solution),
                        'Packed_items: '+ str(packed_items),
                        'Packed_weights: '+ str(packed_weights)]
                wf = open("C:\\Users\\VQ\\VScode\\Knapsack\\result\\"+file+"\\"+file1+"\\"+ file2+"\\"+"result00.txt", 'w')
                wf.write("\n".join(output))
                wf.close
        time_end1 =time.time()
        print("Runtime of {}: {:.3f} ".format(file,time_end1-time_start1))        
if __name__ == '__main__':
    main()