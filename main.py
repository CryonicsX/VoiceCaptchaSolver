import requests, flask, re
import speech_recognition as sr
from flask import request, jsonify


list = {
    "zero": "0",
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eighth": "8",
    "eight": "8",
    "ate": "8",
    "nine": "9"
}

class voice_solver:

    def get_voice_url(url):

        response = requests.get(url)
        match = re.search(r"captchaAudioChallengePath: '(.*?)'", response.text)
        if match:
            captcha_audio_challenge_path = match.group(1)
            print("captchaAudioChallengePath:", captcha_audio_challenge_path)
            return captcha_audio_challenge_path
        else:
            print("captchaAudioChallengePath değeri bulunamadı.")



    def concatenate_numbers(number_list):
        concatenated_number = ''.join(number_list)
        return concatenated_number


    def convert_text_to_numbers(text_list, conversion_dict):
        result = []
        for word in text_list:
            if word in conversion_dict:
                result.append(conversion_dict[word])
            else:
                result.append(word)  # Eğer sözlükte eşleşen bir değer yoksa, aynı kelimeyi ekleyin
        return result

    def solve_captcha(url):
        response = requests.get(url)
        with open("audio.wav", "wb") as file:
            file.write(response.content)

        recognizer = sr.Recognizer()
        with sr.AudioFile("audio.wav") as source:
            audio_data = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio_data).split("hear")[1].split(" ")[1:]
                converted_list = voice_solver.convert_text_to_numbers(text, list)
                concatenated_number = voice_solver.concatenate_numbers(converted_list)
                return concatenated_number

                
            except sr.UnknownValueError:
                print("Voice Error")
                return "ERROR"
            except sr.RequestError as e:
                print("Google api error{0}".format(e))    
                return "ERROR"  


class api:
    def __init__(self, port: str) -> None:
        self.base_api = "/api"
        self.app = flask.Flask(__name__)
        app = self.app
        #run_with_ngrok(app)
        self.port = port

    

        @app.route(f"{self.base_api}/solve", methods=["POST"])
        def send_index():
            url = request.get_json(silent=True)["url"]
            res = voice_solver.solve_captcha(url)
            if res != "ERROR":
                return str(res), 200
            else:
                return res, 200
            
        @app.route(f"{self.base_api}/get_url", methods=["POST"])
        def send_url():
            url = request.get_json(silent=True)["url"]
            res = voice_solver.get_voice_url(url)
            if res != "ERROR":
                return str(res), 200
            else:
                return res, 200


    def start_server(self):
        self.app.run(debug=True, port=self.port)




if __name__ == "__main__":
    api(1337).start_server()

