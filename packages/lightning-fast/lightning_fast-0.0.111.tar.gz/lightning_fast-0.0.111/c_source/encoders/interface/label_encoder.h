//
// Created by 徐秋实 on 2021/12/9.
//

#ifndef LIGHTNING_FAST_C_ENCODERS_SRC_LABEL_ENCODER_H_
#define LIGHTNING_FAST_C_ENCODERS_SRC_LABEL_ENCODER_H_
#include <unordered_map>
#include "boost/progress.hpp"
#include "pybind11/pybind11.h"

namespace py = pybind11;
namespace encoders {
class LabelEncoder {
 public:
  std::unordered_map<std::string, int> encoder_map;

 public:
  LabelEncoder();

  /// 使用一个一维字符串列表进行fit
  /// \param string_vector
  /// \param n_worker
  void encode1D(const std::vector<std::string> &string_vector);

  /// 将一个一维字符串transform
  /// \param string_vector
  /// \param n_worker
  std::vector<int> transform1D(const std::vector<std::string> &string_vector, int n_worker = 1);

 private:
  /// 将长度等分成工人数
  /// \param length 总长度
  /// \param n_worker 工人数
  /// \return 每一个值为分组的起点与重点，左闭右闭
  static std::vector<std::pair<u_long, u_long>> split1DListByWorkers(u_long length, int n_worker);

  /// 将给定的字符串列表, 进行编码
  /// \param string_vector 输入字符串列表
  /// \param start_end_point 分割后的开始结束位置
  /// \param result_vector 结果列表
  static void singleThreadTransform1d(
      const std::unordered_map<std::string, int> &encoder_map,
      const std::vector<std::string> &string_vector,
      const std::pair<u_long, u_long> &start_end_point,
      std::vector<int> &result_vector
  );
};
}
#endif //LIGHTNING_FAST_C_ENCODERS_SRC_LABEL_ENCODER_H_
