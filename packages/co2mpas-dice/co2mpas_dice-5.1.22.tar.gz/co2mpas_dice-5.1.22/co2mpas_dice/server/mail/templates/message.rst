Info
----
{{ tabulate(info, tablefmt='grid') | safe }}

Uploaded Files
--------------
{{ tabulate(files, tablefmt='grid') | safe }}
{% if status_random == 0 %}
Random Number
-------------
{{ tabulate(random, tablefmt='grid') | safe }}
{% endif %}