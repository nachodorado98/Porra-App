import os

EMAIL_ACCOUNT=os.environ.get("EMAIL_ACCOUNT")
CONTRASENA_LOGIN=os.environ.get("CONTRASENA_LOGIN")
SERVIDOR_CORREO=os.environ.get("SERVIDOR_CORREO")
PUERTO_CORREO=int(os.environ.get("PUERTO_CORREO"))
ASUNTO_CORREO="¡Bienvenido a nuestra familia!"
HTML_CORREO="""
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