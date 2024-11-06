import openai
import pyttsx3
import speech_recognition as sr
import os

# Set your OpenAI API key
openai.api_key = "" # Or use a direct key here for testing (not recommended)

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# TTS engine setup (optional: adjust rate and voice if needed)
tts_engine.setProperty("rate", 150)  # Speed of speech
tts_engine.setProperty("volume", 0.9)  # Volume level (0.0 to 1.0)
voices = tts_engine.getProperty('voices')

def recognize_speech():
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            print("Recognizing speech...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
            return None

def get_ai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-2024-08-06",  # or "gpt-3.5-turbo" if you’re using GPT-3.5
            messages=[
                {"role": "system", "content": "You are a helpful assistant that responds concisely and clearly."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        return "I'm having trouble responding right now."

def speak_text(text):
    # Set the desired voice by index (e.g., use the voice index you found from the list above)
    tts_engine.setProperty('voice', voices[110].id)  # Change 1 to the index of your chosen voice
    
    # Set rate (lower values for slower, higher for faster speech)
    tts_engine.setProperty('rate', 125)  # Slower for a calmer tone, faster for an energetic tone
    
    # Set volume (0.0 to 1.0)
    tts_engine.setProperty('volume', 0.9)

    tts_engine.say(text)
    tts_engine.runAndWait()

def main():
    print("Starting real-time voice assistant. Say 'exit' to quit.")
    while True:
        # Step 1: Get spoken input
        spoken_text = recognize_speech()
        if not spoken_text:
            continue

        # Exit if the user says "exit"
        if spoken_text.lower() == "exit":
            print("Exiting conversation.")
            break

        # Step 2: Get AI response
        ai_response = get_ai_response(spoken_text)
        print(f"AI says: {ai_response}")

        # Step 3: Speak AI response
        speak_text(ai_response)

if __name__ == "__main__":
    main()
