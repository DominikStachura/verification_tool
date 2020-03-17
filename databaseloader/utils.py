from aptiv.grom.gtrepo.interfaces import ISignsObj


def get_type_and_shape():
    prop = ISignsObj.get('signType')
    line_completer_items = [(term.token, term.title, None) for term in prop.vocabulary.by_token.values()]
    signs_categories = [category[0] for category in line_completer_items]
    signs_shapes = set(prop.categories)
    return signs_categories, signs_shapes

signs_categories, signs_shapes = get_type_and_shape()