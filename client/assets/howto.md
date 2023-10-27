### Modelling instructions

(Don't have your own data ready yet? Scroll down to the _Demo_ with sample data.)

**First, we explore what normative model is best for you.**

- Explore model naming conventions in the 'Model information' tab.
- Then, choose a normative model in the 'Compute here!' tab:
  - Select the _Data Type_ you want to use.
  - Explore the available models for this data type in the _Normative Model_ dropdown menu. Selecting a model will show model-specific information on training data and hyperparameters.
  - Choose a model according to your preferences.
    (Hint: to learn more about hyperparameters and model training, please refer to [Fraza et al.](https://www.sciencedirect.com/science/article/pii/S1053811921009873) (2021) for BLR and [Kia et al.](https://journals.plos.org/plosone/article/comments?id=10.1371/journal.pone.0278776) (2022) for HBR.)

**Then, prepare your data for processing.**

- Split your data into an adaptation and test set according to your preferred ratio (for example, 50/50). Adaptation data is used for transferring the model, while test data is to evaluate it. The split is a trade-off between higher quality of model (more adaptation data) and better estimate of model quality (more test data).
- From your chosen model, view the model-specific information and download the provided data template .csv.
- Ensure that the column names of your data sets match the template.
- Upload your test and adaptation data in the right boxes.

**Finaly, submit your computation request...**

- Enter the email address where you would like to receive your results.
- Press _Submit_. Congratulations!
- Wait a moment to receive your session ID and feedback on how well your data matches the template.

**What happens next?**

- Make sure to save your session ID if you would like to request help with troubleshooting.
- Within some time you should receive an email in your inbox with a link to download both your results and model-related error measures.
- Please be patient: the waiting time may vary according to model choice, data set and network traffic. Check your spam folder, and wait several hours before requesting support through the PCNportal [![Gitter](https://badges.gitter.im/PCNportal/community.svg)](https://gitter.im/PCNportal/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge).
- Please remember to appropriately cite [PCNportal](https://wellcomeopenresearch.org/articles/8-326), used data and models.

**What can I do with my results?**
The resulting z-scores represent the deviations per feature per subject. Follow-up analysis can exploit this information to learn more about the relationship between your data and, for example, cognitive ability or diagnostic measures on the individual level. Some options for follow-up analysis are mass univariate group comparisons, post-hoc classification, and multivariate prediction, discussed in [Rutherford et al. (2022)](https://www.biorxiv.org/content/10.1101/2022.11.14.516460v1).

The other result files contain different evaluation measures per subject of the transferred model fit. Pearson's Rho correlation and its p-value, Squared Mean Standardised Error (SMSE), Root Mean Squared Error (RMSE) and explained variance are provided. Pearson's Rho, SMSE and RMSE all score the model fit by evaluating the predicted mean, with a lower Pearson's Rho and a higher SMSE and RMSE indicating a better fit (example usage in [Kia et al.](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9731431/) 2023).

Normative modelling is also a very visual concept, but visualization is not directly supported on the website yet. You can use the code at the bottom of this Jupyter [notebook](https://github.com/predictive-clinical-neuroscience/braincharts/blob/master/scripts/apply_normative_models_ct.ipynb) to plot your own results.
<br />

---

### Demo

Follow these instructions if you want to give the website a test run.

First, download the demo [test data](https://drive.google.com/uc?export=download&id=1S2uQ-lbP7km-OVLqQhehVisV1CwHDjKJ) and [adaptation data](https://drive.google.com/uc?export=download&id=1PjiA-zIzJFsvmHZiBtsj5P2dRfZeH6XV) from the [FCON1000](http://fcon_1000.projects.nitrc.org/) initiative.

Fill in these modelling settings in the 'Compute here!' tab:

- for Data Type, select “ThickAvg”,
- for Normative Model, select ‘BLR_lifespan_57K_82sites’,
- for ‘Upload test data’, upload the provided test data file: “fcon1000_te.csv”,
- for ‘Upload adaptation data’, upload the provided adaptation data file: “fcon1000_tr.csv”,
- for ‘Email address for results’, enter an email address to receive your demo results,
- click _Submit_.

After submission, your tab should look something like below:

<img src="assets/demo.png" width='70%' length='70%'/>

The green box will appear some time later after computation is complete. When it shows up, it's time to check your inbox for results!
