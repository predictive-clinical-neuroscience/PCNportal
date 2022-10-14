# Created by: Pieter Barkema
# Date: February, 2022
# Description:
#    Users can access this online app to process their neuroimaging date
#    with normative modelling. It should return visualizations 
#    and results to users accessing from all over the world, 
#    It is hosted as a website from a remote gunicorn server.

# python code for sshing into mentat
#        cmd = 'plink mentat004.dccn.nl -l piebar -pw "mypassword"'
        # retcode = subprocess.call(cmd,shell=True)
        # os.chdir("")

from dash import Dash, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
from subprocess import PIPE, Popen, run, call, check_output
from flask import Flask
#import os, sys
import io, os, base64

# Create a flask server
server = Flask(__name__)
# Create  Dash app
app = Dash(server=server, external_stylesheets=[dbc.themes.MATERIA]) #

def retrieve_options(data_type=None):
    import ast
    # can be models or models/data_type
    chosen_dir = "models"
    if data_type is not None:
        chosen_dir = os.path.join("models", data_type)
    username = os.environ['MYUSER']
    py_script = os.path.join(os.environ['PROJECTDIR'], "test_scripts", "server", "list_subdirs.py")
    print(f'{username, py_script}')
    list_dirs = ["ssh", "-o", "StrictHostKeyChecking=no", username, "python", py_script, str(chosen_dir)]
    # ssh -o StrictHostKeyChecking=no ***REMOVED*** python ***REMOVED***/list_subdirs.py "models"
    #test ssh: ["ssh", "-o", "StrictHostKeyChecking=no", "***REMOVED***", "python", "***REMOVED***/list_subdirs.py", "models"]#
    p = Popen(list_dirs, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, err = p.communicate()
    # is this helpful? gives the return code of the command
    # rc = p.returncode
    # strip, to get rid of (/n)
    
    byte_to_string = str(output, encoding='UTF-8').strip()
    print(f'{byte_to_string}')
    string_to_list = ast.literal_eval(byte_to_string)

    return string_to_list

# -----------------------------------------------------------------
# The entire contents of the app.
app.layout = html.Div([
    dbc.Col(
    dcc.Tabs([
        dcc.Tab(label='Home', children=[
            html.Br(),
            html.Div(
                
                dcc.Markdown('''

                ### Fuss-free normative modelling

                The [Predictive Clinical Neuroscience](https://predictiveclinicalneuroscience.com/) group at the Donders Institute and RadboudUMC 
                develops statistical and machine learning techniques 
                to predict and stratify brain disorders on the basis of neuroimaging data.

                Case-control studies are not sufficient to understand brain dysfunction, due to the large clinical heterogeneity.
                Normative models are a highly effective way to deal with this individual variability, and
                can be developed using our [PCNtoolkit](https://github.com/amarquand/PCNtoolkit); a highly flexible framework that accounts for site effects
                and only requires knowledge of basic Python programming. Nevertheless, developing normative models
                takes considerable technical and computational resources. Moreover, normative models, like all
                big data models, are most effective when trained on huge neuroimaging data sets - a constraint for scientists.

                We developed this website to make it trivial to use pre-trained normative models (see 'Model information'), trained on 10.000s of neuroimages from many different sites.
                Scientists can now make use of these models in a few clicks (see 'Modelling'), requiring no technical background or compute power, and only a data set of choice. 
                With minimal effort, you can find out how abnormal your IDPs are across covariates, such as age and gender.
                
                Happy modelling!

                Learn more about normative modelling, and how to develop your own models with PCNtoolkit [here](https://pcntoolkit.readthedocs.io/en/latest/pages/pcntoolkit_background.html).

                
                __Disclaimer:__ this application is GDPR compliant. By submitting your data on our website, you give permission to process your data.
                Data will be removed from our system within 30 days, as per EU regulations. The normative models should purely be used for scientific investigations and explorations,
                and have not been approved for clinical applications, although this is a future goal.

            ''', link_target="_blank"), style={'margin':'auto','width':"80%"}
            )
        ]),
        dcc.Tab(label='How to Model', children=[
            html.Br(),
            html.Div(
                
                dcc.Markdown('''

                ### How to turn data into z-scores
                - First take a look at the provided template for both adaptation and test data.
                - Then, go to the 'Compute here!' tab and select the data type you'll be using.
                - You can now select one of the available models for this data type (described in 'Model information')
                - Upload your adaptation and test data in the right boxes.
                - Enter the email address where you would like to receive your downloadable results.
                - Press submit!

                
            ''', link_target="_blank"), style={'margin':'auto','width':"80%"}
            )
        ]
        ),
        dcc.Tab(label='Model information', children=[
            html.Br(),
            html.Div(
                dcc.Markdown(
                            '''
                ## Available models

                Please find below information on published models (with references) and unpublished models.

                #### Published models

                * (Example) Rutherford et al (eLife, 2022): a Bayesian Linear Regression model trained on n MRI scans.

                #### Unpublished models

                Unpublished models make use of Bayesian Linear Regression and Hierarchical Bayesian Regression. \n
                The model names contain information of their learning configurations, and can be understood as alg_sample_etc, where:
                * alg = algorithm
                * sample = training sample
            ''', style={'margin':'auto','width':"80%"}
            )
            )

        ]),
        dcc.Tab(label='Compute here!', id='modelling',
        
        children=[
            html.Div(children=[
            
                # -----------------------------------------------------------------
                html.Br(),
                html.Label('Data type'),
                dcc.Dropdown(options = retrieve_options(), id='data-type'), # For styling commented: retrieve_options()
                
                html.Br(),
                html.Label('Normative Model'),
                dcc.Dropdown( options = ['please select data type first'], value = 'please select data type first', id='model-selection'),
                dcc.Markdown(id="model-readme"), 
                html.Br(),
                html.Label('Select data format'),
                dcc.Dropdown(['.csv'], '.csv'), #['.csv', 'NIFTI', '[other formats]']

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
                , id= 'Upl_1'
                ),             
                # List the uploaded data file(s)
                html.Ul(id="list-data-file"),
                
                html.Hr(),
                dcc.Upload(html.A('Upload adaptation data')),
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
                , id= 'Upl_2'
                ),
                # List the uploaded covariate file(s)
                html.Ul(id="list-cov-file"),            
                html.Br(),
                html.Label('Email address for results: '),
                html.Br(),
                dcc.Input(value='pieter.barkema@donders.ru.nl', type='text', id='email_address', style={'width':'30%'}),         
                # -----------------------------------------------------------------
                # The data submission and results retrieval section
                html.Div(
                    children=[
                        # -----------------------------------------------------------------
                        # Check lists with all options to control results output
                        dcc.Checklist(className ='checkbox_1',
                                    style={'margin-right': '0%'},
                                    options=[
                                        {'label': 'raw data', 'value': 'I1ST2', 'disabled': True},
                                        {'label': 'raw data', 'value': 'I2ST2', 'disabled': True},
                                        {'label': 'raw data', 'value': 'I3ST2', 'disabled': True},
                                        {'label': 'raw data', 'value': 'I4ST2', 'disabled': True}
                                            ],
                                    value=['I1ST2'],
                                    labelStyle = {'display': 'block'}
                                            ),
                        dcc.Checklist(className ='checkbox_2',
                                    style={'margin-right': '0%'},
                                    options=[
                                        {'label': 'visualization', 'value': 'I1MT', 'disabled': True},
                                        {'label': 'visualization', 'value': 'I2MT', 'disabled': True},
                                        {'label': 'visualization', 'value': 'I3MT', 'disabled': True},
                                        {'label': 'visualization', 'value': 'I4MT', 'disabled': True}
                                        ],
                                    value=[],
                                    labelStyle = {'display': 'block'}
                                            ),
                        dcc.Checklist(className ='checkbox_3',
                                    style={'margin-right': '0%'},
                                options=[
                                    {'label': 'z-score brain space', 'value': 'I1ST1', 'disabled': True},
                                    {'label': 'Centile plots', 'value': 'I2ST1', 'disabled': True},
                                    {'label': 'Exp. Var. plots', 'value': 'I3ST1', 'disabled': True},
                                    {'label': '[other error measures]', 'value': 'I4ST1', 'disabled': True}
                                        ],
                                value=['I1ST1'],
                                labelStyle = {'display': 'block'}
                                        ),
                        html.Div(
                            style={'float':'right'},
                            children=[
                                html.Button("Submit", id="btn_csv"),
                                #html.Plaintext(id="submitted"),

                                # To-do: make it downloadable onclick. this works together with disable_download also commented out.
                                # Download your predictions in .csv format!
                                #html.Button("Download", id="results_onclick", disabled=True),
                                # Store the results files so they can be downloaded on click, not instantly
                                #dcc.Store(id="csv_store_session", storage_type="session"),
                                #dcc.Download(id="download-dataframe-csv")
                            ]
                        )
                        ]
                    , style={'float': 'right', 'display':'flex'}
                    ),
                
                    html.Div(
                        style={'float':'right'},
                        children=[
                            html.Plaintext(id="submitted")
                        ]
                            
                        
                    )
            ], style={'margin':'auto','width':'80%','padding': 10, 'flex': 1}),
        ])
    ])
    )
    ,
    html.Div(
        style={'padding':'5%','position': 'absolute', 'left': '75%', 'top': '100%'},#'width': '5%', 'height': '5%', 
        children=[
            html.Img(src='assets/wellcome_logo.png', alt='image', style={'float': 'right', 'padding': '2%','height':'50%', 'width':'50%'}),
            html.Img(src='assets/erc_logo.png', alt='image', style={'float': 'right','padding': '2%','height':'50%', 'width':'50%'}),
            html.Br(),
            html.Img(src='assets/donders_logo.png', alt='image', style={'float': 'right','padding': '2%','height':'70%', 'width':'70%'}),
            html.Img(src='assets/pcn_logo.png', alt='image', style={'float': 'right','padding': '2%','height':'70%', 'width':'70%'})
        ]
    )
], style={'display': 'flex', 'flex-direction': 'row', 'height': '80%', 'width': '60%', 'position': 'relative', 'top':'40%', 'left':'20%' })
# -----------------------------------------------------------------
# Functions that handle input and output for the Dash components.

