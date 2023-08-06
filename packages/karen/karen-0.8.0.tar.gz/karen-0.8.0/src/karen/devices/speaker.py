import os
import logging
import tempfile
from karen.shared import threaded
from karen import GenericDevice


class Speaker(GenericDevice):
    """
    Speaker device to convert any text to speech send to the audio output device.
    """
    
    def __init__(
            self, 
            parent=None,
            callback=None):
        """
        Speaker Initialization

        Args:
            parent (object): Containing object's reference.  Normally this would be the device container. (optional)
            callback (function): Callback function for which to send any captured data.
        """

        super(Speaker, self).__init__(parent=parent, callback=callback)
                
        from karen import __version__
        self.version = __version__
        
        self._packageName = "karen"
        
        # Local variable instantiation and initialization
        self.type = "SPEAKER"
        self.logger = logging.getLogger(self.type)
        
    @threaded
    def _doCallback(self, inData):
        """
        Calls the specified callback as a thread to keep from blocking additional processing.

        Args:
            text (str):  Text to send to callback function
        
        Returns:
            (thread):  The thread on which the callback is created to be sent to avoid blocking calls.
        """

        try:
            if self.callback is not None:
                self.callback("SPEAKER_INPUT", inData, deviceId=self.deviceId)
        except Exception:
            pass
        
        return
    
    def say(self, text):
        """
        Sends text to the festival executable to be translated and sent to the audio device.
        
        Args:
            text (str):  The text to convert into speech.
            
        Returns:
            (bool): True on success else raises exception.
        """
        
        if self._isRunning:
            fd, say_file = tempfile.mkstemp()
                
            with open(say_file, 'w') as f:
                f.write(str(text)) 
                
            self.logger.info("SAYING " + str(text))
            os.system("festival --tts " + say_file )
            os.close(fd)
        
        return True
    
    def accepts(self):
        return ["start", "stop", "speak"]
        
    def isRunning(self):
        """
        Identifies if the device is actively running.

        Returns:
            (bool):  True if running; False if not running.
        """

        return self._isRunning
    
    def speak(self, httpRequest=None):
        """
        Accepts inbound commands from Brain and sends to standard "say()" function.

        Args:
            httpRequest (KHTTPHandler): Handler for inbound request.

        Returns:
            (bool):  True on success else will raise an exception.
        """
        
        if httpRequest.isJSON:
            data = httpRequest.JSONData
            if data is not None:
                if "text" in data:
                    self.say(str(data["text"]))
        return True
    
    def stop(self, httpRequest=None):
        """
        Stops the speaker.  Function provided for compatibility as speaker does not require a daemon.
        
        Args:
            httpRequest (KHTTPHandler): Handler for inbound request.  Not used.

        Returns:
            (bool):  True on success else will raise an exception.
        """
        self._isRunning = False
        return True
        
    def start(self, httpRequest=None, useThreads=True):
        """
        Starts the speaker.  Function provided for compatibility as speaker does not require a daemon.

        Args:
            httpRequest (KHTTPHandler): Handler for inbound request.  Not used.
            useThreads (bool):  Indicates if the brain should be started on a new thread.
        
        Returns:
            (bool):  True on success else will raise an exception.
        """
        self._isRunning = True
        
        return True
    
    def wait(self, seconds=0):
        """
        Waits for any active speakers to complete before closing.  Provided for compatibility as speaker does not requrie a daemon.
        
        Args:
            seconds (int):  Number of seconds to wait before calling the "stop()" function
            
        Returns:
            (bool):  True on success else will raise an exception.
        """
        return True