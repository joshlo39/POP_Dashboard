import streamlit as st
import sys
import gspread
import requests
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaIoBaseDownload
import io
from PIL import Image
import pyrebase
from reportlab.lib.pagesizes import letter 
from utils import * 
 
def pdf_merger():
    #------------Authentication--------------#
    admin_cred = credentials.Certificate('Firebase Admin SDK.json')
    #firebase_admin.initialize_app(admin_cred)

    firebaseConfig = {
        "apiKey": "AIzaSyAsytsTB2K_PRrtkuxMA8s8cCaup-5Zedc",
        "authDomain": "streamlit-pop-pdfmerger.firebaseapp.com",
        "databaseURL": "https://streamlit-pop-pdfmerger-default-rtdb.firebaseio.com/",
        "projectId": "streamlit-pop-pdfmerger",
        "storageBucket": "streamlit-pop-pdfmerger.appspot.com",
        "messagingSenderId": "574365299032",
        "appId": "1:574365299032:web:86bd2a476ade31a8df352d",
        "measurementId": "G-G8KW4CQV60"
    }


    firebase = pyrebase.initialize_app(firebaseConfig)
    auth = firebase.auth()

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive',]
    creds = Credentials.from_service_account_file('service_credentials.json', scopes=SCOPES)
    sheets_service = build('sheets', 'v4', credentials=creds)
    drive_service = build('drive', 'v3', credentials=creds)


    #------------Configuring Streamlit--------#
    st.title("Peace of Pi: PDF Merger")
    default_sheet = "Practice Test Analysis!C2:C1335"
    range_name = st.text_input("Enter the name of the sheet and the range of cells you want to download:"
                            ,value = default_sheet)
    default_URL = "https://docs.google.com/spreadsheets/d/1RjkWwLxLb9dk8OjNYY6CwxTw4NXOaTO955qKuslNgBE/edit#gid=0"
    range_name = range_name.upper()
    spreadsheet_url = st.text_input("Enter the URL of the spreadsheet:"
                                    ,value = default_URL)
    spreadsheet_id = spreadsheet_url.split('/')[-2]
    names = [
    "Adriana Vingerhoets", "Aanya Naipaul", "Adriana Vingerhoets", "Alejandro Moreno",
    "Andrea Murzi", "Andres Camargo", "Angelo Socarras", "Antonio De Castilho",
    "Arielle Socol", "Bella Morales", "Brigida Sarcona", "Camila Moran",
    "Cristina Macias", "Daisy Stein", "Daniel Esparragoza", "Daniel Sutton",
    "Daniela Duran", "Daniela Padron", "Daniella Vargas", "David Ramirez",
    "Diego Gutierrez", "Dylan Medina", "Eden Ohayon", "Elizabeth Chinea",
    "Emilia Sarcona", "Esteban Chiquito", "Fabiana Tejera", "Freddy Romero",
    "Gabriela Sobrinho", "Gabriella Alfonso", "Gabriella Suao", "Giovanna Musiello",
    "Isabella Torres", "Jade Shim-You", "Jett Pinkerton", "Jielianne Rodriguez",
    "Juan Rodriguez", "Julia Tavares", "Justin Cardenas", "Kirsten Chong",
    "Lauren Kettlewell", "Liam Lesentier", "Lily Quintero", "Lola Shaoul",
    "Lucas Delgado", "Melany Rodriguez", "Mia Vasquez", "Michelle Mendez",
    "Natalie Fernandez", "Nathaly Gonzalez Henriquez", "Nicholas Santiago",
    "Nicolas Alvarez", "Niya Bourdon", "Noah Gomberg", "Ofri Ezra", "Paula Cohen",
    "Paulina Baquero", "Roberto Gamarra", "Rocket Pinkerton", "Sabrina Bianco",
    "Sofia Aleman", "Sol Pereyra Lopez", "Sophia Loszynski", "Sydney Young",
    "Thomas Dos Santos Lara", "Timothy Kinigopoulo", "Tom Sela", "Valerie Duran",
    "Renan De Souza", "Zoe Mcmahon"
    ]
    student_name = st.selectbox("Select a student name:", names)
    if student_name:
        if st.button("Update Cell"):
            if update_sheet_cell(sheets_service, spreadsheet_id, "Dashboard!A1", student_name):
                st.success("Cell updated successfully!")
     
    #---------------Sidebar----------------#
    # student_names = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges="Templates!A2:A2", includeGridData=False).execute()
    # List of names

                    
                    
    #-----------------Settup--------------------#

    practice_tests = ["Ptest #1 (202003U)","Ptest #2 (202012A)","Ptest #3 (202010A)",
                    "Ptest #4 (202011U)","Ptest #5 (202012U)","Ptest #6 (202009U)",
                    "Ptest #7 (202010SD)","Ptest #8 (202010U)","Ptest #9 (202103A)","Ptest #10 (202103U)",
                    "Ptest #11 (201912U)","Ptest #12 (202009A)","Ptest #13 (202008A)","Ptest #14 (201911U)",
                    "Ptest #15 (202105U)","Ptest #16 (201905U)","Ptest #17 (201910U)","Ptest #18 (201905A)",
                    "Ptest #19 (201903U)","Ptest #20 (202105A)","Ptest #21 (202306U)","Ptest #22 (202304SD)",
                      "Ptest #23 (202305U)","D Practice Test #1", "D Practice Test #2", "D Practice Test #3","D Practice Test #4",
                      "NL Practice Test #1","NL Practice Test #2","NL Practice Test #3","NL Practice Test #4"]
    

    sheet_name = range_name.split("!")[0]
    
    category_range = sheet_name + "!" + "K" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "K" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    difficulty_range = sheet_name + "!" + "I" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "I" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    section_range = sheet_name + "!" + "B" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "B" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    correctness_range = sheet_name + "!" + "D" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "D" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    test_range = sheet_name + "!" + "A" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "A" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    solutions_range = sheet_name + "!" + "F" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "F" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    
    sub_category_one_range= sheet_name + "!" + "L" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "L" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    sub_category_two_range= sheet_name + "!" + "M" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "M" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    sub_category_three_range= sheet_name + "!" + "N" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "N" + (range_name.split("!")[1].split(":")[1].split()[0][1:])

    solutions_images_range = sheet_name + "!" + "E" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "E" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    range_list = [category_range, difficulty_range, section_range, correctness_range,test_range,solutions_range,solutions_images_range,sub_category_one_range,sub_category_two_range,sub_category_three_range]

    
    category = ["HOA","PSDA","PAM","GEOM","Vocab","Big Picture","Reading for Function","Literal Comprehension","Text Completion","Supporting Evidence", "Graphs and Charts","Comma Uses and Misuses","Subject-verb agreement","Combining and Separating Sentences","Essential and Non-essential clauses","Transitions","Plain Text"]
    sub_category_one = ['Linear Functions Part 1','Angles and Triangles','Intro to Functions','Linear Functions Part 2','Polynomial Expressions','Rational Expressions','Special Cases','Right Triangles & Trig','Exponential Functions','Quadratic Equations',
 'Isolating Variables',
 'Systems of Equations',
 'Linear Equations',
 'Interpreting Graph',
 'Two-Way Tables',
 'Scatter Plots',
 'Percents',
 'Unit Conversions',
 'Data and Stats 1',
 'Rates',
 'Rational Functions',
 'Quadratic & Polynomial Functions',
 'Linear vs. Exponential Functions',
 'Ratios',
 'Planar Geometry',
 'Solid Geometry',
 'Equation of a Circle',
 'Exponential Equations',
 'Absolute Value',
 'Probability',
 'Radical Equations',
 'Similar Triangles',
 'Linear Equations and Inequalities WP',
 'Parallel and Perpendicular Lines',
 'Circle Ratios',
 'Exponential & Radical Expressions',
 'Rational Equations',
 'Complex Numbers',
 'Data and Stats 2']
    sub_category_two =[
     "Deriving Equation", "Parallel Lines & Transversals", "Evaluating", "Deriving Inequality", "Adding/Subtracting",
    "POG", "Dividing", "Linear Equations", "Pythagorean", "Finding y-int", "SOS",
    "NA", "Finding Slope", "Substitution", "Factoring", "Fractions & Decimals", "45-45-90",
    "Line Graph", "Fraction of", "Predicted Value", "Percent of", "Single Conversion", "Median",
    "Interpreting", "Deriving Graph", "30-60-90", "Mixed", "Word Problem", "Factored Form",
    "Unit Circle", "Probability", "Number of Solutions", "Special Cases", "Elimination", "Direct Proportionality",
    "Finding Area", "Greater/Less than", "Intercepts", "Finding Volume", "Adding & Subtracting", "Quadratic Formula",
    "Shift", "Base Reduction", "Distributing", "Finding Perimeter", "Solving", "Mean",
    "Data Set", "Basic", "Range", "Multiplying", "Comparing", "Standard Form",
    "Congruency", "Create & Solve", "Systems of Equations", "sinx=cosy", "Interpreting Equation", "Percent Inc/Dec",
    "Cubic", "Proportions", "OG", "Finding Arc Length", "Interpreting Graph", "Vertex Form",
    "Inequality Graph", "Isosceles", "Product Rule", "Linear Combination", "Trig", "Actual vs. Predicted",
    "Percent Change", "Sub & Solve", "Pie Chart", "Population Density", "Finding Length", "Tangent Line",
    "Standard Deviation", "Rate to Rate", "Classic", "Proof", "Easy", "General Form",
    "Radical to Exponential", "Sum of Solutions", "Finding Solution", "Outlier", "Skew", "Definition",
    "Reverse", "Square Root Method", "Graph", "Cylinder", "Linear Function", "Quadratic Function",
    "Finding Surface Area", "Finding x-int", "Constants", "Rectangular Prism", "Create & Sub", "Triple",
    "Hard", "Finding Area of Shaded Region", "Triangles", "Average Speed", "Inequality", "Finding Ratio",
    "Fractions", "Long Division", "PTSI", "Double Conversion", "How many times", "Bar Graph",
    "Finding Radius", "Reading Graph", "Arc Length and Angle", "Equation", "Extraneous Solutions", "Area",
    "Vertical Angles", "Angle sum of Quadrilaterals", "Zeros from equation", "Quotient Rule", "Directly Proportional", "Margin of Error",
    "Sample Selection", "Likelihood", "Proving", "Finding Width", "Degrees and Radians", "Create Equation & Solve",
    "Right Triangle", "Percent Mixed", "Finding Value", "Solving for x", "Volume", "Parallel",
    "Single", "Finding Intercepts", "Deriving Table", "Ratio", "Finding intercepts", "Perpendicular",
    "Finding Arc Measure", "Proportion", "Max", "y-int", "Radians & Degrees", "Pythagorean Theorem",
    "Multi-Dimensional", "Radical as well", "Finding Predicted y-value", "Perimeter", "Complex", "Surface Area",
    "Radical to Exponential ", "x-int", "Density", "POS", "Deriving Expression", "Min", "Comparing Means", "Finding Angle", "Square root method"
]
    sub_category_three = [
    "Table", "Finding Angle", "f(a)", "NA", "Slope-Intercept Form", "Table to Graph", "Perfect Square", "Points", "Infinitely Many Solutions", "Trapezoid", "Equation", "Factoring", "Word Problem", "Graph", "Factored Form", "Square", "Part", "Box-Plot", "Whole", "Frequency Table", "Standard Form", "Inequality", "Triangle + Kite", "Bar Graph", "Finding vertex", "Scatter Plots", "Constants", "Unit Circle", "Elimination", "Discriminant", "Finding x-int", "No Solution", "Data Set", "Parallelogram", "Diameter", "Right Triangle", "Decimals", "Asymptote", "Ratio & Area", "Trick", "Deriving Graph", "Trig", "Perpendicular", "One-Variable", "New", "Percent Inc/Dec", "Dot Plot", "Percent", "Function Notation", "Deriving Equation", "One Solution", "Proving", "Geometric Mean", "Decrease", "Quadratic Equation", "Finding Radius", "Rectangle", "Frequency", "Substitution", "Line Graph", "If", "A>1", "Rate to Rate", "Interpreting", "Finding Sine and Cosine", "How Many Times", "Increase", "Finding Sine", "Distributing negative", "Unit Conversion", "Finding Ratio", "Product Rule", "Ratio", "Finding Center", "A=1", "f(0)", "Extraneous Solutions", "y-int", "Interpreting intercept", "Cylinder", "Finding Cosine", "Square Root Method", "Quadratic Formula", "Outer-Inner", "Hour Glass", "Finding Sine and Tangent", "Difference of Squares", "Finding Circumference", "Mixed", "y", "Finding Solution", "Vertex Form", "Area", "Finding Sum of x-coordinates", "Radical to Exponential", "Initial Amount", "Rationalizing", "Radius and Angle", "U-Sub", "y-value", "Triangle", "f(x)=a", "Solving", "Scale", "Circle", "Finding Side Length", "PTSI", "Distributing Negative", "Finding y-value", "Sphere", "f(x)=0", "Finding Perimeter", "x", "Rate of Change", "Proof", "X^4", "Triangle and Circle", "Reading Graph", "Equations", "Cube", "Standard to General Form", "Cylinder and Sphere", "Equation and Point", "Dividing", "Shift", "Grouping", "Absolute Value", "Adding & Subtracting", "Rectangle and Semi-Circle", "Finding Max", "Form", "Radius", "Diff of Squares", "PFT", "Constants", "GCF", "Slope and Point", "Right Triangles", "Deriving", "Rectangular Prism", "Sub and Solve", "Definition", "Cone", "Finding Area", "a=1", "Linear", "Cosine", "Finding Vertex", "Sub & Solve", "Word Problems", "One-Step", "x=a", "From Equation", "Tangent", "Infinitely Many", "Both", "Isosceles Right Triangle", "Similarity", "a>1", "Function", "Sine", "Time", "Finding Slope", "Exponential Function", "Radians to degrees", "x-int", "POG", "Angle", "Squared", "Two-Step", "Exponential", "Factored", "From Graph", "Inscribed Square", "Histogram", "Rate Word Problem", "How many times", "Quadratic Function", "Single", "Percent of", "Combined Mean", "Finding x", "Max", "Radians to Degrees", "Find height", "Directly Proportional", "Finding y", "Initial", "Outer - Inner", "Finding Diameter", "Rate word problem", "System of Inequality", "Classic", "Deriving Table", "Double Bubble", "Factor by grouping", "Multi-step", "Exponential Functions", "Isosceles Triangle", "Solving for y", "Finding Constants", "Percent greater"
]
    difficulty = ["1","2","3","4","5"]
    correctness = {
        "Correct":"1",
        "Incorrect":"0"
        }
    section = ["1","2","2E","2H","3","4"]
    
    st.subheader("Filter")
    selected_tests = set(st.multiselect("Practice Tests:", practice_tests))
    selected_difficulty = set(st.multiselect("Difficulty", difficulty))
    
    selected_category = set(st.multiselect("Category", category))
    selected_category_one = set(st.multiselect("Sub-Category 1",sub_category_one))
    selected_category_two = set(st.multiselect("Sub-Category 2",sub_category_two))
    selected_category_three = set(st.multiselect("Sub-Category 3",sub_category_three))
    
    selected_correctness = set(st.multiselect("Correct or Incorrect", correctness.values()))
    
    selected_section = set(st.multiselect("Section/Module", section))
    download_result = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=range_name, includeGridData=True).execute()
    filtered_dataset = sheets_service.spreadsheets().values().batchGet(spreadsheetId=spreadsheet_id, ranges=range_list).execute()
    
    #store the values into individual array
    category_values = filtered_dataset['valueRanges'][0]['values']
    difficulty_values = filtered_dataset['valueRanges'][1]['values']
    section_values = filtered_dataset['valueRanges'][2]['values']
    correctness_values = filtered_dataset['valueRanges'][3]['values']
    test_values = filtered_dataset['valueRanges'][4]['values']
    sub_category_one_values = filtered_dataset['valueRanges'][7]['values']
    sub_category_two_values = filtered_dataset['valueRanges'][8]['values'] 
    sub_category_three_values = filtered_dataset['valueRanges'][9]['values']
    print(f"SubCat 3 Values {sub_category_three_values}")
    # Flags to check if filters are active
    is_category_filter = len(selected_category) > 0
    is_difficulty_filter = len(selected_difficulty) > 0
    is_section_filter = len(selected_section) > 0
    is_correctness_filter = len(selected_correctness) > 0
    is_test_filter = len(selected_tests) > 0
    is_subcategory1_filter = len(selected_category_one) > 0
    is_subcategory2_filter = len(selected_category_two) > 0
    is_subcategory3_filter = len(selected_category_three) > 0
    save_dir = 'downloaded_pngs'
    #-----------------Normal Packet--------------------#
    if st.button("Generate PDF"):
        hyperlinks = []
        #GET Calls to Google Sheets API
                # Delete images from folder
        for filename in os.listdir(save_dir):
            if filename.endswith(".png"):
                os.remove(os.path.join(save_dir, filename))
        pdf_path = 'downloaded_pngs/merged.pdf'
        

        #i dont think this does anything important 
        video_hyperlinks = []
        for number_of_rows, row in enumerate(download_result['sheets'][0]['data'][0]['rowData']):
            for num_of_row_values, cell in enumerate((row['values'])):
                # Check if cell meets all active filters
                #the logic is if the filter is not active then reurns true for that particular filter
                    if 'hyperlink' in cell:
                        video_hyperlinks.append(cell['hyperlink'])     
        
        idx = 0 # Index of the current cell
        for number_of_rows, row in enumerate(download_result['sheets'][0]['data'][0]['rowData']):
            for num_of_row_values, cell in enumerate((row['values'])):
                # Check if cell meets all active filters
                #the logic is if the filter is not active then reurns true for that particular filter
                if (not is_category_filter or category_values[idx][0] in selected_category) and \
                (not is_difficulty_filter or difficulty_values[idx][0] in selected_difficulty) and \
                (not is_section_filter or section_values[idx][0] in selected_section) and \
                (not is_correctness_filter or correctness_values[idx][0] in selected_correctness) and \
                    (not is_test_filter or test_values[idx][0] in selected_tests) and \
                    (not is_subcategory1_filter or sub_category_one_values[idx][0] in selected_category_one) and \
                    (not is_subcategory2_filter or sub_category_two_values[idx][0] in selected_category_two) and \
                    (not is_subcategory3_filter or sub_category_three_values[idx][0] in selected_category_three):
                    if 'hyperlink' in cell:
                        hyperlinks.append(cell['hyperlink'])     
                
                idx += 1
                
        os.makedirs(save_dir, exist_ok=True)
        
        # Download images
        for idx, url in enumerate(hyperlinks):
            try:
                if 'drive.google.com' in url:
                    file_id = url.split('/')[-2]
                    file_path = os.path.join(save_dir, f'image_{idx + 1}.png')
                    download_drive_file(drive_service, file_id, file_path)
                else:
                    print(f"Failed to download or invalid content type for URL: {url}")
            except Exception as e:
                print(f"Request failed for URL {url}: {e}")
                
        
        images = []
        
        #Convert images to pdf
        # file_names = os.listdir(save_dir)
        # file_names.remove('merged.pdf') 
        # file_names.sort(key = lambda x: int(x.split('_')[1].split('.')[0]))
        # for filename in (file_names):
        #     if filename.endswith(".png"):
        #         filepath = os.path.join(save_dir, filename)
        #         image = (Image.open(filepath))
        #         images.append(image.convert('RGB'))
        
        #hyperlinks for video 
        solutions_result = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=solutions_range, includeGridData=True).execute()
        solution_data = solutions_result['sheets'][0]['data'][0]['rowData']

        #-----------------Getting all video link--------------------#
        # video_hyperlinks = [] 
        # for i,item in enumerate(solution_data):
        #     print(f"Category Index: {i}, Value: {category_values[i][0]}")
        #     if (not is_category_filter or category_values[i][0] in selected_category) and \
        #         (not is_difficulty_filter or difficulty_values[i][0] in selected_difficulty) and \
        #         (not is_section_filter or section_values[i][0] in selected_section) and \
        #         (not is_correctness_filter or correctness_values[i][0] in selected_correctness) and \
        #         (not is_test_filter or test_values[i][0] in selected_tests):
        #         for idx,value in enumerate(item['values']):
        #                 uri = value['userEnteredFormat']['textFormat']['link']['uri']
        #                 video_hyperlinks.append(uri)

        #video hyperlinks comes in order
        #images don't come in order 
        print(f"Length of Video Hyperlink", len(video_hyperlinks))
        for idx,uri in enumerate(video_hyperlinks):
           print(f'Index: {idx}, URI: {uri}') 
        #------Images------#
        image_paths = []
        inner_array = []
        file_names = [f for f in os.listdir(save_dir) if f != 'random.txt'] 
        if 'merged.pdf' in file_names:
            file_names.remove('merged.pdf')
        print(f"File Names: {file_names}")
        file_names.sort(key = lambda x: int(x.split('_')[1].split('.')[0]))
        get_rick_rolled= "https://www.youtube.com/watch?v=v7ScGV5128A"
        for idx, filename in enumerate(file_names):
            if filename.endswith(".png"):
                print(f"Index: {idx}, Filename: {filename}, URI: {get_rick_rolled}")
                filepath = os.path.join(save_dir, filename)

                inner_array.append((filepath, (f" ", get_rick_rolled)))
                
                if len(inner_array) == 4:
                    image_paths.append(sorted(inner_array))
                    inner_array = []
        #if there is a non-full page of images, then append it to the end of the outer array
        if inner_array:
            image_paths.append(inner_array)
        for idx,page in enumerate(image_paths):
            print(f"Page Index:{idx}")
            for image in page:
                print(f"Image Tuple: {image}")
        
        
        #------Video Hyperlinks------#
        #i dont think i use this
        # hyperlink_details = [[]]
        # for idx, url in enumerate(hyperlinks):
        #     hyperlink_details[0].append(())
            
        
        # print(f"hyperlink_details", hyperlink_details)
        #create_pdf_with_2x2_images_hyperlinks('downloaded_pngs/merged.pdf', image_paths )
        create_pdf_with_2x2_images_hyperlinks_small_hyperlink('downloaded_pngs/merged.pdf', image_paths )
        
        # pdf_path = os.path.join(save_dir,'merged.pdf')
        # if len(images) > 0:
        #     images[0].save(pdf_path, save_all=True, append_images=images[1:])
        # else:
        #     st.error("No images to merge")

        # Delete images from folder
        for filename in os.listdir(save_dir):
            if filename.endswith(".png"):
                os.remove(os.path.join(save_dir, filename))
        pdf_path = 'downloaded_pngs/merged.pdf'
        
        #open pdf for user to download
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                btn = st.download_button(
                    label = "Merged PDF",
                    data = f,
                    file_name = 'merged.pdf',
                    mime = 'application/octet-stream'
                )
        for filename in os.listdir(save_dir):
            if filename.endswith(".pdf"):
                os.remove(os.path.join(save_dir, filename))
