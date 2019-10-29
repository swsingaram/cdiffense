# CDiffense!

## Overview

Clostrdium Difficile (*C. Diff.*) is a highly contagious bacteria that thrives in an environment like the ICU ward.  Millions of ICU patients are infected with *C. Diff.* each year, increasing the risk of a flare-up if these patients are overlooked.  Patients diagnosed with *C. Diff.*  often undergo lengthy and uncomfortable treatments; and as a consequence, hospitalization costs increase by a factor of four on average.

CDiffense is a clinical decision support resource for clinicians to assess which ICU patients are at risk for a *C. Diff.* infection.  CDiffense offers on-the-spot assessment, so that clinicans can assess the patient's risk for *C. Diff.* upon admission.  To use CDiffense, please visit [www.cdiffense.xyz](www.cdiffense.xyz); a short presentation about CDiffense is [here](https://www.slideshare.net/SurendraWSingaram/c-diffense-179826520).  CDiffense was created by Surendra (Walter) Singaram as a Health Data Science Fellow at Insight Data Science.  The project took three weeks to complete, from ideation to deployment.

## Data

MIMIC-III (Medical Information Mart for Intensive Care III) is a large, freely-available database comprising deidentified health-related data associated with over forty thousand patients who stayed in critical care units of the Beth Israel Deaconess Medical Center between 2001 and 2012.

The database includes information such as demographics, vital sign measurements made at the bedside (~1 data point per hour), laboratory test results, procedures, medications, caregiver notes, imaging reports, and mortality (both in and out of hospital).  In this project, we will use the admissions table, the patient table, and the diagnostic table for our analysis.

PostgreSQL was used to manipulate the following tables.

Please see the notebook on [Cleaning and EDA](https://github.com/swsingaram/cdiffense/blob/master/CDiffense_cleanup_EDA.ipynb) for further details.

### Admissions Table

The ADMISSIONS table gives information regarding a patient’s admission to the hospital. Since each unique hospital visit for a patient is assigned a unique HADM_ID, the ADMISSIONS table can be considered as a definition table for HADM_ID. Information available includes timing information for admission and discharge, demographic information, the source of the admission, and so on.

### Patients Table

The PATIENTS table gives information regarding a patient's de-identified date of birth and the genotypical sex of the patient.

### The D_ICD Diagnosis Table

This table defines International Classification of Diseases Version 9 (ICD-9) codes for diagnoses. These codes are assigned at the end of the patient’s stay and are used by the hospital to bill for care provided.  The ICD-9 code is used as the "ground truth" for the patient's final diagnosis.  (The ICD-9 code for *C. Diff.* is 00845.)

## Model

Patient inputs were both numerical (patient vitals, age, and length of stay) as well as categorical (admission type/location and preliminary diagnosis); the categorical variables were one-hot encoded.  CDiffense takes the patients inputs and calculates the probability the patient is in the *C. Diff.* positive class by using a binary classifier.  Logistic regression showed robust performance among the other binary classifiers it was tested against: a random forest model and a gradient-boosted random forest model.  (Performance was measured by the area under the ROC curve.)

Please see the notebook on [Model Training and Testing](https://github.com/swsingaram/cdiffense/blob/master/CDIffense_Training_Cross-Validation_Testing_Feature_Importance.ipynb) for further details.

CDiffense was deployed on Amazon AWS using Dash.  The source code of the app can be found [here](https://github.com/swsingaram/cdiffense/blob/master/app/cdiff_web_application_scaled_features.py)

## Acknowledgements

I am grateful to my friends Dr. Kang Liu and Dr. Robert Lowenstein, M.D., for many fruitful discussions.