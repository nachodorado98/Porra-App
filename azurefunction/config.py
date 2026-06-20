import os

EMAIL_ACCOUNT=os.environ.get("EMAIL_ACCOUNT")
CONTRASENA_LOGIN=os.environ.get("CONTRASENA_LOGIN")
SERVIDOR_CORREO=os.environ.get("SERVIDOR_CORREO")
PUERTO_CORREO=int(os.environ.get("PUERTO_CORREO"))
URL_APP=os.environ.get("URL_APP")

ASUNTO_CORREO_BIENVENIDA="¡Bienvenido a nuestra familia!"
HTML_CORREO_BIENVENIDA="""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="x-apple-disable-message-reformatting">
    <meta name="color-scheme" content="light">
    <meta name="supported-color-schemes" content="light">
    <title>Bienvenido a Porra App</title>
    <style>
        @media only screen and (max-width: 620px) {{
            .container {{ width: 100% !important; }}
            .px {{ padding-left: 24px !important; padding-right: 24px !important; }}
            .h1 {{ font-size: 22px !important; line-height: 30px !important; }}
            .code {{ font-size: 22px !important; letter-spacing: 4px !important; }}
        }}
    </style>
</head>
<body style="margin:0; padding:0; background-color:#f2f4f7; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; -webkit-font-smoothing:antialiased;">

    <div style="display:none; max-height:0; overflow:hidden; opacity:0; visibility:hidden; mso-hide:all; font-size:1px; line-height:1px; color:#f2f4f7;">
        Tu registro en Porra App se ha completado. Aquí tienes el código de tu liga.
    </div>

    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f2f4f7;">
        <tr>
            <td align="center" style="padding:32px 16px;">

                <table role="presentation" class="container" width="600" border="0" cellspacing="0" cellpadding="0" style="width:600px; max-width:600px; background-color:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 4px 16px rgba(16,24,40,0.06);">

                    <!-- Header -->
                    <tr>
                        <td align="center" style="background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%); background-color:#0f172a; padding:36px 24px; color:#ffffff;">
                            <h1 style="margin:0; font-size:26px; line-height:32px; font-weight:700; letter-spacing:-0.5px; color:#ffffff;">⚽ Porra App</h1>
                            <p style="margin:8px 0 0; font-size:14px; color:#cbd5e1;">Tu liga de predicciones de fútbol</p>
                        </td>
                    </tr>

                    <!-- Content -->
                    <tr>
                        <td class="px" style="padding:40px 48px 16px; color:#0f172a;">
                            <h2 class="h1" style="margin:0 0 16px; font-size:24px; line-height:32px; font-weight:600; color:#0f172a;">¡Hola, {nombre}! 👋</h2>
                            <p style="margin:0 0 16px; font-size:16px; line-height:24px; color:#475467;">
                                Te confirmamos que tu registro en <strong style="color:#0f172a;">Porra App</strong> se ha completado correctamente. Ya puedes acceder a todas las funcionalidades de la plataforma y empezar a competir con tus amigos.
                            </p>
                            <p style="margin:0 0 24px; font-size:16px; line-height:24px; color:#475467;">
                                Te has unido a tu liga con el siguiente código. Compártelo con tus amigos para que se unan contigo:
                            </p>
                        </td>
                    </tr>

                    <!-- Code box -->
                    <tr>
                        <td class="px" align="center" style="padding:0 48px 32px;">
                            <table role="presentation" border="0" cellspacing="0" cellpadding="0" style="background-color:#f8fafc; border:1px dashed #cbd5e1; border-radius:10px;">
                                <tr>
                                    <td align="center" style="padding:20px 32px;">
                                        <p style="margin:0 0 6px; font-size:12px; letter-spacing:1.5px; text-transform:uppercase; color:#64748b; font-weight:600;">Código de tu liga</p>
                                        <p class="code" style="margin:0; font-family:'Courier New',Consolas,monospace; font-size:28px; letter-spacing:6px; font-weight:700; color:#0f172a;">{codigo}</p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- Sign-off -->
                    <tr>
                        <td class="px" style="padding:0 48px 40px;">
                            <p style="margin:0 0 4px; font-size:16px; line-height:24px; color:#475467;">Un saludo,</p>
                            <p style="margin:0; font-size:16px; line-height:24px; color:#0f172a; font-weight:600;">El equipo de Porra App</p>
                        </td>
                    </tr>

                    <!-- Divider -->
                    <tr>
                        <td style="padding:0 48px;">
                            <hr style="border:none; border-top:1px solid #e4e7ec; margin:0;">
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td align="center" style="padding:24px 48px 32px;">
                            <p style="margin:0 0 8px; font-size:12px; line-height:18px; color:#98a2b3;">
                                Este es un correo automático. Por favor, no respondas a este mensaje.
                            </p>
                            <p style="margin:0; font-size:12px; line-height:18px; color:#98a2b3;">
                                &copy; 2026 Porra App. Todos los derechos reservados.
                            </p>
                        </td>
                    </tr>

                </table>

            </td>
        </tr>
    </table>

</body>
</html>
"""



