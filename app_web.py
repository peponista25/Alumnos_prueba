import streamlit as st
from supabase import create_client, Client

# Configuración visual para celulares
st.set_page_config(page_title="Seguimiento Escolar", page_icon="🏫", layout="centered")

# 1. CONEXIÓN A SUPABASE
SUPABASE_URL = "https://libvhnsryvyhsytfandl.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxpYnZobnNyeXZ5aHN5dGZhbmRsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3OTE5MDcwMzQsImV4cCI6MjEwNzQ4MzAzNH0.pgzLmsiU1vgYuV4StnWRSEfRfu8XMD9iKoAaTV4K5Q0"

# Esta función evita que se conecte mil veces a la base de datos
@st.cache_resource
def iniciar_conexion():
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = iniciar_conexion()

# 2. ENCABEZADO
st.title("📱 Seguimiento Escolar")
st.write("Agrega o consulta alumnos desde cualquier dispositivo.")

# 3. FORMULARIO PARA AGREGAR ALUMNOS
st.header("Registrar Nuevo Alumno")
with st.form("formulario_alumnos", clear_on_submit=True):
    nombre = st.text_input("Apellido y Nombres")
    dni = st.text_input("DNI")
    edad = st.number_input("Edad", min_value=10, max_value=99, step=1)
    curso = st.text_input("Curso (Ej: 1er Año)")
    telefono = st.text_input("Teléfono")
    
    # Botón de guardar
    boton_guardar = st.form_submit_button("Guardar en la Nube", use_container_width=True)

if boton_guardar:
    if nombre and dni:
        datos = {
            "apellido_nombres": nombre,
            "dni": dni,
            "edad": edad,
            "curso": curso,
            "telefono": telefono
        }
        try:
            supabase.table("alumnos").insert(datos).execute()
            st.success("¡Alumno guardado correctamente!")
        except Exception as e:
            st.error(f"Error al guardar: {e}")
    else:
        st.warning("Por favor completa al menos el Nombre y el DNI.")

st.divider() # Línea separadora

# 4. LISTA DE ALUMNOS (ESTILO CELULAR)
st.header("📋 Lista de Alumnos")

try:
    respuesta = supabase.table("alumnos").select("*").execute()
    alumnos = respuesta.data
    
    if alumnos:
        for alumno in alumnos:
            # Crea un menú desplegable por cada alumno (ideal para pantallas táctiles)
            with st.expander(f"👤 {alumno['apellido_nombres']} - {alumno['curso']}"):
                st.write(f"**DNI:** {alumno['dni']}")
                st.write(f"**Edad:** {alumno['edad']} años")
                st.write(f"**Teléfono:** {alumno['telefono']}")
    else:
        st.info("Todavía no hay alumnos registrados.")
except Exception as e:
    st.error(f"Error al cargar la base de datos: {e}")