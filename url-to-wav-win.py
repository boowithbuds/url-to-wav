import subprocess
import sys
import os
import shutil
from datetime import datetime


# ─────────────────────────────────────────────
#  AUTO-INSTALADOR DE DEPENDENCIAS (WINDOWS)
# ─────────────────────────────────────────────

def comando_existe(cmd):
    """Devuelve True si el comando está disponible en el sistema"""
    return shutil.which(cmd) is not None

def instalar_dependencias():
    print("🔧 Verificando dependencias en Windows...\n")

    # yt-dlp — se instala/actualiza mediante pip
    if not comando_existe("yt-dlp"):
        print("📦 Instalando yt-dlp...")
        subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], capture_output=True)
    else:
        print("⬆️ Actualizando yt-dlp...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-U", "yt-dlp"], capture_output=True)

    # ffmpeg — se instala usando winget si no está presente
    if not comando_existe("ffmpeg"):
        print("📦 Instalando ffmpeg...")
        if comando_existe("winget"):
            subprocess.run([
                "winget", "install", "-e", "--id", "Gyan.FFmpeg", 
                "--accept-source-agreements", "--accept-package-agreements"
            ], capture_output=True)
        else:
            print("⚠️ 'winget' no está disponible. Por favor instala ffmpeg manualmente.")
    else:
        print("✅ ffmpeg OK")

    # deno — se instala usando winget para evitar errores 403
    if not comando_existe("deno"):
        print("📦 Instalando deno...")
        if comando_existe("winget"):
            subprocess.run([
                "winget", "install", "-e", "--id", "DenoLand.Deno", 
                "--accept-source-agreements", "--accept-package-agreements"
            ], capture_output=True)
        else:
            print("⚠️ 'winget' no está disponible. Por favor instala deno manualmente.")
    else:
        print("✅ deno OK")

    print("\n✅ Todo listo!\n" + "─"*50 + "\n")


# ─────────────────────────────────────────────
#  DESCARGADOR
# ─────────────────────────────────────────────

def descargar_audio_ig(url, carpeta_destino="~/Desktop"):
    """Descarga audio de video y lo convierte a WAV"""

    # Expandir ~ al Escritorio de Windows (ej: C:\Users\TuUsuario\Desktop)
    carpeta_destino = os.path.expanduser(carpeta_destino)
    os.makedirs(carpeta_destino, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output = os.path.join(carpeta_destino, f"ig_audio_{timestamp}.wav")

    comando = [
        "yt-dlp",
        "-x",
        "--audio-format", "wav",
        "-o", output,
        url
    ]

    print(f"📥 Descargando de: {url}\n")
    result = subprocess.run(comando)

    if result.returncode == 0 and os.path.exists(output):
        print(f"\n✅ Audio guardado en: {output}")
        return output
    else:
        print(f"\n❌ Error al descargar")
        return None


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Uso: python Ig_Sampler_Win.py <URL_DE_video>")
        print("Ejemplo: python Ig_Sampler_Win.py \"https://www.instagram.com/reel/ABC123/\"")
        sys.exit(1)

    instalar_dependencias()

    url = sys.argv[1]
    descargar_audio_ig(url)
