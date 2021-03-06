import pandas as pd
import numpy as np
import subprocess
import fileinput
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

#Split path into all of its parts
def splitall(path):
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])
    return allparts


def listdir_nohidden(path):
    listdir = []
    for f in os.listdir(path):
        if not f.startswith('.'):
            listdir.append(f)
    return listdir

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

def create_onset_file(Onset_Data_Labels, data_dict, start_time, directory= "0", num = 0):
    start_ind = determine_start_data(Onset_Data_Labels, data_dict)

    if start_ind == -1:
        return -1
    #ind = len( Onset_Data_Labels[start_ind[0]])
    onset = Onset_Data_Labels[start_ind[0]].replace("Start", "")
    #onset_name = Onset_Data_Labels[start_ind[0]][0:ind] + ".txt"
    if num == 0:
        onset_name = os.path.join("Scripts", "Onset_Files", onset+ ".txt")
    else:
        if directory != "0":
            onset_name = os.path.join("Scripts", "Onset_Files", directory, onset +str(num) + ".txt")
        else:
            onset_name = os.path.join("Scripts", "Onset_Files", onset + str(num) + ".txt")
    f = open(onset_name, "w")
    count = 0
    for ind in range(len(data_dict[Onset_Data_Labels[start_ind[0]]])):
        if (np.isnan(data_dict[Onset_Data_Labels[start_ind[0]]][ind]) == False):
            f.write(str(data_dict[Onset_Data_Labels[start_ind[0]]][ind] - start_time) + " ")
            f.write(str(start_ind[1][count]) + " 1\n")
            count+=1
    f.close()

    return 0

def get_all_CSV(file_path):
    direct = os.path.dirname(file_path)
    csv_list= [x for x in os.listdir(direct) if x.endswith('.csv')]
    full_paths_csv = []
    for i in csv_list:
        path = os.path.join(direct, i)
        full_paths_csv.append(path)
    full_paths_csv.sort()
    return full_paths_csv

def get_paths_BIDS(file_path):
    path_list = []
    path_split = splitall(file_path)
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
    base_path = os.path.join(*path_split)

    sub_count = len([name for name in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, name)) and name != "derivatives"])
    for i in range(1,sub_count+1):
        if i < 10:
            sub_list.append(file_name_repeat+ "-0"+str(i))
        else:
            sub_list.append(file_name_repeat+ "-"+str(i))


    for sub in sub_list:
        file_name = "_".join(file_name_list)
        file_name = sub+"_" + file_name
        path = os.path.join(base_path, sub, inner_directory, file_name)
        path_list.append(path)

    return path_list

def create_Time_Series(input_file, mask, num = 0):
    if mask == "":
        ts = os.path.split(input_file)
        tsName = ts[len(ts)-1]
        tsNamesub = tsName.split("_")
        tsN = tsNamesub[0] + "_" + tsNamesub[1]

        if num == 0:
            TSname = os.path.join("Scripts", "Time_Series", tsN + ".txt")
        else:
            TSname = os.path.join("Scripts", "Time_Series", tsN + str(num) + ".txt")
        subprocess.call(['fslmeants', '-i', input_file, '-o', TSname])
    else:
        ts = os.path.split(input_file)
        tsName = ts[len(ts) - 1]
        tsNamesub = tsName.split("_")
        tsN = tsNamesub[0] + "_" + tsNamesub[1]
        if num == 0:
            TSname = os.path.join("Scripts", "Time_Series", tsN + ".txt")
        else:
            TSname = os.path.join("Scripts", "Time_Series", tsN + str(num) + ".txt")
        subprocess.call(['fslmeants', '-i', input_file, '-o', TSname, '-m', mask])

def fslBET(BOLD_path,sub_dir, num = 0):
    BOLD = os.path.basename(BOLD_path) + "_brain"

    if num == 0:
        BetPath = os.path.join("Scripts", "BET_Files", "BET")
        subprocess.call(['bet', BOLD_path, BetPath,"-f", "0.5", "-g", "0"])
    else:
        BetPath = os.path.join("Scripts", "BET_Files", sub_dir, "BET"+ str(num))
        subprocess.call(['bet', BOLD_path, BetPath,"-f", "0.5", "-g", "0"])


