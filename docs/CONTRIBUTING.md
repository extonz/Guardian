# 🤝 Guía de Contribución

¡Gracias por tu interés en contribuir a Guardian! Aquí está cómo puedes ayudar.


## Cómo Contribuir

### Reportar Bugs

1. Ve a [Issues](https://github.com/extonz/guardian/issues)
2. Haz clic en "New Issue"
3. Usa el template de bug report
4. Incluye:
   - Descripción clara del problema
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Sistema operativo y versión de Python
   - Screenshots si es relevante

### Proponer Mejoras

1. Ve a [Discussions](https://github.com/extonz/guardian/discussions)
2. Crea una nueva discussion
3. Describe la mejora y por qué sería útil

### Enviar Pull Requests

1. **Fork el repositorio**
   ```bash
   git clone https://github.com/extonz/guardian.git
   cd guardian
   ```

2. **Crea una rama para tu feature**
   ```bash
   git checkout -b feature/AmazingFeature
   ```

3. **Realiza tus cambios**
   - Sigue el estilo de código existente
   - Añade tests si es posible
   - Actualiza documentación

4. **Commit tus cambios**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```

5. **Push a tu rama**
   ```bash
   git push origin feature/AmazingFeature
   ```

6. **Abre un Pull Request**
   - Describe claramente qué cambios haces
   - Referencia issues relacionados
   - Incluye screenshots si es relevante

## Guía de Estilo

### Python

- Seguir [PEP 8](https://pep8.org/)
- Usar nombres descriptivos
- Documentar funciones con docstrings
- Máximo 88 caracteres por línea

```python
def amazing_function(param1, param2):
    """
    Descripción clara de qué hace la función.
    
    Args:
        param1: Descripción del parámetro
        param2: Descripción del parámetro
    
    Returns:
        Descripción del valor retornado
    """
    return result
```

### Commits

- Usar mensajes descriptivos
- Primera línea: máximo 50 caracteres
- Explicación en las siguientes líneas si es necesario

```
Add support for custom themes

- Implement ThemeManager class
- Add three predefined themes
- Update documentation
```

### Documentación

- Mantener README.md actualizado
- Documentar nuevas características
- Incluir ejemplos de uso
- Actualizar CHANGELOG.md

## Proceso de Review

1. Los maintainers revisarán tu PR
2. Pedirán cambios si es necesario
3. Una vez aprobado, será mergeado

## Configuración de Desarrollo

```bash
# Instalar en modo desarrollo
pip install -e .

# Instalar herramientas de desarrollo
pip install pytest black flake8 mypy

# Ejecutar tests
pytest

# Verificar estilo
black --check .
flake8 .
mypy .
```

## Estructura de Directorios

```
guardian/
├── src/           # Código fuente
├── ui/            # Interfaz de usuario
├── docs/          # Documentación
├── tests/         # Tests unitarios
├── main.py        # Punto de entrada
└── requirements.txt
```

## Áreas para Contribuir

### Desarrollo
- [ ] Nuevas características
- [ ] Mejoras de UI/UX
- [ ] Optimizaciones de rendimiento
- [ ] Soporte para más SO

### Documentación
- [ ] Traducciones
- [ ] Mejoras en README
- [ ] Ejemplos adicionales
- [ ] Tutoriales

### Testing
- [ ] Tests unitarios
- [ ] Tests de integración
- [ ] Pruebas de compatibilidad

### Community
- [ ] Responder preguntas
- [ ] Ayudar con issues
- [ ] Compartir ideas en discussions

## Licencia

Al contribuir, aceptas que tus cambios serán licenciados bajo MIT License.

## Preguntas

Si tienes preguntas:
- Abre una [Discussion](https://github.com/extonz/guardian/discussions)
- Contacta al autor
- Revisa la documentación existente

¡Gracias por contribuir! 🎉
