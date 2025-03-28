from pathlib import Path, PureWindowsPath
from urllib.parse import urlparse

from asdf.extension import Converter


class FileManagerConverter(Converter):
    tags = [
        "tag:dkist.nso.edu:dkist/array_container-0.2.0",
        "asdf://dkist.nso.edu/tags/file_manager-1.0.0",
    ]
    types = ["dkist.io.file_manager.FileManager"]

    def from_yaml_tree(self, node, tag, ctx):
        from dkist.io.file_manager import FileManager
        from dkist.io.loaders import AstropyFITSLoader

        url = urlparse(ctx.url or ".")
        if url.scheme not in ("file", ""):
            raise ValueError("Currently only loading local asdf files is supported.")
        filepath = Path(url.path)
        if isinstance(filepath, PureWindowsPath):
            # If we are on windows we need to strip the leading /
            filepath = Path(url.path.strip("/"))
        base_path = filepath.parent

        file_manager = FileManager.from_parts(node["fileuris"],
                                              node["target"],
                                              node["datatype"],
                                              node["shape"],
                                              loader=AstropyFITSLoader,
                                              basepath=base_path)
        return file_manager

    def to_yaml_tree(self, obj, tag, ctx):
        node = {}
        node["fileuris"] = obj._striped_external_array._fileuris.tolist()
        node["target"] = obj._striped_external_array.target
        node["datatype"] = obj._striped_external_array.dtype
        node["shape"] = obj._striped_external_array.shape
        return node
