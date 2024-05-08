from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from pytube import YouTube
import threading

class VideoDownloader(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.url_input = TextInput(hint_text='Enter YouTube video URL')
        self.download_button = Button(text='Download Video')
        self.status_label = Label(text='Ready to download')

        self.download_button.bind(on_press=self.download_video)

        self.add_widget(self.url_input)
        self.add_widget(self.download_button)
        self.add_widget(self.status_label)

    def download_video(self, instance):
        video_url = self.url_input.text

        # Update status label
        self.status_label.text = 'Downloading...'

        # Use threading to avoid blocking the Kivy event loop
        threading.Thread(target=self._download_video_thread, args=(video_url,)).start()

    def _download_video_thread(self, video_url):
        try:
            yt = YouTube(video_url)
            stream = yt.streams.get_highest_resolution()
            stream.download()  # Downloads to the current directory
            self._update_status('Download complete!')
        except Exception as e:
            self._update_status(f'Error: {e}')

    def _update_status(self, message):
        # Update the label from a separate thread
        Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', message))

class YouTubeDownloaderApp(App):
    def build(self):
        return VideoDownloader()

if __name__ == '__main__':
    YouTubeDownloaderApp().run()
