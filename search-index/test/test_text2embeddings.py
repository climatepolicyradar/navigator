import text2embeddings


def test_get_text_from_merged_block():
    # Case 1: Single superscript. c.f cclw-10007. Superscript has been removed.
    input_1 = {
        "text": [
            "The central indicator for measuring the depletion of natural resources at the macroeconomic level is the environmentally adjusted GDP: GDP – GDPE . It is the adjustment of GDP by the depletion (depreciation) of natural capital, which is the consumption of environmental products. Consumption of environmental products means quantitative reduction of minerals, bio-resources and the observed reduction in ecosystem services.  "
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

    expected_1 = "The central indicator for measuring the depletion of natural resources at the macroeconomic level is the environmentally adjusted GDP: GDP – GDP . It is the adjustment of GDP by the depletion (depreciation) of natural capital, which is the consumption of environmental products. Consumption of environmental products means quantitative reduction of minerals, bio-resources and the observed reduction in ecosystem services."

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

    expected_2 = "It is this government's priority to reduce carbon emissions by 2030."

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

    expected_3 = "CO2 has risen by 0.5% since the last year."

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

    expected_4 = "On the 1st April."

    result_4 = text2embeddings.get_text_from_merged_block(input_4)
    assert result_4 == expected_4


def test_get_text_from_list():
    # Case 1: A nice complex nested list example with context.
    previous_context_block = (
        "The P.P.U.C.-\n* shall develop a standard contract providing for net energy metering, "
        "and shall, upon request, make this contract available to eligible "
        "customer-generators;\n* shall prepare appropriate technical standards for grid "
        "connection of renewable energy systems, and inspect and provide a license for those "
        "renewable energy installations that meet the technical standards developed by P.P.U.C. "
        "and the other provisions of this legislation. Issuance of a license shall be solely to "
        "show that the P.P.U.C. has approved the interconnection of the customer=s renewable "
        "energy system and the P.P.U.C. grid and shall not be interpreted to impose liability or "
        "approval by the P.P.U.C. for any part of the renewable energy system, its design, "
        "or its method of implementation. The technical standards imposed will be based solely "
        "on those necessary to ensure the safety of P.P.U.C. personnel and for the maintenance "
        "of P.P.U.C, power quality. Standards and technical requirements shall be consistent "
        "with existing technical practices for similar types of installations in the United "
        "States, Australia, or the European Union.\n\t* A licensee shall inform the P.P.U.C. of "
        "any proposed technical changes to the renewable energy system that affects either the "
        "maximum power output or the components that provide the interconnection between the "
        "renewable energy system and the P.P.U.C. grid and will, under the licensing agreement, "
        "not make those changes without P.P.U.C. approval.\n\t* The failure of a licensee to "
        "promptly inform the P.P.U.C. in writing of any technical changes to the renewable "
        "energy system that affects any of the above may, at the P.P.U.C. discretion, "
        "result in a fine of not more than two hundred dollars ($200).\n\t* shall, "
        "at its own-expense, make available to each of its eligible customer generators who have "
        "installed a net metering system the meter (or set of meters) that is needed to "
        "determine the net flow of electricity both into and out of the electricity grid;"
    )

    input_text_block = {
        "text": [
            "\n<li1>\n<Lbl>(d)<\\Lbl><LBody>shall, at its own expense, annually inspect grid-connected renewable energy installations to ensure that unauthorized changes have not been made and to ensure that the grid interconnection arrangements remain adequate for maintaining safety and power quality.<\\LBody>\\n",
            "<Lbl>(e)<\\Lbl><LBody>shall not charge the customer any additional standby, capacity, interconnection, or other fee or charge that is greater than such fees charged to all members of that customer class; and<\\LBody>\\n",
            "<Lbl>(f)<\\Lbl><LBody>may, at its own expense, and with the written consent of the customer, install one or more additional meters to monitor the flow of electricity in each direction. The additional metering shall be used only to provide the information necessary to accurately bill or credit the customer-generator or to collect renewable energy generating system performance information for research purposes.<\\LBody>\\n\\n<\\li1>\\n",
        ],
        "text_block_id": "p4_b96",
        "coords": [
            [44.00691223144531, 27.4151611328125],
            [549.7152709960938, 27.4151611328125],
            [44.00691223144531, 226.27561950683594],
            [549.7152709960938, 226.27561950683594],
        ],
        "type": "list",
        "path": ["Document", "L[4]", "LI[4]", "Lbl"],
        "custom_attributes": {
            "possibly_contiguous_with_same_page_context": True,
            "paths": [
                ["Document", "L[4]", "LI[4]", "Lbl"],
                ["Document", "L[4]", "LI[4]", "LBody"],
                ["Document", "L[4]", "LI[5]", "Lbl"],
                ["Document", "L[4]", "LI[5]", "LBody"],
                ["Document", "L[4]", "LI[6]", "Lbl"],
                ["Document", "L[4]", "LI[6]", "LBody"],
            ],
            "text_block_ids": [
                "p4_b96",
                "p4_b97",
                "p4_b98",
                "p4_b99",
                "p4_b100",
                "p4_b101",
            ],
            "pretty_list_string": "* shall, at its own expense, annually inspect grid-connected renewable energy installations to ensure that unauthorized changes have not been made and to ensure that the grid interconnection arrangements remain adequate for maintaining safety and power quality.\\n\n* shall not charge the customer any additional standby, capacity, interconnection, or other fee or charge that is greater than such fees charged to all members of that customer class; and\\n\n* may, at its own expense, and with the written consent of the customer, install one or more additional meters to monitor the flow of electricity in each direction. The additional metering shall be used only to provide the information necessary to accurately bill or credit the customer-generator or to collect renewable energy generating system performance information for research purposes.\\n\\n\\n\n",
            "original_list_text": [
                ["(d)"],
                [
                    " shall, at its own expense, annually inspect grid-connected renewable energy installations to ensure that unauthorized changes have not been made and to ensure that the grid interconnection arrangements remain adequate for maintaining safety and power quality. "
                ],
                ["(e)"],
                [
                    " shall not charge the customer any additional standby, capacity, interconnection, or other fee or charge that is greater than such fees charged to all members of that customer class; and "
                ],
                ["(f)"],
                [
                    " may, at its own expense, and with the written consent of the customer, install one or more additional meters to monitor the flow of electricity in each direction. The additional metering shall be used only to provide the information necessary to accurately bill or credit the customer-generator or to collect renewable energy generating system performance information for research purposes. "
                ],
            ],
            "num_nesting_levels": 1,
        },
    }
    actual = text2embeddings.get_text_from_list(
        input_text_block, previous_context_block
    )

    expected = (
        "The P.P.U.C.-\n* shall develop a standard contract providing for net energy metering, and shall, "
        "upon request, make this contract available to eligible customer-generators;\n* shall prepare "
        "appropriate technical standards for grid connection of renewable energy systems, and inspect and "
        "provide a license for those renewable energy installations that meet the technical standards "
        "developed by P.P.U.C. and the other provisions of this legislation. Issuance of a license shall be "
        "solely to show that the P.P.U.C. has approved the interconnection of the customer=s renewable energy "
        "system and the P.P.U.C. grid and shall not be interpreted to impose liability or approval by the "
        "P.P.U.C. for any part of the renewable energy system, its design, or its method of implementation. "
        "The technical standards imposed will be based solely on those necessary to ensure the safety of "
        "P.P.U.C. personnel and for the maintenance of P.P.U.C, power quality. Standards and technical "
        "requirements shall be consistent with existing technical practices for similar types of installations "
        "in the United States, Australia, or the European Union.\n\t* A licensee shall inform the P.P.U.C. of "
        "any proposed technical changes to the renewable energy system that affects either the maximum power "
        "output or the components that provide the interconnection between the renewable energy system and the "
        "P.P.U.C. grid and will, under the licensing agreement, not make those changes without P.P.U.C. "
        "approval.\n\t* The failure of a licensee to promptly inform the P.P.U.C. in writing of any technical "
        "changes to the renewable energy system that affects any of the above may, at the P.P.U.C. discretion, "
        "result in a fine of not more than two hundred dollars ($200).\n\t* shall, at its own-expense, "
        "make available to each of its eligible customer generators who have installed a net metering system "
        "the meter (or set of meters) that is needed to determine the net flow of electricity both into and "
        "out of the electricity grid;\n* shall, at its own expense, annually inspect grid-connected renewable "
        "energy installations to ensure that unauthorized changes have not been made and to ensure that the "
        "grid interconnection arrangements remain adequate for maintaining safety and power quality.\n* shall "
        "not charge the customer any additional standby, capacity, interconnection, or other fee or charge "
        "that is greater than such fees charged to all members of that customer class; and\n* may, at its own "
        "expense, and with the written consent of the customer, install one or more additional meters to "
        "monitor the flow of electricity in each direction. The additional metering shall be used only to "
        "provide the information necessary to accurately bill or credit the customer-generator or to collect "
        "renewable energy generating system performance information for research purposes."
    )

    assert actual == expected
