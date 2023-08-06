INSTRUCTIONS
============

1. unzip the attached zip file *{{ receipt_id | safe }}.zip* into a **FOLDER**,
2. [optional] copy the {{ data_type == 'co2mpas' and 'CO2MPAS' or 'JET' | safe }} outputs (i.e., .{{ data_type | safe }}.zip) inside the FOLDER
   that contains the **DICE Receipt** *{{ receipt_id | safe }}.dice* and the
   script *verification.py*,
3. open the **{{ data_type == 'co2mpas' and 'CO2MPAS' or 'CMD' | safe }} console** and change directory to the previous mentioned
   FOLDER (you can use the command `cd relative/path/to/folder`),
4. run the script `verification.py` using the command `python verification.py`,
5. read the console log to see the verification status.

.. note:: The generation of the **COMPLETE {{ data_type == 'co2mpas' and 'CORRELATION' or 'DICE' | safe }} FILE** works only if you
          have not renamed/modified the {{ data_type == 'co2mpas' and 'CO2MPAS' or 'JET' | safe }} outputs.