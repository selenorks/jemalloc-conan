echo ANDROID_NDK=$ANDROID_NDK
if ["${ARCH}" != "armv7"]; then
#armv8
    export PLATFORM=android-21
    export PATH=$ANDROID_NDK/toolchains/aarch64-linux-android-4.9/prebuilt/linux-x86_64/aarch64-linux-android/bin:$PATH
    export CFLAGS="-DANDROID \
    -isystem ${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm64/usr/include \
    -isystem ${ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/include \
    -isystem ${ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/libs/arch-arm64/include \
    -isystem ${ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/include/backward \
    -Wno-psabi --sysroot=${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm64 -funwind-tables -fsigned-char -no-canonical-prefixes -fdata-sections -ffunction-sections -Wa,--noexecstack  -fomit-frame-pointer -fstrict-aliasing -funswitch-loops -finline-limit=300 -O3 -DNDEBUG -fPIC"
    export CXXFLAGS="$CFLAGS"
    export CPPFLAGS="$CFLAGS"
    export LDFLAGS="-fPIC -L${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm64/usr/lib --sysroot=${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm64"
    export CC="$ANDROID_NDK/toolchains/aarch64-linux-android-4.9/prebuilt/linux-x86_64/bin/aarch64-linux-android-gcc"
    export CXX="$ANDROID_NDK/toolchains/aarch64-linux-android-4.9/prebuilt/linux-x86_64/bin/aarch64-linux-android-g++"

    ./autogen.sh --host=x86_64-linux --build=x86_64-pc-linux-gnu --with-jemalloc-prefix --target=arm-linux-androideabi --disable-tls --disable-syscall  $OPTS
else
#armv7
    export PLATFORM=android-16
    export PATH=$ANDROID_NDK/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/arm-linux-androideabi/bin:$PATH
    export CFLAGS="-DANDROID \
-isystem ${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm/usr/include \
-isystem ${ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/include \
-isystem ${ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/libs/armeabi-v7a/include \
-isystem ${ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/include/backward \
-fexceptions -Wno-psabi --sysroot=${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm -funwind-tables -finline-limit=64 -fsigned-char -no-canonical-prefixes -march=armv7-a -mfloat-abi=softfp -mfpu=neon -fdata-sections -ffunction-sections -Wa,--noexecstack  -Wl,--fix-cortex-a8 -Wl,--no-undefined -Wl,--gc-sections -Wl,-z,noexecstack -Wl,-z,relro -Wl,-z,now -Wl,-z,nocopyreloc -fdiagnostics-color=always -mthumb -fomit-frame-pointer -fno-strict-aliasing -fPIC $OPT_FLAGS"
    export CXXFLAGS="${CFLAGS}"
    export LDFLAGS="-fPIC -L${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm/usr/lib --sysroot=${ANDROID_NDK}/platforms/${PLATFORM}/arch-arm"
    export LIBS="${ANDROID_NDK}/sources/cxx-stl/gnu-libstdc++/4.9/libs/armeabi-v7a/libgnustl_shared.so"
    export CC="${ANDROID_NDK}/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin/arm-linux-androideabi-gcc"
    export CXX="${ANDROID_NDK}/toolchains/arm-linux-androideabi-4.9/prebuilt/linux-x86_64/bin/arm-linux-androideabi-g++"

    ./autogen.sh --host=x86_64-linux --build=x86_64-pc-linux-gnu --with-jemalloc-prefix --target=arm-linux-androideabi --disable-tls  $OPTS
fi
make
