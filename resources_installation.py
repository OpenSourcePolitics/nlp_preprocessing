"""
This file aims to address the downloading of all resources required by stanza and nltk
"""
import os
import stanza
import nltk
import torch
from data_management.utils import get_stanza_resources_root

stanza.download("fr")
nltk.download("stopwords")


def customise_lemmatization_model():
    """
    Updates the initial model of stanza with custom lemmas to improve the precision of the processor.
    See : https://stanfordnlp.github.io/stanza/lemma.html for further
    """
    root_path = get_stanza_resources_root()
    model = torch.load(os.path.join(root_path, 'stanza_resources/fr/lemma/gsd.pt'),
                       map_location='cpu')
    word_dict, composite_dict = model['dicts']

    # Customize your own dictionary
    composite_dict[('Présidente', 'NOUN')] = 'présidente'
    word_dict['Présidente'] = 'président'

    # Save your model
    torch.save(model, os.path.join(root_path, 'stanza_resources/fr/lemma/gsd.pt'))


customise_lemmatization_model()
