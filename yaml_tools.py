
import yaml


def load_yaml(file_path):
    """
    从 yaml 文件读取配置
    :param file_path:
    :return:
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)
    except Exception as e:
        print(f"读取配置文件失败: {e}")
        return None


def save_yaml(file_path, data):
    """
    保存配置到 yaml 文件
    :param file_path:
    :param data:
    :return:
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True)
    except Exception as e:
        print(f"保存配置文件失败: {e}")
        return None
