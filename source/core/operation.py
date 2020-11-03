from .collection import ImgCollection

# TODO: auto-generate operation name
class OpBase:
    op_id = 0

    def __init__(self, *args, **kwargs):
        self.op_name = str(self.__class__.op_id) + "_" + self.__class__.__name__
        OpBase.op_id += 1

        self.op_ex = None
        self.op_func = self.process
        self.op_params = (args, kwargs)

        self.init(*args, **kwargs)

    def __call__(self, ex):
        self.op_ex = ex
        return self

    def init(self, *args, **kwargs):
        pass

    def execute(self):
        raise NotImplementedError

    def process(self, *args, **kwargs):
        raise NotImplementedError

    def op_ex_check(self):
        if not self.op_ex:
            raise AttributeError(f"op_ex is not defined for {self.op_name}")

    def op_func_check(self):
        if not self.op_func:
            raise AttributeError(f"op_func is not defined for {self.op_name}")

    def op_params_check(self):
        if not self.op_params:
            raise AttributeError(f"op_params is not defined for {self.op_name}")


def op_execution_profile(execute):
    def wrapper(self):
        ret = execute(self)
        print(f"executed operation {self.op_name}")
        return ret
    return wrapper


class OpInput(OpBase):
    def __init__(self, *args, **kwargs):
        super(OpInput, self).__init__(*args, **kwargs)

    def __call__(self, ex):
        raise TypeError("OpInput does not accept any inputs")

    @op_execution_profile
    def execute(self):
        self.op_func_check()
        return self.op_func(*self.op_params[0], **self.op_params[1])


class OpOutput(OpBase):
    @op_execution_profile
    def execute(self):
        self.op_ex_check()
        self.op_func_check()

        collection = self.op_ex.execute()
        self.op_func(collection, *self.op_params[0], **self.op_params[1])
        return collection


class OpOneToOne(OpBase):
    @op_execution_profile
    def execute(self):
        self.op_ex_check()
        self.op_func_check()

        collection = self.op_ex.execute()
        if not isinstance(collection, ImgCollection):
            raise TypeError(f"{self.op_name} expects the input type ImgCollection, but got {type(collection)} from {self.op_ex.op_name}")

        for imgelem in collection:
            self.op_func(imgelem, *self.op_params[0], **self.op_params[1])
        return collection


class OpOneToMany(OpBase):
    def __init__(self, *args, **kwargs):
        super(OpOneToMany, self).__init__(*args, **kwargs)
        self.num_outputs = 1

    # TODO: support multiple output Ops
    def __call__(self, ex):
        self.op_ex = ex
        return self

    @property
    def num_outputs(self):
        return self.__num_outputs

    @num_outputs.setter
    def num_outputs(self, num_outputs):
        self.__num_outputs = num_outputs
