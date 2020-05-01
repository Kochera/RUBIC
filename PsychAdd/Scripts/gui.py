import pandas as pd
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.button import Button
from kivy.config import Config
from Scripts.AnalyzeCSV import get_headers, remove_string_data, create_data_dictionary, read_csv, create_onset_file, get_start_time, get_paths_BIDS
from kivy.core.window import Window
Config.set('graphics', 'resizable', False)
file_path = ""
HEADERS= []
Onset_Data_List = []
Data_Dict = {}
df = pd.DataFrame
batch = False
# create the layout class
class MainWindow(Screen):
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

    def on_pre_enter(self):
        Window.size = (250, 500)
        Config.set('graphics', 'resizable', False)

class Filechooserts(Screen):
    def __init__(self, **kwargs):
        super(Filechooserts, self).__init__(**kwargs)
        self.path = ObjectProperty(None)
    def on_pre_enter(self):
        Window.size = (700, 700)
        Config.set('graphics', 'resizable', False)

    def select(self, *args):
        try:
            self.path.text = args[1][0]
        except:
            pass

    def savePath(self, instance, path):
        global file_path
        file_path = path.text
        return file_path

class TSWindow(Screen):
    def __init__(self, **kwargs):
        super(TSWindow, self).__init__(**kwargs)

class Filechooser(Screen):
    def __init__(self, **kwargs):
        super(Filechooser, self).__init__(**kwargs)
        self.path = ObjectProperty(None)
    def on_pre_enter(self):
        Window.size = (700, 700)
        Config.set('graphics', 'resizable', False)


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
        if batch == False:
            start_time = get_start_time(df)
            create_onset_file(Onset_Data_List, Data_Dict, start_time)
            return 0
        else:
            paths = get_paths_BIDS(file_path)
            count = 1
            for i in paths:
                df = read_csv(i)
                cols = get_headers(df)
                Data_Dict = create_data_dictionary(df=df, data_labels=cols)
                start_time = get_start_time(df)
                create_onset_file(Onset_Data_List, Data_Dict, start_time, count)
                count += 1

        for i in self.buttons:
            i.background_color = [0.8, 0.8, 0.8, 1]
            Onset_Data_List.clear()


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


class WindowManager(ScreenManager):
    pass


class PsychopyAddonApp(App):
    def build(self):
        return WindowManager()
#kv = Builder.load_file("PsychopyAddon.kv")


def activateGUI():
    PsychopyAddonApp().run()

