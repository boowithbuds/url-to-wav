#!/usr/bin/env python3
import subprocess
import sys
import os
from datetime import datetime


# ─────────────────────────────────────────────
#  AUTO-INSTALADOR DE DEPENDENCIAS
#  Se ejecuta siempre antes de descargar.
#  Comprueba si cada herramienta está instalada
#  y la instala/actualiza si hace falta.
# ─────────────────────────────────────────────

def comando_existe(cmd):
    """Devuelve True si el comando está disponible en el sistema"""
    return subprocess.run(["which", cmd], capture_output=True).returncode == 0

def instalar_dependencias():
    print("🔧 Verificando dependencias...\n")

    # Homebrew — gestor de paquetes para Mac, necesario para instalar ffmpeg y deno
    if not comando_existe("brew"):
        print("📦 Instalando Homebrew...")
        os.system('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')
    else:
        print("✅ Homebrew OK")

    # yt-dlp — herramienta que hace la descarga. Se actualiza siempre para evitar errores 403
    if not comando_existe("yt-dlp"):
        print("📦 Instalando yt-dlp...")
        subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], capture_output=True)
    else:
        print("⬆️  Actualizando yt-dlp...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"], capture_output=True)

    # ffmpeg — convierte el audio descargado al formato WAV
    if not comando_existe("ffmpeg"):
        print("📦 Instalando ffmpeg...")
        subprocess.run(["brew", "install", "ffmpeg"], capture_output=True)
    else:
        print("✅ ffmpeg OK")

    # deno — runtime de JavaScript que yt-dlp necesita para resolver
    # los challenges de YouTube (sin esto da error 403 en muchos videos)
    if not comando_existe("deno"):
        print("📦 Instalando deno...")
        subprocess.run(["brew", "install", "deno"], capture_output=True)
    else:
        print("✅ deno OK")

    print("\n✅ Todo listo!\n" + "─"*50 + "\n")


# ─────────────────────────────────────────────
#  DESCARGADOR
#  Recibe la URL, construye el comando yt-dlp
#  y guarda el audio como WAV en la carpeta destino.
# ─────────────────────────────────────────────

def descargar_audio_ig(url, carpeta_destino="~/Desktop"):
    """Descarga audio de video y lo convierte a WAV"""

    # Expandir ~ a la ruta real del usuario (ej: /Users/pvk/Desktop)
    carpeta_destino = os.path.expanduser(carpeta_destino)
    os.makedirs(carpeta_destino, exist_ok=True)

    # Timestamp en el nombre para no sobreescribir archivos anteriores
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = os.path.join(carpeta_destino, f"ig_audio_{timestamp}.wav")

    # Comando yt-dlp:
    #   -x              → extraer solo audio (sin video)
    #   --audio-format  → convertir a WAV usando ffmpeg
    #   -o              → ruta de salida del archivo
    comando = [
        "yt-dlp",
        "-x",
        "--audio-format", "wav",
        "-o", output,
        url
    ]

    print(f"📥 Descargando de: {url}\n")
    result = subprocess.run(comando)

    # Comprobar que el proceso terminó bien Y que el archivo existe
    if result.returncode == 0 and os.path.exists(output):
        print(f"\n✅ Audio guardado en: {output}")
        return output
    else:
        print(f"\n❌ Error al descargar")
        return None


# ─────────────────────────────────────────────
#  MAIN
#  Punto de entrada del script.
#  Lee la URL desde los argumentos de la terminal,
#  instala dependencias y lanza la descarga.
# ─────────────────────────────────────────────

if __name__ == "__main__":

    # Comprobar que se pasó al menos una URL como argumento
    if len(sys.argv) < 2:
        print("Uso: python3 Ig_Sampler.py <URL_DE_video>")
        print("Ejemplo: python3 Ig_Sampler.py 'https://www.instagram.com/reel/ABC123/'")
        sys.exit(1)

    # Instalar/actualizar todo antes de intentar descargar
    instalar_dependencias()

    url = sys.argv[1]
    descargar_audio_ig(url)

#### Use with: python3 url-to-wav.py "VideoUrl" ####