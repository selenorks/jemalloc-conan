import os
import platform
import sys

if __name__ == "__main__":
    os.system('conan export selenorks/stable')
   
    def test(settings):
        argv =  " ".join(sys.argv[1:])
        command = "conan test_package %s %s" % (settings, argv)
        retcode = os.system(command)
        if retcode != 0:
            exit("Error while executing:\n\t %s" % command)


    if platform.system() == "Windows":
        for compiler_version in ("14",):
            compiler = '-s compiler="Visual Studio" -s compiler.version=%s ' % compiler_version
            # Static x86
            test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MDd')
            test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MD')
    
            # Static x86_64
            test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MDd')
            test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MD')

    else:  # Compiler and version not specified, please set it in your home/.conan/conan.conf (Valid for Macos and Linux)
        if not os.getenv("TRAVIS", False):  
            # Static x86
            test('-s arch=x86 -s build_type=Debug')
            test('-s arch=x86 -s build_type=Release')
    
            # Shared x86
            test('-s arch=x86 -s build_type=Debug')
            test('-s arch=x86 -s build_type=Release')

        # Static x86_64
        test('-s arch=x86_64 -s build_type=Debug')
        test('-s arch=x86_64 -s build_type=Release')

        # Shared x86_64
        test('-s arch=x86_64 -s build_type=Debug')
        test('-s arch=x86_64 -s build_type=Release')
