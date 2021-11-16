import utilities
import soundfile as sf

#kick 1/4
def makeKickPatternOne(inAudio, inBPM, inNumCompas,inSampleRate):

    #Simple QuarterNote [1/4] Pattern
    audio = inAudio
    kickInterval = utilities.computeInterval(inBPM, inSampleRate)
    loopKick = []

    intervalOne = kickInterval
    intervalTwo = kickInterval * 2
    intervalTres = kickInterval * 3

    cont, cont2, cont3, cont4 = 0, 0, 0, 0

    for sample in range(kickInterval * 4):
        if sample < intervalOne:
            if cont < len(audio):
                loopKick.append(audio[cont])
            else:
                loopKick.append(0)
            cont += 1

        elif sample >= intervalOne and sample < intervalTwo:
            if cont2 < len(audio):
                loopKick.append(audio[cont2])
            else:
                loopKick.append(0)
            cont2 += 1

        elif sample >= intervalTwo and sample < intervalTres:
            if cont3 < len(audio):
                loopKick.append(audio[cont3])
            else:
                loopKick.append(0)
            cont3 += 1

        else:
            if cont4 < len(audio):
                loopKick.append(audio[cont4])
            else:
                loopKick.append(0)
            cont4 += 1

    compasCompleto = []
    for compas in range(inNumCompas):
        for sample in loopKick:
            compasCompleto.append(sample)

    #sf.write('../Results/LoopKickOne.wav', compasCompleto, inSampleRate, 'PCM_24')

    #print("KICK LOOP CREADO")
    #print("-----------")

    return compasCompleto, inSampleRate, (len(compasCompleto) / inSampleRate)  #  #kick

#kick 1/8 var
def makeKickPatternTwo(inAudio, inBPM, inNumCompas,inSampleRate):

    # Eight note [1/8] pattern with variations
    audio = inAudio
    kickInterval = utilities.computeInterval(inBPM, inSampleRate)
    loopKick = []

    intervalOne = kickInterval/2
    intervalTwo = kickInterval
    intervalTres = kickInterval * 1.5
    intervalCuatro = kickInterval * 2
    intervalCinco = kickInterval * 2.5
    intervalSix = kickInterval * 3
    intervalSeven = kickInterval * 3.5

    cont, cont2, cont3, cont4, cont5, cont6, cont7, cont8 = 0, 0, 0, 0, 0, 0, 0, 0

    for sample in range(kickInterval * 4):
        if sample < intervalOne:
            if cont < len(audio):
                loopKick.append(audio[cont])
            else:
                loopKick.append(0)
            cont += 1
        elif sample >= intervalOne and sample < intervalTwo:
            if cont2 < len(audio):
                loopKick.append(0)
            cont2 += 1
        elif sample >= intervalTwo and sample < intervalTres:
            if cont3 < len(audio):
                loopKick.append(audio[cont3])
            else:
                loopKick.append(0)
            cont3 += 1
        elif sample >= intervalTres and sample < intervalCuatro:
            if cont4 < len(audio):
                loopKick.append(audio[cont4])
            else:
                loopKick.append(0)
            cont4 += 1
        elif sample >= intervalCuatro and sample < intervalCinco:
            if cont5 < len(audio):
                loopKick.append(audio[cont5])
            else:
                loopKick.append(0)
            cont5 += 1
        elif sample >= intervalCinco and sample < intervalSix:
            if cont6 < len(audio):
                loopKick.append(0)
            cont6 += 1
        elif sample >= intervalSix and sample < intervalSeven:
            if cont7 < len(audio):
                loopKick.append(audio[cont7])
            else:
                loopKick.append(0)
            cont7 += 1
        else:
            if cont8 < len(audio):
                loopKick.append(audio[cont8])
            else:
                loopKick.append(0)
            cont8 += 1

    compasCompleto = []
    for compas in range(inNumCompas):
        for sample in loopKick:
            compasCompleto.append(sample)

    #sf.write('../Results/LoopKickTwo.wav', compasCompleto, inSampleRate, 'PCM_24')

    #print("KICK LOOP CREADO")
    #print("-----------")

    return compasCompleto, inSampleRate, (len(compasCompleto) / inSampleRate)

