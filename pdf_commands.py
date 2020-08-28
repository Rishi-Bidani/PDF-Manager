from tkinter import filedialog
import PyPDF2
from PyPDF2 import PdfFileWriter, PdfFileReader
from tkinter import *
from functools import partial
import os

gui = Tk()
gui.geometry("700x700")
gui.title("Work With PDF's")


class ClearPage:
    def __init__(self, screen):
        self.screen = screen

    def Clear(self):
        for widget in self.screen.winfo_children():
            widget.destroy()


class LabelWidget:
    def __init__(self, window, text, font, size, wraplength=None):
        self.window = window
        self.text = text
        self.font = font
        self.size = size
        self.wraplength = wraplength

    def Call(self):
        var = Label(self.window, text=self.text, wraplength=self.wraplength)
        var.config(font=(f'{self.font}', self.size))
        return var


class MainScreen(ClearPage):
    Path = ""
    Filename = ""
    MergePath = ""
    MergeFilename = ""

    def mainpage(self):
        # Heading
        label1 = LabelWidget(gui, "PDF Format", "Courier", 26)
        label1.Call().place(relx=0.375, rely=0.039)

        # Choose file
        label2 = LabelWidget(gui, "Choose File", "Courier", 18)
        label2.Call().place(relx=0.05, y=110)

        # Filename after choosing
        label3 = LabelWidget(self.screen, "File Name: ", "Courier", 16)
        label3.Call().place(relx=0.05, y=150)

        # Input box Label
        label4 = LabelWidget(self.screen, "Pages To Delete", "Courier", 16)
        label4.Call().place(relx=0.05, y=190)

        # Filename after choosing merge
        label5 = LabelWidget(self.screen, "Merging File: ", "Courier", 16)
        label5.Call().place(relx=0.05, y=340)

        # Input box
        getPageDel = Entry(self.screen)
        getPageDel.place(relx=0.4, y=190, width=350, height=25)

        # Labels for Merge
        mergechoosefile = LabelWidget(self.screen, "Choose Merge file", "Courier", 16)
        mergechoosefile.Call().place(relx=0.05, rely=0.4)

        # ---------------- Buttons on Main Screen---------------------------

        selectfile = Button(self.screen, text='Select a pdf file', padx="15", pady="10", bg="lightgrey",
                   command=lambda: self.file_opener())
        selectfile.place(relx=0.4, y=100)

        # -----
        selectmergefile = Button(self.screen, text='Select a pdf file', padx="15", pady="10", bg="lightgrey",
                   command=lambda: self.mergefiles_opener())
        selectmergefile.place(relx=0.4, rely=0.39)

        # -----
        deletebutton = Button(self.screen, text='Delete Pages', padx="15", pady="10", bg="lightgrey",
                   command=partial(self.getEntries, getPageDel))
        deletebutton.place(relx=0.15, rely=0.8)

        # -----
        mergebutton = Button(self.screen, text='Merge Pdf', padx="15", pady="10", bg="lightgrey",
                   command=partial(self.mergefiles))
        mergebutton.place(relx=0.5, rely=0.8)
        # ------------------------------------------------------------------

    def file_opener(self):
        location = filedialog.askopenfile(initialdir=r"/C:\MY DATA\python projects\work with pdf")
        print(type(location))
        path = os.path.abspath(location.name)
        MainScreen.Path = path

        filename = os.path.basename(location.name)
        MainScreen.Filename = filename

        filenameLabel = LabelWidget(self.screen, f'{filename}', "Courier", 16)
        filenameLabel.Call().place(relx=0.4, y=150)

        print(path)

    def mergefiles_opener(self):
        mergelocation = filedialog.askopenfile(initialdir='/')
        mergepath = os.path.abspath(mergelocation.name)
        MainScreen.MergePath = mergepath

        mergefilename = os.path.basename(mergelocation.name)
        MainScreen.MergeFilename = mergefilename

        mergefilenamelabel = LabelWidget(self.screen, f'{mergefilename}', "Courier", 16)
        mergefilenamelabel.Call().place(relx=0.4, y=340)

    def getEntries(self, listofpagestodel):
        result = [None if x.strip() == 'None' else int(x) for x in listofpagestodel.get().split(',')]
        self.delpages(result)

    def delpages(self, listofpagestodel):
        print(listofpagestodel)
        pages_to_delete = listofpagestodel  # page numbering starts from 0
        infile = PdfFileReader(MainScreen.Path, 'rb')
        output = PdfFileWriter()
        counter = 1
        outputfilename = ""
        name, extension = os.path.splitext(MainScreen.Filename)

        while counter <= 5:
            if os.path.exists(name + f'{counter}' + '.pdf'):
                counter += 1
            elif not os.path.exists(name + f'{counter}' + '.pdf'):
                outputfile = name + f'{counter}' + '.pdf'
                outputfilename = outputfile
                break
            else:
                gui.destry()

        for i in range(infile.getNumPages()):
            if i not in pages_to_delete:
                p = infile.getPage(i)
                output.addPage(p)

        with open(f'{outputfilename}', 'wb') as f:
            output.write(f)

    def mergefiles(self):
        # Open the files that have to be merged one by one
        pdf1File = open(f'{MainScreen.Filename}', 'rb')
        pdf2File = open(f'{MainScreen.MergeFilename}', 'rb')

        # Read the files that you have opened
        pdf1Reader = PyPDF2.PdfFileReader(pdf1File)
        pdf2Reader = PyPDF2.PdfFileReader(pdf2File)

        # Create a new PdfFileWriter object which represents a blank PDF document
        pdfWriter = PyPDF2.PdfFileWriter()

        # Loop through all the pagenumbers for the first document
        for pageNum in range(pdf1Reader.numPages):
            pageObj = pdf1Reader.getPage(pageNum)
            pdfWriter.addPage(pageObj)

        # Loop through all the pagenumbers for the second document
        for pageNum in range(pdf2Reader.numPages):
            pageObj = pdf2Reader.getPage(pageNum)
            pdfWriter.addPage(pageObj)

        # Now that you have copied all the pages in both the documents, write them into the a new document
        counter = 1
        name = 'Merged'
        outputfilename = ""
        while counter <= 10:
            if os.path.exists(name + f'{counter}' + '.pdf'):
                counter += 1
            elif not os.path.exists(name + f'{counter}' + '.pdf'):
                outputfile = name + f'{counter}' + '.pdf'
                outputfilename = outputfile
                break
            else:
                gui.destry()
        pdfOutputFile = open(f'{outputfilename}', 'wb')
        pdfWriter.write(pdfOutputFile)

        # Close all the files - Created as well as opened
        pdfOutputFile.close()
        pdf1File.close()
        pdf2File.close()


a = MainScreen(gui)
a.mainpage()
gui.mainloop()
