import re

def step_f_replacer(input_text):
    step_f_lines = [
        (r"BY SENDING AN INSTRUCTION, YOU AUTHORISE US TO DISCLOSE YOUR NAME AND ACCOUNT\r?\n", ""),
        
        (r"ELECTRONIC INSTRUCTIONS:\r?\n", ""),
        
        (r"1. FREE FORMAT MT 599/MT 568 USERS: YOUR DEADLINE IS 10:00 (BRUSSELS TIME) ON THE BUSINESS DAY BEFORE THE DEADLINE DATE.\r?\n", ""),
        
        (r"2. EASYWAY USERS:\r?\n", ""),
    
        (r"A. TO ACCEDE TO THE RESTRUCTURING SUPPORT AGREEMENT, BLOCK THE POSITION, SUBMIT PAPER WORK ON THE TRANSACTION WEBSITE AND RECEIVE EARLY CONSENT FEE, CHOOSE OPTION 001\r?\n", ""),
        
        (r"B. TO ACCEDE TO THE RESTRUCTURING SUPPORT AGREEMENT, BLOCK THE POSITION, SUBMIT PAPER WORK ON THE TRANSACTION WEBSITE AND RECEIVE EARLY CONSENT FEE CHOOSE OPTION 002\r?\n", ""),
        
        (r"ALWAYS SELECT 'BENEFICIARY AND DELIVERY DETAILS' AND MENTION IN FIELD 'BENEFICIARY' THE BO'S NAME PRECEDED BY 'NAME', PHONE NUMBER AND EMAIL ADDRESS PRECEDED BY 'ADDRESS' NOTE: IF YOU DO NOT MAKE THIS DISTINCTION, YOUR INSTRUCTION MAY BE REJECTED\r?\n", ""),
        
        (r"MENTION IN FIELD 'NARRATIVE TO SERVICE PROVIDER': YOUR CONTACT NAME AND PHONE NUMBER PRECEDED BY 'INX CONTACT DETAILS'\r?\n", ""),
        
        (r"3. EUCLID USERS:\r?\n", ""),
    
        (r"A. TO ACCEDE TO THE RESTRUCTURING SUPPORT AGREEMENT, BLOCK THE POSITION, SUBMIT PAPER WORK ON THE TRANSACTION WEBSITE AND RECEIVE EARLY CONSENT FEE, SEND AN INSTRUCTION TYPE '54' WITH SUBTYPE 'COY1'\r?\n", ""),

        (r"B. TO ACCEDE TO THE RESTRUCTURING SUPPORT AGREEMENT, BLOCK THE POSITION, SUBMIT PAPER WORK ON THE TRANSACTION WEBSITE AND RECEIVE EARLY CONSENT FEE SEND AN INSTRUCTION TYPE '54' WITH SUBTYPE 'COY2'\r?\n", ""),
        
        (r"C. TO TAKE NO ACTION, SEND AN INSTRUCTION TYPE '54' SUBTYPE 'NOAC'. MENTION THE EVENT NUMBER IN FIELD 72 AS FOLLOWS: 'EVNB CA00000XXXXXXX' \(WHERE XXXXXXX IS THE EVENT NUMBER\)\r?\n", ""),
        
        (r"ALWAYS MENTION IN FIELD:\r?\n", ""),
        
        (r"88D: THE BO'S NAME PRECEDED BY 'NAME', PHONE NUMBER AND EMAIL ADDRESS PRECEDED BY 'ADDRESS'\r?\n", ""),
        
        (r"NOTE: IF YOU DO NOT MAKE THIS DISTINCTION, YOUR INSTRUCTION MAY BE REJECTED\r?\n", ""),
        
        (r"4. SWIFT MT565 USERS:\r?\n", ""),
        
        (r"A. TO ACCEDE TO THE RESTRUCTURING SUPPORT AGREEMENT, BLOCK THE POSITION, SUBMIT PAPER WORK ON THE TRANSACTION WEBSITE AND RECEIVE EARLY CONSENT FEE, USE CAON 001 CAOP CONY\r?\n", ""),
        
        (r"B. TO ACCEDE TO THE RESTRUCTURING SUPPORT AGREEMENT, BLOCK THE POSITION, SUBMIT PAPER WORK ON THE TRANSACTION WEBSITE AND RECEIVE EARLY CONSENT FEE USE CAON 002 CAOP CONY\r?\n", ""),
        
        (r"ALWAYS MENTION IN FIELD:\r?\n", ""),
        
        (r"95V:OWND: THE BO'S NAME PRECEDED BY 'NAME', PHONE NUMBER AND EMAIL ADDRESS PRECEDED BY 'ADDRESS'\r?\n", ""),
        
        (r"NOTE: IF YOU DO NOT MAKE THIS DISTINCTION, YOUR INSTRUCTION MAY BE REJECTED\r?\n", ""),
        
        (r"70E:INST: YOUR CONTACT NAME AND PHONE NUMBER PRECEDED BY 'INX CONTACT DETAILS\n", ""),
    ]

    first_match_pos = None
    last_match_pos = None

    for pattern, _ in step_f_lines:
        match = re.search(pattern, input_text)
        if match:
            print(pattern)

            if first_match_pos is None:
                first_match_pos = match.start()
            last_match_pos = match.end()

    # Remove the text between the first and last matches
    if first_match_pos is not None and last_match_pos is not None:
        input_text = input_text[:first_match_pos] + input_text[last_match_pos:]

    print("Removed:")
    print(input_text[first_match_pos:last_match_pos],"\n\n")

    return input_text


    