#hat 1/16
def makeKickPatternDNB(inAudio, inBPM, inNumCompas,inSampleRate):

    # Simple sixteenth note [1/16] pattern
    audio = inAudio
    hatInterval = utilities.computeInterval(inBPM, inSampleRate)
    loopHat = []

    intervalOne = hatInterval/4
    intervalTwo = hatInterval/2
    intervalTres = hatInterval * 0.75
    intervalCuatro = hatInterval
    intervalCinco = hatInterval * 1.25
    intervalSix = hatInterval * 1.5
    intervalSeven = hatInterval * 1.75
    intervalEight = hatInterval * 2
    intervalNine = hatInterval * 2.25
    intervalTen = hatInterval * 2.5
    intervalEleven = hatInterval * 2.75
    intervalDoce = hatInterval * 3
    intervalTrece = hatInterval * 3.25
    intervalCatorce = hatInterval * 3.5
    intervalQuince = hatInterval * 3.75

    cont, cont2, cont3, cont4, cont5, cont6, cont7, cont8 = 0, 0, 0, 0, 0, 0, 0, 0
    cont9, cont10, cont11, cont12, cont13, cont14, cont15, cont16 = 0, 0, 0, 0, 0, 0, 0, 0

    for sample in range(hatInterval * 4):
        if sample < intervalOne:
            if cont < len(audio):
                loopHat.append(audio[sample])
            else:
                loopHat.append(0)
            cont += 1
        elif sample >= intervalOne and sample < intervalTwo:
            if cont2 < len(audio):
                loopHat.append(0)
            cont2 += 1
        elif sample >= intervalTwo and sample < intervalTres:
            if cont3 < len(audio):
                loopHat.append(0)
            cont3 += 1
        elif sample >= intervalTres and sample < intervalCuatro:
            if cont4 < len(audio):
                loopHat.append(0)
            cont4 += 1
        elif sample >= intervalCuatro and sample < intervalCinco:
            if cont5 < len(audio):
                loopHat.append(0)
            cont5 += 1
        elif sample >= intervalCinco and sample < intervalSix:
            if cont6 < len(audio):
                loopHat.append(0)
            cont6 += 1
        elif sample >= intervalSix and sample < intervalSeven:
            if cont7 < len(audio):
                loopHat.append(0)
            cont7 += 1
        elif sample >= intervalSeven and sample < intervalEight:
            if cont8 < len(audio):
                loopHat.append(0)
            cont8 += 1
        elif sample >= intervalEight and sample < intervalNine:
            if cont9 < len(audio):
                loopHat.append(0)
            cont9 += 1
        elif sample >= intervalNine and sample < intervalTen:
            if cont10 < len(audio):
                loopHat.append(0)
            cont10 += 1
        elif sample >= intervalTen and sample < intervalEleven:
            if cont11 < len(audio):
                loopHat.append(audio[cont11])
            else:
                loopHat.append(0)
            cont11 += 1
        elif sample >= intervalEleven and sample < intervalDoce:
            if cont12 < len(audio):
                loopHat.append(0)
            cont12 += 1
        elif sample >= intervalDoce and sample < intervalTrece:
            if cont13 < len(audio):
                loopHat.append(0)
            cont13 += 1
        elif sample >= intervalTrece and sample < intervalCatorce:
            if cont14 < len(audio):
                loopHat.append(0)
            cont14 += 1
        elif sample >= intervalCatorce and sample < intervalQuince:
            if cont15 < len(audio):
                loopHat.append(0)
            cont15 += 1
        else:
            if cont16 < len(audio):
                loopHat.append(0)
            cont16 += 1

    compasCompleto = []
    for compas in range(inNumCompas):
        for sample in loopHat:
            compasCompleto.append(sample)

    #sf.write('../Results/LoopHatTwo.wav', compasCompleto, inSampleRate, 'PCM_24')

    #print("HIHAT LOOP CREADO")
    #print("-----------")

    return compasCompleto, inSampleRate, (len(compasCompleto) / inSampleRate)

