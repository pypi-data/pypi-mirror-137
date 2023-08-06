import os
os.system("git clone https://github.com/AMKCode/pyseing.git")
os.chdir("./pyseing/src")
os.system("git clone https://github.com/pybind/pybind11.git")

os.chdir("./build")
os.system("cmake ..")
os.system("make")
os.chdir("..")
os.chdir("..")
os.chdir("..")
os.system("cp ./pyseing/src/build/pyseing* .")

import pyseing
