export PLATFORM=android-16
export PATH=$ANDROID_NDK/build/tools/~/android-ndk-armv7/arm-linux-androideabi/bin:$PATH

export CFLAGS="-DANDROID \
-isystem ${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm/usr/include \
-isystem ${ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/include \
-isystem ${ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/libs/armeabi-v7a/include \
-isystem ${ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/include/backward \
-fexceptions -Wno-psabi --sysroot=${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm -funwind-tables -finline-limit=64 -fsigned-char -no-canonical-prefixes -march=armv7-a -mfloat-abi=softfp -mfpu=neon -fdata-sections -ffunction-sections -Wa,--noexecstack  -Wl,--fix-cortex-a8 -Wl,--no-undefined -Wl,--gc-sections -Wl,-z,noexecstack -Wl,-z,relro -Wl,-z,now -Wl,-z,nocopyreloc -fdiagnostics-color=always -mthumb -fomit-frame-pointer -fno-strict-aliasing -O3 -DNDEBUG -fPIC"

export CXXFLAGS="$CFLAGS"
export CPPFLAGS="$CFLAGS"
export LDFLAGS="-fPIC -L${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm/usr/lib --sysroot=${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm"

export CC="${ANDROID_NDK}/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin/arm-linux-androideabi-gcc"
export CXX="${ANDROID_NDK}/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin/arm-linux-androideabi-g++"

./autogen.sh --host=x86_64-linux --build=x86_64-pc-linux-gnu --prefix=${PREFIX}  --with-jemalloc-prefix --target=arm-linux-androideabi --disable-tls