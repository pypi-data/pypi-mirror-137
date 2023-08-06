from setuptools import setup, find_packages, Extension
import pybind11
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))
#cpp_args = ['-std=c++11', '-stdlib=libc++', '-mmacosx-version-min=10.7']



fcc_module = Extension(
    'functionc',
    sources=['functionc.cpp'],
    include_dirs=[pybind11.get_include(), 
    
                  "include"],
    language='c++',
    #extra_compile_args=cpp_args,
    extra_compile_args=['-std=c++14', '-stdlib=libc++', '-mmacosx-version-min=10.7'],
    )

setup(
    name='topic_cluster_visualizer',
    version='0.2',
    description='',
    url = 'https://github.com/lyric2249/topicclustervisualizer',
    packages=find_packages(exclude=['tests']),
    install_requires = ['plotly >= 4.14.3', 'factor-analyzer >= 0.4.0'],
    ext_modules=[fcc_module],
)


#import 

#os.path.abspath(__file__)

#import os
#import os.path
#my_path = os.path.abspath()
#os.pardir
