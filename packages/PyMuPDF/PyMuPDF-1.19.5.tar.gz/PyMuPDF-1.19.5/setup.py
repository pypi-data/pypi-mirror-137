import os
import re
import sys
import json

from setuptools import Extension, setup

DEFAULT = [
    "mupdf",
    "mupdf-third",
]

ALPINE = DEFAULT + [
    "jbig2dec",
    "jpeg",
    "openjp2",
    "harfbuzz",
]
ARCH_LINUX = DEFAULT + [
    "jbig2dec",
    "openjp2",
    "jpeg",
    "freetype",
    "gumbo",
]
OPENSUSE = ARCH_LINUX + [
    "harfbuzz",
    "png16",
]
FEDORA = ARCH_LINUX + [
    "harfbuzz",
]
NIX = ARCH_LINUX + ["harfbuzz"]
LIBRARIES = {
    "default": DEFAULT,
    "ubuntu": DEFAULT,
    "arch": ARCH_LINUX,
    "manjaro": ARCH_LINUX,
    "artix": ARCH_LINUX,
    "opensuse": OPENSUSE,
    "fedora": FEDORA,
    "alpine": ALPINE,
    "nix": NIX,
}


def load_libraries():
    if os.getenv("NIX_STORE"):
        return LIBRARIES["nix"]

    try:
        import distro

        os_id = distro.id()
    except:
        os_id = ""
    if os_id in list(LIBRARIES.keys()) + ["manjaro", "artix"]:
        return LIBRARIES[os_id]

    filepath = "/etc/os-release"
    if not os.path.exists(filepath):
        return LIBRARIES["default"]
    regex = re.compile("^([\\w]+)=(?:'|\")?(.*?)(?:'|\")?$")
    with open(filepath) as os_release:
        info = {
            regex.match(line.strip()).group(1): re.sub(
                r'\\([$"\'\\`])', r"\1", regex.match(line.strip()).group(2)
            )
            for line in os_release
            if regex.match(line.strip())
        }

    os_id = info["ID"]
    if os_id.startswith("opensuse"):
        os_id = "opensuse"
    if os_id not in LIBRARIES.keys():
        return LIBRARIES["default"]
    return LIBRARIES[os_id]


# check the platform
if sys.platform.startswith("linux") or "gnu" in sys.platform:
    include_dirs = [
        "/usr/include/mupdf",
        "/usr/local/include/mupdf",
        "mupdf/thirdparty/freetype/include",
        "/usr/include/freetype2",
    ]
    libraries = load_libraries()
    library_dirs = []
    extra_link_args = []

elif sys.platform.startswith(("darwin", "freebsd", "openbsd")):
    include_dirs = [
        "/usr/local/include/mupdf",
        "/usr/local/include",
        "mupdf/thirdparty/freetype/include",
        "/usr/local/include/freetype2",
        "/usr/X11R6/include/freetype2",
        "/opt/homebrew/include",
        "/opt/homebrew/include/mupdf",
        "/opt/homebrew/include/freetype2",
    ]
    libraries = ["mupdf", "mupdf-third"]
    library_dirs = ["/usr/local/lib", "/opt/homebrew/lib"]
    extra_link_args = []


else:
    include_dirs = [
        "./mupdf/include",
        "./mupdf/include/mupdf",
        "./mupdf/thirdparty/freetype/include",
    ]
    libraries = ["libmupdf", "libresources", "libthirdparty"]
    library_dirs = ["./mupdf/platform/win32/x64/Release"]
    extra_link_args = ["/NODEFAULTLIB:MSVCRT"]

# add any local include and library folders
pymupdf_dirs = os.environ.get("PYMUPDF_DIRS", None)
if pymupdf_dirs:
    with open(pymupdf_dirs) as dirfile:
        local_dirs = json.load(dirfile)
        include_dirs += local_dirs.get("include_dirs", [])
        library_dirs += local_dirs.get("library_dirs", [])


module = Extension(
    "fitz._fitz",
    ["fitz/fitz_wrap.c"],
    language="c++",
    include_dirs=include_dirs,
    library_dirs=library_dirs,
    libraries=libraries,
    extra_link_args=extra_link_args,
)

setup_py_cwd = os.path.dirname(__file__)
classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "Intended Audience :: Information Technology",
    "Operating System :: MacOS",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: C",
    "Programming Language :: Python :: 3 :: Only",
    "Programming Language :: Python :: Implementation :: CPython",
    "Topic :: Utilities",
    "Topic :: Multimedia :: Graphics",
    "Topic :: Software Development :: Libraries",
]
with open(os.path.join(setup_py_cwd, "README.md"), encoding="utf-8") as f:
    readme = f.read()

setup(
    name="PyMuPDF",
    version="1.19.5",
    description="Python bindings for the PDF toolkit and renderer MuPDF",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=classifiers,
    url="https://github.com/pymupdf/PyMuPDF",
    author="Jorj McKie",
    author_email="jorj.x.mckie@outlook.de",
    ext_modules=[module],
    python_requires=">=3.6",
    py_modules=["fitz.fitz", "fitz.utils", "fitz.__main__"],
    license="GNU AFFERO GPL 3.0",
    project_urls={
        "Documentation": "https://pymupdf.readthedocs.io/",
        "Source": "https://github.com/pymupdf/pymupdf",
        "Tracker": "https://github.com/pymupdf/PyMuPDF/issues",
        "Changelog": "https://pymupdf.readthedocs.io/en/latest/changes.html",
        "Discussions": "https://github.com/pymupdf/PyMuPDF/discussions",
    },
)
