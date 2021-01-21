# CVSS V2, Base scoring only
# work in progress
# use https://nvd.nist.gov/vuln-metrics/cvss/v2-calculator to check yourself

def get_ac(access_complexity):
    if access_complexity is 'H':
        return 0.35
    elif access_complexity is 'M':
        return 0.61
    elif access_complexity is 'L':
        return 0.71
    return

def get_auth(authentication):
    if authentication is 'N':
        return 0.704
    elif authentication is 'S':
        return 0.56
    elif authentication is 'M':
        return 0.45
    return

def get_av(access_vector):
    if access_vector is 'L':
        return 0.395
    elif access_vector is 'A':
        return 0.646
    elif access_vector is 'N':
        return 1
    return

def get_conf(conf_impact):
    if conf_impact is 'N':
        return 0
    elif conf_impact is 'P':
        return 0.275
    elif conf_impact is 'C':
        return 0.660
    return

def get_integ(integ_impact):
    if integ_impact is 'N':
        return 0
    elif integ_impact is 'P':
        return 0.275
    elif integ_impact is 'C':
        return 0.660
    return
 
def get_integ(integ_impact):
    if integ_impact is 'N':
        return 0
    elif integ_impact is 'P':
        return 0.275
    elif integ_impact is 'C':
        return 0.660
    return

def get_avail(aval_impact):
    if aval_impact is 'N':
        return 0
    elif aval_impact is 'P':
        return 0.275
    elif aval_impact is 'C':
        return 0.660
    return

def get_cdp(cdp):
    if cdp is 'N':
        return 0
    elif cdp is 'L':
        return 0.1
    elif cdp is 'LM':
        return 0.3
    elif cdp is 'MH':
        return 0.4
    elif cdp is 'H':
        return 0.5
    return

class CVSS():
    def __init__(self):
        # static value, assume target exists in env on a considerable scale
        # TODO: input Security requirements and TD
        self.TD = 1.0
        self.base = dict.fromkeys('AV','AC','AU','C','I','A')
        self.env = dict.fromkeys('CPD','TD','CR','IR','AR')
        # TODO: figure out how were importing values here
        # then calculate the base score
        self.base_score = self.calulate_base()
        # since temporal is not used
        self.temporal = self.base_score
        self.env_score = self.calulate_env()
        self.calulate_overall()

    def calulate_base(self):
        self.impact = 10.41 * (1 - (1 - self.conf_impact) * (1 - self.integ_impact) * (1 - self.aval_impact))
        self.exploitability = 20 * self.access_complexity * self.authentication * self.access_vector
        if self.impact == 0:
            self.f_Impact = 0
        else:
            self.f_Impact = 1.176
        self.base_score = (0.6*self.impact) + (((0.4*self.exploitability)-1.5)*self.f_impact)
        return

    def calulate_env(self):
        self.env = ((self.adj_temp + (10 - self.adj_temp) * self.CDP) * self.TD)
        return
 
# AdjustedTemporal = TemporalScore recomputed with the Impact sub-equation 
#                    replaced with the following AdjustedImpact equation.
 
# AdjustedImpact = Min(10, 
#                      10.41 * (1 - 
#                                 (1 - ConfImpact * ConfReq) 
#                               * (1 - IntegImpact * IntegReq) 
#                               * (1 - AvailImpact * AvailReq)))
 

    def calulate_overall(self):
        print('cal overall')