"""This module is for cleaning up the data."""
# -*- coding: utf-8 -*-

def clean():
    """Temp function for cleaning"""
    with open('corpus.txt', 'r') as f_obj:
        corpus_text = f_obj.readline().decode('string-escape').encode('ascii', 'ignore').strip()
        print corpus_text
