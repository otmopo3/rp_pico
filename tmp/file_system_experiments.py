import os

cur_dir = os.getcwd()
print(cur_dir)

print(os.stat(cur_dir))

for dr in os.ilistdir(cur_dir):
    print(dr)