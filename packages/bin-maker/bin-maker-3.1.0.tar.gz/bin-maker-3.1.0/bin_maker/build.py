import json
import os
import shutil
from distutils.command.build_ext import build_ext
from multiprocessing import cpu_count
from pathlib import Path
from Cython.Build import cythonize
from setuptools import find_packages, Extension, setup
import re

if os.path.exists('./build'):
    print('found exist build directory,remove it')
    shutil.rmtree('./build')

config_entity = None
if os.path.exists('./bin_maker.json'):
    print('found bin_maker.json,load extra config')

    with open('./bin_maker.json', 'r', encoding='utf-8') as file:
        config_entity = json.load(file)

local_packages = find_packages()

if config_entity is not None:
    for modules in config_entity['exclude_modules']:
        if modules in local_packages:
            print(f'excluting modules:{modules}')
            local_packages.remove(modules)

extentions = []
for obj in local_packages:
    dir_path = os.path.join('.', obj.replace(".", "/"))
    for name in os.listdir(dir_path):
        file_path = f'{dir_path}/{name}'
        if "__" in name or '.py' not in name or os.path.isdir(file_path):
            print(f'skip :{file_path}')
            continue

        if config_entity is not None and len(list(filter(lambda x: re.match(x, file_path), config_entity['exclude_files']))) > 0:
            print(f'skip path:{file_path}')
            continue

        extentions.append(Extension(
            obj + '.' + name.replace('.py', ''), ["%s/%s" % (obj.replace(".", "/"), name)]))


class KitBuildExt(build_ext):
    def run(self):
        build_ext.run(self)

        build_dir = Path(self.build_lib)
        root_dir = Path(__file__).parent

        target_dir = build_dir if not self.inplace else root_dir

        """
        copy __init__.py to cython compile path,otherwise compile will fail
        """
        for obj in local_packages:
            dir_path = obj.replace(".", "/")
            self.copy_file(Path(dir_path) / "__init__.py",
                           os.getcwd(), target_dir)

    def copy_file(self, path, source_dir, destination_dir):
        if not (source_dir / path).exists():
            return

        shutil.copyfile(str(source_dir / path), str(destination_dir / path))


def build():
    setup(
        name='bin-maker',
        version='3.1.0',
        packages=local_packages,
        platforms="any",
        ext_modules=cythonize(
            extentions,
            build_dir="build",
            annotate=True,
            compiler_directives=dict(always_allow_keywords=True),
            language_level=3,
            nthreads=cpu_count()
        ),
        cmdclass=dict(build_ext=KitBuildExt),
    )
