#!/usr/bin/env python3  

import rospy
import matplotlib.pyplot as plt
import numpy as np

def sortDataSet():
    dataset = {'dataset_1': 'cartographer', 'dataset_2': 'rtab'}
    datasetName = dataset.copy()
    datasetPath = {'dataset_1':'/home/russapat/obodroid_ws/src/rs_capture/text/no_human_2d_traj_221106_.txt', 
                    'dataset_2': '/home/russapat/obodroid_ws/src/rs_capture/text/global_poses_maxdept_7.txt'}
    # timeStamp = {'dataset_1': [], 'dataset_2': []}
    index = {'dataset_1': 0, 'dataset_2': 0}
    print('Dateset Name: ' + datasetName['dataset_1'])
    
    with open(datasetPath['dataset_1']) as dataset['dataset_1']:
        numlineDataset_1 = dataset['dataset_1'].readlines()
        datalenDataset_1 = len(numlineDataset_1)
        matrixDataset_1 = np.empty([datalenDataset_1,8])
        for line in numlineDataset_1:
            matrixDataset_1[index['dataset_1'],0] = line.split(' ')[0]        # Timestamp
            matrixDataset_1[index['dataset_1'],1] = line.split(' ')[1]        # X-position 
            matrixDataset_1[index['dataset_1'],2] = line.split(' ')[2]        # Y-position
            matrixDataset_1[index['dataset_1'],4] = line.split(' ')[4]        # quanternion
            matrixDataset_1[index['dataset_1'],5] = line.split(' ')[5]        # quanternion
            matrixDataset_1[index['dataset_1'],6] = line.split(' ')[6]        # quanternion
            matrixDataset_1[index['dataset_1'],7] = line.split(' ')[7]        # quanternion
            index['dataset_1'] += 1
        # print(matrixDataset_1)
        # print(datalenDataset_1)
        dataset['dataset_1'].close()

    with open(datasetPath['dataset_2']) as dataset['dataset_2']:
        numlineDataset_2 = dataset['dataset_2'].readlines()
        datalenDataset_2 = len(numlineDataset_2)
        matrixDataset_2 = np.empty([datalenDataset_2,8])
        for line in dataset['dataset_2'].readlines():
            matrixDataset_2[index['dataset_2'],0] = line.split(' ')[0]        # Timestamp
            matrixDataset_2[index['dataset_2'],1] = line.split(' ')[1]        # X-position 
            matrixDataset_2[index['dataset_2'],2] = line.split(' ')[2]        # Y-position
            matrixDataset_2[index['dataset_2'],4] = line.split(' ')[4]        # quanternion
            matrixDataset_2[index['dataset_2'],5] = line.split(' ')[5]        # quanternion
            matrixDataset_2[index['dataset_2'],6] = line.split(' ')[6]        # quanternion
            matrixDataset_2[index['dataset_2'],7] = line.split(' ')[7]        # quanternion
            index['dataset_2'] += 1
        dataset['dataset_2'].close()
        print(matrixDataset_2)
        print(datalenDataset_2)


sortDataSet()

