import speech_recognition as sr
import pyttsx3 as stt
import time
import re
from User_Identity import identity


'''
Primary objective: 
    print out what I have said

Utilizing libraries: 
    speech_recognition
    pyttsx3
    pyaudio
    time
    re
'''

#-----------------------------------------------------------------------------------------------------------------#

# create an instance of the identity class
user = identity()

"""
Function that is called to provide text-to-speech (tts)
:parameter: message that will be read aloud
:return: None
"""
def tts(message):
    print("\n" + message)
    py = stt.init()
    py.say(message)
    py.runAndWait()


"""
Function that is called to confirm what the user has said
:parameter: None
:return: boolean based on confirmation status
"""
def confirm():

    while 1:
        confirmation = sr.Recognizer()
        mic = sr.Microphone(device_index=1)
        with mic as source1:
            confirmation.adjust_for_ambient_noise(source1, duration=.75)

            # print("\nIs that correct?")
            tts("Is that correct?")
            audio2 = confirmation.listen(source1, phrase_time_limit=2)

        confirmed = confirmation.recognize_google(audio2)
        confirmed = confirmed.lower()

        if "yes" in confirmed:
            # print("\nI heard " + confirmed)
            tts("I heard " + confirmed)
            return True

        elif "no" in confirmed:
            # print("\nI heard " + confirmed)
            tts("I heard " + confirmed)
            return False

        else:
            # print("\n Please respond with YES or NO")
            tts("Please respond with yes or no")


"""
Function for testing 
:parameter: None
:return: None
"""
def test1():
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    while 1:
        try:
            with mic as source:
                # print("One moment, I am filtering ambient audio")
                tts("One moment, I'm filtering ambient audio")
                r.adjust_for_ambient_noise(source, duration=.5)

                # print("\nOkay, now I am listening!")
                tts("Okay, now I'm listening!")
                audio1 = r.listen(source, phrase_time_limit=4)

            message = r.recognize_google(audio1)
            message = message.lower()

            # print("\nI believe you said: " + message)
            tts("I believe you said " + message)

            confirmed = confirm()

            if confirmed:

                if "my name is" in message:
                    name = re.search('(?<=my name is )(\w+)', message).group(1)
                    if name.isalpha():
                        user.name = name

                    # print("\nWell it's nice to meet you, " + name.capitalize())
                    tts("Well it's nice to meet you " + name)
                    time.sleep(1)

                with mic as source:
                    r.adjust_for_ambient_noise(source, duration=.75)

                    # print("\nDo you have another question?")
                    tts("Do you have another question?")
                    audio2 = r.listen(source, phrase_time_limit=3)

                message = r.recognize_google(audio2)
                message = message.lower()

                if "no" in message:
                    if user.name:
                        tts("Okay. Well have a good day then, " + user.name)
                    else:
                        tts("Okay. Well have a good day then.")
                    break

            else:
                # print("My mistake. Let's try that one more time")
                tts("My mistake. Let's try that onc more time")
                pass

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")


def main():
    test1()
    print("I am no longer listening")


if __name__ == "__main__":
    main()