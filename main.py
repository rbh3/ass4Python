import tkFileDialog
import tkMessageBox
import os
from Tkinter import *

from pre import model


class gui:
    # initialize the Gui Window
    def __init__(self, master):
        self.master = master
        master.title("K Means Clustering")
        m=model()
        self.textBoxPath = Text(master,height=1)
        self.textBoxPath.insert('end', 'Path...')
        self.textBoxPath.configure(state='disabled')
        self.textBoxCluster = Text(master,width=30,height=1)
        self.textBoxCluster.insert('end', 'Num Of Cluster')
        self.textBoxRuns = Text(master,width=30,height=1)
        self.textBoxRuns.insert('end', 'Num Of runs')
        self.browse_button = Button(master, text="Browse", command=lambda: self.update("Browse", m))
        self.preProcess_button = Button(master, text="Pre-Process", command=lambda: self.update("pre", m))
        self.Cluster_button = Button(master, text="Cluster", command=lambda: self.update("clust", m))

        # LAYOUT
        self.textBoxPath.grid(row=1, column=1,  sticky=W)
        self.browse_button.grid(row=1, column=2,  sticky=W+E)
        self.textBoxCluster.grid(row=2, column=1,  sticky=W)
        self.textBoxRuns.grid(row=2, column=2,  sticky=E)
        self.preProcess_button.grid(row=3, column=1,  sticky=W)
        self.Cluster_button.grid(row=3, column=2, sticky=W+E)

    # update the GUI after pressing the buttons
    def update(self, method, m):
        # Browse Button
        if method == "Browse":
            filename = tkFileDialog.askopenfilename(title="choose your Excel file", filetypes=(("Data Files","*.xlsx"),("excel files","*.xls")))
            self.textBoxPath.configure(state='normal')
            self.textBoxPath.delete('0.0',END)
            self.textBoxPath.insert('end',filename)
            self.textBoxPath.configure(state='disabled')
        # Pre Proccess Button
        elif method == "pre":
            if (self.textBoxPath.get('0.0', 'end-1c')== "" or self.textBoxPath.get('0.0', 'end-1c')== "Path..."):
                tkMessageBox.showinfo("K Means Clustering", "Invalid Path!")
                return
            # clean the data using the clean method in modle
            m.clean(self.textBoxPath.get('0.0','end-1c'))
        # Cluster Button
        elif method=="clust":
            # checking Arguments
            try:
                n_cluster=int(self.textBoxCluster.get('0.0','end-1c'))
                if(n_cluster<=0):
                    tkMessageBox.showerror("K Means Clustering", "Num Of Clusters Must be a positive number!")
                    return
                n_runs=int(self.textBoxRuns.get('0.0','end-1c'))
                if(n_runs <= 0):
                    tkMessageBox.showerror("K Means Clustering", "Num Of Runs Must be a positive number!")
                    return
            except Exception:
                tkMessageBox.showerror("K Means Clustering", "One of the Numbers is invalid!")
                return
            # Cluser the data using the kmeans method in modle
            m.k_means(n_cluster,n_runs)
            # Gui Pics side by side
            # pic 1
            picPath1=r'./scatterPlot.gif'
            pic1=PhotoImage(file=picPath1)
            self.imageLabel=Label(image=pic1, width='400px', height='400px')
            self.imageLabel.image = pic1
            self.imageLabel.grid(row=4, column=1, sticky=W)
            # pic2
            picPath2 = r'./map.gif'
            pic2=PhotoImage(file=picPath2)
            self.imageLabe2=Label(image=pic2, width='600px', height='400px')
            self.imageLabe2.image = pic2
            self.imageLabe2.grid(row=4, column=2, sticky=E)
            #finish msg
            tkMessageBox.showinfo("K Means Clustering","Cluster completed successfully!")

root = Tk()
my_gui = gui(root)

# safe exit using X
def on_closing():
    if tkMessageBox.askokcancel("Quit", "Do you want to quit?"):
        root.destroy()
        os._exit(0)

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()