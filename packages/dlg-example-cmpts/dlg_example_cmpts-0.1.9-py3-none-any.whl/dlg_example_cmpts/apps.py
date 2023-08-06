"""
dlg_example_cmpts appComponent module.

This is the module of dlg_example_cmpts containing DALiuGE
application components.
Here you put your main application classes and objects.

Typically a component project will contain multiple components and will
then result in a single EAGLE palette.

Be creative! do whatever you need to do!
"""

__version__ = "0.1.0"
import json
import logging
import pickle
import urllib
from glob import glob

import numpy as np
from dlg import droputils
from dlg.drop import BarrierAppDROP, BranchAppDrop

logger = logging.getLogger(__name__)

##
# @brief MyBranch
# @details Simple app to demonstrate how to write a branch actually making a
# decision and passing data on.
# Most of the code is boilerplate and can be copied verbatim. Note that a
# branch app is allowed
# to have multiple inputs, but just exactly two outputs. This example is using
# just a single input. There is an associated logical graph available on
# github:
#
#    https://github.com//EAGLE-graph-repo/examples/branchDemo.graph
#
# The application assumes to receive a random floating point array with values
# in the range [0,1] on input. It will calculate the mean of that array and
# then branch depending on whether the mean is smaller or larger than 0.5.
#
# @par EAGLE_START
# @param category PythonApp
# @param[in] param/appclass Application Class/dlg_example_cmpts.apps.MyBranch/String/readonly/ # noqa: E501
#     \~English Import direction for application class
# @param[in] port/array Array/float/
#     \~English Port receiving the input array
# @param[out] port/Y Y/float/
#     \~English Port carrying the mean value of the array if mean < 0.5
# @param[out] port/N N/float/
#     \~English Port carrying the mean value of the array if mean >= 0.5
# @par EAGLE_END


class MyBranch(BranchAppDrop):
    def initialize(self, **kwargs):
        BranchAppDrop.initialize(self, **kwargs)

    def run(self):
        """
        Just reading the input array and calculating the mean.
        """
        input = self.inputs[0]
        data = pickle.loads(droputils.allDropContents(input))
        self.value = data.mean()

    def writeData(self):
        """
        Prepare the data and write to port (self.ind) identified by condition.
        """
        output = self.outputs[self.ind]
        d = pickle.dumps(self.value)
        output.len = len(d)
        logger.info(f">>>>>>> Writing value {self.value} to output {self.ind}")
        output.write(d)

    def condition(self):
        """
        Check value, call write method and return boolean.
        """
        if self.value < 0.5:
            self.ind = 0
            result = True
        else:
            self.ind = 1
            result = False
        self.writeData()
        return result


##
# @brief LengthCheck
#
# This branch returns true if the length of the input array is > 0. It also
# passes the array on to the output ports (will be an empty array in the case
# of N==0).
#
# @par EAGLE_START
# @param category PythonApp
# @param[in] param/appclass Application Class/dlg_example_cmpts.apps.LengthCheck/String/readonly/ # noqa: E501
#     \~English Import direction for application class
# @param[in] port/array Array/float/
#     \~English Port receiving the input array
# @param[out] port/Y Y/float/
#     \~English Port carrying the array if Y.
# @param[out] port/N N/float/
#     \~English Port carrying an empty array (N)
# @par EAGLE_END


class LengthCheck(BranchAppDrop):
    def initialize(self, **kwargs):
        BranchAppDrop.initialize(self, **kwargs)

    def readData(self):
        """
        Just reading the inoput array and determining the size
        """
        input = self.inputs[0]
        self.raw = droputils.allDropContents(input)
        data = pickle.loads(self.raw)
        # make sure we always have a ndarray with at least 1dim.
        if isinstance(data, np.ndarray):
            # that's what we want..
            if data.size == 0:
                # fix this strange case
                data = np.array([data])
                self.raw = pickle.dumps(data)
        elif not isinstance(data, np.ndarray) and type(data) not in (
            list,
            tuple,
        ):
            raise TypeError
        else:
            # can only be list or tuple. convert those.
            data = np.array(data)
            self.raw = pickle.dumps(data)

        self.value = data.size

    def writeData(self):
        """
        Write unmodified data to port (self.ind) identified by condition.
        """
        output = self.outputs[self.ind]
        output.len = self.value
        output.write(self.raw)

    def condition(self):
        """
        Check value, call write method and return boolean.
        """
        self.readData()
        if self.value > 0:
            self.ind = 0
            result = True
        else:
            self.ind = 1
            result = False
        self.writeData()
        return result

    def run(self):
        self.readData()


