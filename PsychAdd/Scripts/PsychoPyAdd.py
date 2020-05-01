import pandas as pd
import numpy as np
from tkinter import *

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)


def create_onset_file(Onset_Data_Labels, data_dict, start_time):
    start_ind = determine_start_data(Onset_Data_Labels, data_dict)

    if start_ind == -1:
        return -1
    #ind = len( Onset_Data_Labels[start_ind[0]])
    onset = Onset_Data_Labels[start_ind[0]].replace("Start", "")
    #onset_name = Onset_Data_Labels[start_ind[0]][0:ind] + ".txt"
    onset_name = onset + ".txt"
    f = open(onset_name, "w")
    count = 0
    for ind in range(len(data_dict[Onset_Data_Labels[start_ind[0]]])):
        if (np.isnan(data_dict[Onset_Data_Labels[start_ind[0]]][ind]) == False):
            f.write(str(data_dict[Onset_Data_Labels[start_ind[0]]][ind] - start_time) + ", ")
            f.write(str(start_ind[1][count]) + ", 1\n")
            count+=1
    f.close()

    return 0

def batch_csv():
    pass



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


#Take all column headers from file and store in a list
def create_labels_set(df):
    # Fill List with column headers from excel sheet
    # List makes data sliceable/subscriptable
    data_labels = []
    for i in df.head(0):
        data_labels.append(i)
    return data_labels

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

