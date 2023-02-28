[PCNportal](https://pcnportal.dccn.nl/) is a website that facilitates access to modelling with finetuned normative models for neuroimaging analysis that are pre-trained and applied with the Python package [PCNtoolkit](https://pcntoolkit.readthedocs.io/en/latest/). Normative modelling is increasingly in demand to analyze the differences between individual brains in neuroimaging and neuropsychiatry.

This GitHub contains the client side and server side code for the PCNportal project. The client side contains code to facilitate the GUI and website service, while the server side code contains functionality to model with PCNtoolkit on a remote server and share results.

Please refer to the GitHub [Wiki](https://github.com/predictive-clinical-neuroscience/PCNportal/wiki) to learn more about the implementation and development pipeline of the website, also containing tutorials and a demo.

## Using the website

The latest version of the website is available at https://pcnportal.dccn.nl/ and provides all instructions necessary to start modelling and explains how to use the results. Only a data set of supported models is needed to get started, but we also provide data to run a demo under the tab 'How to model'.

## Features

PCNportal provides a user-friendly lightweight GUI, but also adds functionality to PCNtoolkit. 

The website:
- hosts resources to learn about normative modelling in theory and practice,
- dynamically updates available models and model-specific information,
- checks data for errors and provides feedback,
- shares results through a public server and an automated email service,
- hosts data on secure Institute servers and cleans up data older than thirty days to comply with privacy guidelines,
- automatically runs, checks and manages parallelized computation jobs.

## Testing & Installation

Testing the website's functionality can be done through modelling with demo data, as can be found on the website under 'How to Model' (but also available in the Wiki's client side page). More demo data can be found in [PCNportal/client/docs](https://github.com/predictive-clinical-neuroscience/PCNportal/tree/main/client/docs).

To locally deploy the GUI without modelling functionality, please follow these instructions. You will first need to install [Docker](https://docs.docker.com/get-docker/), and then:
* Open up cmd and clone the GitHub repository with 
  ~~~
  git clone https://github.com/predictive-clinical-neuroscience/PCNportal.git
  ~~~
* Then go to the PCNportal/client/ subdirectory of your local repository clone.
* First build your image with:
  ~~~ 
  docker-compose build
  ~~~
* Then, to run the application use: 
  ~~~
  docker-compose up
  ~~~ 
* Access the GUI at localhost:5000 (e.g.: http://127.0.0.1:5000/). Another port can be specified in docker-compose.override.yml.
* Please make sure entrypoint.sh has LF line endings. CRLF Windows line endings will prevent a succesful run.

The latest version of the image is publically hosted at [DockerHub](https://hub.docker.com/repository/docker/ifdevdocker/pcnonlinedev/general).

During this process, the dependencies for PCNportal will be installed as provided in [requirements.txt](https://github.com/predictive-clinical-neuroscience/PCNportal/blob/main/client/requirements.txt).

To test the backend modelling functionality, please refer to PCNtoolkit [tutorials](https://pcntoolkit.readthedocs.io/en/latest/pages/normative_modelling_walkthrough.html) and corresponding documentation.

## Network diagram

PCNportal is a client-server application that combines the functionality of an easy GUI with that of heavy duty parallelized computation of the backend. We use various services, such as [Flask](https://flask.palletsprojects.com/en/2.2.x/), [Docker](https://www.docker.com/), [gunicorn](https://gunicorn.org/), [Gmail](https://developers.google.com/gmail/api/guides), [SURFdrive](surfdrive.surf.nl) and [TORQUE](https://wiki.archlinux.org/title/TORQUE) to accomplish this. A sketch of our network diagram:

![Pipeline PCNportal](https://user-images.githubusercontent.com/39303377/220601095-5e27b7fe-a9d4-491e-88f9-f4f3db3a59ad.png) 

## Assistance
To report bugs or issues or if you have any questions or feature requests, please use our [Gitter](https://gitter.im/PCNportal/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge).

## Contributions
Contributions of models are accepted and encouraged by PCNportal. Models trained with PCNtoolkit can be added instantly after adapting the standard directory structure. 

Example:  
<img width="166" alt="image" src="https://user-images.githubusercontent.com/39303377/220667045-60502ea0-308c-4b5a-9a07-c74a979f518f.png">

'Models' contains all models with naming convention NM\_0\_\{x\}\_fit.pkl where _x_ is the model number corresponding to the order of idp ids.
The features that were used in training should be saved in 'idp_ids.txt', the names of data collection sites in 'site_ids.txt', the names of mandatory columns (covariates and site effects) in 'mandatory_columns.txt'. All strings should be separated with return ('\n'). Any information about the model and how its trained (including hyperparameters) should be provided in the 'README.md', along with a data template link that follows the syntax: _\[Download\]\(download_link\)_.

Models not trained with PCNtoolkit can be accepted when a Python script is provided for transfer learning. Please contact us on Gitter to discuss such options.

Models will be tested by experts before being hosted on the website.

## License

PCNportal is licensed under the GNU General Public License v3.0.

