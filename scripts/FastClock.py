import java
import java.beans
import jmri
import json
import httplib
from yaml import load, Loader

# First, define the listener.  This one just prints some
# information on the change, but more complicated code is
# of course possible.
timebase = jmri.InstanceManager.getDefault(jmri.Timebase)
class TimeListener(java.beans.PropertyChangeListener):
    lightIncrimenter = 0
    _lightChangeInterval = 15

    def __init__(self, lightChangeInterval):
        self._lightChangeInterval = lightChangeInterval

    def sunrise(self):
        self.lightUpdate('sunrise')

    def noon(self):
        self.lightUpdate('noon')

    def evening(self):
        self.lightUpdate('evening')

    def sunset(self):
        self.lightUpdate('sunset')

    def moon(self):
        self.lightUpdate('moon')

    def lightUpdate(self, time):
        url = 'api/v1/' + time
        hdr = {"content-type": "application/json"}
        conn = httplib.HTTPConnection("127.0.0.1:5000")
        conn.request('POST', url , json.dumps({"data": "nothing"}), hdr)
        res = conn.getresponse()
        if res.status != 200:
            print("API ERROR")
            print("-------------------------------------")
            print(res.status)
            print("-------------------------------------")
            print(res.reason)
        data = res.read()
        print(data)
        conn.close()
        return

    def incrimentLights(self):
        self.lightIncrimenter += 1
        if self.lightIncrimenter == 1:
            self.sunrise()
        elif self.lightIncrimenter == 2:
            self.noon()
        elif self.lightIncrimenter == 3:
            self.evening()
        elif self.lightIncrimenter == 4:
            self.sunset()
        elif self.lightIncrimenter == 5:
            self.lightIncrimenter = 0
            self.moon()
        else:
            self.lightIncrimenter = 0
        return

    def propertyChange(self, event):
        print ("change",event.propertyName)
        print ("from", event.oldValue, "to", event.newValue)
        if (event.newValue % self._lightChangeInterval == 0):
            self.incrimentLights()
        if (event.newValue == 0 or event.newValue== 30):
            print ('incriment lights')
        return
stream = open("config.yaml", "r", encoding="uft-8")
config = load(stream, Loader=Loader)
stream.close()
if len(config) > 0:
    timebase.addMinuteChangeListener(TimeListener(config["interval"]))
else:
    timebase.addMinuteChangeListener(TimeListener(15))
