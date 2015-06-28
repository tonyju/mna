class threephaseconstantbranch(object):
    def __init__(self):
        self.diagg=[0.0,0.0,0.0]#ohm
        self.diagb=[0.0,0.0,0.0]#ohm
        self.offdiagg=[0.0,0.0,0.0,0.0,0.0,0.0]#ohm [0][1] [0][2] [1][0] [1][2] [2][0] [2][1]
        self.offdiagb=[0.0,0.0,0.0,0.0,0.0,0.0]#ohm
        self.frnode=[-2,-2,-2]
        self.tonode=[-2,-2,-2]
        self.frnodename=['','','']
        self.tonodename=['','','']
        self.branchid=[-1,-1,-1]
