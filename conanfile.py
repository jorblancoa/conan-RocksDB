from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

# https://github.com/giorgioazzinnaro/rocksdb/blob/master/INSTALL.md

class RocksdbConan(ConanFile):
    name = "RocksDB"
    version = "5.8"
    license = "https://github.com/facebook/rocksdb/blob/master/COPYING"
    url = "https://github.com/giorgioazzinnaro/conan-RocksDB"
    description = "A library that provides an embeddable, persistent key-value store for fast storage."
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    source_tgz = "https://github.com/facebook/rocksdb/archive/v%s.tar.gz" % version

    requires = (
        "zlib/1.2.11@conan/stable",
        "bzip2/1.0.6@conan/stable",
        "LZ4/1.8.0@bincrafters/stable"
        # TODO snappy, zstandard
    )

    def source(self):
        self.output.info("Downloading %s" %self.source_tgz)
        tools.download(self.source_tgz, "rocksdb.tar.gz")

        tools.unzip("rocksdb.tar.gz")
        os.remove("rocksdb.tar.gz")

    @property
    def subfolder(self):
        return "rocksdb-%s" % self.version

    def build(self):
        if tools.os_info.is_windows:
            self.windows_build()
        else:
            self.unix_build()

    def windows_build(self):
        # TODO
        True

    def unix_build(self):
        with tools.chdir(self.subfolder):
            env_build = AutoToolsBuildEnvironment(self)
            env_build.fpic = True
            env_build.libs.append("pthread")

            if self.settings.build_type == "Debug":
                env_build.make()  # $ make
            else:
                if self.options.shared:
                    env_build.make(["shared_lib"])  # $ make shared_lib
                else:
                    env_build.make(["static_lib"])  # $ make static_lib

    def package(self):
        self.copy("LICENSE.Apache", src=self.subfolder, keep_path=False)
        self.copy("LICENSE.leveldb", src=self.subfolder, keep_path=False)

        self.copy("*.h", dst="include", src=("%s/include" % self.subfolder))

        if self.options.shared:
            self.copy("librocksdb.so", dst="lib", src=self.subfolder, keep_path=False)
        else:
            self.copy("librocksdb.a", dst="lib", src=self.subfolder, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["rocksdb"]