#snare 1/4
def makeSnarePatternOne(inAudio, inBPM, inNumCompas,inSampleRate):

    #QuarterNote [1/4] Pattern with OFFSET
    audio = inAudio
    snareInterval = utilities.computeInterval(inBPM, inSampleRate)
    loopSnare = []

    intervalOne = snareInterval
    intervalTwo = snareInterval * 2
    intervalTres = snareInterval * 3

    cont, cont2, cont3, cont4 = 0, 0, 0, 0

    for sample in range(snareInterval * 4):
        if sample < intervalOne:
            #if cont < len(audio):
                #loopSnare.append(0)
            #else:
            loopSnare.append(0)
            cont += 1
        elif sample >= intervalOne and sample < intervalTwo:
            if cont2 < len(audio):
                loopSnare.append(audio[cont2])
            else:
                loopSnare.append(0)
            cont2 += 1
        elif sample >= intervalTwo and sample < intervalTres:
            #if cont3 < len(audio):
            loopSnare.append(0)
            cont3 += 1
        else:
            if cont4 < len(audio):
                loopSnare.append(audio[cont4])
            else:
                loopSnare.append(0)
            cont4 += 1

    compasCompleto = []
    for compas in range(inNumCompas):
        for sample in loopSnare:
            compasCompleto.append(sample)

    #sf.write('../Results/LoopSnareOne.wav', compasCompleto, inSampleRate, 'PCM_24')

    #print("SNARE LOOP CREADO")
    #print("-----------")

    return compasCompleto, inSampleRate, (len(compasCompleto) / inSampleRate)

#snare 1/8
def makeSnarePatternTwo(inAudio, inBPM, inNumCompas,inSampleRate):

    # Eight note [1/8] pattern with variations
    audio = inAudio
    snareInterval = utilities.computeInterval(inBPM, inSampleRate)
    loopSnare = []

    intervalOne = snareInterval/2
    intervalTwo = snareInterval
    intervalTres = snareInterval * 1.5
    intervalCuatro = snareInterval * 2
    intervalCinco = snareInterval * 2.5
    intervalSix = snareInterval * 3
    intervalSeven = snareInterval * 3.5

    cont, cont2, cont3, cont4, cont5, cont6, cont7, cont8 = 0, 0, 0, 0, 0, 0, 0, 0

    for sample in range(snareInterval * 4):
        if sample < intervalOne:
            if cont < len(audio):
                loopSnare.append(0)
            else:
                loopSnare.append(0)
            cont += 1
        elif sample >= intervalOne and sample < intervalTwo:
            if cont2 < len(audio):
                loopSnare.append(0)
            else:
                loopSnare.append(0)
            cont2 += 1
        elif sample >= intervalTwo and sample < intervalTres:
            if cont3 < len(audio):
                loopSnare.append(audio[cont3])
            else:
                loopSnare.append(0)
            cont3 += 1
        elif sample >= intervalTres and sample < intervalCuatro:
            if cont4 < len(audio):
                loopSnare.append(audio[cont4])
            else:
                loopSnare.append(0)
            cont4 += 1
        elif sample >= intervalCuatro and sample < intervalCinco:
            if cont5 < len(audio):
                loopSnare.append(0)
            else:
                loopSnare.append(0)
            cont5 += 1
        elif sample >= intervalCinco and sample < intervalSix:
            if cont6 < len(audio):
                loopSnare.append(0)
            else:
                loopSnare.append(0)
            cont6 += 1
        elif sample >= intervalSix and sample < intervalSeven:
            if cont7 < len(audio):
                loopSnare.append(audio[cont7])
            else:
                loopSnare.append(0)
            cont7 += 1
        else:
            if cont8 < len(audio):
                loopSnare.append(audio[cont8])
            else:
                loopSnare.append(0)
            cont8 += 1

    compasCompleto = []
    for compas in range(inNumCompas):
        for sample in loopSnare:
            compasCompleto.append(sample)

    #sf.write('../Results/LoopSnareTwo.wav', compasCompleto, inSampleRate, 'PCM_24')

    #print("SNARE LOOP CREADO")
    #print("-----------")

    return compasCompleto, inSampleRate, (len(compasCompleto) / inSampleRate)

