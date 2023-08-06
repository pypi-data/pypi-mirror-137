import subprocess
import sys

from lightning_fast.config import ROOT_PATH

source_dir = ROOT_PATH / ".." / "c_source"
target_dir = ROOT_PATH / "c_dynamic_library"
build_dir = source_dir / "cmake-build-c-dynamic-library"
build_dir.mkdir(parents=True, exist_ok=True)

subprocess.check_call(
    [
        "cmake",
        "..",
        f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={target_dir}",
        f"-DPYTHON_EXECUTABLE={sys.executable}",
        f"-DCMAKE_BUILD_TYPE=Release"
    ],
    cwd=build_dir,
)
subprocess.check_call("make", cwd=build_dir)


if __name__ == "__main__":
    from lightning_fast.c_dynamic_library.encoders import LabelEncoder
    from lightning_fast.c_dynamic_library.encoders import OneDStringVector

    from tests.time_statistic.old_encoder_statistic import LabelEncoderComparison

    total_test_words = LabelEncoderComparison.generate_words(
        ["赵", "钱", "孙", "李", "周", "吴", "郑", "王"], 0, 7, 100
    )
    input_string_list = OneDStringVector(total_test_words)
    encoder = LabelEncoder()
    encoder.encode_1d(input_string_list, 1)
    print(encoder.label_map)