def myfunction(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"),width=200,height=200)

def set_Up_Main_Screen(window, df, set):
    if set:
        window.geometry('1080x650')
        window.resizable(width=False, height=True)

    photo = PhotoImage(file="Rutgers-RUBIC.gif")

    # Setting up basic data
    data_labels = create_labels_set(df)
    data_dict = create_data_dictionary(df, data_labels)

    # Getting Data but without strings
    data_labels_no_strings = remove_string_data(data_labels, data_dict)
    data_dict_no_strings = create_data_dictionary(df, data_labels_no_strings)
    start_time = get_start_time(df)


    #Adding Frames to mainFrame
    mainFrame = Frame(window, relief = GROOVE, bg="black")


    #Adding Canvas to make it scrollable
    #canvas = Canvas(mainFrame)
    #frame = Frame(canvas, bg="black")
    #myscrollbar = Scrollbar(mainFrame, orient="vertical", command = canvas.yview)
    #canvas.configure(yscrollcommand=myscrollbar.set)

    #myscrollbar.pack(side="right", fill="y")
    #canvas.pack(side="left")
    #canvas.create_window((0, 0), window=frame, anchor='nw')
    #frame.bind("<Configure>", myfunction)


    image_label = Label(mainFrame, image=photo)
    image_label.image = photo
    image_label.pack()

    instructions = Label(mainFrame, text="Choose Columns of interest for Onset File",
                         bg="black", fg="white", font="none 11 bold")


    # Initializing Frames mutable frames
    mid_frame = middle_frame(mainFrame, data_labels_no_strings, data_dict_no_strings, start_time)
    left_frame = left_main_frame(mainFrame, df, mid_frame)

    # Setting Frames onto MainFrame
    image_label.grid(row=0, column=0)
    instructions.grid(row=0, column=1)
    left_frame.grid(row=1, column=0, sticky=N)
    mid_frame.grid(row=1, column=1, sticky=S)

    mainFrame.grid(row=0, column=0)

    #Setting Mainframe on the Window
    #frame.grid(row=0, column=0)
    #frame.mainloop()


#Button Function activated when pressed
def enter(window, fileEntry, frames, set):
    try:
        df = pd.read_csv(fileEntry.get())
        done = True
    except:
        Label(frames[0], text="Incorrect Path", font="none 10", fg="red", bg="black").grid(row=4, column=0)
        done = False

    if done == True:
        for frame in frames:
            frame.destroy()
        set_Up_Main_Screen(window, df, set)



#Create initial screen for getting psychopy log file
def initial_frame(window,file, done):

    window.geometry('275x90')
    window.resizable(width=False, height=False)
    init_frame = Frame(window, bg = 'black')

    #Initializing Frame Widgets
    text_label = Label(init_frame, text= "Enter Path to Log File from Psychopy", width = 30, fg = "white", bg = "black", font = "none 11 bold")
    fileEntry = Entry(init_frame, width = 30, bg = "white")
    entry = Button(init_frame, text='Enter', width=5, command=lambda: enter(window, fileEntry, [init_frame], True), bg="gray")

    #Place Widgets on Window
    text_label.grid(row=1, column = 0)
    fileEntry.grid(row=2, column=0)
    entry.grid(row=3, column=0)

    return init_frame

def left_main_frame(window, file, mid_frame):
    left_frame = Frame(window, bg='black')

    #initializing Frame widgets
    newPath_label = Label(left_frame, text="Enter new log file path", font="none 10", fg="white", bg="black")
    newPath_entry = Entry(left_frame, width=30, bg='white')
    submit_button = Button(left_frame, text='Change Log File', width = 15,
           command = lambda: enter(window, newPath_entry, [left_frame,mid_frame], False), bg = "gray")


    #Organize Widgets onto Frame
    newPath_label.grid(row=1, column=0)
    newPath_entry.grid(row=2, column=0)
    submit_button.grid(row = 3, column=0)

    return left_frame


def middle_frame(window, data_labels, data_dict, start_time):
    # Submit Button Function
    def submit():
        label = Label(frame, bg="black", font="none 10 bold")
        combined_list = [0] * len(data_dict[Onset_Data_Labels[0]])
        if (len(Onset_Data_Labels) >= 2):
            for name in Onset_Data_Labels:
                if "start" not in name.lower():
                    for j in range(len(data_dict[name])):
                        if (np.isnan(data_dict[name][j]) == False):
                            combined_list[j] += data_dict[name][j]
                        else:
                            pass
            created =create_onset_file(Onset_Data_Labels, data_dict, start_time)
            if created == 0:
                for key in range(len(data_labels)):
                    buttons[key].configure(bg='gray')
                label.configure(text="Onset File Created", width=22, fg="green")
                Onset_Data_Labels.clear()
            else:
                label.configure(text="No Start Data Chosen", width=20, fg="red")
        else:
            label.configure(text="Incorrect # of Options", width=22, fg="red")
        label.grid(row=row + 4, column=1)

    #Function for column label buttons being pressed
    def click(buttons, key, Onset_Data_Labels, labels):
        if (buttons[key].cget('bg') == 'gray'):
            buttons[key].configure(bg='green')
            Onset_Data_Labels.append(labels[key])
        elif (buttons[key].cget('bg') == 'green'):
            buttons[key].configure(bg='gray')
            Onset_Data_Labels.remove(labels[key])

    #Start of function
    Onset_Data_Labels = []
    frame = Frame(window, bg='black')

    #Making Buttons labeled with data labels from CSV
    buttons = {}
    k = len(data_labels)
    row = 1
    column = 0
    for ind in range(k):
        buttons[ind] = Button(frame, text=data_labels[ind], width=30,
                              command = lambda ind=ind:click(buttons, ind, Onset_Data_Labels, data_labels)
                              , bg = "gray")
        buttons[ind].grid(row=row, column=column)
        column += 1
        if (column % 3 == 0):
            row += 1
            column -= 3

    #Making output button to create Onset file and reset GUI to create another onset file if wanted
    Button(frame, text='Output Onset File', width = 17,
           command = lambda: submit(), bg = "gray").grid(row= row+1, column = 1)


    return frame



def main():
    window = Tk()
    file = ""
    done = False

    #Setting up all windows and frames
    window.title("Psychopy Add-On")
    window.configure(background="black")
    frame1 = initial_frame(window, file, done)

    frame1.grid(row=0, column=0)

    window.mainloop()

    if done:
        df = pd.read_csv(file)
        # Setting up basic data
        data_labels = create_labels_set(df)
        data_dict = create_data_dictionary(df, data_labels)

        # Getting Data but without strings
        data_labels_no_strings = remove_string_data(data_labels, data_dict)
        data_dict_no_strings = create_data_dictionary(df, data_labels_no_strings)
        start_time = get_start_time(df)

        #Initializing Frames
        #header_frame = Header_Frame(window)
        #left_frame = new_path_frame(window, file)
        #buttons_frame = create_buttons(window, data_labels_no_strings, data_dict_no_strings, start_time)

        #Setting Frames onto Window
        #header_frame.grid(row=0, column=0)


if __name__ == '__main__':
    main()

