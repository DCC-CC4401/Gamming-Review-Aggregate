let bol = true;

function hasError(variable, max, regex, min=0){
	if (variable.length < min || variable.length > 100 || !regex.test(variable)){
		bol = false;
		return true;
	}
	return false;
}

function error_text(type, name){
	return type + " '" + name + "' no es válido. \n\n";
}

function validation() {
	bol = true;
    let error = "";

	//Validar sector
    let sector = document.getElementsByName("sector")[0].value; 
	let sector_regex = /^([a-zA-Z]+)((\s)([a-zA-Z]|[1-9])+)*$/

	if(sector.length!=0){
		if(hasError(sector,100,sector_regex)){
			error += error_text("Sector",sector);
		}
	}

	//Validar Nombre
    let nombre = document.getElementsByName("nombre")[0].value; 
	let nombre_regex = /(^([A-zÁ-ú]+)$)|(^([A-zÁ-ú]+)(\s)([A-zÁ-ú]+)$)|(^([A-zÁ-ú]+)(\s)([A-zÁ-ú]+)(\s)([A-zÁ-ú]+)$)|(^([A-zÁ-ú]+)(\s)([A-zÁ-ú]+)(\s)([A-zÁ-ú]+)(\s)([A-zÁ-ú]+)$)/;

	if(hasError(nombre,100,nombre_regex)){
		error += error_text("Nombre", nombre);
	}

	//Validar email 
	let email = document.getElementsByName("email")[0].value; 
	let email_regex = /(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@[*[a-zA-Z0-9-]+.[a-zA-Z0-9-.]+]*/;

	if(hasError(email,100,email_regex)){
		error += error_text("Email", email);
	}

	//Validar numero de celular
	let number = document.getElementsByName("celular")[0].value; 
	let number_regex = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{3,6}$/

	if(hasError(number,100,number_regex)){
		error += error_text("Numero", number);
	}

	//Validar fechas de avistamientos
	let date = document.getElementsByName("dia-hora-avistamiento");
	let large = date.length;
	let date_regex =/^\d{4}\-\d{2}\-\d{2}\n\d{2}:\d{2}$/;

	for(let i = 0; i < large; i++){
		if(hasError(date[i].value,100, date_regex)){
			let num = i+1;
			error += error_text("Día-hora del avistamiento " + num, date[i].value);
		}
	}

	error += "Ingrese los datos nuevamente";

	if(bol){
		confirm("¿Esta seguro que desea enviar esta información?")
		let form = document.getElementById("formulario");
		form.innerHTML = "<h3> Hemos recibido su información, muchas gracias por colaborar</h3>";
	}
	else{
		alert(error);
		return false;
	}
}
