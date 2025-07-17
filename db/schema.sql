-- Tabla empresas
CREATE TABLE empresas (
    id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE CHECK (correo ~* '^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$'),
    telefono TEXT,
    provincia TEXT,
    direccion TEXT,
    cp TEXT,
    url_web TEXT,
    sector TEXT
);

-- Tabla envios_mail
CREATE TABLE envios_mail (
    id SERIAL PRIMARY KEY,
    id_empresa INTEGER REFERENCES empresas(id) ON DELETE SET NULL,
    fecha_envio DATE NOT NULL,
    estado TEXT CHECK (estado IN ('pendiente', 'enviado', 'error')) DEFAULT 'pendiente',
    baja BOOLEAN DEFAULT FALSE,
    error TEXT
);
