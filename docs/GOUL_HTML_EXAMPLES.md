# 🌐 Ejemplos HTML en Goul

## Introducción

Con Goul, ahora puedes crear contenido HTML y visualizarlo en el navegador Pixel Browser. Esta guía te muestra cómo crear páginas web simples usando Goul.

---

## Ejemplo 1: Página Simple

```goul
// archivo: pagina_simple.goul
var html = html("<h1>Mi Primer Sitio Web</h1><p>Creado con Goul</p>");
```

Visualiza el resultado en Pixel Browser.

---

## Ejemplo 2: Página con Estilos

```goul
// archivo: pagina_estirada.goul

var titulo = tag("h1", "Bienvenido", {"class": "titulo"});
var subtitulo = tag("h2", "Mi sitio personal", {"class": "subtitulo"});
var parrafo = tag("p", "Este es mi primer párrafo en una página web hecha con Goul");

var contenido = titulo + subtitulo + parrafo;

// Crear estilos
var h1_style = "h1 { color: blue; text-align: center; margin: 20px; }";
var h2_style = "h2 { color: purple; font-size: 18px; }";
var p_style = "p { color: #333; font-family: Arial, sans-serif; line-height: 1.6; }";

var css_completo = "<style>" + h1_style + h2_style + p_style + "</style>";

var pagina_final = css_completo + contenido;
var resultado = html(pagina_final);
```

---

## Ejemplo 3: Página con Lista

```goul
// archivo: lista_tareas.goul

var titulo = tag("h1", "📋 Mi Lista de Tareas");

var tarea1 = tag("li", "Aprender Goul", {"style": "color: green;"});
var tarea2 = tag("li", "Crear una página web");
var tarea3 = tag("li", "Maestría en Pixel-OS");

var lista = tag("ul", tarea1 + tarea2 + tarea3);

var pagina = titulo + lista;
var resultado = html(pagina);
```

---

## Ejemplo 4: Tarjeta de Perfil

```goul
// archivo: perfil.goul

// Estilos
var styles = "<style>
    body { 
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', sans-serif;
        margin: 0;
        padding: 20px;
    }
    .card {
        background: white;
        border-radius: 10px;
        padding: 30px;
        max-width: 400px;
        margin: 0 auto;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .card h2 {
        color: #333;
        margin-top: 0;
    }
    .info {
        color: #666;
        margin: 10px 0;
    }
    .avatar {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: #667eea;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 40px;
        margin-bottom: 20px;
    }
</style>";

// Contenido
var avatar = "<div class='avatar'>👨‍💻</div>";
var nombre = tag("h2", "Carlos Developer");
var email = tag("p", "📧 Email: carlos@pixel-os.local", {"class": "info"});
var ubicacion = tag("p", "📍 Ubicación: Madrid, España", {"class": "info"});
var bio = tag("p", "Desarrollador apasionado por crear software increíble", {"class": "info"});

var card = "<div class='card'>" + avatar + nombre + email + ubicacion + bio + "</div>";

var pagina = styles + card;
var resultado = html(pagina);
```

---

## Ejemplo 5: Tabla de Datos

```goul
// archivo: tabla_empleados.goul

var styles = "<style>
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 20px 0;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 12px;
        text-align: left;
    }
    th {
        background-color: #4CAF50;
        color: white;
    }
    tr:hover {
        background-color: #f5f5f5;
    }
</style>";

var titulo = tag("h1", "📊 Tabla de Empleados");

// Encabezados
var thead = "<thead><tr><th>Nombre</th><th>Puesto</th><th>Departamento</th><th>Salario</th></tr></thead>";

// Filas
var fila1 = "<tr><td>Ana García</td><td>Ingeniera</td><td>Tech</td><td>$60,000</td></tr>";
var fila2 = "<tr><td>Marco López</td><td>Diseñador</td><td>Diseño</td><td>$50,000</td></tr>";
var fila3 = "<tr><td>Sofia Chen</td><td>Gerente</td><td>Admin</td><td>$70,000</td></tr>";

var tabla = "<table>" + thead + fila1 + fila2 + fila3 + "</table>";

var pagina = styles + titulo + tabla;
var resultado = html(pagina);
```

