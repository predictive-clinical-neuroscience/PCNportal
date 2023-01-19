# Created by: Pieter Barkema
# Date: February, 2022
# Description:
#    Users can access this online app to process their neuroimaging date
#    with normative modelling. It should return visualizations 
#    and results to users accessing from all over the world, 
#    It is hosted as a website from a remote gunicorn server.


from dash import Dash, html, dcc, Input, Output, State, no_update
import dash_bootstrap_components as dbc
from dash_extensions.enrich import MultiplexerTransform, DashProxy
from dash.exceptions import PreventUpdate
import pandas as pd
from subprocess import PIPE, Popen, run, call, check_output
from flask import Flask
#import os, sys
import io, os, base64

# Create a flask server
server = Flask(__name__)
# Create  Dash app
app = DashProxy(server=server, external_stylesheets=[dbc.themes.MATERIA], 
                title='PCNportal', update_title=None,transforms=[MultiplexerTransform()])
#app.title="PCNportal"

def retrieve_options(data_type=None):
    import ast
    # can be models or models/data_type
    chosen_dir = "models"
    if data_type is not None:
        chosen_dir = os.path.join("models", data_type)
    py_script = os.path.join(os.environ['PROJECTDIR'], os.environ['SCRIPTDIR'], os.environ['LISTDIR'])

    list_dirs = ["ssh", "-o", "StrictHostKeyChecking=no", os.environ['MYUSER'], "python", py_script, str(chosen_dir)]
    # ssh -o StrictHostKeyChecking=no ***REMOVED*** python ***REMOVED***/list_subdirs.py "models"
    #test ssh: ["ssh", "-o", "StrictHostKeyChecking=no", "***REMOVED***", "python", "***REMOVED***/list_subdirs.py", "models"]#
    p = Popen(list_dirs, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    # is this helpful? gives the return code of the command
    # rc = p.returncode
    # strip, to get rid of (/n)
    
    byte_to_string = str(output, encoding='UTF-8').strip()
    string_to_list = ast.literal_eval(byte_to_string)

    return string_to_list

# -----------------------------------------------------------------
# The entire contents of the app.
app.layout = html.Div([ 
    html.Div([
    dbc.Col(
    dcc.Tabs([
        #!["A pretty tiger"](https://github.com/predictive-clinical-neuroscience/braincharts/blob/master/docs/image_files/ThickAvg_BLR_lifespan_age.png?raw=true)
        dcc.Tab(label='Home', children=[
            html.Br(),
            html.Div(
                dcc.Markdown(id='home-readme', link_target="_blank", dangerously_allow_html=True), style={'margin':'auto','width':"80%"}
            )
        ]),
        dcc.Tab(label='How to model', children=[
            html.Br(),
            html.Div(
                dcc.Markdown(id="howto-readme", link_target="_blank",), style={'margin':'auto','width':"80%"}
            )
        ]
        ),
        dcc.Tab(label='Model information', children=[
            html.Br(),
            html.Div(
                dcc.Markdown(id="modelinfo-readme", link_target="_blank",), style={'margin':'auto','width':"80%"},
                
            )
            
        ]),
        dcc.Tab(label='Compute here!', id='modelling',
        
        children=[
            html.Div(children=[
            
                # -----------------------------------------------------------------
                dcc.Store(id='session_id', data=""),
                dcc.Store(id='previous_request', data=[]),
                dcc.Store(id="download_template", data=""),
                dcc.Store(id="covariate_names", data=[]),
                #dcc.Store(id='submit_bool', data='False'),
                html.Br(),
                html.Label('Data type'),
                dcc.Dropdown(options = retrieve_options(), id='data-type'), # For styling commented: 
                
                html.Br(),
                html.Label('Normative Model'),
                dcc.Dropdown(['please select data type first...'], 'please select data type first...', id='model-selection'), #"please select data type first..."
                html.Br(),
                dcc.Markdown(id="model-readme", link_target="_blank", dangerously_allow_html=True), 
                html.Br(),
                html.Label('Select data file format'),
                dcc.Dropdown(['.csv'], '.csv', id='file-format'), #['.csv', 'NIFTI', '[other formats]']

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
                }
                , id= 'upload_test_data'
                , max_size= 1000000000 #1 GB
                ),             
                # List the uploaded data file(s)
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
                }
                , id= 'upload_adapt_data'
                , max_size= 1000000000 #1 GB
                ),
                # List the uploaded covariate file(s)
                html.P(id="list-adapt-fname"),            
                html.Br(),
                html.Label('Email address for results: '),
                html.Br(),
                dcc.Input(value='', type='text', id='email_address', style={'width':'40%'}),         
                # -----------------------------------------------------------------
                # The data submission and results retrieval section
                html.Div(
                    children=[
                        # -----------------------------------------------------------------
                        # Check lists with all options to control results output
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
                            dbc.Alert(id="loading_or_error", is_open=False,
                            children="Your computation request is being submitted..."),
                            dbc.Alert(id="completed", is_open=False, color='success'),
                            html.Br(),
                        ]
                        
                       ),

            ], style={'margin':'auto', 'width':'75%', 'flex': 1}),
        ]),
    
    ])#, style={'padding': '5%'}),
    )
    ,
    html.Div(
        style={'padding':'1%','position': 'absolute', 'left': '85%', 'top': '100%'},#'width': '5%', 'height': '5%', 
        children=[
            html.Img(id="load-readme-trigger",src='assets/merged_images.png', alt='image', style={'float': 'right', 'padding': '0%','height':'130%', 'width':'130%'}),
        ]
    )
], className="myDiv", style={'font-size':'small','display': 'flex', 'flex-direction': 'row', 'height': '40%', 'width': '50%', 'position': 'relative', 'top':'40%', 'left':'25%', 'backgroundColor':'white'})#, 'opacity':'1.00
])#, style={'backgroundColor':'blue'}
# -----------------------------------------------------------------
# Functions that handle input and output for the Dash components.

