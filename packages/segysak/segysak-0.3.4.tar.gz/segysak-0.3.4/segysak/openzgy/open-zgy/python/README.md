# OpenZGY implemented in pure Python

This library deals with the ZGY file format developed by Schlumberger for storing 3d data for seismic interpretation.

This folder contais the pure Python version.

doc/ contains the documentation of the ZGY file format.

openzgy/ contains a reference implementation of a library to read this format.

The focus of the reference implementation is to demonstrate how the format works. The code is written in pure Python. Performance is comparable to the native C++ implementation, so the library might also be used directly in production code.

The code is designed to not have too many levels of abstraction that will hide the finer details of the format. Because the whole point is to let people understand those details.

Schlumber might at some point choose to publish this project as open source. A decision on this has not been made yet.

The pure Python implementation supports read and write of uncompressed local files. See openzgy/api.py for the public interface, or in a Python shell type

    import openzgy.api
    help(openzgy.api)

As is standard in Python, you can also get help on individual classes and individual methods. E.g.

    help(openzgy.api.ZgyReader.read)

If you install the binary "SdGlue" Python module you will also be able to read and write sd:// uris using seismic store.

    pip3 install SdGlue-*.whl

Unlike the core OpenZGY, this library will need to match your OS and Pyhon version. The build server supports 10 or so combinations of Linux and Python. No windows support yet.

If you install ZFP version 0.5.5 you will be able to read and write compressed files. You may need to build that library from source. ZFP is open source, but I haven't found any repo that has pre-built Python packages for it.