ASUNTO_CORREO_LANZAMIENTO="🚀 ¡Porra App ya está disponible!"
HTML_CORREO_LANZAMIENTO="""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="x-apple-disable-message-reformatting">
    <meta name="color-scheme" content="light">
    <meta name="supported-color-schemes" content="light">
    <title>Porra App ya está disponible</title>
    <style>
        @media only screen and (max-width: 620px) {{
            .container {{ width: 100% !important; }}
            .px {{ padding-left: 24px !important; padding-right: 24px !important; }}
            .h1 {{ font-size: 22px !important; line-height: 30px !important; }}
        }}
    </style>
</head>
<body style="margin:0; padding:0; background-color:#f2f4f7; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; -webkit-font-smoothing:antialiased;">

    <div style="display:none; max-height:0; overflow:hidden; opacity:0; visibility:hidden; mso-hide:all; font-size:1px; line-height:1px; color:#f2f4f7;">
        Porra App ya está disponible. Aquí tienes tus datos de acceso.
    </div>

    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f2f4f7;">
        <tr>
            <td align="center" style="padding:32px 16px;">

                <table role="presentation" class="container" width="600" border="0" cellspacing="0" cellpadding="0"
                       style="width:600px; max-width:600px; background-color:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 4px 16px rgba(16,24,40,0.06);">

                    <!-- Header -->
                    <tr>
                        <td align="center" style="background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%); background-color:#0f172a; padding:36px 24px; color:#ffffff;">
                            <h1 style="margin:0; font-size:26px; line-height:32px; font-weight:700; letter-spacing:-0.5px; color:#ffffff;">
                                ⚽ Porra App
                            </h1>
                            <p style="margin:8px 0 0; font-size:14px; color:#cbd5e1;">
                                Tu liga de predicciones de fútbol
                            </p>
                        </td>
                    </tr>

                    <!-- Content -->
                    <tr>
                        <td class="px" style="padding:40px 48px 24px; color:#0f172a;">
                            <h2 class="h1" style="margin:0 0 16px; font-size:24px; line-height:32px; font-weight:600; color:#0f172a;">
                                ¡Hola, {nombre}! 👋
                            </h2>

                            <p style="margin:0 0 16px; font-size:16px; line-height:24px; color:#475467;">
                                Tenemos una buena noticia: <strong style="color:#0f172a;">Porra App ya está disponible</strong>.
                            </p>

                            <p style="margin:0 0 16px; font-size:16px; line-height:24px; color:#475467;">
                                Ya puedes acceder a la aplicación y empezar a disfrutar de todas sus funcionalidades.
                            </p>

                            <p style="margin:0; font-size:16px; line-height:24px; color:#475467;">
                                Estos son tus datos de acceso:
                            </p>
                        </td>
                    </tr>

                    <!-- Datos de acceso -->
                    <tr>
                        <td class="px" align="center" style="padding:0 48px 32px;">
                            <table role="presentation" border="0" cellspacing="0" cellpadding="0"
                                   style="background-color:#f8fafc; border:1px solid #e4e7ec; border-radius:10px; width:100%;">
                                <tr>
                                    <td style="padding:24px 32px;">

                                        <p style="margin:0 0 8px; font-size:12px; letter-spacing:1.5px; text-transform:uppercase; color:#64748b; font-weight:600;">
                                            Nombre
                                        </p>
                                        <p style="margin:0 0 16px; font-size:18px; font-weight:600; color:#0f172a;">
                                            {nombre}
                                        </p>

                                        <p style="margin:0 0 8px; font-size:12px; letter-spacing:1.5px; text-transform:uppercase; color:#64748b; font-weight:600;">
                                            Usuario
                                        </p>
                                        <p style="margin:0 0 16px; font-size:18px; font-weight:600; color:#0f172a;">
                                            {usuario}
                                        </p>

                                        <p style="margin:0 0 8px; font-size:12px; letter-spacing:1.5px; text-transform:uppercase; color:#64748b; font-weight:600;">
                                            Código de tu liga
                                        </p>
                                        <p style="margin:0; font-family:'Courier New',Consolas,monospace; font-size:24px; letter-spacing:4px; font-weight:700; color:#0f172a;">
                                            {codigo}
                                        </p>

                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- CTA -->
                    <tr>
                        <td class="px" align="center" style="padding:0 48px 40px;">
                            <a href="{url_app}"
                               style="display:inline-block; background-color:#0f172a; color:#ffffff; text-decoration:none; padding:14px 28px; border-radius:8px; font-weight:600; font-size:16px;">
                                Acceder a Porra App
                            </a>
                        </td>
                    </tr>

                    <!-- Divider -->
                    <tr>
                        <td style="padding:0 48px;">
                            <hr style="border:none; border-top:1px solid #e4e7ec; margin:0;">
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td align="center" style="padding:24px 48px 32px;">
                            <p style="margin:0 0 8px; font-size:12px; line-height:18px; color:#98a2b3;">
                                Este es un correo automático. Por favor, no respondas a este mensaje.
                            </p>
                            <p style="margin:0; font-size:12px; line-height:18px; color:#98a2b3;">
                                &copy; 2026 Porra App. Todos los derechos reservados.
                            </p>
                        </td>
                    </tr>

                </table>

            </td>
        </tr>
    </table>

</body>
</html>
"""




