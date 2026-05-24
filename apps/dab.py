import subprocess
import json
import time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

class DabManager:
    def __init__(self, channel="12A", port=8000):
        self.channel = channel
        self.port = port
        self.base_url = f"http://127.0.0.1:{port}"

        self.welle_proc = None
        self.audio_proc = None

        self.services = []
        self.current_sid = None
        self.current_station = None

    def start_welle(self):
        if self.welle_proc and self.welle_proc.poll() is None:
            return

        self.welle_proc = subprocess.Popen(
            ["welle-cli", "-c", self.channel, "-w", str(self.port)],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
            text=True
        )

        time.sleep(2)

    def stop_welle(self):
        self.stop_audio()

        if self.welle_proc and self.welle_proc.poll() is None:
            self.welle_proc.terminate()
            try:
                self.welle_proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.welle_proc.kill()
                self.welle_proc.wait()

        self.welle_proc = None

    def get_mux_info(self):
        try:
            with urlopen(f"{self.base_url}/mux.json", timeout=0.5) as response:
                return json.loads(response.read().decode("utf-8"))
        except (URLError, HTTPError, TimeoutError, json.JSONDecodeError):
            return None

    def refresh_services(self):
        data = self.get_mux_info()
        if not data:
            return []

        self.services = data.get("services", [])
        return self.services

    def find_service_by_name(self, station_name):
        self.refresh_services()

        wanted = station_name.strip().lower()

        for service in self.services:
            label = service["label"]["label"].strip().lower()
            shortlabel = service["label"]["shortlabel"].strip().lower()

            if wanted in (label, shortlabel):
                return service

        return None

    def play_station(self, station_name):
        self.start_welle()

        service = self.find_service_by_name(station_name)
        if not service:
            return False

        sid = service["sid"]
        url_mp3 = service.get("url_mp3", f"/mp3/{sid}")
        stream_url = f"{self.base_url}{url_mp3}"

        self.stop_audio()

        self.audio_proc = subprocess.Popen(
            ["mpg123", "-q", stream_url],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

        self.current_sid = sid
        self.current_station = service["label"]["label"].strip()

        return True

    def stop_audio(self):
        if self.audio_proc and self.audio_proc.poll() is None:
            self.audio_proc.terminate()
            try:
                self.audio_proc.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self.audio_proc.kill()
                self.audio_proc.wait()

        self.audio_proc = None
        self.current_sid = None
        self.current_station = None

    def toggle_station(self, station_name):
        if self.current_station and self.current_station.strip().lower() == station_name.strip().lower():
            self.stop_audio()
            return False

        return self.play_station(station_name)

    def get_current_service_info(self):
        if not self.current_sid:
            return None

        data = self.get_mux_info()
        if not data:
            return None

        for service in data.get("services", []):
            if service.get("sid") == self.current_sid:
                return {
                    "station": service["label"]["label"].strip(),
                    "shortlabel": service["label"]["shortlabel"].strip(),
                    "sid": service["sid"],
                    "bitrate": service["components"][0]["subchannel"]["bitrate"],
                    "protection": service["components"][0]["subchannel"]["protection"],
                    "codec": service["components"][0]["ascty"],
                    "pty": service.get("ptystring", ""),
                    "dls": service.get("dls", {}).get("label", ""),
                    "audio_left": service.get("audiolevel", {}).get("left", -1),
                    "audio_right": service.get("audiolevel", {}).get("right", -1),
                    "frame_errors": service.get("errorcounters", {}).get("frameerrors", 0),
                    "rs_errors": service.get("errorcounters", {}).get("rserrors", 0),
                    "aac_errors": service.get("errorcounters", {}).get("aacerrors", 0),
                    "snr": data.get("demodulator", {}).get("snr"),
                    "frequency_correction": data.get("demodulator", {}).get("frequencycorrection"),
                    "fic_crc_errors": data.get("demodulator", {}).get("fic", {}).get("numcrcerrors"),
                    "ensemble": data.get("ensemble", {}).get("label", {}).get("label", ""),
                    "gain": data.get("receiver", {}).get("hardware", {}).get("gain"),
                }

        return None
