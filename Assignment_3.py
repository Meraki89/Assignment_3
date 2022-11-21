from functions import *
import os


def assignment_3(keyword):
    en_all_text = []
    de_all_text = []
    fr_all_text = []
    for element in keyword:
        # clean content of Wikipedia keyword articles in English
        # en_text_keyword1.txt and en_text_keyword2.txt
        english_keyword_clean(element)

        # clean content of Wikipedia keyword articles in German
        # de_text_keyword1.txt and de_text_keyword2.txt
        german_keyword_clean(element)

        # clean content of Wikipedia keyword articles in French
        # fr_text_keyword1.txt and fr_text_keyword2.txt
        french_keyword_clean(element)

        # list of links (en) and content of clean texts of all links (en)
        # en_links_keyword1.txt and en_links_keyword2.txt
        # appends all_text_keyword1"_clean.txt and all_text_keyword1"_clean.txt
        en_all_text.append(extract_english(element))

        # list of links (de) and content of clean texts of all links (de)
        # de_links_keyword1.txt and de_links_keyword2.txt
        # appends "keyword1_fulltext_german.txt and keyword2_fulltext_german.txt
        de_all_text.append(extract_german(element))

        # list of links (fr) and content of clean texts of all links (fr)
        # fr_links_keyword1.txt and fr_links_keyword2.txt
        # appends "keyword1_fulltext_french.txt and keyword2_fulltext_french.txt
        fr_all_text.append(extract_french(element))

    # joins and deletes all_text_keyword1"_clean.txt and all_text_keyword2"_clean.txt
    # to get "en_all_text" in one file and get rid of the unnecessary two other files
    join_files([en_all_text[0], en_all_text[1]], "en_all_text.txt")
    os.remove(en_all_text[0])
    os.remove(en_all_text[1])

    # joins and deletes keyword1_fulltext_german.txt and keyword2_fulltext_german.txt
    # to get "de_all_text" in one file and get rid of the unnecessary two other files
    join_files([de_all_text[0], de_all_text[1]], "de_all_text.txt")
    os.remove(de_all_text[0])
    os.remove(de_all_text[1])

    # joins and deletes keyword1_fulltext_french.txt and keyword2_fulltext_french.txt
    # to get "fr_all_text" in one file and get rid of the unnecessary two other files
    join_files([fr_all_text[0], fr_all_text[1]], "fr_all_text.txt")
    os.remove(fr_all_text[0])
    os.remove(fr_all_text[1])

    return None


print(assignment_3(["Vaccine", "Antibody"]))