---

## Ejemplo 6: Formulario Interactivo

```goul
// archivo: formulario.goul

var styles = "<style>
    form {
        max-width: 500px;
        margin: 20px auto;
        background: #f9f9f9;
        padding: 20px;
        border-radius: 8px;
    }
    label {
        display: block;
        margin-top: 10px;
        font-weight: bold;
    }
    input, textarea, select {
        width: 100%;
        padding: 8px;
        margin-top: 5px;
        border: 1px solid #ddd;
        border-radius: 4px;
        box-sizing: border-box;
    }
    button {
        background: #4CAF50;
        color: white;
        padding: 10px 20px;
        margin-top: 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
    }
    button:hover {
        background: #45a049;
    }
</style>";

var titulo = tag("h1", "Formulario de Contacto");

var form = "<form>
    <label>Nombre:</label>
    <input type='text' placeholder='Tu nombre' />
    
    <label>Email:</label>
    <input type='email' placeholder='tu@ejemplo.com' />
    
    <label>Asunto:</label>
    <select>
        <option>Consulta</option>
        <option>Soporte</option>
        <option>Sugerencia</option>
    </select>
    
    <label>Mensaje:</label>
    <textarea rows='5' placeholder='Escribe tu mensaje aquí...'></textarea>
    
    <button>Enviar</button>
</form>";

var pagina = styles + titulo + form;
var resultado = html(pagina);
```

---

## Ejemplo 7: Dashboard de Ventas

```goul
// archivo: dashboard.goul

var styles = "<style>
    body {
        background: #f5f5f5;
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 20px;
    }
    .dashboard {
        max-width: 1200px;
        margin: 0 auto;
    }
    .card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .metric {
        display: inline-block;
        width: 23%;
        margin-right: 2%;
        text-align: center;
    }
    .number {
        font-size: 32px;
        font-weight: bold;
        color: #4CAF50;
    }
    .label {
        color: #666;
        margin-top: 10px;
    }
</style>";

var titulo = tag("h1", "💼 Dashboard de Ventas");

var metrica1 = "<div class='metric'><div class='number'>$45,230</div><div class='label'>Ventas Totales</div></div>";
var metrica2 = "<div class='metric'><div class='number'>128</div><div class='label'>Clientes</div></div>";
var metrica3 = "<div class='metric'><div class='number'>92%</div><div class='label'>Satisfacción</div></div>";
var metrica4 = "<div class='metric'><div class='number'>$3,502</div><div class='label'>Promedio por Venta</div></div>";

var metricas = "<div class='card'>" + metrica1 + metrica2 + metrica3 + metrica4 + "</div>";

var info = "<div class='card'><p>📈 Incremento de ventas: +15% este mes<br/>⭐ Evaluación: 4.8/5<br/>✅ Metas alcanzadas: 95%</p></div>";

var pagina = styles + titulo + metricas + info;
var resultado = html(pagina);
```

---

## Ejemplo 8: Página de Blog

```goul
// archivo: blog.goul

var styles = "<style>
    body {
        background: #fff;
        font-family: Georgia, serif;
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    .post {
        border-bottom: 1px solid #eee;
        padding: 20px 0;
    }
    .post h2 {
        color: #333;
        margin-bottom: 10px;
    }
    .meta {
        color: #999;
        font-size: 14px;
    }
    .content {
        color: #666;
        line-height: 1.8;
    }
</style>";

var titulo = tag("h1", "📝 Mi Blog");

var post1_titulo = tag("h2", "Mi Viaje a Goul");
var post1_meta = tag("p", "Publicado: 5 de Febrero de 2026", {"class": "meta"});
var post1_content = tag("p", "Hoy comencé mi jornada aprendiendo el lenguaje de programación Goul. Es increíble cómo puedo crear aplicaciones complejas...", {"class": "content"});
var post1 = "<div class='post'>" + post1_titulo + post1_meta + post1_content + "</div>";

var post2_titulo = tag("h2", "Creando Webs con Goul");
var post2_meta = tag("p", "Publicado: 3 de Febrero de 2026", {"class": "meta"});
var post2_content = tag("p", "Uno de los features más interesantes de Goul es su capacidad de generar HTML. Veamos cómo funcionan las funciones tag() y css()...", {"class": "content"});
var post2 = "<div class='post'>" + post2_titulo + post2_meta + post2_content + "</div>";

var pagina = styles + titulo + post1 + post2;
var resultado = html(pagina);
```

