#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import String
import speech_recognition as sr
import pyaudio
import wave

DEVICE_INDEX = 4  # Replace with your microphone index
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 4096
RECORD_SECONDS = 7
TEMP_AUDIO_FILE = "recorded_audio.wav"

def record_audio(device_index, output_file):
    """Record audio from the specified microphone and save it to a file."""
    p = pyaudio.PyAudio()
    try:
        if device_index >= p.get_device_count() or device_index < 0:
            rospy.logerr("Invalid device index: {}. Please check the device list.".format(device_index))
            p.terminate()
            return False

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=device_index,
                        frames_per_buffer=CHUNK)
        rospy.loginfo("Recording...")
        frames = []
        for _ in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)

        rospy.loginfo("Recording finished.")
        stream.stop_stream()
        stream.close()
        p.terminate()

        # 写入 WAV 文件
        wf = wave.open(output_file, 'wb')
        try:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))
        finally:
            wf.close()

        return True
    except Exception as e:
        rospy.logerr("Error during recording: {}".format(e))
        p.terminate()
        return False


def recognize_audio(file_path):
    """Recognize speech from an audio file."""
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            rospy.loginfo("Processing audio for recognition...")
            audio_data = recognizer.record(source)

        rospy.loginfo("Recognizing speech...")
        text = recognizer.recognize_google(audio_data, language="en-US")
        rospy.loginfo("Recognized Text: {}".format(text))

        return text
    except sr.UnknownValueError:
        rospy.logwarn("Google Web Speech API could not understand the audio.")
    except sr.RequestError as e:
        rospy.logerr("API Request Error: {}".format(e))

    return None

def voice_recognition_node():
    rospy.init_node('voice_recognition_node', anonymous=True)
    pub = rospy.Publisher('recognized_speech', String, queue_size=10)
    rate = rospy.Rate(0.2)  # Publish every 5 seconds

    while not rospy.is_shutdown():
        if record_audio(DEVICE_INDEX, TEMP_AUDIO_FILE):
            recognized_text = recognize_audio(TEMP_AUDIO_FILE)
            if recognized_text:
                msg = String(data=recognized_text)
                pub.publish(msg)
                rospy.loginfo("Published: {}".format(recognized_text))

        rate.sleep()

if __name__ == '__main__':
    try:
        voice_recognition_node()
    except rospy.ROSInterruptException:
        pass
