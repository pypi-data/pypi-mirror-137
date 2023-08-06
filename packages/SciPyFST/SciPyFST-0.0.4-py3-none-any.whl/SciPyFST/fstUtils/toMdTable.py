from .. import fst

def toMdTable(fst:'fst'):
    """
    !!! DRAFT !!!
    Output example:\n
    | Input \\ State | q0  | q1  | q2  | q3  |
    |:--------------:|:---:|:---:|:---:|:---:|
    |       0        | ... | ... | ... | q0  |
    |       1        | ... | q2  | ... | ... |
    |       2        | ... | ... | ... | ... |
    """

    outString = "| Input \\ State |"
    if fst.isMoore():
        for state in fst.states:
            outString += " {state}/{outSignal} |".format(state = state, outSignal = fst.getOutSignal(state, None, "-"))
    else:
        for state in fst.states:
            outString += " {state} |".format(state = state)
    outString += "\n|:---:|"
    for state in fst.states:
        outString += ":---:|"
    outString += "\n"
    for inSignal in fst.inAlphabet + [None] if fst.withEpsilon() else fst.inAlphabet:
        outString += "| {inSignal} |".format(inSignal = inSignal if inSignal is not None else 'ε' )
        for curentState in fst.states:
            tempVal = ', '.join(fst.getNextState(curentState, inSignal)) \
                if isinstance(fst.getNextState(curentState, inSignal), list) \
                else fst.getNextState(curentState, inSignal)
            if tempVal is not None:
                if fst.isMoore() or fst.isFSM():
                    outString += " {nextState} |".format(nextState = tempVal)
                else:
                    outString += " {nextState}/{outSignal} |".format(nextState = tempVal, outSignal = fst.getOutSignal(curentState, inSignal, "-"))
            else:
                if fst.isMoore() or fst.isFSM():
                    outString += " - |"
                else:
                    outString += " -/{outSignal} |".format(nextState = tempVal, outSignal = fst.getOutSignal(curentState, inSignal, "-"))
        outString += "\n"
    return outString
