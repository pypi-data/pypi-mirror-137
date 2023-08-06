# project_structure_pypi

A package created solely for teaching (and maybe entertainment) reasons.

It has a package with two modules, scraper and date. 

`scraper` looks for a date in wikipedia and extracts the celebrities that were born that day

`date` has a `Date` class that displayes the date, and has a method `to_wiki_format` so the wikipedia URL can read it

Thus, both classes can work together, first to ask for a date, then it translate it to something readable by the wikipedia URL, and then scrape the necessary data.