ASUNTO_CORREO_RECORDATORIO_PORRA="⏰ Recuerda completar tu porra antes del 11/06/2026"
HTML_CORREO_RECORDATORIO_PORRA="""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="x-apple-disable-message-reformatting">
    <meta name="color-scheme" content="light">
    <meta name="supported-color-schemes" content="light">
    <title>Recordatorio Porra App</title>
    <style>
        @media only screen and (max-width: 620px) {{
            .container {{ width: 100% !important; }}
            .px {{ padding-left: 24px !important; padding-right: 24px !important; }}
            .h1 {{ font-size: 22px !important; line-height: 30px !important; }}
        }}
    </style>
</head>
<body style="margin:0; padding:0; background-color:#f2f4f7; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; -webkit-font-smoothing:antialiased;">

    <div style="display:none; max-height:0; overflow:hidden; opacity:0; visibility:hidden; mso-hide:all; font-size:1px; line-height:1px; color:#f2f4f7;">
        Todavía no has completado tu porra. Hazlo antes del 11 de junio.
    </div>

    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f2f4f7;">
        <tr>
            <td align="center" style="padding:32px 16px;">

                <table role="presentation" class="container" width="600" border="0" cellspacing="0" cellpadding="0"
                       style="width:600px; max-width:600px; background-color:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 4px 16px rgba(16,24,40,0.06);">

                    <!-- Header -->
                    <tr>
                        <td align="center" style="background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%); background-color:#0f172a; padding:36px 24px; color:#ffffff;">
                            <h1 style="margin:0; font-size:26px; line-height:32px; font-weight:700; letter-spacing:-0.5px; color:#ffffff;">
                                ⚽ Porra App
                            </h1>
                            <p style="margin:8px 0 0; font-size:14px; color:#cbd5e1;">
                                Tu liga de predicciones de fútbol
                            </p>
                        </td>
                    </tr>

                    <!-- Content -->
                    <tr>
                        <td class="px" style="padding:40px 48px 24px; color:#0f172a;">

                            <h2 class="h1" style="margin:0 0 16px; font-size:24px; line-height:32px; font-weight:600; color:#0f172a;">
                                ¡Hola, {nombre}! 👋
                            </h2>

                            <p style="margin:0 0 16px; font-size:16px; line-height:24px; color:#475467;">
                                Te recordamos que <strong style="color:#0f172a;">todavía no has completado tu porra</strong>.
                            </p>

                            <p style="margin:0 0 16px; font-size:16px; line-height:24px; color:#475467;">
                                Aún estás a tiempo de realizar tus predicciones y competir con el resto de participantes.
                            </p>

                            <p style="margin:0; font-size:16px; line-height:24px; color:#475467;">
                                Recuerda que una vez comience el evento, ya no será posible modificar ni enviar la porra.
                            </p>

                        </td>
                    </tr>

                    <!-- Fecha límite -->
                    <tr>
                        <td class="px" align="center" style="padding:0 48px 32px;">
                            <table role="presentation" border="0" cellspacing="0" cellpadding="0"
                                   style="background-color:#f8fafc; border:1px solid #e4e7ec; border-radius:10px; width:100%;">
                                <tr>
                                    <td style="padding:24px 32px; text-align:center;">

                                        <p style="margin:0 0 10px; font-size:12px; letter-spacing:1.5px; text-transform:uppercase; color:#64748b; font-weight:600;">
                                            Fecha límite
                                        </p>

                                        <p style="margin:0; font-size:26px; font-weight:700; color:#0f172a;">
                                            📅 11/06/2026
                                        </p>

                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- CTA -->
                    <tr>
                        <td class="px" align="center" style="padding:0 48px 40px;">
                            <a href="{url_app}"
                               style="display:inline-block; background-color:#0f172a; color:#ffffff; text-decoration:none; padding:14px 28px; border-radius:8px; font-weight:600; font-size:16px;">
                                Completar mi porra
                            </a>
                        </td>
                    </tr>

                    <!-- Divider -->
                    <tr>
                        <td style="padding:0 48px;">
                            <hr style="border:none; border-top:1px solid #e4e7ec; margin:0;">
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td align="center" style="padding:24px 48px 32px;">
                            <p style="margin:0 0 8px; font-size:12px; line-height:18px; color:#98a2b3;">
                                Este es un correo automático. Por favor, no respondas a este mensaje.
                            </p>

                            <p style="margin:0; font-size:12px; line-height:18px; color:#98a2b3;">
                                &copy; 2026 Porra App. Todos los derechos reservados.
                            </p>
                        </td>
                    </tr>

                </table>

            </td>
        </tr>
    </table>

</body>
</html>
"""



