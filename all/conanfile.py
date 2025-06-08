from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout
from conan.tools.files import get
from conan.tools.cmake import CMakeToolchain
required_conan_version = ">=1.51.1"


class MyWebSocket(ConanFile):
    name = "my_web_socket"
    settings = "os", "compiler", "build_type", "arch"
    generators = "CMakeDeps"
    options = {
        "log_co_spawn_print_exception": [True, False],
        "log_write": [True, False],
        "log_read": [True, False],
        "log_boost_asio": [True, False],
    }
    default_options = {
        "log_co_spawn_print_exception": False,
        "log_write": False,
        "log_read": False,
        "log_boost_asio": False
    }

    def generate(self):
        tc = CMakeToolchain(self)
        tc.user_presets_path = False #workaround because this leads to useless options in cmake-tools configure
        unformatted_flags=self.conf.get("tools.build:cxxflags")
        if unformatted_flags:
            flags= " ".join(unformatted_flags)
            self.output.info(f'Using CXXFLAGS: "{flags}"')
            tc.variables["CMAKE_CXX_FLAGS"] = flags
        tc.variables["LOG_CO_SPAWN_PRINT_EXCEPTIONS"] = self.options.log_co_spawn_print_exception
        tc.variables["LOG_WRITE"] = self.options.log_write
        tc.variables["LOG_READ"] = self.options.log_read
        tc.variables["LOG_BOOST_ASIO"] = self.options.log_boost_asio
        tc.generate()

    def requirements(self):
        self.requires("boost/1.86.0")
        self.requires("certify/cci.20201114@modern-durak")
        self.requires("fmt/11.2.0")

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
        self.cpp_info.components[self.name].requires = ["boost::headers","certify::_certify","fmt::fmt"]
        self.cpp_info.components[self.name].libs = [self.name]
