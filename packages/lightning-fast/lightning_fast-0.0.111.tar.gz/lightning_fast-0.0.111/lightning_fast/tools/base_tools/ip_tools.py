import socket


class IpTools:
    """
    一些辅助ip查询相关的工具
    """

    @classmethod
    def get_ip(cls) -> str:
        """
        查询本机的对外ip
        :return: ip字符串
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable, A type private address.
            s.connect(("10.255.255.255", 1))
            ip = s.getsockname()[0]
        except OSError:
            ip = "127.0.0.1"
        finally:
            s.close()
        return ip
