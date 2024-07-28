from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.files import get

required_conan_version = ">=1.51.1"


class ConfuSociConan(ConanFile):
    name = "lib_name"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    generators = "CMakeDeps", "CMakeToolchain"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        self.options["soci"].with_boost = True
        self.options["soci"].with_sqlite3 = True

    def requirements(self):
        self.requires("boost/1.83.0")

    def source(self):
        get(self, **self.conan_data["sources"][self.version], strip_root=True)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def layout(self):
        cmake_layout(self, src_folder=self.name + "-" + str(self.version))

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = [self.name]
