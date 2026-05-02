# agent/tools.py — Herramientas del agente NexGen Automations
import os
import yaml
import logging
from datetime import datetime

logger = logging.getLogger("agentkit")


def cargar_info_negocio() -> dict:
    """Carga la información del negocio desde business.yaml."""
    try:
        with open("config/business.yaml", "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logger.error("config/business.yaml no encontrado")
        return {}


def obtener_horario() -> dict:
    """Retorna el horario de atención del negocio."""
    info = cargar_info_negocio()
    return {
        "horario": info.get("negocio", {}).get("horario", "24/7"),
        "esta_abierto": True,  # NexGen atiende 24/7
    }


def buscar_en_knowledge(consulta: str) -> str:
    """Busca información relevante en los archivos de /knowledge."""
    resultados = []
    knowledge_dir = "knowledge"

    if not os.path.exists(knowledge_dir):
        return "No hay archivos de conocimiento disponibles."

    for archivo in os.listdir(knowledge_dir):
        ruta = os.path.join(knowledge_dir, archivo)
        if archivo.startswith(".") or not os.path.isfile(ruta):
            continue
        try:
            with open(ruta, "r", encoding="utf-8") as f:
                contenido = f.read()
                if consulta.lower() in contenido.lower():
                    resultados.append(f"[{archivo}]: {contenido[:500]}")
        except (UnicodeDecodeError, IOError):
            continue

    return "\n---\n".join(resultados) if resultados else "No encontré información específica sobre eso."


def registrar_lead(telefono: str, tipo_negocio: str, empleados: str, problema: str) -> dict:
    """Registra un lead calificado con su información."""
    lead = {
        "telefono": telefono,
        "tipo_negocio": tipo_negocio,
        "empleados": empleados,
        "problema": problema,
        "fecha": datetime.utcnow().isoformat(),
        "estado": "calificado",
    }
    logger.info(f"Lead registrado: {telefono} — {tipo_negocio}")
    return lead


def solicitar_sesion_consultoria(telefono: str, nombre: str, email: str, disponibilidad: str) -> dict:
    """Registra una solicitud de sesión de consultoría gratuita."""
    solicitud = {
        "telefono": telefono,
        "nombre": nombre,
        "email": email,
        "disponibilidad": disponibilidad,
        "fecha_solicitud": datetime.utcnow().isoformat(),
        "estado": "pendiente",
    }
    logger.info(f"Sesión solicitada: {nombre} ({email})")
    return solicitud


def recomendar_servicio(empleados: int, problema: str) -> str:
    """Recomienda el servicio de NexGen más adecuado según el perfil del lead."""
    problema_lower = problema.lower()

    if "clientes" in problema_lower or "leads" in problema_lower or "ventas" in problema_lower:
        if empleados <= 5:
            return "Sistema de Respuesta Automática por WhatsApp"
        else:
            return "Agente de IA para Captar y Calificar Clientes"
    elif "organización" in problema_lower or "crm" in problema_lower or "sistema" in problema_lower:
        return "Ecosistema Digital Completo"
    elif "tiempo" in problema_lower or "personal" in problema_lower:
        return "Sistema de Respuesta Automática por WhatsApp"
    else:
        return "Sesión de consultoría gratuita para evaluar la mejor solución"
