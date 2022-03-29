import os
from pathlib import Path

import pandas as pd

from unittest.mock import patch
from extract.document import Document, Page, TextBlock
from processor.postprocessor import (
    HyphenationPostProcessor,
    AdobeListGroupingPostProcessor,
    AdobeTextStylingPostProcessor,
)
import pytest


@pytest.fixture
def test_input_path() -> Path:
    return (
        Path(__file__).parent / "data/cclw-1318-d7f66920a18e4ddf94c83cf21fa2bcfa.json"
    )


# Keep these as fixtures in case they get more complex in the future.
@pytest.fixture
def adobe_list_postprocessor() -> AdobeListGroupingPostProcessor:
    return AdobeListGroupingPostProcessor()


@pytest.fixture
def adobe_text_styling_postprocessor() -> AdobeTextStylingPostProcessor:
    return AdobeTextStylingPostProcessor()


@pytest.fixture
def adobe_hyphenation_postprocessor() -> HyphenationPostProcessor:
    return HyphenationPostProcessor()


def test_hyphenation_postprocessor_rewrap_hyphenated_words(
    adobe_hyphenation_postprocessor,
):
    # Test case 1: hyphenation for incomplete words. cf pd 2 of cclw-8650-24af4f121de143baa3b633481f7adb78.pdf
    # TODO:
    #  The examples in this test case indicates the presence of a bug (e.g. the word performance is truncated before
    #  the next text block. Observing the results files indicates that this is because the next element is considered
    #  a HyphenSpan element even though the first hyphenated word (remodelling) does not suffer from the same issue.
    #  It's unclear how common this is is, but it happens in this document more than once (including 2nd test case).
    #  Leaving these cases for now as the bug is out of the scope of this test.
    input = [
        "Targets of incentive measures are all new construction of buildings, or extensions, renovations, improvements, remodel-",
        "ling, pre-installation/repairs of cooling system equipment that contribute to the improvement of energy conservation perfor",
    ]
    expected = [
        "Targets of incentive measures are all new construction of buildings, or extensions, renovations, improvements, ",
        "remodelling, pre-installation/repairs of cooling system equipment that contribute to the improvement of energy conservation perfor",
    ]
    output = adobe_hyphenation_postprocessor._rewrap_hyphenated_words(input)
    assert output == expected

    # Test case 2: Keep the hyphenation if the word is a sub-word of the English Language.
    # cf. pg 1 of cclw-8149-5b598bd3e88c4ce99f44cfbd283c9679.pdf
    input_2 = [
        "The extreme demand on these two plants makes the ",
        "power supply highly unreliable. During the dry season the ",
        "power supply deficit can increase from 13 to 23.5 MW, ",
        "meaning that people increasingly turn to expensive, diesel-",
        "powered generators as an alternative source of energy. ",
        "Technical and commercial losses of 24.4% have further ",
        "reduced the availability of electricity. Burundi’s energy envi",
    ]
    expected_2 = [
        "The extreme demand on these two plants makes the ",
        "power supply highly unreliable. During the dry season the ",
        "power supply deficit can increase from 13 to 23.5 MW, ",
        "meaning that people increasingly turn to expensive, ",
        "diesel-powered generators as an alternative source of energy. ",
        "Technical and commercial losses of 24.4% have further ",
        "reduced the availability of electricity. Burundi’s energy envi",
    ]
    output_2 = adobe_hyphenation_postprocessor._rewrap_hyphenated_words(input_2)

    assert output_2 == expected_2


def test_adobe_list_find_all_list_occurrences(adobe_list_postprocessor):
    regex = adobe_list_postprocessor.list_regex_pattern
    # Case 1:
    input = ["Document", "L[3]", "LI", "LBody", "Span[2]"]
    expected_output = ["L[3]"]
    actual_output = adobe_list_postprocessor._find_all_list_occurrences(regex, input)
    assert actual_output == expected_output
    # Case 2:
    input_2 = ["Document", "L", "LI", "LBody", "Span[2]", "L[1]"]
    expected_output_2 = ["L", "L[1]"]
    actual_output_2 = adobe_list_postprocessor._find_all_list_occurrences(
        regex, input_2
    )
    assert actual_output_2 == expected_output_2
    # Case 3: No matching regex.
    input_3 = ["Document", "P"]
    actual_output_3 = adobe_list_postprocessor._find_all_list_occurrences(
        regex, input_3
    )
    assert actual_output_3 == []


