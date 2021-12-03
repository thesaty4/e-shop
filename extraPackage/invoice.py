from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')

def genrate_invoice_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    pdf = result.getvalue()
    #return HttpResponse(pdf, content_type='application/pdf')
    # force download
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_"+str(context_dict['checkout'])+".pdf"
        # filename = "Invoice_%s.pdf" %(data['order_id'])
        content = "inline; filename='%s'" %(filename)
        # download = request.GET.get("download")
        #if download:
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
    return response

def genrate_reciept_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)
    pdf = result.getvalue()
    #return HttpResponse(pdf, content_type='application/pdf')
    # force download
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Reciept_"+str(context_dict['checkout'])+".pdf"
        # filename = "Invoice_%s.pdf" %(data['order_id'])
        content = "inline; filename='%s'" %(filename)
        # download = request.GET.get("download")
        #if download:
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
    return response

    