#
#   Crawler routines for SLAC/XTC
#   Tested using Anaconda / Python 3.4
#

import sys
import os
import glob
import csv
import lib.cfel_filetools as cfel_file



def crawler_merge():

    #
    #   Read .csv files
    #
    data = cfel_file.csv_to_dict('data_status.csv')
    #run,status

    cheetah = cfel_file.csv_to_dict('cheetah_status.csv')
    #run,status,directory,processed,hits,hitrate%

    datasets = cfel_file.csv_to_dict('datasets.txt')
    #Run, DatasetID, Directory

    # Check for missing data
    if data=={} or cheetah=={} or datasets=={}:
        return



    #
    # Compatibility: convert r0002 (string) to 2 (integer) so that run is in the same format in each dict
    #   This may disappear later if datasets['run'] is in the same format
    #
    for i, run in enumerate(data['run']):
        run_num= int(run[1:])
        data['run'][i] = run_num

    for i, run in enumerate(cheetah['run']):
        run_num = int(run[1:])
        cheetah['run'][i] = run_num

    for i, run in enumerate(datasets['# Run']):
        run_num = int(run[1:])
        datasets['# Run'][i] = run_num

    print(datasets.keys())

    #print(data['run'])
    #print(datasets['# Run'])

    # Find unique run numbers
    # (some runs may be missing from some of the tables)
    all_runs = data['run'] + cheetah['run'] + datasets['# Run']
    uniq_runs = list(sorted(set(all_runs)))
    #print(uniq_runs)


    # Output should be:
    # Run, Dataset, XTC, Cheetah, CrystFEL, H5 Directory, Nprocessed, Nhits, Nindex, Hitrate%
    run_out = []
    dataset_out = []
    datastatus_out = []
    cheetahstatus_out = []
    crystfel_out = []
    h5dir_out = []
    nprocessed_out = []
    nhits_out = []
    nindexed_out = []
    hitrate_out = []


    #
    # Loop through all possible runs and collate information
    #   being sensible when data is not in one of the other files
    #
    for run in uniq_runs:

        # Stuff contained in XTC info
        # run,status
        datastatus = '---'
        if run in data['run']:
            i = data['run'].index(run)
            datastatus = data['status'][i]


        # Stuff contained in datasets file
        # Run, DatasetID, Directory
        dataset = '---'
        h5dir = '---'
        if run in datasets['# Run']:
            i = datasets['# Run'].index(run)
            dataset = datasets[' DatasetID'][i].strip()
            h5dir = datasets[' Directory'][i].strip()


        # Stuff contained in Cheetah status file
        # Match on dataset directory (to handle one run having multiple output directories)
        # Check run numbers match to guard against matching '---' entries
        # run,status,directory,processed,hits,hitrate%
        cheetahstatus = '---'
        nprocessed = '---'
        nhits = '---'
        hitrate = '---'
        if h5dir in cheetah['directory']:
            i = cheetah['directory'].index(h5dir)
            if cheetah['run'][i] == run:
                cheetahstatus = cheetah['status'][i].strip()
                nprocessed = cheetah['processed'][i].strip()
                nhits = cheetah['hits'][i].strip()
                hitrate = cheetah['hitrate%'][i].strip()
                if hitrate.replace('.','',1).isnumeric():
                    hitrate = '{:0.2f}'.format(float(hitrate))
            else:
                print(cheetah['run'][i], run)


        # CrystFEL stuff is not yet included
        crystfel_status = '---'
        nindexed = '---'


        # Concatenate info for this run into output list
        run_out.append(run)
        datastatus_out.append(datastatus)
        dataset_out.append(dataset)
        h5dir_out.append(h5dir)
        cheetahstatus_out.append(cheetahstatus)
        nprocessed_out.append(nprocessed)
        nhits_out.append(nhits)
        hitrate_out.append(hitrate)
        crystfel_out.append(crystfel_status)
        nindexed_out.append(nindexed)


    #
    # Output should be:
    # Run, Dataset, XTC, Cheetah, CrystFEL, H5 Directory, , Nhits, Nindex, Hitrate%
    #
    result = {
        'Run' : run_out,
        'Dataset' : dataset_out,
        'XTC' : datastatus_out,
        'Cheetah' : cheetahstatus_out,
        'CrystFEL' : crystfel_out,
        'H5Directory' : h5dir_out,
        'Nprocessed' : nprocessed_out,
        'Nhits' : nhits_out,
        'Nindex' : nindexed_out,
        'Hitrate%' : hitrate_out
    }


    # Write dict to CSV file
    keys_to_save = ['Run', 'Dataset','XTC','Cheetah','CrystFEL','H5Directory','Nprocessed','Nhits','Nindex','Hitrate%']
    cfel_file.dict_to_csv('crawler.csv', result, keys_to_save)




#
#   Help snippets
#
    #if 'your_element' in mylist:
    #    print
    #    mylist.index('your_element')
    #else:
    #    print
    #    None

