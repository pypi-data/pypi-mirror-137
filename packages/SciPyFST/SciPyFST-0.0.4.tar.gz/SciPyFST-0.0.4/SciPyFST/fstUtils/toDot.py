from .. import fst

def toDot(fst:'fst', **kwargs):
    """
    nameGV = 'fst'\n
    rankdirGV = 'LR'\n
    colorOfNoneState = None\n
    colorOfUnreachableStates = 'aqua'\n
    highlightStates = []\n
    highlightStatesColor = 'lightblue'\n
    highlightPath = []\n
    highlightPathColor = 'red3'\n
    \n
    !!! DRAFT !!!
    Output example:\n
    digraph fst {\n
        rankdir=LR;\n
        node [shape = point ]; none\n
        node [shape = doublecircle]; 0; # initState\n
        none -> 0;\n
        node [shape = circle]; 0 1; # states\n
        node [style=filled, fillcolor=red];\n
        0 -> 1 [ label = 2 ]; # State -> nextState [ label = "inAlphabet" ]\n
        0 -> 0 [ label = 1 ];\n
        1 -> 0 [ label = 0 ];\n
        1 -> 2 [ label = 0 ];\n
        2 -> 1 [ label = 2 ];\n
        2 -> 2 [ label = 0 ];
    }
    """

    nameGV = kwargs.pop('nameGV', 'fst')
    rankdirGV = kwargs.pop('rankdirGV', 'LR')
    colorOfNoneState = kwargs.pop('colorOfNoneState', None)
    colorOfUnreachableStates = kwargs.pop('colorOfUnreachableStates', None)
    highlightStates = kwargs.pop('highlightStates', [])
    highlightStatesColor = kwargs.pop('highlightStatesColor', 'lightblue')
    highlightPath = kwargs.pop('highlightPath', None)
    highlightPathColor = kwargs.pop('highlightPathColor', 'red3')

    ifNotInDict = '-'
    unreachableStates = fst.getUnreachableStates() if colorOfUnreachableStates is not None else []
    if highlightPath is not None:
        hlPathStates = fst.playFST(highlightPath)[1]
        hlPathTransition = list(zip(hlPathStates, highlightPath, hlPathStates[1:]))
    else:
        hlPathStates = []
        hlPathTransition = []

    # Dot header
    outString = "digraph {} {{\n\trankdir={};\n\tnode [shape=point]; start;".format(nameGV, rankdirGV)
    # InitState
    outString += "\n\tnode [shape=circle];"
    nodeStyle = "style=filled, fillcolor={}, ".format(highlightStatesColor) if fst.initState in highlightStates else ""
    nodeStyle2 = "color={hlc}, fontcolor={hlc}, style=bold, ".format(hlc=highlightPathColor) if fst.initState in hlPathStates else ""
    nodeStyle3 = "shape=doublecircle, " if fst.initState in fst.finalStates else ""
    if fst.isMoore():
        outString += "\n\t\"{initState}\" [{style}{style2}label=\"{initState}/{outSignal}\"];".format(
            initState = str(fst.initState),
            outSignal = fst.getOutSignal(fst.initState, None, ifNotInDict),
            style = nodeStyle,
            style2 = nodeStyle2)
    else:
        outString += "\n\t\"{initState}\" [{style3}{style}{style2}label=\"{initState}\"];".format(
            initState = str(fst.initState),
            style3 = nodeStyle3,
            style = nodeStyle,
            style2 = nodeStyle2)
    outString += "\n\tstart -> \"{initState}\" [label=start];\n\tnode [shape=circle];".format(initState = str(fst.initState))
    # all states
    for state in fst.states:
        if state != fst.initState:
            nodeStyle = "shape=doublecircle, " if state in fst.finalStates else ""
            if state in highlightStates:
                nodeStyle += "style=filled, fillcolor={}, ".format(highlightStatesColor)
            elif state in unreachableStates:
                nodeStyle += "style=filled, fillcolor={}, ".format(colorOfUnreachableStates)

            nodeStyle2 = "color={hlc}, fontcolor={hlc}, style=bold, ".format(hlc=highlightPathColor) if state in hlPathStates else ""
            if fst.isMoore():
                outString += "\n\t\"{state}\" [{style}{style2}label=\"{state}/{outSignal}\"];".format(
                    state = state,
                    style = nodeStyle,
                    style2 = nodeStyle2,
                    outSignal = fst.getOutSignal(state, None, ifNotInDict))
            else:
                outString += "\n\t\"{state}\" [{style}{style2}label=\"{state}\"];".format(
                    state = state,
                    style = nodeStyle,
                    style2 = nodeStyle2)
    # None state
    if colorOfNoneState is not None:
        outString += "\n\t\"-\" [style=filled, fillcolor={}, label=\"fail\"];".format(colorOfNoneState)

    outString += "\n\tnode [style=filled, fillcolor=hotpink];"
    # transition
    for (state, inSignal, nextState) in fst.transitionFunction:
        pathStyle = "color={hlc}, fontcolor={hlc}, style=bold, ".format(hlc=highlightPathColor) \
            if (state, inSignal, nextState) in hlPathTransition else ""
        if nextState is None:
            nextState = ifNotInDict
        if fst.isMoore() or fst.isFSM():
            outString += "\n\t\"{state}\" -> \"{nextState}\" [{style}label={inSignal}];".format(
                state = str(state), nextState = str(nextState),
                inSignal = str(inSignal) if inSignal is not None else 'ε',
                style = pathStyle)
        else:
            outString += "\n\t\"{state}\" -> \"{nextState}\" [{style}label=\"{inSignal}/{outSignal}\"];".format(
                state = str(state), nextState = str(nextState), inSignal = str(inSignal),
                outSignal = fst.getOutSignal(state, inSignal, ifNotInDict), style = pathStyle)
    outString += "\n}"
    return outString
