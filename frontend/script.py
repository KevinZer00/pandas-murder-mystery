import pandas as pd
from js import document
from pyodide.ffi import create_proxy

# load the datasets
crew_manifest = pd.read_csv('../datasets/crew_manifest_final.csv')
communication_logs = pd.read_csv('../datasets/communication_logs_final.csv')
interview_logs = pd.read_csv('../datasets/interview_logs_final.csv')
medical_logs = pd.read_csv('../datasets/medical_logs_final.csv')
security_logs = pd.read_csv('../datasets/security_logs_final.csv')

def run_query(event):
    query_box = document.getElementById('query')
    output_box = document.getElementById('output')

    # environment to run user code 
    env = {
        "pd": pd,
        "crew_manifest": crew_manifest,
        "communication_logs": communication_logs,
        "interview_logs": interview_logs,
        "medical_logs": medical_logs,
        "security_logs": security_logs
    }

    try:
        code = query_box.value.strip()

        # split lines, separate last line
        lines = code.split("\n")
        *statements, last_line = lines

        # execute all lines except last one 
        for stmt in statements:
            exec(stmt, env)

        # evaluate last line if it's valid
        try:
            result = eval(last_line, env)  # try evaluating the last line
        except SyntaxError:
            exec(last_line, env)  # if not evaluable, just execute it
            result = None

        # display result
        if result is not None:
            if hasattr(result, "to_html"):
                output_box.innerHTML = result.to_html()
            else:
                output_box.innerText = str(result)
        else:
            output_box.innerText = "Code executed successfully. (No output)"

    except Exception as e:
        output_box.innerText = f"Error: {e}"


# bind the button click to run_query
button = document.getElementById("run-btn")
button.addEventListener("click", create_proxy(run_query))


imposter_name = "Elliot Perez"

def check_answer(event):
    user_input = document.getElementById("imposter-input").value.strip()

    result_message = document.getElementById("result-message")

    # check if user typed name in all lowercase
    if user_input.lower() == imposter_name.lower():
        result_message.innerText = "You've found the imposter!"
        result_message.style.color = "lime"
    else:
        result_message.innerText = "Wrong guess. Try again before it's too late!"
        result_message.style.color = "red"

button2 = document.getElementById("submit-answer")
button2.addEventListener("click", create_proxy(check_answer))