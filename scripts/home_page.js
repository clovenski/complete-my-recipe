var queryParams = new Set([]);
// var delayTimer = null;

// function searchIngredient(name) {
//     if (name.length == 0) {
//         clearTimeout(delayTimer);
//         document.getElementById("suggestions").innerHTML = "Suggestions pop up here.";
//     } else {
//         clearTimeout(delayTimer);
//         delayTimer = setTimeout(function() {
//             var request = new XMLHttpRequest();
//             request.onreadystatechange = function() {
//                 if (this.readyState == 4 && this.status == 200) {
//                     document.getElementById("suggestions").innerHTML = "";
//                     response = JSON.parse(this.responseText);
//                     if (response.length == 0) {
//                         document.getElementById("suggestions").innerHTML = "No matches.";
//                     }
//                     for (var i = 0; i < response.length; i++) {
//                         var ingredient = response[i]["name"];
//                         if (queryParams.has(ingredient)) {
//                             continue;
//                         }
//                         var suggestion = document.createElement("button");
//                         suggestion.id = ingredient;
//                         suggestion.setAttribute("class", "suggestion");
//                         suggestion.setAttribute("onclick", "addIngredient(this.id)");
//                         suggestion.innerHTML = response[i]["name"];
//                         document.getElementById("suggestions").appendChild(suggestion);
//                     }
//                 }
//             };
//             request.open("GET", "/data/ingredients/?search=" + name, true);
//             request.send();
//         },1500);
//     }
// }

// function addIngredient(name) {
//     queryParams.add(name);
//     document.getElementById("searchButton").disabled = false;
//     var ingredient = document.getElementById(name);
//     document.getElementById("suggestions").removeChild(ingredient);
//     document.getElementById("userIngredients").appendChild(ingredient);
//     ingredient.setAttribute("onclick", "removeIngredient(this.id)");
//     ingredient.setAttribute("class", "userIngredient");
// }

function removeIngredient(name) {
    queryParams.delete(name);
    if (queryParams.size == 0) {
        document.getElementById("searchButton").disabled = true;
    }
    var ingredient = document.getElementById(name);
    document.getElementById("userIngredients").removeChild(ingredient);
}

function enterIngred(e, val) {
    var keycode = (e.keycode ? e.keycode : e.which);
    if (keycode == "13" && val != "") {
        var ingred = document.createElement("button");
        ingred.id = val;
        ingred.innerHTML = val;
        queryParams.add(ingred.id);
        document.getElementById("searchButton").disabled = false;
        document.getElementById("userIngredients").appendChild(ingred);
        ingred.setAttribute("onclick", "removeIngredient(this.id)");
        ingred.setAttribute("class", "userIngredient");
        document.getElementById("ingredinput").value = "";
    }
}

function executeSearch() {
    if (queryParams.size > 0) {
        var link = "/data/recipes/";
        var missing = document.getElementById("tolerance").value;
        if (missing != "") {
            link += "?tolerance=" + missing;
        } else {
            link += "?tolerance=5";
        }
        link += "&ingredients=";
        queryParams.forEach(function(id) {
            link += id.replace(/ /g, '_') + "+";
        });
        link = link.substring(0, link.length - 1);
        window.location = link;
    }
}