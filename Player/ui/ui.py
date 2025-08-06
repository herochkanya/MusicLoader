from kivy.uix.screenmanager import ScreenManager, Screen
from ui.downloader import DownloaderUI
from config import load_screen

# Main screen for the app
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Here add an ui

# Downloaser (startup) screen
class DownloaderScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Add to the screen the DownloaderUI class
        self.add_widget(DownloaderUI())

# Main application UI manager
class AppUI(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MainScreen(name='main'))
        self.add_widget(DownloaderScreen(name='downloader'))

    def choose_screen(self):
        if load_screen == 'downloader':
            self.current = 'downloader'
        elif load_screen == 'main':
            self.current = 'main'
