class Char(str):
    def __new__(cls, value):
        if not isinstance(value, str):
            raise TypeError(f'Cannot assign {type(value)} to Char. It need of type str')
        if len(value) > 1:
            raise ValueError('Char can be initilized with single character.')
        return super().__new__(cls, value)
