import time
import threading
import json
import os
from statistics import mean, stdev

class MouseAnalyzer:
    """
    {
      "event": "click" | "move" | ...,
      "device_timestamp": 1690000000.123,   
      "server_timestamp": 1690000000.456,  
      "roundtrip_ms": 12.3,                 
      "sample_id": "optional id",
      "notes": "..."
    }
    """
    def __init__(self, save_dir=None, window_size=1000):
        self.save_dir = save_dir or os.environ.get('PHONE_MOUSE_UPLOAD_DIR', '/tmp/phone_mouse_uploads')
        os.makedirs(self.save_dir, exist_ok=True)
        self.lock = threading.Lock()
        self.samples = []
        self.window_size = int(window_size)

    def add_sample(self, sample: dict):
        s = dict(sample)
        if 'server_timestamp' not in s:
            s['server_timestamp'] = time.time()
        if 'device_timestamp' in s and isinstance(s['device_timestamp'], (int,float)):
            s['device_to_server_ms'] = (s['server_timestamp'] - s['device_timestamp']) * 1000.0
        if 'roundtrip_ms' in s:
            try:
                s['roundtrip_ms'] = float(s['roundtrip_ms'])
            except:
                s['roundtrip_ms'] = None
        with self.lock:
            self.samples.append(s)
            if len(self.samples) > self.window_size:
                self.samples = self.samples[-self.window_size:]
        try:
            fname = os.path.join(self.save_dir, "mouse_samples.log")
            with open(fname, "a", encoding="utf-8") as f:
                f.write(json.dumps(s, ensure_ascii=False) + "\n")
        except Exception:
            pass
        return s

    def clear(self):
        with self.lock:
            self.samples = []

    def summary(self):
        with self.lock:
            samples = list(self.samples)
        total = len(samples)
        by_event = {}
        device_to_server = [s.get('device_to_server_ms') for s in samples if s.get('device_to_server_ms') is not None]
        rts = [s.get('roundtrip_ms') for s in samples if s.get('roundtrip_ms') is not None]
        for s in samples:
            e = s.get('event','unknown')
            by_event.setdefault(e,0)
            by_event[e]+=1
        def stats_list(values):
            if not values:
                return {}
            try:
                return {
                    'count': len(values),
                    'mean_ms': mean(values),
                    'stdev_ms': stdev(values) if len(values) > 1 else 0.0,
                    'min_ms': min(values),
                    'max_ms': max(values)
                }
            except Exception:
                return {}
        return {
            'total_samples': total,
            'by_event': by_event,
            'device_to_server': stats_list(device_to_server),
            'roundtrip': stats_list(rts),
            'suggestions': self._suggestions(device_to_server, rts)
        }

    def _suggestions(self, device_to_server, rts):
        suggestions = []
        if device_to_server and mean(device_to_server) > 100:
            suggestions.append("Latência device→server alta. Sugere-se verificar rede Wi-Fi local ou reduzir payload.")
        if rts and mean(rts) > 80:
            suggestions.append("Roundtrip alto. Verifique qualidade da rede ou otimize Bluetooth LE no dispositivo.")
        if rts and len(rts) > 1 and stdev(rts) > 20:
            suggestions.append("Jitter alto detectado. Sugere-se suavizar medições e verificar interferência na rede.")
        if not suggestions:
            suggestions.append("Latência aceitável. Colete mais amostras para melhor precisão.")
        return suggestions