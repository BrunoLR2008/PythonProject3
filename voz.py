import speech_recognition as sr
import sounddevice as sd
import scipy.io.wavfile as wav
import io
import unicodedata

reconhecedor = sr.Recognizer()
taxa_amostragem = 44100
duracao = 5  # segundos de gravação
frase_correta='Eu amo Python'

def normalizar(texto):
    """Deixa o texto em minúsculas, sem acentos e sem pontuação,
    para a comparação não ser tão rígida."""
    texto = texto.lower().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto = "".join(c for c in texto if c.isalnum() or c.isspace())
    return texto

print("=== EXERCICIOS DE PRONÚNCIA ===")
while True:
    print(f'Repita a frase: {frase_correta}')
    print("Pode falar agora (gravando por 5 segundos)...")
    audio_gravado = sd.rec(int(duracao * taxa_amostragem), samplerate=taxa_amostragem, channels=1, dtype='int16')
    sd.wait()  # Aguarda terminar a gravação
    print("Transcrevendo...")

    # Converte a gravação na memória para o SpeechRecognition ler
    buffer_wav = io.BytesIO()
    wav.write(buffer_wav, taxa_amostragem, audio_gravado)
    buffer_wav.seek(0)

    with sr.AudioFile(buffer_wav) as fonte:
        audio = reconhecedor.record(fonte)

    try:
        texto = reconhecedor.recognize_google(audio, language="pt-BR")
        print("Você disse:", texto)
        if normalizar(texto) == normalizar(frase_correta):
            print("Correto,Você falou a frase correta!")
        else:
            print('ERRADO! TENTE NOVAMENTE!')
            print(f'A frase certa era:{frase_correta}')
    except sr.UnknownValueError:
        print("Não entendi o que você disse.")
    except sr.RequestError:
        print("Erro ao conectar com o serviço do Google.")

    pergunta=input("\nDeseja fazer novamente? (s/n)").strip().lower()
    if pergunta != "s":
        break