##
# @brief FileGlob
# @details An App that uses glob to find all files matching a
# template given by a filepath and a wildcard string
#
# @par EAGLE_START
# @param category PythonApp
# @param[in] param/wildcard wildcard/"*"/String/readwrite/
#     \~English Wildcard used to search for files
# @param[in] param/filepath filepath/"."/String/readwrite/
#     \~English Path to search for files
# param/appclass Application Class/dlg_example_cmpts.apps.FileGlob/String/readonly/ # noqa: E501
#     \~English Import path for application class
# @param[out] port/file_list file_list/array/
#     \~English Port carrying the list of files
# @par EAGLE_END


class FileGlob(BarrierAppDROP):
    """
    Simple app collecting file names in a directory
    based on a wild-card pattern
    """

    def initialize(self, **kwargs):
        self.wildcard = self._getArg(kwargs, "wildcard", "*")
        self.filepath = self._getArg(kwargs, "filepath", ".")
        BarrierAppDROP.initialize(self, **kwargs)

    def writeData(self):
        """
        Prepare the data and write to all outputs
        """
        for output in self.outputs:
            d = pickle.dumps(self.value)
            output.len = len(d)
            output.write(d)

    def run(self):
        filetmpl = f"{self.filepath}/{self.wildcard}"
        self.value = glob(filetmpl)
        self.writeData()


##
# @brief PickOne
# @details App that picks the first element of an input list, passes that
# to all outputs, except the first one. The first output is used to pass
# the remaining array on. This app is useful for a loop.
#
# @par EAGLE_START
# @param category PythonApp
# @param/appclass Application Class/dlg_example_cmpts.apps.PickOne/String/readonly/ # noqa: E501
#     \~English Import path for application class
# @param[in] port/rest_array rest_array//array/readwrite/
#     \~English List of elements
# @param[out] port/element element/complex/
#     \~English Port carrying the first element of input array
#               the type is dependent on the list element type.
# @par EAGLE_END
class PickOne(BarrierAppDROP):
    """
    Simple app picking one element at a time. Good for Loops.
    """

    def initialize(self, **kwargs):
        BarrierAppDROP.initialize(self, **kwargs)

    def readData(self):
        input = self.inputs[0]
        data = pickle.loads(droputils.allDropContents(input))

        # make sure we always have a ndarray with at least 1dim.
        if type(data) not in (list, tuple) and not isinstance(
            data, (np.ndarray)
        ):
            raise TypeError
        if isinstance(data, np.ndarray) and data.ndim == 0:
            data = np.array([data])
        else:
            data = np.array(data)
        self.value = data[0] if len(data) else None
        self.rest = data[1:] if len(data) > 1 else np.array([])

    def writeData(self):
        """
        Prepare the data and write to all outputs
        """
        # write rest to array output
        # and value to every other output
        for output in self.outputs:
            if output.name == "rest_array":
                d = pickle.dumps(self.rest)
                output.len = len(d)
            else:
                d = pickle.dumps(self.value)
                output.len = len(d)
            output.write(d)

    def run(self):
        self.readData()
        self.writeData()


##
# @brief ExtractColumn
# @details App that extracts one column of an table-like ndarray. The array is
# assumed to be row major, i.e. the second index refers to columns.
# The column is # selected by index counting from 0. If the array is 1-D the
# result is a 1 element array. The component is passing whatever type is in
# the selected column.
#
# @par EAGLE_START
# @param category PythonApp
# @param/appclass Application Class/dlg_example_cmpts.apps.ExtractColumn/String/readonly/ # noqa: E501
#     \~English Import path for application class
# @param[in] param/index index/0/Integer/readwrite/
#     \~English 0-base index of column to extract
# @param[in] port/table_array table_array//array/readwrite/
#     \~English List of elements
# @param[out] port/column column/1Darray/
#     \~English Port carrying the first element of input array
#               the type is dependent on the list element type.
# @par EAGLE_END
class ExtractColumn(BarrierAppDROP):
    """
    Simple app extracting a column from a 2D ndarray.
    """

    def initialize(self, **kwargs):
        self.index = self._getArg(kwargs, "index", 0)
        BarrierAppDROP.initialize(self, **kwargs)

    def readData(self):
        input = self.inputs[0]
        table_array = pickle.loads(droputils.allDropContents(input))

        # make sure we always have a ndarray with 2dim.
        if not isinstance(table_array, (np.ndarray)) or table_array.ndim != 2:
            raise TypeError
        self.column = table_array[:, self.index]

    def writeData(self):
        """
        Prepare the data and write to all outputs
        """
        # write rest to array output
        # and value to every other output
        for output in self.outputs:
            if output.name == "column":
                d = pickle.dumps(self.column)
                output.len = len(d)
            output.write(d)

    def run(self):
        self.readData()
        self.writeData()


