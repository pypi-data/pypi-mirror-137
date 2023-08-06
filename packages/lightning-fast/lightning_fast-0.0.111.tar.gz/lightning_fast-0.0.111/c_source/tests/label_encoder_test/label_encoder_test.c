//
// Created by 徐秋实 on 2020/10/10.
//
#include <stdio.h>
#include <string.h>
#include "error.h"
#include "uthash/uthash.h"
#include "tpl/tpl.h"
#include "label_encoder_test.h"
#include <errno.h>

//extern int errno;

static uniqueWords *find_word(uniqueWords **unique_words, char *word) {
    uniqueWords *tmp;
    HASH_FIND_STR(*unique_words, word, tmp); // NOLINT(hicpp-multiway-paths-covered,hicpp-signed-bitwise)
    return tmp;
}

static void add_word(uniqueWords **unique_words, char *new_word, int *counter) {
    uniqueWords *new_kv = malloc(sizeof(uniqueWords));
    uniqueWords *tmp = find_word(unique_words, new_word);
    if (NULL == tmp) {
        new_kv->word = malloc(sizeof(char) * (strlen(new_word) + 1));
        strcpy(new_kv->word, new_word);
        *counter += 1;
        new_kv->value = *counter;
        HASH_ADD_KEYPTR( // NOLINT(hicpp-multiway-paths-covered,hicpp-signed-bitwise)
                hh,
                *unique_words,
                new_kv->word,
                strlen(new_kv->word),
                new_kv
        );
    }
}

static void flatten_add_word(uniqueWords **unique_words, char *new_word, int value) {
    uniqueWords *new_kv = malloc(sizeof(uniqueWords));
    uniqueWords *tmp = find_word(unique_words, new_word);
    if (NULL == tmp) {
        new_kv->word = malloc(sizeof(char) * (strlen(new_word) + 1));
        strcpy(new_kv->word, new_word);
        new_kv->value = value;
        HASH_ADD_KEYPTR( // NOLINT(hicpp-multiway-paths-covered,hicpp-signed-bitwise)
                hh,
                *unique_words,
                new_kv->word,
                strlen(new_kv->word),
                new_kv
        );
    }
}

void free_unique_words(uniqueWords **unique_words) {
    uniqueWords *s;
    uniqueWords *tmp;
    HASH_ITER(hh, *unique_words, s, tmp) {
        free(s->word);
        s->word = NULL;
        free(s);
        s = NULL;
    }
    *unique_words = NULL;
}

void print_unique_words(uniqueWords **unique_words) {
    uniqueWords *s;
    uniqueWords *tmp;
    printf("{\n");
    HASH_ITER(hh, *unique_words, s, tmp) {
        printf("\t%s: %d,\n", s->word, s->value);
    }
    printf("}\n");
}

void print_unique_words_summary(uniqueWords **unique_words) {
    int max_count = 10;
    int counter = 0;
    uniqueWords *s;
    uniqueWords *tmp;
    printf("{\n");
    HASH_ITER(hh, *unique_words, s, tmp) {
        if (counter < max_count) {
            printf("\t%s: %d,\n", s->word, s->value);
            counter++;
        } else {
            printf("\t...\n");
            break;
        }
    }
    printf("}\n");
}

uniqueWords *get_encoder(char **words, int word_count) {
    uniqueWords *unique_word = NULL;
    int counter = 0;
    for (int i = 0; i < word_count; i++) {
        add_word(&unique_word, words[i], &counter);
    }
    return unique_word;
}

uniqueWords *get_encoder_by_string(char *sample_words, char sep_char) {
    uniqueWords *unique_word = NULL;
    int max_word_length = 1000;
    char * sample_words_copy = sample_words;
    char * tmp = malloc(sizeof(char) * max_word_length); // 字符串超过1000直接报错
    int tmp_index = 0;
    int counter = 0;
    while(*sample_words_copy != '\0') {
        if (*sample_words_copy != sep_char) {
            *(tmp + tmp_index) = *sample_words_copy;
            tmp_index += 1;
        } else {
            if (tmp_index > max_word_length) {
                errno = CUSTOM_ERROR;
                fprintf(stderr, "单词长度超过1000, 现在为%d", tmp_index + 1);
                exit(errno);
            }
            *(tmp + tmp_index) = '\0';
            add_word(&unique_word, tmp, &counter);
            tmp_index = 0;
        }
        sample_words_copy += 1;
    }
    if (tmp_index > max_word_length) {
        errno = CUSTOM_ERROR;
        fprintf(stderr, "单词长度超过1000, 现在为%d", tmp_index + 1);
        exit(errno);
    }
    *(tmp + tmp_index) = '\0';
    add_word(&unique_word, tmp, &counter);
    return unique_word;
}

