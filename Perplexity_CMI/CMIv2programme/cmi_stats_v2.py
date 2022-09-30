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
#   (The corpora file names are currently hardcoded in that function. Sorry for that!)
#
# 5. Calculate the code-mixing of the entire corpus using cmi_stats/2.
#    A typical usage is:
#
#       >>> cmi_stats('ned', tagsets.ndtags)
#
#    where 'ned' says that the Dutch corpus should be the one processed and
#    tagsets.ndtags that it's annotated with the tagset of Nguyen & Dogruöz.
# 
#    Another example:
#
#       >>> cmi_stats('cswsest', tagsets.csws16tags)
#
#    where 'cswsest' is the 2016 EMNLP code-switching workshop English-Spanish
#    training corpus and tagsets.csws16tags that year's version of the tagset.
#
#    The system output statistics come in seven groups, as follows:
#       1. Cc = the overall CMI value for the entire corpus.
#       2. The total number of utterances and the number of code-mixed utterances.
#       3. The fraction (%) of mixed and non-mixed utterances, respectively.
#       4. The average code-mixing per utterance (Cu) in the mixed utterances
#           and overall in the corpus.
#       5. The number of utterance-internal code-switching points overall;
#           average number of switches inside the mixed utterances and
#           average for all utterances; the number of switches between utterances
#           and the fraction of switches between utterances.
#       6. The fraction of mixed utterances in different Cu intervals together with
#           the average number of switch points in each of those intervals.
#       7. The number and fraction of words annotated with each tag in the tagset.
#
###################################################################################

###################################################################################
#
# The Code-Mixing Index is further described in the following two papers:
#
# [CMI v2] Gambäck, B. and Das, A.: Comparing the level of code-switching in corpora.
# Proc. of the 10th International Conference on Language Resources and Evaluation (LREC).
# Portoroz, Slovenia (May 2016), pp 1850–1855.
#
# [CMI v1] Gambäck, B. and Das, A.: On measuring the complexity of code-mixing.
# Proc. of the 1st Workshop on Language Technologies for Indian Social Media (Social-India).
# Goa, India (Dec 2014), pp. 1-7.
#
###################################################################################

import cmi_tagsets as tagsets
import cmi_corpus_reader as creader


#########################################################################
#                                                                       #
#                       MAPPING OF LANGUAGE TAGS                        #
#                      FOR THE PREDEFINED TAGSETS                       #
#                  (See the definitions of the predefined               #
#                   tagsets at the beginning of the file.)              #
#                                                                       #
#########################################################################


#########################################################################
# Calculate the number of words tagged by each language tag, including
# defining which language any mixed words belong to, for each tagset.
#
# Return the number of words tagged as belonging to any language
# and the number of non-language words in the utterance, as well as
# the number of words belonging to the utterance's matrix language
# (dominating language) and that matrix language itself.
#
def maptags(tags, tagset, prevmatrix):

    if tagset == tagsets.dastags:
        eng = tags[0] + tags[1] + tags[2]   # EN + EN+{HI|BN}_SUFFIX
        bng = tags[3] + tags[4]             # BN + BN+EN_SUFFIX
        hnd = tags[5] + tags[6]             # HN + HN+EN_SUFFIX
        #ne = tags[7]  + tags[10]
        #acro = tags[11] + tags[13] + tags[14]
        ## While this option is based on the suffixes of NEs and ACROs
        eng += tags[8] + tags[12]           # eng above + {NE|ACRO}+EN_SUFFIX
        bng += tags[9] + tags[13]           # bng above + {NE|ACRO}+BN_SUFFIX
        hnd += tags[10] + tags[14]          # hnd above + {NE|ACRO}+HI_SUFFIX
        ne = tags[7]
        acro = tags[11]

        other = tags[15] + tags[16]
        nonlang = ne + acro + other
        lang = eng + bng + hnd
        #domlang = max(eng,bng,hnd)       
        lang1 = eng
        lang2 = max(bng,hnd)

    elif tagset == tagsets.nitatags:
        eng = tags[0]
        bng = tags[1]
        hnd = tags[2]
        mix = tags[3]
        nonlang = tags[4] + tags[5] + tags[6] + tags[7]
        lang = eng + bng + hnd + mix
        lang1 = eng
        lang2 = max(bng,hnd)

    elif tagset == tagsets.ndtags:
        lang1 = tags[0] # ned
        lang2 = tags[1] # tur
        nonlang = tags[2]
        lang = lang1 + lang2

    elif tagset == tagsets.vyastags:
        lang1 = tags[0]
        lang2 = tags[1]
        error = tags[2] + tags[3]
        nonlang = 0
        lang = lang1 + lang2 + error

    elif tagset == tagsets.firetags:
        eng = tags[0] + tags[1] + tags[2]
        bng = tags[3] + tags[4]
        hnd = tags[5] + tags[6]
        gur = tags[7] 
        kan = tags[8]
        mix = tags[9]
        nonlang = tags[10]
        lang = eng + bng + hnd + gur + kan + mix
        #domlang = max(eng,bng,hnd,gur,kan)
        lang1 = eng
        lang2 = max(bng,hnd,gur,kan)

    elif tagset == tagsets.csws14tags:
        lang1 = tags[0]
        lang2 = tags[1]
        mix = tags[2] + tags[3]
        nonlang = tags[4] + tags[5]
        lang = lang1 + lang2 + mix

    elif tagset == tagsets.csws16tags:
        lang1 = tags[0]
        lang2 = tags[1]
        fw = tags[2]
        mix = tags[3] + tags[4]
        nonlang = tags[5] + tags[6] + tags[6]
        lang = lang1 + lang2 + fw + mi