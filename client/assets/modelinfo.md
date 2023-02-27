## Model information

Here you can find general information about our available models. The models have been trained on extensive data sets with thorough parameter tuning. A subset of these models have also formed the basis of published work.
The model names contain information of their learning configurations, and can be viewed per data type. The data types currently supported can be found under 'Data type' in the 'Compute here!' tab. **Model-specific information is provided upon choosing a data type from the dropdown menu.**

The model name follows the syntax *"{alg}\_{name}\_{sample}\_{n}sites"*:
* alg = algorithm (options: HBR, BLR)
* name = description of the model
* sample = training sample size (e.g. 10K is 10.000 subjects)
* n = amount of unique training data collection sites

Example: 'BLR_lifespan_57K_82sites' makes use of the Bayesian Linear Regression algorithm, across the human lifespan, trained on ~57.000 subjects from 82 different collection sites.

Please note: the number of available models is constantly growing, and more data types will continue to be supported. Let us know about specific requests on [![Gitter](https://badges.gitter.im/PCNportal/community.svg)](https://gitter.im/PCNportal/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge).
  
  
<br />
### Model contributions 

Contributions of models are accepted and encouraged by PCNportal. Models trained with PCNtoolkit can be added instantly after adapting the standard directory structure, while other models will need to provide an API as well. 

Example directory:  
![img](assets/modelcontribution.png)
'Models' contains all models with naming convention NM\_0\_\{x\}\_fit.pkl where _x_ is the model number corresponding to the order of idp ids.
The features that were used in training should be saved in 'idp_ids.txt', the names of data collection sites in 'site_ids.txt', the names of mandatory columns (covariates and site effects) in 'mandatory_columns.txt'. All strings should be separated with return ('\n'). Any information about the model and how its trained (including hyperparameters) should be provided in the 'README.md', along with a data template link that follows the syntax: _\[Download\]\(download\_link\)_.

Models not trained with PCNtoolkit can be accepted when a Python script is provided for transfer learning. Please contact us on Gitter to discuss such options.

Models will be tested by experts before being hosted on the website.