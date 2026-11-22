# Created by: Pieter Barkema
# Date: February, 2022
# Description:
#    This file creates a GUI for uploading and processing neuroimaging data
#    with normative modelling. The backend computes results and returns them to
#    users accessing from all over the world.
#    It is hosted as a website from a remote gunicorn server.


from dash import Dash, html, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc
from dash_extensions.enrich import MultiplexerTransform, DashProxy
from dash.exceptions import PreventUpdate
import pandas as pd
from subprocess import PIPE, Popen, run, call, check_output
from flask import Flask
import ast, io, json, os, base64, subprocess

server = Flask(__name__)
# DashProxy is used instead of Dash to enable mapping multiple functions to one output (currently unused).
app = DashProxy(server=server, external_stylesheets=[dbc.themes.MATERIA],
                title='PCNportal', update_title=None,transforms=[MultiplexerTransform()])

NOT_CONNECTED = ["No information could be retrieved. You are not connected to the server."]

def run_server_script(script, *args):
    """Run a script from the server scripts folder and return what it prints ("" on failure)."""
    script_path = os.path.join(os.environ['PROJECTDIR'], os.environ['SCRIPTDIR'], script)
    python = os.environ['PROJECTDIR'] + "/" + os.environ['PYTHON_ENV'] + "/bin/python"
    cmd = ["ssh", "-o", "StrictHostKeyChecking=no", os.environ['MYUSER'], python, script_path, *args]
    p = Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, _ = p.communicate()
    return str(output, encoding='UTF-8').strip()

# This function retrieves available data types or models.
def retrieve_options(data_type=None):
    try:
        # Choose between data type or models directory
        chosen_dir = os.path.join(os.environ['PROJECTDIR'], os.environ['MODELS'])
        if data_type is not None:
            chosen_dir = os.path.join(chosen_dir, data_type)
        output = run_server_script(os.environ['LISTDIR'], chosen_dir)
    except KeyError:
        return NOT_CONNECTED
    # Catch empty strings when no connection to the server could be made.
    try:
        return ast.literal_eval(output)
    except (SyntaxError, ValueError, TypeError):
        return NOT_CONNECTED
