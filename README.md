# NLP Preprocessing
### Purpose
This tool applies a several preprocessing functions to the proposals that you want to analyse. The data generated at this stage will the be used for word clouds generation and speech analysis.

*Please note that this repository is not made to be user driven : it is required by other projects but as much as possible
the interactions with the users will be limited.* 

- **French stop words removal** : stop words are the words that are essentials to language but that does not contain relavant informations in terms of semantic analysis. In this category you'll find pronouns, co-ordinating conjunction, the most commons words like "a", "the" etc...
This preprocessing function will be used to avoid noise in your word cloud for instance. 

- **Lemmatization** : this action consists in turning the different forms of a word into its canonical form. For instance, it will remove the gender and plural marks, it will set the verbs to their infinitive form etc. This action is used to concentrate the statistical information on the canonical form rather than spread it between the forms. 
Once again this is a really useful feature to generate interesting word clouds.

- **Special character cleaning**: this features aims to focus solely on the textual data by removing the special characters such as numbers, backslash, question marks etc... 

These functions target a macro analysis approach over the consultation meaning that we do not focus on the discourse of a single participant but we rather try to investigates the global trends. 

### Expected output
This repository will output a global .json file which will contain three dictionaries storing in the order : 

- the whole dataset with a new column called preprocessed_proposals
- a dictionary storing the word frequency computed on the preprocessed proposals (used to generate word clouds)
- a dictionary storing the word frequency computed on the body of the proposals (used to do speech analysis)


## TLDR
```
make build
```

## Setup
- python >= 3.8
- clone the repository and install the requirements (nice practice : do so in a dedicated environment)
- install docker (see [here](https://docs.docker.com/get-docker/))

### Execution on your data
#### Python
if you have successfully installed python >= 3.8 and installed the requirements in an environment proposed 
above you can run the following command to launch the preprocessing:
```
python main.py -f "ABSOLUTE_PATH_TO_YOUR_FILE.xls"
```
This command will generate several json files: the one to focus on "nlp_preprocessing_output.json". 
It will be created in the ```./dist``` repository in the project. 

Please note that the following extensions are supported : .csv / .xls

#### Run with docker
If you prefer work with docker several steps will be required to launch the script on your data: 
- add your file in the directory ```./data``` and then open the dockerfile with a text editor. 
On line 23 you'll find this command :
```
RUN python ./main.py -f "/nlp_preprocessing/data/subset_raw_data.csv"
```
Change the name subset_raw_data.csv with the name of your file. Please do not change anything else. 
Save the dockerfile and then run the following command:
```
make build
```
A file called nlp_preprocessing_output.json will be added on your machine in your ```./dist``` folder





