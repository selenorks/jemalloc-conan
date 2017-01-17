from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="selenorks")
    compiler = {"compiler": "Visual Studio", "compiler.version": "14"}
    builder.add(dict({"arch": "x86", "build_type": "Release", "compiler.runtime": "MDd"}.items() + compiler.items()))
    builder.add(dict({"arch": "x86", "build_type": "Debug", "compiler.runtime": "MD"}.items() + compiler.items()))
    builder.add(dict({"arch": "x86_64", "build_type": "Release", "compiler.runtime": "MDd"}.items() + compiler.items()))
    builder.add(dict({"arch": "x86_64", "build_type": "Debug", "compiler.runtime": "MD"}.items() + compiler.items()))
    
    builder.run()