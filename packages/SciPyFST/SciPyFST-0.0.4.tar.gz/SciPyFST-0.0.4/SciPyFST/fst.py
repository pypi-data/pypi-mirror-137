from copy import deepcopy

class fst:
    def __init__(self,
                states:list=[],
                initState=None,
                inAlphabet:list=[],
                outAlphabet:list=[],
                transitionFunction:list=[],
                outputFunction:list=[],
                finalStates:list=[],
        ):
        self.states = sorted(dict.fromkeys(states))#, key=str)
        """ states = [0,1,2] """

        self.initState = deepcopy(initState)
        """ initState = 0 """

        self.inAlphabet = sorted(dict.fromkeys(inAlphabet))#, key=str)
        """ inAlphabet = [0,1] """

        self.outAlphabet = sorted(dict.fromkeys(outAlphabet))#, key=str)
        """ outAlphabet = [0,1,2] """

        self.transitionFunction = deepcopy(transitionFunction)
        """ transitionFunction [ [State, inAlphabet, nextState], ...]\n
        transitionFunction = [ [0,0,1], [1,0,1], [1,1,2] ] """

        self.outputFunction = deepcopy(outputFunction)
        """
        outputFunction Moore [ [State, outAlphabet], ...]\n
        outputFunction = [ [0,0], [1,0], [2,2]]\n
        outputFunction Mealy [ [State, inAlphabet, outAlphabet], ...]\n
        outputFunction = [ [0,1,0], [1,1,0], [2,2,2]]
        """

        self.finalStates = sorted(dict.fromkeys(finalStates))#, key=str)
        """ finalStates = [0,1,2] """

        self.__type = self.__detTypeByOutputFunction()

        self.states = sorted(dict.fromkeys(self.states + self.__getStatesFromTransitionAndOutputFunction()))#, key=str)
        self.inAlphabet = sorted(dict.fromkeys(self.inAlphabet + self.__getInAlphabetFromTransitionAndOutputFunction()))#, key=str)
        self.outAlphabet = sorted(dict.fromkeys(self.outAlphabet + self.__getOutAlphabetFromTransitionAndOutputFunction()))#, key=str)

        self.trFuncDict = dict()
        for (curentState, inSignal, nextState) in self.transitionFunction:
            if (curentState, inSignal) in self.trFuncDict:
                temp = self.trFuncDict[curentState, inSignal] \
                    if isinstance(self.trFuncDict[curentState, inSignal], list) \
                    else [self.trFuncDict[curentState, inSignal]]
                self.trFuncDict[curentState, inSignal] = temp + [nextState]
            else:
                self.trFuncDict[curentState, inSignal] = nextState

        self.outFuncDict = dict()
        if self.isMoore():
            for (curentState, outSignal) in self.outputFunction:
                self.outFuncDict[curentState] = outSignal
        else:
            for (curentState, inSignal, outSignal) in self.outputFunction:
                self.outFuncDict[curentState, inSignal] = outSignal

        self.comboStateAndOutDict = dict()
        for (curentState, inSignal, nextState) in self.transitionFunction:
            if self.isMoore():
                self.comboStateAndOutDict[curentState, inSignal] = [nextState, self.outFuncDict.get(curentState)]
            else:
                self.comboStateAndOutDict[curentState, inSignal] = [nextState, self.outFuncDict.get((curentState, inSignal))]

    def __detTypeByOutputFunction(self):
        if self.outputFunction:
            if len(self.outputFunction[0]) == 2:
                return 'Moore'
            return 'Mealy'
        return 'FSM'

    def __getStatesFromTransitionAndOutputFunction(self):
        #if self.isFSM():
        #    return []
        toOut = []
        if self.initState is not None:
            toOut.append(self.initState)
        for (curentState, inSignal, nextState) in self.transitionFunction:
            if curentState is not None:
                toOut.append(curentState)
            if nextState is not None:
                toOut.append(nextState)
        if self.isMoore():
            for (curentState, outSignal) in self.outputFunction:
                if curentState is not None:
                    toOut.append(curentState)
        else:
            for (curentState, inSignal, outSignal) in self.outputFunction:
                if curentState is not None:
                    toOut.append(curentState)
        return sorted(dict.fromkeys(toOut))#, key=str)

    def __getInAlphabetFromTransitionAndOutputFunction(self):
        toOut = []
        for (curentState, inSignal, nextState) in self.transitionFunction:
            if inSignal is not None:
                toOut.append(inSignal)
        if self.isMealy():
            for (curentState, inSignal, outSignal) in self.outputFunction:
                if inSignal is not None:
                    toOut.append(inSignal)
        return sorted(dict.fromkeys(toOut))#, key=str)

    def __getOutAlphabetFromTransitionAndOutputFunction(self):
        if self.isFSM():
            return []
        toOut = []
        if self.isMoore():
            for (curentState, outSignal) in self.outputFunction:
                if outSignal is not None:
                    toOut.append(outSignal)
        else:
            for (curentState, inSignal, outSignal) in self.outputFunction:
                if outSignal is not None:
                    toOut.append(outSignal)
        return sorted(dict.fromkeys(toOut))#, key=str)

    def isValid(self):
        """ Check TODO more checks needed """
        if self.initState not in self.states:
            return False
        # TODO more checks needed
        return True

    def getType(self):
        """
        Return FST type as string - "Moore" or "Mealy"
        """
        return self.__type

    def setType(self, typeString='Moore'):
        """
        TODO broken with adding FSM
        Set FST type - "Moore" or "Mealy"
        """
        if typeString in ['Moore', 'Mealy']:
            if not self.outputFunction:
                self.__type = typeString
                return True
            dem = True
            for out in self.outputFunction:
                if (typeString == 'Moore' and len(out) != 2) or (typeString == 'Mealy' and len(out) != 3):
                    dem = False
                    break
            if dem:
                self.__type = typeString
                return True
        return False

    def deepcopy(self):
        fstOut = fst(self.states, self.initState, self.inAlphabet,\
            self.outAlphabet, self.transitionFunction, self.outputFunction,\
            self.finalStates)
        return fstOut

    def addState(self, state):
        if state not in self.states:
            self.states.append(state)
            self.states = sorted(dict.fromkeys(self.states))#, key=str)
        return True

    def addTransition(self, curentState, inSignal, nextState):
        self.addState(curentState)
        self.addState(nextState)
        if [curentState, inSignal, nextState] not in self.transitionFunction:
            self.transitionFunction.append([curentState, inSignal, nextState])
        self.trFuncDict[curentState, inSignal] = nextState
        return True

    def isMoore(self):
        """
        Return True if self.getType() == 'Moore' else False
        """
        return True if self.getType() == 'Moore' else False

    def isMealy(self):
        """
        Return True if self.getType() == 'Mealy' else False
        """
        return True if self.getType() == 'Mealy' else False

    def isFSM(self):
        """
        Return True if self.getType() == 'FSM' else False
        """
        return True if self.getType() == 'FSM' else False

    def withEpsilon(self):
        """
        Return True if epsilon(None) in transitionFunction(inAlphabet)
        """
        for (state, inSignal, nextState) in self.transitionFunction:
            if inSignal is None:
                return True
        return False

    def getNextState(self, curentState, inSignal, ifNotInDict=None):
        nextSate = self.trFuncDict.get((curentState, inSignal), ifNotInDict)
        if nextSate is None:
            return ifNotInDict
        return nextSate

    def getNextStates(self, curentStates, inSignal, ifNotInDict=None):
        """
        return set of next states for set of curent states & input signal,
        ε-closure is NOT INCLUDED!
        if input signal == None return set of ε-accessible in one step states
        """
        states = set(curentStates) if isinstance(curentStates, (list, set)) else set([curentStates,])
        nextStates = set()
        for state in states:
            if (state, inSignal) in self.trFuncDict:
                temp = self.trFuncDict.get((state, inSignal))
                nextStates.update( temp if isinstance(temp, (list, set)) else set([temp,]) )
            elif inSignal is not None:
                nextStates.update( [None,] )
        return nextStates

    def getOutSignal(self, curentState, inSignal, ifNotInDict=None):
        if self.isMoore():
            outSignal = self.outFuncDict.get(curentState, ifNotInDict)
        else:
            outSignal = self.outFuncDict.get((curentState, inSignal), ifNotInDict)
        if outSignal is None:
            return ifNotInDict
        return outSignal

    def playFST(self, inSignals: list, startState=None):
        outSignals = []
        curentState = self.initState if startState is None else startState
        outStates = []
        for inSignal in inSignals:
            outStates.append(curentState)
            outSignals.append(self.getOutSignal(curentState, inSignal, -1))
            curentState = self.getNextState(curentState, inSignal)#, curentState)
        outStates.append(curentState)
        if self.isMoore():
            outSignals.append(self.getOutSignal(curentState, inSignal, -1))
            return outSignals[1:], outStates
        return outSignals, outStates

    def getEpsilonClosure(self, states):
        """
        return ε-closure of a state or set of states
        https://en.wikipedia.org/wiki/Nondeterministic_finite_automaton#%CE%B5-closure_of_a_state_or_set_of_states
        """
        inStates = set(states) if isinstance(states, (list, set)) else set([states,])
        while True:
            nextStates = self.getNextStates(inStates, None)
            if set(nextStates).issubset(inStates):
                break
            inStates.update(nextStates)
        return inStates

    def playFSM(self, inSignals: list, debug=None):
        def __debug(a):
            if debug: print("--> " + a)
        __debug( "Start print debug info for playFSM():" )
        curentStates = set(self.initState) \
            if isinstance(self.initState, (list, set)) \
            else set([self.initState,])
        for inSignal in inSignals:
            __debug( "  curent state(s): " + str(curentStates) )
            __debug( "  input signal: " + str(inSignal) )
            nextStates = self.getNextStates(curentStates, inSignal)
            __debug( "    next state(s): " + str(nextStates) )
            curentStates = self.getEpsilonClosure(nextStates)
            __debug( "      + ε-closure: " + str(curentStates) )
        if curentStates & set(self.finalStates):
            __debug( "accepting state(s): " + str(curentStates & set(self.finalStates)) )
            return True
        __debug( "last states: " + str( curentStates ) + ", all accepting states: " + str(self.finalStates) )
        return False

    def asMoore(self):
        if self.isMoore():
            return self.deepcopy()

        initStateMoore = 0
        #initStateSignalMoore = -1
        newMooreState_qi = initStateMoore # q0 without q
        markedTranOut = dict() # key - [topHeaderState_Si, leftHeaderSignal_Xj], val - existMooreState_qi. See point (1)
        dictForSearchNewState = dict() # key - [tableState_Sm, tableSignal_Yn] from table, val - existMooreState_qi. See point (1)
        eqStatesFor_Si = dict() # key - tableState_Sm, val - list of existMooreState_qi [0, 2, ...]. See point (2)

        outputFunctionMoore = [] # list [[state, outSignal], [...] ... ]. See point (3)

        # add q0 state to S0
        #mapForSearchNewState[self.initState, None] = newMooreState_qi
        eqStatesFor_Si[self.initState] = [newMooreState_qi]
        #outputFunctionMoore.append([newMooreState_qi, initStateSignalMoore])

        # mark all equivalent transition-output pair as new Moore states. See point (1) & (2)
        for topHeaderState_Si in self.states:
            for leftHeaderSignal_Xj in self.inAlphabet:
                tableState_Sm = self.getNextState(topHeaderState_Si, leftHeaderSignal_Xj)
                tableSignal_Yn = self.getOutSignal(topHeaderState_Si, leftHeaderSignal_Xj)
                existMooreState_qi = dictForSearchNewState.get((tableState_Sm, tableSignal_Yn)) # (1)
                if existMooreState_qi is None:
                    newMooreState_qi += 1
                    existMooreState_qi = newMooreState_qi
                    dictForSearchNewState[(tableState_Sm, tableSignal_Yn)] = existMooreState_qi # (1) add new state
                    outputFunctionMoore.append([existMooreState_qi, tableSignal_Yn])
                    tempList = eqStatesFor_Si.get(tableState_Sm, []) # (2)
                    tempList.append(newMooreState_qi)
                    eqStatesFor_Si[tableState_Sm] = tempList
                markedTranOut[topHeaderState_Si, leftHeaderSignal_Xj] = existMooreState_qi

        # create transition table (4)
        transitionFunctionMoore = []
        for key_Si, list_qj in eqStatesFor_Si.items():
            for qj in list_qj:
                for signal in self.inAlphabet:
                    transitionFunctionMoore.append([qj, signal, markedTranOut.get((key_Si, signal))])

        return fst([], initStateMoore, [], [], transitionFunctionMoore, outputFunctionMoore)

    def getTestSignal(self):
        listOfInSignalsList = []
        def recGetNext(curentState, visitedStates:dict, inSignals:list):
            if visitedStates.get(curentState) is None:
                visitedStates[curentState] = 1
                for inSignal in self.inAlphabet:
                    copyOfInSignals = deepcopy(inSignals)
                    copyOfInSignals.append(inSignal)
                    nextCurentState = self.getNextState(curentState, inSignal)
                    if nextCurentState is None:
                        listOfInSignalsList.append(copyOfInSignals)
                        return
                    else:
                        recGetNext(nextCurentState, deepcopy(visitedStates), copyOfInSignals)
            else:
                listOfInSignalsList.append(inSignals)
                return
        recGetNext(self.initState, dict(), [])
        return listOfInSignalsList

    def _isContains(self, fst:'fst'):
        listOfInSignalsList = fst.getTestSignal()
        for inSignalList in listOfInSignalsList:
            if self.playFST(inSignalList)[0] != fst.playFST(inSignalList)[0]:
                return False
        return True

    def isContains(self, fst:'fst'):
        def recGetNext(curentState, visitedStates:dict, inSignals:list):
            if visitedStates.get(curentState) is None:
                visitedStates[curentState] = 1
                for inSignal in fst.inAlphabet:
                    copyOfInSignals = deepcopy(inSignals)
                    copyOfInSignals.append(inSignal)
                    nextCurentState = fst.getNextState(curentState, inSignal)
                    if nextCurentState is None:
                        return self.playFST(copyOfInSignals)[0] == fst.playFST(copyOfInSignals)[0]
                    else:
                        if not recGetNext(nextCurentState, deepcopy(visitedStates), copyOfInSignals):
                            return False
            else:
                return self.playFST(inSignals)[0] == fst.playFST(inSignals)[0]
            return True
        return recGetNext(fst.initState, dict(), [])

    def isSimilar(self, fst:'fst'):
        return self.isContains(fst) and fst.isContains(self)

    def getUnreachableStates(self):
        unreachableStates = dict.fromkeys(self.states)
        def recGetNext(curentState, visitedStates:dict):
            unreachableStates.pop(curentState, None)
            if visitedStates.get(curentState) is None:
                visitedStates[curentState] = 1
                for inSignal in self.inAlphabet:
                    nextCurentState = self.getNextState(curentState, inSignal)
                    if nextCurentState is None:
                        return
                    else:
                        recGetNext(nextCurentState, deepcopy(visitedStates))
            else:
                return
        recGetNext(self.initState, dict())
        return sorted(unreachableStates)
