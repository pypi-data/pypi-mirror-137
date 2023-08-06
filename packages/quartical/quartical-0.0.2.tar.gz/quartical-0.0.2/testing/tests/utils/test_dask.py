import pickle

import pytest
from quartical.utils.dask import Blocker, blockwise_unique, as_dict
import dask.array as da
import numpy as np
from numpy.testing import assert_array_equal


@pytest.fixture(scope="module")
def test_data():

    da.random.seed(0)

    return da.random.randint(0, 10, size=(100), chunks=10)


# ----------------------------------as_dict------------------------------------

@pytest.mark.parametrize("outputs", [["a"], ["a", "b"], ["a", "b", "c"]])
def test_as_dict(outputs):
    """Check that as_dict correctly wraps a number of outputs."""

    def f():
        return (1,)*len(outputs) if len(outputs) > 1 else 1

    output_dict = as_dict(f, *outputs)()

    assert all([output in output_dict for output in outputs])


def test_insufficient_names():
    """Check that we raise an error if we have insufficient names."""

    def f(a, b, c):
        return a, b, c

    with pytest.raises(ValueError):
        as_dict(f, "a", "b")(0, 0, 0)

# -----------------------------blockwise_unique--------------------------------


def test_values(test_data):

    da_unique = blockwise_unique(test_data)

    np_unique = np.concatenate(
        [np.unique(b.compute()) for b in test_data.blocks])

    assert_array_equal(np_unique, da_unique.compute())


def test_blockwise_unique_pickling(test_data):
    da_unique = blockwise_unique(test_data)
    assert_array_equal(pickle.loads(pickle.dumps(da_unique)), da_unique)


def test_indices(test_data):

    _, da_indices = blockwise_unique(test_data, return_index=True)

    np_indices = np.concatenate(
        [np.unique(b.compute(), return_index=True)[1]
         for b in test_data.blocks])

    assert_array_equal(np_indices, da_indices.compute())


def test_counts(test_data):

    _, da_counts = blockwise_unique(test_data, return_counts=True)

    np_counts = np.concatenate(
        [np.unique(b.compute(), return_counts=True)[1]
         for b in test_data.blocks])

    assert_array_equal(np_counts, da_counts.compute())


def test_inverse(test_data):

    _, da_inverse = blockwise_unique(test_data, return_inverse=True)

    np_inverse = np.concatenate(
        [np.unique(b.compute(), return_inverse=True)[1]
         for b in test_data.blocks])

    assert_array_equal(np_inverse, da_inverse.compute())


def test_ndarr():
    """Check for exception when dealing with multidimensional arrays."""

    arr = da.zeros([10, 10], chunks=(5, 5))

    with pytest.raises(ValueError):
        assert blockwise_unique(arr)


def test_axis():
    """Check for exception when using unsupported axis argument."""

    arr = da.zeros(10, chunks=(5,))

    with pytest.raises(ValueError):
        assert blockwise_unique(arr, axis=1)


# -----------------------------------Blocker-----------------------------------

def test_1dsum(test_data):
    """Test that the blocker works for a simple 1D blockwise sum."""

    B = Blocker(as_dict(np.sum, "sum"), "i")

    B.add_input("a", test_data, "i")
    B.add_input("keepdims", True)

    B.add_output("sum", "i", ((1,)*test_data.npartitions,), np.float64)

    da_blocksum = B.get_dask_outputs()["sum"]

    np_blocksum = np.concatenate(
        [np.sum(b.compute(), keepdims=True) for b in test_data.blocks])

    assert_array_equal(np_blocksum, da_blocksum.compute())


@pytest.mark.filterwarnings("ignore: Increasing")
def test_ndsum(test_data):
    """Test that the blocker works for an ND blockwise sum."""

    B = Blocker(as_dict(lambda a: (np.atleast_2d(np.sum(a))), "sum"), "ij")

    local_test_data = da.outer(test_data, test_data.T)

    B.add_input("a", local_test_data, "ij")

    i_blocks, j_blocks = local_test_data.numblocks

    B.add_output("sum", "ij", ((1,)*i_blocks, (1,)*j_blocks), np.float64)

    da_blocksum = B.get_dask_outputs()["sum"]

    np_blocksum = np.concatenate(
        [np.sum(local_test_data.blocks[i].compute(), keepdims=True)
         for i in np.ndindex(local_test_data.numblocks)]).reshape((10, 10))

    assert_array_equal(np_blocksum, da_blocksum.compute())


