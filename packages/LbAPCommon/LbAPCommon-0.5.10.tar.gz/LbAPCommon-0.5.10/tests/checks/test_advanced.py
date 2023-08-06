###############################################################################
# (c) Copyright 2021 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "COPYING".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from textwrap import dedent

import pytest

import LbAPCommon
from LbAPCommon import checks
from LbAPCommon.checks_utils import checks_to_JSON

pytest.importorskip("XRootD")


def test_num_entries_parsing_to_JSON():
    rendered_yaml = dedent(
        """\
    checks:
        check_num_entries:
            type: num_entries
            count: 1000
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check_num_entries
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)

    job_name = list(jobs_data.keys())[0]
    check_name = list(checks_data.keys())[0]

    result = checks.run_job_checks(
        [check_name],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )[check_name]

    check_results_with_job = {
        job_name: {
            check_name: result,
        }
    }

    checks_json = checks_to_JSON(checks_data, check_results_with_job)

    json_expected = dedent(
        """\
    {
      "job_1": {
        "check_num_entries": {
          "passed": true,
          "messages": [
            "Found 5135823 in DecayTree (1000 required)"
          ],
          "input": {
            "type": "num_entries",
            "count": 1000,
            "tree_pattern": "DecayTree"
          },
          "output": {
            "DecayTree": {
              "num_entries": 5135823
            }
          }
        }
      }
    }"""
    )

    assert checks_json == json_expected


def test_range_parsing_to_JSON():
    rendered_yaml = dedent(
        """\
    checks:
        check_range:
            type: range
            expression: H1_PZ
            limits:
                min: 0
                max: 500000
            blind_ranges:
                -
                    min: 80000
                    max: 100000
                -
                    min: 180000
                    max: 200000
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check_range
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)

    job_name = list(jobs_data.keys())[0]
    check_name = list(checks_data.keys())[0]

    result = checks.run_job_checks(
        [check_name],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )[check_name]

    check_results_with_job = {
        job_name: {
            check_name: result,
        }
    }

    checks_json = checks_to_JSON(checks_data, check_results_with_job)

    json_expected = dedent(
        """\
    {
      "job_1": {
        "check_range": {
          "passed": true,
          "messages": [
            "Histogram of H1_PZ successfully filled from TTree DecayTree (contains 4776546.0 events)"
          ],
          "input": {
            "type": "range",
            "expression": "H1_PZ",
            "limits": {
              "min": 0.0,
              "max": 500000.0
            },
            "blind_ranges": [
              {
                "min": 80000.0,
                "max": 100000.0
              },
              {
                "min": 180000.0,
                "max": 200000.0
              }
            ],
            "tree_pattern": "DecayTree",
            "n_bins": 50
          },
          "output": {
            "DecayTree": {
              "histograms": [
                {
                  "_typename": "TH1D",
                  "fUniqueID": 0,
                  "fBits": 0,
                  "fName": null,
                  "fTitle": "",
                  "fLineColor": 602,
                  "fLineStyle": 1,
                  "fLineWidth": 1,
                  "fFillColor": 0,
                  "fFillStyle": 1001,
                  "fMarkerColor": 1,
                  "fMarkerStyle": 1,
                  "fMarkerSize": 1.0,
                  "fNcells": 52,
                  "fXaxis": {
                    "_typename": "TAxis",
                    "fUniqueID": 0,
                    "fBits": 0,
                    "fName": "H1_PZ",
                    "fTitle": "H1_PZ",
                    "fNdivisions": 510,
                    "fAxisColor": 1,
                    "fLabelColor": 1,
                    "fLabelFont": 42,
                    "fLabelOffset": 0.005,
                    "fLabelSize": 0.035,
                    "fTickLength": 0.03,
                    "fTitleOffset": 1.0,
                    "fTitleSize": 0.035,
                    "fTitleColor": 1,
                    "fTitleFont": 42,
                    "fNbins": 50,
                    "fXmin": 0.0,
                    "fXmax": 500000.0,
                    "fXbins": [],
                    "fFirst": 0,
                    "fLast": 0,
                    "fBits2": 0,
                    "fTimeDisplay": false,
                    "fTimeFormat": "",
                    "fLabels": null,
                    "fModLabs": null
                  },
                  "fYaxis": {
                    "_typename": "TAxis",
                    "fUniqueID": 0,
                    "fBits": 0,
                    "fName": "yaxis",
                    "fTitle": "",
                    "fNdivisions": 510,
                    "fAxisColor": 1,
                    "fLabelColor": 1,
                    "fLabelFont": 42,
                    "fLabelOffset": 0.005,
                    "fLabelSize": 0.035,
                    "fTickLength": 0.03,
                    "fTitleOffset": 1.0,
                    "fTitleSize": 0.035,
                    "fTitleColor": 1,
                    "fTitleFont": 42,
                    "fNbins": 1,
                    "fXmin": 0.0,
                    "fXmax": 1.0,
                    "fXbins": [],
                    "fFirst": 0,
                    "fLast": 0,
                    "fBits2": 0,
                    "fTimeDisplay": false,
                    "fTimeFormat": "",
                    "fLabels": null,
                    "fModLabs": null
                  },
                  "fZaxis": {
                    "_typename": "TAxis",
                    "fUniqueID": 0,
                    "fBits": 0,
                    "fName": "zaxis",
                    "fTitle": "",
                    "fNdivisions": 510,
                    "fAxisColor": 1,
                    "fLabelColor": 1,
                    "fLabelFont": 42,
                    "fLabelOffset": 0.005,
                    "fLabelSize": 0.035,
                    "fTickLength": 0.03,
                    "fTitleOffset": 1.0,
                    "fTitleSize": 0.035,
                    "fTitleColor": 1,
                    "fTitleFont": 42,
                    "fNbins": 1,
                    "fXmin": 0.0,
                    "fXmax": 1.0,
                    "fXbins": [],
                    "fFirst": 0,
                    "fLast": 0,
                    "fBits2": 0,
                    "fTimeDisplay": false,
                    "fTimeFormat": "",
                    "fLabels": null,
                    "fModLabs": null
                  },
                  "fBarOffset": 0,
                  "fBarWidth": 1000,
                  "fEntries": 4776546.0,
                  "fTsumw": 4776546.0,
                  "fTsumw2": 4776546.0,
                  "fTsumwx": 214617100000.0,
                  "fTsumwx2": 2.245448605e+16,
                  "fMaximum": -1111.0,
                  "fMinimum": -1111.0,
                  "fNormFactor": 0.0,
                  "fContour": [],
                  "fSumw2": [
                    0.0,
                    1068515.0,
                    911171.0,
                    630749.0,
                    449908.0,
                    336446.0,
                    265471.0,
                    219142.0,
                    186119.0,
                    0.0,
                    0.0,
                    122888.0,
                    107285.0,
                    92548.0,
                    78798.0,
                    65261.0,
                    53400.0,
                    44413.0,
                    36398.0,
                    0.0,
                    0.0,
                    19816.0,
                    16119.0,
                    12874.0,
                    10512.0,
                    8506.0,
                    6869.0,
                    5591.0,
                    4593.0,
                    3772.0,
                    3049.0,
                    2522.0,
                    2166.0,
                    1754.0,
                    1520.0,
                    1286.0,
                    1033.0,
                    932.0,
                    822.0,
                    720.0,
                    610.0,
                    474.0,
                    443.0,
                    391.0,
                    347.0,
                    310.0,
                    262.0,
                    210.0,
                    186.0,
                    171.0,
                    174.0,
                    0.0
                  ],
                  "fOption": "",
                  "fFunctions": {
                    "_typename": "TList",
                    "name": "TList",
                    "arr": [],
                    "opt": []
                  },
                  "fBufferSize": 0,
                  "fBuffer": [],
                  "fBinStatErrOpt": 0,
                  "fStatOverflows": 2
                }
              ],
              "num_entries": 4776546,
              "mean": 44931.44209225662,
              "variance": 2682154203.3712554,
              "stddev": 51789.51827707278,
              "num_entries_in_mean_window": 0
            }
          }
        }
      }
    }"""
    )

    assert checks_json == json_expected


