from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.event import EventDispatcher
import os

from core.downloader import download_audio
from config import MUSIC_DIR


class DownloaderUI(BoxLayout, EventDispatcher):
    # Adding all ui elements
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)
        self.register_event_type('on_success_download')

        # Url input
        self.url_input = TextInput(
            font_size=20,
            size_hint_y=None,
            height=100,
            hint_text='Paste your Youtube link here',
            multiline=False
        )
        self.url_input.bind(on_text_validate=self.on_enter)

        # Folder input
        self.folder_input = TextInput(
            font_size=16,
            size_hint_y=None,
            height=40,
            hint_text='Enter or select folder name',
            multiline=False
        )

        # List of folders
        self.folders_scroll = ScrollView(size_hint=(1, None), height=100)
        self.folders_list = GridLayout(cols=1, spacing=4, size_hint_y=None)
        self.folders_list.bind(minimum_height=self.folders_list.setter('height'))
        self.folders_scroll.add_widget(self.folders_list)

        self.refresh_folders_list()

        # Download button
        download_btn = Button(
            text='Download',
            size_hint_y=None,
            height=60
        )
        download_btn.bind(on_release=self.on_download)

        # Status label (mini debug)
        self.status_label = Label(
            text='Ready to download',
            size_hint_y=None,
            height=60
        )

        self.add_widget(self.url_input)
        self.add_widget(self.folder_input)
        self.add_widget(self.folders_scroll)
        self.add_widget(download_btn)
        self.add_widget(self.status_label)

    # Adding new folders and refreshing the list with buttons
    def refresh_folders_list(self):
        # Creating base folder if it doesn't exist
        self.folders_list.clear_widgets()
        if not os.path.exists(MUSIC_DIR):
            os.makedirs(MUSIC_DIR)
        # Creating input folders if they don't exist
        # Creating buttons for each folder
        for folder_name in sorted(os.listdir(MUSIC_DIR)):
            folder_path = os.path.join(MUSIC_DIR, folder_name)
            if os.path.isdir(folder_path):
                btn = Button(text=folder_name, size_hint_y=None, height=30)
                btn.bind(on_release=lambda btn_instance: self.on_folder_select(btn_instance.text))
                self.folders_list.add_widget(btn)

    # Paste folder name into input
    def on_folder_select(self, folder_name):
        self.folder_input.text = folder_name

    # Start download on enter
    def on_enter(self, instance):
        self.on_download(None)

    # In-ui download logic
    def on_download(self, instance):
        # Get URL and folder name from inputs
        url = self.url_input.text.strip()
        # Base (downloads) dir if input is empty
        folder = self.folder_input.text.strip() or 'downloads'

        if not url:
            self.status_label.text = "❌ Enter URL!"
            return

        self.status_label.text = "⏳ Downloading..."

        # Use def from core/downloader.py
        result = download_audio(url, target_folder=folder)

        # If download was successful or an error occurred, update the status label
        if result:
            if isinstance(result, list):
                # Plalist downloaded, show summary
                self.status_label.text = f"✅ Playlist downloaded: {len(result)} tracks saved to '{folder}'"
            else:
                title = result.get("title", "Unknown")
                artist = result.get("artist", "Unknown artist")
                self.status_label.text = f"✅ {title} — {artist} (saved to '{folder}')"
            self.refresh_folders_list()
            self.dispatch('on_success_download', result)
        else:
            self.status_label.text = "❌ Error while loading!"

    def on_success_download(self, track_info):
        pass
