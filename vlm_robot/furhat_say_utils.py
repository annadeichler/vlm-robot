import re
import requests
from datetime import datetime
import urllib.parse

def download_wav_to_sound_object(url,fn):
    # Fetch the WAV file from the URL
    response = requests.get(url)
    response.raise_for_status()  # This will raise an error if the download faile
    open(fn,'wb').write(response.content)

def generate_timestamp():
    # Get the current date and time
    now = datetime.now()

    # Format the date and time as a string suitable for a filename
    #timestamp = now.strftime("%Y%m%d_%H%M%S")
    timestamp = now.strftime("%Y%m%d_%H%M%S_") + str(int(now.microsecond / 1000)).zfill(2)
    # Return the formatted timestamp with the desired file extension
    return timestamp

def say_repeat (say_text_in, repetitions):
    global tts_url
    print("say_repeat: " + say_text_in)
    say_text_in = say_text_in.replace("... ", ", ")
    say_text_in = say_text_in.replace("-", ", ")
    say_text_in = say_text_in.replace("...", ".")
    say_text_in = say_text_in.replace("..", ".")
    parts = re.split(r'(?<=[.!?]) ', say_text_in)
    for i, part in enumerate(parts):
        say_text = part
        print(say_text)
        say_text = say_text.replace(",", "")
        say_text = say_text.replace("?", ".")
        say_text = say_text.replace("!", "")
        say_text = say_text.replace("...", ".")
        say_text = say_text.replace("..", ".")
        if not say_text.endswith("?") and not say_text.endswith("."):
            say_text += "."
        #gpt_result = gpt_result.replace("uh ", "uh, ")
        #gpt_result = gpt_result.replace("um ", "um, ")
        #gpt_result = gpt_result.replace("like ", "like, ")
        say_text = say_text.replace("Is it a mammal.", "So, Is it a mammal.")
        say_text = say_text.replace("Is it a reptile.", "Ok, Is it a mammal.")
        say_text = say_text.replace("live ", "reside ")
        say_text = say_text.replace("pew ", " ")
        say_text = say_text.replace("huh ", " ")
        say_text = say_text.replace("oh ", " ")
        say_text = say_text.replace("hmm ", "")
        say_text = say_text.replace("Hmm ", "")
        say_text = say_text.replace("knw ", "know ")
        say_text = say_text.replace("phew ", "okey ")
        print('say_repeat_text:',say_text)
        print('rep:',repetitions)
        certainty = 0
        if repetitions == 1:
            read_level = 0.6
            spontaneous_level = 0.2
            pitch = -0.5
            speaking_rate = -0.5      
        elif repetitions == 2:
            read_level = 1
            spontaneous_level = 0.2
            pitch = 0.5
            speaking_rate = -1.2
        else:
            read_level = 1.2
            spontaneous_level = 0.2
            pitch = 0.75
            speaking_rate = -3   
        print('read_level:',read_level)
        print('spontaneous_level:',spontaneous_level)
        print('certainty:',certainty)
        print("Pitch:", pitch)
        print("Speaking Rate:", speaking_rate)
        gpt_text = urllib.parse.quote_plus(say_text)
        #print('gpt_text' + gpt_text)
        # furhat.say(text=gpt_result,blocking=True)
        #furhat.say(url='http://130.237.67.69:5134/speak/?text=' + gpt_text, blocking=True, lipsync=True)

        say_string = "{}{}&spk_vec={},{}&f0={}&sr={}".format(tts_url,gpt_text,read_level,spontaneous_level, pitch,speaking_rate)
        ctrl_string =  "&spk_vec={},{}&f0={}&sr={}".format(read_level,spontaneous_level, pitch,speaking_rate)
        timestamp = generate_timestamp()

        filename = folder_name + "/" + timestamp + ".wav"
        filename_text = folder_name + "/" + timestamp + ".text"
        filename_ctrl = folder_name + "/" + timestamp + ".ctrl"

        download_wav_to_sound_object(say_string, filename)
        furhat.say(url="http://localhost:8000/" +  filename, blocking=True, lipsync=True)
        print('say_string: ',say_string)
        # Don't forget to close the sound object when done
        log_data = {
            "timestamp": timestamp,
            "filename": filename,
            "certainty": certainty,
            "pitch": pitch,
            "speaking_rate": speaking_rate,
            "say_string": say_string,
            "system": say_text
        }
        log_feedback(log_data)
        with open(filename_text, 'w') as file:
            file.write(say_text)
        with open(filename_ctrl, 'w') as file:
            file.write(ctrl_string)


