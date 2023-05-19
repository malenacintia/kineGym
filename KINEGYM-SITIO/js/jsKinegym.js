let cad = `
<div class="banner">
<img src="img/banner.jpg">
</div> 
`

document.getElementById("headerjs").innerHTML = cad;

cad = `
<div class="redes">
<p>Seguinos en nuestras redes sociales</p>
<a href="#"><i class="fa-brands fa-instagram"></i></a>
<a href="#"><i class="fa-regular fa-envelope"></i></a>
</div>
<div class="logo">
<i class="fa-solid fa-dumbbell"></i>
</div>
<p>2023 KineGym</p>
<div class="menu">
<nav class="navegacion" id="navFoot">
    <ul>
        <a href="kinegymInicio.html"><i class="fa-solid fa-house"></i>
            Inicio</a>

        <a href="kinegymInicio.html#servicios"><i class="fa-solid fa-magnifying-glass-plus"></i>
            Servicios</a>

        <a href="kinegymInicio.html#acercaDe"><i class="fa-solid fa-people-line"></i>
            Sobre nosotros</a>

        <a class="active" href="kinegymContacto.html"><i class="fa-solid fa-comment-dots"></i>
            Contacto</a>
    </ul>
</nav>
</div>
`
document.getElementById("footerjs").innerHTML = cad;


//VALIDAR FORMULARIO

var formulario = document.getElementsByName('formulario')[0];
elementos = formulario.elements,
    boton = document.getElementById('b1');

var validarNombre = function (e) {
    if (formulario.nombre.value == 0) {
        alert("Completa el campo nombre.");
        e.preventDefault();
    }
}

var validarTel = function (e) {
    if (formulario.tel.value == 0) {
        alert("Completá tu número de teléfono.");
        e.preventDefault();
    }
}

var validarCheckbox = function (e) {
    if (formulario.opcion[0].checked == true ||
        formulario.opcion[1].checked == true ||
        formulario.opcion[2].checked == true ||
        formulario.opcion[3].checked == true ||
        formulario.opcion[4].checked == true) {
    } else {
        alert("Selecciona al menos una opción.")
        e.preventDefault()
    }
}
var validarEnviar = function (e) {
    validarNombre(e);
    validarTel(e);
    validarCheckbox(e);
}

formulario.addEventListener("submit", validarEnviar)

 document.getElementById("b1").addEventListener("click", function () {
    if (validarEnviar !== alert) {
        console.log("Se envió el mensaje")
        document.getElementById("chequeo").innerHTML = "¡Se envió tu mensaje!";
    }
}); 

document.getElementById("boton_reset").addEventListener("click", function () {
    document.getElementById("chequeo").innerHTML = `Tu mensaje se enviará cuando pulses "Enviar"`
    console.log("Se reinició el formulario");
}); 

//INTENTO FORMSPREE
const form = document.querySelector("#formulario")

form.addEventListener(`submit`, handlesubmit)

async function handlesubmit(event) {
    event.preventDefault()
    const form = new FormData(this)
    const response = await fetch(this.action, {
        method: this.method,
        body: form,
        headers: {
            "Accept": "application/json"
        }
    })
    if (response.ok) {
        this.reset()
        alert("Gracias por contactarnos, nos comunicaremos pronto.")
    }
}


//APIREST CITAS
 var mostrar = document.querySelector('#mostrar')

function traer() {
    fetch('https://api.themotivate365.com/stoic-quote')
        .then(res => res.json())
        .then(json => {
            console.log(json)
            document.getElementById("mostrar").innerHTML = `
                    <div style="background-color:grey" width="auto" heigth="40px">
                    <h3>Nombre: ${json.author}</h3>
                    <p>Mail: ${json.quote}</p>
                    </div>
                    `
        })
        .catch(error => console.log("Ocurrió un error", error)) 
}




