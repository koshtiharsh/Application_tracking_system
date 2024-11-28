import requests
import fitz  # PyMuPDF
import re

corrections =[]

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text")
    doc.close()
    return text

def is_exact_match(span_text, incorrect_text):
    pattern = r'\b' + re.escape(incorrect_text) + r'\b'
    matches = list(re.finditer(pattern, span_text))
    return matches

def is_all_caps(text):
    # Check if the text is all uppercase and at least 2 characters long
    return text.isupper() and len(text) >= 2 and text.isalpha()

def apply_corrections_to_pdf(pdf_path, matches, output_path):
    doc = fitz.open(pdf_path)
    
    filtered_matches = []
    for match in matches:
        incorrect_text = match['context']['text'][match['context']['offset']:
                                                match['context']['offset'] + match['context']['length']]

        filtered_matches.append(match)
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        spans = page.get_text("dict")["blocks"]
        
        for match in filtered_matches:
            incorrect_text = match['context']['text'][match['context']['offset']:
                                                    match['context']['offset'] + match['context']['length']]
            correct_text = match['replacements'][0]['value'] if match['replacements'] else incorrect_text

            for block in spans:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            exact_matches = is_exact_match(span["text"], incorrect_text)
                            
                            for exact_match in exact_matches:
                                matched_text = span["text"][exact_match.start():exact_match.end()]
                                print(f"Matched text: {matched_text}")
                                if is_all_caps(matched_text):
                                    continue
                                
                                start_pos = exact_match.start()
                                end_pos = exact_match.end()
                                
                                span_width = span["bbox"][2] - span["bbox"][0]
                                char_width = span_width / len(span["text"])
                                
                                x0 = span["bbox"][0] + (start_pos * char_width)
                                x1 = span["bbox"][0] + (end_pos * char_width)
                                y0 = span["bbox"][1]
                                y1 = span["bbox"][3]
                                
                                word_rect = fitz.Rect(x0, y0, x1, y1)
                                
                                padding = (y1 - y0) * 0.05
                                cover_rect = word_rect + (-padding, -padding, padding, padding)
                                page.draw_rect(cover_rect, color=(1, 1, 1), fill=(1, 1, 1))
                                
                                highlight = page.add_highlight_annot(word_rect)
                                highlight.set_colors(stroke=(0, 0.8, 0))
                                highlight.update()
                                
                                try:
                                    page.insert_text(
                                        point=(x0, y1 - ((y1 - y0) * 0.2)),
                                        text=correct_text,
                                        fontsize=span["size"],
                                        fontname=span["font"]
                                    )
                                except:
                                    page.insert_text(
                                        point=(x0, y1 - ((y1 - y0) * 0.2)),
                                        text=correct_text,
                                        fontsize=span["size"],
                                        fontname="helv"
                                    )
    
    
    # Save the modified PDF
    doc.save(output_path)
    doc.close()

def check_and_correct_pdf(pdf_path, output_path):
    # Extract text from PDF
    text = extract_text_from_pdf(pdf_path)
    
    # LanguageTool API endpoint
    url = "https://api.languagetool.org/v2/check"
    
    # Request parameters
    params = {
        'text': text,
        'language': 'en-US',
        'enabledRules': 'MORFOLOGIK_RULE_EN_US',
        'disabledRules': 'UPPERCASE_SENTENCE_START,CASE_RULE'
    }
    
    try:
        # Send request to LanguageTool API
        response = requests.post(url, data=params)
        response.raise_for_status()
        
        # Process corrections
        result = response.json()
        if result['matches']:
            apply_corrections_to_pdf(pdf_path, result['matches'], output_path)
            print(f"Corrections applied successfully. Output saved to: {output_path}")
            print(f"Number of corrections made: {len(result['matches'])}")
            
            # Print corrections for verification
            print("\nCorrections made:")
            for match in result['matches']:
                incorrect = match['context']['text'][match['context']['offset']:
                                                   match['context']['offset'] + match['context']['length']]
                correct = match['replacements'][0]['value'] if match['replacements'] else incorrect
                # Only print if not all caps
                if not is_all_caps(incorrect):
                    corrections.append(f'{incorrect} to {correct}')
                    # print(f"Changed '{incorrect}' to '{correct}'")
        else:
            print("No corrections needed.")
         
    except requests.exceptions.RequestException as e:
        print(f"Error accessing LanguageTool API: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return corrections 

# # Usage
# if __name__ == "__main__":
#     input_pdf = "r.pdf"
#     output_pdf = "corrected_resume.pdf"
#     check_and_correct_pdf(input_pdf, output_pdf)