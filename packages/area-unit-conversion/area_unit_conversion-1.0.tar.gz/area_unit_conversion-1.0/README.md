# **Area Unit Conversion** [![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)]()

Python module to convert unit of area from one system of units to another.

## **Introduction** 

This package was created for real estate business purposes. The availables units of length are the most commonly used in industry.

**Availables units:**

| Abbrev | Unit "EN"         | Unit "ES"            | value  |
|:------:|:-----------------:|:--------------------:|:------:|
| km²    | Square Kilometers | Kilómetros cuadrados | km2    |
| m²     | Square Meters     | Metros cuadrados     | m2     |
| mi²    | Square Miles      | Millas cuadradas     | mi2    |
| yd²    | Square Yard       | Yardas cuadradas     | yd2    |
| ft²    | Square Feet       | Pies cuadrados       | ft2    |
| in²    | Square Inches     | Pulgadas cuadradas   | in2    |
| ha     | Hectares          | Hectáreas            | ha     |
| ac     | Acres             | Acres                | ac     |

## **Installation**
```
$ pip install area_unit_conversion
```

## **Usage**

### **convert**

Converts unit of area from one system of units to another

| Argument        | Type  | Default  | Description                       |
|:---------------:|:-----:|:--------:|:---------------------------------:|
| from_unit_type  | str   | None     | Original system of unit area      |
| to_unit_type    | str   | None     | Desired system of unit area       |
| value           | float | 0        | Area value to convert             |


```
import area_unit_conversion

area_unit_conversion.convert('m2','ha',10000) 

# Return 1

```

### **get_units_of_length**

Lists available units of length

| Argument | Type  | Default  | Description          |
|:--------:|:-----:|:--------:|:--------------------:|
| lang     | str   | "en"     | iso code of language |

 Options: "es" | "en"

```
import area_unit_conversion

area_unit_conversion.get_units_of_length() 

# Return
[
    {
        'abbreviation': 'km²', 
        'value': 'km2', 
        'name': 'Square Kilometers'
    },{   
        'abbreviation': 'm²', 
        'value': 'm2', 
        'name': 'Square Meters'
    },{
        'abbreviation': 'mi²',
        'value': 'mi2',
        'name': 'Square Miles'
    }, 
    
    etc. , etc.
    }
]

```

## **Test**
Running tests:
```
$ pytest
```

Checking the package installs correctly with different Python versions and interpreters.

Tested with python3.6, python3.7, python3.8, python3.9 and python3.10 versions:
```
$ tox
```

## **Contributing**
Contributions are welcome - submit an issue/pull request.