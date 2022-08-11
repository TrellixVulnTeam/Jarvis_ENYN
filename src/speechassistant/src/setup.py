import os
import traceback
from fnmatch import fnmatch

from Cython.Build import cythonize
from setuptools import setup


def build_all_files():
    root = ""
    pattern = "*.py"

    for path, subdirs, files in os.walk(root):
        for name in files:
            try:
                if fnmatch(name, pattern) and not "main" in name:
                    file_with_path = os.path.join(path, name)
                    os.rename(file_with_path, name + "x")
                    setup(
                        name="JarvisBuild",
                        ext_modules=cythonize(file_with_path + "x"),
                        zip_safe=False,
                    )
                    print(name + "x built.")
            except Exception:
                traceback.print_exc()


# if __name__ == "__main__":
#     build_all_files()
