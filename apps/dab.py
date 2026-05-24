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
        print("Starting welle on channel:", self.channel)
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

    def is_welle_running(self):
        return self.welle_proc is not None and self.welle_proc.poll() is None

    def tune_channel(self, channel):
        if self.channel == channel and self.is_welle_running():
            return

        self.stop_welle()
        self.channel = channel
        self.start_welle()

    def play_station(self, station):
        channel = station["channelName"]
        sid = self.normalise_sid(station["stationSId"])
        
        if self.channel != channel or not self.is_welle_running():
            self.stop_audio()
            self.tune_channel(channel)
        else:
            self.stop_audio()
            
        stream_url = f"{self.base_url}/mp3/{sid}"
        
        self.audio_proc = subprocess.Popen(
            ["mpv", stream_url],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        self.current_sid = sid
        self.current_station = station["stationName"]
        return True

    def normalise_sid(self, sid):
        if isinstance(sid, str):
            sid = sid.strip()
            if sid.lower().startswith("0x"):
                return int(sid, 16)
            return int(sid)
        return int(sid)

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

    def toggle_station(self, station):
        station_name = station["stationName"]
        sid = station["stationSId"]

        if self.current_sid == sid:
            self.stop_audio()
            return False

        return self.play_station(station)

    def get_station_list(self):
        
        with open('data/stations.json', 'r') as f:
            stations = json.load(f)

        return stations

    def get_current_service_info(self):
        if not self.current_sid:
            return None

        data = self.get_mux_info()
        if not data:
            return None

        for service in data.get("services", []):
            service_sid = self.normalise_sid(service.get("sid"))
            if service_sid == self.current_sid:
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
