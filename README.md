PCNportal is a website that provides access to modelling with finetuned normative models for neuroimaging analysis, pre-trained and applied with the package [PCNtoolkit](https://pcntoolkit.readthedocs.io/en/latest/).

## Using the website
The latest version of the website is available at https://pcnportal.dccn.nl/, and provides all instructions necessary to start modelling.
This GitHub contains the client side and server side code for the [PCNportal](https://pcnportal.dccn.nl/) project. The client side contains code to facilitate the GUI and website service, while the server side code contains functionality to model with PCNtoolkit on a remote server and share results.

Please refer to the Wiki of this GitHub page to learn more about the implementation and development pipeline of the website.

## Features

PCNportal provides a user-friendly lightweight GUI, but also adds functionality to PCNtoolkit. The website:
- hosts all resources necessary to learn about normative modelling in theory and practice,
- dynamically checks available models and provides model-specific information,
- contains data control checks to point out errors and provides feedback on the request,
- shares results through a public server and an automated email service,
- cleans up data older than thirty days to comply with privacy guidelines,
- automatically runs, checks and manages parallelized computation jobs.

## Testing

Testing the website can be done through modelling with demo data (also see Wiki's client side page).

To locally deploy the GUI without modelling functionality, please follow these instructions:
* pull image from DockerHub
* docker compose build
* docker compose up
* but SSH failure

To test modelling functionality, please refer to PCNtoolkit tutorials and documentation.

## Assistance
To report bugs or issues or if you have any questions or feature requests, please use our [Gitter](https://gitter.im/PCNportal/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge).

## License

PCNportal is licensed under the GNU General Public License v3.0.

