class twophaseconstantbranch(object):
    def __init__(self):
        self.diagr=[0.0,0.0]#ohm
        self.diagx=[0.0,0.0]#ohm
        self.offdiagr=[0.0,0.0]#the first element is [0][1] second element is [1][0]
        self.offidagx=[0.0,0.0]#the first element is [0][1] second element is [1][0]
        self.frnode=[-2,-2]
        self.tonode=[-2,-2]
        self.frnodename=['','']
        self.tonodename=['','']