ASUNTO_CORREO_CIERRE_PORRA = "🏆 ¡Empieza el torneo! La porra ya está cerrada"
HTML_CORREO_CIERRE_PORRA="""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="x-apple-disable-message-reformatting">
    <meta name="color-scheme" content="light">
    <meta name="supported-color-schemes" content="light">
    <title>La porra ya está cerrada</title>
    <style>
        @media only screen and (max-width: 620px) {{
            .container {{ width: 100% !important; }}
            .px {{ padding-left: 24px !important; padding-right: 24px !important; }}
            .h1 {{ font-size: 22px !important; line-height: 30px !important; }}
        }}
    </style>
</head>
<body style="margin:0; padding:0; background-color:#f2f4f7; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; -webkit-font-smoothing:antialiased;">

    <div style="display:none; max-height:0; overflow:hidden; opacity:0; visibility:hidden; mso-hide:all; font-size:1px; line-height:1px; color:#f2f4f7;">
        La porra ya está cerrada. Ahora solo queda disfrutar del evento.
    </div>

    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f2f4f7;">
        <tr>
            <td align="center" style="padding:32px 16px;">

                <table role="presentation" class="container" width="600" border="0" cellspacing="0" cellpadding="0"
                       style="width:600px; max-width:600px; background-color:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 4px 16px rgba(16,24,40,0.06);">

                    <!-- Header -->
                    <tr>
                        <td align="center" style="background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%); background-color:#0f172a; padding:36px 24px; color:#ffffff;">
                            <h1 style="margin:0; font-size:26px; line-height:32px; font-weight:700; letter-spacing:-0.5px; color:#ffffff;">
                                ⚽ Porra App
                            </h1>
                            <p style="margin:8px 0 0; font-size:14px; color:#cbd5e1;">
                                Tu liga de predicciones de fútbol
                            </p>
                        </td>
                    </tr>

                    <!-- Content -->
                    <tr>
                        <td class="px" style="padding:40px 48px 24px; color:#0f172a;">

                            <h2 class="h1" style="margin:0 0 16px; font-size:24px; line-height:32px; font-weight:600; color:#0f172a;">
                                ¡Hola, {nombre}! 👋
                            </h2>

                            <p style="margin:0 0 16px; font-size:16px; line-height:24px; color:#475467;">
                                El plazo para completar y modificar las porras ya ha finalizado.
                            </p>

                            <p style="margin:0 0 16px; font-size:16px; line-height:24px; color:#475467;">
                                A partir de ahora, solo queda disfrutar del evento y seguir la clasificación para ver quién se convierte en el ganador de la liga.
                            </p>

                            <p style="margin:0; font-size:16px; line-height:24px; color:#475467;">
                                Gracias por formar parte de <strong style="color:#0f172a;">Porra App</strong>. ¡Mucha suerte! 🍀
                            </p>

                        </td>
                    </tr>

                    <!-- Caja destacada -->
                    <tr>
                        <td class="px" align="center" style="padding:0 48px 32px;">
                            <table role="presentation" border="0" cellspacing="0" cellpadding="0"
                                   style="background-color:#f8fafc; border:1px solid #e4e7ec; border-radius:10px; width:100%;">
                                <tr>
                                    <td style="padding:24px 32px; text-align:center;">

                                        <p style="margin:0 0 10px; font-size:12px; letter-spacing:1.5px; text-transform:uppercase; color:#64748b; font-weight:600;">
                                            Estado de la porra
                                        </p>

                                        <p style="margin:0; font-size:26px; font-weight:700; color:#0f172a;">
                                            ✅ Cerrada
                                        </p>

                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- CTA -->
                    <tr>
                        <td class="px" align="center" style="padding:0 48px 40px;">
                            <a href="{url_app}"
                               style="display:inline-block; background-color:#0f172a; color:#ffffff; text-decoration:none; padding:14px 28px; border-radius:8px; font-weight:600; font-size:16px;">
                                Ver clasificación
                            </a>
                        </td>
                    </tr>

                    <!-- Divider -->
                    <tr>
                        <td style="padding:0 48px;">
                            <hr style="border:none; border-top:1px solid #e4e7ec; margin:0;">
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td align="center" style="padding:24px 48px 32px;">
                            <p style="margin:0 0 8px; font-size:12px; line-height:18px; color:#98a2b3;">
                                Este es un correo automático. Por favor, no respondas a este mensaje.
                            </p>

                            <p style="margin:0; font-size:12px; line-height:18px; color:#98a2b3;">
                                &copy; 2026 Porra App. Todos los derechos reservados.
                            </p>
                        </td>
                    </tr>

                </table>

            </td>
        </tr>
    </table>

</body>
</html>
"""


