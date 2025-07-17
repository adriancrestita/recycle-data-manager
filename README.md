/gestion_datos_reciclaje/
│
├── app.py                           # Punto de entrada. Lanza interfaz Tkinter.
│
├── config/
│   └── .env                         # Variables de entorno: DB_URL, etc.
│
├── db/
│   ├── conexion.py                  # Función para conectar a PostgreSQL
│   └── schema.sql                   # Script SQL con creación de tablas
│
├── logica/
│   ├── empresas.py                  # CRUD de empresas
│   ├── auditorias.py                # CRUD de auditorías
│   ├── csv_importer.py              # Procesa CSV y valida antes de insertar
│   ├── validador.py                 # Validación de email, fecha, duplicados
│   ├── mailing_export.py            # Exporta correos pendientes a CSV
│   ├── logs.py                      # Manejo de logs de envío e importación
│   └── util.py                      # Funciones auxiliares comunes
│
├── ui/
│   ├── pantalla_principal.py        # Menú principal con botones
│   ├── formulario_empresa.py        # Interfaz para crear empresa
│   ├── formulario_auditoria.py      # Crear auditorías por empresa
│   ├── carga_csv.py                 # Subida de CSV, muestra feedback
│   └── ver_logs.py                  # Vista de logs de envío
│
├── scripts/
│   └── envio_programado.py          # Script CLI para exportar correos automáticamente
│
├── data/
│   ├── empresas.csv                 # CSV de prueba para empresas
│   ├── auditorias.csv              # CSV de prueba para auditorías
│   └── contactos_pendientes.csv     # CSV generado para envío por GAS
│
├── requirements.txt                 # Librerías necesarias
└── README.md                        # Documentación de uso del sistema
