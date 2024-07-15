# take 'iam_ondb_home' and reformat the directories
import os
import shutil

base_dir = '../iam_ondb_home'

# get all the directories (excluding the files)
directories = os.listdir(base_dir)
# remove the files
directories = [directory for directory in directories if os.path.isdir(f'{base_dir}/{directory}')]

for directory in directories:
    # # flatten all the subdirectories
    # subdirs = os.listdir(f'{base_dir}/{directory}')
    # # create a single subdirectory
    # os.makedirs(f'{base_dir}/{directory}/{directory.split("-")[0]}')
    # for subdir in subdirs:
    #     files = os.listdir(f'{base_dir}/{directory}/{subdir}')
    #     for file in files:
    #         # move the files to the single subdirectory
    #         shutil.move(f'{base_dir}/{directory}/{subdir}/{file}', f'{base_dir}/{directory}/{directory.split("-")[0]}/{file}')
    #     # remove the subdirectory
    #     os.rmdir(f'{base_dir}/{directory}/{subdir}')
    #
    # now flatten subdirectories
    for file in os.listdir(f'{base_dir}/{directory}/{directory.split("-")[0]}'):
        for subdir in os.listdir(f'{base_dir}/{directory}/{directory.split("-")[0]}/{file}'):
            # move the files to the main directory
            shutil.move(f'{base_dir}/{directory}/{directory.split("-")[0]}/{file}/{subdir}', f'{base_dir}/{directory}/{directory.split("-")[0]}/{file}')