def test_mixed_axes(test_data):
    """Test that the blocker works for a simple 1D blockwise sum."""

    B = Blocker(as_dict(lambda a, b: a[:, None] + b[None, :], "add"), "ij")

    B.add_input("a", test_data, "i")
    B.add_input("b", test_data, "j")

    chunks = (test_data.chunks[0], test_data.chunks[0])

    B.add_output("add", "ij", chunks, np.float64)

    da_blockadd = B.get_dask_outputs()["add"]

    np_test_data = test_data.compute()

    np_blockadd = np_test_data[:, None] + np_test_data[None, :]

    assert_array_equal(np_blockadd, da_blockadd.compute())


def test_missing_axis(test_data):
    """Test that having an output index not present on the input fails."""

    B = Blocker(as_dict(np.square, "square"), "j")

    # This is necessary to bypass an error which may be raised earlier.
    local_test_data = test_data.rechunk(test_data.shape)

    B.add_input("x", local_test_data, "i")

    B.add_output("square", "j", ((1,),), np.float64)

    with pytest.raises(KeyError):
        assert B.get_dask_outputs()


def test_mismatched_axis(test_data):
    """Test that having unequal chunks along an axis fails."""

    B = Blocker(as_dict(lambda a, b: a + b, "add"), "i")

    B.add_input("a", test_data, "i")

    with pytest.raises(ValueError):
        assert B.add_input("b", test_data.rechunk(9), "i")


def test_inconsistent_input(test_data):
    """Test that having indices on a scalar fails."""

    B = Blocker(as_dict(lambda a: a, "add"), "i")

    B.add_input("a", test_data, "i")
    B.add_input("b", True, "i")

    B.add_output("add", "i", ((1,)*test_data.npartitions,), np.float64)

    with pytest.raises(ValueError):
        assert B.get_dask_outputs()


def test_per_chunk_list_input(test_data):
    """Test list with an entry per chunk."""

    B = Blocker(as_dict(lambda a, b: a + b, "add"), "i")

    B.add_input("a", test_data, "i")
    B.add_input("b", list(range(10)), "i")

    chunks = (test_data.chunks[0],)

    B.add_output("add", "i", chunks, np.float64)

    da_listadd = B.get_dask_outputs()["add"]

    np_listadd = test_data.compute() + np.repeat(list(range(10)), 10)

    assert_array_equal(np_listadd, da_listadd.compute())


def test_along_axis_list_input(test_data):
    """Test list with an entry per chunk along an axis."""

    B = Blocker(as_dict(lambda a, b: a[:, None] + b, "add"), "ij")

    test_list = list(range(6))

    B.add_input("a", test_data, "i")
    B.add_input("b", test_list, "j")

    chunks = (test_data.chunks[0], (1,)*len(test_list))

    B.add_output("add", "ij", chunks, np.float64)

    da_listadd = B.get_dask_outputs()["add"]

    np_listadd = test_data.compute()[:, None] + np.array(test_list)[None, :]

    assert_array_equal(np_listadd, da_listadd.compute())


def test_multi_axis_list_input(test_data):
    """Test list with an entry per chunk along multiple axes."""

    B = Blocker(as_dict(lambda a, b: a[:, None] + b, "add"), "ij")

    inner_list_len = 6

    test_list = [[j]*inner_list_len for j in range(test_data.npartitions)]

    B.add_input("a", test_data, "i")
    B.add_input("b", test_list, "ij")

    chunks = (test_data.chunks[0], (1,)*inner_list_len)

    B.add_output("add", "ij", chunks, np.float64)

    da_listadd = B.get_dask_outputs()["add"]

    np_listadd = \
        test_data.compute()[:, None] + np.array(test_list).repeat(10, axis=0)

    assert_array_equal(np_listadd, da_listadd.compute())


@pytest.mark.filterwarnings("ignore: Increasing")
def test_contraction(test_data):
    """Check that we raise an error when a contraction would be required."""

    B = Blocker(as_dict(lambda a: (np.atleast_1d(np.sum(a))), "sum"), "i")

    local_test_data = da.outer(test_data, test_data.T)

    with pytest.raises(ValueError):
        B.add_input("a", local_test_data, "ij")

# -----------------------------------------------------------------------------
