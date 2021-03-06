import pandas as pd
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.config import Config
from Scripts.analyze_csv import get_headers, remove_string_data, create_data_dictionary,\
    read_csv, create_onset_file, get_start_time, get_paths_BIDS, create_Time_Series, fslBET, edit_run_fsf,\
    listdir_nohidden, output_final, delete_data, get_all_CSV
from kivy.core.window import Window
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
import os

file_path = ""
bold_file = ""
fsf_file = ""
mask_file = ""
all_bolds = []
HEADERS= []
Onset_Data_List = []
Data_Dict = {}
folder_list = []
df = pd.DataFrame
batch = False
batchts = False
batchBET = False

class P(Screen):
    pass

class P2(Screen):
    pass

class P3(Screen):
    pass
def show_popup(title):
    show = P()

    popupWindow = Popup(title=title, content = show, size_hint = (None, None), size= (400,200) )

    popupWindow.open()

def show_popup2(title):
    show = P2()

    popupWindow = Popup(title=title, content=show, size_hint=(None, None), size=(450, 200))

    popupWindow.open()

def show_popup3(title):
    show = P3()

    popupWindow = Popup(title=title, content=show, size_hint=(None, None), size=(450, 200))

    popupWindow.open()
# create the layout class
class MainWindow(Screen):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

    def on_pre_enter(self):
        Config.set('graphics', 'resizable', '0')
        Config.write()
        Window.size = (225, 400)

    def organize_data(self):
        output_final()

    def clear_data(self):
        delete_data()


class Filechooser(Screen):
    def __init__(self, **kwargs):
        super(Filechooser, self).__init__(**kwargs)
        self.path = ObjectProperty(None)

    def on_pre_enter(self):
        Window.size = (700, 700)



    def select(self, *args):
        try:
            self.path.text = args[1][0]
        except:
            pass

    def checked(self, instance, value):
        global batch
        if value is True:
            batch = True
        else:
            batch = False

    def savePath(self, instance, path):
        global file_path
        file_path = path.text
        return file_path

    def getcols(self, instance):
        global file_path
        global HEADERS
        global Data_Dict
        global df
        df = read_csv(file_path)
        cols= get_headers(df)
        Data_Dict = create_data_dictionary(df=df, data_labels=cols)
        HEADERS = remove_string_data(data_dict=Data_Dict, data_labels=cols)
        return HEADERS



class SecondWindow(Screen):
    def __init__(self, **kwargs):
        super(SecondWindow, self).__init__(**kwargs)
        self.buttons = []

    def chooseOnsetData(self, instance):
        global Onset_Data_List
        if instance.background_color == [0.8,0.8,0.8,1]:
            Onset_Data_List.append(instance.text)
            instance.background_color = [0,1,0,1]
        else:
            Onset_Data_List.remove(instance.text)
            instance.background_color= [0.8,0.8,0.8,1]

    def make_Onset_File(self, instance):
        global df
        global Data_Dict
        global Onset_Data_List
        global batch
        global folder_list
        if batch == False:
            start_time = get_start_time(df)
            create_onset_file(Onset_Data_List, Data_Dict, start_time)
        else:
            paths = get_all_CSV(file_path)
            folder = "subject"
            sub_num = 1
            for i in range(len(paths)):
                folder_name = folder + str(sub_num)
                folder_path = os.path.join("Scripts", "Onset_Files", folder_name)
                if os.path.exists(folder_path):
                    folder_list.append(folder_name)
                    sub_num +=1
                else:
                    os.mkdir(folder_path)
                    folder_list.append(folder_name)
                    sub_num += 1

            count = 1
            for i in paths:
                df = read_csv(i)
                cols = get_headers(df)
                Data_Dict = create_data_dictionary(df=df, data_labels=cols)
                start_time = get_start_time(df)
                create_onset_file(Onset_Data_List, Data_Dict, start_time,folder_list[count-1], count)
                count += 1

        for i in self.buttons:
            i.background_color = [0.8, 0.8, 0.8, 1]
            Onset_Data_List.clear()

        show_popup("Onset File Created")


    def on_enter(self):
        global HEADERS
        right = 0.18
        top = 0.8
        count = 0
        for header in HEADERS:
            button = Button(text=header, pos_hint={"right": right, "top": top}, size_hint=(0.17, 0.03), background_color=[0.8,0.8,0.8,1])
            button.bind(on_release=self.chooseOnsetData)
            self.buttons.append(button)
            self.ids.floatOnset.add_widget(button)
            right += 0.2
            count += 1
            if (count-5 ==0):
                top -= 0.05
                right = 0.18
                count -=5

        enter_button = Button(text="Create Onset File", pos_hint={"right": 0.6, "bottom": 1}, size_hint=(0.17, 0.03), background_color=[0.8,0.8,0.8,1])
        enter_button.bind(on_release=self.make_Onset_File)
        self.ids.floatOnset.add_widget(enter_button)

    def on_pre_enter(self):
        Window.size = (700, 700)

