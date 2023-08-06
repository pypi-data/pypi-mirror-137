





def check_directionality_viable(noAnimals, col_headers_lower_case):
    directionalitySetting = True

    if noAnimals > 1:
        NoseCoords = []
        EarLeftCoords = []
        EarRightCoords = []
        for animal in range(noAnimals):
            possible_NoseCoords = ['nose_' + str(animal + 1) + '_x', 'nose_' + str(animal + 1) + '_y']
            possible_EarLeftCoords = ['ear_left_' + str(animal + 1) + '_x', 'ear_left_' + str(animal + 1) + '_y']
            possible_EarRightCoords = ['ear_right_' + str(animal + 1) + '_x', 'ear_right_' + str(animal + 1) + '_y']
            directionalityCordHeaders = possible_NoseCoords + possible_EarLeftCoords + possible_EarRightCoords
            if not set(directionalityCordHeaders).issubset(col_headers_lower_case):
                possible_EarLeftCoords = ['left_ear_' + str(animal + 1) + '_x', 'left_ear_' + str(animal + 1) + '_y']
                possible_EarRightCoords = ['right_ear' + str(animal + 1) + '_x', 'right_ear_' + str(animal + 1) + '_y']
                directionalityCordHeaders = possible_NoseCoords + possible_EarLeftCoords + possible_EarRightCoords
                if not set(directionalityCordHeaders).issubset(col_headers_lower_case):
                    return False, NoseCoords, EarLeftCoords, EarRightCoords
                else:
                    NoseCoords.extend((possible_NoseCoords))
                    EarLeftCoords.extend((possible_EarLeftCoords))
                    EarRightCoords.extend((possible_EarRightCoords))
            else:
                NoseCoords.extend((possible_NoseCoords))
                EarLeftCoords.extend((possible_EarLeftCoords))
                EarRightCoords.extend((possible_EarRightCoords))

    else:
        NoseCoords = ['nose_x', 'nose_y']
        EarLeftCoords = ['ear_left_x', 'ear_left_y']
        EarRightCoords = ['ear_right_x', 'ear_right_y']
        directionalityCordHeaders = NoseCoords + EarLeftCoords + EarRightCoords
        if not set(directionalityCordHeaders).issubset(col_headers_lower_case):
            EarLeftCoords = ['left_ear_x', 'left_ear_y']
            EarRightCoords = ['right_ear_x', 'right_ear_y']
            directionalityCordHeaders = NoseCoords + EarLeftCoords + EarRightCoords
            if not set(directionalityCordHeaders).issubset(col_headers_lower_case):
                return False, NoseCoords, EarLeftCoords, EarRightCoords


    return directionalitySetting, NoseCoords, EarLeftCoords, EarRightCoords