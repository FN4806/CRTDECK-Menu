import subprocess
import json
import time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
import os
import signal

import logging

logging.basicConfig(
    filename="dab_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s"
)

log = logging.getLogger("dab")

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

        cmd = ["welle-cli", "-c", self.channel, "-w", str(self.port)]
        log.debug(f"Running: {cmd}")

        self.welle_proc = subprocess.Popen(
            cmd,
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
            os.killpg(os.getpgid(self.welle_proc.pid), signal.SIGTERM)
            try:
                self.welle_proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                os.killpg(os.getpgid(self.welle_proc.pid), signal.SIGKILL)
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
        channel = channel.strip().upper()
        if self.channel == channel and self.is_welle_running():
            return

        self.stop_audio()
        self.stop_welle()
        time.sleep(0.5)
        self.channel = channel
        self.start_welle()
        
        for _ in range(10):
            data = self.get_mux_info()
            if data and data.get("services"):
                log.debug("Locked ensemble: %s", data.get("ensemble", {}).get("label", {}).get("label"))
                log.debug("SIDs: %s", [s.get("sid") for s in data.get("services", [])])
                return
            time.sleep(0.5)

        log.debug(f"No services found on {self.channel}")
        
        time.sleep(2.5)

    def play_station(self, station):
        channel = station["channelName"]
        sid = self.normalise_sid(station["stationSId"])
        
        self.tune_channel(channel)
        
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
        sid = self.normalise_sid(station["stationSId"])

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
                
                dls = service.get("dls") or {}
                audiolevel = service.get("audiolevel") or {}
                errorcounters = service.get("errorcounters") or {}
                demodulator = data.get("demodulator") or {}
                fic = demodulator.get("fic") or {}
                ensemble = data.get("ensemble") or {}
                ensemble_label = ensemble.get("label") or {}
                receiver = data.get("receiver") or {}
                hardware = receiver.get("hardware") or {}
                
                return {
                    "station": service["label"]["label"].strip(),
                    "shortlabel": service["label"]["shortlabel"].strip(),
                    "sid": service["sid"],
                    "bitrate": service["components"][0]["subchannel"]["bitrate"],
                    "protection": service["components"][0]["subchannel"]["protection"],
                    "codec": service["components"][0]["ascty"],
                    "pty": service.get("ptystring", ""),
                    "dls": dls.get("label", ""),
                    "audio_left": audiolevel.get("left", -1),
                    "audio_right": audiolevel.get("right", -1),
                    "frame_errors": errorcounters.get("frameerrors", 0),
                    "rs_errors": errorcounters.get("rserrors", 0),
                    "aac_errors": errorcounters.get("aacerrors", 0),
                    "snr": demodulator.get("snr"),
                    "frequency_correction": demodulator.get("frequencycorrection"),
                    "fic_crc_errors": fic.get("numcrcerrors"),
                    "ensemble": ensemble_label.get("label", ""),
                    "gain": hardware.get("gain"),
                }

        return None
