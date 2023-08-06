from .. import fst

def playToWave(fst:'fst', inSignals: list, hscale=1, useLogic=False):
    """
    { "signal": [
    { "name": "CLK",  "wave": "p......." },
    { "name": "CMD",  "wave": "x.3x=x4x=x=x=x=x", "data": ["RAS", "NOP"] },
    { "name": "STT",  "wave": "x.=x..=x........", "data": "ROW COL" }
    { "name": "OUT",  "wave": "z.......0.1010z.", "data": "ROW COL" }
    ]}
    """
    useLogicForStates = False
    curentState = fst.initState
    waveCLK = "{ \"name\": \"CLK\",  \"wave\": \"P."
    waveRST = "{ \"name\": \"RST\",  \"wave\": \"10"
    waveCMD = "{ \"name\": \"CMD\",  \"wave\": \"zz"
    dataCMD = "\", \"data\": ["
    waveSTT = "{ \"name\": \"STT\",  \"wave\": \"x"
    dataSTT = "\", \"data\": ["
    waveOUT = "{ \"name\": \"OUT\",  \"wave\": \"x"
    dataOUT = "\", \"data\": ["
    prefixCMD = ""
    prefixSTT = ""
    prefixOUT = ""
    oldCMD = None
    oldSTT = None
    oldOUT = None
    # fix state after "reset"
    if fst.isMealy():
        if useLogicForStates and useLogic and curentState in [0, 1]:
            waveSTT += str(curentState)
        else:
            waveSTT += "="
            dataSTT += "{prefix}\"{val}\"".format(prefix = prefixSTT, val = curentState)
            prefixSTT = ", "
        oldSTT = curentState
        waveOUT += "x"

    # play FST and draw Wave
    for inSignal in inSignals:
        waveCLK += "."
        waveRST += "."
        # Draw inSignal - CMD
        if oldCMD == inSignal:
            waveCMD += "."
        else:
            if useLogic and inSignal in [0, 1]:
                waveCMD += str(inSignal)
            else:
                waveCMD += "="
                dataCMD += "{prefix}\"{val}\"".format(prefix = prefixCMD, val = str(inSignal))
                prefixCMD = ", "
        # Draw States - STT
        if oldSTT == curentState:
            waveSTT += "."
        else:
            if useLogicForStates and useLogic and curentState in [0, 1]:
                waveSTT += str(curentState)
            else:
                waveSTT += "="
                dataSTT += "{prefix}\"{val}\"".format(prefix = prefixSTT, val = str(curentState))
                prefixSTT = ", "
        # Draw outSignal - OUT
        curentOUT = fst.getOutSignal(curentState, inSignal, '...')
        if oldOUT == curentOUT:
            waveOUT += "."
        else:
            if useLogic and curentOUT in [0, 1]:
                waveOUT += str(curentOUT)
            else:
                waveOUT += "="
                dataOUT += "{prefix}\"{val}\"".format(prefix = prefixOUT, val = str(curentOUT))
                prefixOUT = ", "
        # keep old value
        oldCMD = inSignal
        oldSTT = curentState
        oldOUT = curentOUT
        curentState = fst.getNextState(curentState, inSignal, curentState)
    waveCLK += "\" },"
    waveRST += "\" },"
    waveCMD += dataCMD + "],\"phase\":" + str(0.85 * hscale) + "},"
    waveSTT += dataSTT + "] },"
    waveOUT += dataOUT + "],\"phase\":" + ( str(-0.2 * hscale) if fst.isMealy() else "0" ) + "}"
    wave = "{ \"signal\": [" + waveCLK + waveRST + waveCMD + waveSTT + waveOUT + "],\"config\":{\"hscale\":" + str(hscale) + "}}"
    return wave
