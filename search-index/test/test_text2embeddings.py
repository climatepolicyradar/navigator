import pytest
import text2embeddings


def test_get_text_from_merged_block():
    # Case 1: Single superscript. c.f cclw-10007. Superscript has been removed.
    input_1 = {
        "text": [
            "The central indicator for measuring the depletion of natural resources at the macroeconomic level is the environmentally adjusted GDP: GDP \u2013 GDPE . It is the adjustment of GDP by the depletion (depreciation) of natural capital, which is the consumption of environmental products. Consumption of environmental products means quantitative reduction of minerals, bio-resources and the observed reduction in ecosystem services.  "
        ],
        "text_block_id": "p6_b91_merged",
        "coords": [
            [85.08000183105469, 207.0596923828125],
            [555.9367065429688, 207.0596923828125],
            [85.08000183105469, 278.4237060546875],
            [555.9367065429688, 278.4237060546875],
        ],
        "type": "merged_text_block",
        "path": ["Document", "P[40]"],
        "custom_attributes": {
            "styleSpans": [{"style": "superscript", "start_idx": 144, "end_idx": 144}]
        },
    }

    expected_1 = (
        "The central indicator for measuring the depletion of natural resources at the macroeconomic level is the environmentally adjusted GDP: GDP – GDP . It is the adjustment of GDP by the depletion (depreciation) of natural capital, which is the consumption of environmental products. Consumption of environmental products means quantitative reduction of minerals, bio-resources and the observed reduction in ecosystem services.",
        "p6_b91_merged",
    )

    result_1 = text2embeddings.get_text_from_merged_block(input_1)
    assert result_1 == expected_1

    # Case 2: Double digit superscripts (made up input for illustrative purposes).
    input_2 = {
        "text": [
            "It is this government's priority to reduce carbon emissions by 2030.12 "
        ],
        "text_block_id": "p6_b3_merged",
        "type": "merged_text_block",
        "custom_attributes": {
            "styleSpans": [{"style": "superscript", "start_idx": 68, "end_idx": 69}]
        },
    }

    expected_2 = (
        "It is this government's priority to reduce carbon emissions by 2030.",
        "p6_b3_merged",
    )

    result_2 = text2embeddings.get_text_from_merged_block(input_2)
    assert result_2 == expected_2

    # Case 3: Do not remove subscripts! (e.g. CO2). Made up input for readability and illustrative purposes.
    # We can see that the 2 in co2 is a subscript.
    input_3 = {
        "text": ["CO2 has risen by 0.5% since the last year. "],
        "text_block_id": "p6_b3_merged",
        "type": "merged_text_block",
        "custom_attributes": {
            "styleSpans": [{"style": "subscript", "start_idx": 2, "end_idx": 2}]
        },
    }

    expected_3 = ("CO2 has risen by 0.5% since the last year.", "p6_b3_merged")

    result_3 = text2embeddings.get_text_from_merged_block(input_3)
    assert result_3 == expected_3

    # Case 4: Do not remove superscripts if they match regex such as 1st, 2nd, 3rd, 4th, 5th, 6th, 7th, 8th, 9th, 10th.
    # In this case, there is semantics in the superscript that LLMs may be able to understand.
    input_4 = {
        "text": ["On the 1st April. "],
        "text_block_id": "p6_b3_merged",
        "type": "merged_text_block",
        "custom_attributes": {
            "styleSpans": [{"style": "superscript", "start_idx": 8, "end_idx": 9}]
        },
    }

    expected_4 = ("On the 1st April.", "p6_b3_merged")

    result_4 = text2embeddings.get_text_from_merged_block(input_4)
    assert result_4 == expected_4
