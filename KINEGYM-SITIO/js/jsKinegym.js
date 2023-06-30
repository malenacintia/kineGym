let cad = `
<div class="banner">
<img src="img/banner.jpg">
</div> 
`;

if (document.getElementById("headerjs")) {

    document.getElementById("headerjs").innerHTML = cad;
}

cad = `
<div class="redes">
<p>Seguinos en nuestras redes sociales</p>
<a href="https://www.instagram.com/"><i class="fa-brands fa-instagram"></i></a>
<a href="mailto:malenacintia@.com"><i class="fa-regular fa-envelope"></i></a>
</div>
<div class="logo">
<i class="fa-solid fa-dumbbell"></i>
</div>
<p>2023 KineGym</p>
<div class="menu">
<nav class="navegacion" id="navFoot">
    <ul>
        <a href="index.html"><i class="fa-solid fa-house"></i>
            Inicio</a>

        <a href="index.html#servicios"><i class="fa-solid fa-magnifying-glass-plus"></i>
            Servicios</a>

        <a href="index.html#acercaDe"><i class="fa-solid fa-people-line"></i>
            Sobre nosotros</a>

        <a class="active" href="kinegymContacto.html"><i class="fa-solid fa-comment-dots"></i>
            Contacto</a>
    </ul>
</nav>
</div>
`

if (document.getElementById("footerjs")) {

    document.getElementById("footerjs").innerHTML = cad;
}


//VALIDAR FORMULARIO

if (document.getElementById("formulario")) {

    var formulario = document.getElementsByName('formulario')[0];
    elementos = formulario.elements,
        boton = document.getElementById('b1');

    var validarNombre = function(e) {
        if (formulario.nombre.value == 0) {
            alert("Completa el campo nombre.");
            e.preventDefault();
        }
    }

    var validarTel = function(e) {
        if (formulario.tel.value == 0) {
            alert("Completá tu número de teléfono.");
            e.preventDefault();
        }
    }

    var validarCheckbox = function(e) {
        if (formulario.opcion[0].checked == true ||
            formulario.opcion[1].checked == true ||
            formulario.opcion[2].checked == true ||
            formulario.opcion[3].checked == true ||
            formulario.opcion[4].checked == true) {} else {
            alert("Selecciona al menos una opción.")
            e.preventDefault()
        }
    }

    var validarEnviar = function(e) {
        validarNombre(e);
        validarTel(e);
        validarCheckbox(e);
        e.preventDefault()
    }

    formulario.addEventListener("submit", validarEnviar)

    //creo que el erro esta en el if siguiente y luego debo trasladarlo al formspree
    document.getElementById("b1").addEventListener("click", function() {
        if (validarEnviar.ok) {
            console.log("Se envió el mensaje")
            document.getElementById("chequeo").innerHTML = "¡Se envió tu mensaje!";
        }
    });

    document.getElementById("boton_reset").addEventListener("click", function() {
        document.getElementById("chequeo").innerHTML = `Tu mensaje se enviará cuando pulses "Enviar"`
        console.log("Se reinició el formulario");
    });

    //INTENTO API FORMSPREE
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

}

//APIREST CITAS ESTOICAS
var mostrar = document.querySelector('#mostrar')

function traer() {
    fetch('https://api.themotivate365.com/stoic-quote')
        .then(res => res.json())
        .then(json => {
            console.log(json)
            document.getElementById("mostrar").innerHTML = `
                    <div class="apirest">
                    <h3>Autor: ${json.author}</h3>
                    <p>"${json.quote}"</p>
                    </div>
                    `

        })
        .catch(error => console.log("Ocurrió un error", error))
}