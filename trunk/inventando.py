# import the wxPython GUI package
import wx




# Create a new frame class, derived from the wxPython Frame.
class MyFrame(wx.Frame):

    def __init__(self, parent, id, title):
        # First, call the base class' __init__ method to create the frame
        wx.Frame.__init__(self, parent, id, title)

        panel = wx.Panel(self, -1)

        com = wx.StaticText(panel, -1, "Tipo de comuncacion:",wx.Point(15,50))
        
        x = ['Reactivos', 'Moronas', 'KQML', 'Negociacion']
     
        self.tipoCom = wx.ComboBox(panel, -1,"",wx.Point(500,100), wx.Size(110,60), x, style=wx.CB_READONLY)
        self.panel = panel

        self.tipoCom.Bind(wx.EVT_TEXT, self.comboTipoCom)

        sizer = wx.FlexGridSizer(2, 2, 5, 5)
      
        sizer.Add(com)
        sizer.Add(self.tipoCom)

        border = wx.BoxSizer()
        border.Add(sizer, 0, wx.ALL, 15)
        panel.SetSizerAndFit(border)
        self.capa = []
    

    def comboTipoCom(self,event):
        comunicacion =   self.tipoCom.GetValue()
       
        sizer = wx.FlexGridSizer(2, 2, 5, 5)
        
        label1 = wx.StaticText(self.panel, -1, "Numero de agentes:",wx.Point(15,50))
        self.agentes = wx.TextCtrl(self.panel, -1, "" ,wx.Point(175,50), style=1)
        
        label2 = wx.StaticText(self.panel, -1, "Numero de esmeraldas:",wx.Point(15,80))
        self.esmes = wx.TextCtrl(self.panel, -1, "" ,wx.Point(175,80), style=1)
        
        label5 = wx.StaticText(self.panel, -1, "Numero de obsaculos:",wx.Point(15,110))
        self.obst = wx.TextCtrl(self.panel, -1, "" ,wx.Point(175,110),    style=1)
        
        label3 = wx.StaticText(self.panel, -1, "Seleccione el orden de las self.capas:",wx.Point(15,140))
        
        if comunicacion == 'Reactivos':
            self.capa = ['1','2','3','4']
            
            obs = wx.StaticText(self.panel, -1, "Evitar obstaculos:",wx.Point(45,170))
            self.a =  wx.ComboBox(self.panel, -1,"",wx.Point(270,170), wx.Size(50,40), self.capa, style=wx.CB_READONLY)
           
            
            regresar = wx.StaticText(self.panel, -1, "Regresar nave:",wx.Point(45,200))
            self.b =  wx.ComboBox(self.panel, -1,"",wx.Point(270,200), wx.Size(50,40), self.capa, style=wx.CB_READONLY)
            
            cargar = wx.StaticText(self.panel, -1, "Cargar esmeralda:",wx.Point(45,230))
            self.c =  wx.ComboBox(self.panel, -1,"",wx.Point(270,230), wx.Size(50,40), self.capa, style=wx.CB_READONLY)
            
            explorar = wx.StaticText(self.panel, -1, "Explorar:",wx.Point(45,260))
            self.d =  wx.ComboBox(self.panel, -1,"",wx.Point(270,260), wx.Size(50,40), self.capa, style=wx.CB_READONLY)

            esp = wx.StaticText(self.panel, -1, "Agente self.especial:",wx.Point(15,290))
            self.especial = wx.CheckBox(self.panel, -1, "", wx.Point(175, 290))
            
            submit = wx.Button(self.panel, -1, 'Iniciar', (150, 350))
            submit.Bind(wx.EVT_BUTTON, self.buttonClick)
           
                        
            

        elif comunicacion == 'KQML':
            
            self.capa = ['1','2','3','4', '5']
        
            obs = wx.StaticText(self.panel, -1, "Evitar obstaculos:",wx.Point(45,170))
            self.a =  wx.ComboBox(self.panel, -1,"",wx.Point(270,170), wx.Size(50,40), self.capa, style=wx.CB_READONLY)
           
            
            regresar = wx.StaticText(self.panel, -1, "Regresar nave:",wx.Point(45,200))
            self.b =  wx.ComboBox(self.panel, -1,"",wx.Point(270,200), wx.Size(50,40), self.capa, style=wx.CB_READONLY)
            
            cargar = wx.StaticText(self.panel, -1, "Cargar esmeralda:",wx.Point(45,230))
            self.c =  wx.ComboBox(self.panel, -1,"",wx.Point(270,230), wx.Size(50,40), self.capa, style=wx.CB_READONLY)

            msj = wx.StaticText(self.panel, -1, "Revisar mensajes:",wx.Point(45,260))
            self.d =  wx.ComboBox(self.panel, -1,"",wx.Point(270,260), wx.Size(50,40), self.capa, style=wx.CB_READONLY)
            
            explorar = wx.StaticText(self.panel, -1, "Explorar:",wx.Point(45,290))
            self.e =  wx.ComboBox(self.panel, -1,"",wx.Point(270,290), wx.Size(50,40), self.capa, style=wx.CB_READONLY)

            esp = wx.StaticText(self.panel, -1, "Agente especial:",wx.Point(15,320))
            self.especial = wx.CheckBox(self.panel, -1, "", wx.Point(175, 320))
            
            submit = wx.Button(self.panel, -1, 'Iniciar', (150, 380))
            submit.Bind(wx.EVT_BUTTON, self.buttonClick)

        elif comunicacion == 'Moronas':
            
            self.capa = ['1','2','3','4', '5']
            
            ons = wx.StaticText(self.panel, -1, "Evitar obstaculos:",wx.Point(45,170))
            self.a =  wx.ComboBox(self.panel, -1,"",wx.Point(270,170), wx.Size(50,40), self.capa, style=wx.CB_READONLY)
           
            
            regresar = wx.StaticText(self.panel, -1, "Regresar nave:",wx.Point(45,200))
            self.b =  wx.ComboBox(self.panel, -1,"",wx.Point(270,200), wx.Size(50,40), self.capa, style=wx.CB_READONLY)
            
            cargar = wx.StaticText(self.panel, -1, "Cargar esmeralda:",wx.Point(45,230))
            self.c =  wx.ComboBox(self.panel, -1,"",wx.Point(270,230), wx.Size(50,40), self.capa, style=wx.CB_READONLY)

            msj = wx.StaticText(self.panel, -1, "Seguir moronas:",wx.Point(45,260))
            self.d =  wx.ComboBox(self.panel, -1,"",wx.Point(270,260), wx.Size(50,40), self.capa, style=wx.CB_READONLY)
            
            explorar = wx.StaticText(self.panel, -1, "Explorar:",wx.Point(45,290))
            self.e =  wx.ComboBox(self.panel, -1,"",wx.Point(270,290), wx.Size(50,40), self.capa, style=wx.CB_READONLY)

            esp = wx.StaticText(self.panel, -1, "Agente especial:",wx.Point(15,320))
            self.especial = wx.CheckBox(self.panel, -1, "", wx.Point(175, 320))
            
            submit = wx.Button(self.panel, -1, 'Iniciar', (150, 380))
            submit.Bind(wx.EVT_BUTTON, self.buttonClick)

        elif comunicacion == 'Negociacion':
            
            self.capa = ['1','2','3','4', '5']

            obs = wx.StaticText(self.panel, -1, "Evitar obstaculos:",wx.Point(45,170))
            self.a =  wx.ComboBox(self.panel, -1,"",wx.Point(270,170), wx.Size(50,40), self.capa, style=wx.CB_READONLY)
           
            
            regresar = wx.StaticText(self.panel, -1, "Regresar nave:",wx.Point(45,200))
            self.b =  wx.ComboBox(self.panel, -1,"",wx.Point(270,200), wx.Size(50,40), self.capa, style=wx.CB_READONLY)
            
            ccargar = wx.StaticText(self.panel, -1, "Contratos:",wx.Point(45,230))
            self.c =  wx.ComboBox(self.panel, -1,"",wx.Point(270,230), wx.Size(50,40), self.capa, style=wx.CB_READONLY)

            msj = wx.StaticText(self.panel, -1, "Cargar esmeralda:",wx.Point(45,260))
            self.d =  wx.ComboBox(self.panel, -1,"",wx.Point(270,260), wx.Size(50,40), self.capa, style=wx.CB_READONLY)
            
            exp = wx.StaticText(self.panel, -1, "Explorar:",wx.Point(45,290))
            self.e =  wx.ComboBox(self.panel, -1,"",wx.Point(270,290), wx.Size(50,40), self.capa, style=wx.CB_READONLY)

            esp = wx.StaticText(self.panel, -1, "Agente especial:",wx.Point(15,320))
            self.especial = wx.CheckBox(self.panel, -1, "", wx.Point(175, 320))
            
            submit = wx.Button(self.panel, -1, 'Iniciar', (150, 380))

            submit.Bind(wx.EVT_BUTTON, self.buttonClick)

            
    def buttonClick(self,event):
            orden = []
            sizer = wx.FlexGridSizer(2, 2, 5, 5)
            
            try:
                orden = [int(self.a.GetValue()), int(self.b.GetValue()), int(self.c.GetValue()), int(self.d.GetValue())]
                if len(self.capa) == 5:
                    orden.append(int(self.e.GetValue()))
            except:
                dial = wx.MessageDialog(None, "Todos los campos deben estar llenos", "Alerta", wx.OK | wx.ICON_ERROR)
                dial.ShowModal()
                return

            for num in range(1, len(orden)+1):
                print num
                if num not in orden:
                    print num, 'mal'
                    dial = wx.MessageDialog(None, "Los numeros de las capas no pueden estar repetidos", "Alerta", wx.OK | wx.ICON_ERROR)
                    dial.ShowModal()
                    return
            
            if (self.agentes.GetValue() == "" or self.esmes.GetValue() == "" or  self.obst.GetValue() == ""  ):
                dial = wx.MessageDialog(None, "Todos los campos deben estar llenos", "Alerta", wx.OK | wx.ICON_ERROR)
                dial.ShowModal()
                return
            
                 
             ##   maingrafico(int(self.agentes.GetValue()),int(self.esmeraldas.GetValue()), orden, int(self.obs.GetValue()),self.tipoCom.GetValue())
            try:
                maingrafico(int(self.agentes.GetValue()),int(self.esmes.GetValue()), orden, int(self.obst.GetValue()),self.tipoCom.GetValue(),int(self.especial.GetValue()))

            except:
                dial = wx.MessageDialog(None, "Llene los datos correctamente", "Alerta", wx.OK | wx.ICON_ERROR)
                dial.ShowModal()
                return
                
                
                

    


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




