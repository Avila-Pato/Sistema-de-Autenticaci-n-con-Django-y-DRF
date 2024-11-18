

Este repositorio contiene un sistema de autenticación robusto basado en Django y Django Rest Framework (DRF). Incluye la funcionalidad de registro, inicio de sesión, verificación de correo electrónico, y la creación de contraseñas, junto con un sistema de selección de ganador y envío de correos. Este sistema es ideal para proyectos que requieren características avanzadas de autenticación de usuarios y gestión de seguridad.

## Características Principales

### 1. **Registro de Usuarios**
- **Clase `RegisterSerializer`**: Se encarga de serializar y validar los datos de registro, como `username`, `email` y `password`. Verifica que el nombre de usuario y el correo electrónico no estén ya registrados.
- **Vista `register`**: Permite a los nuevos usuarios registrarse. Envía un correo de verificación con un enlace único para activar la cuenta.

### 2. **Verificación de Correo Electrónico**
- **Clase `VerifyEmailSerializer`**: Maneja la validación de los tokens y `uid` usados en el proceso de verificación.
- **Vista `verify_email`**: Decodifica el `uid` y verifica la validez del token. Activa la cuenta si la verificación es exitosa.

### 3. **Creación de Contraseñas**
- **Clase `CreatePasswordSerializer`**: Permite a los usuarios crear una nueva contraseña tras la activación de la cuenta.
- **Vista `create_password`**: Verifica si el usuario está activo y permite establecer una nueva contraseña.

### 4. **Inicio de Sesión**
- **Clase `LoginSerializer`**: Maneja la validación de las credenciales de usuario.
- **Vista `login`**: Verifica las credenciales ingresadas y autentica al usuario, asegurándose de que la cuenta esté activa.

### 5. **Envío de Correos**
- **Función `enviar_correo`**: Envía correos electrónicos de prueba o notificaciones específicas.
- **Uso de `send_mail`**: Se utiliza para enviar correos electrónicos con mensajes personalizados.

### 6. **Generación de Ganadores Aleatorios**
- **Vista `generate_winner`**: Selecciona aleatoriamente un usuario activo como ganador y le envía un correo de notificación.

## Seguridad y Configuración
- El proyecto incluye configuraciones de CORS y la implementación de autenticación JWT a través de `rest_framework_simplejwt`.
- Se utilizan validaciones específicas para proteger contra registros duplicados y verificar la integridad de las contraseñas.
- **CORS**: Permite solicitudes de dominios específicos como `localhost:3000`, ideal para el desarrollo de frontend separado.

## Configuraciones de Email
- **SMTP**: Configurado para enviar correos electrónicos usando un servidor SMTP.
- **Variables de Entorno**: Se recomienda configurar `EMAIL_HOST_USER` y `EMAIL_HOST_PASSWORD` con credenciales seguras en un archivo de entorno (.env).

## Instalación y Configuración
1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/usuario/nombre-repositorio.git
