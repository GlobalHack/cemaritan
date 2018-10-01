import sys
import json

print("We loggin python, yo!")

arg1 = float(sys.argv[1])
arg2 = float(sys.argv[2])
arg3 = sys.argv[3]

result = arg1 * arg2

print(str(result))
print(result, arg3)
sys.stdout.flush()
