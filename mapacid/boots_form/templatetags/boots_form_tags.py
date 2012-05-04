from django import template
import django

register = template.Library()

@register.simple_tag
def boots_form(obj, inline=None):
    '''
    the required param, is only used when obj = Field for optional required fields.
    '''
    
    if isinstance(obj, django.forms.BaseForm):
        return form(obj, inline)
    elif isinstance(obj, django.forms.forms.BoundField):
        return form_field(obj, inline)
    else:
        raise Exception, 'Bootstrap template tag recieved a non form or field object'



def form_field(field, inline):
    if inline=="inline":
        field.field.widget.attrs['placeholder']=field.label
        t = template.loader.get_template('boots_form/form_field_inline.html')
    else:
        t = template.loader.get_template('boots_form/form_field.html')
    return t.render(template.Context({'field': field}))


def form(form, inline):
    form_html = ''

    if inline=="inline":
        t = template.loader.get_template('boots_form/form_field_inline.html')
    else:
        t = template.loader.get_template('boots_form/form_field.html')
    
 
    for fld in form.visible_fields():
        row = t.render(template.Context({'field': fld,}))
        form_html += row
    
    for fld in form.hidden_fields():
        row = unicode(fld)
        form_html += u'<div style="display:none;"> %s </div>' %(row)  
    
    
    return form_html

