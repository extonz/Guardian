#!/usr/bin/env python3
"""
Script de limpieza para preparar el proyecto para GitHub.
Elimina archivos innecesarios y organiza la estructura.
"""

import os
import shutil
from pathlib import Path

def clean_project():
    """Limpia el proyecto para GitHub."""
    root = Path(".")
    
    # Archivos a eliminar
    files_to_remove = [
        "main.exe",
        "main.spec",
        "organize.py",
        "NUEVAS_FUNCIONES.md",  # Documentación antigua
        "CAMBIOS_NUEVOS.md",     # Documentación antigua
    ]
    
    # Directorios a eliminar
    dirs_to_remove = [
        "build",
        "dist",
        "__pycache__",
    ]
    
    print("🧹 Limpiando proyecto...")
    
    # Eliminar archivos
    for file in files_to_remove:
        file_path = root / file
        if file_path.exists():
            file_path.unlink()
            print(f"  ✓ Eliminado: {file}")
    
    # Eliminar directorios
    for dir_name in dirs_to_remove:
        dir_path = root / dir_name
        if dir_path.exists():
            shutil.rmtree(dir_path)
            print(f"  ✓ Eliminada carpeta: {dir_name}")
    
    # Limpiar __pycache__ recursivamente
    for pycache_dir in root.rglob("__pycache__"):
        shutil.rmtree(pycache_dir)
        print(f"  ✓ Eliminada carpeta: {pycache_dir}")
    
    # Eliminar archivos .pyc
    for pyc_file in root.rglob("*.pyc"):
        pyc_file.unlink()
        print(f"  ✓ Eliminado: {pyc_file}")
    
    # Asegurar que existe data/
    data_dir = root / "data"
    data_dir.mkdir(exist_ok=True)
    (data_dir / ".gitkeep").touch()
    
    # Asegurar que existe tests/
    tests_dir = root / "tests"
    tests_dir.mkdir(exist_ok=True)
    (tests_dir / ".gitkeep").touch()
    
    print("\n✅ Limpieza completada!")
    print("\n📋 Próximos pasos:")
    print("  1. Revisa la estructura del proyecto")
    print("  2. Actualiza los URLs en README_MAIN.md")
    print("  3. Ejecuta: git add .")
    print("  4. Ejecuta: git commit -m 'feat: add new features and reorganize'")
    print("  5. Ejecuta: git push origin main")

if __name__ == "__main__":
    clean_project()
