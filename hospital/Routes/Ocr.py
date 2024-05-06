from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import pytesseract
from PIL import Image
import io, json, os
from PyPDF2 import PdfReader
from hospital.models import Patient , PatientDocument
from g4f.client import Client
from django.conf import settings
import ast

def generate_summary(text):
    client = Client()
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
         messages=[
                    {"role": "System", "content": "You are a use full ai to give the summary of the given content in english"},
                    {"role": "user", "content": f"give me the summary of the following content '''{text}'''."}
                  ]
    )
    ai_response = chat_completion.choices[0].message.content or ""
    return ai_response

def handle_conversation(request, user_input):
    client = Client()
    directory_path = os.path.join(settings.STATIC_ROOT, 'ai_convo')
    os.makedirs(directory_path, exist_ok=True)
    try:
        file_path = os.path.join(directory_path, f'conversation_history{request.user.id}.json')
        with open(file_path, 'r') as file:
            conversation_history = json.load(file)
    except FileNotFoundError:
        conversation_history = []
        conversation_history.append({"role": "system", "content": "You are a useful Ai for memorize my data about me and my documentation you should be give the details whenever i will ask you i can search the thing using keyword or concept so toy should proved details following structure if the document match more then one give thee dict in the set of list. give me the response in json structure like [{'document_id':0, 'document_short_details':'detail', 'summary_of_doc':'summary', 'updated_time_of_doc':'time', 'response_of_question':'response'},{'document_id':1, 'document_short_details':'detail', 'summary_of_doc':'summary', 'updated_time_of_doc':'time', 'response_of_question':'response'}]"})
        
    conversation_history.append({"role": "user", "content": user_input})
    chat_completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conversation_history
    )
    ai_response = chat_completion.choices[0].message.content or ""
    conversation_history.append({"role": "assistant", "content": ai_response})
    with open(file_path, 'w') as file:
        json.dump(conversation_history, file)
    print(ai_response)

def get_bot_response(request):
    directory_path = os.path.join(settings.STATIC_ROOT, 'ai_convo')
    os.makedirs(directory_path, exist_ok=True)
    client = Client()

    if request.method == 'POST':
        # text = request.POST.get("text", "") + ".Give me the response the format of [{'document_id': 123, 'document_short_details': 'detail', 'summary_of_doc': 'summary', 'updated_time_of_doc': 'time', 'response_of_question': 'response'}, {'document_id': 456, 'document_short_details': 'detail', 'summary_of_doc': 'summary', 'updated_time_of_doc': 'time', 'response_of_question': 'response'}]"
        text = request.POST.get("text", "") +".  Note:for keys and string values use should double quotes in the json i need to convert it python dictionary. dont add extra messages, titles, information, markdowns just Give me the response the format of [{'document_id': 18, 'document_short_details': 'Template for a letter explaining absence from work due to personal reasons.', 'summary_of_doc': 'The content is a template for a letter explaining the absence from work on a specific date due to personal reasons. It includes the sender's contact information, recipient's details, date of absence, and a polite closing.', 'updated_time_of_doc': '2024-05-05 20:50:59.800213+00:00', 'response_of_question': 'This is a template for a letter explaining absence from work due to personal reasons on a specific date.'}]. "

        try:
            file_path = os.path.join(directory_path, f'conversation_history{request.user.id}.json')
            with open(file_path, 'r') as file:
                conversation_history = json.load(file)
            conversation_history.append({"role": "user", "content": text})
            
            chat_completion = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation_history
            )
            ai_response = chat_completion.choices[0].message.content or ""
            try:
                python_dict = ast.literal_eval(ai_response)
                docs = []
                docs_id = []
                document_short_details = []
                summary_of_doc = []
                updated_time_of_doc = []
                print(python_dict)
                for i in python_dict:
                    docs.append(PatientDocument.objects.get(id=int(i['document_id'])))
                    docs_id.append(i['document_id'])
                    document_short_details.append(i['document_short_details'])
                    summary_of_doc.append(i['document_short_details'])
                    updated_time_of_doc.append(i['updated_time_of_doc'])
                patient = Patient.objects.get(user=request.user)
                return render(request, "OCR_Ai/bot_temp.html",{'patient': patient, "ai_response":zip(docs, docs_id, document_short_details, summary_of_doc, updated_time_of_doc), "response_of_question":python_dict[0].get('response_of_question')})
            except Exception as e:
                print("error : ", e)
                patient = Patient.objects.get(user=request.user)
                return render(request, "OCR_Ai/bot_temp.html",{'patient': patient, 'response_of_question': ai_response})
        
        except FileNotFoundError:
            return HttpResponse("Details not exists.")
    else:
        patient = Patient.objects.get(user=request.user)
        context = {'patient': patient}
        return render(request, "OCR_Ai/bot_temp.html", context)
    
            