# -----------------------------------------------------------------
# The GUI of the app is specified below.
app.layout = html.Div([ 
    html.Div([
    # Columns keep the tabs and their contents centered and aligned.
    dbc.Col(
    dcc.Tabs([
        dcc.Tab(label='Home', children=[
            html.Br(),
            html.Div(
                dcc.Markdown(id='home-readme', link_target="_blank", dangerously_allow_html=True), style={'margin':'auto','width':"80%"}
            )
        ]),
        dcc.Tab(label='How to model', children=[
            html.Br(),
            html.Div(
                dcc.Markdown(id="howto-readme", link_target="_blank", dangerously_allow_html=True), style={'margin':'auto','width':"80%"}
            )
        ]),
        dcc.Tab(label='Model information', children=[
            html.Br(),
            html.Div(
                dcc.Markdown(id="modelinfo-readme", link_target="_blank", dangerously_allow_html=True), style={'margin':'auto','width':"80%"},
            )
        ]),
        

        # The submission form
        dcc.Tab(label='Compute here!', id='modelling',
        children=[
            html.Div(children=[
                # Best practice for variable storage in Dash
                dcc.Store(id='session_id', data=""),
                dcc.Store(id='previous_request', data=[]),
                dcc.Store(id="model_regions", data=[]),
                dcc.Store(id="mandatory_columns", data=[]),

                html.Br(),
                html.Label('Data type'),
                dcc.Dropdown(retrieve_options(), 'please select data type first...', id='data-type'),
                
                html.Br(),
                html.Label('Normative Model'),
                dcc.Dropdown(['please select data type first...'], 'please select data type first...', id='model-selection'),
                html.Br(),
                dcc.Markdown(id="model-readme", link_target="_blank", dangerously_allow_html=True), 
                
                html.Label('Select data file format'),
                # Only .csv is supported at this time
                dcc.Dropdown(['.csv'], '.csv', id='file-format'),

                html.Br(),
                html.Hr(),
                html.Label('Upload test data'),
                html.Hr(),
                dcc.Upload([
                    'Drag and Drop or ',
                    html.A('Select a File')
                ], style={
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center'
                },
                    id= 'upload_test_data',
                    # 1GB limit prevents security risk of overloading server memory
                    max_size= 1000000000
                ),             
                html.P(id="list-test-fname"),
                html.Hr(),
                html.Label('Upload adaptation data'),
                html.Hr(),
                dcc.Upload([
                    'Drag and Drop or ',
                    html.A('Select a File')
                ], style={
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center'
                },
                    id= 'upload_adapt_data',
                    max_size= 1000000000 #1 GB
                ),
                html.P(id="list-adapt-fname"),

                html.Br(),
                html.Label('Email address for results: '),
                html.Br(),
                dcc.Input(value='', type='text', id='email_address', style={'width':'40%'}),         

                html.Div(
                    children=[
                        # -----------------------------------------------------------------
                        # TO-DO: Check boxes to control what results the user wants to receive.
                        # dcc.Checklist(className ='checkbox_1',
                        #             style={'margin-right': '0%'},
                        #             options=[
                        #                 {'label': 'raw data', 'value': 'I1ST2', 'disabled': True},
                        #                 {'label': 'raw data', 'value': 'I2ST2', 'disabled': True},
                        #                 {'label': 'raw data', 'value': 'I3ST2', 'disabled': True},
                        #                 {'label': 'raw data', 'value': 'I4ST2', 'disabled': True}
                        #                     ],
                        #             value=['I1ST2'],
                        #             labelStyle = {'display': 'block'}
                        #                     ),
                        # dcc.Checklist(className ='checkbox_2',
                        #             style={'margin-right': '0%'},
                        #             options=[
                        #                 {'label': 'visualization', 'value': 'I1MT', 'disabled': True},
                        #                 {'label': 'visualization', 'value': 'I2MT', 'disabled': True},
                        #                 {'label': 'visualization', 'value': 'I3MT', 'disabled': True},
                        #                 {'label': 'visualization', 'value': 'I4MT', 'disabled': True}
                        #                 ],
                        #             value=[],
                        #             labelStyle = {'display': 'block'}
                        #                     ),
                        # dcc.Checklist(className ='checkbox_3',
                        #             style={'margin-right': '0%'},
                        #         options=[
                        #             {'label': 'z-score brain space', 'value': 'I1ST1', 'disabled': True},
                        #             {'label': 'Centile plots', 'value': 'I2ST1', 'disabled': True},
                        #             {'label': 'Exp. Var. plots', 'value': 'I3ST1', 'disabled': True},
                        #             {'label': '[other error measures]', 'value': 'I4ST1', 'disabled': True}
                        #                 ],
                        #         value=['I1ST1'],
                        #         labelStyle = {'display': 'block'}
                        #                 ),
                        html.Div(
                            style={'float':'right'},
                            children=[
                                html.Button("Submit", id="btn_csv", disabled=False),
                            ]
                        )
                        ]
                    , style={'float': 'right', 'display':'flex'}
                    ),
                
                    html.Div(
                        style={'float':'center'},
                        children=[
                            html.Br(),
                            # Instant feedback loading/error on request without waiting for completion.
                            dbc.Alert(id="loading_or_error", is_open=False,
                                children="Your computation request is being submitted..."),
                            # Slower feedback when request is completed.    
                            dbc.Alert(id="completed", is_open=False, color='success'),
                            html.Br(),
                        ]
                       ),
                    html.Div(
                dcc.Markdown(id="compute", link_target="_blank", dangerously_allow_html=True), style={'margin':'auto'},
            )
            ], style={'margin':'auto', 'width':'75%', 'flex': 1}),
        ]),
        dcc.Tab(label='Data privacy', children=[
            html.Br(),
            html.Div(
                dcc.Markdown(id="dataprivacy", link_target="_blank", dangerously_allow_html=True), style={'margin':'auto','width':"80%"},
            )
        ]),
    ])
    ),
#     html.Div(
#         style={'position': 'absolute', 'left': '78%', 'top': '88%', 'height':'90px', 'width':'70px'}, #'padding':'0%', 'left': '99%', 'top': '97%',
#         children=[
#             # Workaround: readmes didn't load. Let image loading trigger the readme loading. 
#             html.Img(id="load-readme-trigger",src='assets/merged_images_update.png', alt='image', style={'height':'90%', 'width':'90%'}), #'padding': '0%', , 'height':'700%', 'width':'700%'
#         ]
# ),

    ], className="myDiv", style={'position': 'absolute', 'font-size':'small','display': 'flex', 'flex-direction': 'row', 'z-index': '1', 'height': '40%', 'width': '50%', 'position': 'relative', 'top':'40%', 'left':'25%', 'backgroundColor':'white'}),
    html.Div(
   # style={'position': 'fixed', 'left': '68%', 'top': '-13%', 'height':'300px', 'width':'300px', 'z-index': '0'}, #'padding':'0%', 'left': '99%', 'top': '97%',
    style={'position': 'fixed', 'left': '72%', 'top': '-6.8%', 'height':'320px', 'width':'320px', 'z-index': '100'},
    children=[
        # Workaround: readmes didn't load. Let image loading trigger the readme loading. 
        html.Img(id="load-readme-trigger",src='assets/merged_images_update.png', alt='sponsor_logos_image', style={'height':'100%', 'width':'100%'}), #'padding': '0%', , 'height':'700%', 'width':'700%'
    ]
),
], style={'position': 'relative', 'flex-direction': 'column','vertical-align':'top'})
# -----------------------------------------------------------------
# All functions that handle input and output for the Dash components.
# -----------------------------------------------------------------

