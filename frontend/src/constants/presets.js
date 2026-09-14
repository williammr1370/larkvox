/**
 * Textos predefinidos, modelos y usuarios para el panel de pruebas.
 */

export const TEXT_PRESETS = [
  {
    id: "saludo",
    label: "Saludo",
    text: "Hola, soy el asistente virtual del Proyecto LarkVox. ¿En qué puedo ayudarte hoy?",
  },
  {
    id: "espera",
    label: "Espera",
    text: "Gracias por llamar. Voy a revisar tu información, por favor espera un momento.",
  },
  {
    id: "cierre",
    label: "Cierre",
    text: "He recibido tus datos correctamente. Un agente se pondrá en contacto contigo en las próximas 24 horas. ¡Que tengas un buen día!",
  },
  {
    id: "numero",
    label: "Números",
    text: "Tu número de pedido es el 4 5 8 7 2 1. Repito, 4 5 8 7 2 1.",
  },
  {
    id: "fecha",
    label: "Fecha/Hora",
    text: "Tu cita está agendada para el martes 15 de septiembre a las 3 y 30 de la tarde.",
  },
];

export const MODELOS_DISPONIBLES = [
  {
    model_id: "eleven_flash_v2_5",
    name: "Flash v2.5 (ultra rápido)",
    description: "Ultra baja latencia · 32 idiomas · Ideal para conversación",
    recomendado: true,
  },
  {
    model_id: "eleven_turbo_v2_5",
    name: "Turbo v2.5 (equilibrado)",
    description: "Buena calidad · Baja latencia · 32 idiomas",
  },
  {
    model_id: "eleven_multilingual_v2",
    name: "Multilingual v2 (alta calidad)",
    description: "Máxima naturalidad · 29 idiomas · Mayor latencia",
  },
  {
    model_id: "eleven_v3_conversational",
    name: "v3 Conversational (experimental)",
    description: "El más expresivo · Optimizado para diálogo · 70+ idiomas",
  },
  {
    model_id: "eleven_v3",
    name: "v3 (máxima expresividad)",
    description: "El más expresivo · Requiere prompt engineering · 70+ idiomas",
  },
];

export const USUARIOS = ["William", "Agustina"];