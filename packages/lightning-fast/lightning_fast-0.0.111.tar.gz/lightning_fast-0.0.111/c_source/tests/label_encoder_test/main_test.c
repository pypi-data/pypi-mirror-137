//
// Created by 徐秋实 on 2020/10/10.
//
#include <unistd.h>
#include <locale.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <time.h>
#include <limits.h>
#include "error.h"
#include "common_tools.h"
#include "label_encoder_test.h"
#include <errno.h>


void test_label_encoder(void) {
  clock_t start, finish;
  double duration;
//    int max_length = 100000;
  int max_length = 100;
  int word_length = 3;
  char *sample_chars[] = {"赵", "钱", "孙", "李", "周", "吴", "郑", "王"};
  int char_count = sizeof(sample_chars) / sizeof(char *);
  srand(222); // NOLINT(cert-msc51-cpp)
  char **sample_words = (char **) malloc(sizeof(char *) * max_length);
  char *sample_words_string = (char *) malloc(sizeof(char) * 1000 * 5);
  // 超过1000字符那就出错吧。。。
  char tmp_word[1000];
  char *word_one, *word_two, *word_three;
  for (int i = 0; i < max_length; i++) {
    tmp_word[0] = '\0';
    word_one = sample_chars[(int) (rand()) % char_count]; // NOLINT(cert-msc50-cpp)
    word_two = sample_chars[(int) (rand()) % char_count]; // NOLINT(cert-msc50-cpp)
    word_three = sample_chars[(int) (rand()) % char_count]; // NOLINT(cert-msc50-cpp)
    strcat(tmp_word, word_one);
    strcat(tmp_word, word_two);
    strcat(tmp_word, word_three);
    sample_words[i] = (char *) malloc(sizeof(tmp_word) + 1);
    strcpy(sample_words[i], tmp_word);
    strcat(sample_words_string, word_one);
    strcat(sample_words_string, word_two);
    strcat(sample_words_string, word_three);
    strcat(sample_words_string, "\t");
  }
  print_title("原始数组情况", 50, "blue", '-');
  printf("总共%d个词, 每个词%d个字符\n", max_length, word_length);
  print_title("测试根据字符串数组获取encoder", 50, "blue", '-');
  start = clock();
  uniqueWords *unique_words = get_encoder(sample_words, max_length);
  finish = clock();
  print_title("结果", 50, "blue", '-');
  print_unique_words_summary(&unique_words);
  duration = (double) (finish - start) / CLOCKS_PER_SEC;
  printf("%f seconds\n", duration);
  print_title("测试根据字符串获取encoder", 50, "blue", '-');
  start = clock();
  uniqueWords *unique_words_by_string = get_encoder_by_string(sample_words_string, '\t');
  print_unique_words_summary(&unique_words_by_string);
  finish = clock();
  duration = (double) (finish - start) / CLOCKS_PER_SEC;
  printf("%f seconds\n", duration);
  print_title("序列化并保存encoder到'./tmp/label_encoder.tpl'", 70, "blue", '-');
  char cwd[PATH_MAX];
  if (getcwd(cwd, sizeof(cwd)) != NULL) {
    printf("Current working dir: %s\n", cwd);
  } else {
    perror("getcwd() error");
    exit(1);
  }
  char *last_backslash = strrchr(cwd, '/');
  if (last_backslash) {
    *last_backslash = '\0';
  }
  strcat(cwd, "/tmp/label_encoder.tpl");
  printf("Save path is %s\n", cwd);
  save_encoder(&unique_words, cwd);
  free_unique_words(&unique_words);
  print_title("重新load encoder'./tmp/label_encoder.tpl'\n", 70, "blue", '-');
  uniqueWords *loaded_unique_words = load_encoder(cwd);
  print_unique_words_summary(&loaded_unique_words);
  print_title("测试编码(字符串数组)", 50, "blue", '-');
  int *result = encode_words(&loaded_unique_words, sample_words, max_length);
  draw_int_list(result, max_length);
  print_title("测试编码(字符串)", 50, "blue", '-');
  int *result_string = encode_words_by_string(&loaded_unique_words, sample_words_string, max_length, '\t');
  draw_int_list(result_string, max_length);
}

int main() {
  setlocale(LC_ALL, "");
  print_title("测试label encoder", 100, "yellow", '=');
  test_label_encoder();
  return 0;
}