#snare 1/16 dembow
def makeSnareDembow(inAudio, inBPM, inNumCompas,inSampleRate):

    # Simple sixteenth note [1/16] pattern
    audio = inAudio
    hatInterval = utilities.computeInterval(inBPM, inSampleRate)
    loopHat = []

    intervalOne = hatInterval/4
    intervalTwo = hatInterval/2
    intervalTres = hatInterval * 0.75
    intervalCuatro = hatInterval
    intervalCinco = hatInterval * 1.25
    intervalSix = hatInterval * 1.5
    intervalSeven = hatInterval * 1.75
    intervalEight = hatInterval * 2
    intervalNine = hatInterval * 2.25
    intervalTen = hatInterval * 2.5
    intervalEleven = hatInterval * 2.75
    intervalDoce = hatInterval * 3
    intervalTrece = hatInterval * 3.25
    intervalCatorce = hatInterval * 3.5
    intervalQuince = hatInterval * 3.75

    cont, cont2, cont3, cont4, cont5, cont6, cont7, cont8 = 0, 0, 0, 0, 0, 0, 0, 0
    cont9, cont10, cont11, cont12, cont13, cont14, cont15, cont16 = 0, 0, 0, 0, 0, 0, 0, 0

    for sample in range(hatInterval * 4):
        if sample < intervalOne:
            if cont < len(audio): #1
                loopHat.append(0)
            cont += 1
        elif sample >= intervalOne and sample < intervalTwo:
            if cont2 < len(audio): #2
                loopHat.append(0)
            cont2 += 1
        elif sample >= intervalTwo and sample < intervalTres:
            if cont3 < len(audio): #3
                loopHat.append(0)
            cont3 += 1
        elif sample >= intervalTres and sample < intervalCuatro:
            if cont4 < len(audio): #4
                loopHat.append(audio[cont4])
            else:
                loopHat.append(0)
            cont4 += 1
        elif sample >= intervalCuatro and sample < intervalCinco:
            if cont5 < len(audio): #5
                loopHat.append(0)
            cont5 += 1
        elif sample >= intervalCinco and sample < intervalSix:
            if cont6 < len(audio): #6
                loopHat.append(0)
            cont6 += 1
        elif sample >= intervalSix and sample < intervalSeven:
            if cont7 < len(audio): #7
                loopHat.append(audio[cont7])
            else:
                loopHat.append(0)
            cont7 += 1
        elif sample >= intervalSeven and sample < intervalEight:
            if cont8 < len(audio): #8
                loopHat.append(0)
            cont8 += 1
        elif sample >= intervalEight and sample < intervalNine:
            if cont9 < len(audio): #9
                loopHat.append(0)
            cont9 += 1
        elif sample >= intervalNine and sample < intervalTen:
            if cont10 < len(audio): #10
                loopHat.append(0)
            cont10 += 1
        elif sample >= intervalTen and sample < intervalEleven:
            if cont11 < len(audio): #11
                loopHat.append(0)
            cont11 += 1
        elif sample >= intervalEleven and sample < intervalDoce:
            if cont12 < len(audio): #12
                loopHat.append(audio[cont12])
            else:
                loopHat.append(0)
            cont12 += 1
        elif sample >= intervalDoce and sample < intervalTrece:
            if cont13 < len(audio): #13
                loopHat.append(0)
            cont13 += 1
        elif sample >= intervalTrece and sample < intervalCatorce:
            if cont14 < len(audio): #14
                loopHat.append(0)
            cont14 += 1
        elif sample >= intervalCatorce and sample < intervalQuince:
            if cont15 < len(audio): #15
                loopHat.append(audio[cont15])
            else:
                loopHat.append(0)
            cont15 += 1
        else:
            if cont16 < len(audio): #16
                loopHat.append(0)
            cont16 += 1

    compasCompleto = []
    for compas in range(inNumCompas):
        for sample in loopHat:
            compasCompleto.append(sample)

    #sf.write('../Results/LoopHatTwo.wav', compasCompleto, inSampleRate, 'PCM_24')

    #print("HIHAT LOOP CREADO")
    #print("-----------")

    return compasCompleto, inSampleRate, (len(compasCompleto) / inSampleRate)

