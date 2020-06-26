from pathlib import Path
import os
import wx
import PyPDF2

extensions = {
    ".pdf"
}
exclusion = {
    '', None, 'untitled'
}


def rec_file_search(path):
    if os.path.isdir(path):
        files = os.listdir(path)
        for file in files:
            rec_file_search(path + "\\"+file)
    else:
        p = Path(path)
        if p.suffix in extensions:
            try:
                pdf = PyPDF2.PdfFileReader(path)
                if('/Title' in pdf.documentInfo and pdf.documentInfo.title not in exclusion):
                    abs_pathlist.append(path)
                    pathlist.append(path)
                    plist.append(p)
                    titlelist.append(pdf.documentInfo.title)
                else:
                    print("Can't get title")
            except Exception as e:
                print(path+str(e))


def rename(self):
    for i in range(len(titlelist)):
        path = pathlist[i]
        title = titlelist[i]
        p = plist[i]
        j = 0
        parent = str(p.parent)+'\\'
        if(os.path.exists(parent+title+".pdf")):
            while True:
                if(not os.path.exists(parent+title+"("+str(i)+").pdf")):
                    os.rename(path, parent+title+"("+str(i)+").pdf")
                else:
                    j += 1
        else:
            os.rename(path, parent+title+".pdf")
    print('rename done!')


class FileDropTarget(wx.FileDropTarget):
    def __init__(self, window, listctrl):
        self.listctrl = listctrl
        wx.FileDropTarget.__init__(self)
        self.window = window

    def OnDropFiles(self, x, y, files):
        for filepath in files:
            print("DnD:"+str(filepath))
            App.add(self, filepath)
        return True


class App(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(
            800, 400), style=wx.DEFAULT_FRAME_STYLE)
        p = wx.Panel(self, wx.ID_ANY)
        self.listctrl = wx.ListCtrl(p, wx.ID_ANY, style=wx.LC_REPORT)
        self.listctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.item_select)
        self.listctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                           self.item_select)  # select時とやるべきことは同じ
        self.listctrl.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.delete)
        self.listctrl.InsertColumn(0, "title", wx.LIST_FORMAT_LEFT, 300)
        self.listctrl.InsertColumn(1, "path", wx.LIST_FORMAT_LEFT, 1500)
        for i in range(len(titlelist)):
            self.listctrl.InsertItem(i, titlelist[i])
            self.listctrl.SetItem(i, 1, pathlist[i])
        self.dltbtn = wx.Button(p, label="delete", size=(100, 50))
        self.dltbtn.Bind(wx.EVT_BUTTON, self.delete)
        self.savebtn = wx.Button(p, label="save(実行)", size=(200, 50))
        self.savebtn.Bind(wx.EVT_BUTTON, self.rename)
        self.addbtn = wx.Button(p, label="add_folder", size=(100, 50))
        self.addbtn.Bind(wx.EVT_BUTTON, self.add_folder)
        self.add_filebtn = wx.Button(p, label="add_file", size=(100, 50))
        self.add_filebtn.Bind(wx.EVT_BUTTON, self.add_file)
        self.clrbtn = wx.Button(p, label="clear", size=(100, 50))
        self.clrbtn.Bind(wx.EVT_BUTTON, self.flush)

        dt = FileDropTarget(self, self.listctrl)
        self.SetDropTarget(dt)

        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout2 = wx.BoxSizer(wx.VERTICAL)
        layout3 = wx.BoxSizer(wx.VERTICAL)

        layout.Add(self.listctrl, 1, wx.GROW)
        layout2.Add(self.addbtn, 0.1, wx.BOTTOM, border=10)
        layout2.Add(self.add_filebtn, 0.1, wx.BOTTOM, border=10)
        layout2.Add(self.dltbtn, 0.1, wx.BOTTOM, border=10)
        layout2.Add(self.clrbtn, 0.1, wx.BOTTOM, border=10)
        layout.Add(layout2)
        layout3.Add(layout, wx.EXPAND)
        layout3.Add(self.savebtn, 1, wx.ALIGN_RIGHT)
        p.SetSizer(layout3)

        self.Show()

    def item_select(self, event):
        self.select_indexlist = []
        item = -1
        while 1:
            item = self.listctrl.GetNextItem(
                item, wx.LIST_NEXT_ALL, wx.LIST_STATE_SELECTED)
            if item != -1:
                self.select_indexlist.append(item)
            else:
                break

    def delete(self, event):
        j = 0
        for select_index in self.select_indexlist:
            print("delete "+str(titlelist[select_index-j]))
            titlelist.pop(select_index-j)
            pathlist.pop(select_index-j)
            abs_pathlist.pop(select_index-j)
            plist.pop(select_index-j)
            self.listctrl.DeleteItem(select_index-j)
            j += 1
        self.select_indexlist = []

    def add(self, abs_path):
        rec_file_search(abs_path)
        self.listctrl.DeleteAllItems()
        for i in range(len(titlelist)):
            self.listctrl.InsertItem(i, str(titlelist[i]))
            self.listctrl.SetItem(i, 1, pathlist[i])

    def add_folder(self, event):
        folder = wx.DirDialog(self, style=wx.DD_CHANGE_DIR,
                              message="Select a directory")
        if folder.ShowModal() == wx.ID_OK:
            abs_path = folder.GetPath()
            folder.Destroy()
            App.add(self, abs_path)

    def add_file(self, event):
        file = wx.FileDialog(self, style=wx.DD_CHANGE_DIR,
                             message="Select a file")
        if file.ShowModal() == wx.ID_OK:
            self.abs_path = file.GetPath()
            file.Destroy()
            App.add(self.abs_path)

    def rename(self, event):
        for i in range(len(titlelist)):
            path = pathlist[i]
            title = titlelist[i]
            p = plist[i]
            j = 0
            parent = str(p.parent)+'\\'
            if(os.path.exists(parent+title+".pdf")):
                while True:
                    if(not os.path.exists(parent+title+"("+str(j)+").pdf")):
                        os.rename(path, parent+title+"("+str(j)+").pdf")
                        j = 0
                        break
                    else:
                        j += 1
            else:
                os.rename(path, parent+title+".pdf")
        App.flush(self, event)
        print('rename done')

    def flush(self, event):
        pathlist.clear()
        titlelist.clear()
        plist.clear()
        self.listctrl.DeleteAllItems()


if __name__ == '__main__':
    abs_pathlist = []
    pathlist = []
    titlelist = []
    plist = []
    select_indexlist = []
    app = wx.App()
    App(None, wx.ID_ANY, "PDFtitleRenamer")
    app.MainLoop()
