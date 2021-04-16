## based on OWASP risk rating

# clculates impact or likihood
def calc_scores(_dict):
    # set Numerical Score
    _dict["Numerical Score"] = int(0)
    for key,value in _dict:
        if "Score" in key:
            continue
        else:
            _dict["Numerical Score"] = value + _dict["Numerical Score"]
            
    # set Categorical Score
    if _dict["Numerical Score"] < 3:
        _dict["Categorical Score"] = "Low"
    elif _dict["Numerical Score"] < 6:
        _dict["Categorical Score"] = "Medium"
    elif _dict["Numerical Score"] < 9:
        _dict["Categorical Score"] = "High"
    else:
        _dict["Categorical Score"] = None
    return

# translating the risk matrix
def calc_risk(_likihood,_impact):
    if _likihood["Categorical Score"] == "Low" and _impact["Categorical Score"] == "Low":
        return "Note"
    elif (_likihood["Categorical Score"] == "Low" and _impact["Categorical Score"] == "Medium") or \
        (_likihood["Categorical Score"] == "Medium" and _impact["Categorical Score"] == "Low"):
        return "Low"
    elif (_likihood["Categorical Score"] == "Low" and _impact["Categorical Score"] == "High") or \
        (_likihood["Categorical Score"] == "High" and _impact["Categorical Score"] == "Low") or \
           (_likihood["Categorical Score"] == "Medium" and _impact["Categorical Score"] == "Medium"):
        return "Medium"
    elif (_likihood["Categorical Score"] == "High" and _impact["Categorical Score"] == "Medium") or \
        (_likihood["Categorical Score"] == "Medium" and _impact["Categorical Score"] == "High"):
        return "High"
    elif _likihood["Categorical Score"] == "High" and _impact["Categorical Score"] == "High":
        return "Critical"
    else:
        return None


likihood = dict.fromkeys("SL","M","O","S","ED","EE","Aw","ID","Numerical Score","Categorical Score")
impact = dict.fromkeys("C","I","A","Ac","FD","RD","NCD","PV", "Numerical Score","Categorical Score")

