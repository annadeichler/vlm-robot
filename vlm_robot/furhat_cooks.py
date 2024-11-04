from furhat_remote_api import FurhatRemoteAPI
import base64
import os
from furhat_say_utils import say_repeat, say_url, say_url_feedback, generate_timestamp
from gpt_combined import GPTCookingAssistant, GPTImageAnalyzer
import threading
from furhat_gesture import tilt_head
from camera import *

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

if __name__ == "__main__":
    # init tt
    tts_url = "http://130.237.67.34:5134/speak/?text="
    tts_system = "tacotron_prosody"
    system_persona = "affective"
    folder_name = f"session_dev"
    if not os.path.exists(folder_name):
            os.makedirs(folder_name)
    tmp_tts_folder = "tmp_tts"
    if not os.path.exists(tmp_tts_folder):
        os.makedirs(tmp_tts_folder)

    # Create an instance of the FurhatRemoteAPI class, providing the address of the robot or the SDK running the virtual robot
    furhat = FurhatRemoteAPI("localhost")

    # init gpt
    # Initialize shared list and API keys
    image_data = []
    api_key = "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"
    image_path = "media/sreenshot.png"

    # init camera
    camera_handler = CameraHandler(quality='720p')  # Example for 1080p quality
    # print("Starting video stream. Press 'q' to quit.")
    # camera_handler.stream_video()
    camera_handler.take_screenshot(
        file_format='png', screenshot_path=image_path
    )

    # Initialize both agents
    cooking_assistant = GPTCookingAssistant(api_key, image_data)
    image_analyzer = GPTImageAnalyzer(api_key, image_data)

    # Start the image analyzer in a separate thread
    image_thread = threading.Thread(target=image_analyzer.run_periodically, args=(image_path,))
    image_thread.daemon = True
    image_thread.start()

    # Listen to user speech and return ASR result
    hello_mess = "Hi let's do some cooking!"
    say_url(furhat, hello_mess, tts_url, tts_system, system_persona, 5, tmp_tts_folder=tmp_tts_folder)

    context = []
    timestamp = generate_timestamp()
    progress_level = 1

    print("context0:", context)
    first_time = 1
    number_of_questions = 0
    print ("going into while")
    conversation_history = ""
    try:
        while(True):
            # Extract the question, yes, and no parts
            #gpt_question, yes_part, no_part = parts
            # print(gpt_result)
            print ("------")

            # ## TODO: parse gpt results here
            # gpt_say = "Great, we are cooking now!."      
            # say_url(furhat, gpt_say, tts_url, tts_system, system_persona, tmp_tts_folder=tmp_tts_folder)
            print('1---listening...')
            first_time = 0
            asr_result = furhat.listen()
            while not asr_result.message:
                print("The string is empty.")
                error_mess = "you have to say something."
                say_url(furhat, error_mess, tts_url, tts_system, system_persona, tmp_tts_folder=tmp_tts_folder)

                print('2----listening...')
                asr_result = furhat.listen()
            print("=============asr_result.message", asr_result.message)

            repetitions = 0
            while "repeat" in asr_result.message: # TODO: more sophisticated way to check repetitions
                repetitions += 1
                print("The string includes 'repeat'.")  

                say_repeat(gpt_say,repetitions)
                print('3---listening...')
                asr_result = furhat.listen()

            is_it_phrases = ["is it", "asset", "it's it's"]
        
            asr_message = asr_result.message
            print("processed asr_message",asr_message)
            conversation_history += f"User: {asr_message}\n"
            
            tilt_head(furhat)

            # asr_res = asr_message + "(json)"
            # context,gpt_result = send_to_gpt(context,asr_res, headers=gpt_headers)

            gpt_say = cooking_assistant.give_response(conversation_history)
            conversation_history += f"GPT: {gpt_say}\n"
            # vars        ## TODO: parse gpt results here
            # gpt_say = "Great, we are cooking now!."      
            say_url(furhat, gpt_say, tts_url, tts_system, system_persona, tmp_tts_folder=tmp_tts_folder)
    except:
        camera_handler.release()