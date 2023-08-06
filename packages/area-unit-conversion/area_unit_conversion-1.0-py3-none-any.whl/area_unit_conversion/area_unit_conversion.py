""" Module to convert unit of area from one system of units to another """

# Units of length
TYPES = {
    'km2':
    {
        'name_en': 'Square Kilometers',
        'name_es': 'Kilómetros cuadrados',
        'abbreviation': 'km²',
        'value': 'km2',
        'to_m2': 1000000
    },
    'm2':
    {
        'name_en': 'Square Meters',
        'name_es': 'Metros cuadrados',
        'abbreviation': 'm²',
        'value': 'm2',
        'to_m2': 1
    },
    'mi2':
    {
        'name_en': 'Square Miles',
        'name_es': 'Millas cuadradas',
        'abbreviation': 'mi²',
        'value': 'mi2',
        'to_m2': 2590000
    },
    'yd2':
    {
        'name_en': 'Square Yards',
        'name_es': 'Yardas cuadradas',
        'abbreviation': 'yd²',
        'value': 'yd2',
        'to_m2': 0.83613119866071
    },
    'ft2':
    {
        'name_en': 'Square Feet',
        'name_es': 'Pies cuadrados',
        'abbreviation': 'ft²',
        'value': 'ft2',
        'to_m2': 0.09290346651785666432
    },
    'in2':
    {
        'name_en': 'Square Inches',
        'name_es': 'Pulgadas cuadradas',
        'abbreviation': 'in²',
        'value': 'in2',
        'to_m2': 0.00064516296192956010865
    },
    'ha':
    {
        'name_en': 'Hectares',
        'name_es': 'Hectáreas',
        'abbreviation': 'ha',
        'value': 'ha',
        'to_m2': 10000
    },
    'ac':
    {
        'name_en': 'Acres',
        'name_es': 'Acres',
        'abbreviation': 'ac',
        'value': 'ac',
        'to_m2': 4046.8750015178361537
    },
}


def __get_unit_of_length_by_key(key: str) -> dict:
    return TYPES.get(key)


def convert(from_unit_type: str = None, to_unit_type: str = None, value: float = 0) -> float:

    from_unit = __get_unit_of_length_by_key(from_unit_type)
    to_unit = __get_unit_of_length_by_key(to_unit_type)

    # Always transform to square meters
    to_m2 = value * from_unit['to_m2']
    # Convert to_unit_type
    result = to_m2 / to_unit['to_m2']

    # text = f'{value} {from_unit["abbreviation"]} are {result:.10f} {to_unit["abbreviation"]}'
    # print(text)
    return result


def get_units_of_length(lang: str = 'en') -> list:
    """
    Lists available units of length

    Args:
        lang (str, optional): iso code of language for list units of area . Defaults to 'en'.
        options: "es" | "en"
    Returns:
        list: A list with dictionaries units of area
    """
    units_of_length = []

    for unit in TYPES:

        unit_type = __get_unit_of_length_by_key(unit)
        del unit_type['to_m2']

        if lang == 'es':

            del unit_type['name_en']
            name = unit_type['name_es']
            del unit_type['name_es']
            unit_type['name'] = name

        else:

            del unit_type['name_es']
            name = unit_type['name_en']
            del unit_type['name_en']
            unit_type['name'] = name

        units_of_length.append(unit_type)

    return units_of_length
