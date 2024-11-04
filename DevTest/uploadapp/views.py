import pandas as pd
from django.shortcuts import render,redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse

def upload_file_view(request):
    summary_report = None  
    if request.method == 'POST' and request.FILES['file']:
        
        uploaded_file = request.FILES['file']
        try:

            df = pd.read_excel(uploaded_file)  
        except ValueError:
         
            try:
                df = pd.read_csv(uploaded_file, encoding='ISO-8859-1')  # Try common alternative encoding
            except UnicodeDecodeError:
                return render(request, 'uploadapp/upload.html', {
                    'error': 'File encoding is unsupported. Please upload a valid CSV or Excel file.'
                })


        if 'Cust State' in df.columns and 'DPD' in df.columns:
            
            summary = df.groupby('Cust State').agg(
                Total_Count=('DPD', 'size'),
                Avg_DPD=('DPD', 'mean'),
                Max_DPD=('DPD', 'max')
            ).reset_index()


            summary_html = summary.to_html(index=False)
            
           
            subject = f"Python Assignment - {settings.MY_NAME}"
            html_message = f"""
            <html>
                <body>
                    <h2>Summary Report</h2>
                    {summary_html}
                </body>
            </html>
            """
            send_mail(
                subject=subject,
                message="Please find the summary report below.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=['vasukrishn2002@gmail.com'],
                html_message=html_message, 
            )
            return render(request, 'uploadapp/sucess.html')
        else:
            summary_html = "<p>File does not contain the required columns 'Cust State' and 'DPD'.</p>"

        return render(request, 'uploadapp/upload.html', {'summary': summary_html})

    return render(request, 'uploadapp/upload.html')



def sucess(request):
    return render(request, 'sucess.html')