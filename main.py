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
client = None
btlist = None
addlist = None

UUID_NUS = "6e400002-b5a3-f393-e0a9-e50e24dcca9e"

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

    def buttons(self):
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
        self.ids.container.clear_widgets()
        for clr in colorlist:
            colortext = str(clr)
            clrbtn = Button(text=colortext)
            clrbtn.bind(on_press=self.assign_clr)
            self.ids.container.add_widget(clrbtn)
        
        button2 = Button(text='Disconnect')    
        button2.bind(on_press=self.BTdisconnect)
        self.ids.container.add_widget(button2)
        # if client.is_connected:

    def BTdisconnect(self, instance):
        global client
        async def disconnectBT():
            await client.disconnect()
        
        asyncio.run(disconnectBT())
        exit(0)

    def scan_button(self, instance):
        main()

    def assign_var(self, instance):
        global connect_to 
        connect_to = instance.text
        print(connect_to)
        self.ids.container.clear_widgets()
            
        async def connectBT(addressname):
            index = btlist.index(addressname)
            address = addlist[index]
            global client
            client = BleakClient(address)
            await client.connect()
            if client.is_connected:
                print(f"Connected to {addressname}")

            else:
                print(f"Failed to connect to {addressname}")

        asyncio.run(connectBT(connect_to))
        
        self.colors()

    def assign_clr(self, instance1):
        # send_color = 
        string_to_send = instance1.text
        bytes_ts = string_to_send.encode("utf-8")

        async def send_bytes(bytes):
                    await client.write_gatt_char(UUID_NUS, bytes)
                    print(f"Sent: {bytes.decode('utf-8')}")

        asyncio.run(send_bytes(bytes_ts))

        # self.colors()
        
        # await client.write_gatt_char(UUID_NUS, bytes_ts)
        # print(f"Sent: {bytes_ts.decode('utf-8')}")
        # p = Popen(['python', 'subroutine.py', connect_to, send_color], shell=True)
        # returncode = p.wait()



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
    task = None

    def app_method(self):     
        return Builder.load_file('Gem_Light.kv')

    def app_func(self):
        '''This will run both methods asynchronously and then block until they
        are finished
        '''
        self.task = asyncio.ensure_future(self.waste_time_freely())

        async def run_wrapper():
            # we don't actually need to set asyncio as the lib because it is
            # the default, but it doesn't hurt to be explicit
            await self.async_run(async_lib='asyncio')
            print('App done')
            self.task.cancel()

        return asyncio.gather(run_wrapper(), self.task)

    async def waste_time_freely(self):
        '''This method is also run by the asyncio loop and periodically prints
        something.
        '''
        try:
            i = 0
            while True:
                # if self.root is not None:
                    # status = self.root.ids.label.status
                    # print('{} on the beach'.format(status))

                    # # get some sleep
                    # if self.root.ids.btn1.state != 'down' and i >= 2:
                    #     i = 0
                    #     print('Yawn, getting tired. Going to sleep')
                    #     self.root.ids.btn1.trigger_action()

                i += 1
                await asyncio.sleep(2)
        except asyncio.CancelledError as e:
            print('Wasting time was canceled', e)
        finally:
            # when canceled, print that it finished
            print('Done wasting time')
    
def main():
    global btlist, addlist
    btlist, addlist = asyncio.run(scan())
    # btlist = [x for x in btlist if x is not None]
    print(btlist)
    print(addlist)
    
    
if __name__ == '__main__':
    main()
    Gem_Light().run()  
