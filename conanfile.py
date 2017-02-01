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
        self.run("git clone https://github.com/jemalloc/jemalloc-cmake.git %s -b jemalloc-cmake.%s --depth 1" % (self.ZIP_FOLDER_NAME, self.version))

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
            platform_define =  "__arm__" if self.settings.arch != "armv8" else  "__arm64__"
            host_flags = "-arch %s -miphoneos-version-min=5.0 -isysroot $(xcrun -sdk %s --show-sdk-path) -I$(xcrun -sdk %s --show-sdk-path)/usr/include/ -D%s" % (arch, sdk, sdk, platform_define)
            flags = " -O3 -g " if str(self.info.settings.build_type) == "Release" else "-O0 -g "
            exports = [ "HOST_FLAGS=\"%s\"" % host_flags,
                "CHOST=\"arm-apple-darwin\"",
                "CC=\"$(xcrun -find -sdk %s clang)\"" % (sdk),
                "CXX=\"$(xcrun -find -sdk %s clang++)\"" % (sdk),
                "LDFLAGS=\"%s\"" % host_flags,
                "CPPFLAGS=\"%s %s\"" % (host_flags, flags),
                "CFLAGS=\"%s %s\"" % (host_flags, flags)
                ]

            self.run("cd %s && %s ./autogen.sh %s" % (self.ZIP_FOLDER_NAME, " ".join(exports), opt))
            self.run("cd %s && %s make" % (self.ZIP_FOLDER_NAME, " ".join(exports)))

        elif self.settings.os == "Android":
            ndk_path = os.getenv("ANDROID_NDK")
            print("ANDROID_NDK=%s" % ndk_path)
            if not ndk_path:
                print("Please set envirement varible ANDROID_NDK")
                sys.exit(-1)

            if self.settings.arch == "armv7":
                flags = "-DANDROID \
-isystem ${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm/usr/include \
-isystem ${ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/include \
-isystem ${ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/libs/armeabi-v7a/include \
-isystem ${ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/include/backward \
-fexceptions -Wno-psabi --sysroot=${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm -funwind-tables -finline-limit=64 -fsigned-char -no-canonical-prefixes -march=armv7-a -mfloat-abi=softfp -mfpu=neon -fdata-sections -ffunction-sections -Wa,--noexecstack  -Wl,--fix-cortex-a8 -Wl,--no-undefined -Wl,--gc-sections -Wl,-z,noexecstack -Wl,-z,relro -Wl,-z,now -Wl,-z,nocopyreloc -fdiagnostics-color=always -mthumb -fomit-frame-pointer -fno-strict-aliasing -fPIC"
                exports = [
                    "PLATFORM=android-16" 
                    "CC=\"${ANDROID_NDK}/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin/arm-linux-androideabi-gcc\"",
                    "CXX=\"${ANDROID_NDK}/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin/arm-linux-androideabi-g++\"",
                    "LDFLAGS=\"-fPIC -L${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm/usr/lib --sysroot=${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm\"",
                    "CPPFLAGS=\"%s\"" % (flags),
                    "CFLAGS=\"%s\"" % (flags),
                    "CXXFLAGS=\"%s\"" % (flags),
                    "PATH=\"$ANDROID_NDK/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/arm-linux-androideabi/bin:$PATH\"",
                    ]
                opt = "--host=x86_64-linux --build=x86_64-pc-linux-gnu --with-jemalloc-prefix --target=arm-linux-androideabi --disable-tls "
            else:
                flags = "-DANDROID \
-isystem ${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm64/usr/include \
-isystem ${ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/include \
-isystem ${ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/libs/arch-arm64/include \
-isystem ${ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/include/backward \
-Wno-psabi --sysroot=${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm64 -funwind-tables -fsigned-char -no-canonical-prefixes -fdata-sections -ffunction-sections -Wa,--noexecstack  -fomit-frame-pointer -fstrict-aliasing -funswitch-loops -finline-limit=300 -O3 -DNDEBUG -fPIC"
            
                exports = [
                    "PLATFORM=android-21" 
                    "CC=\"${ANDROID_NDK}/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin/arm-linux-androideabi-gcc\"",
                    "CXX=\"${ANDROID_NDK}/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin/arm-linux-androideabi-g++\"",
                    "LDFLAGS=\"-fPIC -L${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm64/usr/lib --sysroot=${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm64\"",
                    "CPPFLAGS=\"%s\"" % (flags),
                    "CFLAGS=\"%s\"" % (flags),
                    "CXXFLAGS=\"%s\"" % (flags),
                    "PATH=\"$ANDROID_NDK/toolchains/aarch64-linux-android-4.9/prebuilt/linux-x86_64/aarch64-linux-android/bin:$PATH\"",
                    ]
                opt = "--host=x86_64-linux --build=x86_64-pc-linux-gnu --with-jemalloc-prefix --target=arm-linux-androideabi --disable-tls --disable-syscall "

            flags += " -O3 -g -DNDEBUG " if str(self.info.settings.build_type) == "Release" else "-O0 -g "
            opt += "" if str(self.info.settings.build_type) == "Release" else " --enable-debug "
            
            script = os.path.abspath(os.path.join(self.ZIP_FOLDER_NAME,"build.sh"))
            file = open(script ,"w")
            file.write("#!/bin/bash\n")
            file.write("".join(["export %s\n" %x for x in exports]))
            file.write("echo CC=${ANDROID_NDK}/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin/arm-linux-androideabi-gcc\n")
            file.write("echo $CC\n")
            file.write("cd %s && ./autogen.sh %s" % (os.path.abspath(self.ZIP_FOLDER_NAME), opt))
            file.write("\n")
            file.close()
            self.run("chmod +x %s" % script)

            self.run(os.path.join(self.ZIP_FOLDER_NAME, script))
            self.run("cd %s && make" % (self.ZIP_FOLDER_NAME))
        else:
            compile_flag = "-m32 " if self.settings.arch == "x86" else ""
            compile_flag += " -fPIC "
            compile_flag += " -O3 -g " if str(self.info.settings.build_type) == "Release" else "-O0 -g "
            linker_flag = "-m32 " if self.settings.arch == "x86" else ""
            compile_flag += "-mmacosx-version-min=10.7 " if self.settings.os == "Macos" else ""
            debug_flag = "" if str(self.info.settings.build_type) == "Release" else "--enable-debug "
            self.run("cd %s && CFLAGS='%s' CXXFLAGS='%s' LDFLAGS='%s' ./autogen.sh --with-jemalloc-prefix %s" 
                     % (self.ZIP_FOLDER_NAME, compile_flag, compile_flag, linker_flag, debug_flag))
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
