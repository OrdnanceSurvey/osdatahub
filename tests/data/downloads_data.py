import itertools
from typeguard import TypeCheckError

from osdatahub.DownloadsAPI.downloads_api import _DownloadObj
from pytest import param
from tqdm import tqdm


def generate_product_list_params(file_name, file_format, file_subformat, area, return_downloadobj):
    params = {
        "fileName": file_name,
        "format": file_format,
        "subformat": file_subformat,
        "area": area
    }
    return dict(filter(lambda i: i[1] is not None, params.items()))


def product_list_pass(product_name):
    test_variables = "file_name, file_format, file_subformat, area, return_downloadobj, expected_url, expected_params"
    file_names = ["test_file_name", "test_filename2"]
    file_formats = ["test_file_format"]
    file_subformats = ["test_file_subformat"]
    area = ["GB", "TM"]
    return_downloadobj_values = [True, False]

    permutations = list(itertools.product(file_names, file_formats, file_subformats, area, return_downloadobj_values))
    expected_params = [generate_product_list_params(*p) for p in permutations]
    test_data = [param(*values, f"https://api.os.uk/downloads/v1/products/{product_name}/downloads", expected_param)
                 for values, expected_param in zip(permutations, expected_params)]

    return test_variables, test_data


def product_list_fail():
    test_variables = "file_name, file_format, file_subformat, area, return_downloadobj, expected_result"

    test_data = [
        param(123, None, None, None, False, (TypeError, TypeCheckError)),
        param(None, 123, None, None, False, (TypeError, TypeCheckError)),
        param(None, None, 123, None, False, (TypeError, TypeCheckError)),
        param(None, None, None, 123, False, (TypeError, TypeCheckError)),
        param(None, None, None, "Wrong Area Code", False, (ValueError, TypeCheckError)),
        param(None, None, None, None, "wrong value", (TypeError, TypeCheckError))
    ]
    return test_variables, test_data


def fake_product(i):
    return {
        "md5": f"test_md5{i}",
        "size": f"{i}",
        "url": f"https://testurl{i}.com",
        "format": f"test_format{i}",
        "test_subformat": f"test_subformat{i}",
        "area": "HP",
        "fileName": f"testfile{i}.zip"
    }


def download_pass():
    test_variables = "output_dir, " \
                     "download_multiple, " \
                     "overwrite, " \
                     "processes, " \
                     "product_list_mock_return , " \
                     "downloadobj_mock_return, " \
                     "expected_download_return, " \
                     "download_called_value"

    fake_products = [fake_product(x) for x in range[5]]

    test_data = [
        param(".",
              True,
              True,
              1,
              [_DownloadObj(url="testurl.com", size=100, file_name="testfile.zip")],

              ),
        param(fake_products[0],
              ".",
              False,
              True,
              [".", True, tqdm()]
              ),
        param(fake_products[0],
              "test",
              False,
              True,
              )
    ]

    return test_variables, test_data
