from django.test import TestCase

@login_required
def my_certificates(request):
    certificates = Certificate.objects.filter(made_by=request.user)
    context = {'certificates_1': [],
               'certificates_5': [],
               'certificates_10': [],
               'certificates_20': [],
               'certificates_50': [],
               'certificates_100': [],
               'certificates_200': [],
               'certificates_500': []}
    for cert in certificates:
        if cert.nominal == 1:
            context['certificates_1'].append(cert)
        elif cert.nominal == 5:
            context['certificates_5'].append(cert)
        elif cert.nominal == 10:
            context['certificates_10'].append(cert)
        elif cert.nominal == 20:
            context['certificates_20'].append(cert)
        elif cert.nominal == 50:
            context['certificates_50'].append(cert)
        elif cert.nominal == 100:
            context['certificates_100'].append(cert)
        elif cert.nominal == 200:
            context['certificates_200'].append(cert)
        elif cert.nominal == 500:
            context['certificates_500'].append(cert)
    return render(request, template_name='MainApp/my_certificates.html', context=context)