class Filechooserbold(Screen):
    def __init__(self, **kwargs):
        super(Filechooserbold, self).__init__(**kwargs)
        self.bold = ObjectProperty(None)


    def on_pre_enter(self):
        Window.size = (700, 700)


    def select(self, *args):
        try:
            self.bold.text = args[1][0]
        except:
            pass

    def checked(self, instance, value):
        global batchBET
        if value is True:
            batchBET = True
        else:
            batchBET = False

    def saveBold(self, instance, bold):
        global bold_file
        bold_file = bold.text
        return bold_file

class BETwindow(Screen):
    def __init__(self, **kwargs):
        super(BETwindow, self).__init__(**kwargs)
        self.boldData = ObjectProperty(None)

    def on_pre_enter(self):
        Window.size = (500, 300)

    def on_enter(self, *args):
        global bold_file
        self.boldData.text = os.path.basename(bold_file)

    def makeBET(self):
        global batchBET
        global bold_file
        global all_bolds
        if batchBET == False:
            fslBET(bold_file, 0)
        else:
            paths = get_paths_BIDS(bold_file)
            all_bolds = paths
            folder = "subject"
            sub_num = 1
            for i in range(len(paths)):
                folder_name = folder + str(sub_num)
                folder_path = os.path.join("Scripts", "BET_Files", folder_name)
                if os.path.exists(folder_path):
                    folder_list.append(folder_name)
                    sub_num += 1
                else:
                    os.mkdir(folder_path)
                    folder_list.append(folder_name)
                    sub_num += 1

            count = 1
            for i in paths:
                fslBET(i,folder_list[count-1], num=count)
                count += 1
        show_popup2("BET")



class Filechooserfsf(Screen):
    def __init__(self, **kwargs):
        super(Filechooserfsf, self).__init__(**kwargs)
        self.fsf = ObjectProperty(None)


    def on_pre_enter(self):
        Window.size = (700, 700)


    def select(self, *args):
        try:
            self.fsf.text = args[1][0]
        except:
            pass


    def savefsf(self, instance, fsf):
        global fsf_file
        fsf_file = fsf.text
        return fsf_file

class FEATWindow(Screen):
    def __init__(self, **kwargs):
        super(FEATWindow, self).__init__(**kwargs)

    def on_pre_enter(self):
        Window.size = (500, 400)


    def make_FEAT(self):
        global fsf_file
        global all_bolds

        subjectsBET = listdir_nohidden(os.path.join("Scripts", "BET_Files"))
        bets = []
        betcount = 1
        for i in subjectsBET:
            bets.append(os.path.join("Scripts", "BET_Files", "subject"+str(betcount), "BET" + str(betcount)))
            betcount+=1
        subjectsOnset = listdir_nohidden(os.path.join("Scripts", "Onset_Files"))
        onset_lists = []

        for j in subjectsOnset:
            onset_lists.append(listdir_nohidden(os.path.join("Scripts", "Onset_Files", j)))


        for z in range(len(onset_lists)):
            sub = "subject" + str(z+1)
            baseOnset = os.path.join("Scripts", "Onset_Files", sub)
            for j in range(len(onset_lists[z])):
                curr = onset_lists[z][j]
                onset_lists[z][j] = os.path.join(baseOnset, curr)



        edit_run_fsf(fsf_file, all_bolds, bets, onset_lists)

        show_popup3("FEAT Finished")




class Filechoosermask(Screen):
    def __init__(self, **kwargs):
        super(Filechoosermask, self).__init__(**kwargs)
        self.mask = ObjectProperty(None)


    def on_pre_enter(self):
        Window.size = (700, 700)


    def select(self, *args):
        try:
            self.mask.text = args[1][0]
        except:
            pass



    def saveMask(self, instance, mask):
        global mask_file
        mask_file = mask.text
        return mask_file

class TSWindow(Screen):
    def __init__(self, **kwargs):
        super(TSWindow, self).__init__(**kwargs)
        self.boldData = ObjectProperty(None)
        self.maskData = ObjectProperty(None)

    def on_pre_enter(self):
        Window.size = (500, 400)


    def on_enter(self, *args):
        global bold_file
        global mask_file
        self.boldData.text = os.path.basename(bold_file)
        if mask_file != "":
            self.maskData.text = os.path.basename(mask_file)
        else:
            self.maskData.text = mask_file

    def makeTS(self):
        global batchts
        global bold_file
        global mask_file
        if batchts == False:
            create_Time_Series(input_file=bold_file, mask=mask_file)

        else:
            paths = get_paths_BIDS(bold_file)
            count = 1
            for i in paths:
                create_Time_Series(input_file = i, mask=mask_file, num=count)
                count +=1
        show_popup2("Time Series")

class WindowManager(ScreenManager):
    pass


class psychpyaddonapp(App):
    def build(self):
        return WindowManager()
#kv = Builder.load_file("PsychopyAddon.kv")


def activateGUI():
    psychpyaddonapp().run()

