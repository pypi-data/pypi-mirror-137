//
// Created by 徐秋实 on 2021/12/13.
//
#include <cstdlib>
#include <random>
#include "label_encoder_test.h"
void LabelEncoderTest::basic_test() {
  int max_length = 2000000;
//  srand(222); // NOLINT(cert-msc51-cpp)
  std::vector<std::string> sample_chars = {
      "a", "b", "c", "d", "e", "f", "g", "h", "i",
      "j", "k", "l", "m", "n", "o", "p", "q", "r",
      "s", "t", "u", "v", "w", "x", "y", "z", "A",
      "B", "C", "D", "E", "F", "G", "H", "I", "J",
      "K", "L", "M", "N", "O", "P", "Q", "R", "S",
      "T", "U", "V", "W", "X", "Y", "Z",
  };
  u_long char_count = sample_chars.size();
  std::vector<std::string> sample_words = std::vector<std::string>();
  for (int i = 0; i < max_length; i++) {
    std::string tmp_word;
    for (int j = 0; j < rand() % 8 + 2; j++) { // NOLINT(cert-msc50-cpp)
      tmp_word += sample_chars[(int) (rand()) % char_count]; // NOLINT(cert-msc50-cpp)
    }
    sample_words.push_back(tmp_word);
  }
  auto test_encoder = encoders::LabelEncoder();
  test_encoder.encode1D(sample_words);
  auto transform_result = test_encoder.transform1D(sample_words);
}
