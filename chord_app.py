import pyaudio
import wave
from pathlib import Path
from threading import Thread

# user_notes = ""
NOTES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
CHORDS = {"C": ["C", "E", "G", "Bb"]}
CHUNK = 1024
NOTE_PATH = Path(r"C:\Users\User\Desktop\workspaces\local\python_projects\music_chord_app")

def check_note(msg: str) -> str:
    """Validate user input for note."""

    while True:
        note = input(msg).capitalize()
        if note in NOTES:
            print("Valid entry - playing the note " + note + "...")
            return note
        print("Invalid - try again")

def check_chord(msg: str) -> str:
    """Validate user input for chord."""

    while True:
        chord = input(msg).capitalize()
        if chord in NOTES:
            print("Valid entry - playing the NOTES for the " + chord + "7 chord...")
            return chord
        print("Invalid - try again")

def play_music(file: str) -> None:
    
    """Plays .wav note file."""
    print(file)
    # open the file for reading.
    wf = wave.open(str(file), 'rb')

    # create an audio object
    p = pyaudio.PyAudio()

    # open stream based on the wave object which has been input.
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    # read data (based on the CHUNK size)
    data = wf.readframes(CHUNK)

    # play stream (looping from beginning of file to the end)
    print(f"playing...{file} ")
    while data:
        # writing to the stream is what *actually* plays the sound.
        stream.write(data)
        data = wf.readframes(CHUNK)
    print(f"finished playing!...{file} ")

    # cleanup stuff.
    wf.close()
    stream.close()
    p.terminate()


if __name__ == "__main__":

    while True:

        # Play note.
        user_note = check_note("Enter a note you want to play: ")
        note_file = f"{NOTE_PATH}\{user_note}.wav"
        play_music(note_file)
        # note_file = './' + user_note + ".wav"

        # Play chord in line.
        threads = []
        user_chord = check_chord("Please type in the note you want to learn the 7th chord for...")
        for note in CHORDS[user_chord]:

            # Play note.
            note_file = f"{NOTE_PATH}\{note}.wav"
            play_music(note_file)

            # Create thread. (creation)
            threads.append(Thread(target=play_music, args=(note_file,)))

        # Play chord at same time. (execution)
        for thread in threads:
            thread.start()

        # Wait for threads to finish.
        for thread in threads:
            thread.join()
