import PyPDF2 as pypdf
import os
#from sklearn.datasets import load_iris
import pandas as pd
import openpyxl


# poano
# datefrom
# dateto
# company
# TIN
# poaperson
# ticketno
# ticketdate
# product code
# product
# uom
# quantity

delstr = "\<>*?/"":|"
pdf_data_list = []

def replaceAll(str):
    # company = company.replaceAll('\<>*?/":|','')
    str = str.replace('"','')
    str = str.replace('\\', '')
    str = str.replace('<', '')
    str = str.replace('>', '')
    str = str.replace('*', '')
    str = str.replace('/', '')
    str = str.replace('""', '')
    str = str.replace(':', '')
    str = str.replace('|', '')
    return str

def getmonth(str):
    if str=="yanvar":
        return "01"
    elif str== "fevral":
        return "02"
    elif str=="mart":
        return "03"
    elif str=="aprel":
        return "04"
    elif str=="may":
        return "05"
    elif str=="iyun":
        return "06"
    elif str=="iyul":
        return "07"
    elif str=="avgust":
        return "08"
    elif str=="sentabr":
        return "09"
    elif str=="oktabr":
        return "10"
    elif str=="noyabr":
        return "11"
    elif str=="dekabr":
        return "12"
    else:
        return "none"

str = "2023 yil 31 may"

def getdate(str):
    year = str.split(' yil ')[0]
    str1 = str.split(' yil ')[1]
    date = str1.split(' ')[0]
    str2 = str1.split(' ')[1]
    month = getmonth(str2)
    dt = date+'.'+month+'.'+year
    return dt

for file in os.listdir(os.chdir('./pdf')):
    pdf = pypdf.PdfReader(file)
    pdf_pages = pdf.pages[0]
    pdf_text = pdf_pages.extract_text()
    #print(pdf_text)
    poano = pdf_text.split('ISHONCHNOMA № \n')[1].split('Berilgan sana:\n')[0].replace('\n', '')
    datefrom =  pdf_text.split('Berilgan sana:\n')[1].split('Ishonchnoma amal qilish muddati:\n')[0].replace('\n','')
    dateto =  pdf_text.split('Ishonchnoma amal qilish muddati:\n')[1].split('Tashkilot nomi:\n')[0].replace('\n', '')
    company =  pdf_text.split('Tashkilot nomi:\n')[1].split('Manzil:\n')[0].replace('\n', '')
    #company = company.replaceAll('\<>*?/":|','')
    company = replaceAll(company)
    #print('-'+datefrom+'-')
    #print('-' + dateto + '-')

    datefrom = getdate(datefrom)
    dateto = getdate(dateto)

    tin = pdf_text.split('STIR:\n')[1].split('Ishonchnoma berildi:\n')[0].replace('\n', '')
    poaperson =  pdf_text.split('FISh: \n')[1].split('\n')[0]
    ticketno =  pdf_text.split('Qabul qilinishi kerak bo‘lgan tovar-moddiy boyliklar ro‘yxati\n')[0].split('\n')[-2].split('-')[0].split(' ')[-1]
    ticketyear =  pdf_text.split('Qabul qilinishi kerak bo‘lgan tovar-moddiy boyliklar ro‘yxati\n')[0].split('\n')[-2].split('-')[0].split(' ')[0]
    ticketday =  pdf_text.split('Qabul qilinishi kerak bo‘lgan tovar-moddiy boyliklar ro‘yxati\n')[0].split('\n')[-2].split('-')[0].split(' ')[2]
    ticketmonth =  pdf_text.split('Qabul qilinishi kerak bo‘lgan tovar-moddiy boyliklar ro‘yxati\n')[0].split('\n')[-2].split('-')[0].split(' ')[3].replace('maydagi', '05')
    ticketdate = f"{ticketday}.{ticketmonth}.{ticketyear}"
    # product_code = pdf_pages.extract_text().split('Miqdori\n1\n2\n3\n4\n5\n1\n')[1]

    productstr = pdf_text.split('5\n1\n')[1]
    #print(productstr)

    grade = ''

    if 'kilogramm' in productstr:
        uom = 'kilogramm'
        grade = productstr.split('kilogramm',1)[0]
        gcode = grade[0:7]
        if gcode.isnumeric():
            grade = grade.split('\n',1)[1]
        #grade = grade.split('\n',1)[1]
        vol = productstr.split('kilogramm',1)[1]
        vol = vol.split('(',1)[0]
        vol = vol.replace('\n', '')
        vol = vol.replace(' ', '')
        vol = vol.split(',')[0]
        volval = int(vol)/1000
        vol = str(volval)
    elif 'tonna' in productstr:
        uom = 'tonna'
        grade = productstr.split('tonna',1)[0]
        gcode = grade[0:7]
        if gcode.isnumeric():
            grade = grade.split('\n',1)[1]
        vol = productstr.split('tonna', 1)[1]
        vol = vol.split('(', 1)[0]
        vol = vol.replace('\n','')
        vol = vol.replace(' ','')
        vol = vol.split(',')[0]

    vol = vol.replace('\n','')
    vol = vol.replace(' ','')
    vol = vol.split(',')[0]

    print('uom='+uom)
    grade = grade.replace('\n',' ')
    grade = grade.strip()

    print('grade="'+grade+'"')
    print('vol="'+vol+'"')

    #print(productstr)
    #print('####\n'+pdf_text)

    newfile = ticketno + " " + poano + " " + company + ".pdf"
    os.rename(file, newfile)
    pdf_data_list.append({
        'ticketno': ticketno,
        'company': company,

        'poano': poano,
        'datefrom': datefrom,
        'dateto': dateto,
        'tin': tin,
        'poaperson': poaperson,

    })

#df = pd.DataFrame(pdf_data_list)
#df.to_excel('111.xlsx')
#df.excelwriter('111.xlsx')
#display(df)