##
# @brief AdvUrlRetrieve
# @details An APP that retrieves the content of a URL and writes
# it to all outputs. The URL can be specified either completely or
# partially through the inputs. In that case the urlTempl parameter can
# use placeholders to construct the final URL.
# @par EAGLE_START
# @param category PythonApp
# @param[in] param/urlTempl URL Template/"https://eagle.icrar.org"/String/readwrite/ # noqa: E501
#     \~English The URL to retrieve
# @param[in] param/appclass Application Class/dlg_example_cmpts.apps.AdvUrlRetrieve/String/readonly/ # noqa: E501
#     \~English Application class
# @param[in] port/urlPart URL Part/String/
#     \~English The port carrying the content read from the URL.
# @param[out] port/content Content/String/
#     \~English The port carrying the content read from the URL.
# @par EAGLE_END
class AdvUrlRetrieve(BarrierAppDROP):
    """
    An App that retrieves the content of a URL and allows to construct the URL
    through input placeholders.

    Keywords:
    URL:   string, URL to retrieve.
    """

    def initialize(self, **kwargs):
        self.urlTempl = self._getArg(kwargs, "urlTempl", "")
        BarrierAppDROP.initialize(self, **kwargs)

    def constructUrl(self):
        url = self.urlTempl
        # this will ignore inputs not referenced in template
        for x, v in enumerate(self.urlParts):
            pathRef = "%%i%d" % (x,)
            if pathRef in url:
                url = url.replace(pathRef, v)
        logger.info(f"Constructed URL: {url}")
        return url

    def readData(self):
        # for this app we are expecting URL fractions on the inputs
        urlParts = []
        for input in self.inputs:
            part = pickle.loads(droputils.allDropContents(input))
            # make sure the placeholders are strings
            logger.info(f"URL part: {part}")
            if not isinstance(part, str):
                raise TypeError
            urlParts.append(part)
        self.urlParts = urlParts
        self.url = self.constructUrl()
        try:
            u = urllib.request.urlopen(self.url)
        except Exception as e:
            raise e
        # finally read the content of the URL
        self.content = u.read()

    def writeData(self):
        """
        Prepare the data and write to all outputs
        """
        outs = self.outputs
        written = False
        if len(outs) < 1:
            raise Exception("At least one output required for %r" % self)
        for output in outs:
            if output.name.lower() == "content":
                # we are not pickling here, but just pass on the data.
                output.len = len(self.content)
                output.write(self.content)
                written = True
            else:
                logger.warning(f"Output with name {output.name} ignored!")

        if not written:
            raise TypeError(
                "No matching output drop found." + "Nothing written"
            )

    def run(self):
        self.readData()
        self.writeData()


##
# @brief String2JSON
# @details App that reads a string from a single input and tries
# to convert that to JSON
# @par EAGLE_START
# @param category PythonApp
# @param/appclass Application Class/dlg_example_cmpts.apps.String2JSON/String/readonly/ # noqa: E501
#     \~English Import path for application class
# @param[in] port/string string/string/readwrite/
#     \~English String to be converted
# @param[out] port/element element/complex/
#     \~English Port carrying the JSON structure
# @par EAGLE_END
class String2JSON(BarrierAppDROP):
    def initialize(self, **kwargs):
        BarrierAppDROP.initialize(self, **kwargs)

    def readData(self):
        input = self.inputs[0]  # ignore all but the first
        try:
            data = json.loads(droputils.allDropContents(input))
        except json.decoder.JSONDecodeError:
            raise TypeError
        self.json = data

    def writeData(self):
        """
        Prepare the data and write to all outputs
        """
        # write rest to array output
        # and value to every other output
        for output in self.outputs:
            d = pickle.dumps(self.json)
            output.len = len(d)
            output.write(d)

    def run(self):
        self.readData()
        self.writeData()


##
# @brief GenericGather
# @details App that reads all its inputs and simply writes them in
# concatenated to all its outputs. This can be used stand-alone or
# as part of a Gather. It does not do anything to the data, just
# passing it on.
#
# @par EAGLE_START
# @param category PythonApp
# @param/appclass Application Class/dlg_example_cmpts.apps.GenericGather/String/readonly/ # noqa: E501
#     \~English Import path for application class
# @param[in] port/input input/complex/readwrite/
#     \~English 0-base placeholder port for inputs
# @param[out] port/output output/complex/
#     \~English Placeholder port for outputs
# @par EAGLE_END
class GenericGather(BarrierAppDROP):
    def initialize(self, **kwargs):
        BarrierAppDROP.initialize(self, **kwargs)

    def readWriteData(self):

        inputs = self.inputs
        outputs = self.outputs
        total_len = 0
        for input in inputs:
            total_len += input.len
        for output in outputs:
            output.len = total_len
            for input in inputs:
                d = droputils.allDropContents(input)
                output.write(d)

    def run(self):
        self.readWriteData()