@csrf_exempt
def upload_image_view(request):
    if request.method == 'POST' and request.FILES['document']:
        uploaded_file = request.FILES['document']
        
        if is_valid_image(uploaded_file):        
            extracted_text = extract_text_from_image(uploaded_file)
        else:
            extracted_text = extract_text_from_pdf(uploaded_file)
        summary = generate_summary(extracted_text)
        updated_doc = PatientDocument.objects.create(user=request.user, file=uploaded_file, file_content=extracted_text, summary=summary)
        req_data = f"['text content':'{extracted_text}', 'document id': {updated_doc.id},'summary': '{summary}', date:{updated_doc.last_updated_file}'']"
        handle_conversation(request, req_data)
        
        patient = Patient.objects.get(user=request.user)
        doc_items = PatientDocument.objects.filter(user = request.user)[::-1]
        context = {'patient': patient, "doc": doc_items}
        
        return render(request, 'OCR_Ai/get_file.html',context)
    else:
        patient = Patient.objects.get(user=request.user)
        doc_items = PatientDocument.objects.filter(user = request.user)[::-1]
        context = {'patient': patient, "doc": doc_items}
        
        return render(request, 'OCR_Ai/get_file.html',context)

def is_valid_image(image):
    """
    Check if the uploaded file is a valid image.
    
    Args:
    - image: Uploaded file object.
    
    Returns:
    - valid (bool): True if the file is a valid image, False otherwise.
    """
    # Get the file extension
    file_extension = image.name.split('.')[-1].lower()
    
    # Check if the file extension corresponds to an image format
    valid_extensions = ['jpg', 'jpeg', 'png', 'gif']
    if file_extension in valid_extensions:
        return True
    else:
        return False


def extract_text_from_image(image):
    """
    Extract text from an image.
    
    Args:
    - image: Image file object.
    
    Returns:
    - text (str): Extracted text from the image.
    """
    # Set the path to the Tesseract executable
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"
    
    with Image.open(image) as img:
        # Use pytesseract to extract text from the image
        text = pytesseract.image_to_string(img, lang="eng")
    return text


def extract_text_from_pdf(pdf_file):
    """
    Extract text from a PDF file.
    
    Args:
    - pdf_file: PDF file object.
    
    Returns:
    - text (str): Extracted text from the PDF.
    """
    # Read the content of the PDF file
    pdf_content = pdf_file.read()
    
    # Create a PdfReader object
    pdf_reader = PdfReader(io.BytesIO(pdf_content))
    
    # Initialize an empty string to store the extracted text
    extracted_text = ""
    
    # Iterate through each page of the PDF
    for page_num in range(len(pdf_reader.pages)):
        # Extract text from the current page and append it to the extracted_text string
        page = pdf_reader.pages[page_num]
        extracted_text += page.extract_text()
    return extracted_text
    
    
def show_doc(request):
    try:    
        patient = Patient.objects.get(user=request.user)
        doc_items = PatientDocument.objects.filter(user = request.user)[::-1]
        context = {'patient': patient, "doc": doc_items}
    except:
        context = {}
    return render(request, 'OCR_Ai/show_docs.html',context)