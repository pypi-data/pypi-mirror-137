from __future__ import division
import os
import numpy as np
from configparser import ConfigParser, NoSectionError, NoOptionError
import glob
from simba.rw_dfs import *
from shapely.geometry import Point, Polygon
from datetime import datetime
from simba.drop_bp_cords import get_fn_ext
from simba.features_scripts.unit_tests import read_video_info
from simba.misc_tools import check_directionality_viable
from shapely.geometry import Point
from shapely import geometry
from copy import deepcopy


# inifile = r"Z:\DeepLabCut\DLC_extract\Troubleshooting\ROI_2_animals\project_folder\project_config.ini"
# videoFileName = "Video10.mp4"

def ROItoFeatures(inifile):
    dateTime = datetime.now().strftime('%Y%m%d%H%M%S')
    config = ConfigParser()
    config.read(inifile)
    noAnimals = config.getint('ROI settings', 'no_of_animals')
    try:
        wfileType = config.get('General settings', 'workflow_file_type')
    except NoOptionError:
        wfileType = 'csv'
    csv_dir = config.get('General settings', 'csv_path')
    csv_dir_in = os.path.join(csv_dir, 'features_extracted')
    vidInfPath = config.get('General settings', 'project_path')
    logFolderPath = os.path.join(vidInfPath, 'logs')
    vidInfPath = os.path.join(logFolderPath, 'video_info.csv')
    vidinfDf = pd.read_csv(vidInfPath)
    vidinfDf["Video"] = vidinfDf["Video"].astype(str)
    try:
        multiAnimalIDList = config.get('Multi animal IDs', 'id_list')
        multiAnimalIDList = multiAnimalIDList.split(",")
        if multiAnimalIDList[0] != '':
            multiAnimalStatus = True
            print('Applying settings for multi-animal tracking...')
        else:
            multiAnimalStatus = False
            for animal in range(noAnimals):
                multiAnimalIDList.append('Animal_' + str(animal + 1) + '_')
            print('Applying settings for classical tracking...')
    except NoSectionError:
        multiAnimalIDList = []
        for animal in range(noAnimals):
            multiAnimalIDList.append('Animal_' + str(animal + 1) + '_')
        multiAnimalStatus = False
        print('Applying settings for classical tracking...')

    multiAnimalIDList = [x for x in multiAnimalIDList if x]
    trackedBodyParts = []
    for currAnimal in range(1,noAnimals+1):
        trackedBodyParts.append(config.get('ROI settings', 'animal_' + str(currAnimal) + '_bp'))

    trackedBodyParts = [(x + '_x', x + '_y') for x in trackedBodyParts]
    ROIcoordinatesPath = os.path.join(logFolderPath, 'measures', 'ROI_definitions.h5')
    rectanglesInfo = pd.read_hdf(ROIcoordinatesPath, key='rectangles')
    circleInfo = pd.read_hdf(ROIcoordinatesPath, key='circleDf')
    polygonInfo = pd.read_hdf(ROIcoordinatesPath, key='polygons')

    def line_length(p, q, n, M, coord):
        Px, Py = np.abs(p[0] - M[0]), np.abs(p[1] - M[1])
        Qx, Qy = np.abs(q[0] - M[0]), np.abs(q[1] - M[1])
        Nx, Ny = np.abs(n[0] - M[0]), np.abs(n[1] - M[1])
        Ph = np.sqrt(Px*Px + Py*Py)
        Qh = np.sqrt(Qx*Qx + Qy*Qy)
        Nh = np.sqrt(Nx*Nx + Ny*Ny)
        if (Nh < Ph and Nh < Qh and Qh < Ph):
            coord.extend((q[0], q[1]))
            return True, coord
        elif (Nh < Ph and Nh < Qh and Ph < Qh):
            coord.extend((p[0], p[1]))
            return True, coord
        else:
            return False, coord

    filesFound = glob.glob(csv_dir_in + '/*.' + wfileType)
    if len(filesFound) == 0:
        print('No feature-files found. Please extract features before appending ROI-features.')

    print('Extracting ROI features from ' + str(len(filesFound)) + ' files...')
    print('Please be patient, code is not optimized...')
    summary_df_list = []
    for currFile in filesFound:
        dir_name, CurrentVideoName, ext = get_fn_ext(currFile)
        CurrVidFn = CurrentVideoName + ext
        print('Analyzing ROI features for ' + CurrentVideoName + '...')
        Rectangles = (rectanglesInfo.loc[rectanglesInfo['Video'] == str(CurrentVideoName)])
        Circles = (circleInfo.loc[circleInfo['Video'] == str(CurrentVideoName)])
        Polygons = (polygonInfo.loc[polygonInfo['Video'] == str(CurrentVideoName)])
        currVideoSettings, currPixPerMM, fps = read_video_info(vidinfDf, CurrentVideoName)
        currDfPath = os.path.join(csv_dir_in, CurrVidFn)
        currDf = read_df(currDfPath, wfileType)
        currDf = currDf.fillna(0)
        currDf = currDf.apply(pd.to_numeric).reset_index(drop=True)
        currDf = currDf.loc[:, ~currDf.columns.str.contains('^Unnamed')]

        col_headers_lower_case = [x.lower() for x in list(currDf.columns)]

        directionalitySetting, NoseCords, EarLeftCoords, EarRightCoords = check_directionality_viable(noAnimals, col_headers_lower_case)

        NoseCords = [NoseCords[i * 2:(i + 1) * 2] for i in range((len(NoseCords) + 2 - 1) // 2 )]
        EarLeftCoords = [EarLeftCoords[i * 2:(i + 1) * 2] for i in range((len(EarLeftCoords) + 2 - 1) // 2)]
        EarRightCoords = [EarRightCoords[i * 2:(i + 1) * 2] for i in range((len(EarRightCoords) + 2 - 1) // 2)]

        #### FEATURES COLUMNS AND NUMPY ARRAYS WITH COORDINATES######
        rectangleFeatures = np.array([0]*5)
        Rectangle_col_inside_value, Rectangle_col_distance, Rectangle_col_facing = [], [], []
        for rectangle in range(len(Rectangles)):
            for bodypart in range(len(trackedBodyParts)):
                ROI_col_name = str(Rectangles['Name'].iloc[rectangle] + '_' + multiAnimalIDList[bodypart] + 'in_zone')
                Rectangle_col_inside_value.append(ROI_col_name)
                currDf[ROI_col_name] = 0
                ROI_col_name = str(Rectangles['Name'].iloc[rectangle] + '_' + multiAnimalIDList[bodypart] + 'distance')
                currDf[ROI_col_name] = 0
                Rectangle_col_distance.append(ROI_col_name)
                if directionalitySetting:
                    ROI_col_name = str(Rectangles['Name'].iloc[rectangle] + '_' + multiAnimalIDList[bodypart] + 'facing')
                    currDf[ROI_col_name] = 0
                    Rectangle_col_facing.append(ROI_col_name)
            rectangleArray = np.array([Rectangles['Name'].iloc[rectangle], Rectangles['topLeftX'].iloc[rectangle], Rectangles['topLeftY'].iloc[rectangle], Rectangles['topLeftX'].iloc[rectangle] + Rectangles['width'].iloc[rectangle], Rectangles['topLeftY'].iloc[rectangle] + Rectangles['height'].iloc[rectangle]])
            rectangleFeatures = np.vstack((rectangleFeatures, rectangleArray))
        rectangleFeatures = np.delete(rectangleFeatures, 0, 0)

        circleFeatures = np.array([0] * 4)
        circle_col_inside_value, circle_col_distance, circle_col_facing = [], [], []
        for circle in range(len(Circles)):
            for bodypart in range(len(trackedBodyParts)):
                ROI_col_name = str(Circles['Name'].iloc[circle] + '_' + multiAnimalIDList[bodypart] + 'in_zone')
                circle_col_inside_value.append(ROI_col_name)
                currDf[ROI_col_name] = 0
                ROI_col_name = str(Circles['Name'].iloc[circle] + '_' + multiAnimalIDList[bodypart] + 'distance')
                currDf[ROI_col_name] = 0
                circle_col_distance.append(ROI_col_name)
                if directionalitySetting:
                    ROI_col_name = str(Circles['Name'].iloc[circle] + '_' + multiAnimalIDList[bodypart] + 'facing')
                    currDf[ROI_col_name] = 0
                    circle_col_facing.append(ROI_col_name)
            circleArray = np.array([Circles['Name'].iloc[circle], Circles['centerX'].iloc[circle], Circles['centerY'].iloc[circle], Circles['radius'].iloc[circle]])
            circleFeatures = np.vstack((circleFeatures, circleArray))
        circleFeatures = np.delete(circleFeatures, 0, 0)

        polygonFeatures = np.array([0] * 2)
        polygon_col_inside_value, polygon_col_distance, polygon_col_facing = [], [], []
        for polygon in range(len(Polygons)):
            for bodypart in range(len(trackedBodyParts)):
                ROI_col_name = str(Polygons['Name'].iloc[polygon] + '_' + multiAnimalIDList[bodypart] + 'in_zone')
                polygon_col_inside_value.append(ROI_col_name)
                currDf[ROI_col_name] = 0
                ROI_col_name = str(Polygons['Name'].iloc[polygon] + '_' + multiAnimalIDList[bodypart] + 'distance')
                currDf[ROI_col_name] = 0
                polygon_col_distance.append(ROI_col_name)
                if directionalitySetting:
                    ROI_col_name = str(Polygons['Name'].iloc[polygon] + '_' + multiAnimalIDList[bodypart] + 'facing')
                    currDf[ROI_col_name] = 0
                    polygon_col_facing.append(ROI_col_name)
            polygonArray = np.array([Polygons['Name'].iloc[polygon], Polygons['vertices'].iloc[polygon]])
            polygonFeatures = np.vstack((polygonFeatures, polygonArray))
        polygonFeatures = np.delete(polygonFeatures, 0, 0)

        ### CALUCLATE BOOLEAN, IF ANIMAL IS IN RECTANGLES, CIRCLES, OR POLYGONS
        for index, row in currDf.iterrows():
            loop = 0
            for rectangle in range(len(Rectangles)):
                for bodyparts in range(len(trackedBodyParts)):
                    currROIColName = Rectangle_col_inside_value[loop]
                    loop+=1
                    if ((((int(rectangleFeatures[rectangle, 1]) - 10) <= row[trackedBodyParts[bodyparts][0]] <= (int(rectangleFeatures[rectangle, 3]) + 10))) and (((int(rectangleFeatures[rectangle, 2]) - 10) <= row[trackedBodyParts[bodyparts][1]] <= (int(rectangleFeatures[rectangle, 4]) + 10)))):
                        currDf.loc[index, currROIColName] = 1
            for column in Rectangle_col_inside_value:
                colName1 = str(column) + '_cumulative_time'
                currDf[colName1] = currDf[column].cumsum() * float(1/fps)
                colName2 = str(column) + '_cumulative_percent'
                currDf[colName2] = currDf[colName1]/currDf.index

            loop = 0
            for circles in range(len(Circles)):
                for bodyparts in range(len(trackedBodyParts)):
                    currROIColName = circle_col_inside_value[loop]
                    loop+=1
                    euclidPxDistance = np.sqrt((int(row[trackedBodyParts[bodyparts][0]]) - int(circleFeatures[circle, 1])) ** 2 + ((int(row[trackedBodyParts[bodyparts][1]]) - int(circleFeatures[circle, 2])) ** 2))
                    if euclidPxDistance <= int(circleFeatures[circle, 3]):
                        currDf.loc[index, currROIColName] = 1
            for column in circle_col_inside_value:
                colName1 = str(column) + '_cumulative_time'
                currDf[colName1] = currDf[column].cumsum() * float(1 / fps)
                colName2 = str(column) + '_cumulative_percent'
                currDf[colName2] = currDf[colName1] / currDf.index

            loop = 0
            for polyGon in range(len(Polygons)):
                currPolyGon = Polygon(polygonFeatures[0, 1])
                for bodyparts in range(len(trackedBodyParts)):
                    currROIColName = polygon_col_inside_value[loop]
                    loop += 1
                    currBpLoc = Point(row[trackedBodyParts[bodyparts][0]], row[trackedBodyParts[bodyparts][1]])
                    PolyGonCheck = (currPolyGon.contains(currBpLoc))
                    if PolyGonCheck == True:
                        currDf.loc[index, currROIColName] = 1

            for column in polygon_col_inside_value:
                colName1 = str(column) + '_cumulative_time'
                currDf[colName1] = currDf[column].cumsum() * float(1 / fps)
                colName2 = str(column) + '_cumulative_percent'
                currDf[colName2] = currDf[colName1] / currDf.index

        ### CALUCLATE DISTANCE TO CENTER OF EACH RECTANGLE AND CIRCLES
        for index, row in currDf.iterrows():
            loop = 0
            for rectangle in range(len(Rectangles)):
                currRecCenter = [(int(rectangleFeatures[rectangle, 1]) + int(rectangleFeatures[rectangle, 3])) / 2, (int(rectangleFeatures[rectangle, 2]) + int(rectangleFeatures[rectangle, 4])) / 2 ]
                for bodyparts in range(len(trackedBodyParts)):
                    currROIColName = Rectangle_col_distance[loop]
                    currDf.loc[index, currROIColName] = (np.sqrt((row[trackedBodyParts[bodyparts][0]] - currRecCenter[0]) ** 2 + (row[trackedBodyParts[bodyparts][1]] - currRecCenter[1]) ** 2)) / currPixPerMM
                    loop += 1
            loop = 0
            for circle in range(len(Circles)):
                currCircleCenterX, currCircleCenterY = (int(circleFeatures[circle, 1]), int(circleFeatures[circle, 2]))
                for bodyparts in range(len(trackedBodyParts)):
                    currROIColName = circle_col_distance[loop]
                    currDf.loc[index, currROIColName] = (np.sqrt((int(row[trackedBodyParts[bodyparts][0]]) - currCircleCenterX) ** 2 + (int(row[trackedBodyParts[bodyparts][1]]) - currCircleCenterY) ** 2)) / currPixPerMM
                    loop += 1

            loop = 0
            polygonCenterCord = np.array([0] * 2)
            for polygon in range(len(Polygons)):
                CurrVertices = polygonFeatures[polygon, 1]
                CurrVertices = np.array(CurrVertices, np.int32)
                pointList = []
                for i in CurrVertices:
                    point = geometry.Point(i)
                    pointList.append(point)
                polyGon = geometry.Polygon([[p.x, p.y] for p in pointList])
                polyGonCenter = polyGon.centroid.wkt
                polyGonCenter = polyGonCenter.replace("POINT", '')
                polyGonCenter = polyGonCenter.replace("(", '')
                polyGonCenter = polyGonCenter.replace(")", '')
                polyGonCenter = polyGonCenter.split(" ", 3)
                polyGonCenter = polyGonCenter[1:3]
                polyGonCenter = [float(i) for i in polyGonCenter]
                polyGonCenterX, polyGonCenterY = polyGonCenter[0], polyGonCenter[1]
                polyArray = np.array([polyGonCenterX, polyGonCenterY])
                polygonCenterCord = np.vstack((polygonCenterCord, polyArray))
                for bodyparts in range(len(trackedBodyParts)):
                    currROIColName = polygon_col_distance[loop]
                    currDf.loc[index, currROIColName] = (np.sqrt((int(row[trackedBodyParts[bodyparts][0]]) - polyGonCenterX) ** 2 + (int(row[trackedBodyParts[bodyparts][1]]) - polyGonCenterY) ** 2)) / currPixPerMM
                    loop += 1
            polygonCenterCord = np.delete(polygonCenterCord, 0, 0)

        ### CALCULATE IF ANIMAL IS DIRECTING TOWARDS THE CENTER OF THE RECTANGLES AND CIRCLES
        if directionalitySetting:
            directionality_df = deepcopy(currDf)
            directionality_df.columns = [x.lower() for x in directionality_df.columns]
            for index, row in directionality_df.iterrows():
                loop = 0

                for rectangle in range(len(Rectangles)):
                    for bodyparts in range(len(trackedBodyParts)):
                        p, q, n, m, coord = ([] for i in range(5))
                        currROIColName = Rectangle_col_facing[loop].lower()
                        p.extend((row[EarLeftCoords[bodyparts][0]], row[EarLeftCoords[bodyparts][1]]))
                        q.extend((row[EarRightCoords[bodyparts][0]], row[EarRightCoords[bodyparts][1]]))
                        n.extend((row[NoseCords[bodyparts][0]], row[NoseCords[bodyparts][1]]))
                        m.extend(((int(rectangleFeatures[rectangle, 1]) + int(rectangleFeatures[rectangle, 3])) / 2, (int(rectangleFeatures[rectangle, 2]) + int(rectangleFeatures[rectangle, 4])) / 2 ))
                        center_facing_check = line_length(p, q, n, m, coord)
                        if center_facing_check[0] == True:
                            directionality_df.loc[index, currROIColName] = 1
                        else:
                            directionality_df.loc[index, currROIColName] = 0
                        loop += 1

                loop = 0
                for circle in range(len(Circles)):
                    for bodyparts in range(len(trackedBodyParts)):
                        p, q, n, m, coord = ([] for i in range(5))
                        currROIColName = circle_col_facing[loop].lower()
                        p.extend((row[EarLeftCoords[bodyparts][0]], row[EarLeftCoords[bodyparts][1]]))
                        q.extend((row[EarRightCoords[bodyparts][0]], row[EarRightCoords[bodyparts][1]]))
                        n.extend((row[NoseCords[bodyparts][0]], row[NoseCords[bodyparts][1]]))
                        m.extend((int(circleFeatures[circle, 1]), int(circleFeatures[circle, 2])))
                        center_facing_check = line_length(p, q, n, m, coord)
                        if center_facing_check[0] == True:
                            directionality_df.loc[index, currROIColName] = 1
                        else:
                            directionality_df.loc[index, currROIColName] = 0
                        loop += 1

                loop = 0
                for polygon in range(len(Polygons)):
                    for bodyparts in range(len(trackedBodyParts)):
                        p, q, n, m, coord = ([] for i in range(5))
                        currROIColName = polygon_col_facing[loop].lower()
                        p.extend((row[EarLeftCoords[bodyparts][0]], row[EarLeftCoords[bodyparts][1]]))
                        q.extend((row[EarRightCoords[bodyparts][0]], row[EarRightCoords[bodyparts][1]]))
                        n.extend((row[NoseCords[bodyparts][0]], row[NoseCords[bodyparts][1]]))
                        m.extend((int(polygonCenterCord[polygon][0]), int(polygonCenterCord[polygon][1])))
                        center_facing_check = line_length(p, q, n, m, coord)
                        if center_facing_check[0] == True:
                            directionality_df.loc[index, currROIColName] = 1
                        else:
                            directionality_df.loc[index, currROIColName] = 0
                        loop += 1

            directionality_df.columns = currDf.columns
            currDf = directionality_df


        currDf = currDf.fillna(0)
        currDf = currDf.replace(np.inf, 0)
        save_df(currDf, wfileType, currFile)
        print('New feature file with ROI data saved: ' + str(r'project_folder\csv\features_extracted') + str(r'\\') + str(CurrVidFn))

        distance_facing_list, header_list = [], ['Video']
        for distance_col in Rectangle_col_distance:
            distance_facing_list.append(currDf[distance_col].mean())
            header_list.append(distance_col + '_mean_mm')
        for distance_col in circle_col_distance:
            distance_facing_list.append(currDf[distance_col].mean())
            header_list.append(distance_col + '_mean_mm')
        for facing_col in Rectangle_col_facing:
            distance_facing_list.append(currDf[facing_col].sum() / fps)
            header_list.append(facing_col + '_sum_(s)')
        for facing_col in circle_col_facing:
            distance_facing_list.append(currDf[facing_col].sum() / fps)
            header_list.append(facing_col + '_sum_(s)')
        distance_facing_list.insert(0, CurrentVideoName)
        summary_df_list.append(pd.DataFrame([distance_facing_list], columns=header_list))
    try:
        summary_df_out = pd.concat(summary_df_list, axis=0)
    except FutureWarning:
        print('WARNING: Not all of your videos have defined ROIs. Please define ROIs for all videos')

    tmp = summary_df_out.select_dtypes(include=[np.number])
    summary_df_out.loc[:, tmp.columns] = np.round(tmp, decimals=2)

    summary_file_name = os.path.join(logFolderPath, 'ROI_features_summary_' + str(dateTime) + '.csv')
    summary_df_out.to_csv(summary_file_name, index=False)
    print('Summary file containing the mean distances between the animal and ROI centroids in the video, and the total (sum) seconds directing towards each ROI for each animal in each video is saved @' + str(summary_file_name))
    print('COMPLETE: All ROI feature data appended to feature files. The new features can be found as the last columns in the CSV (or parquet) files inside the project-folder/csv/features_extracted directory.')
