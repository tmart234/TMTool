# CVSS V2, Base scoring only
# work in progress

def get_ac(access_complexity):
    if access_complexity is 'high':
        return 0.35
    elif access_complexity is 'medium':
        return 0.61
    elif access_complexity is 'low':
        return 0.71
    return

def get_auth(authentication):
    if authentication is 'none':
        return 0.704
    elif authentication is 'single':
        return 0.56
    elif authentication is 'multiple':
        return 0.45
    return

def get_av(access_vector):
    if access_vector is 'local':
        return 0.395
    elif access_vector is 'local network':
        return 0.646
    elif access_vector is 'network':
        return 1
    return

def get_conf(conf_impact):
    if conf_impact is 'none':
        return 0
    elif conf_impact is 'partial':
        return 0.275
    elif conf_impact is 'complete':
        return 0.660
    return

def get_integ(integ_impact):
    if integ_impact is 'none':
        return 0
    elif integ_impact is 'partial':
        return 0.275
    elif integ_impact is 'complete':
        return 0.660
    return
 
def get_integ(integ_impact):
    if integ_impact is 'none':
        return 0
    elif integ_impact is 'partial':
        return 0.275
    elif integ_impact is 'complete':
        return 0.660
    return

def get_avail(aval_impact):
    if aval_impact is 'none':
        return 0
    elif aval_impact is 'partial':
        return 0.275
    elif aval_impact is 'complete':
        return 0.660
    return

class Base():
    def __init__(self):
        # TODO: figure out how were importing values here
        # then calculate the base score
        self.calulate_base()

    def calulate_base(self):
        self.impact = 10.41 * (1 - (1 - self.conf_impact) * (1 - self.integ_impact) * (1 - self.aval_impact))
        self.exploitability = 20 * self.access_complexity * self.authentication * self.access_vector
        if self.impact == 0:
            self.f_Impact = 0
        else:
            self.f_Impact = 1.176
        self.base_score = (0.6*self.impact) + (((0.4*self.exploitability)-1.5)*self.f_impact)