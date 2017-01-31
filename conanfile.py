from conans import ConanFile, tools
import os
from conans.tools import download, unzip, replace_in_file
from conans import CMake
import platform

class JeMallocConan(ConanFile):
    name = "jemalloc"
    version = "4.3.1"
    ZIP_FOLDER_NAME = "jemalloc-cmake-jemalloc-cmake.%s" % version

        
    settings = "os", "arch", "compiler", "build_type"

    exports = ["CMakeLists.txt", "FindJemalloc.cmake"]
    description = "jemalloc is a general purpose malloc(3) implementation that emphasizes fragmentation avoidance and scalable concurrency support."
    license="https://github.com/jemalloc/jemalloc/blob/dev/COPYING"
    url = "http://github.com/selenorks/jemalloc-conan"

    def source(self):
        self.run("git clone https://github.com/jemalloc/jemalloc-cmake.git %s -b jemalloc-cmake.%s" % (self.ZIP_FOLDER_NAME, self.version))

    def build(self):
        """ Define your project building. You decide the way of building it
            to reuse it later in any other project.
        """

        if self.settings.os == "Windows":
            cmake = CMake(self.settings)
            build_dir = self.ZIP_FOLDER_NAME + '/build'
            if not os.path.exists(build_dir):
                os.makedirs(build_dir)

            os.chdir(build_dir)
            self.run('cmake .. %s' % (cmake.command_line))
            self.run("cmake --build . %s" % (cmake.build_config))
        elif self.settings.os == "iOS":
            opt = "--host=arm-apple-darwin"
            sdk = "iphoneos"
            arch = self.settings.arch if self.settings.arch != "armv8" else "arm64"
            host_flags = "-arch %s -miphoneos-version-min=5.0 -isysroot $(xcrun -sdk %s --show-sdk-path)" % (arch, sdk)
            flags = " -O3 -g " if str(self.info.settings.build_type) == "Release" else "-O0 -g "
            exports = [ "HOST_FLAGS=\"%s\"" % host_flags,
                "CHOST=\"arm-apple-darwin\"",
                "CC=\"$(xcrun -find -sdk %s clang)\"" % (sdk),
                "CXX=\"$(xcrun -find -sdk %s clang++)\"" % (sdk),
                "CPP=\"$(xcrun -find -sdk %s cpp)\"" % (sdk),
                "LDFLAGS=\"%s\"" % host_flags,
                "CXXFLAGS=\"%s %s\"" % (host_flags, flags),
                "CFLAGS=\"%s %s\"" % (host_flags, flags)
                ]

            self.run("cd %s && %s ./configure %s --disable-libxml2" % (self.ZIP_FOLDER_NAME, " ".join(exports), opt))
            self.run("cd %s && %s make" % (self.ZIP_FOLDER_NAME, " ".join(exports)))

        else:
            compile_flag = "-m32 " if self.settings.arch == "x86" else ""
            compile_flag += " -fPIC "
            compile_flag += " -O3 -g " if str(self.info.settings.build_type) == "Release" else "-O0 -g "
            linker_flag = "-m32 " if self.settings.arch == "x86" else ""
            compile_flag += "-mmacosx-version-min=10.7 " if self.settings.os == "Macos" else ""
            self.run("cd %s && CFLAGS='%s' CXXFLAGS='%s' LDFLAGS='%s' ./autogen.sh --with-jemalloc-prefix" 
                     % (self.ZIP_FOLDER_NAME, compile_flag, compile_flag, linker_flag))
            self.run("cd %s && make" % self.ZIP_FOLDER_NAME)

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
            if self.settings.os == "Macos":
                self.copy(pattern="*.dylib", dst="lib", keep_path=False)
            else:
                self.copy(pattern="*.so", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
                self.copy(pattern="*.so.*", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)
            self.copy(pattern="*.a", dst="lib", src=self.ZIP_FOLDER_NAME, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["jemalloc"]
