def readChessTable():
    filename = "chessboard.txt"
    w0 = None
    with open(filename) as f:
        ls = f.readlines()
        w0 = list(map(lambda l: list(map(int, l.split())), ls))
    return w0

def getChessTables(w0):
    w1 = [[w0[j][i] for j in range(15)] for i in range(15)]
    w2 =  [[w0[j][i + j] for j in range(15 - i)] for i in range(15)]
    w2 += [[w0[i + j][j] for j in range(15 - i)] for i in range(1, 15)]
    w3 =  [[w0[j][i - j] for j in range(i + 1)] for i in range(15)]
    w3 += [[w0[j][i - j + 14] for j in range(i, 15)] for i in range(1, 15)]
    return w0, w1, w2, w3

def gameOver(chessboard):
    ws = getChessTables(chessboard)
    def judge(ws, A):
        for w in ws:
            for l in w:
                n = len(l)
                i, j = 0, 0
                while i < n:
                    while i < n and l[i] != A:
                        i += 1
                    if i >= n:
                        break
                    j = i
                    while j < n and l[j] == A:
                        j += 1
                    if j - i >= 5:
                        return True
                    i = j
        return False
    return judge(ws, 1) or judge(ws, 2)

def DFS(isAI, depth, alpha, beta, chessboard):
    nextPos = (-1, -1)
    if gameOver(chessboard) or depth == 0:
        return evaluate(isAI, chessboard), nextPos
    
    def hasNeighbor(x, y):
        def isChess(x, y):
            return 0 <= x and x < 15 and 0 <= y and y < 15 and chessboard[x][y] != 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if isChess(x + i, y + j):
                    return True
        return False

    for i in range(15):
        for j in range(15):
            if chessboard[i][j] == 0 and hasNeighbor(i, j):
                chessboard[i][j] = 1 if isAI else 2
                tmp = DFS(not isAI, depth - 1, -beta, -alpha, chessboard)
                # print(tmp)
                value = -tmp[0]
                chessboard[i][j] = 0
                
                if value > alpha:
                    if value >= beta:
                        return beta, nextPos
                    alpha = value
                    nextPos = (i, j)
    
    return alpha, nextPos

def evaluate(isAI, chessboard):
    ws = getChessTables(chessboard)
    
    def cal(ws, A, B):
        ans = 0
        for w in ws:
            # print("Hello")
            for l in w:
                # print("World")
                n = len(l)
                i, j = 0, 0
                while i < n:
                    while i < n and l[i] != A:
                        i += 1
                    if i >= n:
                        break
                    j = i
                    while j < n and l[j] == A:
                        j += 1
                    # print(i, j)
                    if i - 1 >= 0 and j < n and l[i - 1] != B and l[j] != B:
                        ans += 10 ** (j - i)
                    else:
                        ans += 10 ** (j - i - 1)
                    i = j
        return ans
    
    A = 1 if isAI else 2
    B = 2 if isAI else 1
    
    return cal(ws, A, B) - cal(ws, B, A)

def decision():
    chessboard = readChessTable()
    num1, num2 = 0, 0
    for i in range(15):
        for j in range(15):
            if chessboard[i][j] == 1:
                num1 += 1
            if chessboard[i][j] == 2:
                num2 += 1
    alpha, pos = DFS(num1 == num2, 3, -99999999, 99999999, chessboard)
    return pos

if __name__ == "__main__":
    while True:
        print("Press ENTER to continue:")
        input()
        pos = decision()
        print(pos)
