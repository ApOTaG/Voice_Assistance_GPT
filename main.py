import sounddevice as sd
import soundfile as sound_file
from num2words import num2words
import re
from translate import Translator
from transliterate import translit
import config
import tts
import stt
from fuzzywuzzy import fuzz
import openai

print(f"{config.VA_NAME} (v{config.VA_VER}) запустился...")

def gpt_question(voice):
    translator = Translator(from_lang="RU", to_lang="EN")
    voice = translator.translate(voice)
    ask = voice

    openai.api_key = "#gpt-api-key"#<---gpt-api-key

    model_engine = "text-davinci-003"
    prompt = ask

    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    response = completion.choices[0].text

    print(response)
    translator2 = Translator(from_lang="EN", to_lang="RU")
    response = translator2.translate(response)
    response = translit(response, 'ru')
    response = replace_numbers_with_text(response)
    print(response)
    tts.va_speak(response)

def replace_numbers_with_text(text):
    # Создаем регулярное выражение для поиска чисел
    pattern = re.compile(r'\d+')

    # Используем функцию подстановки для замены чисел на текст
    def replace(match):
        number = int(match.group(0))
        return num2words(number, lang='ru')

    # Применяем замену с помощью регулярных выражений
    result = re.sub(pattern, replace, text)
    return result

def va_respond(voice: str):
    print(voice)
    if voice.startswith(config.VA_ALIAS):
        # обращаются к ассистенту
        cmd = recognize_cmd(voice)
        print(cmd)

        if cmd['percent'] < 40 or cmd['cmd'] not in config.VA_CMD_LIST.keys():
            if voice.split()[:3]:
                hmm = 'audio_words/hmm.wav'
                data_set, fsample = sound_file.read(hmm)
                sd.play(data_set, fsample)
                gpt_question(voice)

                return False
        else:
            execute_cmd(cmd['cmd'])
            return True



def filter_cmd(raw_voice: str):
    cmd = raw_voice

    for x in config.VA_ALIAS:
        cmd = cmd.replace(x, "").strip()

    for x in config.VA_TBR:
        cmd = cmd.replace(x, "").strip()

    return cmd


def recognize_cmd(cmd: str):
    rc = {'cmd': '', 'percent': 0}
    for c, v in config.VA_CMD_LIST.items():

        for x in v:
            vrt = fuzz.ratio(cmd, x)
            if vrt > rc['percent']:
                rc['cmd'] = c
                rc['percent'] = vrt

    return rc





def execute_cmd(cmd: str):
    if cmd == 'help':
        text = "Я умею: ..."
        text += "произносить время ..."
        text += "и погоду ..."
        text += "включать ютуб, музыку, дискорд, стим, майнкрафт ..."
        text += "включать и выключать звук ..."
        text += "и открывать браузер"
        tts.va_speak(text)
        pass
    elif cmd == 'hello':
        hello = 'audio_words/hello.wav'
        data_set, fsample = sound_file.read(hello)
        sd.play(data_set, fsample)

    elif cmd == 'thanks':
        thx = 'audio_words/thanks.wav'
        data_set, fsample = sound_file.read(thx)
        sd.play(data_set, fsample)

    elif cmd == 'name':
        hel = 'audio_words/name.wav'
        data_set, fsample = sound_file.read(hel)
        sd.play(data_set, fsample)


stt.va_listen(va_respond)