@app.callback(
    Output(component_id='home-readme', component_property='children'),
    Output(component_id='howto-readme', component_property='children'),
    Output(component_id='modelinfo-readme', component_property='children'),
    Output(component_id='compute', component_property='children'),
    Output(component_id='dataprivacy', component_property='children'),
    Input(component_id='load-readme-trigger', component_property='children'),
    prevent_initial_call=False
)
# Function for loading in static markdown files files.
def load_tabs_markdown(load_readme_trigger):
    def read(name):
        with open(os.path.join('assets', name), 'r', encoding='utf-8') as mdfile:
            return mdfile.readlines()
    return read('home.md'), read('howto.md'), read('modelinfo.md'), read('compute.md'), read('dataprivacy.md')

# Reads the chosen model's covariates, batch effects and regions (and README.md, if any)
# from model/normative_model.json on the server.
@app.callback(
    Output(component_id='model-readme', component_property='children'),
    Output(component_id='mandatory_columns', component_property='data'),
    Output(component_id='model_regions', component_property='data'),
    Input(component_id='model-selection', component_property='value'),
    State(component_id='data-type', component_property='value'),
    prevent_initial_call=True
)
def model_information(model_selection, data_type):
    # Only execute when model is chosen, to prevent errors.
    # no_update prevents error when 3 values are expected to be returned but none are returned.
    if model_selection in [None, 'please select data type first...', 'Select...', ""] or not data_type:
        return no_update, no_update, no_update

    model_path = os.path.join(os.environ['PROJECTDIR'], os.environ['MODELS'], data_type, model_selection)
    try:
        info = json.loads(run_server_script("model_info.py", model_path))
    except ValueError:  # No connection, or not a PCNtoolkit 1.x model
        return "No information could be retrieved for this model.", [], []

    batch_effects = ", ".join(f"{be} ({len(values)} values)" for be, values in info["batch_effects"].items())
    summary = (f"**Covariates:** {', '.join(info['covariates'])}  \n"
               f"**Batch effects:** {batch_effects}  \n"
               f"**Regions:** {len(info['regions'])}\n")
    mandatory_columns = info["covariates"] + list(info["batch_effects"])
    return info["readme"] + "\n\n" + summary, mandatory_columns, info["regions"]

# Function to restrict model choice based on data type choice
@app.callback(
    Output(component_id='model-selection', component_property='options'),
    [Input(component_id='data-type', component_property='value')],
    prevent_initial_call=True
)
def update_dp(data_type):
    model_selection_list = retrieve_options(data_type)
    return model_selection_list

