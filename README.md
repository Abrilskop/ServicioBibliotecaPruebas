# 📚 Servicio de Biblioteca - TDD (Laboratorio 08)

Este proyecto implementa la capa de acceso a datos (DAO) para un sistema de biblioteca utilizando la metodología **TDD (Test Driven Development)** y el patrón de diseño **Singleton**.

El objetivo principal es demostrar la aplicación del ciclo **Rojo-Verde-Refactor**, utilizando **Mocks** para aislar las pruebas unitarias de la base de datos real.

## 🚀 Características del Proyecto

*   **Metodología TDD:** Todo el código funcional fue escrito *después* de crear una prueba fallida (Fase Roja).
*   **Unit Testing:** Pruebas unitarias con el framework nativo `unittest` de Python.
*   **Mocking:** Uso de `unittest.mock.MagicMock` para simular conexiones a MySQL y cursores, permitiendo ejecutar el proyecto sin necesidad de un servidor de base de datos activo.
*   **Arquitectura Limpia:** Separación de responsabilidades en capas (`dao`, `entidades`, `conexion`).

## 🛠️ Estructura del Proyecto

```text
ServicioBiblioteca/
├── conexion/           # Patrón Singleton y configuración de DB
│   ├── BaseConexion.py
│   ├── Conexion.py
│   └── Configuracion.py
├── dao/                # Data Access Objects (Lógica implementada)
│   ├── LibroDAO.py
│   ├── EjemplarDAO.py      # Implementado mediante TDD
│   ├── SolicitanteDAO.py   # Implementado mediante TDD
│   └── PrestamoDAO.py      # Implementado mediante TDD
├── entidades/          # Clases de Dominio (POJOs)
│   ├── CLibro.py
│   ├── CEjemplar.py
│   ├── CSolicitante.py
│   └── CPrestamo.py
├── pruebas/            # Pruebas Unitarias
│   ├── test_PruebasConexion.py
│   ├── test_PruebaLibroDAO.py
│   ├── test_EjemplarDAO.py
│   ├── test_SolicitanteDAO.py
│   └── test_PrestamoDAO.py
└── README.md
```

##  Requisitos Previos

*   **Python 3.x** instalado.
*   No se requieren librerías externas para ejecutar las pruebas (se utilizan librerías estándar).

## 🧪 Cómo Ejecutar las Pruebas (TDD)

Para verificar que todos los módulos (`Ejemplar`, `Solicitante`, `Préstamo`, `Libro`) pasan las pruebas correctamente, puedes ejecutar los tests desde la terminal.

### Opción 1: Ejecutar todas las pruebas (Recomendado)
Desde la carpeta raíz del proyecto, ejecuta:

```bash
python -m unittest discover -s pruebas -p "test_*.py"
```

### Opción 2: Ejecutar un módulo específico

Si deseas probar solo una clase (por ejemplo, Ejemplar):

```bash
python -m unittest pruebas/test_EjemplarDAO.py