def test_adobe_text_styling_merge_test_blocks(adobe_text_styling_postprocessor):
    # Case 1: We can see that the blocks have the same path but are separated due to styling
    # markers such as underlines. We want to merge them.
    # cf. cclw-4974. This is actually a bad case, but for purposes of testing this function is fine.
    example = (
        {
            "text": ["You are here: "],
            "text_block_id": "p0_b6",
            "coords": [
                [44.00700378417969, 133.54104614257812],
                [103.91917419433594, 133.54104614257812],
                [44.00700378417969, 146.8739776611328],
                [103.91917419433594, 146.8739776611328],
            ],
            "type": "P",
            "path": ["Document", "P[2]"],
            "custom_attributes": None,
        },
        {
            "text": ["PacLII "],
            "text_block_id": "p0_b7",
            "coords": [
                [106.28599548339844, 133.7310791015625],
                [136.11973571777344, 133.7310791015625],
                [106.28599548339844, 146.8739776611328],
                [136.11973571777344, 146.8739776611328],
            ],
            "type": "StyleSpan",
            "path": ["Document", "P[2]"],
            "custom_attributes": {
                "TextDecorationColor": [0, 0.2666629999999941, 0.7294159999999863],
                "TextDecorationThickness": 0,
                "TextDecorationType": "Underline",
            },
        },
        {
            "text": ["Databases "],
            "text_block_id": "p0_b9",
            "coords": [
                [149.80599975585938, 133.7310791015625],
                [192.9376678466797, 133.7310791015625],
                [149.80599975585938, 146.8739776611328],
                [192.9376678466797, 146.8739776611328],
            ],
            "type": "StyleSpan",
            "path": ["Document", "P[2]"],
            "custom_attributes": {
                "TextDecorationColor": [0, 0.2666629999999941, 0.7294159999999863],
                "TextDecorationThickness": 0,
                "TextDecorationType": "Underline",
            },
        },
        {
            "text": ["Palau Net Metering Act of 2009, RPPL 8-39 2012 "],
            "text_block_id": "p0_b12",
            "coords": [
                [332.98500061035156, 133.54104614257812],
                [544.6615600585938, 133.54104614257812],
                [332.98500061035156, 146.8739776611328],
                [544.6615600585938, 146.8739776611328],
            ],
            "type": "P",
            "path": ["Document", "P[2]"],
            "custom_attributes": None,
        },
    )

    expected_output = {
        "text": [
            "You are here: PacLII Databases Palau Net Metering Act of 2009, RPPL 8-39 2012 "
        ],
        "coords": [
            [44.00700378417969, 133.54104614257812],
            [544.6615600585938, 133.54104614257812],
            [44.00700378417969, 146.8739776611328],
            [544.6615600585938, 146.8739776611328],
        ],
        "path": ["Document", "P[2]"],
        "text_block_id": "p0_b6_merged",
        "custom_attributes": {
            "styleSpans": [
                {"style": "underline", "start_idx": 14, "end_idx": 19},
                {"style": "underline", "start_idx": 21, "end_idx": 29},
            ]
        },
    }

    actual_output = adobe_text_styling_postprocessor.merge_text_blocks(example)
    assert actual_output == expected_output


