import fitz
import re
import transformers
from parser import column_boxes

tokenizer = transformers.AutoTokenizer.from_pretrained(
    "/data/saikat/RegBank_Policy_POC/misc/mixtral-tokenizer/"
)

def create_store(filepath):
    
    doc = fitz.open(filepath)

    page_num = 1
    text_list = []

    for page in doc:
        bboxes = column_boxes(page, footer_margin=50, no_image_text=True)

        block_num = 1
        for rect in bboxes:
            block_text = page.get_text(clip=rect, sort=True)

            paragraph_text = block_text
            paragraph_text = paragraph_text.replace("\n", " ")
            paragraph_text = re.sub(r"\-\n", "", paragraph_text)
            paragraph_text = re.sub(r"\'", "", paragraph_text)
            paragraph_text = paragraph_text.replace("\\n", " ")
            paragraph_text = paragraph_text.replace("\\xa0", " ")
            paragraph_text = re.sub(" +", " ", paragraph_text)
            paragraph_text = re.sub(r"Page\s\d{1,}", "", paragraph_text)

            text_list.append((page_num, block_num, paragraph_text))
            block_num += 1
        page_num += 1

    sorted_text_list = sorted(text_list, key=lambda x: (x[0], x[1]))

    docs = []

    for list_item in sorted_text_list:

        page_num = list_item[0]
        block_num = list_item[1]
        paragraph_text = list_item[2]

        token_length = len(tokenizer.tokenize(paragraph_text))

        if token_length > 0:
            docs.append(paragraph_text)

    return docs   