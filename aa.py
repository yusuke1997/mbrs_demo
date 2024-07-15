from dataclasses import dataclass

@dataclass
class Arguments:
    arg1: int
    arg2: str
    arg3: float

def my_function(args: Arguments):
    print(f"arg1: {args.arg1}, arg2: {args.arg2}, arg3: {args.arg3}")

# 使用例
args = Arguments(arg1=10, arg2="hello", arg3=3.14, arg4 = 'aaa')
my_function(args)