def test_adobe_list_processor_semantic_lists(adobe_list_postprocessor):
    # Case 1: A list with multiple nesting levels. This if from cclw-4974, pg.
    # Ignore most of the df input as it's just metadata, here what is being tested is
    # the formatting of the text. The rest of the pandas stuff is required for some
    # of the procesing but is not being tested here.
    in_df = pd.DataFrame(
        {
            "text": {
                0: ["(a)"],
                1: [
                    " shall develop a standard contract providing for net energy metering, and shall, upon request, make this contract available to eligible customer-generators; "
                ],
                2: ["(b)"],
                3: [
                    " shall prepare appropriate technical standards for grid connection of renewable energy systems, and inspect and provide a license for those renewable energy installations that meet the technical standards developed by P.P.U.C. and the other provisions of this legislation. Issuance of a license shall be solely to show that the P.P.U.C. has approved the interconnection of the customer=s renewable energy system and the P.P.U.C. grid and shall not be interpreted to impose liability or approval by the P.P.U.C. for any part of the renewable energy system, its design, or its method of implementation. The technical standards imposed will be based solely on those necessary to ensure the safety of P.P.U.C. personnel and for the maintenance of P.P.U.C, power quality. Standards and technical requirements shall be consistent with existing technical practices for similar types of installations in the United States, Australia, or the European Union. "
                ],
                4: ["(1)"],
                5: [
                    " A licensee shall inform the P.P.U.C. of any proposed technical changes to the renewable energy system that affects either the maximum power output or the components that provide the interconnection between the renewable energy system and the P.P.U.C. grid and will, under the licensing agreement, not make those changes without P.P.U.C. approval. "
                ],
                6: ["(2)"],
                7: [
                    " The failure of a licensee to promptly inform the P.P.U.C. in writing of any technical changes to the renewable energy system that affects any of the above may, at the P.P.U.C. discretion, result in a fine of not more than two hundred dollars ($200). "
                ],
                8: ["(c)"],
                9: [
                    " shall, at its own-expense, make available to each of its eligible customer generators who have installed a net metering system the meter (or set of meters) that is needed to determine the net flow of electricity both into and out of the electricity grid; "
                ],
            },
            "text_block_id": {
                0: "p3_b8",
                1: "p3_b9",
                2: "p3_b10",
                3: "p3_b11",
                4: "p3_b12",
                5: "p3_b13",
                6: "p3_b14",
                7: "p3_b15",
                8: "p3_b16",
                9: "p3_b17",
            },
            "coords": {
                0: [
                    [44.00700378417969, 339.5602569580078],
                    [57.333221435546875, 339.5602569580078],
                    [44.00700378417969, 355.3356170654297],
                    [57.333221435546875, 355.3356170654297],
                ],
                1: [
                    [44.006988525390625, 339.5602569580078],
                    [534.8775482177734, 339.5602569580078],
                    [44.006988525390625, 368.8419189453125],
                    [534.8775482177734, 368.8419189453125],
                ],
                2: [
                    [44.00700378417969, 404.0902557373047],
                    [58.00553894042969, 404.0902557373047],
                    [44.00700378417969, 419.86561584472656],
                    [58.00553894042969, 419.86561584472656],
                ],
                3: [
                    [44.00697326660156, 404.0902557373047],
                    [549.0081329345703, 404.0902557373047],
                    [44.00697326660156, 541.4223175048828],
                    [549.0081329345703, 541.4223175048828],
                ],
                4: [
                    [44.00700378417969, 576.6704559326172],
                    [58.00553894042969, 576.6704559326172],
                    [44.00700378417969, 592.4458160400391],
                    [58.00553894042969, 592.4458160400391],
                ],
                5: [
                    [44.00697326660156, 576.6704559326172],
                    [550.2843170166016, 576.6704559326172],
                    [44.00697326660156, 632.9647216796875],
                    [550.2843170166016, 632.9647216796875],
                ],
                6: [
                    [44.00700378417969, 668.2130584716797],
                    [58.00553894042969, 668.2130584716797],
                    [44.00700378417969, 683.9884185791016],
                    [58.00553894042969, 683.9884185791016],
                ],
                7: [
                    [44.00697326660156, 668.2130584716797],
                    [542.5611267089844, 668.2130584716797],
                    [44.00697326660156, 711.0010223388672],
                    [542.5611267089844, 711.0010223388672],
                ],
                8: [
                    [44.00700378417969, 746.249267578125],
                    [57.333221435546875, 746.249267578125],
                    [44.00700378417969, 762.0246124267578],
                    [57.333221435546875, 762.0246124267578],
                ],
                9: [
                    [44.006988525390625, 746.249267578125],
                    [534.8199157714844, 746.249267578125],
                    [44.006988525390625, 789.0372161865234],
                    [534.8199157714844, 789.0372161865234],
                ],
            },
            "type": {
                0: "Lbl",
                1: "LBody",
                2: "Lbl",
                3: "ParagraphSpan",
                4: "Lbl",
                5: "LBody",
                6: "Lbl",
                7: "LBody",
                8: "Lbl",
                9: "LBody",
            },
            "path": {
                0: ["Document", "L[4]", "LI", "Lbl"],
                1: ["Document", "L[4]", "LI", "LBody"],
                2: ["Document", "L[4]", "LI[2]", "Lbl"],
                3: ["Document", "L[4]", "LI[2]", "LBody", "ParagraphSpan"],
                4: ["Document", "L[4]", "LI[2]", "LBody", "L", "LI", "Lbl"],
                5: ["Document", "L[4]", "LI[2]", "LBody", "L", "LI", "LBody"],
                6: ["Document", "L[4]", "LI[2]", "LBody", "L", "LI[2]", "Lbl"],
                7: ["Document", "L[4]", "LI[2]", "LBody", "L", "LI[2]", "LBody"],
                8: ["Document", "L[4]", "LI[3]", "Lbl"],
                9: ["Document", "L[4]", "LI[3]", "LBody"],
            },
            "custom_attributes": {
                0: None,
                1: None,
                2: None,
                3: None,
                4: None,
                5: None,
                6: None,
                7: None,
                8: None,
                9: None,
            },
            "page_num": {0: 3, 1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 3},
            "list_num": {0: 1, 1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 2, 8: 1, 9: 1},
            "first_list_index": {
                0: 0,
                1: 0,
                2: 0,
                3: 0,
                4: 4,
                5: 4,
                6: 4,
                7: 4,
                8: 0,
                9: 0,
            },
            "last_list_index": {
                0: 9,
                1: 9,
                2: 9,
                3: 9,
                4: 7,
                5: 7,
                6: 7,
                7: 7,
                8: 9,
                9: 9,
            },
            "first_list_ix_bool": {
                0: True,
                1: False,
                2: False,
                3: False,
                4: True,
                5: False,
                6: False,
                7: False,
                8: False,
                9: False,
            },
            "last_list_ix_bool": {
                0: False,
                1: False,
                2: False,
                3: False,
                4: False,
                5: False,
                6: False,
                7: True,
                8: False,
                9: True,
            },
        }
    )

    expected_out = [
        "\n<li1>\n<Lbl>(a)<\\Lbl><LBody>shall develop a standard contract providing for net energy metering, and shall, upon request, make this contract available to eligible customer-generators;<\\LBody>\n",
        "<Lbl>(b)<\\Lbl><LBody>shall prepare appropriate technical standards for grid connection of renewable energy systems, and inspect and provide a license for those renewable energy installations that meet the technical standards developed by P.P.U.C. and the other provisions of this legislation. Issuance of a license shall be solely to show that the P.P.U.C. has approved the interconnection of the customer=s renewable energy system and the P.P.U.C. grid and shall not be interpreted to impose liability or approval by the P.P.U.C. for any part of the renewable energy system, its design, or its method of implementation. The technical standards imposed will be based solely on those necessary to ensure the safety of P.P.U.C. personnel and for the maintenance of P.P.U.C, power quality. Standards and technical requirements shall be consistent with existing technical practices for similar types of installations in the United States, Australia, or the European Union.<\\LBody>\n",
        "\n<li2>\n<Lbl>(1)<\\Lbl><LBody>A licensee shall inform the P.P.U.C. of any proposed technical changes to the renewable energy system that affects either the maximum power output or the components that provide the interconnection between the renewable energy system and the P.P.U.C. grid and will, under the licensing agreement, not make those changes without P.P.U.C. approval.<\\LBody>\n",
        "<Lbl>(2)<\\Lbl><LBody>The failure of a licensee to promptly inform the P.P.U.C. in writing of any technical changes to the renewable energy system that affects any of the above may, at the P.P.U.C. discretion, result in a fine of not more than two hundred dollars ($200).<\\LBody>\n\n<\\li2>\n",
        "<Lbl>(c)<\\Lbl><LBody>shall, at its own-expense, make available to each of its eligible customer generators who have installed a net metering system the meter (or set of meters) that is needed to determine the net flow of electricity both into and out of the electricity grid;<\\LBody>\n\n<\\li1>\n",
    ]

    actual_out = adobe_list_postprocessor._format_semantic_lists(in_df)
    assert actual_out == expected_out


