## Model information

Here you can find general information about our available models. The models have been trained on extensive data sets with thorough parameter tuning. A subset of these models have also formed the basis of published work.
The model names contain information of their learning configurations, and can be viewed per data type. The data types currently supported can be found under 'Data type' in the 'Compute here!' tab. **Model-specific information is provided upon choosing a data type from the dropdown menu.**

The model name follows the syntax _"{alg}\_{name}\_{sample}\_{n}sites"_:

- alg = algorithm (options: HBR, BLR)
- name = description of the model
- sample = training sample size (e.g. 10K is 10.000 subjects)
- n = amount of unique training data collection sites

Example: 'BLR_lifespan_57K_82sites' makes use of the Bayesian Linear Regression algorithm, across the human lifespan, trained on ~57.000 subjects from 82 different collection sites.

We currently support two algorithms, Bayesian Linear Regression (BLR) and Hierarchical Bayesian Regression (HBR). For choosing a model, the main practical difference is that HBR requires full Bayesian estimation. HBR therefore takes more time to provide results and may provide better results.

Please note: the number of available models is constantly growing, and more data types will continue to be supported. Let us know about specific requests on [![Gitter](https://badges.gitter.im/PCNportal/community.svg)](https://gitter.im/PCNportal/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge).

<br />
### Model contributions

Contributions of new models to PCNportal are accepted and encouraged. Models trained with the [PCNtoolkit](https://github.com/amarquand/PCNtoolkit) library can be added to the platform easily after adapting the standard directory structure. Models trained otherwise will need to provide an API as well.

Example directory:  
![img](assets/modelcontribution.png)

To contribute a model, please prepare a model directory that follows the same structure as the others. The full up-to-date instructions on how to contribute models can be found [here](https://docs.google.com/document/d/1PxYHUmn4XjvPJXtqMNHkkKLAPrzsYonlNxdtxMxlXoA/edit?usp=sharing).

Models not trained with PCNtoolkit can be accepted when a Python script is provided for transfer learning. Please contact us on Gitter to discuss such options. Models will be tested by experts before being hosted on the website.
