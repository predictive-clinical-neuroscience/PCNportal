PCNportal is a website that facilitates access to modelling with finetuned normative models for neuroimaging analysis, that are pre-trained and applied with the package [PCNtoolkit](https://pcntoolkit.readthedocs.io/en/latest/).

This GitHub contains the client side and server side code for the [PCNportal](https://pcnportal.dccn.nl/) project. The client side contains code to facilitate the GUI and website service, while the server side code contains functionality to model with PCNtoolkit on a remote server and share results.

Please refer to the GitHub [Wiki](https://github.com/predictive-clinical-neuroscience/PCNportal/wiki) to learn more about the implementation and development pipeline of the website, also containing tutorials and a demo.

## Using the website

The latest version of the website is available at https://pcnportal.dccn.nl/, and provides all instructions necessary to start modelling and how to use the results. Only a data set of supported models is needed. If not available, a demo is provided to test the website under the tab 'How to model'.

## Features

PCNportal provides a user-friendly lightweight GUI, but also adds functionality to PCNtoolkit. The website:
- hosts resources to learn about normative modelling in theory and practice,
- dynamically updates available models and model-specific information,
- checks data for errors and provides feedback,
- shares results through a public server and an automated email service,
- cleans up data older than thirty days to comply with privacy guidelines,
- automatically runs, checks and manages parallelized computation jobs.

## Testing

Testing the website can be done through modelling with demo data (also see Wiki's client side page).

To locally deploy the GUI without modelling functionality, please follow these instructions after installing [Docker](https://docs.docker.com/get-docker/):
* Pull the latest image from our [DockerHub](https://hub.docker.com/repository/docker/ifdevdocker/pcnonlinedev/general). For example:
''' docker pull ifdevdocker/pcnonlinedev:0.5-beta3'''
* ?> 'docker-compose up'
* Provides access to the GUI at localhost:5000 (e.g.: http://127.0.0.1:5000/), but not to the backend.

To test the backend modelling functionality, please refer to PCNtoolkit [tutorials] and corresponding documentation.


## Network diagram

PCNportal is a client-server application that combines the functionality of an easy GUI with that of heavy duty parallelized computation of the backend. We use various services, such as [Flask](https://flask.palletsprojects.com/en/2.2.x/), [Docker](https://www.docker.com/), [gunicorn](https://gunicorn.org/), [Gmail](https://developers.google.com/gmail/api/guides), [SURFdrive](surfdrive.surf.nl) and [TORQUE](https://wiki.archlinux.org/title/TORQUE) to accomplish this:

![Pipeline PCNportal](https://user-images.githubusercontent.com/39303377/220601095-5e27b7fe-a9d4-491e-88f9-f4f3db3a59ad.png) 

## Assistance
To report bugs or issues or if you have any questions or feature requests, please use our [Gitter](https://gitter.im/PCNportal/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge).

## License

PCNportal is licensed under the GNU General Public License v3.0.

