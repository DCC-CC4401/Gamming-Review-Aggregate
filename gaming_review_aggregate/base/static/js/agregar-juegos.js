let genres = ["Action", "Adventure", "Fighting", "Platform",
        "Puzzle", "Racing", "Role-playing", "Shooter", "Simulation",
        "Sports", "Strategy", "Other"];

let large = 0;
let large_genres = genres.length;
function addOptions(genre, num, v1, v2, value){
    if(value == null){
    }

    else{
        let option = document.createElement("option");
        option.text = value;
        genre.add(option);
    }

    var bol = false;
    for (let i = 0; i < large_genres; i++){
        if(num == 1){
            bol = genres[i] == v1;
        }
        else if(num == 2){
            bol = (genres[i] == v1  || genres[i] == v2);
        }

        if(bol){
        }
        else{
            if (value==genres[i]){
            }
            else{
                let option = document.createElement("option");
                option.text = genres[i];
                genre.add(option);
            }
        }
    }

}

function addgenre(){
    if (large == 0){
        let genre = document.getElementById('gen1');
        addOptions(genre, 0);
        large++;
    }

    else if (large == 1){
        let genre2 = document.getElementById('addgenre2');
        genre2.innerHTML = '<select id="gen2" name="gen" onchange="changeGenres(2)">';

        let genre_value = document.getElementById('gen1').value;
        let gen2 = document.getElementById('gen2');
        addOptions(gen2, 1, genre_value);
        large++;

    }
    else if (large == 2) {
        let genre3 = document.getElementById('addgenre3');
        genre3.innerHTML = '<select id="gen3" name="gen" onchange="changeGenres(3)">';

        let genre_value = document.getElementById('gen1').value;
        let genre_value2 = document.getElementById('gen2').value;

        let gen3 = document.getElementById('gen3');

        addOptions(gen3, 2, genre_value, genre_value2);

        let boton = document.getElementById("add-genre-button");
        boton.setAttribute("style", "display:none");
        large++;
    }
}

function changeGenres(n){
    var genre = "";
    var value = "";
    if (n == 1){
        genre = document.getElementById("gen1");
        value = genre.value;
    }
    else if (n == 2){
        genre = document.getElementById("gen2");
        value = genre.value;
 
    }
    else if (n == 3){
        genre = document.getElementById("gen3");
        value = genre.value;
    }

    if (large == 1){
    }

    else if (large == 2){
        var x = n + 1;
        if(x==4){
            x=1
        }

        let genre2 = document.getElementById("gen" + x);
        let value2 = genre2.value;

        genre.innerHTML = "";
        genre2.innerHTML = "";

        addOptions(genre, 1 , value2, 0, value);
        if(value == value2){
            addOptions(genre2, 1, value);
        }
        else{
            addOptions(genre2, 1, value, 0, value2);
        }

    }
    else if (large == 3){
        var x1 = n + 1;
        var x2 = n + 2;
        if(x1 == 4){
            x1 = 1
            x2 = 2;
        }
        if(x2 == 4){
            x2 = 1;
        }

        let genre2 = document.getElementById("gen" + x1);
        let value2 = genre2.value;

        let genre3 = document.getElementById("gen" + x2);
        let value3 = genre3.value;

        genre.innerHTML = "";
        genre2.innerHTML = "";
        genre3.innerHTML = "";

        addOptions(genre, 2, value2, value3, value);
        if(value == value2){
            addOptions(genre2, 2, value, value3);
            addOptions(genre3, 2, value, value2, value3);
        }
        else if (value == value3 || value2 == value3){
            addOptions(genre2, 2, value, value3, value2);
            addOptions(genre3, 2, value, value2);
        }
        else{
            addOptions(genre2, large, value, value3, value2);
            addOptions(genre3, large, value, value2, value3);
        }
    }
}