int * encode_words(uniqueWords ** unique_words, char ** words, int words_count) {
    int * result = malloc(sizeof(int) * words_count);
    uniqueWords * tmp;
    for (int i = 0; i < words_count; i ++ ) {
       tmp = find_word(unique_words, words[i]);
       if (NULL == tmp) {
           result[i] = -1;
       } else {
           result[i] = tmp->value;
       }
    }
    return result;
}

int * encode_words_by_string(uniqueWords ** unique_words, char * words, int words_count, char sep_char) {
    int * result = malloc(sizeof(int) * words_count);
    uniqueWords * tmp;
    int max_word_length = 1000;
    char * sample_words_copy = words;
    char * tmp_word = malloc(sizeof(char) * max_word_length); // 字符串超过1000直接报错
    int tmp_word_index = 0;
    int result_counter = 0;
    while(*sample_words_copy != '\0') {
        if (*sample_words_copy != sep_char) {
            *(tmp_word + tmp_word_index) = *sample_words_copy;
            tmp_word_index += 1;
        } else {
            if (tmp_word_index > max_word_length) {
                errno = CUSTOM_ERROR;
                fprintf(stderr, "单词长度超过1000, 现在为%d", tmp_word_index + 1);
                exit(errno);
            }
            *(tmp_word + tmp_word_index) = '\0';
            tmp = find_word(unique_words, tmp_word);
            if (NULL == tmp) {
                result[result_counter] = -1;
            } else {
                result[result_counter] = tmp->value;
            }
            result_counter += 1;
            tmp_word_index = 0;
        }
        sample_words_copy += 1;
    }
    if (tmp_word_index > max_word_length) {
        errno = CUSTOM_ERROR;
        fprintf(stderr, "单词长度超过1000, 现在为%d", tmp_word_index + 1);
        exit(errno);
    }
    *(tmp_word + tmp_word_index) = '\0';
    tmp = find_word(unique_words, tmp_word);
    if (NULL == tmp) {
        result[result_counter] = -1;
    } else {
        result[result_counter] = tmp->value;
    }
    return result;
}

void save_encoder(uniqueWords **unique_words, char *save_path) {
    int max_word_length = 100;
    uniqueWords *s;
    uniqueWords *tmp;
    tpl_node *tn;
    char *word = malloc(sizeof(char) * (max_word_length + 1)); // 大于100长度的词直接报错;
    int value;
    tn = tpl_map("A(si)", &word, &value);
    HASH_ITER(hh, *unique_words, s, tmp) {
        if (strlen(s->word) > 100) {
            errno = CUSTOM_ERROR;
            fprintf(stderr, "单词长度超过100, 现在为%d", (int) strlen(s->word));
            exit(errno);
        } else {
            strcpy(word, s->word);
            value = s->value;
            tpl_pack(tn, 1);
        }
    }
    tpl_dump(tn, TPL_FILE, save_path); // NOLINT(hicpp-signed-bitwise)
    tpl_free(tn);
}


uniqueWords * load_encoder(char * file_path) {
    int max_word_length = 100;
    uniqueWords *unique_word = NULL;
    tpl_node *tn;
    char *word = malloc(sizeof(char) * (max_word_length + 1)); // 大于100长度的词直接报错;
    int value;
    tn = tpl_map("A(si)", &word, &value);
    tpl_load(tn, TPL_FILE, file_path); // NOLINT(hicpp-signed-bitwise)

    while ( tpl_unpack(tn,1) > 0 ) {
        flatten_add_word(&unique_word, word, value);
    }
    tpl_free(tn);
    return unique_word;
}
