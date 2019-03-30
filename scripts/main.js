var queryParams = new Set([]);
var delayTimer = null;

function searchIngredient(name) {
    if (name.length == 0) {
        clearTimeout(delayTimer);
        document.getElementById("suggestions").innerHTML = "Suggestions pop up here.";
    } else {
        clearTimeout(delayTimer);
        delayTimer = setTimeout(function() {
            var request = new XMLHttpRequest();
            request.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    document.getElementById("suggestions").innerHTML = "";
                    response = JSON.parse(this.responseText);
                    if (response.length == 0) {
                        document.getElementById("suggestions").innerHTML = "No matches.";
                    }
                    for (var i = 0; i < response.length; i++) {
                        var ingredientID = response[i]["id"];
                        if (queryParams.has(ingredientID)) {
                            console.log(ingredientID);
                            continue;
                        }
                        var suggestion = document.createElement("button");
                        suggestion.id = ingredientID;
                        suggestion.setAttribute("onclick", "addIngredient(this.id)");
                        suggestion.innerHTML = response[i]["name"];
                        document.getElementById("suggestions").appendChild(suggestion);
                    }
                }
            };
            request.open("GET", "/data/ingredients/?search=" + name, true);
            request.send();
        },1500);
    }
}

function addIngredient(id) {
    queryParams.add(id);
    var ingredient = document.getElementById(id);
    document.getElementById("suggestions").removeChild(ingredient);
    document.getElementById("userIngredients").appendChild(ingredient);
    ingredient.setAttribute("onclick", "removeIngredient(this.id)");
    queryParams.add(id);
}

function removeIngredient(id) {
    queryParams.delete(id);
    var ingredient = document.getElementById(id);
    document.getElementById("userIngredients").removeChild(ingredient);
}

function executeSearch() {
    var link = "/data/recipes/";
    if (queryParams.size > 0) {
        link += "?ingredients=";
        queryParams.forEach(function(id) {
            link += id + "+";
        });
        link = link.substring(0, link.length - 1);
    }
    window.location = link;
}