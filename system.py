class whole_system(object):
    """Class that contains the whole system"""
    def __init__(self):
        self.nnodes=0
        self.nbranches=0
        self.onephasepqbrancharray=[]
        self.threephaseconstantbrancharray=[]
        self.onephasetrfmarray=[]
        self.onephasevoltagesourcearray=[]
        self.onephaseregulatorarray=[]
