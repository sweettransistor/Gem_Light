from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.button import Button 
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
import asyncio
from bleak import BleakScanner, BleakClient
from subprocess import Popen, PIPE 

# hierarhy:
#   Gem_Light (App)
#   |- MyScreens (ScreenManager)
#      |- MyScreen1 (Screen)
#      |- MyScreen2 (Screen)
#      |- MyScreen3 (Screen)
connectto = 0
colorlist = ['red', 'green', 'blue', 'orange', 'cyan', 'purple', 'cross', 'rflash', 'gflash', 'bflash', 'off'] 
connect_to = None
send_color = None

async def scan():
    # Scan for devices
    devicelist = []
    addresslist = []

    devices = await BleakScanner.discover()
    for device in devices:
        # if device.name == "GLOWING GEM":  # Replace with your device's name
        if device.name is not None:
            devicelist.append(device.name)
            addresslist.append(device)
    return devicelist, addresslist  # Or return the device object

class MyScreens(ScreenManager):
    def screen_manager_method(self):
        
        print('Hello from screen manager')

class MainScreen(Screen):
    def screen_method(self):
        print('Hello from screen 1')

class LoadScreen(Screen):
    #btntext = None

    async def buttons(self):
        self.ids.container.clear_widgets()
        for item in btlist:
            btntext = str(item)
            btn = Button(text=btntext)
            btn.bind(on_press=self.assign_var)
            self.ids.container.add_widget(btn)
            
        button1 = Button(text='Rescan and Restart...')    
        button1.bind(on_press=self.scan_button)
        self.ids.container.add_widget(button1)

    def colors(self):
        # self.ids.container.clear_widgets()
        for clr in colorlist:
            colortext = str(clr)
            clrbtn = Button(text=colortext)
            clrbtn.bind(on_press=self.assign_clr)
            self.ids.container.add_widget(clrbtn)
    
    def scan_button(self, instance):
        exit(_ExitCode = 1)

    async def assign_var(self, instance):
        global connect_to 
        connect_to = instance.text
        print(connect_to)
        self.ids.container.clear_widgets()

        await self.connectBT(connect_to)
        self.colors()

    def assign_clr(self, instance1):
        send_color = instance1.text
        p = Popen(['python', 'subroutine.py', connect_to, send_color], shell=True)
        returncode = p.wait()
        
    async def connectBT(self, addressname):
        index = btlist.index(addressname)
        address = addlist[index]
        client = BleakClient(address)
        await client.connect()
        if client.is_connected:
            print(f"Connected to {addressname}")

        else:
            print(f"Failed to connect to {addressname}")

class ReturnScreen(Screen):     
     
    # def colors(self):
    #     self.ids.container.clear_widgets() 
    #     red = Button(text='red')
    #     red.bind(on_press=self.color_type)
    #     self.ids.container.add_widget(red)

    # def color_type(self, color_command):
    #     color = color_command.text
    #     print(color)

    # p = subprocess.Popen(['python', 'subroutine.py'])
    # returncode = p.wait()

    

    # def change_state(request):
    print("Welcome Back")
    # change_state()   

    # def screen_method(self):
    #     for i in btlist:
    #         btn = Button(text = str(i))
    #         self.add_widget(btn)
    # return
        # Run the scanner and return the device object
        # btlist = asyncio.run(scan())

class MyScreen3(Screen):
    def screen_method(self):
        print('Hello from screen 3')

class Gem_Light(App):
    def app_method(self):     
        return Builder.load_file('Gem_Light.kv')


if __name__ == '__main__':
    global btlist, addlist
    btlist, addlist = asyncio.run(scan())

    # btlist = [x for x in btlist if x is not None]
    print(btlist)
    print(addlist)
    Gem_Light().run()
