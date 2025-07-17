CREATE TABLE empresas (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT UNIQUE NOT NULL CHECK (correo ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    telefono TEXT,
    cp TEXT,
    provincia TEXT,
    direccion TEXT,
    url_web TEXT,
    sector TEXT
);


CREATE TABLE envios_mail (
    id SERIAL PRIMARY KEY,
    id_empresa INTEGER REFERENCES empresas(id) ON DELETE CASCADE,
    fecha_envio DATE NOT NULL,
    baja BOOLEAN DEFAULT FALSE,
    estado TEXT CHECK (estado IN ('pendiente', 'enviado')) NOT NULL
);


CREATE TABLE csv_imports_log (
    id SERIAL PRIMARY KEY,
    nombre_archivo TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    registros_validos INTEGER NOT NULL CHECK (registros_validos >= 0)
);

