def deathProb(age: int, iswoman: bool):
    if age < 12:
        return 0.25
    elif age < 45:
        return 0.15 if iswoman else 0.1
    elif age < 76:
        return 0.35 if iswoman else 0.3
    elif age < 125:
        return 0.65 if iswoman else 0.7
    else:
        return 1.0

def fixedDeathProb(iswoman: bool):
    women = [(0,12,0.25), (12,45,0.15), (45,76,0.35),(76,125,0.65)]
    men = [(0,12,0.25), (12,45,0.1), (45,76,0.3), (76,125,0.7)]
    return women if iswoman else men

def pregnantProb(age: int):
    if age < 12:
        return 0
    elif age < 15:
        return 0.2
    elif age < 21:
        return 0.45
    elif age < 35:
        return 0.8
    elif age < 45:
        return 0.4
    elif age < 60:
        return 0.2
    else:
        return 0.05

def partnerWantedProb(age: int):
    if age < 12:
        return 0
    elif age < 15:
        return 0.6
    elif age < 21:
        return 0.65
    elif age < 35:
        return 0.8
    elif age < 45:
        return 0.6
    elif age < 60:
        return 0.5
    else:
        return 0.2

def childsWantedProb(babynumber: int):
    probs = [0.6, 0.75, 0.35, 0.2, 0.1, 0.05]
    return probs[babynumber]

def bePartnersProb(agediff: int):
    if agediff <= 5:
        return 0.45
    elif agediff <= 10:
        return 0.4
    elif agediff <= 15:
        return 0.35
    elif agediff <= 20:
        return 0.25
    else:
        return 0.15

def mourningTimeLambda(age: int):
    if age <= 15:
        return 3
    elif age <= 35:
        return 6
    elif age <= 45:
        return 12
    elif age <= 60:
        return 24
    else:
        return 48

def babiesBorn(probability: float):
    if probability <= 0.7:
        return 1
    elif probability <= 0.86:
        return 2
    elif probability <= 0.94:
        return 3
    elif probability <= 0.98:
        return 4
    else:
        return 5   

