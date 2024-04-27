# Portal Swagger

Bienvenido a Portal Swagger, una API de backend diseñada para ser consumida tanto por un módulo en Odoo (webhook) como por un portal web cliente. Este backend gestiona tres tipos de usuarios: clientes, asesores y administradores. Los administradores tienen la autoridad para crear cualquier tipo de usuario, mientras que los asesores solo pueden registrar clientes y los clientes solo pueden consumir datos. Todos los usuarios tienen la capacidad de cambiar sus contraseñas. El registro de clientes se valida con Odoo antes de registrarse. Los datos de clientes devueltos se obtienen de Odoo.

## URL Base
La URL base para acceder a la API es `http://localhost:5000/api`.

## Autenticación
Todos los endpoints requieren autenticación utilizando JWT (Tokens Web JSON). El token debe incluirse en el encabezado `Authorization` de la solicitud.

## Endpoints

### Endpoints de Autenticación

#### Autenticación de Administrador

- **Iniciar sesión de Administrador:** `POST /auth/admin/login`
  - Permite a un administrador iniciar sesión proporcionando correo electrónico y contraseña.
  - Cuerpo de la Solicitud: `LoginAdminBody`
  - Respuesta: `LoginAdminResponse`

- **Registrar Administrador:** `POST /auth/admin/register`
  - Permite a un administrador registrar un nuevo usuario administrador.
  - Cuerpo de la Solicitud: `RegisterAdminBody`
  - Respuesta: `RegisterAdminResponse`

#### Autenticación de Asesor

- **Iniciar sesión de Asesor:** `POST /auth/manager/login`
  - Permite a un asesor iniciar sesión proporcionando correo electrónico y contraseña.
  - Cuerpo de la Solicitud: `LoginManagerBody`
  - Respuesta: `LoginManagerResponse`

- **Registrar Asesor:** `POST /auth/manager/register`
  - Permite a un administrador registrar un nuevo usuario asesor.
  - Cuerpo de la Solicitud: `RegisterManagerBody`
  - Respuesta: `RegisterManagerResponse`

#### Autenticación de Cliente

- **Iniciar sesión de Cliente:** `POST /auth/client/login`
  - Permite a un cliente iniciar sesión proporcionando el número de documento y contraseña.
  - Cuerpo de la Solicitud: `LoginClientBody`
  - Respuesta: `LoginClientResponse`

- **Registrar Cliente:** `POST /auth/client/register`
  - Permite a un administrador o asesor registrar un nuevo usuario cliente.
  - Cuerpo de la Solicitud: `RegisterClientBody`
  - Respuesta: `RegisterClientResponse`

### Endpoints de Cliente

- **Obtener Suscripciones de Socio:** `GET /partner_subscription`
  - Obtiene las suscripciones de socio para un cliente.
  - Respuesta: Lista de objetos de suscripción.

- **Obtener Factura de Socio:** `GET /partner_bill/{subscription_id}`
  - Obtiene detalles de la factura de socio para una suscripción específica.
  - Parámetro de Ruta: `subscription_id`
  - Respuesta: Objeto de detalles de la factura.

### Endpoints de Asesor

- **Obtener Clientes:** `GET /clients`
  - Obtiene una lista de clientes.
  - Respuesta: Lista de objetos de cliente.

### Endpoints de Administrador

- **Obtener Asesores:** `GET /managers`
  - Obtiene una lista de asesores.
  - Respuesta: Lista de objetos de asesor.

- **Obtener Administradores:** `GET /admins`
  - Obtiene una lista de administradores.
  - Respuesta: Lista de objetos de administrador.

### Cambiar Contraseña

- **Cambiar Contraseña:** `PUT /auth/change_password`
  - Permite a los usuarios cambiar su contraseña.
  - Cuerpo de la Solicitud: `ChangePasswordBody`
  - Respuesta: Mensaje indicando el cambio de contraseña exitoso.

Estos endpoints facilitan la autenticación de usuarios, el registro y la recuperación de datos según sus respectivos roles.