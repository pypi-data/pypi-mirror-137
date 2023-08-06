class SingletonMeta(type):
    """
    使用此类作为metaclass则类会变成单例
    此类根据类的名字、实例化时传入的参数进行去重。即如果传入不同的参数则会形成不同的单例
    """

    _instances = {}

    def __call__(cls, *args, **kwargs) -> object:
        # kwd_mark = object()
        # key = args + (kwd_mark, cls.__name__) + tuple(sorted(kwargs.items()))
        key = str(args) + str((cls.__name__,)) + str(tuple(sorted(kwargs.items())))
        if key not in cls._instances:
            cls._instances[key] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instances[key]

    @classmethod
    def clear(mcs):
        mcs._instances = {}
