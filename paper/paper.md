---
title: 'PCNportal: a flexible web-based framework for accessible normative modelling'
tags:
  - Neuroimaging
  - Normative modelling
  - Individual variability
  - Mental illness
  - Online interface
authors:
  - name: Pieter W. Barkema
    orcid: 0000-0002-2189-5160
    affiliation: "1,2"
    corresponding: true
  - name: Saige Rutherford
    orcid: 0000-0003-3006-9044
    affiliation: "1,2,3"
  - name: Hurng-Chun Lee
    orcid: 0000-0001-7693-6890
    affiliation: 1
  - name: Seyed Mostafa Kia
    orcid: 0000-0002-7128-814X
    affiliation: "1,2,4"
  - name: Hannah S. Savage
    orcid: 0000-0002-1057-7239
    affiliation: "1,2"
  - name: Christian F. Beckmann
    orcid: 0000-0002-3373-3193
    affiliation: "1,2,5"
  - name: Andre F. Marquand
    orcid: 0000-0001-5903-203X
    affiliation: "1,2"
    corresponding: true

affiliations:
 - name: Donders Institute for Brain, Cognition, and Behavior, Radboud University, Nijmegen, the Netherlands
   index: 1
 - name: Department of Cognitive Neuroscience, Radboud University Medical Center, Nijmegen, the Netherlands
   index: 2
 - name: Department of Psychiatry, University of Michigan, Ann Arbor, MI, USA
   index: 3
 - name: Department of Psychiatry, Utrecht University Medical Center, Utrecht, the Netherlands
   index: 4
 - name: Centre for Functional MRI of the Brain, University of Oxford, Oxford, UK
   index: 5

date: 23rd February 2023
bibliography: paper.bib
---

# Summary

The neuroscience of mental disorders remains poorly understood despite large scientific efforts. A major factor in this knowledge gap has been the strong focus on group average effects which largely neglect individual differences in brain structure or function. As a consequence, most analytical approaches classically used to study mental disorders assume that subjects with the same diagnostic label neurobiologically deviate in the same way; a misleading assumption. 

Normative modelling is one recently successful framework that can address this problem [@Marquand:2016; @Marquand:2019]. Normative modelling detects individual-level differences by placing each person into the reference population, producing individualized deviation scores. Applied to brain data, the magnitude and spatial pattern of individual brain deviations can then be linked to the severity of symptoms, psychiatric diagnosis, or other behavioral characteristics. Researchers from various clinical and non-clinical fields could benefit from adopting this framework to facilitate valid inference on the individual brain level, paving the way towards precision medicine.

However, the methodological underpinnings of normative modelling are relatively complex and the estimation of normative models requires access to large datasets processed using consistent pipelines. These factors reduce the accessibility of normative modelling to many seeking its benefits. Our research group has developed the python-based normative modelling package PCNtoolkit [@Marquand:2021] which provides access to many validated algorithms for normative modelling and solutions for accommodating data collection site effects [@Kia:2020] non-Gaussian data distributions [@Fraza:2021; @de_Boer:2022; @Dinga:2021], federated model estimation [@Kia:2022] and other statistical problems in a consistent and principled way. Despite efforts to make the PCNtoolkit more accessible  [@Rutherford:2022c], considerable time, technological skill and computational resources are still necessary for developing optimized normative models. These constraints leave much potential of normative modelling unfulfilled for the neuroscience community. To address these problems, we introduce PCNportal: an online platform integrated with PCNtoolkit that offers access to pre-trained research-grade normative models estimated on tens of thousands of participants, without the need for computation power or programming abilities – only a data set and an internet connection. We believe this increased accessibility of normative models will not only benefit precision medicine for mental illness, but will generally contribute to a better understanding of individual differences – in the brain or any type of human feature. 

# Statement of need

