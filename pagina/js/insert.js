let i = 2;
let foto = 0;

function addZero(num){
	if (num < 10){
		return '0' + num;
	}
	else{
		return num;
	}
}

function time(){
	let date = new Date();
	let year = date.getFullYear();
	let month = addZero(date.getMonth());
	let day = addZero(date.getDate());

	let text = year + "-" + month + "-" + day;

	let hour = addZero(date.getHours());
	let minutes = addZero(date.getMinutes());
	text += "\n" + hour + ":" + minutes;
	return text;
}


function insertInputFile() {
    if (i > 5) {
		alert("No puedes ingresar más de 5 fotos");
		return;
    }

    let c = document.getElementById("fotos" + foto);
    c.innerHTML += "<div class='entrada'> <div class='leyenda'>Foto</div> <input type='file'" + "name='foto-avistamiento'> </div>"
	i+=1;
}

function insertNewA() {
	foto+=1
    let c = document.getElementById("avistamientos");
	c.innerHTML += `
	<h4> Información avistamiento</h4>
	<div class="entrada">
		<div class="leyenda" >Día - Hora </div>
			<textarea name="dia-hora-avistamiento" rows=2 >` + time() + `</textarea>

		</div>
	<div class="entrada">

	<div class="leyenda">Tipo</div>
		<select name="tipo-avistamiento">
			<option value="insecto">Insecto</option>
			<option value="aracnido">Arácnido</option>
			<option value="miriapodo">Miriápodo</option>
			<option value="nose">No sé</option>
		</select>
	</div>

	<div class="entrada">
		<div class="leyenda">Estado</div>
			<select name="estado-avistamiento">
			<option value="vivo">Vivo</option>
			<option value="muerto">Muerto</option>
			<option value="nose">No sé</option>
		</select>
	</div>

	<div id="fotos` + foto + `">
		<div class="entrada">
			<div class="leyenda">Foto</div>
				<input type="file" name="foto-avistamiento">
			</div>
		</div>
	</div>`;
	i = 2;
}
insertNewA();