def edit_run_fsf(fsfin, boldList, bet, onset):
    for i in range(len(boldList)):
        base = os.path.basename(fsfin)
        subprocess.call(['cp', fsfin, os.path.join("Scripts", "fsf_File")])
        fsf = os.path.join("Scripts", "fsf_File", base)
        base_sep = base.split('.')
        base_sep[0] = base_sep[0] + str(i+1)
        base_new = '.'.join(base_sep)
        subprocess.call(['mv', fsf, os.path.join("Scripts", 'fsf_File', base_new)])

    list_fsf_paths = listdir_nohidden(os.path.join("Scripts", "fsf_File"))
    list_fsf = []
    for i in list_fsf_paths:
        list_fsf.append(os.path.join("Scripts", "fsf_File", i))
    list_fsf.sort()

    count = 0

    for fsf_path in list_fsf:
        file= fileinput.input(fsf_path, inplace=True)
        for line in file:
            if("set fmri(outputdir)" in line):
                direct = os.path.join("Scripts", "FEAT", "subject" + str(count+1))
                direct_abs = os.path.abspath(direct)
                line = "set fmri(outputdir) "+ '"' + direct_abs + '"'
            print(line, end = "")
            if ("set fmri(outputdir)" in line):
                print()
        file.close()
        file= fileinput.input(fsf_path, inplace=True)
        for line in file:
            if("set feat_files(1)" in line):
                bold_no_nii = boldList[count].split(".")
                line = "set feat_files(1) " + '"' + bold_no_nii[0] + '"'
            print(line, end="")
            if ("set feat_files(1)" in line):
                print()
        file.close()
        file = fileinput.input(fsf_path, inplace=True)
        for line in file:
            if("set highres_files(1)" in line):
                direct_abs = os.path.abspath(bet[count])
                line = "set highres_files(1) " + '"' + direct_abs +'"'
            print(line, end = "")
            if ("set highres_files(1)" in line):
                print()

        file.close()
        file = fileinput.input(fsf_path, inplace=True)


        for line in file:
            for i in range(len(onset[count])):
                if ("set fmri(evtitle" + str(i + 1) + ")" in line):
                    direct_abs = os.path.abspath(str(onset[count][i]))
                    base = os.path.basename(onset[count][i])
                    base_name = base.split('.')
                    line = "set fmri(evtitle" + str(i + 1) + ") " + '"' + base_name[0] + '"'
            print(line, end="")

        file.close()
        file = fileinput.input(fsf_path, inplace=True)

        for line in file:
            for i in range(len(onset[count])):
                if("set fmri(custom"+str(i+1) +")" in line):
                    direct_abs = os.path.abspath(str(onset[count][i]))
                    line = "set fmri(custom" + str(i+1) + ") " + '"' + direct_abs + '"'
            print(line, end = "")

        file.close()
        count +=1

        direct = os.path.dirname(fsf_path)
        bak_list = [x for x in os.listdir(direct) if x.endswith('.bak')]
        full_paths_bak = []
        for i in bak_list:
            path = os.path.join(direct, i)
            full_paths_bak.append(path)
        for j in full_paths_bak:
            subprocess.call(['rm', j])

    for fsf_path in list_fsf:
        path = os.path.abspath(fsf_path)
        subprocess.call(['feat', path])


def output_final():
    os.mkdir("Data")
    for i in listdir_nohidden(os.path.join("Scripts", "Onset_Files")):
        file_onset = os.path.join("Scripts", "Onset_Files", i)
        subprocess.call(['cp', '-avr', file_onset, os.path.join("Data")])

    count =1
    for i in listdir_nohidden(os.path.join("Scripts", "BET_Files")):
        for j in listdir_nohidden(os.path.join("Scripts", "BET_Files", i)):
            file_BET = os.path.join("Scripts", "BET_Files", i, j)
            subprocess.call(['cp', file_BET, os.path.join("Data", "subject" + str(count))])
        count +=1

    count = 1
    feat_list = listdir_nohidden(os.path.join("Scripts", "FEAT"))
    feat_list.sort()
    for i in feat_list:
        feat_file = os.path.join("Scripts", "FEAT", i)
        subprocess.call(['cp', '-avr', feat_file, os.path.join("Data", "subject" + str(count))])
        count +=1

def delete_data():
    for i in listdir_nohidden(os.path.join("Scripts", "Onset_Files")):
        dir_onset = os.path.join("Scripts", "Onset_Files", i)
        subprocess.call(['rm', '-r', dir_onset])

    for i in listdir_nohidden(os.path.join("Scripts", "BET_Files")):
        dir_BET = os.path.join("Scripts", "BET_Files", i)
        subprocess.call(['rm', '-r', dir_BET])

    for i in listdir_nohidden(os.path.join("Scripts", "FEAT")):
        feat_file = os.path.join("Scripts", "FEAT", i)
        subprocess.call(['rm', '-r', feat_file])

    for i in listdir_nohidden(os.path.join("Scripts", "fsf_File")):
        fsf_file = os.path.join("Scripts", "fsf_File", i)
        subprocess.call(['rm', fsf_file])