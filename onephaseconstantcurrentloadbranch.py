class onephaseconstantcurrentloadbranch(object):#current and power factor is constant
    def __init__(self):
        self.frnode=-2
        self.tonode=-2
        self.frnodename=''
        self.tonodename=''
        self.p=0.0#kW
        self.q=0.0#kVar
        self.vn=0.0#normal voltage,kV
        