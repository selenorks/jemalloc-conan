from conan.packager import ConanMultiPackager

if __name__ == "__main__":
    builder = ConanMultiPackager(username="myuser")
    compiler = {"compiler": "Visual Studio", "compiler.version": "14"}
    builder.add({"arch": "x86", "build_type": "Release", "compiler.runtime": "MDd"}.update(compiler))
    builder.add({"arch": "x86", "build_type": "Debug", "compiler.runtime": "MD"}.update(compiler))
    builder.add({"arch": "x86_64", "build_type": "Release", "compiler.runtime": "MDd"}.update(compiler))
    builder.add({"arch": "x86_64", "build_type": "Debug", "compiler.runtime": "MD"}.update(compiler))
    
    builder.run()