from kivy.app import App
from ui.ui import AppUI

class PlayerApp(App):
    def build(self):
        app_ui = AppUI()
        # Open downloader screen on start
        app_ui.choose_screen()
        return app_ui


if __name__ == '__main__':
    PlayerApp().run()