def test_range_2d_parsing_to_JSON():
    rendered_yaml = dedent(
        """\
    checks:
        check_range_nd:
            type: range_nd
            expressions:
                x: H1_PZ
                y: H2_PZ
            limits:
                x:
                    min: 0
                    max: 500000
                y:
                    min: 0
                    max: 500000
            n_bins:
                x: 25
                y: 25
            tree_pattern: DecayTree

    job_1:
        application: DaVinci/v45r8
        input:
            bk_query: /bookkeeping/path/ALLSTREAMS.DST
        output: FILETYPE.ROOT
        options:
            - options.py
            - $VAR/a.py
        wg: Charm
        inform: a.b@c.d
        checks:
            - check_range_nd
    """
    )
    jobs_data, checks_data = LbAPCommon.parse_yaml(rendered_yaml)

    job_name = list(jobs_data.keys())[0]
    check_name = list(checks_data.keys())[0]

    result = checks.run_job_checks(
        [check_name],
        checks_data,
        [
            "root://eospublic.cern.ch//eos/opendata/lhcb/AntimatterMatters2017/data/B2HHH_MagnetDown.root"
        ],
    )[check_name]

    check_results_with_job = {
        job_name: {
            check_name: result,
        }
    }

    checks_json = checks_to_JSON(checks_data, check_results_with_job)

    json_expected = dedent(
        """\
    {
      "job_1": {
        "check_range_nd": {
          "passed": true,
          "messages": [
            "Histogram of H1_PZ, H2_PZ successfully filled from TTree DecayTree (contains 5134453.0 events)"
          ],
          "input": {
            "type": "range_nd",
            "expressions": {
              "x": "H1_PZ",
              "y": "H2_PZ"
            },
            "limits": {
              "x": {
                "min": 0.0,
                "max": 500000.0
              },
              "y": {
                "min": 0.0,
                "max": 500000.0
              }
            },
            "n_bins": {
              "x": 25,
              "y": 25
            },
            "tree_pattern": "DecayTree"
          },
          "output": {
            "DecayTree": {
              "histograms": [
                {
                  "_typename": "TH2D",
                  "fUniqueID": 0,
                  "fBits": 0,
                  "fName": null,
                  "fTitle": "",
                  "fLineColor": 602,
                  "fLineStyle": 1,
                  "fLineWidth": 1,
                  "fFillColor": 0,
                  "fFillStyle": 1001,
                  "fMarkerColor": 1,
                  "fMarkerStyle": 1,
                  "fMarkerSize": 1.0,
                  "fNcells": 729,
                  "fXaxis": {
                    "_typename": "TAxis",
                    "fUniqueID": 0,
                    "fBits": 0,
                    "fName": "H1_PZ",
                    "fTitle": "H1_PZ",
                    "fNdivisions": 510,
                    "fAxisColor": 1,
                    "fLabelColor": 1,
                    "fLabelFont": 42,
                    "fLabelOffset": 0.005,
                    "fLabelSize": 0.035,
                    "fTickLength": 0.03,
                    "fTitleOffset": 1.0,
                    "fTitleSize": 0.035,
                    "fTitleColor": 1,
                    "fTitleFont": 42,
                    "fNbins": 25,
                    "fXmin": 0.0,
                    "fXmax": 500000.0,
                    "fXbins": [],
                    "fFirst": 0,
                    "fLast": 0,
                    "fBits2": 0,
                    "fTimeDisplay": false,
                    "fTimeFormat": "",
                    "fLabels": null,
                    "fModLabs": null
                  },
                  "fYaxis": {
                    "_typename": "TAxis",
                    "fUniqueID": 0,
                    "fBits": 0,
                    "fName": "H2_PZ",
                    "fTitle": "H2_PZ",
                    "fNdivisions": 510,
                    "fAxisColor": 1,
                    "fLabelColor": 1,
                    "fLabelFont": 42,
                    "fLabelOffset": 0.005,
                    "fLabelSize": 0.035,
                    "fTickLength": 0.03,
                    "fTitleOffset": 1.0,
                    "fTitleSize": 0.035,
                    "fTitleColor": 1,
                    "fTitleFont": 42,
                    "fNbins": 25,
                    "fXmin": 0.0,
                    "fXmax": 500000.0,
                    "fXbins": [],
                    "fFirst": 0,
                    "fLast": 0,
                    "fBits2": 0,
                    "fTimeDisplay": false,
                    "fTimeFormat": "",
                    "fLabels": null,
                    "fModLabs": null
                  },
                  "fZaxis": {
                    "_typename": "TAxis",
                    "fUniqueID": 0,
                    "fBits": 0,
                    "fName": "zaxis",
                    "fTitle": "",
                    "fNdivisions": 510,
                    "fAxisColor": 1,
                    "fLabelColor": 1,
                    "fLabelFont": 42,
                    "fLabelOffset": 0.005,
                    "fLabelSize": 0.035,
                    "fTickLength": 0.03,
                    "fTitleOffset": 1.0,
                    "fTitleSize": 0.035,
                    "fTitleColor": 1,
                    "fTitleFont": 42,
                    "fNbins": 1,
                    "fXmin": 0.0,
                    "fXmax": 1.0,
                    "fXbins": [],
                    "fFirst": 0,
                    "fLast": 0,
                    "fBits2": 0,
                    "fTimeDisplay": false,
                    "fTimeFormat": "",
                    "fLabels": null,
                    "fModLabs": null
                  },
                  "fBarOffset": 0,
                  "fBarWidth": 1000,
                  "fEntries": 5135823.0,
                  "fTsumw": 5134453.0,
                  "fTsumw2": 5134453.0,
                  "fTsumwx": 254786850000.0,
                  "fTsumwx2": 2.69808253e+16,
                  "fMaximum": -1111.0,
                  "fMinimum": -1111.0,
                  "fNormFactor": 0.0,
                  "fContour": [],
                  "fSumw2": [
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1018980.0,
                    617269.0,
                    364465.0,
                    259905.0,
                    208043.0,
                    167270.0,
                    130047.0,
                    92642.0,
                    64561.0,
                    44079.0,
                    29506.0,
                    19241.0,
                    12641.0,
                    8424.0,
                    5641.0,
                    3837.0,
                    2677.0,
                    1871.0,
                    1447.0,
                    1083.0,
                    750.0,
                    597.0,
                    448.0,
                    316.0,
                    277.0,
                    1012.0,
                    0.0,
                    500540.0,
                    255329.0,
                    132717.0,
                    84353.0,
                    57993.0,
                    40397.0,
                    27584.0,
                    17926.0,
                    11441.0,
                    7366.0,
                    4528.0,
                    2917.0,
                    1890.0,
                    1220.0,
                    755.0,
                    560.0,
                    365.0,
                    284.0,
                    181.0,
                    164.0,
                    89.0,
                    89.0,
                    80.0,
                    51.0,
                    42.0,
                    222.0,
                    0.0,
                    234750.0,
                    113352.0,
                    58847.0,
                    35695.0,
                    22481.0,
                    14084.0,
                    8606.0,
                    5174.0,
                    3097.0,
                    1860.0,
                    1150.0,
                    733.0,
                    479.0,
                    313.0,
                    224.0,
                    145.0,
                    121.0,
                    89.0,
                    64.0,
                    41.0,
                    36.0,
                    26.0,
                    17.0,
                    15.0,
                    18.0,
                    67.0,
                    0.0,
                    116342.0,
                    52786.0,
                    26582.0,
                    14985.0,
                    9128.0,
                    5198.0,
                    3062.0,
                    1714.0,
                    953.0,
                    675.0,
                    392.0,
                    246.0,
                    171.0,
                    104.0,
                    94.0,
                    53.0,
                    53.0,
                    24.0,
                    22.0,
                    18.0,
                    18.0,
                    10.0,
                    12.0,
                    5.0,
                    3.0,
                    24.0,
                    0.0,
                    58377.0,
                    24158.0,
                    11571.0,
                    6261.0,
                    3512.0,
                    1931.0,
                    1149.0,
                    645.0,
                    375.0,
                    230.0,
                    165.0,
                    109.0,
                    85.0,
                    59.0,
                    43.0,
                    47.0,
                    27.0,
                    16.0,
                    16.0,
                    11.0,
                    9.0,
                    5.0,
                    7.0,
                    2.0,
                    2.0,
                    16.0,
                    0.0,
                    27836.0,
                    10419.0,
                    4716.0,
                    2356.0,
                    1292.0,
                    680.0,
                    433.0,
                    277.0,
                    183.0,
                    105.0,
                    88.0,
                    58.0,
                    49.0,
                    23.0,
                    26.0,
                    21.0,
                    15.0,
                    13.0,
                    10.0,
                    1.0,
                    7.0,
                    3.0,
                    4.0,
                    1.0,
                    1.0,
                    5.0,
                    0.0,
                    12717.0,
                    4186.0,
                    1697.0,
                    894.0,
                    466.0,
                    286.0,
                    215.0,
                    126.0,
                    79.0,
                    72.0,
                    46.0,
                    30.0,
                    20.0,
                    15.0,
                    18.0,
                    8.0,
                    5.0,
                    4.0,
                    2.0,
                    3.0,
                    1.0,
                    4.0,
                    2.0,
                    0.0,
                    0.0,
                    7.0,
                    0.0,
                    5471.0,
                    1613.0,
                    609.0,
                    386.0,
                    250.0,
                    157.0,
                    101.0,
                    63.0,
                    47.0,
                    40.0,
                    22.0,
                    16.0,
                    10.0,
                    11.0,
                    6.0,
                    9.0,
                    2.0,
                    4.0,
                    4.0,
                    4.0,
                    2.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    5.0,
                    0.0,
                    2326.0,
                    715.0,
                    315.0,
                    173.0,
                    97.0,
                    73.0,
                    55.0,
                    36.0,
                    29.0,
                    20.0,
                    15.0,
                    15.0,
                    10.0,
                    4.0,
                    8.0,
                    3.0,
                    7.0,
                    5.0,
                    6.0,
                    2.0,
                    1.0,
                    1.0,
                    0.0,
                    2.0,
                    1.0,
                    2.0,
                    0.0,
                    1118.0,
                    352.0,
                    161.0,
                    94.0,
                    61.0,
                    32.0,
                    33.0,
                    24.0,
                    22.0,
                    18.0,
                    8.0,
                    10.0,
                    8.0,
                    4.0,
                    2.0,
                    1.0,
                    0.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    1.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    582.0,
                    192.0,
                    91.0,
                    65.0,
                    50.0,
                    25.0,
                    23.0,
                    15.0,
                    7.0,
                    7.0,
                    5.0,
                    4.0,
                    4.0,
                    2.0,
                    1.0,
                    2.0,
                    0.0,
                    4.0,
                    1.0,
                    1.0,
                    0.0,
                    1.0,
                    0.0,
                    2.0,
                    0.0,
                    0.0,
                    0.0,
                    292.0,
                    121.0,
                    55.0,
                    31.0,
                    22.0,
                    15.0,
                    14.0,
                    8.0,
                    8.0,
                    2.0,
                    6.0,
                    2.0,
                    3.0,
                    2.0,
                    2.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    2.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    155.0,
                    67.0,
                    35.0,
                    23.0,
                    16.0,
                    8.0,
                    10.0,
                    4.0,
                    4.0,
                    3.0,
                    0.0,
                    2.0,
                    1.0,
                    1.0,
                    0.0,
                    1.0,
                    1.0,
                    1.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    2.0,
                    0.0,
                    89.0,
                    30.0,
                    17.0,
                    17.0,
                    1.0,
                    6.0,
                    3.0,
                    2.0,
                    2.0,
                    1.0,
                    1.0,
                    0.0,
                    2.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    46.0,
                    23.0,
                    15.0,
                    4.0,
                    7.0,
                    5.0,
                    0.0,
                    1.0,
                    1.0,
                    0.0,
                    3.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    27.0,
                    11.0,
                    8.0,
                    4.0,
                    4.0,
                    3.0,
                    5.0,
                    1.0,
                    0.0,
                    1.0,
                    0.0,
                    1.0,
                    1.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    16.0,
                    9.0,
                    5.0,
                    7.0,
                    1.0,
                    1.0,
                    1.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    2.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    11.0,
                    5.0,
                    2.0,
                    3.0,
                    2.0,
                    0.0,
                    3.0,
                    1.0,
                    1.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    5.0,
                    6.0,
                    4.0,
                    2.0,
                    3.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    2.0,
                    0.0,
                    3.0,
                    0.0,
                    0.0,
                    1.0,
                    2.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    4.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    3.0,
                    4.0,
                    2.0,
                    2.0,
                    1.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    2.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    2.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    2.0,
                    0.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0
                  ],
                  "fOption": "",
                  "fFunctions": {
                    "_typename": "TList",
                    "name": "TList",
                    "arr": [],
                    "opt": []
                  },
                  "fBufferSize": 0,
                  "fBuffer": [],
                  "fBinStatErrOpt": 0,
                  "fStatOverflows": 2,
                  "fScalefactor": 1.0,
                  "fTsumwy": 127193530000.0,
                  "fTsumwy2": 6083686900000000.0,
                  "fTsumwxy": 5285343700000000.0
                }
              ],
              "num_entries": 5135823
            }
          }
        }
      }
    }"""
    )

    assert checks_json == json_expected