---

## Ejemplo 9: Tabla de Precios

```goul
// archivo: precios.goul

var styles = "<style>
    body {
        background: #f5f7fa;
        font-family: 'Segoe UI', sans-serif;
        padding: 40px 20px;
    }
    .pricing {
        display: flex;
        gap: 20px;
        max-width: 1200px;
        margin: 0 auto;
    }
    .card {
        background: white;
        border-radius: 8px;
        padding: 30px;
        flex: 1;
        text-align: center;
        border: 2px solid #ddd;
    }
    .card.featured {
        border-color: #4CAF50;
        transform: scale(1.05);
    }
    .price {
        font-size: 48px;
        color: #4CAF50;
        margin: 20px 0;
    }
    .list {
        text-align: left;
        color: #666;
    }
    button {
        background: #4CAF50;
        color: white;
        padding: 10px 30px;
        border: none;
        border-radius: 4px;
        margin-top: 20px;
        cursor: pointer;
    }
</style>";

var titulo = tag("h1", "Planes de Precios");

var basic = "<div class='card'><h3>Basic</h3><div class='price'>$9</div><div class='list'><p>✓ 5 Proyectos<br/>✓ 1 GB almacenamiento<br/>✓ Email soporte</p></div><button>Comenzar</button></div>";

var pro = "<div class='card featured'><h3>Pro</h3><div class='price'>$29</div><div class='list'><p>✓ Proyectos ilimitados<br/>✓ 100 GB almacenamiento<br/>✓ Soporte prioritario</p></div><button>Comenzar</button></div>";

var enterprise = "<div class='card'><h3>Enterprise</h3><div class='price'>$99</div><div class='list'><p>✓ Todo en Pro<br/>✓ Almacenamiento ilimitado<br/>✓ Asistente dedicado</p></div><button>Contactar</button></div>";

var pricing = "<div class='pricing'>" + basic + pro + enterprise + "</div>";

var pagina = styles + titulo + pricing;
var resultado = html(pagina);
```

---

## Cómo Usar Estos Ejemplos

### Paso 1: Copiar el código
Copia cualquiera de los ejemplos anteriores

### Paso 2: Guardar en Code Editor
1. Abre **Code Editor** desde el desktop
2. Pega el código
3. Presiona **Ctrl+S** y guarda como `nombre.goul`

### Paso 3: Ejecutar
1. Presiona **F5** para ejecutar
2. El HTML aparecerá en el Output

### Paso 4: Ver en el Navegador
1. Guarda el HTML como archivo `.html` en Documentos
2. Abre **Pixel Browser**
3. Carga el archivo

---

## Tips para Crear Mejores Páginas

### 1. Mantén el HTML Limpio
```goul
// ✅ Bueno
var titulo = tag("h1", "Bienvenido");
var subtitulo = tag("h2", "Mi sitio");

// ❌ Evitar
var html_largo = "<h1>Bienvenido</h1><h2>Mi sitio</h2>";
```

### 2. Usa Variables para Estilos Reutilizables
```goul
var color_primario = "#4CAF50";
var estilo_boton = "background: " + color_primario + "; color: white; padding: 10px;";
```

### 3. Crea Funciones Helper
```goul
function crear_boton(texto, url) {
    return "<a href='" + url + "' style='background: #4CAF50; color: white; padding: 10px; text-decoration: none;'>" + texto + "</a>";
}

var boton1 = crear_boton("Inicio", "/");
var boton2 = crear_boton("Contacto", "/contacto");
```

---

## Próximo Paso

Ahora que conoces cómo crear HTML con Goul:
1. Experimenta combinando ejemplos
2. Crea tu propia página
3. Explora la documentación completa: [GOUL_COMPLETE_GUIDE.md](GOUL_COMPLETE_GUIDE.md)

¡Feliz creación de webs! 🌐✨
