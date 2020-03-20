from aptiv.grom.gtrepo.interfaces import ISignsObj


def get_type_and_shape():
    prop = ISignsObj.get('signType')
    line_completer_items = [(term.token, term.title, None) for term in prop.vocabulary.by_token.values()]
    signs_categories = [category[0] for category in line_completer_items]
    signs_icons = []
    # signs_icons = [icon.decode() for icon in prop.icons['signs/triangular/']]
    for icon in prop.icons['signs/triangular/']:
        if icon is None:
            signs_icons.append('None')
        else:
            signs_icons.append(icon.decode())
    signs_shapes = set(prop.categories)
    return signs_categories, signs_shapes, signs_icons
