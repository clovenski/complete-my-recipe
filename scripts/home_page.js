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
                        var ingredient = response[i]["name"];
                        if (queryParams.has(ingredient)) {
                            continue;
                        }
                        var suggestion = document.createElement("button");
                        suggestion.id = ingredient;
                        suggestion.setAttribute("class", "suggestion");
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

function addIngredient(name) {
    queryParams.add(name);
    var ingredient = document.getElementById(name);
    document.getElementById("suggestions").removeChild(ingredient);
    document.getElementById("userIngredients").appendChild(ingredient);
    ingredient.setAttribute("onclick", "removeIngredient(this.id)");
    ingredient.setAttribute("class", "userIngredient");
    queryParams.add(name);
}

function removeIngredient(name) {
    queryParams.delete(name);
    var ingredient = document.getElementById(name);
    document.getElementById("userIngredients").removeChild(ingredient);
}

function executeSearch() {
    var link = "/data/recipes/";
    var missing = document.getElementById("tolerance").value;
    if (missing != "") {
        link += "?tolerance=" + missing;
    } else {
        link += "?tolerance=5";
    }
    if (queryParams.size > 0) {
        link += "&ingredients=";
        queryParams.forEach(function(id) {
            link += id + "+";
        });
        link = link.substring(0, link.length - 1);
    }
    window.location = link;
}