from tkinter.ttk import Label, Button, Style
import keyboard as ky # type: ignore
import datetime

class WidgetBuilder:
    def build_widget(root, widget, text, row, column, columnspan=1,  padx = 10, pady=10, **kwargs):
        widget = widget(root, text=text, **kwargs)
        widget.grid(row=row, column=column, columnspan=columnspan, padx=padx, pady=pady)
        return widget
    
    def destroy_widget(root, row, column, arr = 0):
        try:
            root.grid_slaves(row=row, column=column)[arr].destroy()
        except:
            pass

class InterfaceUnlockedBuilder:
    def build(botThread):
            InterfaceUnlockedBuilder.style()
            InterfaceUnlockedBuilder.start_bnt(botThread)
            InterfaceUnlockedBuilder.stop_bnt(botThread)
            InterfaceUnlockedBuilder.btn_reset_times_runned(botThread)
            InterfaceUnlockedBuilder.label_times_runned(botThread)
            InterfaceUnlockedBuilder.label_info(botThread)
            InterfaceUnlockedBuilder.label_running_in(botThread)

    def style():
            style = Style()
            style.configure('E.TButton', font=('calibri', 10, 'bold'), foreground='red')
            style.configure('S.TButton', font=('calibri', 10, 'bold'), foreground='green')
            style.map('E.TButton', foreground=[('active', 'red')], background=[('active', 'red')])  
            style.map('S.TButton', foreground=[('active', 'green')], background=[('active', 'green')])
            return style

    def start_running_for(botThread):
        if botThread.is_running == False:
            return

        WidgetBuilder.destroy_widget(botThread.root, 2, 6)
        WidgetBuilder.build_widget(botThread.root, Label, f"Running for {datetime.timedelta(0, botThread.running_time)}", 2, 6)

        botThread.root.after(1000, lambda: InterfaceUnlockedBuilder.start_running_for(botThread))
        botThread.running_time +=1
    
    def start_bnt(botThread):
        ky.add_hotkey('F1', lambda: botThread.start())
        WidgetBuilder.build_widget(botThread.root, Button, "Start bot", 2, 3, style='S.TButton', command=lambda: botThread.start())

    def stop_bnt(botThread):
        ky.add_hotkey('F8', lambda: botThread.stop())    
        WidgetBuilder.build_widget(botThread.root, Button, "Stop bot", 2, 4, style='E.TButton', command=lambda: botThread.stop())

    def label_times_runned(botThread):
        WidgetBuilder.build_widget(botThread.root, Label, f"Bot runned {botThread.times_runned} times", 4, 4, 2,)


    def btn_reset_times_runned(botThread):
        WidgetBuilder.build_widget(botThread.root, Button, "Reset counter", 4, 2, 2, command=lambda: botThread.resetTimesRunned())

    def label_info(botThread):
        WidgetBuilder.destroy_widget(botThread.root, 3, 4)
        if botThread.image_was_detected == False:
            WidgetBuilder.build_widget(botThread.root, Label, "Image not detected!", 3, 4, foreground='red')
            return

        if botThread.is_running:
            WidgetBuilder.build_widget(botThread.root, Label, "Bot is running", 3, 4, foreground='green')
        else:
            WidgetBuilder.build_widget(botThread.root, Label, "Bot is not running", 3, 4, foreground='red')
    
    def label_running_in(botThread):
        if botThread.is_running == False:
            return
        
        WidgetBuilder.destroy_widget(botThread.root, 6, 4)

        if botThread.running_in > 0:
            WidgetBuilder.build_widget(botThread.root, Label, f"Running in {botThread.running_in} seconds", 6, 4)
            botThread.running_in -= 1
            botThread.root.after(1000, lambda: InterfaceUnlockedBuilder.label_running_in(botThread))
        else:
            WidgetBuilder.build_widget(botThread.root, Label, f"Running...", 6, 4)
            return

class BotInterfaceBuilder:

    def __init__(self):
         self.unlocked_interfaces = None
         pass

    def build(botThread):
            BotInterfaceBuilder.style()
            BotInterfaceBuilder.detect_image_btn(botThread)
            BotInterfaceBuilder.exit_bnt(botThread)
            BotInterfaceBuilder.label_info(botThread)

    def unlock_interface(self, botThread):
        self.unlocked_interfaces = InterfaceUnlockedBuilder
        self.unlocked_interfaces.build(botThread)

    def count_running__time(self, botThread):
        self.unlocked_interfaces.start_running_for(botThread)


    def style():
            style = Style()
            style.configure('E.TButton', font=('calibri', 10, 'bold'), foreground='red')
            style.configure('S.TButton', font=('calibri', 10, 'bold'), foreground='green')
            style.map('E.TButton', foreground=[('active', 'red')], background=[('active', 'red')])  
            style.map('S.TButton', foreground=[('active', 'green')], background=[('active', 'green')])
            return style

    def detect_image_btn(botThread):
            WidgetBuilder.build_widget(botThread.root, Button, "Detect image", 3, 3, command=lambda: botThread.detectImage())

    def label_info(botThread):
        WidgetBuilder.destroy_widget(botThread.root, 3, 4)
        if botThread.image_was_detected == False:
            WidgetBuilder.build_widget(botThread.root, Label, "Image not detected", 3, 4, foreground='red')
            return

        if botThread.is_running:
            WidgetBuilder.build_widget(botThread.root, Label, "Bot is running", 3, 4, foreground='green')
        else:
            WidgetBuilder.build_widget(botThread.root, Label, "Bot is not running", 3, 4, foreground='red')
    
    def exit_bnt(botThread):
        WidgetBuilder.build_widget(botThread.root, Button, "Exit", 6, 2, 2, style='E.TButton', command=lambda: botThread.exit())