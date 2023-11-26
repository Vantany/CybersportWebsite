class Attack():

    def __init__(self, cap = 0, pot = 0, div = 1) -> None:
        self.capability = cap
        self.potential = pot
        self.divider = div

    def countWeight(self):
        global attack_weight
        return attack_weight[self.capability][self.potential] / self.divider


class checkLine():

    def __init__(self) -> None:
        self.subFig = "x"
        self.Attacks = []
        self.curAttack = Attack()
        self.iter = 1
        self.checkEdge = False
        self.attackplace = 1

    def getAttacks(self, cellX, cellY, subFig, dx, dy):
        self.subctitudeFigure(subFig)
        x, y = cellX - dx, cellY - dy
        while abs(x-cellX) <= 5 and abs(y - cellY) <= 5:
            if self.checkCell(x, y):
                break
            x -= dx
            y -= dy

        self.turnAround()

        x, y = cellX + dx, cellY + dy
        while abs(x - cellX) <= 5 and abs(y - cellY) <= 5:
            if self.checkCell(x, y):
                break

        return self.Attacks
        
    
    def checkCell(self, x, y):
        global grid
        fig = grid[x][y] if (x<19 and y<19) else "b"

        if self.iter == 4 and fig == self.subFig:
            self.checkEdge = True
        elif self.iter == 5:
            self.checkEdgeCell(x, y)
            return 0
        
        self.iter += 1

        if (fig == "o" or fig == "x"):
            if self.subFig != fig:
                self.Attacks.append(self.curAttack)
                return fig
            else:
                self.curAttack.capability += 1
                self.attackplace += 1
        elif fig == "b":
            self.Attacks.append(self.curAttack)
            return "b"
        else:
            if self.curAttack.capability:
                self.curAttack.potential += 1
                self.Attacks.append(self.curAttack)
                self.curAttack = Attack()
                self.curAttack.potential += 1
            self.curAttack.divider += 1
            self.attackplace += 1

    def subctitudeFigure(self, fig):
        self.subFig = fig
        self.curAttack.capability += 1

    def checkEdgeCell(self, x, y):
        if self.checkEdge:
            global grid
            fig = grid[x][y] if (x<19 and y<19) else "b"  
            if fig == self.curFig or fig == 0:
                self.curAttack.potential += 1

            if (self.curAttack.capability):
                self.Attacks.append(self.curAttack)

    def turnAround(self):
        self.iter = 1
        self.checkEdge = False
        self.curAttack = self.Attacks[0]
        self.Attacks.pop(0)


class Game():

    def getfig(self, x, y):
        global grid
        return grid[x][y] if (x < 19 and y<19) else "b" 

    def checkline(self, x, y, dx, dy, newFig):
        x = int(x)
        y = int(y)
        score = 0
        while (self.getfig(x-dx, y-dy) == newFig):
            x -= dx
            y -= dy

        while(self.getfig(x, y) == newFig):
            x += dx
            y += dy
            score += 1

        return True if score >= 5 else False
        

    def checkWin(self, cellX, cellY):
        res = None
        newFig = self.getfig(cellX, cellY)
        if not newFig:
            return False
        
        res = res or self.checkline(cellX, cellY, 1, 0, newFig)
        res = res or self.checkline(cellX, cellY, 0, 1, newFig)
        res = res or self.checkline(cellX, cellY, 1, 1, newFig)
        res = res or self.checkline(cellX, cellY, 1, -1, newFig)

        return res

    def countWeight(self, x, y):
        attacks = self.getAllAttacks(x, y)
        if not attacks:
            return
        sum = 0

        sum += self.Count(attacks.x, "x")
        sum += self.Count(attacks.o, "o")

        return sum
    
    def Count(self, atks, curFig):
        global que, attack_weight
        weight = 0
        breakPoints = 0

        for p in ["0", "45", "90", "135"]:
            if self.isBreakPoint(atks[p]):
                breakPoints += 1
                if breakPoints == 2:
                    weight += 100
                    break

            for a in atks[p]:
                if a.capability > 5:
                    a.capability = 5
                if a.capability == 5 and (curFig == que):
                    weight += 100
                weight += attack_weight[a.capability][a.potential] / a.divider

        return weight

    
    def getAllAttacks(self, cellX, cellY):
        global grid
        if grid[cellX][cellY] != 0:
            return False
        
        cX = {}
        cO = {}

        cX["0"] = self.getAttackLine(cellX, cellY, "x", 1, 0)
        cX["90"] = self.getAttackLine(cellX, cellY, "x", 0, 1)
        cX["45"] = self.getAttackLine(cellX, cellY, "x", 1, -1)
        cX["135"] = self.getAttackLine(cellX, cellY, "x", 1, 1)
        
        cX["0"] = self.getAttackLine(cellX, cellY, "o", 1, 0)
        cX["90"] = self.getAttackLine(cellX, cellY, "o", 0, 1)
        cX["45"] = self.getAttackLine(cellX, cellY, "o", 1, -1)
        cX["135"] = self.getAttackLine(cellX, cellY, "o", 1, 1)


    def getAttackLine(self, cellX, cellY, subFig, dx, dy):
        C = checkLine()
        C.getAttacks(cellX, cellY, subFig, dx, dy)
        return self.filterAttacks(C)
    
    def filterAttacks(self, attackLine ):
        res = []
        if attackLine.attackplace >= 5:
            for a in attackLine.Attacks:
                if a.capability and a.potential or a.capability >= 5:
                    res.append(a)
        
        attackLine.Attacks = res
        return res
    
    def isBreakPoint(self, attackLine):
        if not attackLine or len(attackLine) == 0:
            return False
        
        for a in attackLine:
            if a.divider == 1:
                centAtk = a

        if centAtk.capability >= 4:
            return True
        if centAtk.potential == 2 and centAtk.capability >= 3:
            return True
        
        res = False
        for a in attackLine:
            score = centAtk.copability
            if a.divider == 2:
                if centAtk.potential == 2 and a.potential == 2:
                    score += 1
                if score + a.capability >= 4:
                    res = True
                    break
        
        return res

new_game = Game()
grid = [[0]*19 for i in range(19)]
attack_weight = [[0, 0, 0], [0, 0.1, 0.25], [0, 2, 5], [0, 4, 7], [0, 6, 100], [200, 200, 200]]
que = "0"
str_grid = "_xxxxxoo_xoxo__xoo_o_oxx_oo_x______o_______x___oo_x_x_o_x_______oxo___o_x__o_o______x__o_____x__o_____o______x_____xoxoo___xo_____o__x_x__________x__x____o_xo__x__o___x_______o_x______xo______oxo_x_xx__xox___ox____x_oo__ox_x_x___o__________x______________o_____x____o___x___xo___x__x_xo__x_x___ox___x_______x____x_o_x__x_o__ox__o__x__ox_x_____x_oo_____x____o_ox"
for i in range(19*19):
    grid[i//19][i%19] = str_grid[i] if str_grid[i] in ["x", "o"] else 0

def win_checker():
    win = False
    for row in range(19):
        for column in range(19):
            if new_game.checkWin(row, column):
                win = True

    return win

print(win_checker())