While normative modelling has been mainly a tool for data scientists, the increase in appreciation for individual brain differences in clinical research comes with an increase in demand from users without a background in computer science and programming. Recent applications illustrate the growing success of normative modelling, such as in Alzheimer’s Disease [@Verdi:2022] and schizophrenia [@Lv:2021], and software packages provide the tools necessary to support the increase in demand from a diverse audience. Our PCNtoolkit, for example, has been used to research individuals with autism spectrum disorder, where normative models revealed highly individualized brain development trajectories that cannot be captured by classical ‘case-control’ (group-average) studies [@Zabihi:2019]. PCNtoolkit has also been used for stratifying attention-deficit/hyperactivity disorder (ADHD) [@Wolfers:2020], schizophrenia and bipolar disorder [@Wolfers:2021], and general psychopathology [@Parkes:2021]. PCNtoolkit has thus proven to be a strong foundation for large scale normative modelling, but – as noted above – still requires significant computation power, time and technical expertise to use. We present PCNportal here as a solution, supported by a scientific paper concurrently in submission [@Rutherford:2022a].

PCNportal is built as an extension of PCNtoolkit that allows users to easily apply normative models pre-trained on large neuroimaging datasets to a brain imaging dataset of choice without needing programming code or computing power. In more detail, PCNportal is a lightweight client-server application. The client side is a Flask-based online application (https://pcnportal.dccn.nl/) with a simple user-friendly graphical user interface. It contains all instructions and information necessary to quickly get started with modelling, but also refers to elaborate tutorials and published work using these models to promote a deeper understanding of the subject matter. On the server side, a set of helper scripts integrate the online application with a back-end, based on PCNtoolkit, which performs the computations necessary to adapt the pre-trained model to the new dataset (via transfer learning) and distribute the computational workload across our dedicated computation nodes to reduce modelling time. PCNportal then uploads the anonymized results to a public server and shares them with the user through email. Lastly, it automatically deletes all user data after a thirty day period.

The design of PCNportal specifically keeps in mind the growing demand for normative models by being highly scalable and flexible. Our web platform is based on gunicorn and nginx that support scaling up to large user bases. PCNportal is currently hosted within the technical infrastructure of the Donders Center for Cognitive Neuroimaging, where clusters dedicated to mass computation can simultaneously process many user requests. The application is containerized with Docker to ensure that our application can be maintained with ease and is highly portable, ensuring that it can be scaled up to cloud-based platforms as necessary. Currently PCNportal provides access to existing normative models based on cortical thickness, brain volume, surface area and resting-state functional connectivity [@Rutherford:2022b; @Rutherford:2022c; @Kia:2020; @Kia:2022], but we have designed this application to facilitate straightforward contribution of additional models. Flexibly increasing the number of available models is a crucial design feature, as normative models can be developed for many different data types, other than brain images, including but not limited to genetic data, psychophysiological data and digital phenotyping data, with applications to neuropsychiatry and beyond. We therefore designed PCNportal in a way that new models can be dynamically added and are instantly available to users. We welcome model contributions from other groups and enable this process through documented instructions.

Through this contribution, research efforts towards conceptualizing mental illness can directly benefit from fine-tuned and well-validated models contributed by research labs specialized in normative modelling, without requiring specialized technical expertise or infrastructure. The open-source nature  of PCNportal will hopefully serve as an inspiration to other scientific teams that wish to share their big data models and technological infrastructure with a wider audience. Altogether, PCNportal provides freely accessible high-quality brain data  analysis on the individual level for a wide range of neural biomarkers to the research community in a scalable way, with ongoing projects to support modelling data types beyond brain images. By bridging the gap between methodological development and urgent clinical challenges, we aim to build toward a better understanding of neurological or biological differences between individuals that in turn supports the understanding and treatment of mental and physical disorder . 

# Acknowledgements

This research was supported by the Wellcome Trust under a Digital Innovator award (‘BRAINCHART,’ 215698/Z/19/Z)  and the European Research Council (ERC, grant ‘MENTALPRECISION’ 10100118).

# References