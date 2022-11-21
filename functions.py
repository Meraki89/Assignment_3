import re
import os
import nltk
import codecs
import requests
import fileinput
import wikipedia
import wikipediaapi
from bs4 import BeautifulSoup
from nltk import word_tokenize
from urllib.parse import urljoin
from nltk.tokenize import sent_tokenize


###########################################################################################################
# helper functions
###########################################################################################################
def count_words(sentence):
    num_words = len(sentence.split())
    return num_words


def read_lines(file):
    with codecs.open(file, "r", "utf-8") as reader:
        return reader.readlines()


def write_lines(contents, file):
    with codecs.open(file, "w", "utf-8") as writer:
        writer.writelines(contents)


def write_lines_a(contents, file):
    with codecs.open(file, "a", "utf-8") as writer:
        writer.writelines(contents)


def join_url(line):
    return urljoin("https://en.wikipedia.org", line)


def join_files(files: list, joined_outfile):
    with codecs.open(joined_outfile, "w", "utf-8") as outfile, \
            fileinput.input(files, encoding="utf-8") as infile:
        for line in infile:
            outfile.write(line)


def get_links(url):
    try:
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        paragraphs = soup.find(id="mw-content-text").find(class_="mw-parser-output").find_all("p", recursive=False)

        links = []
        for p in paragraphs:
            p_links = p.find_all("a", recursive=False)
            for link in p_links:
                link.get("href")
                links.append(link.get("href"))
        return links
    except Exception as e:
        print(e)
        print(url)


