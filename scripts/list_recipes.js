var query = location.search;
var request = new XMLHttpRequest();
request.open('GET', 'http://localhost:8000/recipes/' + query, true);
request.onload = function() {
  var json = JSON.parse(request.responseText);
  for (var i = 0; i < json.length; i++) {
    var ref = 'view_recipe.html?' + json[i].id;
    var innerHTML = '<li><a href="' + ref + '">' + json[i].name + '</link></li>';
    document.getElementById('recipe_list').innerHTML += innerHTML;
  }
};
request.send(null);