ASUNTO_CORREO_INICIO_MUNDIAL = "🌍 ¡El Mundial ya ha comenzado! Sigue tu porra en directo"
HTML_CORREO_INICIO_MUNDIAL = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="x-apple-disable-message-reformatting">
    <meta name="color-scheme" content="light">
    <meta name="supported-color-schemes" content="light">
    <title>¡El Mundial ya ha comenzado!</title>
    <style>
        @media only screen and (max-width: 620px) {{
            .container {{ width: 100% !important; }}
            .px {{ padding-left: 24px !important; padding-right: 24px !important; }}
            .h1 {{ font-size: 22px !important; line-height: 30px !important; }}
        }}
    </style>
</head>
<body style="margin:0; padding:0; background-color:#f2f4f7; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; -webkit-font-smoothing:antialiased;">

    <div style="display:none; max-height:0; overflow:hidden; opacity:0; visibility:hidden; mso-hide:all; font-size:1px; line-height:1px; color:#f2f4f7;">
        El Mundial ya está en marcha. Sigue tu porra y consulta los resultados en directo.
    </div>

    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f2f4f7;">
        <tr>
            <td align="center" style="padding:32px 16px;">

                <table role="presentation" class="container" width="600" border="0" cellspacing="0" cellpadding="0"
                       style="width:600px; max-width:600px; background-color:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 4px 16px rgba(16,24,40,0.06);">

                    <!-- Header -->
                    <tr>
                        <td align="center" style="background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%); background-color:#0f172a; padding:36px 24px; color:#ffffff;">
                            <h1 style="margin:0; font-size:26px; line-height:32px; font-weight:700; letter-spacing:-0.5px; color:#ffffff;">
                                ⚽ Porra App
                            </h1>
                            <p style="margin:8px 0 0; font-size:14px; color:#cbd5e1;">
                                Tu liga de predicciones de fútbol
                            </p>
                        </td>
                    </tr>

                    <!-- Content -->
                    <tr>
                        <td class="px" style="padding:40px 48px 24px; color:#0f172a;">

                            <h2 class="h1" style="margin:0 0 16px; font-size:24px; line-height:32px; font-weight:600; color:#0f172a;">
                                ¡Hola, {nombre}! 👋
                            </h2>

                            <p style="margin:0 0 16px; font-size:16px; line-height:24px; color:#475467;">
                                ¡El Mundial ya ha comenzado! 🌍⚽
                            </p>

                            <p style="margin:0 0 16px; font-size:16px; line-height:24px; color:#475467;">
                                A partir de ahora podrás seguir la competición y comprobar cómo evolucionan las predicciones de tu liga.
                            </p>

                            <p style="margin:0 0 16px; font-size:16px; line-height:24px; color:#475467;">
                                En el apartado <strong style="color:#0f172a;">Clasificación</strong> se irán actualizando los puntos de todos los participantes conforme avancen los partidos.
                            </p>

                            <p style="margin:0 0 16px; font-size:16px; line-height:24px; color:#475467;">
                                Además, en el apartado <strong style="color:#0f172a;">Resultados</strong> podrás consultar en directo los grupos, los mejores terceros y las eliminatorias según vayan produciéndose.
                            </p>

                            <p style="margin:0; font-size:16px; line-height:24px; color:#475467;">
                                Gracias por formar parte de <strong style="color:#0f172a;">Porra App</strong>. ¡Mucha suerte! 🍀
                            </p>

                        </td>
                    </tr>

                    <!-- Caja destacada -->
                    <tr>
                        <td class="px" align="center" style="padding:0 48px 32px;">
                            <table role="presentation" border="0" cellspacing="0" cellpadding="0"
                                   style="background-color:#f8fafc; border:1px solid #e4e7ec; border-radius:10px; width:100%;">
                                <tr>
                                    <td style="padding:24px 32px; text-align:center;">

                                        <p style="margin:0 0 10px; font-size:12px; letter-spacing:1.5px; text-transform:uppercase; color:#64748b; font-weight:600;">
                                            Estado del torneo
                                        </p>

                                        <p style="margin:0; font-size:26px; font-weight:700; color:#0f172a;">
                                            🟢 En juego
                                        </p>

                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- CTA -->
                    <tr>
                        <td class="px" align="center" style="padding:0 48px 40px;">
                            <a href="{url_app}"
                               style="display:inline-block; background-color:#0f172a; color:#ffffff; text-decoration:none; padding:14px 28px; border-radius:8px; font-weight:600; font-size:16px;">
                                Seguir mi liga
                            </a>
                        </td>
                    </tr>

                    <!-- Divider -->
                    <tr>
                        <td style="padding:0 48px;">
                            <hr style="border:none; border-top:1px solid #e4e7ec; margin:0;">
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td align="center" style="padding:24px 48px 32px;">
                            <p style="margin:0 0 8px; font-size:12px; line-height:18px; color:#98a2b3;">
                                Este es un correo automático. Por favor, no respondas a este mensaje.
                            </p>

                            <p style="margin:0; font-size:12px; line-height:18px; color:#98a2b3;">
                                &copy; 2026 Porra App. Todos los derechos reservados.
                            </p>
                        </td>
                    </tr>

                </table>

            </td>
        </tr>
    </table>