def test_adobe_list_processor_pprinter(adobe_list_postprocessor):
    # c.f. To see the printed output of this test, use pytest with -rP (passed) or -rx (failed) option. This can be useful as it will
    # show how the multiple nesting levels work.
    full_list_text = [
        "\n<li1>\n<Lbl>(a)<\\Lbl><LBody>shall develop a standard contract providing for net energy metering, and shall, upon request, make this contract available to eligible customer-generators;<\\LBody>\n",
        "<Lbl>(b)<\\Lbl><LBody>shall prepare appropriate technical standards for grid connection of renewable energy systems, and inspect and provide a license for those renewable energy installations that meet the technical standards developed by P.P.U.C. and the other provisions of this legislation. Issuance of a license shall be solely to show that the P.P.U.C. has approved the interconnection of the customer=s renewable energy system and the P.P.U.C. grid and shall not be interpreted to impose liability or approval by the P.P.U.C. for any part of the renewable energy system, its design, or its method of implementation. The technical standards imposed will be based solely on those necessary to ensure the safety of P.P.U.C. personnel and for the maintenance of P.P.U.C, power quality. Standards and technical requirements shall be consistent with existing technical practices for similar types of installations in the United States, Australia, or the European Union.<\\LBody>\n",
        "\n<li2>\n<Lbl>(1)<\\Lbl><LBody>A licensee shall inform the P.P.U.C. of any proposed technical changes to the renewable energy system that affects either the maximum power output or the components that provide the interconnection between the renewable energy system and the P.P.U.C. grid and will, under the licensing agreement, not make those changes without P.P.U.C. approval.<\\LBody>\n",
        "<Lbl>(2)<\\Lbl><LBody>The failure of a licensee to promptly inform the P.P.U.C. in writing of any technical changes to the renewable energy system that affects any of the above may, at the P.P.U.C. discretion, result in a fine of not more than two hundred dollars ($200).<\\LBody>\n\n<\\li2>\n",
        "<Lbl>(c)<\\Lbl><LBody>shall, at its own-expense, make available to each of its eligible customer generators who have installed a net metering system the meter (or set of meters) that is needed to determine the net flow of electricity both into and out of the electricity grid;<\\LBody>\n\n<\\li1>\n",
    ]
    expected_out = """* shall develop a standard contract providing for net energy metering, and shall, upon request, make this contract available to eligible customer-generators;
* shall prepare appropriate technical standards for grid connection of renewable energy systems, and inspect and provide a license for those renewable energy installations that meet the technical standards developed by P.P.U.C. and the other provisions of this legislation. Issuance of a license shall be solely to show that the P.P.U.C. has approved the interconnection of the customer=s renewable energy system and the P.P.U.C. grid and shall not be interpreted to impose liability or approval by the P.P.U.C. for any part of the renewable energy system, its design, or its method of implementation. The technical standards imposed will be based solely on those necessary to ensure the safety of P.P.U.C. personnel and for the maintenance of P.P.U.C, power quality. Standards and technical requirements shall be consistent with existing technical practices for similar types of installations in the United States, Australia, or the European Union.
	* A licensee shall inform the P.P.U.C. of any proposed technical changes to the renewable energy system that affects either the maximum power output or the components that provide the interconnection between the renewable energy system and the P.P.U.C. grid and will, under the licensing agreement, not make those changes without P.P.U.C. approval.
	* The failure of a licensee to promptly inform the P.P.U.C. in writing of any technical changes to the renewable energy system that affects any of the above may, at the P.P.U.C. discretion, result in a fine of not more than two hundred dollars ($200).
* shall, at its own-expense, make available to each of its eligible customer generators who have installed a net metering system the meter (or set of meters) that is needed to determine the net flow of electricity both into and out of the electricity grid;
"""
    out_str = adobe_list_postprocessor._pprinter(full_list_text)
    print(out_str)


