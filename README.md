# Quantum Scheduling & AI Advisors

Our project has two main functions.

Students deal with a lot of stress and the last thing we want is to have final scheduling conflicts.\
We want to minimize these conflicts with students using a quantum final scheduler builder we created.

The second focus is an AI advisor where given a netID and a query, we can return a personalized response.
This response recommends upcoming classes to take based of historical grades and data, and more.

**qaoa_scheduler.py** : Quantum algorithms to generate finals schedule\
**cqm_final_scheduler** : Very efficient, (Needs a DWave Quantum Annealer)

**advisor.py** : Generates response using AI/ML for classes advice, also has a function for CLI\
**AIstudentdata.py** : Generated "Mimic" Data to be used to train advisor.py\
**/data** : holds csv files used for advisor.py machine learning.\
**finetunegpt2.py** : fine-tunes a GPT-2 model on the generated dataset applying tokenization, training with Trainer, and saving the final model.

**app.py** : Flask app/API to serve files, route, run functions\
**makedata.py** : Generate json data (database) for classes and students\
**scheduling.py** : Efficient algorithm to find optimal schedules

**/templates or /static** : html and css files for frontend\
**studentdata.json** : json data for classes and students