</body>
</html>
"""


ASUNTO_CORREO_MITAD_GRUPOS = "⚽ Media fase de grupos completada. ¿Cómo va tu porra?"
HTML_CORREO_MITAD_GRUPOS = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="es">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="x-apple-disable-message-reformatting">
    <meta name="color-scheme" content="light">
    <meta name="supported-color-schemes" content="light">
    <title>Media fase de grupos completada</title>
    <style>
        @media only screen and (max-width: 620px) {{
            .container {{ width: 100% !important; }}
            .px {{ padding-left: 24px !important; padding-right: 24px !important; }}
            .h1 {{ font-size: 22px !important; line-height: 30px !important; }}
        }}
    </style>
</head>
<body style="margin:0; padding:0; background-color:#f2f4f7; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif; -webkit-font-smoothing:antialiased;">

    <div style="display:none; max-height:0; overflow:hidden; opacity:0; visibility:hidden; mso-hide:all; font-size:1px; line-height:1px; color:#f2f4f7;">
        Ya hemos llegado a la mitad de la fase de grupos. Consulta cómo va tu porra.
    </div>

    <table role="presentation" width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color:#f2f4f7;">
        <tr>
            <td align="center" style="padding:32px 16px;">

                <table role="presentation" class="container" width="600" border="0" cellspacing="0" cellpadding="0"
                       style="width:600px; max-width:600px; background-color:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 4px 16px rgba(16,24,40,0.06);">

                    <!-- Header -->
                    <tr>
                        <td align="center" style="background:linear-gradient(135deg,#0f172a 0%,#1e293b 100%); background-color:#0f172a; padding:36px 24px; color:#ffffff;">
                            <h1 style="margin:0; font-size:26px; line-height:32px; font-weight:700; letter-spacing:-0.5px; color:#ffffff;">
                                ⚽ Porra App
                            </h1>
                            <p style="margin:8px 0 0; font-size:14px; color:#cbd5e1;">
                                Tu liga de predicciones de fútbol
                            </p>
                        </td>
                    </tr>

                    <!-- Content -->
                    <tr>
                        <td class="px" style="padding:40px 48px 24px; color:#0f172a;">

                            <h2 class="h1" style="margin:0 0 16px; font-size:24px; line-height:32px; font-weight:600; color:#0f172a;">
                                ¡Hola, {nombre}! 👋
                            </h2>

                            <p style="margin:0 0 16px; font-size:16px; line-height:24px; color:#475467;">
                                ¡Ya hemos alcanzado la mitad de la fase de grupos! 📊⚽
                            </p>

                            <p style="margin:0 0 16px; font-size:16px; line-height:24px; color:#475467;">
                                Todavía queda mucho torneo por delante, pero las primeras diferencias entre los participantes de la liga ya empiezan a aparecer.
                            </p>

                            <p style="margin:0 0 16px; font-size:16px; line-height:24px; color:#475467;">
                                En el apartado <strong style="color:#0f172a;">Clasificación</strong> puedes consultar los puntos actualizados y ver quién lidera actualmente tu liga.
                            </p>

                            <p style="margin:0 0 16px; font-size:16px; line-height:24px; color:#475467;">
                                Además, en el apartado <strong style="color:#0f172a;">Resultados</strong> puedes seguir la evolución de los grupos y comprobar cómo van cambiando las posiciones según se disputan los partidos.
                            </p>

                            <p style="margin:0; font-size:16px; line-height:24px; color:#475467;">
                                ¡Aún queda mucho por decidir y todo puede cambiar! 🍀
                            </p>

                        </td>
                    </tr>

                    <!-- Caja destacada -->
                    <tr>
                        <td class="px" align="center" style="padding:0 48px 32px;">
                            <table role="presentation" border="0" cellspacing="0" cellpadding="0"
                                   style="background-color:#f8fafc; border:1px solid #e4e7ec; border-radius:10px; width:100%;">
                                <tr>
                                    <td style="padding:24px 32px; text-align:center;">

                                        <p style="margin:0 0 10px; font-size:12px; letter-spacing:1.5px; text-transform:uppercase; color:#64748b; font-weight:600;">
                                            Estado del torneo
                                        </p>

                                        <p style="margin:0; font-size:26px; font-weight:700; color:#0f172a;">
                                            📊 Mitad de la fase de grupos
                                        </p>

                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>

                    <!-- CTA -->
                    <tr>
                        <td class="px" align="center" style="padding:0 48px 40px;">
                            <a href="{url_app}"
                               style="display:inline-block; background-color:#0f172a; color:#ffffff; text-decoration:none; padding:14px 28px; border-radius:8px; font-weight:600; font-size:16px;">
                                Seguir mi liga
                            </a>
                        </td>
                    </tr>

                    <!-- Divider -->
                    <tr>
                        <td style="padding:0 48px;">
                            <hr style="border:none; border-top:1px solid #e4e7ec; margin:0;">
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td align="center" style="padding:24px 48px 32px;">
                            <p style="margin:0 0 8px; font-size:12px; line-height:18px; color:#98a2b3;">
                                Este es un correo automático. Por favor, no respondas a este mensaje.
                            </p>

                            <p style="margin:0; font-size:12px; line-height:18px; color:#98a2b3;">
                                &copy; 2026 Porra App. Todos los derechos reservados.
                            </p>
                        </td>
                    </tr>

                </table>

            </td>
        </tr>
    </table>

</body>
</html>
"""