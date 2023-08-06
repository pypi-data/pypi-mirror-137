import os

orig_path = os.getcwd()
install_path = os.path.abspath(__file__)[:-12]
os.chdir(install_path)
lib_path = install_path + "/pyseing/src/build/pyseing*"

if not os.path.isdir("pyseing"):
    os.system("git clone https://github.com/AMKCode/pyseing.git")
    os.chdir("./pyseing/src")
    os.system("git clone https://github.com/pybind/pybind11.git")

    os.chdir("./build")
    os.system("cmake ..")
    os.system("make")

   # os.chdir("..")
   # os.chdir("..")
   # os.chdir("..")
   # os.system("cp ./pyseing/src/build/pyseing* .")

os.chdir(orig_path)
os.system("cp " + lib_path + " .")

import pyseing
