#!/usr/bin/env python3
from app import create_app
from app.models import init_db
import threading
import time
import webview
from flask import render_template
from werkzeug.serving import make_server

# Flask uygulamasını oluştur
app = create_app()

# Ana sayfa route'u
@app.route("/")
def home():
    return render_template('index.html')

class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.app = app
        self.server = make_server('127.0.0.1', 5002, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        with self.app.app_context():
            # Veritabanını başlat
            init_db()
            # Sunucuyu başlat
            self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()

def start_server():
    global server
    server = ServerThread(app)
    server.start()
    time.sleep(1)
    return server

if __name__ == "__main__":
    # Sunucuyu başlat
    server = start_server()
    
    try:
        # Webview penceresini oluştur ve başlat
        webview.create_window(
            "Pisi GNU/Linux Gönüllü V1.0",
            "http://127.0.0.1:5002/",
            width=1200,
            height=800,
            resizable=True,
            min_size=(800, 600)
        )
        webview.start(gui='qt')
    except KeyboardInterrupt:
        print("\nUygulama kapatılıyor...")
    finally:
        # Uygulama kapatıldığında sunucuyu durdur
        server.shutdown()