
function getCSRFToken() {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  return csrfToken;
}


var bandera=false

let intervalId;

let finalDateKey = `finalDate_${articuloId}`;

let finalDate = localStorage.getItem(finalDateKey)

    ? new Date(localStorage.getItem(finalDateKey))
    : new Date(FINAL);
   
document.getElementById('resetear').addEventListener('click', () => {
  clearInterval(intervalId)



    // Sumar 24 horas (24 horas * 60 minutos * 60 segundos * 1000 milisegundos)
    finalDate = new Date(new Date().getTime() +  10 * 1000);
   
    localStorage.setItem(finalDateKey, finalDate.toISOString()); // Guardar en LocalStorage
    
    
   
    intervalId = setInterval(restar, 1000); // Reinicia el intervalo
    
})


function segundosaCronometro(seg) {
    var horas  = Math.floor(seg / 3600); // División entera para obtener las horas
    var minutos = Math.floor((seg % 3600) / 60); // Los minutos restantes
    var segundos = Math.floor(seg % 60); // El resto son los segundos restantes

    return { horas, minutos, segundos };

}

function formatoCronometro(horas, minutos, segundos) {
    // Construir el formato de tiempo
    const tiempo = `${String(horas).padStart(2, '0')}:${String(minutos).padStart(2, '0')}:${String(segundos).padStart(2, '0')}`;
    
    // Actualizar el contenido del cronómetro en el HTML
    document.getElementById("cronometro").innerHTML = tiempo; // Aquí actualizamos el div con id "cronometro"
}

function restar() {
    
    
    seg = Math.floor((finalDate - new Date()) / 1000);
    console.log(seg);
        
    if(seg>0){
        
        const { horas, minutos, segundos } = segundosaCronometro(seg); 
        formatoCronometro(horas, minutos, segundos);
    }
    else {

        console.log("el primooo")
        document.getElementById("cronometro").innerHTML = "00:00:00"; // Mostrar 00:00:00 al finalizar
        clearInterval(intervalId); // Detener el intervalo cuando se termine el tiempo
        localStorage.removeItem("finalDate"); // Limpiar finalDate al terminar
        
    }
    
    if (seg == 1 && !bandera) {
      fetch('/endBid/', {
        method: 'POST',  // Usamos POST para enviar datos
        headers: {
          'Content-Type': 'application/json',  // Indicamos que vamos a enviar datos en formato JSON
          'X-CSRFToken': getCSRFToken()  // Asegúrate de incluir el token CSRF (Django lo requiere para solicitudes POST)
        },
        body: JSON.stringify({articuloId: articuloId})
        
      })
      .then(response => response.json())  // Espera la respuesta en formato JSON
      .then(data => {
        console.log('Success:', data);  // Muestra los datos de respuesta si todo salió bien
      })
      .catch((error) => {
        console.error('Error:', error);  // Muestra errores si ocurren
        
      });

      bandera = true
    }}
    


        
    
intervalId = setInterval(restar, (1000)); // invoca la funcion restar cada 1000 ms








