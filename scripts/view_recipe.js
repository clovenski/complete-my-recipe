var query = location.search.substring(1);
var request = new XMLHttpRequest();
request.open('GET', 'http://localhost:8000/recipes/' + query, true);
request.onload = function() {
  var json = JSON.parse(request.responseText);
  document.getElementById('name').innerHTML = json.name;
  document.getElementById('num_ingreds').innerHTML += json.num_ingreds;
  document.getElementById('ingredients').innerHTML += json.ingred_list;
  document.getElementById('instructions').innerHTML += json.instructions;
};
request.send(null);