Dear **{{ data.random.company_name | safe }}**,

the user **<{{ data.random.user_mail | safe }}>** has successfully submitted the
**{{ data_type == 'co2mpas' and 'correlation' or 'JET' | safe }} output report** (*{{ data.database.uploaded_fname | safe }}*).
{% if status_random != 2 %}
The attached zip file *{{ receipt_id | safe }}.zip* contains:

- the **DICE Receipt** *{{ receipt_id | safe }}.dice*,
- a python script *verification.py* to validate the DICE Receipt and optionally
  generate the **COMPLETE {{ data_type == 'co2mpas' and 'CORRELATION' or 'DICE' | safe }} FILE**, and
- a *README.rst* that explains how to use the content of the zip file.

The **DICE receipt hash** is the following:

**{{ data.database.hash__dice_receipt | safe }}**
{% if data_type == 'co2mpas' %}{% if status_random == 0 %}
The random number is **{{ data.random.random | safe}}** for the submitted
vehicle family id (*{{ data.database.vehicle_family_id | safe }}*).
{% elif status_random == 1 %}
The random number is not present in the **DICE Receipt**, because the submitted
vehicle family id *{{ data.database.vehicle_family_id | safe }}* is linked to
*{{ data.ta_id.parent_vehicle_family_id | safe }}* - i.e.,
**DICE Receipt** *{{ splitext(parent[1])[0] | safe }}.dice*.
{% elif status_random == 3 %}
The random number is not present in the **DICE Receipt**, because the submitted
vehicle family id *{{ data.database.vehicle_family_id | safe }}* is hybrid.
{% elif status_random == 4 %}
The random number is not present in the **DICE Receipt**, because you have
corrected just the vehicle family id of the previous submission - i.e.,
**DICE Receipt** *{{ splitext(prev_valid[1])[0] | safe }}.dice*.
{% elif status_random == 5 %}
The random number is not present in the **DICE Receipt**, because you have
corrected the target NEDC values of the previous submission - i.e.,
**DICE Receipt** *{{ splitext(prev_valid[1])[0] | safe }}.dice*. Therefore, a
physical NEDC test should be performed.
{% elif status_random == 6 %}
The random number is not present in the **DICE Receipt**, because you have
submitted a wltp-retest = 'a' that is linked to the previous submission - i.e.,
**DICE Receipt** *{{ splitext(prev_valid[1])[0] | safe }}.dice*.
{% elif status_random == 7 %}
The random number is not present in the **DICE Receipt**, because you have
submitted a correction that does not change CO2MPAS output in respect to the
previous submission - i.e.,
**DICE Receipt** *{{ splitext(prev_valid[1])[0] | safe }}.dice*.
{% endif %}
{% if status_random != 3 %}
The |CO2MPAS| deviations are the following:

{{ tabulate(deviations, headers='firstrow', tablefmt='rst') | safe }}
{% endif %}{% endif %}
To validate the **DICE Receipt** and generate the **COMPLETE {{ data_type == 'co2mpas' and 'CORRELATION' or 'DICE' | safe }} FILE**
you have to unzip the attached file and follow the instructions written in
the *README.rst*.
{% elif status_random == 2 %}
Since the vehicle is a bi-fuel, to complete the submission procedure you have to
submit a second **{{ data_type == 'co2mpas' and 'correlation' or 'JET' | safe }} output report** with the second fuel type.
{% endif %}
Best regards,

The DICE Team

.. |CO2MPAS| replace:: CO\ :sub:`2`\ MPAS