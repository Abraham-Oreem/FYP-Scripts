import PyPDF2
global page_num

def extract_text_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        return text

def main(text):
    for number in range(len(text)+1):
        if(text[number] == 'a' or text[number] == 'A'):
            return(1)
        elif(text[number] == 'b' or text[number] == 'B'):
            return(12)
        elif(text[number] == 'c' or text[number] == 'C'):
            return(14)
        elif(text[number] == 'd' or text[number] == 'D'):
            return(145)

page_num=0
main(extract_text_from_pdf('C:/Users/Dell/Desktop/FYP/sample.pdf'))