def say_url (
        furhat,
        say_text_in, 
        tts_url, 
        tts_system, 
        system_persona, 
        certainty=0,
        tmp_tts_folder="tmp_tts/"):
    print("into say_url")
    if say_text_in:
        say_text_in = say_text_in.replace("... ", ", ")
        say_text_in = say_text_in.replace("-", ", ")
        say_text_in = say_text_in.replace("...", ".")
        say_text_in = say_text_in.replace("..", ".")
        say_text_in = say_text_in.replace(";", ".")
        parts = re.split(r'(?<=[.!?]) ', say_text_in)
        for i, part in enumerate(parts):
            say_text = part
            print(say_text)
            say_text = say_text.replace(",", "")
            say_text = say_text.replace("?", ".")
            say_text = say_text.replace("!", "")
            say_text = say_text.replace("...", ".")
            say_text = say_text.replace("..", ".")
            say_text = say_text.replace("Oops ", "")
            say_text = say_text.replace("Uh oh, ", "")
            say_text = say_text.replace("Uh no, ", "")
            say_text = say_text.replace("whoa, ", "wow ")
            say_text = say_text.replace("Uh, oh no, ", "")
            say_text = say_text.replace("Uh, ", "Interesting ")
            say_text = say_text.replace("Uh-oh, ", "")
            say_text = say_text.replace("Ah, no?", "Uh so it's not.")
            say_text = say_text.replace("Oh, no?", "Uh so it's not.")
            say_text = say_text.replace("Ah, umm, ", "Um")
            say_text = say_text.replace("Ah, well, uh, ", "")
            say_text = say_text.replace("Aah, ", "")
            say_text = say_text.replace("Ah, I ", "Well I ")
            say_text = say_text.replace("Ah, ", "Uh ")
            say_text = say_text.replace(", am I", "")
            say_text = say_text.replace(", isn't it", "")
            say_text = say_text.replace(",", "")
            say_text = say_text.replace("?", ".")
            say_text = say_text.replace("!", "")
            say_text = say_text.replace("  ", " ")
            if not say_text.endswith("?") and not say_text.endswith("."):
                say_text += "."
            #gpt_result = gpt_result.replace("uh ", "uh, ")
            #gpt_result = gpt_result.replace("um ", "um, ")
            #gpt_result = gpt_result.replace("like ", "like, ")
            say_text = say_text.replace("Is it a mammal.", "Ok, is it a mammal.")
            say_text = say_text.replace("Is it a reptile.", "Ok, is it a mammal.")
            say_text = say_text.replace("Is it a bird.", "Ok, is it a bird.")
            say_text = say_text.replace("live ", "reside ")
            say_text = say_text.replace("pew ", " ")
            say_text = say_text.replace("huh ", " ")
            say_text = say_text.replace("oh ", " ")
            say_text = say_text.replace("hmm ", "")
            say_text = say_text.replace("Hmm ", "")
            say_text = say_text.replace("knw ", "know ")
            say_text = say_text.replace("phew ", "okey ")
            #say_text = say_text.replace("like ", "like, ")
            say_text = say_text.replace("Oops ", "")
            say_text = say_text.replace("live ", "reside ")
            say_text = say_text.replace("lives ", "resides ")
            say_text = say_text.replace("pew ", " ")
            say_text = say_text.replace("really ", " ")
            say_text = say_text.replace("huh ", " ")
            say_text = say_text.replace(" or should", ", or should")
            say_text = say_text.replace("oh ", " ")
            say_text = say_text.replace("hmm ", "uh ")
            say_text = say_text.replace("Hmm ", "uh ")
            say_text = say_text.replace("knw ", "know ")
            say_text = say_text.replace("phew ", "okey ")
            say_text = say_text.replace("yay", "yeah ")
            say_text = say_text.replace("shucks", "that sucks")
            say_text = say_text.replace("get there.", "get there soon.")
            #say_text = say_text.replace(" there.", ".")
            say_text = say_text.replace("huh.", ".")       
            say_text = say_text.replace("uh.", ".")
            say_text = say_text.replace("wasn't it.", ".")
            say_text = say_text.replace("is it.", ".")
            say_text = say_text.replace("aren't I.", ".")
            say_text = say_text.replace("Oh wow yes.", "Oh wow that was great to hear.")
            say_text = say_text.replace("Hmmm.", "Um+let+me+think.")
            say_text = say_text.replace("  ", " ")
            say_text = say_text.replace(" .", ".")
            print('say_text2:',say_text)
            print('certainty:',certainty)
            pitch = 0
            speaking_rate = 0
            read_level = 0.6
            spontaneous_level = 1

            # Set pitch and speaking_rate based on the certainty_level
            if system_persona == "affective":
                if -20 <= certainty < -3:
                    read_level = 0.10
                    spontaneous_level = 1.2
                    pitch = -1.1
                    speaking_rate = -1.0
                elif -3 <= certainty < -2:
                    read_level = 0.25
                    spontaneous_level = 1.1
                    pitch = -0.9
                    speaking_rate = -0.8  
                elif -2 <= certainty < -1:
                    read_level = 0.20
                    spontaneous_level = 1
                    pitch = -0.6
                    speaking_rate = -0.4    
                elif -1 <= certainty < 0:
                    read_level = 0.25
                    spontaneous_level = 0.9
                    pitch = -0.3
                    speaking_rate = -0.2    
                elif 0 <= certainty < 1:
                    read_level = 0.25
                    spontaneous_level = 0.9
                    pitch = 0.4
                    speaking_rate = -0.2
                elif 1 <= certainty < 2:
                    read_level = 0.20
                    spontaneous_level = 1.0
                    pitch = 0.6
                    speaking_rate = 0.0
                elif 2 <= certainty < 3:
                    read_level = 0.15
                    spontaneous_level = 1.1
                    pitch = 0.9
                    speaking_rate = 0.2
                elif 3 <= certainty < 20:
                    read_level = 0.10
                    spontaneous_level = 1.2
                    pitch = 1.1
                    speaking_rate = 0.4
                else:
                    print("Invalid certainty level. It must be within the range of -20 to 20.")
                    pitch = 0
                    speaking_rate = 0
            elif system_persona == "non_affective":
                print("non_affective")
                read_level = 0.8
                spontaneous_level = 0.2
                pitch = 0.8
                speaking_rate = -0.2
            else:
                print("Invalid value for system_persona") 
                read_level = 0.8
                spontaneous_level = 0.2
                pitch = 0.8
                speaking_rate = -0.2
            if tts_system == "tacotron" or tts_system == "matcha":
                read_level = 0.7
                spontaneous_level = 0.3
            speaking_rate =1.0
            pitch = 1.0
            # Print the values
            print('read_level:',read_level)
            print('spontaneous_level:',spontaneous_level)
            print("Pitch:", pitch)
            print("Speaking Rate:", speaking_rate)
            gpt_text = urllib.parse.quote_plus(say_text)
            #print('gpt_text' + gpt_text)
            # furhat.say(text=gpt_result,blocking=True)
            #furhat.say(url='http://130.237.67.69:5134/speak/?text=' + gpt_text, blocking=True, lipsync=True)

            say_string = "{}{}&spk_vec={},{}&f0={}&sr={}".format(tts_url,gpt_text,read_level,spontaneous_level, pitch,speaking_rate)
            ctrl_string =  "&spk_vec={},{}&f0={}&sr={}".format(read_level,spontaneous_level, pitch,speaking_rate)
            timestamp = generate_timestamp()

            filename = tmp_tts_folder + "/" + timestamp + ".wav"
            filename_text = tmp_tts_folder + "/" + timestamp + ".text"
            filename_ctrl = tmp_tts_folder + "/" + timestamp + ".ctrl"

            download_wav_to_sound_object(say_string, filename)
            furhat.say(url="http://localhost:8000/" +  filename, blocking=True, lipsync=True)
            print('say_string: ',say_string)
            # Don't forget to close the sound object when done
            # log_data = {
            #     "timestamp": timestamp,
            #     "filename": filename,
            #     "certainty": certainty,
            #     "pitch": pitch,
            #     "speaking_rate": speaking_rate,
            #     "say_string": say_string,
            #     "system": say_text
            # }
            # log_feedback(log_data)
            with open(filename_text, 'w') as file:
                file.write(say_text)
            with open(filename_ctrl, 'w') as file:
                file.write(ctrl_string)
    print("leaving_say_url")

