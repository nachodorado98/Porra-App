variable "nombre_grupo_recursos" {
  description = "El nombre del grupo de recursos"
}

variable "localizacion_grupo_recursos" {
  description = "La region de Azure Region donde todos los recursos se van a crear"
}

variable "nombre_log_analytics" {
  description = "El nombre del log analytics"
}

variable "nombre_entorno_apps" {
  description = "El nombre del entorno de las apps"
}

variable "nombre_app" {
  description = "El nombre de la app (Container App)"
}

variable "nombre_contenedor" {
  description = "El nombre del contenedor"
}

variable "nombre_imagen_contenedor" {
  description = "El nombre de la imagen del contenedor"
}

variable "entorno" {
  description = "Entorno de la aplicacion"
}

variable "user" {
  description = "Usuario de la BBDD"
}

variable "password" {
  description = "Password de la BBDD"
}

variable "db" {
  description = "Nombre de la BBDD"
}

variable "host" {
  description = "Host de la BBDD"
}

variable "port" {
  description = "Port de la BBDD"
}

variable "nombre_storage_account" {
  description = "El nombre de la cuenta de almacenamiento"
}

variable "nombre_service_plan" {
  description = "El nombre del Service Plan"
}

variable "nombre_az_function" {
  description = "El nombre de la Azure Function"
}

variable "email_account" {
  type        = string
  sensitive   = true
  description = "La cuenta de correo"
}

variable "contrasena_login" {
  type        = string
  sensitive   = true
  description = "La contraseña de la cuenta de correo"
}

variable "servidor_correo" {
  type        = string
  description = "El servidor de correo"
}

variable "puerto_correo" {
  type        = string
  description = "El puerto del servidor de correo"
}

variable "endpoint_az_function" {
  description = "El endpoint de la Azure Function"
}