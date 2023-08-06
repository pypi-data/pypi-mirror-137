import os
import logging
import tempfile
import traceback
import sys
import numpy as np
import time
import json
from karen.shared import threaded, py_error_handler, SilenceStream, TCPStreamingClient
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
        return self._isRunning
    
    def speak(self, httpRequest=None):
        if httpRequest.isJSON:
            data = httpRequest.JSONData
            if data is not None:
                if "text" in data:
                    self.say(str(data["text"]))
        return True
    
    def stop(self, httpRequest=None):
        """
        Stops the speaker.  Function provided for compatibility as speaker does not require a daemon.
        
        Returns:
            (bool):  True on success else will raise an exception.
        """
        self._isRunning = False
        return True
        
    def start(self, httpRequest=None, useThreads=True):
        """
        Starts the speaker.  Function provided for compatibility as speaker does not require a daemon.

        Args:
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


try:
    import pyaudio
    import queue
    import webrtcvad
    import collections
    import deepspeech
    from ctypes import CFUNCTYPE, cdll, c_char_p, c_int

    class Listener():
        """
        Listener device to capture audio from microphone and convert any speech to text and send to callback method.
        """
        
        def __init__(
                self, 
                parent=None,
                speechModel=None,           # Speech Model file.  Ideally this could be searched for in a default location
                speechScorer=None,          # Scorer file.  Okay for this to be None as scorer file is not required
                audioChannels=1,            # VAD requires this to be 1 channel
                audioSampleRate=16000,      # VAD requires this to be 16000
                vadAggressiveness=1,        # VAD accepts 1 thru 3
                speechRatio=0.75,           # Must be between 0 and 1 as a decimal
                speechBufferSize=50,        # Buffer size for speech frames
                speechBufferPadding=350,    # Padding, in milliseconds, of speech frames
                audioDeviceIndex=None,
                callback=None):             # Callback is a function that accepts ONE positional argument which will contain the text identified
            """
            Listener Initialization

            Args:
                parent (object): Containing object's reference.  Normally this would be the device container. (optional)
                speechModel (str):  Path and filename of Deepspeech Speech Model file.  If not set then listener will do a 
                    basic seach for the PBMM or TFLite file.
                speechScorer (str):  Path and filename of Deepspeech Scorer file.  Okay for this to be None as scorer file is not required.
                audioChannels (int):  Audio channels for audio source.  VAD requires this to be 1 channel.
                audioSampleRate (int): Audio sample rate of audio source.  VAD requires this to be 16000.
                vadAggressiveness (int): Voice Activity Detection (VAD) aggressiveness for filtering noise.  Accepts 1 thru 3.
                speechRatio (float): Must be between 0 and 1 as a decimal
                speechBufferSize (int): Buffer size for speech frames
                speechBufferPadding (int): Padding, in milliseconds, of speech frames
                audioDeviceIndex (int): Listening device index number.  If not set then will use default audio capture device.
                callback (function): Callback function for which to send capture text    
            """

            from karen import __version__
            self.version = __version__
            
            self._packageName = "karen"

            # Local variable instantiation and initialization
            self.type = "LISTENER"
            self.callback = callback
            self.logger = logging.getLogger(self.type)
            self.parent = parent
            
            self.speechModel = speechModel
            self.speechScorer = speechScorer                  
            self.audioChannels = audioChannels                
            self.audioSampleRate = audioSampleRate            
            self.vadAggressiveness = vadAggressiveness        
            self.speechRatio = speechRatio                    
            self.speechBufferSize = speechBufferSize          
            self.speechBufferPadding = speechBufferPadding
            self.audioDeviceIndex = audioDeviceIndex

            if self.speechModel is None:
                # Search for speech model?
                self.logger.info("Speech model not specified.  Attempting to use defaults.")
                local_path = os.path.join(os.path.expanduser("~/.karen"), "data", "models", "speech")
                os.makedirs(local_path, exist_ok=True)
                
                files = os.listdir(local_path)
                files = sorted(files, reverse=True)  # Very poor attempt to get the latest version of the model if multiple exist.
                bFoundPBMM = False 
                bFoundTFLITE = False
                for file in files:
                    if not bFoundPBMM:
                        if file.startswith("deepspeech") and file.endswith("models.pbmm"):
                            self.speechModel = os.path.abspath(os.path.join(local_path, file))
                            self.logger.debug("Using speech model from " + str(self.speechModel))
                            bFoundPBMM = True
                            
                    if not bFoundPBMM and not bFoundTFLITE:
                        if file.startswith("deepspeech") and file.endswith("models.tflite"):
                            self.speechModel = os.path.abspath(os.path.join(local_path, file))
                            self.logger.debug("Using speech model from " + str(self.speechModel))
                            bFoundTFLITE = True

                    if self.speechScorer is None:
                        if file.startswith("deepspeech") and file.endswith("models.scorer"):
                            self.speechScorer = os.path.abspath(os.path.join(local_path, file))
                            self.logger.debug("Using speech scorer from " + str(self.speechScorer))
            
                if bFoundPBMM and bFoundTFLITE:
                    self.logger.warning("Found both PBMM and TFLite deepspeech models.")
                    self.logger.warning("Defaulting to PBMM model which will not work with Raspberry Pi devices.")
                    self.logger.warning("To use with RPi either delete the PBMM model or specify the TFLite model explicitly.")
                    
            if self.speechModel is None:
                # FIXME: Should we try to download the models if they don't exist?
                raise Exception("Invalid speech model.  Unable to start listener.")
            
            self.stream = None
            self.thread = None
            self._isRunning = False 
            self._isAudioOut = False 
            
        @threaded
        def _doCallback(self, inData):
            """
            Calls the specified callback as a thread to keep from blocking audio device listening

            Args:
                text (str):  Text to send to callback function
            
            Returns:
                (thread):  The thread on which the callback is created to be sent to avoid blocking calls.
            """

            try:
                if self.callback is not None:
                    self.callback("AUDIO_INPUT", inData)
            except Exception:
                pass
            
            return

        @threaded
        def _readFromMic(self):
            """
            Opens audio device for listening and processing speech to text
            
            Returns:
                (thread):  The thread created for the listener while listening for incoming speech.
            """
        
            buffer_queue = queue.Queue()    # Buffer queue for incoming frames of audio
            self._isRunning = True   # Reset to True to insure we can successfully start
        
            def proxy_callback(in_data, frame_count, time_info, status):
                """Callback for the audio capture which adds the incoming audio frames to the buffer queue"""
                
                # Save captured frames to buffer
                buffer_queue.put(in_data)
                
                # Tell the caller that it can continue capturing frames
                return (None, pyaudio.paContinue)
        
            # Using a collections queue to enable fast response to processing items.
            # The collections class is simply faster at handling this data than a simple dict or array.
            # The size of the buffer is the length of the padding and thereby those chunks of audio.
            ring_buffer = collections.deque(
                maxlen=self.speechBufferPadding // (1000 * int(self.audioSampleRate / float(self.speechBufferSize)) // self.audioSampleRate))
        
            # Set up C lib error handler for Alsa programs to trap errors from Alsa spin up
            with SilenceStream(sys.stderr, log_file="/dev/null"):
                _model = deepspeech.Model(self.speechModel)
                if self.speechScorer is not None:
                    _model.enableExternalScorer(self.speechScorer)
                
            _vad = webrtcvad.Vad(self.vadAggressiveness)
            
            ERROR_HANDLER_FUNC = CFUNCTYPE(None, c_char_p, c_int, c_char_p, c_int, c_char_p)
            c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)
            asound = cdll.LoadLibrary('libasound.so')
            asound.snd_lib_error_set_handler(c_error_handler)
            
            _audio_device = pyaudio.PyAudio()
            
            # Open a stream on the audio device for reading frames
            self.stream = _audio_device.open(
                format=pyaudio.paInt16,
                channels=self.audioChannels,
                rate=self.audioSampleRate,
                input=True,
                frames_per_buffer=int(self.audioSampleRate / float(self.speechBufferSize)),
                input_device_index=self.audioDeviceIndex,
                stream_callback=proxy_callback)
            
            self.stream.start_stream()                               # Open audio device stream
            
            # Context of audio frames is used to better identify the spoken words.
            stream_context = _model.createStream()
            
            # Used to flag whether we are above or below the ratio threshold set for speech frames to total frames
            triggered = False
            
            self.logger.info("Started")
            
            # We will loop looking for incoming audio until the KILL_SWITCH is set to True
            while self._isRunning:
        
                # Get current data in buffer as an audio frame
                frame = buffer_queue.get()
        
                # A lot of the following code was pulled from examples on DeepSpeech
                # https://github.com/mozilla/DeepSpeech-examples/blob/r0.7/mic_vad_streaming/mic_vad_streaming.py
                
                # Important note that the frame lengths must be specific sizes for VAD detection to work.
                # Voice Activity Detection (VAD) also expects single channel input at specific rates.
                # Highly recommend reading up on webrtcvad() before adjusting any of this.
                
                # We also skip this process if we are actively sending audio to the output device to avoid
                # looping and thus listening to ourselves.
                if len(frame) >= 640 and not self._isAudioOut:
                    
                    # Bool to determine if this frame includes speech.
                    # This only determines if the frame has speech, it does not translate to text.
                    is_speech = _vad.is_speech(frame, self.audioSampleRate)

                    # Trigger is set for first frame that contains speech and remains triggered until 
                    # we fall below the allowed ratio of speech frames to total frames
        
                    if not triggered:
        
                        # Save the frame to the buffer along with an indication of if it is speech (or not)
                        ring_buffer.append((frame, is_speech))
        
                        # Get the number of frames with speech in them
                        num_voiced = len([f for f, speech in ring_buffer if speech])
        
                        # Compare frames with speech to the expected number of frames with speech
                        if num_voiced > self.speechRatio * ring_buffer.maxlen:
                            
                            # We have more speech than the ratio so we start listening
                            triggered = True
        
                            # Feed data into the deepspeech model for determing the words used
                            for f in ring_buffer:
                                stream_context.feedAudioContent(np.frombuffer(f[0], np.int16))
        
                            # Since we've now fed every frame in the buffer to the deepspeech model
                            # we no longer need the frames collected up to this point
                            ring_buffer.clear()
                
                    else:
                        # We only get here after we've identified we have enough frames to cross the threshold
                        # for the supplied ratio of speech to total frames.  Thus we can safely keep feeding
                        # incoming frames into the deepspeech model until we fall below the threshold again.
                        
                        # Feed to deepspeech model the incoming frame
                        stream_context.feedAudioContent(np.frombuffer(frame, np.int16))
        
                        # Save to ring buffer for calculating the ratio of speech to total frames with speech
                        ring_buffer.append((frame, is_speech))
                        
                        # We have a full collection of frames so now we loop through them to recalculate our total
                        # number of non-spoken frames (as I pulled from an example this could easily be stated as
                        # the inverse of the calculation in the code block above)
                        num_unvoiced = len([f for f, speech in ring_buffer if not speech])
        
                        # Compare our calculated value with the ratio.  In this case we're doing the opposite
                        # of the calculation in the previous code block by looking for frames without speech
                        if num_unvoiced > self.speechRatio * ring_buffer.maxlen:
                            
                            # We have fallen below the threshold for speech per frame ratio
                            triggered = False
                            
                            # Let's see if we heard anything that can be translated to words.
                            # This is the invocation of the deepspeech's primary STT logic.
                            # Note that this is outside the kill_switch block just to insure that all the
                            # buffers are cleaned and closed properly.  (Arguably this is not needed if killed)
                            text = str(stream_context.finishStream())
        
                            # We've completed the hard part.  Now let's just clean up.
                            if self._isRunning:
                                
                                # We'll only process if the text if there is a real value AND we're not already processing something.
                                # We don't block the processing of incoming audio though, we just ignore it if we're processing data.
                                if text.strip() != "":
        
                                    self.logger.info("HEARD " + text)
                                    self._doCallback(text)
                                    
                                stream_context = _model.createStream()  # Create a fresh new context
        
                            ring_buffer.clear()  # Clear the ring buffer as we've crossed the threshold again
        
            self.logger.debug("Stopping streams")        
            self.stream.stop_stream()                          # Stop audio device stream
            self.stream.close()                                # Close audio device stream
            self.logger.debug("Streams stopped")

        def accepts(self):
            return ["start", "stop", "audioOutStart", "audioOutEnd"]
            
        def isRunning(self):
            return self._isRunning
        
        def audioOutStart(self, httpRequest=None):
            self._isAudioOut = True
            return True
        
        def audioOutEnd(self, httpRequest=None):
            self._isAudioOut = False
            return True
        
        def stop(self, httpRequest=None):
            """
            Stops the listener and any active audio streams
            
            Returns:
                (bool):  True on success else will raise an exception.
            """

            if not self._isRunning:
                return True 

            self._isRunning = False
            if self.thread is not None:
                self.thread.join()
                
            self.logger.info("Stopped")
            return True
            
        def start(self, httpRequest=None, useThreads=True):
            """
            Starts the listener to listen to the default audio device

            Args:
                useThreads (bool):  Indicates if the brain should be started on a new thread.
            
            Returns:
                (bool):  True on success else will raise an exception.
            """

            if self._isRunning:
                return True 
            
            self.thread = self._readFromMic()
            if not useThreads:
                self.wait()
                
            return True
        
        def wait(self, seconds=0):
            """
            Waits for any active listeners to complete before closing
            
            Args:
                seconds (int):  Number of seconds to wait before calling the "stop()" function
                
            Returns:
                (bool):  True on success else will raise an exception.
            """
            
            if not self._isRunning:
                return True 
            
            if seconds > 0:
                if self.thread is not None:
                    time.sleep(seconds)
                    self.stop()
            
            else:
                if self.thread is not None:
                    self.thread.join()
                
            return True

except Exception:
    logging.debug(str(sys.exc_info()[0]))
    logging.debug(str(traceback.format_exc()))
    logging.error("Listener disabled due to missing libraries.")


try:
    import cv2 
    from PIL import Image

    class Watcher():
        """
        Watcher device to capture and process inbound video stream for objects and faces.
        """
        
        def __init__(
                self, 
                parent=None,
                classifierFile=None,
                recognizerFile=None,
                namesFile=None,
                trainingSourceFolder=None,
                videoDeviceIndex=0,
                framesPerSecond=29.97,
                orientation=0,
                callback=None):  # Callback is a function that accepts ONE positional argument which will contain the text identified
            """
            Watcher Initialization

            Args:
                classifierFile (str):  Classifier file such as haarcascades to identify generic objects.
                recognizerFile (str): Trained file to be used to identify specific objects. (optional)
                namesFile (str):  File with friendly names tied to recognizer trained data set. (optional)
                trainingSourceFolder (str):  The source directory that contains all the images to use for building a new recognizerFile.
                videoDeviceIndex (int): Video Device identifier. (optional)
                framesPerSecond (float): Number of frames per second.  Defaults to NTSC.
                orientation (int): Device orientation which can be 0, 90, 180, or 270.  (optional)
                videoDeviceIndex (int): Video device index number.  If not set then will use default video capture device.
                callback (function): Callback function for which to send any captured data.
                parent (object): Containing object's reference.  Normally this would be the device container. (optional)
            """

            from . import __version__
            self.version = __version__

            self._packageName = "karen"
            
            # Local variable instantiation and initialization
            self.type = "WATCHER"
            self.callback = callback
            self.logger = logging.getLogger(self.type)
            self.parent = parent
            
            fPath = os.path.join(os.path.dirname(__file__), "data", "models", "watcher")
            self.classifierFile = classifierFile if classifierFile is not None else os.path.abspath(os.path.join(fPath, "haarcascade_frontalface_default.xml"))
            
            hPath = os.path.join(os.path.expanduser("~/.karen"), "data", "models", "watcher")
            self.recognizerFile = recognizerFile if recognizerFile is not None else os.path.abspath(os.path.join(hPath, "recognizer.yml"))
            self.namesFile = namesFile if namesFile is not None else os.path.abspath(os.path.join(hPath, "names.json"))

            if recognizerFile is None or namesFile is None:
                os.makedirs(os.path.dirname(self.namesFile), exist_ok=True)
            
            self.trainingSourceFolder = trainingSourceFolder
            self.videoDeviceIndex = videoDeviceIndex if videoDeviceIndex is not None else 0
            self.framesPerSecond = float(framesPerSecond) if framesPerSecond is not None else 29.97
            
            self.orientation = None
            if orientation == 90:
                self.orientation = cv2.ROTATE_90_CLOCKWISE
            elif orientation == 180:
                self.orientation = cv2.ROTATE_180
            elif orientation == 270 or orientation == -90:
                self.orientation = cv2.ROTATE_90_COUNTERCLOCKWISE
            
            self.clients = []
            self._isRunning = False
            self.lastFrame = None
            
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
                    self.logger.debug(str(inData))
                    self.callback("IMAGE_INPUT", inData)
            except Exception:
                pass
            
            return
        
        @threaded
        def _readFromCamera(self):
            """
            Opens video device for capture and processing for inputs
            
            Returns:
                (thread):  The thread created for the watcher while capturing incoming video.
            """
            self._isRunning = True
            
            if self.classifierFile is None or not os.path.isfile(self.classifierFile):
                self.logger.error("Invalid classifier file specified. Unable to start Watcher.")
                self.classifierFile = None 
                self._isRunning = False
                return False
            
            enableDetection = True
            
            try:
                classifier = cv2.CascadeClassifier(self.classifierFile)
                recognizer = cv2.face.LBPHFaceRecognizer_create()
            except Exception:
                self.logger.warning("OpenCV does not have support for detection/recognition.  Reverting to simple image capture device.")
                enableDetection = False
                pass

            if enableDetection:        
                if self.recognizerFile is None or not os.path.isfile(self.recognizerFile):
                    if self.classifierFile is not None and self.trainingSourceFolder is not None and os.path.isdir(self.trainingSourceFolder):
                        self.logger.info("Recognizer file not found.  Will attempt to generate.")
                        if not self.train():
                            self.logger.critical("Unable to start watcher due to failed recognizer build.")
                            self._isRunning = False
                            return False 
                    else:
                        self.logger.warning("Invalid recognizer file and no training source was provided. Named objects will not be detected.")
                        recognizer = None
                else:
                    recognizer.read(self.recognizerFile)
                
            names = { }
            if self.namesFile is not None and os.path.isfile(self.namesFile):
                with open(self.namesFile, 'r') as fp:
                    obj = json.load(fp)
                
                if isinstance(obj, list):
                    for item in obj:
                        if "id" in item and "name" in item:
                            names[item["id"]] = item["name"]
                
            isPaused = False 
            
            videoDevice = cv2.VideoCapture(self.videoDeviceIndex)
            threadPool = []
            
            lTime = 0  # should be current time but we need to seed the first image.
            yTime = 0
            
            while self._isRunning:
                ret, im = videoDevice.read()
                if ret:
                    
                    t = time.time()
                    if t < (yTime + 0.05):  # No more than 20 frames per second
                        continue 
                    
                    yTime = t 
                    
                    # See if we need to rotate it and do so if required
                    if self.orientation is not None:
                        im = cv2.rotate(im, self.orientation)

                    width = int(im.shape[1])
                    height = int(im.shape[0])
                    
                    if width > 640:
                        width = 640
                        height = int(im.shape[0]) / int(im.shape[1]) * width
                        
                    if height > 480:
                        height = 480
                        width = int(im.shape[1]) / int(im.shape[0]) * height
                    
                    dim = (width, height)
                    im = cv2.resize(im, dim, interpolation=cv2.INTER_AREA)

                    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]  # This can be increated to 100, but at the cost of bandwidth.
                    data = cv2.imencode('.jpg', im, encode_param)[1]
                    try:
                        for client in self.clients:
                            if client.connected:
                                if client.streamQueue.empty():  # discard any images while the queue is not empty
                                    client.bufferStreamData(data)
                                else:
                                    # Dropping frame
                                    pass
                            else:
                                client.logger.debug("Streaming client disconnected.")
                                self.clients.remove(client)
                    except Exception:
                        raise
                    
                    if t < (lTime + 1):
                        continue
                    
                    lTime = t
                    self.lastFrame = data
                    
                    if not enableDetection:
                        continue 
                    
                    # Convert image to grayscale.  
                    # Some folks believe this improves identification, but your mileage may vary.
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    
                    # Detect faces (not the who... just if I see a face).
                    # Returns an array for each face it sees in the frame.
                    faces = classifier.detectMultiScale(gray, 1.2, 5)
                    
                    # Since we care about all the faces we'll store them after they are processed in an array
                    people = []
                    
                    # Iterate through the faces for identification.
                    for (x, y, w, h) in faces:
        
                        # Pull the ID and Distance from the recognizer based on the face in the image
                        # Remember that "gray" is our image now so this is literally cutting out the face
                        # at the coordinates provided and attempting to predict the person it is seeing.
                        
                        if recognizer is None:
                            Id = [0, 0]
                        else:
                            Id = recognizer.predict(gray[y:y + h, x:x + w])

                        # Let's build a JSON array of the person based on what we've learned so far.
                        person = {
                            "id": Id[0],
                            "name": names[Id[0]] if Id[0] in names else "",
                            "distance": Id[1],
                            "coordinates": {
                                "x": int(x),
                                "y": int(y)
                            },
                            "dimensions": {
                                "width": int(w),
                                "height": int(h)
                            }
                        }
        
                        # And now we save our person to our array of people.
                        people.append(person)
                        isPaused = False  # Used to send the latest frame, even if no people are present
                    
                    # Send the list of people in the frame to the brain.
                    # We do this on a separate thread to avoid blocking the image capture process.
                    # Technically we could have offloaded the entire recognizer process to a separate 
                    # thread so may need to consider doing that in the future.
                    if (len(people) > 0) or not isPaused:
                        # We only send data to the brain when we have something to send.
                        t = self._doCallback(people) 
                        
                        i = len(threadPool) - 1
                        while i >= 0:
                            try:
                                if not threadPool[i].isAlive():
                                    threadPool[i].join()
                                    threadPool.pop(i)
                            except Exception:
                                pass
                                
                            i = i - 1
                        
                        threadPool.append(t)
                        isPaused = True  # Set to pause unless I have people.
                        
                    if (len(people) > 0):
                        isPaused = False  # Need to sort out the logic b/c we shouldn't have to count the array again.

            videoDevice.release()
            for item in threadPool:
                if not item.isAlive():
                    item.join()
                
        def stream(self, httpRequest):
            """
            Adds a streaming client to the watcher device for MJPEG streaming output
            
            Args:
                httpRequest (KHTTPHandler): Handler for inbound request (from which to pull the socket).
                
            Returns:
                (bool): True on success or False on failure
                
            """
            
            client = TCPStreamingClient(httpRequest.socket)
            client.start()
            self.clients.append(client)
            httpRequest.isResponseSent = True

            return True
        
        def snapshot(self, httpRequest):
            """
            Displays the snapshot from the last frame
            
            Args:
                httpRequest (KHTTPHandler): Handler for inbound request (from which to pull the socket).
                
            Returns:
                (bool): True on success or False on failure
                
            """
            
            if self.lastFrame is None:
                return httpRequest.sendError()
            
            return httpRequest.sendHTTP(contentBody=self.lastFrame, contentType="image/jpeg")
        
        def accepts(self):
            return ["start", "stop", "stream", "snapshot"]
            
        def isRunning(self):
            return self._isRunning
        
        def train(self, httpRequest=None, trainingSourceFolder=None):
            """
            Retrains the face recognition based on images in the supplied folder
            
            Args:
                trainingSourceFolder (str): The source directory that contains all the images to use for building a new 
                                            recognizerFile.  Will use the configuration value if the input value is left 
                                            empty. (optional)
                
            Returns:
                (bool): True on success or False on failure
                
            """
            if trainingSourceFolder is not None:
                self.trainingSourceFolder = trainingSourceFolder
            
            if self.trainingSourceFolder is None or not os.path.isdir(self.trainingSourceFolder):
                self.logger.error("Invalid training source folder specified.  Unable to retrain recognizer file.")
                return False
            
            self.logger.debug("Using " + str(self.trainingSourceFolder) + " for building recognizer file.")
            
            recognizer = cv2.face.LBPHFaceRecognizer_create()
            classifier = cv2.CascadeClassifier(self.classifierFile)
            
            samples = []
            ids = []
            names = []

            namePaths = sorted([f.path for f in os.scandir(self.trainingSourceFolder) if f.is_dir()])
            for i, entry in enumerate(namePaths):
                names.append({ "id": (i + 1), "name": os.path.basename(entry) })
                self.logger.info("Processing " + os.path.basename(entry) + " directory")
                imagePaths = sorted([f.path for f in os.scandir(entry) if f.is_file()])

                # Loop through input images in the folder supplied.
                for imagePath in imagePaths:
                    
                    try:
                        # Open the image as a resource
                        PIL_img = Image.open(imagePath).convert('L')
                    
                        # Convert to Numpy Array
                        img_numpy = np.array(PIL_img, 'uint8')
                    
                        # At this point we should be okay to proceed with the image supplied.
                        self.logger.debug("Processing " + imagePath)
                    
                        # Let's pull out the faces from the image (may be more than one!)
                        faces = classifier.detectMultiScale(img_numpy)
                
                        # Loop through faces object for detection ... and there should only be 1. 
                        for (x, y, w, h) in faces:
                        
                            # Let's save the results of what we've found so far.
                        
                            # Yes, we are cutting out the face from the image and storing in an array.
                            samples.append(img_numpy[y:y + h, x:x + w]) 
                        
                            # Ids go in the ID array.
                            ids.append(i + 1)
                    except Exception:
                        self.logger.error("Failed to process: " + imagePath)
                        raise

            # Okay, we should be done collecting faces.
            self.logger.info("Identified " + str(len(samples)) + " sample images")
            
            # This is where the real work happens... let's create the training data based on the faces collected.
            recognizer.train(samples, np.array(ids))

            # And now for the final results and saving them to a file.
            self.logger.debug("Writing data to " + self.recognizerFile)
            recognizer.save(self.recognizerFile)
            
            self.logger.debug("Writing data to " + self.namesFile)
            with open(self.namesFile, 'w') as fp:
                json.dump(names, fp)
            
            self.logger.info("Training algorithm completed.")
            
            return True
        
        def stop(self, httpRequest=None):
            """
            Stops the watcher.  
            
            Returns:
                (bool):  True on success else will raise an exception.
            """
            
            for item in self.clients:
                item.kill = True

            if not self._isRunning:
                return True 

            self._isRunning = False
            if self.thread is not None:
                self.logger.debug("Waiting for threads to close.")
                self.thread.join()
                
            self.logger.debug("Stopped.")
            return True
            
        def start(self, httpRequest=None, useThreads=True):
            """
            Starts the watcher.

            Args:
                useThreads (bool):  Indicates if the brain should be started on a new thread.
            
            Returns:
                (bool):  True on success else will raise an exception.
            """
            if self._isRunning:
                return True 
            
            self.thread = self._readFromCamera()
            if not useThreads:
                self.wait()
                
            return True
        
        def wait(self, seconds=0):
            """
            Waits for any active watchers to complete before closing.
            
            Args:
                seconds (int):  Number of seconds to wait before calling the "stop()" function
                
            Returns:
                (bool):  True on success else will raise an exception.
            """
            if not self._isRunning:
                return True 
            
            if seconds > 0:
                if self.thread is not None:
                    time.sleep(seconds)
                    self.stop()
            
            else:
                if self.thread is not None:
                    self.thread.join()
                
            return True

except Exception:
    logging.debug(str(sys.exc_info()[0]))
    logging.debug(str(traceback.format_exc()))
    logging.error("Watcher disabled due to missing libraries.")