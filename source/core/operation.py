from .collection import ImgCollection


class OpBase:
    def __init__(self, *args, **kwargs):
        self.op_name = self.__class__.__name__
        self.op_ex = None
        self.op_func = self.process
        self.op_params = (args, kwargs)

        self.init(*args, **kwargs)

    def init(self, *args, **kwargs):
        pass

    def execute(self):
        raise NotImplementedError

    def process(self, *args, **kwargs):
        raise NotImplementedError


class OpInput(OpBase):
    def __init__(self, *args, **kwargs):
        super(OpInput, self).__init__(*args, **kwargs)

    def __call__(self, ex):
        raise ValueError("input operations do not accept inputs")

    def execute(self):
        if not self.op_func:
            raise ValueError("operation is not defined")
        if not self.op_params:
            return self.op_func()
        return self.op_func(*self.op_params[0], **self.op_params[1])


class OpOneToOne(OpBase):
    def __init__(self, *args, **kwargs):
        super(OpOneToOne, self).__init__(*args, **kwargs)

    def __call__(self, ex):
        self.op_ex = ex
        return self

    def execute(self):
        if not (self.op_ex and self.op_func and self.op_params):
            raise ValueError("operation is not defined")

        collection = self.op_ex.execute()
        if not isinstance(collection, ImgCollection):
            raise ValueError(f"{self.op_name} expects the input type ImgCollection, but got {type(collection)} from {self.op_ex.op_name}")

        for img in collection:
            self.op_func(img, *self.op_params[0], **self.op_params[1])
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
