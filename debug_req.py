import urllib.request
import urllib.parse
import urllib.error

routes = ['/', '/login', '/flights?source=JFK&destination=LAX']

for r in routes:
    req = urllib.request.Request('https://ai-flight-booking-system.vercel.app' + r)
    try:
        resp = urllib.request.urlopen(req)
        print(f"{r} -> HTTP {resp.getcode()}")
    except urllib.error.HTTPError as e:
        print(f"{r} -> HTTP Error: {e.code}")
    except Exception as e:
        print(f"{r} -> Other Exception: {e}")