def reformat_swift_text(input_text):
    transformations = [
        # Replace "--------------- EVENT DETAILS -------------------"
        (r"((-|—)+)( *)EVENT DETAILS( *)((-|—)+)", "+++ EVENT DETAILS +++"),

        # Replace ".-------------------"
        (r"\.((-|—)+)", "."),

        # Delete all ":70E::ADTX//" fields
        (r":\d{2}\w::\w{4}\/\/", ""),

        # Delete "INFORMATION SOURCE: AGENT, [REDACTED], LONDON"
        (r"INFORMATION SOURCE: AGENT, \[REDACTED\], LONDON\r?\n", ""),

        # Replace "--------------- ACTION TO BE TAKEN -------------------"
        (r"((-|—)+)( *)ACTION TO BE TAKEN( *)((-|—)+)", """+++ INSTRUCTION REQUIREMENTS +++\n.\nMINIMUM TO EXERCISE:\nMULTIPLE TO EXERCISE:\n.\nANY RESPONSE RECEIVED THAT IS NOT IN THE CORRECT MULTIPLE, AS STIPULATED UNDER THE FULL EVENT TERMS, WILL BE ROUNDED DOWN AND APPLIED TO THE NEAREST WHOLE MULTIPLE. THE DIFFERENCE BETWEEN THE QUANTITY INSTRUCTED VERSUS THE AMOUNT APPLIED WILL REMAIN UNINSTRUCTED."""),

        # Delete fields starting with specific text

    

        
    ]

    input_text = step_f_replacer(input_text)

    for pattern, replacement in transformations:
        new_text = re.sub(pattern, replacement, input_text, flags=re.DOTALL)
        if new_text != input_text:
            matches = re.findall(pattern, input_text, flags=re.DOTALL)
            for match in matches:
                print(f"Replaced: \n {match}\n\n with  \n\n{replacement} ")
                print("---------------------")
            input_text = new_text

    return input_text


# Example usage
if __name__ == "__main__":
    with open("input_text.txt", "r") as input_file:
        input_text = input_file.read()
    
    reformatted_text = reformat_swift_text(input_text)
    
    with open("output_text.txt", "w") as output_file:
        output_file.write(reformatted_text)