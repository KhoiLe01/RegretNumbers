"""
KKT_general.py
Khoi Le, Derek Sun, Ashwin Lall
"""
import os
import platform

"""
Generates Python file for Gurobi model
Inputs:
k - size of output subset
d - number of attributes
"""
def kkt(k ,d):
    # open or create Gurobi model file if it doesn't exist
    f = open("KKT_conditions.py", "r+", encoding="utf-8")
    f.truncate(0)

    # initiate Gurobi model
    f.write("import gurobipy as gp\nfrom gurobipy import GRB\n\n")
    f.write("m = gp.Model(\"qp\")\n\n")
    f.write("x = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name=\"x\")\n\n")

    # initiate Gurobi model variables
    for i in range (1, k+2):
        f.write("l"+str(i)+" = m.addVar(lb= -1, ub= 1, vtype=GRB.CONTINUOUS, name=\"l"+str(i)+"\")\n")
        f.write("\n")
        for j in range (1, k+2):
            if i != j:
                f.write("m"+str(i)+str(j)+" = m.addVar(lb= 0, ub= 10, vtype=GRB.CONTINUOUS, name=\"m"+str(i)+str(j)+"\")\n")
    f.write("\n")

    for i in range (1,k+2):
        for j in range (1,d+1):
            f.write("p"+str(i)+str(j)+" = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name=\"p"+str(i)+str(j)+"\")\n")
            f.write("v" + str(i) + str(j) + " = m.addVar(lb= 0, ub= 1, vtype=GRB.CONTINUOUS, name=\"v" + str(i) + str(
                j) + "\")\n")
        f.write("\n")

    for i in range (1, k+2):
        for j in range (1, k+2):
            if i != j:
                f.write("a"+str(i)+str(j)+" = m.addVar(lb= 0, ub= 10, vtype=GRB.CONTINUOUS, name=\"a"+str(i)+str(j)+"\")\n")

    # maximize x variable
    f.write("\nm.setObjective(x, GRB.MAXIMIZE)\n")
    f.write("\n")
    count = 0

    for i in range (1, k+1):
        f.write("m.addConstr(p"+str(i)+"1<=p"+str(i+1)+"1, \""+str(count)+"\")\n")
        count += 1
    f.write("\n")

    for i in range (1, k+2):
        for j in range (1, k+2):
            if i != j:
                f.write("m.addConstr(1")
                for q in range (1, d+1):
                    f.write("-p"+str(j)+str(q)+"*v"+str(i)+str(q))
                f.write(">=x, \""+str(count)+"\")\n")
                count += 1
                f.write("m.addConstr(a"+str(i)+str(j)+" == 1")
                for q in range (1, d+1):
                    f.write("-p"+str(j)+str(q)+"*v"+str(i)+str(q))
                f.write("-x, \""+str(count)+"\")\n")
                count += 1

    f.write("\n")

    f.write("m.addConstr(m12")
    for i in range (1, k+2):
        for j in range (1, k+2):
            if not (i == j or (i == 1 and j == 2)):
                f.write("+m"+str(i)+str(j))
    f.write(" == 1, \""+str(count)+ "\")\n")
    count += 1

    f.write("\n")

    for i in range (1, k+2):
        for j in range (1, d+1):
            f.write("m.addConstr(l"+str(i)+"*v"+str(i)+str(j)+" == ")
            new_count = 1
            for q in range (1, k+2):
                if q != i and new_count == 1:
                    f.write("m"+str(q)+str(i)+"*v"+str(q)+str(j))
                    new_count = q
                    break
            for q in range (1, k+2):
                if q != i and q != new_count:
                    f.write("+m"+str(q)+str(i)+"*v"+str(q)+str(j))
            f.write(", \""+str(count)+"\")\n")
            count += 1

            f.write("m.addConstr(l" + str(i) + "*p" + str(i) + str(j) + " == ")
            new_count = 1
            for q in range(1, k + 2):
                if q != i and new_count == 1:
                    f.write("m" + str(q) + str(i) + "*p" + str(q) + str(j))
                    new_count = q
                    break
            for q in range(1, k + 2):
                if q != i and q != new_count:
                    f.write("+m" + str(q) + str(i) + "*p" + str(q) + str(j))
            f.write(", \"" + str(count) + "\")\n")
            count += 1

    f.write("\n")

    for i in range (1, k+2):
        f.write("m.addConstr(p"+str(i)+"1*v"+str(i)+"1")
        for j in range (2, d+1):
            f.write("+p"+str(i)+str(j)+"*v"+str(i)+str(j))
        f.write(" == 1, \""+str(count)+"\")\n")
        count += 1

    f.write("\n")

    for i in range (1, k+2):
        for j in range (1, k+2):
            if i != j:
                f.write("m.addConstr(m"+str(i)+str(j)+"*a"+str(i)+str(j)+" == 0, \""+str(count)+"\")\n")
                count += 1
    f.write("\n")

    # set Gurobi model to NonConvex mode and allow multiple optimal solutions
    f.write("m.Params.NonConvex = 2\nm.Params.PoolSearchMode = 2\nm.Params.PoolSolutions = 5\n")
    f.write("\n")

    f.write("m.optimize()\n\n")

    # print out solutions
    f.write("print(\"All Solutions:\")\n")
    f.write("for i in range (0, m.SolCount):\n")
    f.write("\tprint(\"\\nSolution \"+ str(i+1))\n")
    f.write("\tm.Params.SolutionNumber = i\n")
    f.write("\tprint(m.PoolObjVal)\n")
    f.write("\tfor v in m.getVars():\n")
    f.write("\t\tif v.varName[0] == \"l\" or v.varName[0] == \"m\":")
    f.write("\t\t\tprint('%s %g' % (v.varName, v.xn))\n\n")

    f.write("")

    f.close()

    os.system("gurobi.bat KKT_conditions.py")

def main():
    # prompt user for value of d variable
    d = input("What is the value of d?\n")
    # while value is invalid, prompt user again
    while d.isdigit() == False:
        print('Please input a positive integer.\n')
        d = input("What is the value of d?\n")

    # prompt user for value of k variable
    k = input("What is the value of k?\n")
    while k.isdigit() == False or int(k) < int(d):
        print('Please input a positive integer that is >= d.\n')
        k = input("What is the value of k?\n")

    # generate Gurobi model
    kkt(int(k), int(d))
    # if user is using Windows use gurobi.bat
    if platform.system() == "Windows":
        os.system("gurobi.bat KKT_conditions.py")
    # if user is using Linux use gurobi.sh
    elif platform.system() == "Linux":
        os.system("gurobi.sh KKT_conditions.py")

main()
