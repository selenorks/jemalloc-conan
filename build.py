from conan.packager import ConanMultiPackager
import platform
import os

if __name__ == "__main__":
    builder = ConanMultiPackager()
    if platform.system() == "Windows":
        builder.add_common_builds()
        filtered_builds = []
        for settings, options in builder.builds:
            if settings["compiler"] == "Visual Studio" and settings["compiler.version"] == "14" and settings["compiler.runtime"].startswith("MD"):
                 filtered_builds.append([settings, options])
        builder.builds = filtered_builds

    if platform.system() == "Linux":
        channel = os.getenv("CONAN_ARCHS", "x86,x86_64,armv7,armv8").split(",")

        #builder.add({"arch": "x86", "build_type": "Release", "compiler": "gcc"})
        #builder.add({"arch": "x86_64", "build_type": "Release", "compiler": "gcc"})
        #builder.add({"arch": "x86", "build_type": "Debug", "compiler": "gcc"})
        #builder.add({"arch": "x86_64", "build_type": "Debug", "compiler": "gcc"})
        #Adnroid
        #builder.add({"arch": "armv7", "os": "Android", "build_type": "Release", "compiler": "gcc"})
        #builder.add({"arch": "armv8", "os": "Android", "build_type": "Release", "compiler": "gcc"})
        #builder.add({"arch": "armv7", "os": "Android", "build_type": "Debug", "compiler": "gcc"})
        builder.add({"arch": "armv8", "os": "Android", "build_type": "Debug", "compiler": "gcc"})

        filtered_builds = []
        for settings, options in builder.builds:
            if settings["arch"] in channel:
                 filtered_builds.append([settings, options])
        builder.builds = filtered_builds

    if platform.system() == "Darwin":
        builder.add({"arch": "x86", "build_type": "Release"})
        builder.add({"arch": "x86_64", "build_type": "Release"})
        builder.add({"arch": "x86", "build_type": "Debug"})
        builder.add({"arch": "x86_64", "build_type": "Debug"})
        #iOS
        builder.add({"arch": "armv7", "os": "iOS", "build_type": "Release"})
        builder.add({"arch": "armv8", "os": "iOS", "build_type": "Release"})
        builder.add({"arch": "armv7", "os": "iOS", "build_type": "Debug"})
        builder.add({"arch": "armv8", "os": "iOS", "build_type": "Debug"})

    builder.run()
