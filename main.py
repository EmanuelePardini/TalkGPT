import pyttsx3
import openai
import speech_recognition as sr

# Inizializza il riconoscimento vocale
r = sr.Recognizer()

# Configura l'API OpenAI
openai.api_key = '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'

# Inizializza il contesto della conversazione
prompt = "Sei un assistente che risponde alle domande in italiano."

engine = pyttsx3.init()

voices = engine.getProperty('voices')
for voice in voices:
    print("Voice:")
    print(" - ID: %s" % voice.id)
    print(" - Name: %s" % voice.name)
    print(" - Languages: %s" % voice.languages)
    print(" - Gender: %s" % voice.gender)
    print(" - Age: %s" % voice.age)

# Sostituisci 'voice.id' con l'ID della voce che desideri utilizzare
engine.setProperty('voice', voice.id)

engine.say("Ciao, come stai?")
engine.runAndWait()

while True:
    try:
        # Rileva l'input vocale
        with sr.Microphone() as source:
            audio = r.listen(source)
            text = r.recognize_google(audio, language='it-IT')
            if text != '':
                print('You said: ' + text)

        # Prepara il prompt
        prompt += "\nUser: " + text + "\nAssistant:"

        # Ottieni la risposta da GPT-3
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            temperature=0.6
        )

        # Controlla se la risposta è vuota
        if response.choices and response.choices[0].text.strip():
            message = response.choices[0].text.strip()
        else:
            message = "Mi dispiace, non ho capito. Potresti ripetere?"

        # Stampa e legge la risposta
        print('GPT-3: ' + message)
        engine.say(message)
        engine.runAndWait()

        # Aggiungi la risposta del bot alla conversazione
        prompt += " " + message

    except Exception as e:
        print()
