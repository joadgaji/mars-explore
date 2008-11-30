# import the wxPython GUI package
import wx
from maingrafico import*



# Create a new frame class, derived from the wxPython Frame.
class MyFrame(wx.Frame):

    def __init__(self, parent, id, title):
        # First, call the base class' __init__ method to create the frame
        wx.Frame.__init__(self, parent, id, title)

        # Associate some events with methods of this class
##        self.Bind(wx.EVT_SIZE, self.OnSize)
##        self.Bind(wx.EVT_MOVE, self.OnMove)

        # Add a panel and some controls to display the size and position
        panel = wx.Panel(self, -1)
        label1 = wx.StaticText(panel, -1, "Numero de agentes:")
        label2 = wx.StaticText(panel, -1, "Numero de esmeraldas:")
        label3 = wx.StaticText(panel, -1, "Seleccione el orden que desea para las capas separados por comas: (ej: 1,4,3,2,5)")
        label4 = wx.StaticText(panel, -1, "Capa1: Evitar obstaculos \nCapa2: Volver a la nave \nCapa3: Recoger esmeraldas \nCapa4:Moronas \nCapa5: Explorar \n\n\n " )
        label5 = wx.StaticText(panel, -1, "Numero de piedras para generar obstaculos:")
        com = wx.StaticText(panel, -1, "Tipo de comuncacion:")
        x = ['Reactivos', 'Moronas', 'KQML', 'Negociacion']
        self.agentes = wx.TextCtrl(panel, -1, "", style=0)
        self.esmeraldas = wx.TextCtrl(panel, -1, "", style=0)
        self.capas = wx.TextCtrl(panel, -1, "", style=0)
        self.obs = wx.TextCtrl(panel, -1, "", style=0)
        self.tipoCom = wx.ComboBox(panel, -1,"",wx.Point(100,100), wx.Size(110,60), x, style=wx.CB_READONLY)
        self.panel = panel
        
        self.submit = wx.Button(panel, -1, 'Iniciar', (250, 275))

        ##self.tipoCom.append(self,'hola')
        self.submit.Bind(wx.EVT_BUTTON, self.buttonClick)

        ##self.Bind(wx.EVT_BUTTON, self.OnClicked, id=iniciar.GetId())

        # Use some sizers for layout of the widgets
        sizer = wx.FlexGridSizer(2, 2, 5, 5)
        sizer.Add(label1)
        sizer.Add(self.agentes)
        sizer.Add(label2)
        sizer.Add(self.esmeraldas)
        sizer.Add(com)
        sizer.Add(self.tipoCom)
        sizer.Add(label5)
        sizer.Add(self.obs)
        sizer.Add(label3)
        sizer.Add(self.capas)
        sizer.Add(label4)
       

        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 15)
        panel.SetSizerAndFit(border)
        self.Fit()


    

    def buttonClick(self,event):
##            orden = []
##            if (self.agentes.GetValue() == "" or self.esmeraldas.GetValue() == "" or self.capas.GetValue() == "" or self.obs.GetValue() == ""  or self.tipoCom.GetValue() == ""):
##                dial = wx.MessageDialog(None, "Todos los campos deben estar llenos", "Alerta", wx.OK | wx.ICON_ERROR)
##                dial.ShowModal()
##                return
##
##            if self.tipoCom.GetValue() == "Negociacion" or self.tipoCom.GetValue() == 'Moronas' or self.tipoCom.GetValue() == 'KQML':
##                a = 5
##            else :
##                ##le cambie a 5 y habia 4
##                a = 4
##                
##            for x in self.capas.GetValue():
##                if x.isdigit():
##                    orden = orden + [int(x)]
##
##            if len(orden) != a:
##                dial = wx.MessageDialog(None, "Debe seleccionar todos los numeros del 1 al 5", "Alerta", wx.OK | wx.ICON_ERROR)
##                dial.ShowModal()
##                return
##
##            for x in range(1,a+1):
##                
##                if not orden.count(x) > 0:
##                               dial = wx.MessageDialog(None, "Debes seleccionar todos los numeros del 1 al 5", "Alerta", wx.OK | wx.ICON_ERROR)
##                               dial.ShowModal()
##                               return

            

           ## try:
                 maingrafico(1,150, [1,2,3,4], 4,'Reactivos', 1)
               ## maingrafico(int(self.agentes.GetValue()),int(self.esmeraldas.GetValue()), orden, int(self.obs.GetValue()),self.tipoCom.GetValue())
              ##   return [int(self.agentes.GetValue()),int(self.esmeraldas.GetValue()), orden, int(self.obs.GetValue())]
            ##except:
            ##    dial = wx.MessageDialog(None, "Llene los datos correctamente", "Alerta", wx.OK | wx.ICON_ERROR)
            ##    dial.ShowModal()
                
                

    


# Every wxWidgets application must have a class derived from wx.App
class MyApp(wx.App):

    # wxWindows calls this method to initialize the application
    def OnInit(self):

        # Create an instance of our customized Frame class
        frame = MyFrame(None, -1, "Mars")
        frame.Show(True)

        # Tell wxWindows that this is our main window
        self.SetTopWindow(frame)

        # Return a success flag
        return True



app = MyApp(0)     # Create an instance of the application class
app.MainLoop()     # Tell it to start processing events




