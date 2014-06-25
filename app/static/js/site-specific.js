function addNameField(){
    var newdiv = document.createElement('div');
    newdiv.innerHTML = "<input id=\"nimi\" name=\"nimi\" placeholder=\"Nimi\" type=\"text\" value=\"\">";
    document.getElementById('comment_fields').appendChild(newdiv);
}

