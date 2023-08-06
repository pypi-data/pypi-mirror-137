DICE RECEIPT
============
{{ message }}

VERIFICATION
============
{{ tabulate([
        ['DICE Receipt Hash', hash],
        ['DICE Receipt Signature', signature]
   ], tablefmt='grid') | safe }}

Server Public Key
-----------------
{{ server_pub_key }}