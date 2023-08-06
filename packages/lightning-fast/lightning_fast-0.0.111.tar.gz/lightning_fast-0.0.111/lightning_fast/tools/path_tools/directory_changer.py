import pathlib
import re


class DirectoryChanger:
    @classmethod
    def get_new_root_directory(
        cls,
        origin_path: pathlib.Path,
        source_dir: pathlib.Path,
        target_dir: pathlib.Path,
        create: bool = True,
    ) -> pathlib.Path:
        """
        更换一个根目录。
        从一个origin_path原始路径相对于source_dir的路径中获得相对于另一个target_dir的路径
        比如当前脚本相对于项目为/project_dir/package_dir/a.py, 数据文件目录为/data
        我们想要拿到/data/package_dir/a/这个目录。
        通常可以配合ClassDirectory使用
        :param origin_path: 需要变更的目录
        :param source_dir: 源目录
        :param target_dir: 新源目录
        :param create: 是否创建新目录
        :return: 新目录
        """
        relative_source_dir = origin_path.relative_to(source_dir)
        relative_target_dir = target_dir / relative_source_dir
        relative_target_dir = pathlib.Path(
            re.sub(r"\.[^.\\/]*?$", "", str(relative_target_dir))
        )
        if create:
            relative_target_dir.mkdir(parents=True, exist_ok=True)
        return relative_target_dir