#hat 1/8
def makeHatPatternOne(inAudio, inBPM, inNumCompas,inSampleRate):

    # Simple eight note [1/8] pattern
    audio = inAudio
    hatInterval = utilities.computeInterval(inBPM, inSampleRate)
    loopHat = []

    intervalOne = hatInterval/2
    intervalTwo = hatInterval
    intervalTres = hatInterval * 1.5
    intervalCuatro = hatInterval * 2
    intervalCinco = hatInterval * 2.5
    intervalSix = hatInterval * 3
    intervalSeven = hatInterval * 3.5
    intervalEight = hatInterval * 4

    cont, cont2, cont3, cont4, cont5, cont6, cont7, cont8 = 0, 0, 0, 0, 0, 0, 0, 0

    for sample in range(hatInterval * 4):
        if sample < intervalOne:
            if cont < len(audio):
                loopHat.append(audio[sample])
            else:
                loopHat.append(0)
            cont += 1
        elif sample >= intervalOne and sample < intervalTwo:
            if cont2 < len(audio):
                loopHat.append(audio[cont2])
            else:
                loopHat.append(0)
            cont2 += 1
        elif sample >= intervalTwo and sample < intervalTres:
            if cont3 < len(audio):
                loopHat.append(audio[cont3])
            else:
                loopHat.append(0)
            cont3 += 1
        elif sample >= intervalTres and sample < intervalCuatro:
            if cont4 < len(audio):
                loopHat.append(audio[cont4])
            else:
                loopHat.append(0)
            cont4 += 1
        elif sample >= intervalCuatro and sample < intervalCinco:
            if cont5 < len(audio):
                loopHat.append(audio[cont5])
            else:
                loopHat.append(0)
            cont5 += 1
        elif sample >= intervalCinco and sample < intervalSix:
            if cont6 < len(audio):
                loopHat.append(audio[cont6])
            else:
                loopHat.append(0)
            cont6 += 1
        elif sample >= intervalSix and sample < intervalSeven:
            if cont7 < len(audio):
                loopHat.append(audio[cont7])
            else:
                loopHat.append(0)
            cont7 += 1
        else:
            if cont8 < len(audio):
                loopHat.append(audio[cont8])
            else:
                loopHat.append(0)
            cont8 += 1

    compasCompleto = []
    for compas in range(inNumCompas):
        for sample in loopHat:
            compasCompleto.append(sample)

    #sf.write('../Results/LoopHatOne.wav', compasCompleto, inSampleRate, 'PCM_24')

    #print("HIHAT LOOP CREADO")
    #print("-----------")

    return compasCompleto, inSampleRate, (len(compasCompleto) / inSampleRate)

#hat 1/16
def makeHatPatternTwo(inAudio, inBPM, inNumCompas,inSampleRate):

    # Simple sixteenth note [1/16] pattern
    audio = inAudio
    hatInterval = utilities.computeInterval(inBPM, inSampleRate)
    loopHat = []

    intervalOne = hatInterval/4
    intervalTwo = hatInterval/2
    intervalTres = hatInterval * 0.75
    intervalCuatro = hatInterval
    intervalCinco = hatInterval * 1.25
    intervalSix = hatInterval * 1.5
    intervalSeven = hatInterval * 1.75
    intervalEight = hatInterval * 2
    intervalNine = hatInterval * 2.25
    intervalTen = hatInterval * 2.5
    intervalEleven = hatInterval * 2.75
    intervalDoce = hatInterval * 3
    intervalTrece = hatInterval * 3.25
    intervalCatorce = hatInterval * 3.5
    intervalQuince = hatInterval * 3.75

    cont, cont2, cont3, cont4, cont5, cont6, cont7, cont8 = 0, 0, 0, 0, 0, 0, 0, 0
    cont9, cont10, cont11, cont12, cont13, cont14, cont15, cont16 = 0, 0, 0, 0, 0, 0, 0, 0

    for sample in range(hatInterval * 4):
        if sample < intervalOne:
            if cont < len(audio):
                loopHat.append(audio[sample])
            else:
                loopHat.append(0)
            cont += 1
        elif sample >= intervalOne and sample < intervalTwo:
            if cont2 < len(audio):
                loopHat.append(audio[cont2])
            else:
                loopHat.append(0)
            cont2 += 1
        elif sample >= intervalTwo and sample < intervalTres:
            if cont3 < len(audio):
                loopHat.append(audio[cont3])
            else:
                loopHat.append(0)
            cont3 += 1
        elif sample >= intervalTres and sample < intervalCuatro:
            if cont4 < len(audio):
                loopHat.append(audio[cont4])
            else:
                loopHat.append(0)
            cont4 += 1
        elif sample >= intervalCuatro and sample < intervalCinco:
            if cont5 < len(audio):
                loopHat.append(audio[cont5])
            else:
                loopHat.append(0)
            cont5 += 1
        elif sample >= intervalCinco and sample < intervalSix:
            if cont6 < len(audio):
                loopHat.append(audio[cont6])
            else:
                loopHat.append(0)
            cont6 += 1
        elif sample >= intervalSix and sample < intervalSeven:
            if cont7 < len(audio):
                loopHat.append(audio[cont7])
            else:
                loopHat.append(0)
            cont7 += 1
        elif sample >= intervalSeven and sample < intervalEight:
            if cont8 < len(audio):
                loopHat.append(audio[cont8])
            else:
                loopHat.append(0)
            cont8 += 1
        elif sample >= intervalEight and sample < intervalNine:
            if cont9 < len(audio):
                loopHat.append(audio[cont9])
            else:
                loopHat.append(0)
            cont9 += 1
        elif sample >= intervalNine and sample < intervalTen:
            if cont10 < len(audio):
                loopHat.append(audio[cont10])
            else:
                loopHat.append(0)
            cont10 += 1
        elif sample >= intervalTen and sample < intervalEleven:
            if cont11 < len(audio):
                loopHat.append(audio[cont11])
            else:
                loopHat.append(0)
            cont11 += 1
        elif sample >= intervalEleven and sample < intervalDoce:
            if cont12 < len(audio):
                loopHat.append(audio[cont12])
            else:
                loopHat.append(0)
            cont12 += 1
        elif sample >= intervalDoce and sample < intervalTrece:
            if cont13 < len(audio):
                loopHat.append(audio[cont13])
            else:
                loopHat.append(0)
            cont13 += 1
        elif sample >= intervalTrece and sample < intervalCatorce:
            if cont14 < len(audio):
                loopHat.append(audio[cont14])
            else:
                loopHat.append(0)
            cont14 += 1
        elif sample >= intervalCatorce and sample < intervalQuince:
            if cont15 < len(audio):
                loopHat.append(audio[cont15])
            else:
                loopHat.append(0)
            cont15 += 1
        else:
            if cont16 < len(audio):
                loopHat.append(audio[cont16])
            else:
                loopHat.append(0)
            cont16 += 1

    compasCompleto = []
    for compas in range(inNumCompas):
        for sample in loopHat:
            compasCompleto.append(sample)

    #sf.write('../Results/LoopHatTwo.wav', compasCompleto, inSampleRate, 'PCM_24')

    #print("HIHAT LOOP CREADO")
    #print("-----------")

    return compasCompleto, inSampleRate, (len(compasCompleto) / inSampleRate)