def say_url_feedback (say_text_in, certainty=0):
    global tts_url
    global tts_system
    print("into say_feedback")
    say_text_in = say_text_in.replace("... ", ", ")
    say_text_in = say_text_in.replace("Oh! ", "Oh, ")
    say_text_in = say_text_in.replace("-", ", ")
    say_text_in = say_text_in.replace("...", ".")
    say_text_in = say_text_in.replace("..", ".")
    parts = re.split(r'(?<=[.!?]) ', say_text_in)
    total_parts = len(parts)
    print("total_parts", total_parts)

    for i, part in enumerate(parts):
        total_parts = len(parts)
        say_text = part
        print(say_text)
        say_text = say_text.replace("Oh no, ", "Ok so then ")
        say_text = say_text.replace("Oh, yes!", "wow so far so good.")
        #say_text = say_text.replace("Oh dear, ", "")
        if -10 <= certainty < 0:
            say_text = say_text.replace("Oh, great! ", "")
            say_text = say_text.replace("Oh, ", "uh ")
        elif 0 <= certainty <= 10:
            say_text = say_text.replace("Oh, great! ", "wow, that's great to hear. ")
            say_text = say_text.replace("Oh, ", "wow, ")
        else:
            print("Invalid certainty level. It must be either 5 or -5.")
        say_text = say_text.replace("oops ", "")
        say_text = say_text.replace("uh oh, ", "")
        say_text = say_text.replace("uh no, ", "")
        say_text = say_text.replace("uh, oh no, ", "")
        say_text = say_text.replace("yes yes ", "yes ")
        say_text = say_text.replace("uh, ", "interesting ")
        say_text = say_text.replace("uh-oh, ", "")
        say_text = say_text.replace("ah, no?", "uh so it's not.")
        say_text = say_text.replace("oh, no?", "uh so it's not.")
        say_text = say_text.replace("ah, umm, ", "um")
        say_text = say_text.replace("ah, well, uh, ", "")
        say_text = say_text.replace("aah, ", "")
        say_text = say_text.replace("ah, I ", "Well I ")
        say_text = say_text.replace("ah, ", "Uh ")
        say_text = say_text.replace(", am I", "")
        say_text = say_text.replace(", isn't it", "")
        say_text = say_text.replace(",", "")
        say_text = say_text.replace("?", ".")
        say_text = say_text.replace("!", "")
        say_text = say_text.replace("  ", " ")
        if not say_text.endswith("?") and not say_text.endswith("."):
            say_text += "."
        say_text = say_text.replace(" .", ".")
        #say_text = say_text.replace("uh ", "uh, ")
        #say_text = say_text.replace("um ", "um, ")
        say_text = say_text.replace("like ", "like, ")
        say_text = say_text.replace("Oops ", "")
        say_text = say_text.replace("live ", "reside ")
        say_text = say_text.replace("lives ", "resides ")
        say_text = say_text.replace("pew ", " ")
        say_text = say_text.replace("really ", " ")
        say_text = say_text.replace("huh ", " ")
        say_text = say_text.replace("oh ", " ")
        say_text = say_text.replace("hmm ", "uh ")
        say_text = say_text.replace("Hmm ", "uh ")
        say_text = say_text.replace("knw ", "know ")
        say_text = say_text.replace("phew ", "okey ")
        say_text = say_text.replace("yay", "yeah ")
        say_text = say_text.replace("shucks", "that sucks")
        say_text = say_text.replace("get there.", "get there soon.")
        #say_text = say_text.replace(" there.", ".")
        say_text = say_text.replace("huh.", ".")       
        say_text = say_text.replace("uh.", ".")
        say_text = say_text.replace("wasn't it.", ".")
        say_text = say_text.replace("is it.", ".")
        say_text = say_text.replace("aren't I.", ".")
        say_text = say_text.replace("Oh wow yes.", "Oh wow that was great to hear.")
        say_text = say_text.replace("Hmmm.", "Um+let+me+think.")
        say_text = say_text.replace("No.", "so you answer is that it's not.")
        say_text = say_text.replace("Yes.", "ok, so you answer is yes to that question.")
        say_text = say_text.replace("I'm not as on track as I thought I was.", "uh so I'm not as on track as I thought.")
        say_text = say_text.replace("I'm not doing very great.", "Uh so I'm not doing great.")
        say_text = say_text.replace("that's not it.", "uh so that's not it.")
        say_text = say_text.replace("that sets me back a bit.", "uh so that sets me back a bit.")
        say_text = say_text.replace("I need to think harder.", "I need to think harder on this.")
        say_text = say_text.replace("  ", " ")
        say_text = say_text.replace(" .", ".")
        print('say_url_feedback:',say_text)
        gpt_text = urllib.parse.quote_plus(say_text)
        print('Feedback certainty:',certainty)
        pitch = 0
        speaking_rate = 0
        read_level = 0.2
        spontaneous_level = 0.95
        #import pdb;pdb.set_trace()
        # Set pitch and speaking_rate based on the certainty_level
        if -10 <= certainty < 0:
            read_level = 0.1
            spontaneous_level = 1.1
            pitch = 0.2
            speaking_rate = 2.8       
        elif 0 <= certainty <= 10:
            read_level = 0.25
            spontaneous_level = 0.9
            pitch = 0.9
            speaking_rate = 0.8
        else:
            print("Invalid certainty level. It must be either 5 or -5.")
            pitch = -0.2
            speaking_rate = 0.2
        if tts_system == "tacotron" or tts_system == "matcha":
            read_level = 0.2
            spontaneous_level = 0.8
        # Print the values
        print('read_level:',read_level)
        print('spontaneous_level:',spontaneous_level)
        print("Pitch:", pitch)
        print("Speaking Rate:", speaking_rate)
        #print('gpt_text' + gpt_text)
        # furhat.say(text=gpt_result,blocking=True)
        #furhat.say(url='http://130.237.67.69:5134/speak/?text=' + gpt_text, lipsync=True)
        #furhat.say(url='http://130.237.67.69:5134/speak/?text=' + gpt_text + "&spk_vec=0.2,0.8&f0=-0.9&sr=1.9", lipsync=True)
        say_string = "{}{}&spk_vec={},{}&f0={}&sr={}".format(tts_url,gpt_text,read_level,spontaneous_level, pitch,speaking_rate)
        ctrl_string =  "&spk_vec={},{}&f0={}&sr={}".format(read_level,spontaneous_level, pitch,speaking_rate)
        timestamp = generate_timestamp()
        #folder_name = "audio/"
        filename = folder_name + "/" + timestamp + ".wav"
        filename_text = folder_name + "/" + timestamp + ".text"
        filename_ctrl = folder_name + "/" + timestamp + ".ctrl"
        download_wav_to_sound_object(say_string, filename)
        if i == total_parts - 1:  # Check if it's the last part
            print("Last Part, no block")
            furhat.say(url="http://localhost:8000/" +  filename, lipsync=True)
        else:
            print("blocking")
            furhat.say(url="http://localhost:8000/" +  filename, blocking=True, lipsync=True)
        print('say_string: ',say_string)
        log_data = {
            "timestamp": timestamp,
            "filename": filename,
            "certainty": certainty,
            "pitch": pitch,
            "speaking_rate": speaking_rate,
            "say_string": say_string,
            "system": say_text
        }
        log_feedback(log_data)
        with open(filename_text, 'w') as file:
            file.write(say_text)
        with open(filename_ctrl, 'w') as file:
            file.write(ctrl_string)

    print("leaving say feedback")
