[![Build status](https://ci.appveyor.com/api/projects/status/ndo0i5yvg830oii6?svg=true)](https://ci.appveyor.com/project/selenorks/jemalloc-conan)



# conan-jemalloc

[Conan.io](https://conan.io) package for JeMalloc library

The packages generated with this **conanfile** can be found in [conan.io](https://conan.io/source/jemalloc/1.11.1/lasote/stable).

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py

## Upload packages to server

    $ conan upload jemalloc/1.11.5@selenorks/stable --all
    
## Reuse the packages

### Basic setup

    $ conan install jemalloc/1.11.5@selenorks/stable
    
### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*
    
    [requires]
    jemalloc/1.11.1@selenorks/stable

    [options]
    zlib:shared=true # false
    
    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:</small></span>

    conan install 

Project setup installs the library (and all his dependencies) and generates the files *conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that you need to link with your dependencies.
