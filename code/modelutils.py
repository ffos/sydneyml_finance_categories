import pickle

OUTPUT_FILE_CLASSIFIER = "models/bank_detector_clf.pkl"
OUTPUT_FILE_VECTORIZER = "models/bank_detector_vectorizer.pkl"
OUTPUT_FILE_LABEL_ENCODER = "models/bank_detector_labelEncoder.pkl"

def saveBankDetectorModels(classifier=None, vectorizer=None, labelEncoder=None):
    if classifier == None:
        return False, "Classifier is None"
    if vectorizer == None:
        return False, "Vectorizer is None"
    if labelEncoder == None:
        return False, "LabelEncoder is None"
    pickle.dump(classifier, open(OUTPUT_FILE_CLASSIFIER, "wb"))
    pickle.dump(vectorizer, open(OUTPUT_FILE_VECTORIZER, "wb"))
    pickle.dump(labelEncoder, open(OUTPUT_FILE_LABEL_ENCODER, "wb"))
    return True, "Persisted files:  %s,   %s, and   %s" % (OUTPUT_FILE_CLASSIFIER, OUTPUT_FILE_VECTORIZER, OUTPUT_FILE_LABEL_ENCODER)


def loadBankDetectorModels():
    classifier = pickle.load(open(OUTPUT_FILE_CLASSIFIER, "rb"))
    if classifier == None:
        return False, "Classifier file %s not found" % (OUTPUT_FILE_CLASSIFIER)
    vectorizer = pickle.load(open(OUTPUT_FILE_VECTORIZER, "rb"))
    if vectorizer == None:
        return False, "Vectorizer file %s not found" % (OUTPUT_FILE_VECTORIZER)
    labelEncoder = pickle.load(open(OUTPUT_FILE_LABEL_ENCODER, "rb"))
    if labelEncoder == None:
        return False, "LabelEncoder file %s not found" % (OUTPUT_FILE_LABEL_ENCODER)
    return True, classifier, vectorizer, labelEncoder