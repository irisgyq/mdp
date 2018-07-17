import operator
from collections import deque
from copy import deepcopy

stack = []
queue = deque([])
states = []

def readFile(last_board):
    file = open("gridA.2.csv", "r")
    for line in file:
        last_board.append(line.split(','))
    file.close()
    return

def init(last_board):
    for i in range(0, len(last_board)):
        for j in range(0, len(last_board[0])):
            val = last_board[i][j]
            dir = " "
            if val=="1000" or val == "-800" or val=="1000\n" or val == "-800\n":
                dir = "final"
            elif val == "-" or val == "-\n":
                val = "1000000"
                dir = "wall"
            last_board[i][j]={"value": int(val), "dir": dir}
    return

def print_board(last_board):
    m = len(last_board)
    n = len(last_board[0])
    for i in range(0,m):
        for j in range(0,n):
            print("|", end="")
            if last_board[i][j]["dir"]=="wall":
                print("%8s" % " ", end="")
            else:
                print("%8.2f" % last_board[i][j]["value"], end="")
            print(" ", end="")
            print("%5s" % last_board[i][j]["dir"], end="")
        print("|")
    return

def formula(t, v, row, col, last_board):
    discount = 0.9
    reward = -0.01
    if row<0 or row>=len(last_board) or col<0 or col>=len(last_board[0]) or last_board[row][col]["dir"]=="wall":
        new_v = t * (reward + v * discount)
    else:
        new_v = t * (reward + last_board[row][col]["value"] * discount)
    return new_v

def calculateAllDir(row, col, last_board, tmp_board, condition):
    if condition == "front":
        board = last_board
    elif condition == "back":
        board = tmp_board
    t_north = 0.6
    t_south = 0.15
    t_east = 0.15
    t_west = 0.1
    v = board[row][col]["value"]
    v_north = formula(t_north, v, row - 1, col, board) + formula(t_south, v, row + 1, col, board) + \
              formula(t_east, v, row, col + 1, board) + formula(t_west, v, row, col - 1, board)
    v_south = formula(t_north, v, row + 1, col, board) + formula(t_south, v, row - 1, col, board) + \
              formula(t_east, v, row, col - 1, board) + formula(t_west, v, row, col + 1, board)
    v_east = formula(t_north, v, row, col + 1, board) + formula(t_south, v, row, col - 1, board) + \
             formula(t_east, v, row + 1, col, board) + formula(t_west, v, row - 1, col, board)
    v_west = formula(t_north, v, row, col - 1, board) + formula(t_south, v, row, col + 1, board) + \
             formula(t_east, v, row - 1, col, board) + formula(t_west, v, row + 1, col, board)
    v_max= max(v_north, v_south, v_east, v_west)
    last_board[row][col]["value"]=v_max
    if v_max == v_north:
        last_board[row][col]["dir"]="north"
    elif v_max == v_south:
        last_board[row][col]["dir"]="south"
    elif v_max == v_east:
        last_board[row][col]["dir"]="east"
    elif v_max == v_west:
        last_board[row][col]["dir"]="west"
    return

def enque(row, col, last_board):
    if row-1>=0 and last_board[row-1][col]["dir"]==" ":
        queue.append([last_board[row-1][col], row-1, col])
    if row+1<len(last_board) and last_board[row+1][col]["dir"]==" ":
        queue.append([last_board[row+1][col],row+1, col])
    if col-1>=0 and last_board[row][col-1]["dir"]==" ":
        queue.append([last_board[row][col-1],row,col-1])
    if col+1<len(last_board[0]) and last_board[row][col+1]["dir"]==" ":
        queue.append([last_board[row][col+1],row,col+1])
    return

def main():
    last_board = []
    readFile(last_board)
    flag=False
    init(last_board)

    print("Give the position of start point, x is from 0 - " + str(len(last_board)-1)+" , and y is from 0 - "+str(len(last_board[0])-1)+" :")
    start_x = input("x: ")
    start_y = input("y: ")

    count = 1

    print("The initial board is:")
    print_board(last_board)

    for i in range(0, len(last_board)):
        for j in range(0, len(last_board[0])):
            if last_board[i][j]["value"]==1000 and last_board[i][j]["dir"]=="final":
                row = i
                col = j
                enque(row, col, last_board)

    while flag == False:
        pre_board = deepcopy(last_board)
        tmp_board = deepcopy(last_board)
        length = len(queue)
        tmp_queue = deque([])
        for i in range(0,length):
            grid1 = queue.popleft()
            tmp_row1 = grid1[1]
            tmp_col1 = grid1[2]
            if [tmp_row1,tmp_col1] not in states:
                calculateAllDir(tmp_row1, tmp_col1, last_board, tmp_board, "front")
                enque(tmp_row1, tmp_col1, last_board)
                tmp_queue.append(grid1)
                states.append([tmp_row1, tmp_col1])

        while stack!=[]:
            grid2 = stack.pop()
            tmp_row2 = grid2[1]
            tmp_col2 = grid2[2]
            calculateAllDir(tmp_row2, tmp_col2,last_board, tmp_board, "back")
            tmp_queue.append(grid2)

        while tmp_queue!=deque([]):
            stack.append(tmp_queue.popleft())

        count = count+1
        flag = operator.eq(pre_board, last_board)

    print()
    print("After "+str(count)+" iterations...")
    print()
    print("The final board is:")
    print_board(last_board)

    res = []
    rowrow = int(start_x)
    colcol = int(start_y)
    while (last_board[rowrow][colcol]["value"]==1000 and last_board[rowrow][colcol]["dir"]=="final")==False:
        dir = last_board[rowrow][colcol]["dir"]
        res.append(dir)
        if dir=="north":
            rowrow = rowrow - 1
        elif dir=="south":
            rowrow = rowrow + 1
        elif dir=="east":
            colcol = colcol + 1
        elif dir=="west":
            colcol = colcol - 1

    print()
    print("The optimal route to final state is: ")
    for l in range(0, len(res)):
        print(res[l]+", ", end="")
    print("and final!")

main()
