# -*- coding: utf-8 -*-
from django import forms

from django.core.exceptions import ValidationError

from django.contrib.auth.models import User

from django.db.models import Q

from django.core.files import File


from servico.models import Ponto, PontoCategoria

from utils import getGeoCode

class PontoFileForm(forms.ModelForm):
    ''' Formulario para upload de arquivo de ponto '''
    arquivo  = forms.FileField(required=False)

    def __init__(self, *args, **kargs): 
        self.user = kargs.pop('user', None)
        super(PontoFileForm, self).__init__(*args, **kargs)
        #if self.files :
        #    print self.files['arquivo']
        #    self.fields['titulo'].required = False
        #    self.fields['categoria'].required = False

    def clean(self):
        '''arq =  self.cleaned_data.get('arquivo', None)
        if arq:
            print arq.read()
        '''
        return self.cleaned_data


    def save(self,  *args, **kargs):
        is_new = self.instance.pk is None
        arq = self.cleaned_data.get('arquivo', None)
        commit = kargs.pop('commit', True)#mantem commit padrão caso não esteja explicitamnte definido
        kargs.update({'commit':False})
        self.instance.regs = 0
        self.instance.regs_ok = []

        if not arq:
            instance = super(PontoFileForm, self).save(*args, **kargs) #executa super com commit False
        else:
            #print "chegou"
            for l in arq.readlines():
                #print l
                self.instance.regs +=1
                add = l.split(';')
                if len(add) >=5:
                    self.instance.regs_ok.append(add)
                    json_ret  = getGeoCode( "%s - %s, %s" %(add[3],add[2], add[1]) ) 
                    print "POINT (%s %s)" %( 
                        json_ret['results'][0]['geometry']['location']['lat'], 
                        json_ret['results'][0]['geometry']['location']['lng']
                        )
                    pt_categoria = PontoCategoria.objects.all()[0]
                    pt = Ponto(categoria=pt_categoria, titulo =add[0] , ponto = 'POINT (%s %s)' %( json_ret['results'][0]['geometry']['location']['lng'], json_ret['results'][0]['geometry']['location']['lat']))
                    pt.save()

        
        if commit:
            if not arq:
                instance.save()
                return instance
            else:
                return self.instance.regs_ok


    class Meta:
        model = Ponto

