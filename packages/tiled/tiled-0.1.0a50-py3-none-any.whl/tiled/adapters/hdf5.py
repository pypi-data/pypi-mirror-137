import collections.abc
import warnings

import dask.array
import h5py
import numpy

from ..adapters.utils import IndexersMixin, tree_repr
from ..utils import DictView
from .array import ArrayAdapter


class HDF5DatasetAdapter(ArrayAdapter):
    # TODO Just wrap h5py.Dataset directly, not via dask.array.
    def __init__(self, dataset):
        super().__init__(dask.array.from_array(dataset), metadata=dataset.attrs)


class HDF5Adapter(collections.abc.Mapping, IndexersMixin):
    """
    Read an HDF5 file or a group within one.

    This map the structure of an HDF5 file onto a "Tree" of array structures.

    Examples
    --------

    From the root node of a file given a filepath

    >>> import h5py
    >>> HDF5Adapter.from_file("path/to/file.h5")

    From the root node of a file given an h5py.File object

    >>> import h5py
    >>> file = h5py.File("path/to/file.h5")
    >>> HDF5Adapter.from_file(file)

    From a group within a file

    >>> import h5py
    >>> file = h5py.File("path/to/file.h5")
    >>> HDF5Adapter(file["some_group']["some_sub_group"])

    """

    structure_family = "node"

    def __init__(self, node, access_policy=None, principal=None):
        if (access_policy is not None) and (
            not access_policy.check_compatibility(self)
        ):
            raise ValueError(
                f"Access policy {access_policy} is not compatible with this Tree."
            )
        self._node = node
        self._access_policy = access_policy
        self._principal = principal
        super().__init__()

    @classmethod
    def from_file(cls, file):
        if not isinstance(file, h5py.File):
            file = h5py.File(file, "r")
        return cls(file)

    def __repr__(self):
        return tree_repr(self, list(self))

    @property
    def access_policy(self):
        return self._access_policy

    @property
    def principal(self):
        return self._principal

    def authenticated_as(self, principal):
        if self._principal is not None:
            raise RuntimeError(f"Already authenticated as {self.principal}")
        if self._access_policy is not None:
            raise NotImplementedError
        tree = type(self)(
            self._node,
            access_policy=self._access_policy,
            principal=principal,
        )
        return tree

    @property
    def metadata(self):
        d = dict(self._node.attrs)
        for k, v in list(d.items()):
            # Convert any bytes to str.
            if isinstance(v, bytes):
                d[k] = v.decode()
        return DictView(d)

    def __iter__(self):
        yield from self._node

    def __getitem__(self, key):
        value = self._node[key]
        if isinstance(value, h5py.Group):
            return HDF5Adapter(value)
        else:
            if value.dtype == numpy.dtype("O"):
                warnings.warn(
                    f"The dataset {key} is of object type, using a "
                    "Python-only feature of h5py that is not supported by "
                    "HDF5 in general. Read more about that feature at "
                    "https://docs.h5py.org/en/stable/special.html. "
                    "Consider using a fixed-length field instead. "
                    "Tiled will serve an empty placeholder."
                )
                return HDF5DatasetAdapter(numpy.array([]))
            return HDF5DatasetAdapter(value)

    def __len__(self):
        return len(self._node)

    def search(self, query):
        """
        Return a Tree with a subset of the mapping.
        """
        raise NotImplementedError

    def read(self, fields=None):
        if fields is not None:
            raise NotImplementedError
        return self

    # The following three methods are used by IndexersMixin
    # to define keys_indexer, items_indexer, and values_indexer.

    def _keys_slice(self, start, stop, direction):
        keys = list(self._node)
        if direction < 0:
            keys = reversed(keys)
        return keys[start:stop]

    def _items_slice(self, start, stop, direction):
        items = [(key, self[key]) for key in list(self)]
        if direction < 0:
            items = reversed(items)
        return items[start:stop]

    def _item_by_index(self, index, direction):
        keys = list(self)
        if direction < 0:
            keys = reversed(keys)
        return keys[index]
