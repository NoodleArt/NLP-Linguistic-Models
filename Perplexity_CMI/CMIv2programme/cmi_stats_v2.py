###################################################################################
#
# Code-Mixing Corpus Calculation
# Björn Gambäck, NTNU 2014-2016.
# contact: <gamback@idi.ntnu.no>
#
# For corpora whose documents contain words tagged with language identifiers.
# 
###################################################################################
#
# Prerequisites:
# 1. NLTK
# 2. Python >= v3
#
###################################################################################
#
# Usage (if you're using a predefined corpus and tagset, skip to step 4 or 5!):
#
# 1. Define the tagset of the corpus, unless it's one of the predefined tagsets
#    given in the file cmi_tagsets.py (see that file for descriptions):
#    a. dastags used by Das and Gambäck
#    b. nitatags used in the NITA corpora
#    c. ndtags used by Nguyen & Dogruöz
#    d. vyastags used by Vyas et al.
#    e. firetags used in the FIRE shared task
#    f. csws14tags used in the EMNLP 2014 CS workshop shared task
#    g. csws16tags used in the EMNLP 2016 CS workshop shared task
#
# 2. If introducing a new tagset, define
#    a. which tags are language tags in the langtags/1 mapping in cmi_tagsets.py.
#    b. which tags map to which language. See further maptags/3 below.
#    Also check if some tags/words need special treatment, see cmi_one_utterance/3.
#
# 3. Define a corpus reader class, unless it's one of the predefined corpus readers
#    given in the file cmi_corpus_reader.py.
#
# 4. Add the corpus file name and its language ID to codemix/1 in cmi_corpus_reader.py.
#   (The corpora file names are currently hardcoded in that functio