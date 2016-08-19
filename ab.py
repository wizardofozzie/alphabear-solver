import dialogs, collections, ui

def form_dialog_from_fields_dict(title, fields_dict, autotext=False, colors=True):
    ret = [{'title': k, 'type': v} for k, v in fields_dict.items()]
    if not autotext:
        for d in ret:
            d.update({
                "autocorrection": False,
                "autocapitalization": ui.AUTOCAPITALIZE_NONE,
            })
    if colors:
        for i, d in enumerate(ret, start=1):
            d.update({
                "tint_color": "#{0}".format(
                    'ff0000' if i == 1 else
                    'ffae55' if i == 2 else
                    'f4ff00' if i == 3 else
                    '00ff16'
                    )
            })
    return dialogs.form_dialog(title, ret) 
    
    
my_fields_dict1 = collections.OrderedDict((
    ('1',      'text'), ('2',     'text'), ('3',      'text'),
    ('4',      'text'), ('5',     'text'), ('6',      'text'),
    ('7',      'text'), ('8',     'text'), ('9',      'text'),
    ('10',     'text'),
    ))


def main():
    d = form_dialog_from_fields_dict("Enter letters (group by turns)", my_fields_dict1) or {}
    argz = d['1'], d['2'], d['3'], d['4'], d['5'], d['6'], d['7'], d['8'], d['9'], d['10'] 
    fmt = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9}".format(*argz)
