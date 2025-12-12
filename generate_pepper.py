"""
Script para generar y configurar APP_PEPPER en el archivo .env

Este script genera una clave criptográfica segura y la almacena en el archivo .env
para que sea utilizada por la aplicación como pepper en el hash de contraseñas.
"""

import os
import secrets
from pathlib import Path


def generate_pepper(length: int = 32) -> str:
    """
    Genera una clave aleatoria segura usando secrets.

    Args:
        length: Longitud de la clave en caracteres (por defecto 32)

    Returns:
        Una cadena codificada en base64 segura para URLs
    """
    return secrets.token_urlsafe(length)


def create_env_file(pepper: str, env_path: str = ".env") -> bool:
    """
    Crea o actualiza el archivo .env con la variable APP_PEPPER.

    Args:
        pepper: El valor del pepper a almacenar
        env_path: Ruta del archivo .env (por defecto ".env")

    Returns:
        True si se completó exitosamente, False en caso contrario
    """
    try:
        env_file = Path(env_path)

        # Leer contenido existente si el archivo existe
        existing_content = ""
        if env_file.exists():
            with open(env_file, "r", encoding="utf-8") as f:
                existing_content = f.read()

        # Preparar el nuevo contenido
        lines = existing_content.strip().split("\n") if existing_content.strip() else []

        # Remover línea existente de APP_PEPPER si la hay
        lines = [line for line in lines if not line.startswith("APP_PEPPER=")]

        # Agregar el nuevo APP_PEPPER
        lines.append(f"APP_PEPPER={pepper}")

        # Escribir el archivo actualizado
        with open(env_file, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")

        return True

    except Exception as e:
        print(f"❌ Error al crear/actualizar .env: {e}")
        return False


def create_env_example(env_path: str = ".env.example") -> bool:
    """
    Crea un archivo .env.example como referencia.

    Args:
        env_path: Ruta del archivo .env.example

    Returns:
        True si se completó exitosamente, False en caso contrario
    """
    try:
        example_content = """# Variables de entorno para la aplicación de autenticación

# APP_PEPPER: Clave secreta utilizada como "pepper" en el hash de contraseñas
# Esta clave se concatena a la contraseña del usuario antes de aplicar Argon2id
# Generar una clave segura con: python generate_pepper.py
# IMPORTANTE: Nunca compartir esta clave o incluirla en repositorios públicos
APP_PEPPER=tu_clave_super_secreta_de_32_caracteres_aqui
"""

        with open(env_path, "w", encoding="utf-8") as f:
            f.write(example_content)

        return True

    except Exception as e:
        print(f"❌ Error al crear .env.example: {e}")
        return False


def main():
    """
    Función principal del script.
    Genera un pepper seguro y lo configura en el archivo .env.
    """
    print("=" * 60)
    print("🔐 Generador de APP_PEPPER para Autenticación Segura")
    print("=" * 60)
    print()

    # Generar el pepper
    print("⏳ Generando clave criptográfica segura...")
    pepper = generate_pepper(32)

    print(f"✅ Clave generada exitosamente!")
    print()
    print("📝 Información de la clave:")
    print(f"   Valor: {pepper}")
    print(f"   Longitud: {len(pepper)} caracteres")
    print()

    # Crear/actualizar .env
    print("💾 Guardando en archivo .env...")
    if create_env_file(pepper):
        print("✅ Archivo .env actualizado correctamente!")
    else:
        print("❌ Error al actualizar .env")
        return False

    # Crear .env.example
    print("📄 Creando archivo .env.example como referencia...")
    if create_env_example():
        print("✅ Archivo .env.example creado correctamente!")
    else:
        print("⚠️  Advertencia: No se pudo crear .env.example")

    print()
    print("=" * 60)
    print("✨ ¡Configuración completada!")
    print("=" * 60)
    print()
    print("📌 Próximos pasos:")
    print("   1. Asegúrate de que .env esté en .gitignore")
    print("   2. Ejecuta la aplicación: uvicorn main:app --reload")
    print("   3. Accede a los docs en: http://127.0.0.1:8000/docs")
    print()
    print("⚠️  IMPORTANTE:")
    print("   - Nunca expongas el contenido de .env en repositorios públicos")
    print("   - Usa HTTPS en producción")
    print("   - Implementa rate limiting para prevenir fuerza bruta")
    print()

    return True


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