#hat setback 1/8
def makeHatPatternThree(inAudio, inBPM, inNumCompas,inSampleRate):

    # Eight note [1/8] pattern with setback
    audio = inAudio
    hatInterval = utilities.computeInterval(inBPM, inSampleRate)
    loopHat = []

    intervalOne = hatInterval/2
    intervalTwo = hatInterval
    intervalTres = hatInterval * 1.5
    intervalCuatro = hatInterval * 2
    intervalCinco = hatInterval * 2.5
    intervalSix = hatInterval * 3
    intervalSeven = hatInterval * 3.5

    cont, cont2, cont3, cont4, cont5, cont6, cont7, cont8 = 0, 0, 0, 0, 0, 0, 0, 0

    for sample in range(hatInterval * 4):
        if sample < intervalOne:
            if cont < len(audio):
                loopHat.append(0)
            cont += 1
        elif sample >= intervalOne and sample < intervalTwo:
            if cont2 < len(audio):
                loopHat.append(audio[cont2])
            else:
                loopHat.append(0)
            cont2 += 1
        elif sample >= intervalTwo and sample < intervalTres:
            if cont3 < len(audio):
                loopHat.append(0)
            cont3 += 1
        elif sample >= intervalTres and sample < intervalCuatro:
            if cont4 < len(audio):
                loopHat.append(audio[cont4])
            else:
                loopHat.append(0)
            cont4 += 1
        elif sample >= intervalCuatro and sample < intervalCinco:
            if cont5 < len(audio):
                loopHat.append(0)
            cont5 += 1
        elif sample >= intervalCinco and sample < intervalSix:
            if cont6 < len(audio):
                loopHat.append(audio[cont6])
            else:
                loopHat.append(0)
            cont6 += 1
        elif sample >= intervalSix and sample < intervalSeven:
            if cont7 < len(audio):
                loopHat.append(0)
            cont7 += 1
        else:
            if cont8 < len(audio):
                loopHat.append(audio[cont8])
            else:
                loopHat.append(0)
            cont8 += 1

    compasCompleto = []
    for compas in range(inNumCompas):
        for sample in loopHat:
            compasCompleto.append(sample)

    #sf.write('../Results/LoopHatThree.wav', compasCompleto, inSampleRate, 'PCM_24')

    #print("HIHAT LOOP CREADO")
    #print("-----------")

    return compasCompleto, inSampleRate, (len(compasCompleto) / inSampleRate)