import subprocess
import json

class DabManager:
    def __init__(self):
        self.station_list = []
        self.proc = None
        
        self.station_list = self.get_stations()
    
    def get_stations(self):
        
        with open('data/stations.json', 'r') as f:
            station_list = json.load(f)
        
        return station_list

    def stop(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait()
                
        self.proc = None

    def play_station(self, stationName, channelName):
        self.stop()
        
        self.proc = subprocess.Popen(
            ["welle-cli", "-c", channelName, "-p", stationName],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            text=True
        )
    
    def get_stream_info(self):
        pass
