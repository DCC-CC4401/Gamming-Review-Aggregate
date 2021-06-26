// Funciones que cambian el css cuando un nombre de usuario ya existe -------------------------
// Caso 1 - Nombre de usuario ya usado
function username_used(){
	var name_input = document.getElementById("new-user");			// El input
	var name_input_msj = document.getElementById("new-user-msj");	// El msj de error
	var boton = document.getElementById("create-boton");			// El botón de envío

	// Cambiamos la clase css del mensaje a rojo, el input a rojo, y deshabilitamos el boton
	name_input_msj.setAttribute("class", "leyenda-red");
	name_input.setAttribute("class", "check-input");
	boton.setAttribute("disabled", "true");
}

// Caso 2 - Nombre de usuario es válido
function username_not_used(){
	var name_input = document.getElementById("new-user");			// El input
	var name_input_msj = document.getElementById("new-user-msj");	// El msj de error

	// Cambiamos la clase css del mensaje a nulo, el input normal, y habilitamos el boton
	name_input_msj.setAttribute("class", "leyenda-none");
	name_input.setAttribute("class", "");
}

// Funciones que cambian el css cuando no se ha ingresado una contraseña válida --------------------
// Caso 1 - Password inválido
function invalid_password(){
	var psw_input = document.getElementById("new-passw1");			// El input
	var psw_input_msj = document.getElementById("new-passw1-msj");	// El msj de error
	var boton = document.getElementById("create-boton");			// El botón de envío

	// Cambiamos la clase css del mensaje a rojo, el input a rojo, y deshabilitamos el boton
	psw_input_msj.setAttribute("class", "leyenda-red");
	psw_input.setAttribute("class", "check-input");
	boton.setAttribute("disabled", "true");
}

// Caso 2 - Password válido
function valid_password(){
	var psw_input = document.getElementById("new-passw1");			// El input
	var psw_input_msj = document.getElementById("new-passw1-msj");	// El botón de envío

	// Cambiamos la clase css del mensaje a nulo, el input normal, y habilitamos el boton
	psw_input_msj.setAttribute("class", "leyenda-none");
	psw_input.setAttribute("class", "");
}


// Funciones que cambian el css cuando la segunda contraseña no es igual a la primera -----------
// Caso 1 - Password inválido
function both_invalid_passwords(){
	var psw_input = document.getElementById("new-passw2");			// El input
	var psw_input_msj = document.getElementById("new-passw2-msj");	// El msj de error
	var boton = document.getElementById("create-boton");			// El botón de envío

	// Cambiamos la clase css del mensaje a rojo, el input a rojo, y deshabilitamos el boton
	psw_input_msj.setAttribute("class", "leyenda-red");
	psw_input.setAttribute("class", "check-input");
	boton.setAttribute("disabled", "true");
}

// Caso 2 - Password válido
function both_valid_passwords(){
	var psw_input = document.getElementById("new-passw2");			// El input
	var psw_input_msj = document.getElementById("new-passw2-msj");	// El botón de envío

	// Cambiamos la clase css del mensaje a nulo, el input normal, y habilitamos el boton
	psw_input_msj.setAttribute("class", "leyenda-none");
	psw_input.setAttribute("class", "");
}

// Funcion que cambia el css cuando se envía el login -----------------------------------
// Es llamado cuando el Usuario o password incorrectos
function user_nonexisting(){
	var name_input = document.getElementById("new-user");
	var name_input_msj = document.getElementById("new-user-msj");

	name_input_msj.setAttribute("class", "leyenda-none");
	name_input.setAttribute("class", "");
}

function disable_buttons(){
	var boton1 = document.getElementById("create-boton");			// El botón de envío
	var boton2 = document.getElementById("login-button");

	boton1.setAttribute("disabled", "true");
	boton2.setAttribute("disabled", "true");
}

function able_button_create(){ // funcion que habilita el boton de crear cuenta
	var boton = document.getElementById("create-boton");			// El botón de envío
	// Verificamos si hay otro error activo
	let msj1 = document.getElementById("new-user-msj").getAttribute("class");
	let msj2 = document.getElementById("new-passw1-msj").getAttribute("class");
	let msj3 = document.getElementById("new-passw2-msj").getAttribute("class");
	not_active_error = (msj1 != "leyenda-red" && msj2 != "leyenda-red" && msj3 != "leyenda-red");
	
	let input1 = document.getElementById("new-user");
	let input2 = document.getElementById("new-passw1");
	let input3 = document.getElementById("new-passw2");

	// Si todos los inputs tienen algún valor guardado
	if (input1 != null && input2 != null && input3 != null){
		non_empty_input = (input1.value != '' && input2.value != '' && input3.value != '')
		// Si no hay un error activo y no hay inputs vacíos
		if (not_active_error && non_empty_input) {
			// Volvemos a habilitar el botón
			boton.removeAttribute("disabled");
		}
	}
}

function able_button_login(){ // funcion que habilita el boton de crear cuenta
	var boton = document.getElementById("login-button");	// El botón de envío

	let input1 = document.getElementById("user");
	let input2 = document.getElementById("passw");

	// Si todos los inputs tienen algún valor guardado
	if (input1 != null && input2 != null){
		// Si no hay inputs vacíos
		non_empty_input = (input1.value != '' && input2.value != '')
		if (non_empty_input) {
			// Volvemos a habilitar el botón
			boton.removeAttribute("disabled");
		}
	}
}