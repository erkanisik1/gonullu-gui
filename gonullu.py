from login import LoginWindow
from mainwindow import MainWindow

# Global referanslar
app_instance = None
main_window = None

class App:
    def __init__(self):
        self.login_win = LoginWindow(self.on_login_success)
        self.main_win = None
    
    def on_login_success(self, master_root):
        """Login başarılı olduğunda ana pencereyi aç"""
        print("Login başarılı, ana pencere açılıyor...")
        self.main_win = MainWindow(master_root)
        self.main_win.show()
    
    def run(self):
        """Uygulamayı başlat"""
        self.login_win.show()

if __name__ == "__main__":
    app = App()
    app.run()

