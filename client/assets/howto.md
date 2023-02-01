
### Modelling instructions
(Don't yet have your own data ready? Scroll down to do a demo run.)

**First, we explore what normative model is best for you.**
- Explore the meaning of model names in the 'Model information' tab.
- Then, choose a normative model in the 'Compute here!' tab:
    - Select the _Data Type_ you want to use.
    - Explore the available models for this data type in the _Normative Model_ dropdown menu. Selecting a model will show model-specific information on training data and hyperparameters.
    - Choose a model according to your preferences. 
    (Hint: to learn more about hyperparameters and model training, please refer to [Fraza et al.](https://www.sciencedirect.com/science/article/pii/S1053811921009873) (2021) for BLR and [Kia et al.](https://journals.plos.org/plosone/article/comments?id=10.1371/journal.pone.0278776) (2022) for HBR.)

**Then, your data will need to be prepared for processing.**
- From your chosen model, view the model-specific information and download the provided data template .csv.
- Ensure that the column names of your data sets match the template.
- Split your data into an adaptation and test set according to your preferred ratio.
- Upload your test and adaptation data in the right boxes.

**Finaly, submit your computation request...**
- Enter the email address where you would like to receive your results download link.
- Press _Submit_. Congratulations! 
- Wait a moment to receive feedback on how well your data matches the template, and to receive your session ID.

**What happens next?**
- Your session ID will be provided after the request is submitted. If you would like to request help with troubleshooting, make sure to save this ID.
- Within several hours, you should receive an email in your inbox with a link to download both your results and model-related error measures.
- Please be patient: the waiting time may vary according to model choice, data set and network traffic. Check your spam folder, and wait for 24 hours before requesting support through the PCNportal [![Gitter](https://badges.gitter.im/PCNportal/community.svg)](https://gitter.im/PCNportal/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge).

**What can I do with my results?**
The resulting z-scores represent individualized abnormalities, and follow-up analysis can exploit this information to learn more about the relationship between your provided data and cognitive ability or diagnostic measures. Some options for follow-up analysis are mass univariate group comparisons, post-hoc classification, and multivariate prediction, discussed in [Rutherford et al. (2022)](https://www.biorxiv.org/content/10.1101/2022.11.14.516460v1).

Normative modelling is also a very visual concept, and you can use visualize your own results with the following Python code: (insert link).

---

### Try the demo  

If you just want to give the website a test run, follow these instructions.

First, download the demo [test data](https://drive.google.com/uc?export=download&id=1S2uQ-lbP7km-OVLqQhehVisV1CwHDjKJ) and [adaptation data](https://drive.google.com/uc?export=download&id=1PjiA-zIzJFsvmHZiBtsj5P2dRfZeH6XV) from the FCON1000 project.

Fill in these modelling settings in the 'Compute here!' tab:
- for Data Type, select “ThickAvg”,
- for Normative Model, select ‘BLR_lifespan_57K_82sites’,
- for ‘Upload test data’, upload the provided test data file: “fcon1000_te.csv”,
- for ‘Upload adaptation data’, upload the provided adaptation data file: “fcon1000_tr.csv”,
- for ‘Email address for results’, enter an email address to receive your demo results,
- click _Submit_.

After submission, your tab should look something like below:

<img src="assets/demo.png" width='70%' length='70%'/>

The green box will appear some minutes later after computation is complete. When you see this box, it's time to check your inbox for results!