def clean_text(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    paragraphs = soup.find(id="mw-content-text").find(class_="mw-parser-output").find_all("p", recursive=False)

    text = ""
    for paragraph in paragraphs:
        text += paragraph.text

    text = re.sub(r"\[.*?]+", "", text)
    text = text.replace("\n", "")
    return text


def print_content(keyword):
    try:
        wikipedia.set_lang("en")
        page = wikipedia.page(keyword).content
        with codecs.open(keyword + ".txt", "w", "utf-8") as writer:
            writer.write(page)
    except Exception as e:
        print(e)
        print(keyword)
    return keyword + ".txt"


###########################################################################################################
# POS functions
###########################################################################################################
def tokenize_word(keyword):
    # join_files([clean_texts(keyword), extract_and_clean(keyword)], keyword + "_clean_joined")

    # with codecs.open(keyword + "_clean_joined", "r", "utf-8") as reader:
    # content = reader.read()

    with codecs.open(english_keyword_clean(keyword), "r", "utf-8") as reader:
        content = reader.read()

    words = word_tokenize(content)
    return words


def nouns(keyword):
    write_lines(["\n".join(f"('{word}', '{pos}')" for (word, pos) in nltk.pos_tag(tokenize_word(keyword))
                           if pos == "NN" or pos == "NNS")], keyword + "_nouns.txt")
    return keyword + "_nouns.txt"


def proper_nouns(keyword):
    write_lines(["\n".join(f"('{word}', '{pos}')" for (word, pos) in nltk.pos_tag(tokenize_word(keyword))
                           if pos == "NNP" or pos == "NNPS")], keyword + "_proper_nouns.txt")
    return keyword + "_proper_nouns.txt"


def adjectives(keyword):
    write_lines(["\n".join(f"('{word}', '{pos}')" for (word, pos) in nltk.pos_tag(tokenize_word(keyword))
                           if pos == "JJ" or pos == "JJR" or pos == "JJS")], keyword + "_adjectives.txt")
    return keyword + "_adjectives.txt"


def extract_acronyms(keyword):
    # join_files([clean_texts(keyword), extract_and_clean(keyword)], keyword + "_clean_joined")

    # with codecs.open(keyword + "_clean_joined", "r", "utf-8") as reader:
    # content = reader.read()

    with codecs.open(english_keyword_clean(keyword), "r", "utf-8") as reader:
        content = reader.read()

    pattern = r"\b(?:[a-z]*[A-Z][a-z]*){2,}|(?:[a-zA-Z]\.){2,}"
    results = re.findall(pattern, content)

    write_lines_a([word + "\n" for word in results], keyword + "_acronyms.txt")
    return keyword + "_acronyms.txt"


###########################################################################################################
# content-specific functions
###########################################################################################################
def english_keyword_clean(keyword):
    try:
        with codecs.open(print_content(keyword), "r", "utf-8") as reader:
            content = reader.read()

        content = re.sub(r"==.*?==+", "", content)
        content = content.replace("\n", "")

        sentences = nltk.sent_tokenize(content)

        write_lines_a([sent + "\n" for sent in sentences if count_words(sent) > 5], "en_text_" + keyword + ".txt")
        os.remove(print_content(keyword))
    except Exception as e:
        print(e)
        print(keyword)
    return "en_text_" + keyword + ".txt"


def extract_english_links(keyword):
    try:
        wikipedia.set_lang("en")
        url = wikipedia.page(keyword).url

        with codecs.open("en_links_" + keyword + ".txt", "w", "utf-8") as writer:
            for link in set(get_links(url)):
                writer.write(link + "\n")
    except Exception as e:
        print(e)
        print(keyword)
    return "en_links_" + keyword + ".txt"


def extract_english(keyword):
    for line in read_lines(extract_english_links(keyword)):
        try:
            url = join_url(line)
            sentences = nltk.sent_tokenize(clean_text(url))
            write_lines_a([sent + "\n" for sent in sentences if count_words(sent) > 5],
                          "en_all_text_" + keyword + "_clean.txt")
        except Exception as e:
            print(e)
            print(line)
    return "en_all_text_" + keyword + "_clean.txt"


def german_keyword_clean(keyword):
    try:
        wiki_html = wikipediaapi.Wikipedia(language="en", extract_format=wikipediaapi.ExtractFormat.HTML)
        page = wiki_html.page(keyword)

        url = page.langlinks["de"].fullurl

        sentences = sent_tokenize(clean_text(url), language="german")
        write_lines_a([sent + "\n" for sent in sentences if count_words(sent) > 5], "de_text_" + keyword + ".txt")
    except Exception as e:
        print(e)
        print(keyword)
    return "de_text_" + keyword + ".txt"


def extract_german_links(keyword):
    try:
        wiki_html = wikipediaapi.Wikipedia(language="en", extract_format=wikipediaapi.ExtractFormat.HTML)
        page = wiki_html.page(keyword)

        url = page.langlinks["de"].fullurl

        with codecs.open("de_links_" + keyword + ".txt", "w", "utf-8") as writer:
            for link in set(get_links(url)):
                writer.write(link + "\n")
    except Exception as e:
        print(e)
        print(keyword)
    return "de_links_" + keyword + ".txt"


def extract_german(keyword):
    for line in read_lines(extract_german_links(keyword)):
        try:
            wikipedia.set_lang("de")
            url = urljoin("https://de.wikipedia.org", line)
            sentences = sent_tokenize(clean_text(url), language="german")
            write_lines_a([sent + "\n" for sent in sentences if count_words(sent) > 5],
                          "de_all_text_" + keyword + "_clean.txt")
        except Exception as e:
            print(e)
            print(line)
    return "de_all_text_" + keyword + "_clean.txt"


def french_keyword_clean(keyword):
    try:
        wiki_wiki = wikipediaapi.Wikipedia(language="en", extract_format=wikipediaapi.ExtractFormat.WIKI)
        page = wiki_wiki.page(keyword)

        url = page.langlinks["fr"].fullurl

        sentences = sent_tokenize(clean_text(url), language="french")
        write_lines_a([sent + "\n" for sent in sentences if count_words(sent) > 5], "fr_text_" + keyword + ".txt")
    except Exception as e:
        print(e)
        print(keyword)
    return "fr_text_" + keyword + ".txt"


def extract_french_links(keyword):
    try:
        wiki_html = wikipediaapi.Wikipedia(language="en", extract_format=wikipediaapi.ExtractFormat.HTML)
        page = wiki_html.page(keyword)

        url = page.langlinks["fr"].fullurl

        with codecs.open("fr_links_" + keyword + ".txt", "w", "utf-8") as writer:
            for link in set(get_links(url)):
                writer.write(link + "\n")
    except Exception as e:
        print(e)
        print(keyword)
    return "fr_links_" + keyword + ".txt"


def extract_french(keyword):
    for line in read_lines(extract_french_links(keyword)):
        try:
            wikipedia.set_lang("fr")
            url = urljoin("https://fr.wikipedia.org", line)
            sentences = sent_tokenize(clean_text(url), language="french")
            write_lines_a([sent + "\n" for sent in sentences if count_words(sent) > 5],
                          "fr_all_text_" + keyword + "_clean.txt")
        except Exception as e:
            print(e)
            print(line)
    return "fr_all_text_" + keyword + "_clean.txt"
