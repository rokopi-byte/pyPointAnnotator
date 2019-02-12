import tkinter as tk
import cv2
import PIL.Image, PIL.ImageTk
import os

class MainWindow():

    def __init__(self, main,images,result,labels,image_path,done):

        # canvas for image
        self.idx = 0
        self.refPt = []
        self.labels = labels
        self.result = result
        self.image_path = image_path
        self.images = images
        self.cv_img = cv2.cvtColor(cv2.imread(os.path.join(self.image_path, self.images[self.idx])), cv2.COLOR_BGR2RGB)
        self.img_backup = self.cv_img.copy()
        self.height, self.width, self.no_channels = self.cv_img.shape
        self.canvas = tk.Canvas(main, width = self.width, height = self.height)
        self.canvas.grid(row=1, column=0, columnspan=3)
        self.buttonSave = tk.Button(main, text="Save/Next", command=self.onButtonSave)
        self.buttonSave.grid(row=2, column=2)
        self.buttonUndo = tk.Button(main, text="Undo", command=self.onButtonUndo)
        self.buttonUndo.grid(row=2, column=1)
        self.buttonReset = tk.Button(main, text="Reset", command=self.onButtonReset)
        self.buttonReset.grid(row=2, column=0)
        self.labelNext = tk.Label(main, text=self.labels[len(self.refPt)], fg="red", font=("Helvetica", 16))
        self.labelNext.grid(row=0, column=1, columnspan=2)
        self.done = done
        self.labelCounter = tk.Label(main, text=str(self.done) + "/" + str(len(self.images) + self.done), fg="blue", font=("Helvetica", 16))
        self.labelCounter.grid(row=0, column=0, columnspan=2)

        # images
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))

        # set first image on canvas
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor = tk.NW, image = self.photo)
        self.canvas.bind("<Button 1>",self.onClick)
        self.canvas.bind("<Button 3>",self.onClickSkip)
        self.buttonSave.configure(state="disabled")
        self.buttonUndo.configure(state="disabled")
        self.buttonReset.configure(state="disabled")

    def onButtonUndo(self):
        del self.refPt[-1]
        if len(self.refPt) == 0:
            self.buttonUndo.configure(state="disabled")
            self.buttonReset.configure(state="disabled")
        self.cv_img = self.img_backup.copy()
        for p in self.refPt:
            cv2.circle(self.cv_img,(p[0],p[1]),5,(0,255,0),-1)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
        self.canvas.itemconfig(self.image_on_canvas, image = self.photo)
        self.labelNext.config(text=self.labels[len(self.refPt)])
        self.buttonSave.configure(state="disabled")

    def onButtonReset(self):
        self.refPt = []
        self.buttonReset.configure(state="disabled")
        self.buttonUndo.configure(state="disabled")
        self.cv_img = self.img_backup.copy()
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
        self.canvas.itemconfig(self.image_on_canvas, image = self.photo)
        self.labelNext.config(text=self.labels[len(self.refPt)])
        self.buttonSave.configure(state="disabled")

    def onButtonSave(self):
        with open(self.result, "a") as mylog:
            mystring=self.images[self.idx] + ";"
            for item in self.refPt:
                mystring+=str(item[0]) + "," + str(item[1]) + ";"
            mystring=mystring[:-1]
            mystring+="\n"
            mylog.write(mystring)
            mylog.flush()
        self.refPt = []
        self.idx+=1
        self.buttonSave.configure(state="disabled")
        self.buttonReset.configure(state="disabled")
        self.buttonUndo.configure(state="disabled")
        self.cv_img = cv2.cvtColor(cv2.imread(os.path.join(self.image_path, self.images[self.idx])), cv2.COLOR_BGR2RGB)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
        self.canvas.itemconfig(self.image_on_canvas, image = self.photo)
        self.labelNext.config(text=self.labels[len(self.refPt)])
        self.canvas.bind("<Button 1>",self.onClick)
        self.canvas.bind("<Button 3>",self.onClickSkip)
        self.img_backup = self.cv_img.copy()
        self.done+=1
        self.labelCounter.config(text=str(self.done) + "/" + str(len(self.images) + self.done))

    def onClick(self,event):
        self.refPt.append((event.x, event.y))
        cv2.circle(self.cv_img,(event.x,event.y),5,(0,255,0),-1)
        self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.cv_img))
        self.canvas.itemconfig(self.image_on_canvas, image = self.photo)
        if len(self.refPt)==len(self.labels):
            self.labelNext.config(text="Done")
            self.canvas.unbind("<Button 1>")
            self.canvas.unbind("<Button 3>")
            self.buttonSave.configure(state="normal")
        else:
            self.labelNext.config(text=self.labels[len(self.refPt)])
        self.buttonUndo.configure(state="normal")
        self.buttonReset.configure(state="normal")

    def onClickSkip(self,event):
        self.refPt.append((-1, -1))
        if len(self.refPt)==len(self.labels):
            self.labelNext.config(text="Done")
            self.canvas.unbind("<Button 1>")
            self.canvas.unbind("<Button 3>")
            self.buttonSave.configure(state="normal")			
        else:
            self.labelNext.config(text=self.labels[len(self.refPt)])
        self.buttonUndo.configure(state="normal")
        self.buttonReset.configure(state="normal")