# Evaluates the submitted data and gives a measure of success or a specific error.
def input_checker(mandatory_columns, model_regions, current_request, previous_request, email_address, data_type, model_selection, test_contents, test_filename, adapt_contents, adapt_filename, file_format):
    
    # Trivial errors.
    return_message = ""
    if email_address == "" or data_type =="" or model_selection =='please select data type first...' or test_filename =="" or adapt_filename =="":
        input_validated = False
        return_message = "One of your input fields is empty."
    elif isinstance(adapt_filename,str) and not adapt_filename.endswith(file_format):
        input_validated = False
        return_message = "Your adaptation data file extension does not match selected data type: " + str(file_format)
    elif isinstance(test_filename,str) and not test_filename.endswith(file_format):
        input_validated = False
        return_message = "Your test data file extension does not match selected data type: " + str(file_format)
    # Importantly, this checks if the request has changed at all to prevent spam clicks.
    elif current_request == previous_request:
        input_validated = False
        return_message = "You've already submitted this request."

    else: 
        test_data_columns = parse_contents(test_contents, test_filename).columns
        adapt_data_columns = parse_contents(adapt_contents, adapt_filename).columns
        if not model_regions:
            return False, "No model information was found. Please select the model again."

        # Evaluate only number of matching non-mandatory columns, i.e. idps.
        goal_columns = pd.Index(model_regions)

        # Ensure all mandatory columns are present.
        for col in mandatory_columns:
            if col not in test_data_columns or col not in adapt_data_columns:
                return False, "You are missing some or all of the following mandatory columns (batch effects or covariates) in your data sets: " + ", ".join(mandatory_columns) + ". "
        return_message = [return_message, "Your data set has all the necessary covariates and site effects for this model.", html.Br()]

        # Report the amount of matching template names per file.
        test_data_matches = goal_columns.intersection(test_data_columns).size
        adapt_data_matches = goal_columns.intersection(adapt_data_columns).size
        return_message = return_message +  ["Amount of adaptation features that match the model template: ", str(adapt_data_matches), " out of ", str(goal_columns.size), ". ", html.Br()] #[str(goal_columns.intersection(adapt_data_columns))] + [str(goal_columns.difference(adapt_data_columns))] +
        return_message = return_message + ["Amount of test features that match the model template: ", str(test_data_matches), " out of ", str(goal_columns.size), ". ", html.Br()]
        
        # Currently on the app both adaptation and test data are mandatory, but that is not necessary for modelling (future work).
        if test_data_matches < 1:
            input_validated = False
            return_message = "Your test data has no feature matches with the model's data template. "
            return input_validated, return_message
        if adapt_data_matches < 1:
            input_validated = False
            return_message = return_message + "Your adaptation data has no feature matches with the model's data template. "
            return input_validated, return_message
        input_validated = True
    return input_validated, return_message

