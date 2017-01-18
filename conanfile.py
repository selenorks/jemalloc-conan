from conans import ConanFile, tools
import os
from conans.tools import download, unzip, replace_in_file
from conans import CMake


class JeMallocConan(ConanFile):
    name = "jemalloc"
    version = "4.3.1"
    ZIP_FOLDER_NAME = "jemalloc-cmake-jemalloc-cmake.%s" % version
    settings = "os", "arch", "compiler", "build_type"

    exports = ["CMakeLists.txt", "FindJemalloc.cmake"]
    description = "jemalloc is a general purpose malloc(3) implementation that emphasizes fragmentation avoidance and scalable concurrency support."
    license="https://github.com/jemalloc/jemalloc/blob/dev/COPYING"
    url = "http://github.com/selenorks/jemalloc-conan"
    
    def system_requirements(self):
        self.global_system_requirements=True
        if self.settings.os == "Linux":
            self.output.warn("'libudev' library is required in your computer. Enter sudo password if required...")
            self.run("sudo apt-get install libudev0 libudev0:i386 || true ")
            self.run("sudo apt-get install libudev1 libudev1:i386 || true ")
            self.run("sudo apt-get install libudev-dev libudev-dev:i386 || true ")
            self.run("sudo apt-get install libxml2-dev libxml2-dev:i386 || true ")

    def source(self):
        zip_name = "jemalloc-cmake.%s.zip" % self.version
        major = ".".join(self.version.split("."))
        import urllib
        urllib.urlretrieve ("https://github.com/jemalloc/jemalloc-cmake/archive/jemalloc-cmake.%s.zip" % self.version, zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """
        cmake = CMake(self.settings)
        build_dir = self.ZIP_FOLDER_NAME + '/build'
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)

        os.chdir(build_dir)
        self.run('cmake .. %s' % (cmake.command_line))
        self.run("cmake --build . %s" % (cmake.build_config))

    def package(self):
        """ Define your conan structure: headers, libs, bins and data. After building your
            project, this method is called to create a defined structure:
        """
        
        self.copy("FindJemalloc.cmake", ".", ".")
        self.copy(pattern="*.h", dst="include", src="%s/include" % (self.ZIP_FOLDER_NAME), keep_path=True)

        # Copying static and dynamic libs
        if self.settings.os == "Windows":
            src = self.ZIP_FOLDER_NAME + '/build'
            bin = src + "/" + str(self.settings.build_type)
            self.copy(pattern="*.lib", dst="lib", src=bin, keep_path=False)

        else:
            if self.options.shared:
                if self.settings.os == "Macos":
                    self.copy(pattern="*.dylib", dst="lib", keep_path=False)
                else:
                    self.copy(pattern="*.so", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
                    self.copy(pattern="*.so.*", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
            else:
                self.copy(pattern="*.a", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["jemalloc"]
