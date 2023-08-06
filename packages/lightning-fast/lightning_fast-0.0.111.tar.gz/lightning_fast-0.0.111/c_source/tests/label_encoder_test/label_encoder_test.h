//
// Created by 徐秋实 on 2020/10/10.
//

#ifndef FAST_TOOLS_C_SOURCE_LABEL_ENCODER_H
#define FAST_TOOLS_C_SOURCE_LABEL_ENCODER_H

#include "uthash/uthash.h"

typedef struct UniqueWords {
    char *word;
    int value;
    UT_hash_handle hh;
} uniqueWords;

uniqueWords *get_encoder(char **words, int word_count);

uniqueWords *get_encoder_by_string(char *sample_words, char sep_char);

int * encode_words(uniqueWords ** unique_words, char ** words, int words_count);

int * encode_words_by_string(uniqueWords ** unique_words, char * words, int words_count, char sep_char);

void print_unique_words(uniqueWords **unique_words);

void print_unique_words_summary(uniqueWords ** unique_words);

void save_encoder(uniqueWords **unique_words, char *save_path);

void free_unique_words(uniqueWords **unique_words);

uniqueWords * load_encoder(char * file_path);

#endif //FAST_TOOLS_C_SOURCE_LABEL_ENCODER_H
