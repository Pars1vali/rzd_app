import json

import requests
import streamlit as st

url = "https://pars1vali-rzd-c40d.twc1.net/audio"



def send_audio(uploaded_file):
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        response_json = json.loads(response.text)
        container = st.container(border=True)

        if response_json["speech_valid"] is True:
            container.image("assets/happy.png", width=135)
            container.markdown("**Переговоры соответствуют регламенту**")
            container.markdown("**Текст**")
            container.json(response_json["text"], expanded=False)
        else:
            problems = []
            for problem in response_json["type_problem"]:
                if problem == "special_words":
                    problems.append("Использование запрещенных слов")
                elif problem == "template_error":
                    problems.append("Нарушение шаблона")
                else:
                    problems.append("Неизвестная причина")

            container.image("assets/sad.png", width=135)
            container.markdown("**Переговоры не соответствуют регламенту**.")
            container.markdown("Причины:")
            for problem in problems:
                container.markdown("- " + problem)

            container.markdown("**Текст**")
            container.json(response_json["text"], expanded=False)


title, image = st.columns(2)
title.title("Анализатор служебных переговоров")
image.image("assets/logo.png",width=200)
uploaded_file = st.file_uploader("Загрузите аудио", type=["wav", "mp3"])

if uploaded_file is not None:
    with st.spinner("Обработка"):
        send_audio(uploaded_file)
