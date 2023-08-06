//
// Created by 徐秋实 on 2021/12/9.
//
#include <mutex>
#include <thread>
#include <future>
#include <iostream>
#include "../interface/label_encoder.h"

encoders::LabelEncoder::LabelEncoder() : encoder_map(std::unordered_map<std::string, int>()) {}

void encoders::LabelEncoder::encode1D(const std::vector<std::string> &string_vector) {
  // 这里的序号开始位置设定为当前的遍历开始位置，这样之后合并的时候只需要比较大小取用最小的就可以知道每个词在整体中最早出现的位置是什么。
  auto bar = boost::progress_display(string_vector.size());
  u_long current_appear_index = 0;
  for (const auto &word: string_vector) {
    auto existed_pair = this->encoder_map.find(word);
    if (existed_pair == this->encoder_map.end()) {
      this->encoder_map.emplace(std::make_pair(word, current_appear_index));
      current_appear_index++;
    }
    ++bar;
  }
}

std::vector<int> encoders::LabelEncoder::transform1D(const std::vector<std::string> &string_vector, int n_worker) {
  auto start_end_points = encoders::LabelEncoder::split1DListByWorkers(string_vector.size(), n_worker);
  std::vector<std::thread> workers = std::vector<std::thread>();
  std::vector<int> result_vector(string_vector.size());
  std::vector<std::unordered_map<std::string, int>>
      result_map_list = std::vector<std::unordered_map<std::string, int>>();
  for (int i = 0; i < n_worker; i++) {
    workers.emplace_back(
        std::thread(
            &encoders::LabelEncoder::singleThreadTransform1d,
            std::ref(this->encoder_map),
            std::ref(string_vector),
            std::ref(start_end_points[i]),
            std::ref(result_vector)
        )
    );
  }
  for (auto &worker: workers) {
    worker.join();
  }
  return result_vector;
}

std::vector<std::pair<u_long, u_long>> encoders::LabelEncoder::split1DListByWorkers(const u_long length,
                                                                                    const int n_worker) {
  unsigned long split_size = length / n_worker;
  auto start_end_points = std::vector<std::pair<u_long, u_long>>();
  for (int i = 0; i < n_worker; i++) {
    start_end_points.emplace_back(
        i * split_size,
        (i + 1) * split_size - 1
    );
  }
  if (start_end_points[start_end_points.size() - 1].second < length - 1) {
    start_end_points[start_end_points.size() - 1].second = length - 1;
  }
  return start_end_points;
}

void encoders::LabelEncoder::singleThreadTransform1d(
    const std::unordered_map<std::string, int> &encoder_map,
    const std::vector<std::string> &string_vector,
    const std::pair<u_long, u_long> &start_end_point,
    std::vector<int> &result_vector
) {
  for (u_long word_index = start_end_point.first; word_index < start_end_point.second + 1; word_index++) {
    auto existed_pair = encoder_map.find(string_vector[word_index]);
    if (existed_pair != encoder_map.end()) {
      result_vector[word_index] = existed_pair->second;
    } else {
      result_vector[word_index] = -1;
    }
  }

}