@app.callback(
    Output(component_id='model-readme', component_property='children'),
    [Input(component_id='model-selection', component_property='value')],
    prevent_initial_call=True
)
def model_information(model_selection):
    with open('assets/README.md', 'r') as mdfile:
        readme = mdfile.readlines()
        return readme


# Function to restrict model choice based on data type choice
@app.callback(
    Output(component_id='model-selection', component_property='options'),
    [Input(component_id='data-type', component_property='value')],
    prevent_initial_call=True
)
def update_dp(data_type):
    # TO-DO: link model names to available models in directory.

    # Get models based on data type subdir, pseudocode:
    # model_choice_list = get_available_models(data_type)
    # if data_type == 'Brain surface area':
    #     # here we could put a df with all available models
    #     model_selection_list = ['BSA blr', 'BSA hbr']
    # if data_type == 'Average Thickness':
    #     model_selection_list = ['AT blr', 'AT hbr']
    model_selection_list = retrieve_options(data_type)
    return model_selection_list

# Load data into the model and store the .csv results on the website.
@app.callback(
    Output("submitted", "children"),
    State("email_address", "value"),
    State("data-type", "value"),
    State("model-selection", "value"),
    State("Upl_1", "contents"),
    State("Upl_1", "filename"),
    State('Upl_1', 'last_modified'),
    State("Upl_2", "contents"),
    State("Upl_2", "filename"),
    State('Upl_2', 'last_modified'),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True
)
def update_output(email_address, data_type_dir, model_name, contents_test, name_test, date_test, 
                  contents_adapt, name_adapt, date_adapt, clicks):
    import subprocess
    # TO-DO this if could use an 'else'. We can do data checking here too. 
    if contents_test is not None and contents_adapt is not None:
        # Convert input csv data to pandas
        test_data_pd = parse_contents(contents_test, name_test, date_test)
        adapt_data_pd = parse_contents(contents_adapt, name_adapt, date_adapt)
        # Remote working_dir
        import os, base64, uuid
        session_id = str(uuid.uuid4()).replace("-", "")
        session_path = os.path.join("sessions", session_id)
        os.mkdir(session_id)

        #session_id = "session_id" + str(random.randint(100000,999999))
        test_path = os.path.join(session_path, "/test.pkl")
        adapt_path = os.path.join(session_path, "/adapt.pkl")
        test_data_pd.to_pickle(test_path)
        adapt_data_pd.to_pickle(adapt_path)
        
        # execute a bash script that qsubs an apply_model to the cluster
        # create random session integer as name
        
        # project_folder, can hardcode this in bash script
        # project_dir = "***REMOVED***"
        #model_choice_path = os.path.join(models_dir, data_type_path, model_name)
        # start restructuring dirs here!
        
        #idp_dir = os.path.join(session_dir, "idp_results")
        # create session dir and transfer data there
        username = os.environ['MYUSER']
        projectdir = os.environ['PROJECTDIR']
        executefile = os.environ['EXECUTEFILE']
        #removed /idp_results from {session_dir}
        session_dir = os.path.join(projectdir, "sessions", session_id)
        scp = """ssh -oStrictHostKeyChecking=no {user} mkdir -p {session_dir} && 
        scp -oStrictHostKeyChecking=no {test} {adapt} {user}:{session_dir}""".format(user = username, session_dir = session_dir, test=test_path, adapt=adapt_path)
        subprocess.call(scp, shell=True)
        algorithm = model_name.split("_")[0]
        # os path join does something strange with attaching two paths
        bash_path = os.path.join(projectdir, executefile).replace("\\","/")
        execute = 'ssh -oStrictHostKeyChecking=no {user} {bash_path} {projectdir} {model_name} {data_type_dir} {session_id} {algorithm} {email_address}'.format(user=username, bash_path=bash_path, projectdir = projectdir, model_name=model_name, data_type_dir = data_type_dir, session_id=session_id, algorithm=algorithm, email_address = email_address) 
        #subprocess.call(execute, shell=True)

        finished_message = "Your computation request has been sent!"

        return finished_message

# Convert input .csv to pandas dataframe
# TO-DO: scp could be here as well, we don't really need dataframe of the input data
def parse_contents(contents, filename, date):
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
# Download the results with a button.
@app.callback(
    Output("download-dataframe-csv", "data"),
    State("csv_store_session","data"),
    Input("results_onclick", "n_clicks")
)
def download_results(results_csv, clicks):
    return results_csv

# List uploaded data files (1)
@app.callback(
    Output("list-data-file", "children"),
    Input("Upl_1", "filename"),
    prevent_initial_call=True,
)

def list_data_file(data_name):
    return html.Li(data_name) 

# List uploaded data files (2)
@app.callback(
    Output("list-cov-file", "children"),
    Input("Upl_2", "filename"),
    prevent_initial_call=True,
)
def list_cov_file(cov_name):
    return html.Li(cov_name) 

# Serve the app upon running the script.
if __name__ == '__main__':
    app.run_server(debug=True)