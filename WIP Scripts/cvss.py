# CVSS V2 scoring
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
    else:
        return 0

def get_TD(td):
    if td is 'N':
        return 0
    elif td is 'L':
        return 0.25
    elif td is 'M':
        return 0.75
    elif td is 'H':
        return 1.0
    else:
        return 1.0

def get_conf_req(req):
    if req is 'L':
        return 0.5
    elif req is 'M':
        return 1.0
    elif req is 'H':
        return 1.51
    else:
        return 1.0

def get_integ_req(req):
    if req is 'L':
        return 0.5
    elif req is 'M':
        return 1.0
    elif req is 'H':
        return 1.51
    else:
        return 1.0

def get_avail_req(req):
    if req is 'L':
        return 0.5
    elif req is 'M':
        return 1.0
    elif req is 'H':
        return 1.51
    else:
        return 1.0


class CVSS():
    # takes in a cvss dict
    def __init__(self, cvss_dict):
        # static value, assume target exists in env on a considerable scale
        self.TD = 1.0
        self.temporal_score = None
        self.cvss_dict = cvss_dict
        self.calulate_base()
        # since temporal is not used
        self.temporal = self.base_score
        self.calulate_env()
        self.calulate_overall()
        return

    # TODO: get values from dict and get_() functions above
    def calulate_base(self):
        self.impact = round(10.41 * (1 - (1 - get_conf(self.cvss_dict.get('C'))) * (1 - get_integ(self.cvss_dict.get('I'))) * (1 - get_avail(self.cvss_dict.get('A')))), 1)
        self.exploitability = round(20 * get_ac(self.cvss_dict.get('AC')) * get_auth(self.cvss_dict.get('Au')) * get_av(self.cvss_dict.get('AV')),1)
        self.f_impact = 0
        if self.impact > 0:
            self.f_impact = 1.176
        self.base_score = round((((0.6*self.impact) + (0.4*self.exploitability)-1.5) * self.f_impact), 1)
        return

    def calulate_env(self):
        _conf = (1 - get_conf(self.cvss_dict.get('C')) * get_conf_req(self.cvss_dict.get('CR')))
        _integ = (1 - get_integ(self.cvss_dict.get('I')) * get_integ_req(self.cvss_dict.get('IR')))
        _avail = (1 - get_avail(self.cvss_dict.get('A')) * get_avail_req(self.cvss_dict.get('AR')))
        self.adj_impact = min(10, (10.41 * (1 - (_conf) * (_integ) * (_avail))))
        self.adj_temp = round((((0.6*self.adj_impact) + (0.4*self.exploitability)-1.5) * self.f_impact), 1)
        self.env_score = round(((self.adj_temp + (10 - self.adj_temp) * get_cdp(self.cvss_dict.get('CDP'))) * get_TD(self.cvss_dict.get('TD'))), 1)
        return

    # See overall score decision tree
    def calulate_overall(self):
        if self.env_score:
            self.overall_score = self.env_score
        elif self.temporal_score:
            self.overall_score = self.temporal_score
        else:
            self.overall_score = self.base_score

def main():
    # CVSS Base Score: 5.4
    # Impact Subscore: 6.9
    # Exploitability Subscore: 4.9
    # CVSS Temporal Score: NA
    # CVSS Environmental Score: 8.6
    # Modified Impact Subscore: 10.0
    # Overall CVSS Score: 8.6
    # bullshit example: 
    # https://nvd.nist.gov/vuln-metrics/cvss/v2-calculator?vector=(AV:N/AC:H/Au:N/C:C/I:N/A:N/CDP:MH/TD:H/CR:H/IR:H/AR:L)
    mydict =  {'AV':'N','AC':'H','Au':'N','C':'C','I':'N','A':'N','CDP':'MH','TD':'H','CR':'H','IR':'H','AR':'L'}
    score= CVSS(mydict)
    print(score.overall_score)

if __name__ == "__main__":
    main()
