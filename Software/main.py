import tkinter as tk
from tkinter import *
import tkinter as tk
import matplotlib
import nltk
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg,
    NavigationToolbar2Tk
)
import gensim.models.keyedvectors as word2vec
import gensim
from module import KmeanTextSummary, ReturnDistortions

w2v_model = word2vec.KeyedVectors.load('w2v.model')
vocabulary = []
for word in w2v_model.index_to_key:
    vocabulary.append(word)

def CheckElbow():
    rootElbow = tk.Tk()
    rootElbow.title("Xem số câu tối ưu")
    rootElbow.geometry('900x600')
    figure = Figure(figsize=(6, 4), dpi=100)
    figure_canvas = FigureCanvasTkAgg(figure, rootElbow)
    NavigationToolbar2Tk(figure_canvas, rootElbow)

    #Get Elbow
    TextInput = str(InputTextBox.get(1.0, END + "-1c"))
    contents_parsed = TextInput.lower()
    contents_parsed = contents_parsed.replace('\n', ' ')
    contents_parsed = contents_parsed.strip()
    Sentences = nltk.sent_tokenize(contents_parsed)
    distortions,n_clusters = ReturnDistortions(Sentences, vocabulary, w2v_model, len(Sentences))
    K_shape = range(1,n_clusters)
    #Initial line chart
    axes = figure.add_subplot()
    axes.plot(K_shape, distortions, marker='o', label='Số cụm')
    handles, labels = axes.get_legend_handles_labels()
    axes.legend(handles, labels)
    axes.set_title('Dùng phương pháp elbow để xác định số cụm tối ưu')
    axes.set_ylabel('Distortion')

    figure_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    rootElbow.mainloop()

def TrackingSentences(value=None):
    TextInput = str(InputTextBox.get(1.0, END + "-1c"))
    contents_parsed = TextInput.lower()
    contents_parsed = contents_parsed.replace('\n', ' ')
    contents_parsed = contents_parsed.strip()
    Sentences = nltk.sent_tokenize(contents_parsed)
    SoCauLabel.config(text=f"Số câu văn bản đầu vào là: {len(Sentences)}")
    InputTextBox.edit_modified(False)

def AboutEvent():
    AboutApp = tk.Tk()
    AboutApp.title("Về chúng tôi")
    AboutApp.geometry('700x380')
    AboutTextBox = Text(AboutApp, font=("bold", 14))
    AboutTextBox.grid(row=0, column=0)
    AboutString = """
Đây là đề tào nghiên cứu khoa học cấp sinh viên ICTU 2022 được thực hiện bởi:
- Nguyễn Vũ Hải - Lớp trưởng CNTT K18 CLC - ICTU (chủ nhiệm đề tài)
- Vũ Quang Huy - Sinh viên CNTT K18 CLC - ICTU
- Nguyễn Ngọc Hải - Sinh viên CNTT K18 CLC - ICTU

Tóm tắt văn bản dùng thuật toán K-mean.
Mọi thắc mắc, giải đáp vui lòng liên lạc nvhai.it.tn@gmail.com
            """
    AboutTextBox.insert(END, AboutString)
    AboutApp.mainloop()

def GetResult():
    try:
        inputText = str(InputTextBox.get(1.0, END + "-1c"))
        n_clusters = int(ChonCumTextBox.get(1.0, END + "-1c"))
        SummaryResult = KmeanTextSummary(inputText, n_clusters, w2v_model, vocabulary)
        OutputTextBox.delete("1.0", END)
        OutputTextBox.insert(END, SummaryResult)
    except Exception as e:
        ExceptionString = """
Lỗi !bạn có thể mắc 1 trong những lỗi sau:
- Để trống ô input
- Để trống ô chọn số câu tóm tắt
- Số câu cần tóm tắt >= số câu đầu vào
- Nhập không đúng định sạng số với câu cần tóm tắt
        """
        OutputTextBox.insert(END, ExceptionString)

def ClearAllTextBox():
    InputTextBox.delete("1.0", END)
    ChonCumTextBox.delete("1.0", END)
    OutputTextBox.delete("1.0", END)

def configureApp():
    for i in range(0, 4):
        window.columnconfigure(i, weight=2, minsize=50)
    for i in range(1, 7):
        window.rowconfigure(i, weight=2, minsize=50)
    # Layout column 0
    GeneralLabel.grid(row=0, column=0, columnspan=3)
    About.grid(row=0, column=2,sticky=E)
    InputLabel.grid(row=1, column=0)
    InputTextBox.grid(row=2, column=0, rowspan=7)

    # Layout column 1
    SoCauLabel.grid(row=1, column=1)
    ChonCumButton.grid(row=2, column=1)
    SoCumLabel.grid(row=3, column=1)
    ChonCumTextBox.grid(row=4, column=1, sticky=N)
    TomTatVanBanButton.grid(row=5, column=1)
    ClearTextButton.grid(row=6, column=1)

    # Layout column 2
    OutputLabel.grid(row=1, column=2)
    OutputTextBox.grid(row=2, column=2, rowspan=7)


    


window = tk.Tk()
window.title("Vietnamese Text summarization using K-mean by Nguyen Vu Hai")
window.geometry('1280x720')
GeneralLabel = tk.Label(text="Tóm tắt văn bản sử dụng thuật toán kmean-clustering", font=("bold", 23), padx=40, pady=50)
About = tk.Button(window, text="Về chúng tôi", font=("bold", 14),command = lambda:AboutEvent())

InputLabel = tk.Label(text="Input", font = ("bold",16))
InputTextBox = Text(window, height = 20, width = 40, font = ("bold", 15))
InputTextBox.bind('<<Modified>>', TrackingSentences)

ChonCumButton = tk.Button(window, text="Xem cụm tối ưu",font = ("bold", 13), command = lambda:CheckElbow())
SoCauLabel = tk.Label(window, text="Mời nhập văn bản",font = ("bold",16))
# SoCauLabel.trace("w",TrackingSentences)
SoCumLabel = tk.Label(window, text= "Chọn số câu cần tóm tắt (số cụm)",font = ("bold",13))
ChonCumTextBox = Text(window, height = 1, width = 10, padx=5, font = ("bold", 15))
TomTatVanBanButton = tk.Button(window, text="Tiến hành tóm tắt",font = ("bold", 13), command= lambda:GetResult())
ClearTextButton = tk.Button(window, text="Xóa nội dung các ô", font = ("bold", 13), command= lambda:ClearAllTextBox())


OutputLabel = tk.Label(text = "Output", font = ("bold", 15))
OutputTextBox = Text(window, height = 20, width = 40, font = ("bold", 16))
configureApp()

window.mainloop()