# Main function for validating input.
@app.callback(
    Output("loading_or_error", "children"),
    Output("loading_or_error", "color"),
    Output("loading_or_error", "is_open"),
    Output("loading_or_error", "fade"),
    Output("session_id", "data"),
    Output("previous_request", "data"),
    State("email_address", "value"),
    State("data-type", "value"),
    State("model-selection", "value"),
    State("upload_test_data", "contents"),
    State("upload_test_data", "filename"),
    State("upload_adapt_data", "contents"),
    State("upload_adapt_data", "filename"),
    State("previous_request", "data"),
    State("file-format", "value"),
    State("model_regions", "data"),
    State("mandatory_columns", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def display_alert(email_address, data_type, model_selection, test_contents, test_filename, adapt_contents, adapt_filename, previous_request, file_format, model_regions, mandatory_columns, click):
    current_request = [email_address, data_type, model_selection, test_filename, adapt_filename, file_format]
    input_validated, return_message = input_checker(mandatory_columns, model_regions, current_request, previous_request, email_address, data_type, model_selection, test_contents, test_filename, adapt_contents, adapt_filename, file_format)
    
    # Only create a session ID if their input is valid, and start processing.
    if input_validated == True:
        import os, base64, uuid
        session_id = str(uuid.uuid4()).replace("-", "")
        mode_name = "test_session_" if 'LOCALTESTING' in os.environ else ""
        session_id = mode_name + session_id
        return_message = return_message + ["Your request is being processed with session ID: " + session_id]
        return return_message, "light", True, True, session_id, current_request
    # If invalid, return errors and keep the old session ID if there was one.    
    if input_validated == False:
        return return_message, "danger", True, True, "", previous_request

# Submit computation request to the backend.
@app.callback(
    Output("completed", "children"),
    Output("completed", "color"),
    Output("completed", "is_open"),
    State("email_address", "value"),
    State("data-type", "value"),
    State("model-selection", "value"),
    State("upload_test_data", "contents"),
    State("upload_test_data", "filename"),
    State("upload_adapt_data", "contents"),
    State("upload_adapt_data", "filename"),
    Input("session_id", "data"),
    prevent_initial_call=True,
)
def update_output(email_address, data_type, model_selection, test_contents, test_filename,
                  adapt_contents, adapt_filename, session_id):
    
    # Computation only happens when there is a session ID - a new session ID or else it would've failed during input validation.
    if session_id != "":
        test_data_pd = parse_contents(test_contents, test_filename)
        adapt_data_pd = parse_contents(adapt_contents, adapt_filename)
        # Container session path
        session_path = os.path.join("sessions", session_id).replace("\\","/")
        os.mkdir(session_path)

        # Prepare data for uploading
        test_path = os.path.join(session_path, "test.pkl").replace("\\","/")
        adapt_path = os.path.join(session_path, "adapt.pkl").replace("\\","/")
        test_data_pd.to_pickle(test_path)
        adapt_data_pd.to_pickle(adapt_path)

        username = os.environ['MYUSER'] #"piebar@mentat004.dccn.nl"
        projectdir = os.environ['PROJECTDIR'] #"/project_cephfs/3022051.01"
        scriptdir = os.environ['SCRIPTDIR'] #"test_scripts/server"
        executefile = os.environ['EXECUTEFILE']#"execute_modelling.sh"#
        model_dir = os.environ['MODELS']
        python_env = os.environ['PYTHON_ENV']
        # Upload the data to the server.
        remote_session_dir = os.path.join(projectdir, "sessions", session_id).replace("\\","/")
        scp = 'ssh -o "StrictHostKeyChecking=no" {username} mkdir -p {remote_session_dir} && scp -o "StrictHostKeyChecking=no" {test} {adapt} {username}:{remote_session_dir}'.format(username = username, remote_session_dir = remote_session_dir, test=test_path, adapt=adapt_path)
        subprocess.call(scp, shell=True)
        
        # Remove the temporary session data in the container.
        remove_temp_session = 'rm -r {session_path}'.format(session_path = session_path)
        subprocess.call(remove_temp_session, shell=True)
        # TO-DO: remove algorithm arg as clean up
        algorithm = model_selection.split("_")[0]

        # Submit computation request with all the collected user input.
        bash_path = os.path.join(projectdir, scriptdir, executefile).replace("\\","/") 
        stderr = os.path.join(projectdir, "sessions", session_id, "main_job_error.txt")
        stdout = os.path.join(projectdir, "sessions", session_id, "main_job_output.txt")
        
        execute = "ssh -o 'StrictHostKeyChecking=no' {user} 'sbatch --time=23:00:00 --mem=4G --output={stdout} --error={stderr} --wrap=\"{bash_path} {projectdir} {model_selection} {data_type} {session_id} {model_dir} {email_address}  {python_env}\"'".format(
            user=username,
            bash_path=bash_path,
            projectdir=projectdir,
            model_selection=model_selection,
            data_type=data_type,
            session_id=session_id,
            model_dir=model_dir,
            email_address=email_address,
            stderr=stderr,
            stdout=stdout,
            python_env=python_env
        )
        subprocess.call(execute, shell=True)

        finished_message = "Your request has successfully been submitted with session ID: {session_id}.\nYou should receive results in your inbox the coming hour(s).".format(session_id=session_id)
        return finished_message, "success", True
    else: return no_update, no_update, no_update

# Currently all input is converted to pandas. Might need to change if we allow cifti and nifti input.
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        # potential extension of allowed data types
        # elif 'xls' in filename:
        #     # Assume that the user uploaded an excel file
        #     df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return df

# List file names of uploaded test data.
@app.callback(
    Output("list-test-fname", "children"),
    Input("upload_test_data", "filename"),
    prevent_initial_call=True,
)
def list_test_file(test_fname):
    return [html.Br(), html.Li(test_fname)]

# List file names of uploaded adaptation data.
@app.callback(
    Output("list-adapt-fname", "children"),
    Input("upload_adapt_data", "filename"),
    prevent_initial_call=True,
)
def list_adapt_file(adapt_fname):
    return [html.Br(), html.Li(adapt_fname)]

# Serve the app upon running the script.
if __name__ == '__main__':
    app.run_server()#debug=True