#-----------------End of Normal Packet--------------------#

#-----------------Solutions Packet--------------------#      
    if st.button("Generate Solutions"):
        
        download_result = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=solutions_images_range, includeGridData=True).execute()
        filtered_dataset = sheets_service.spreadsheets().values().batchGet(spreadsheetId=spreadsheet_id, ranges=range_list).execute()
        solutions_result = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=solutions_range, includeGridData=True).execute()
        solution_data = solutions_result['sheets'][0]['data'][0]['rowData']

        #-------Getting hyperlink for the images and downloading the images-------#
        hyperlinks = []
        idx = 0 # Index of the current cell
        for number_of_rows, row in enumerate(download_result['sheets'][0]['data'][0]['rowData']):
            for num_of_row_values, cell in enumerate((row['values'])):
                # Check if cell meets all active filters
                #the logic is if the filter is not active then reurns true for that particular filter
                if (not is_category_filter or category_values[idx][0] in selected_category) and \
                (not is_difficulty_filter or difficulty_values[idx][0] in selected_difficulty) and \
                (not is_section_filter or section_values[idx][0] in selected_section) and \
                (not is_correctness_filter or correctness_values[idx][0] in selected_correctness) and \
                (not is_test_filter or test_values[idx][0] in selected_tests) and \
                (not is_subcategory1_filter or sub_category_one_values[idx][0] in selected_category_one) and \
                (not is_subcategory2_filter or sub_category_two_values[idx][0] in selected_category_two) and \
                (not is_subcategory3_filter or sub_category_three_values[idx][0] in selected_category_three):
                    if 'hyperlink' in cell:
                        hyperlinks.append(cell['hyperlink'])     
                
                idx += 1
                
        os.makedirs(save_dir, exist_ok=True)
        # Delete images from folder
        for filename in os.listdir(save_dir):
            if filename.endswith(".png"):
                os.remove(os.path.join(save_dir, filename))
        pdf_path = 'downloaded_pngs/merged.pdf'
        
        # Download images
        for idx, url in enumerate(hyperlinks):
            try:
                if 'drive.google.com' in url:
                    file_id = url.split('/')[-2]
                    file_path = os.path.join(save_dir, f'image_{idx + 1}.png')
                    download_drive_file(drive_service, file_id, file_path)
                else:
                    print(f"Failed to download or invalid content type for URL: {url}")
            except Exception as e:
                print(f"Request failed for URL {url}: {e}")

        #-------END: Getting hyperlink for the images and downloading the images-------#

        #-----------------Getting all video link--------------------#
        video_hyperlinks = [] 
        for i, item in enumerate(solution_data):
            print(f"Category Index: {i}, Value: {category_values[i][0]}")
            if (not is_category_filter or category_values[i][0] in selected_category) and \
                (not is_difficulty_filter or difficulty_values[i][0] in selected_difficulty) and \
                (not is_section_filter or section_values[i][0] in selected_section) and \
                (not is_correctness_filter or correctness_values[i][0] in selected_correctness) and \
                (not is_test_filter or test_values[i][0] in selected_tests) and \
                (not is_subcategory1_filter or sub_category_one_values[i][0] in selected_category_one) and \
                (not is_subcategory2_filter or sub_category_two_values[i][0] in selected_category_two) and \
                (not is_subcategory3_filter or sub_category_three_values[i][0] in selected_category_three):
                for idx, value in enumerate(item['values']):
                    if 'userEnteredFormat' in value and 'textFormat' in value['userEnteredFormat'] and 'link' in value['userEnteredFormat']['textFormat']:
                        uri = value['userEnteredFormat']['textFormat']['link']['uri']
                        video_hyperlinks.append(uri)
        #video hyperlinks comes in order
        #images don't come in order 
        print(f"video_hyperlinks", video_hyperlinks)
        for idx,uri in enumerate(video_hyperlinks):
           print(f'Index: {idx}, URI: {uri}') 
        #------Images------#
        image_paths = []
        inner_array = []
        
        file_names = [f for f in os.listdir(save_dir) if not f.startswith('r')]
        print(f"File Names: {file_names}")
        file_names.sort(key = lambda x: int(x.split('_')[1].split('.')[0]))
        for idx, filename in enumerate(file_names):
            if filename.endswith(".png"):
                print(f"Index: {idx}, Filename: {filename}, URI: {video_hyperlinks[idx] if len(video_hyperlinks) > 0 else 'https://www.youtube.com/watch?v=v7ScGV5128A'}")
                filepath = os.path.join(save_dir, filename)
                inner_array.append((filepath, (f" ", video_hyperlinks[idx] if len(video_hyperlinks) > 0 else 'https://www.youtube.com/watch?v=v7ScGV5128A')))
                
                if len(inner_array) == 4:
                    image_paths.append(sorted(inner_array))
                    inner_array = []
        #if there is a non-full page of images, then append it to the end of the outer array
        if inner_array:
            image_paths.append(inner_array)
        for idx,page in enumerate(image_paths):
            print(f"Page Index:{idx}")
            for image in page:
                print(f"Image Tuple: {image}")
        if len(video_hyperlinks) > 0:
            create_pdf_with_2x2_images_hyperlinks('downloaded_pngs/merged.pdf', image_paths )
        else:
            create_pdf_with_2x2_images_hyperlinks_small_hyperlink('downloaded_pngs/merged.pdf', image_paths )
    

        # Delete images from folder
        for filename in os.listdir(save_dir):
            if filename.endswith(".png"):
                os.remove(os.path.join(save_dir, filename))
        pdf_path = 'downloaded_pngs/merged.pdf'
        
        
        #open pdf for user to download
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                btn = st.download_button(
                    label = "Merged PDF",
                    data = f,
                    file_name = 'merged.pdf',
                    mime = 'application/octet-stream'
                )
        for filename in os.listdir(save_dir):
            if filename.endswith(".pdf"):
                os.remove(os.path.join(save_dir, filename))

         

    
    
    
    
    
    
    
    
    
    
    
    
    
     
    # #USER AUTHENTICATION
    # def user_logged_in():
    #     return st.session_state['user_token'] is not None
        

    # if 'user_token' not in st.session_state:
    #     st.session_state['user_token'] = None          
    # choices = st.selectbox("Select an option", ["Login", "Signup"])
    # #login
    # email = st.text_input("Email")
    # password = st.text_input("Password", type="password")

    # if choices == "Signup":
    #     submit = st.button("Create my account")
    #     if submit:
    #         try:
    #             user = auth.create_user_with_email_and_password(email, password)
    #             st.success("Account created successfully")
    #         except firebase_admin.auth.EmailAlreadyExistsError:
    #             st.error("Email already exists")
    # else:
    #     if st.button("Login"):
    #         try:
    #             user = auth.sign_in_with_email_and_password(email, password)
    #             st.session_state['user_token'] = user['idToken']
    #             st.success("Logged in successfully")
    #         except:
    #             st.error("Invalid email/password")

    # if user_logged_in():
    #     main()
    # else:
    #     st.info("Please login/signup to continue")
