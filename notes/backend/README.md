# Backend Documentation

Consult Joel for setting up local environment in order to use backend.

Assuming you have everything set up and working, calls to the backend api start with http://localhost:8000/, serving the home page by default.

| Link | Description | Returns | Notes
--- | --- | --- | ---
data/recipes/ | Get a list of all recipes in database | HTML | append `?format=api` or `?format=json` to return browsable api or json
data/recipes/### | Get details of specific recipe | HTML | change ### to hash id of recipe (hash id specific to your local database)
data/recipes/?ingredients=INGREDIENTS | Search database for recipes containing specified list of ingredients | HTML | for example, `?ingredients=chicken+bread` to search for recipes including chicken and/or bread in its ingredients list
data/recipes/?ordering=num_ingreds | Get list of all recipes ordered by number of ingredients | HTML | default is ascending, change to `?ordering=-num_ingreds` for descending
data/ingredients/ | Get a list of all ingredients in database | API | 
data/ingredients/?name=NAME&category=C | Search ingredients by NAME and category C | API | one parameter can be omitted if desired
data/ingredients/?search=SEARCH | Search ingredients whose name contains SEARCH | API | this is a regex search

