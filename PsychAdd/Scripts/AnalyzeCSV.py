import pandas as pd
import numpy as np
import subprocess
import os.path

def read_csv(file):
    df = pd.read_csv(file)
    return df

def get_headers(df):
    column_list = []
    column_headers = df.columns
    for i in column_headers:
        column_list.append(i)
    return column_list

#Find the 5 or t to then find the start time of fMRI Test
def get_start_time(df):
    found = False
    starting_time = -1
    for i in enumerate(df.iloc[0]):
        if found == True:
            starting_time = i[1]
            break
        if i[1] == 5.0 or i[1] == "t":
            found = True
    return starting_time

#Connect Column headers to the data they represent in a dictionary
def create_data_dictionary(df, data_labels):
    #Attach column headers to column data
    data_dict = {}
    for label in data_labels:
        data_dict[label] = pd.Series(df[label])
    return data_dict

#Removes data labels of data that is made up of strings
def remove_string_data(data_labels, data_dict):
    strings = []
    for label in data_labels:
        for ind in range(len(data_dict[label])):
            if type(data_dict[label][ind]) == str:
                strings.append(label)
                break

    for string in strings:
        data_labels.remove(string)

    return data_labels

#Doesn't Quite Work the way I want it to
def determine_start_data(Onset_Data_Labels, data_dict):
    combined_list = [0] * len(data_dict[Onset_Data_Labels[0]])
    for name in Onset_Data_Labels:
        if "start" not in name.lower():
            for j in range(len(data_dict[name])):
                if (np.isnan(data_dict[name][j]) == False):
                    combined_list[j] += data_dict[name][j]
                else:
                    pass
    # Remove 0's aka nans from culiminated data list
    counter = 0
    length = len(combined_list)
    while (counter < length):
        if (combined_list[counter] == 0):
            combined_list.remove(combined_list[counter])
            length -= 1
            continue
        counter +=1

    for index in range(len(Onset_Data_Labels)):
        if "start" in Onset_Data_Labels[index].lower():
            return (index,combined_list)

    return -1

def create_onset_file(Onset_Data_Labels, data_dict, start_time, num = 0):
    start_ind = determine_start_data(Onset_Data_Labels, data_dict)

    if start_ind == -1:
        return -1
    #ind = len( Onset_Data_Labels[start_ind[0]])
    onset = Onset_Data_Labels[start_ind[0]].replace("Start", "")
    path_add = "Onset_Files/"
    #onset_name = Onset_Data_Labels[start_ind[0]][0:ind] + ".txt"
    if num == 0:
        onset_name = os.path.join(path_add, onset+ ".txt")
    else:
        onset_name = os.path.join(path_add, onset +str(num) + ".txt")
    f = open(onset_name, "w")
    count = 0
    for ind in range(len(data_dict[Onset_Data_Labels[start_ind[0]]])):
        if (np.isnan(data_dict[Onset_Data_Labels[start_ind[0]]][ind]) == False):
            f.write(str(data_dict[Onset_Data_Labels[start_ind[0]]][ind] - start_time) + ", ")
            f.write(str(start_ind[1][count]) + ", 1\n")
            count+=1
    f.close()

    return 0

def get_paths_BIDS(file_path):

    path_list = []
    path_split = file_path.split("\\")
    file_name = path_split[len(path_split)-1]
    inner_directory = path_split[len(path_split)-2]
    subject_name = (path_split[len(path_split) - 3])
    path_split.remove(path_split[len(path_split) - 1])
    path_split.remove(path_split[len(path_split) - 1])
    path_split.remove(path_split[len(path_split) - 1])
    sub_list = []
    file_name_list = file_name.split("_")
    file_name_beginning = file_name_list[0]
    file_name_repeat = file_name_beginning.split("-")[0]
    file_name_list.remove(file_name_list[0])
    base_path = "\\".join(path_split)

    sub_count = len([name for name in os.listdir(base_path)])-1
    for i in range(1,sub_count+1):
        if i < 10:
            sub_list.append(file_name_repeat+ "-0"+str(i))
        else:
            sub_list.append(file_name_repeat+ "-"+str(i))


    for sub in sub_list:
        file_name = "_".join(file_name_list)
        file_name = sub+"_" + file_name
        path_list.append(base_path + "\\" + sub + "\\"+inner_directory + "\\" + file_name)

    return path_list

def create_Time_Series():
    pass