def test_adobe_list_processor_update_custom_attributes(adobe_list_postprocessor):
    # For this case, look at the custom attributes change, the rest is mostly irrelevant.
    input_blocks = [
        {
            "text": ["• "],
            "text_block_id": "p34_b1",
            "coords": [
                [70.91999816894531, 71.81997680664062],
                [79.44000244140625, 71.81997680664062],
                [70.91999816894531, 86.51997375488281],
                [79.44000244140625, 86.51997375488281],
            ],
            "type": "Lbl",
            "path": ["Document", "L[47]", "LI", "LBody", "L", "LI[2]", "Lbl"],
            "custom_attributes": None,
        },
        {
            "text": [
                "Legislation has been presented to Parliament to increase penalties for drivers using a handheld mobile. This came into effect on 1st March 2017, alongside a major Think! Campaign. "
            ],
            "text_block_id": "p34_b2_merged",
            "coords": [
                [88.80000305175781, 71.8079833984375],
                [507.3838653564453, 71.8079833984375],
                [88.80000305175781, 115.37997436523438],
                [507.3838653564453, 115.37997436523438],
            ],
            "type": "merged_text_block",
            "path": ["Document", "L[47]", "LI", "LBody", "L", "LI[2]", "LBody"],
            "custom_attributes": {
                "styleSpans": [
                    {"style": "superscript", "start_idx": 130, "end_idx": 131}
                ]
            },
        },
        {
            "text": ["• "],
            "text_block_id": "p34_b5",
            "coords": [
                [70.91999816894531, 120.05998229980469],
                [79.44000244140625, 120.05998229980469],
                [70.91999816894531, 134.75997924804688],
                [79.44000244140625, 134.75997924804688],
            ],
            "type": "Lbl",
            "path": ["Document", "L[47]", "LI", "LBody", "L", "LI[3]", "Lbl"],
            "custom_attributes": None,
        },
        {
            "text": [
                "A major piece of research on young driver safety has been commissioned. "
            ],
            "text_block_id": "p34_b6",
            "coords": [
                [88.80000305175781, 120.0479736328125],
                [486.1919250488281, 120.0479736328125],
                [88.80000305175781, 136.0199737548828],
                [486.1919250488281, 136.0199737548828],
            ],
            "type": "LBody",
            "path": ["Document", "L[47]", "LI", "LBody", "L", "LI[3]", "LBody"],
            "custom_attributes": None,
        },
        {
            "text": ["• "],
            "text_block_id": "p34_b7",
            "coords": [
                [70.91999816894531, 140.57997131347656],
                [79.44000244140625, 140.57997131347656],
                [70.91999816894531, 155.2799835205078],
                [79.44000244140625, 155.2799835205078],
            ],
            "type": "Lbl",
            "path": ["Document", "L[47]", "LI", "LBody", "L", "LI[4]", "Lbl"],
            "custom_attributes": None,
        },
        {
            "text": [
                "We have consulted on improving compulsory basic training for motorcyclists and allowing learner drivers on motorways. "
            ],
            "text_block_id": "p34_b8",
            "coords": [
                [88.80000305175781, 140.56797790527344],
                [518.3038787841797, 140.56797790527344],
                [88.80000305175781, 170.33998107910156],
                [518.3038787841797, 170.33998107910156],
            ],
            "type": "LBody",
            "path": ["Document", "L[47]", "LI", "LBody", "L", "LI[4]", "LBody"],
            "custom_attributes": None,
        },
        {
            "text": ["• "],
            "text_block_id": "p34_b9",
            "coords": [
                [70.91999816894531, 175.0199737548828],
                [79.44000244140625, 175.0199737548828],
                [70.91999816894531, 189.719970703125],
                [79.44000244140625, 189.719970703125],
            ],
            "type": "Lbl",
            "path": ["Document", "L[47]", "LI", "LBody", "L", "LI[5]", "Lbl"],
            "custom_attributes": None,
        },
        {
            "text": [
                "We have continued to push forward on drug driving, which has led to around 10,000 arrests. "
            ],
            "text_block_id": "p34_b10",
            "coords": [
                [88.80000305175781, 175.0079803466797],
                [497.3039093017578, 175.0079803466797],
                [88.80000305175781, 204.7799835205078],
                [497.3039093017578, 204.7799835205078],
            ],
            "type": "LBody",
            "path": ["Document", "L[47]", "LI", "LBody", "L", "LI[5]", "LBody"],
            "custom_attributes": None,
        },
        {
            "text": ["• "],
            "text_block_id": "p34_b11",
            "coords": [
                [70.91999816894531, 209.45997619628906],
                [79.44000244140625, 209.45997619628906],
                [70.91999816894531, 224.15997314453125],
                [79.44000244140625, 224.15997314453125],
            ],
            "type": "Lbl",
            "path": ["Document", "L[47]", "LI", "LBody", "L", "LI[6]", "Lbl"],
            "custom_attributes": None,
        },
        {
            "text": [
                "The Driving and Vehicle Standards Agency has trialled a new practical car driving test, to improve new driver safety. "
            ],
            "text_block_id": "p34_b12",
            "coords": [
                [88.80000305175781, 209.44798278808594],
                [524.0879211425781, 209.44798278808594],
                [88.80000305175781, 239.219970703125],
                [524.0879211425781, 239.219970703125],
            ],
            "type": "LBody",
            "path": ["Document", "L[47]", "LI", "LBody", "L", "LI[6]", "LBody"],
            "custom_attributes": None,
        },
        {
            "text": ["• "],
            "text_block_id": "p34_b8",
            "coords": [
                [78.0, 522.4199829101562],
                [86.52000427246094, 522.4199829101562],
                [78.0, 537.1199798583984],
                [86.52000427246094, 537.1199798583984],
            ],
            "type": "Lbl",
            "path": ["Document", "L[48]", "LI[3]", "LBody", "L", "LI", "Lbl"],
            "custom_attributes": None,
        },
        {
            "text": [
                "Work is continuing to refine the approach to appraising, monitoring and evaluating cycling investment opportunities, to ensure that good quality schemes are delivered. In turn this will help inform a review of Highways England’s cycling performance indicators, to ensure they are meaningful and easily understood. The new approach will be tested in 2017-18 to ensure it is fit for purpose. "
            ],
            "text_block_id": "p34_b9",
            "coords": [
                [92.27999877929688, 522.4079742431641],
                [523.1759185791016, 522.4079742431641],
                [92.27999877929688, 593.5799713134766],
                [523.1759185791016, 593.5799713134766],
            ],
            "type": "LBody",
            "path": ["Document", "L[48]", "LI[3]", "LBody", "L", "LI", "LBody"],
            "custom_attributes": None,
        },
        {
            "text": ["• "],
            "text_block_id": "p34_b10",
            "coords": [
                [78.0, 598.2599792480469],
                [86.52000427246094, 598.2599792480469],
                [78.0, 612.9599761962891],
                [86.52000427246094, 612.9599761962891],
            ],
            "type": "Lbl",
            "path": ["Document", "L[48]", "LI[3]", "LBody", "L", "LI[2]", "Lbl"],
            "custom_attributes": None,
        },
        {
            "text": [
                "Highways England continues to work closely with a range of stakeholders representing the views of vulnerable users, including cyclists. This includes national engagement on development of their overall approach, as well as local engagement regarding specific scheme opportunities and issues. "
            ],
            "text_block_id": "p34_b11",
            "coords": [
                [92.27999877929688, 598.2479705810547],
                [515.8799133300781, 598.2479705810547],
                [92.27999877929688, 655.4999847412109],
                [515.8799133300781, 655.4999847412109],
            ],
            "type": "LBody",
            "path": ["Document", "L[48]", "LI[3]", "LBody", "L", "LI[2]", "LBody"],
            "custom_attributes": None,
        },
        {
            "text": ["• "],
            "text_block_id": "p34_b12",
            "coords": [
                [70.91999816894531, 660.1799774169922],
                [79.44000244140625, 660.1799774169922],
                [70.91999816894531, 674.8799743652344],
                [79.44000244140625, 674.8799743652344],
            ],
            "type": "Lbl",
            "path": ["Document", "L[48]", "LI[3]", "LBody", "L", "LI[3]", "Lbl"],
            "custom_attributes": None,
        },
        {
            "text": [
                "Highways England recognises the need for cycling investment to positively contribute to local cycle networks. To support this they have been testing network planning approaches with specific local highways authorities to ensure that Highway England’s investment supports the ambitions of local authorities, as set out in their Local Cycling and Walking Infrastructure Plans (LCWIPs), as well as Government. Once fully developed they will implement this approach more widely. "
            ],
            "text_block_id": "p34_b13",
            "coords": [
                [70.91999816894531, 660.1679840087891],
                [523.4159545898438, 660.1679840087891],
                [70.91999816894531, 758.9399719238281],
                [523.4159545898438, 758.9399719238281],
            ],
            "type": "LI",
            "path": ["Document", "L[48]", "LI[3]", "LBody", "L", "LI[3]"],
            "custom_attributes": None,
        },
    ]
    expected = {
        "coords": [
            [70.91999816894531, 71.8079833984375],
            [524.0879211425781, 71.8079833984375],
            [70.91999816894531, 758.9399719238281],
            [524.0879211425781, 758.9399719238281],
        ],
        "path": ["Document", "L[47]", "LI", "LBody", "L", "LI[2]", "Lbl"],
        "text_block_id": "p34_b1",
        "type": "list",
        "text": [
            "\n<li1>\n<Lbl>•<\\Lbl><LBody>Legislation has been presented to Parliament to increase penalties for drivers using a handheld mobile. This came into effect on 1st March 2017, alongside a major Think! Campaign.<\\LBody>\n",
            "<Lbl>•<\\Lbl><LBody>A major piece of research on young driver safety has been commissioned.<\\LBody>\n",
            "<Lbl>•<\\Lbl><LBody>We have consulted on improving compulsory basic training for motorcyclists and allowing learner drivers on motorways.<\\LBody>\n",
            "<Lbl>•<\\Lbl><LBody>We have continued to push forward on drug driving, which has led to around 10,000 arrests.<\\LBody>\n",
            "<Lbl>•<\\Lbl><LBody>The Driving and Vehicle Standards Agency has trialled a new practical car driving test, to improve new driver safety.<\\LBody>\n",
            "<Lbl>•<\\Lbl><LBody>Work is continuing to refine the approach to appraising, monitoring and evaluating cycling investment opportunities, to ensure that good quality schemes are delivered. In turn this will help inform a review of Highways England’s cycling performance indicators, to ensure they are meaningful and easily understood. The new approach will be tested in 2017-18 to ensure it is fit for purpose.<\\LBody>\n",
            "<Lbl>•<\\Lbl><LBody>Highways England continues to work closely with a range of stakeholders representing the views of vulnerable users, including cyclists. This includes national engagement on development of their overall approach, as well as local engagement regarding specific scheme opportunities and issues.<\\LBody>\n",
            "<Lbl>•<\\Lbl><LBody>Highways England recognises the need for cycling investment to positively contribute to local cycle networks. To support this they have been testing network planning approaches with specific local highways authorities to ensure that Highway England’s investment supports the ambitions of local authorities, as set out in their Local Cycling and Walking Infrastructure Plans (LCWIPs), as well as Government. Once fully developed they will implement this approach more widely.<\\LBody>\n\n<\\li1>\n",
        ],
        "custom_attributes": {
            "styleSpans": [{"style": "superscript", "start_idx": 130, "end_idx": 131}],
            "paths": [
                ["Document", "L[47]", "LI", "LBody", "L", "LI[2]", "Lbl"],
                ["Document", "L[47]", "LI", "LBody", "L", "LI[2]", "LBody"],
                ["Document", "L[47]", "LI", "LBody", "L", "LI[3]", "Lbl"],
                ["Document", "L[47]", "LI", "LBody", "L", "LI[3]", "LBody"],
                ["Document", "L[47]", "LI", "LBody", "L", "LI[4]", "Lbl"],
                ["Document", "L[47]", "LI", "LBody", "L", "LI[4]", "LBody"],
                ["Document", "L[47]", "LI", "LBody", "L", "LI[5]", "Lbl"],
                ["Document", "L[47]", "LI", "LBody", "L", "LI[5]", "LBody"],
                ["Document", "L[47]", "LI", "LBody", "L", "LI[6]", "Lbl"],
                ["Document", "L[47]", "LI", "LBody", "L", "LI[6]", "LBody"],
                ["Document", "L[48]", "LI[3]", "LBody", "L", "LI", "Lbl"],
                ["Document", "L[48]", "LI[3]", "LBody", "L", "LI", "LBody"],
                ["Document", "L[48]", "LI[3]", "LBody", "L", "LI[2]", "Lbl"],
                ["Document", "L[48]", "LI[3]", "LBody", "L", "LI[2]", "LBody"],
                ["Document", "L[48]", "LI[3]", "LBody", "L", "LI[3]", "Lbl"],
                ["Document", "L[48]", "LI[3]", "LBody", "L", "LI[3]"],
            ],
            "text_block_ids": [
                "p34_b1",
                "p34_b2_merged",
                "p34_b5",
                "p34_b6",
                "p34_b7",
                "p34_b8",
                "p34_b9",
                "p34_b10",
                "p34_b11",
                "p34_b12",
                "p34_b8",
                "p34_b9",
                "p34_b10",
                "p34_b11",
                "p34_b12",
                "p34_b13",
            ],
            "pretty_list_string": "* Legislation has been presented to Parliament to increase penalties for drivers using a handheld mobile. This came into effect on 1st March 2017, alongside a major Think! Campaign.\n* A major piece of research on young driver safety has been commissioned.\n* We have consulted on improving compulsory basic training for motorcyclists and allowing learner drivers on motorways.\n* We have continued to push forward on drug driving, which has led to around 10,000 arrests.\n* The Driving and Vehicle Standards Agency has trialled a new practical car driving test, to improve new driver safety.\n* Work is continuing to refine the approach to appraising, monitoring and evaluating cycling investment opportunities, to ensure that good quality schemes are delivered. In turn this will help inform a review of Highways England’s cycling performance indicators, to ensure they are meaningful and easily understood. The new approach will be tested in 2017-18 to ensure it is fit for purpose.\n* Highways England continues to work closely with a range of stakeholders representing the views of vulnerable users, including cyclists. This includes national engagement on development of their overall approach, as well as local engagement regarding specific scheme opportunities and issues.\n* Highways England recognises the need for cycling investment to positively contribute to local cycle networks. To support this they have been testing network planning approaches with specific local highways authorities to ensure that Highway England’s investment supports the ambitions of local authorities, as set out in their Local Cycling and Walking Infrastructure Plans (LCWIPs), as well as Government. Once fully developed they will implement this approach more widely.\n",
            "original_list_text": [
                ["• "],
                [
                    "Legislation has been presented to Parliament to increase penalties for drivers using a handheld mobile. This came into effect on 1st March 2017, alongside a major Think! Campaign. "
                ],
                ["• "],
                [
                    "A major piece of research on young driver safety has been commissioned. "
                ],
                ["• "],
                [
                    "We have consulted on improving compulsory basic training for motorcyclists and allowing learner drivers on motorways. "
                ],
                ["• "],
                [
                    "We have continued to push forward on drug driving, which has led to around 10,000 arrests. "
                ],
                ["• "],
                [
                    "The Driving and Vehicle Standards Agency has trialled a new practical car driving test, to improve new driver safety. "
                ],
                ["• "],
                [
                    "Work is continuing to refine the approach to appraising, monitoring and evaluating cycling investment opportunities, to ensure that good quality schemes are delivered. In turn this will help inform a review of Highways England’s cycling performance indicators, to ensure they are meaningful and easily understood. The new approach will be tested in 2017-18 to ensure it is fit for purpose. "
                ],
                ["• "],
                [
                    "Highways England continues to work closely with a range of stakeholders representing the views of vulnerable users, including cyclists. This includes national engagement on development of their overall approach, as well as local engagement regarding specific scheme opportunities and issues. "
                ],
                ["• "],
                [
                    "Highways England recognises the need for cycling investment to positively contribute to local cycle networks. To support this they have been testing network planning approaches with specific local highways authorities to ensure that Highway England’s investment supports the ambitions of local authorities, as set out in their Local Cycling and Walking Infrastructure Plans (LCWIPs), as well as Government. Once fully developed they will implement this approach more widely. "
                ],
            ],
        },
    }
    actual = adobe_list_postprocessor._update_custom_attributes(input_blocks)
    assert actual == expected


# Integration test.
def test_postprocessor_integration(
    test_input_path,
    adobe_text_styling_postprocessor,
    adobe_hyphenation_postprocessor,
    adobe_list_postprocessor,
):
    in_doc = Document.from_json(test_input_path)
    # run postprocessors
    hyphenation_doc = adobe_hyphenation_postprocessor.process(in_doc)
    text_styling_doc = adobe_text_styling_postprocessor.process(hyphenation_doc)
    out_doc = adobe_list_postprocessor.process(
        text_styling_doc, f"{test_input_path.stem}.pdf"
    )
    # Basic tests to ensure that nothing has gone wrong.

    # Check that 6 pages have been returned in the document
    assert len(out_doc.pages) == 6

    # Ideally, a lot of these assertions would ocme in the code itself to ensure
    # we can't run it if assumptions aren't valid, but leaving for now.
    for page in out_doc.pages:
        for block in page.text_blocks:
            assert len(block.coords) == 4
            assert len(block.coords[0]) == 2
            assert block.path
            assert block.type
            if block.type == "list":
                assert len(block.custom_attributes["paths"]) > 1
                assert len(block.custom_attributes["pretty_list_string"]) > 0