@app.callback(
    Output(component_id='home-readme', component_property='children'),
    Output(component_id='howto-readme', component_property='children'),
    Output(component_id='modelinfo-readme', component_property='children'),
    Input(component_id='load-readme-trigger', component_property='children'),
    prevent_initial_call=False
)
def load_tabs_markdown(load_readme_trigger):
    with open('assets/home.md', 'r') as mdfile:
        home = mdfile.readlines()
    with open('assets/howto.md', 'r') as mdfile:
        howto = mdfile.readlines()
    with open('assets/modelinfo.md', 'r') as mdfile:
        modelinfo = mdfile.readlines()
    return home, howto, modelinfo

# Function for writing out model information markdown files
@app.callback(
    Output(component_id='model-readme', component_property='children'),
    Output(component_id='download_template', component_property='data'),
    Output(component_id='covariate_names', component_property='data'),
    Input(component_id='model-selection', component_property='value'),
    State(component_id='data-type', component_property='value'),
    prevent_initial_call=True
)
def model_information(model_selection, data_type):
    if model_selection != 'please select data type first...' and model_selection != 'Select...' and model_selection != "":
        projectdir = os.environ['PROJECTDIR']
        username = os.environ['MYUSER']
        model_path = os.path.join(projectdir, "models", data_type, model_selection) 
        readme_path = os.path.join(model_path,"README.md")
        #untested, what path is this? 
        covs_path = os.path.join(model_path, "mandatory_columns.txt") 
        # ssh -o StrictHostKeyChecking=no ***REMOVED*** cat ***REMOVED***/models/ThickAvg/BLR_lifespan_57K_82sites/test_README.md

        cat_readme = ["ssh", "-o", "StrictHostKeyChecking=no", username, "cat", readme_path]
        cat_model_covs = ["ssh", "-o", "StrictHostKeyChecking=no", username, "cat", covs_path]
        p = Popen(cat_readme, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, _ = p.communicate()
        byte_to_string = str(output, encoding='UTF-8')#.strip()
        import re
        #print(f'{byte_to_string=}')
        download_pattern = r"\[Download\]\((.+)\)"
        #split_lines = byte_to_string.splitlines
        # First line that speaks of covariates
        # cov_line = [line for line in split_lines if line.contains("covariates = ")][0]
        #cov_line = cov_line.remove("covariates = ")
        #covariate_lines = re.sub("[\(\[].*?[\)\]]", "", cov_line)
        #covariate_names = re.search(byte_to_string)
        #= "[Download](https://drive.google.com/uc?export=download&id=16QhWrAh2hQOMM2tx62VQDtvGKIkx3DnX)"
        download_link = re.search(download_pattern, byte_to_string).group(1)
        
        # get mandatory covs
        p = Popen(cat_model_covs, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, _ = p.communicate()
        cov_byte_to_string = str(output, encoding='UTF-8')
        # TO-DO: this needs a covariate file to parse first!
        covariate_names = cov_byte_to_string.splitlines()
        return byte_to_string, download_link, covariate_names
    else: return no_update, no_update, no_update
    #***REMOVED***/models/ThickAvg/BLR_lifespan_57K_82sites/test_README.md

# Function to restrict model choice based on data type choice
@app.callback(
    Output(component_id='model-selection', component_property='options'),
    [Input(component_id='data-type', component_property='value')],
    prevent_initial_call=True
)
def update_dp(data_type):
    model_selection_list = retrieve_options(data_type)
    return model_selection_list


# Check if all input fields are valid
def input_checker(covariate_names, download_template, current_request, previous_request, email_address, data_type, model_selection, test_contents, test_filename, adapt_contents, adapt_filename, file_format):
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
    elif current_request == previous_request:
        input_validated = False
        return_message = "You've already submitted this request."
    # check for data type
    else: 
        # check idp name matching
        import pandas as pd
        # remove unnamed columns
        test_data_columns = parse_contents(test_contents, test_filename).columns
        adapt_data_columns = parse_contents(adapt_contents, adapt_filename).columns
        goal_columns = pd.read_csv(download_template)
        # make sure covariates are mandatory
        # is it known what covariates a model is trained on?
        # else, get rid of this feature, just provide a general column checker without covariate removal or checking.
        mandatory_columns = covariate_names
        # remove unnamed column and mandatory columns to count if any features are provided
        goal_columns = goal_columns.drop(goal_columns.filter(regex="Unname"),axis=1)
        goal_columns = goal_columns.drop(mandatory_columns, axis=1).columns
        
        # check for mandatory columns, such as covariates or batch effects
        for col in mandatory_columns:
            if col not in test_data_columns or col not in adapt_data_columns:
                return False, "You are missing some or all of the following mandatory columns (batch effects or covariates) in your data sets: " + ", ".join(mandatory_columns) + ". "
        
        return_message = [return_message, "Your data set has all the necessary covariates for this model.", html.Br()]
        test_data_matches = goal_columns.intersection(test_data_columns).size
        adapt_data_matches = goal_columns.intersection(adapt_data_columns).size
        return_message = return_message +  [str(goal_columns.difference(adapt_data_columns))] + ["Amount of adaptation features that match the model template: ", str(adapt_data_matches), " out of ", str(goal_columns.size), ". ", html.Br()] #[str(goal_columns.intersection(adapt_data_columns))] + 
        return_message = return_message + ["Amount of test features that match the model template: ", str(test_data_matches), " out of ", str(goal_columns.size), ". ", html.Br()]
        input_validated = True
        if test_data_matches < 1:
            input_validated = False
            return_message = "Your test data has no feature matches with the model's data template. "
        if adapt_data_matches < 1:
            input_validated = False
            return_message = return_message + "Your adaptation data has no feature matches with the model's data template. "
    return input_validated, return_message

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
    State("download_template", "data"),
    State("covariate_names", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def display_alert(email_address, data_type, model_selection, test_contents, test_filename, adapt_contents, adapt_filename, previous_request, file_format,download_template, covariate_names, click):
    current_request = [email_address, data_type, model_selection, test_filename, adapt_filename, file_format]
    input_validated, return_message = input_checker(covariate_names, download_template, current_request, previous_request, email_address, data_type, model_selection, test_contents, test_filename, adapt_contents, adapt_filename, file_format)
    
    if input_validated == True:
        import os, base64, uuid
        session_id = str(uuid.uuid4()).replace("-", "")
        return_message = return_message + ["Your request is being processed with session ID: " + session_id]
        
        return return_message, "light", True, True, session_id, current_request
    if input_validated == False:
        return return_message, "danger", True, True, "", previous_request

# Load data into the model and store the .csv results on the website.
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
    
    if session_id != "":
        import subprocess
        # Convert input csv data to pandas
        test_data_pd = parse_contents(test_contents, test_filename)
        adapt_data_pd = parse_contents(adapt_contents, adapt_filename)
        # Remote working_dir

        session_path = os.path.join("sessions", session_id).replace("\\","/")
        os.mkdir(session_path)

        #session_id = "session_id" + str(random.randint(100000,999999))
        test_path = os.path.join(session_path, "test.pkl").replace("\\","/")
        adapt_path = os.path.join(session_path, "adapt.pkl").replace("\\","/")
        test_data_pd.to_pickle(test_path)
        adapt_data_pd.to_pickle(adapt_path)
        
        # execute a bash script that qsubs an apply_model to the cluster
        # create random session integer as name
        
        # project_folder, can hardcode this in bash script
        # project_dir = "***REMOVED***"
        #model_choice_path = os.path.join(models_dir, data_type_path, model_selection)
        # start restructuring dirs here!
        
        #idp_dir = os.path.join(session_dir, "idp_results")
        # create session dir and transfer data there
        username = os.environ['MYUSER'] #"***REMOVED***"
        projectdir = os.environ['PROJECTDIR'] #"***REMOVED***"
        scriptdir = os.environ['SCRIPTDIR'] #"***REMOVED***"
        executefile = os.environ['EXECUTEFILE']#"execute_modelling.sh"#
        #removed /idp_results from {session_dir}
        remote_session_dir = os.path.join(projectdir, "sessions", session_id).replace("\\","/")
        scp = 'ssh -o "StrictHostKeyChecking=no" {username} mkdir -p {remote_session_dir} && scp -o "StrictHostKeyChecking=no" {test} {adapt} {username}:{remote_session_dir}'.format(username = username, remote_session_dir = remote_session_dir, test=test_path, adapt=adapt_path)
        finished_message = "We completed your request with session ID: {session_id}".format(session_id=session_id)
        #print(f'{session_path=}')
        remove_temp_session = 'rm -r {session_path}'.format(session_path = session_path)
        subprocess.call(scp, shell=True)
        subprocess.call(remove_temp_session, shell=True)
        algorithm = model_selection.split("_")[0]
        # os path join does something strange with attaching two paths
        bash_path = os.path.join(projectdir, scriptdir, executefile).replace("\\","/") 
        execute = 'ssh -o "StrictHostKeyChecking=no" {user} {bash_path} {projectdir} {model_selection} {data_type} {session_id} {algorithm} {email_address}'.format(user=username, bash_path=bash_path, projectdir = projectdir, model_selection=model_selection, data_type = data_type, session_id=session_id, algorithm=algorithm, email_address = email_address) 
        subprocess.call(execute, shell=True)
    
        return finished_message, "success", True
    else: return no_update, no_update, no_update

# Convert input .csv to pandas dataframe
# TO-DO: scp could be here as well, we don't really need dataframe of the input data
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        # elif 'xls' in filename:
        #     # Assume that the user uploaded an excel file
        #     df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return df

# List uploaded test data files
@app.callback(
    Output("list-test-fname", "children"),
    Input("upload_test_data", "filename"),
    prevent_initial_call=True,
)
def list_test_file(test_fname):
    return [html.Br(), html.Li(test_fname)]


# List uploaded adaptation data files
@app.callback(
    Output("list-adapt-fname", "children"),
    Input("upload_adapt_data", "filename"),
    prevent_initial_call=True,
)
def list_adapt_file(adapt_fname):
    return [html.Br(), html.Li(adapt_fname)]

# Serve the app upon running the script.
if __name__ == '__main__':
    app.run_server(debug=True)