# File Validation Decorator
A decorator for validating file types and sizes. If the validation fails, an Exception will be raised and the code will stop before reaching the function you are decorating. A successful validation will execute the function being decorated - business as usual.

![Alt_Text](https://source.unsplash.com/Q9y3LRuuxmg)

---

## Example Of A Successful File Validation
```
from file_validation_decorator.file_validation import file_validation

with open('places_to_go.txt') as file:
    @file_validation(file, ['txt', 'jpeg'], 10)
    def test():
        print('it works')

    test()
```

## Example Of A File That Is Too Large In Size
The decorator is provided a file size of 0 below and will raise a FileSizeExceeded error.
```
from file_validation_decorator.file_validation import file_validation

with open('places_to_go.txt') as file:
    @file_validation(file, ['txt', 'jpeg'], 0)
    def test():
        print('it works')

    test()
```

## Example Of A File Extension That Is Not Allowed
The example file being uploaded here is a .txt but a text file is not provided in the accepted file extensions list. This will raise a FileTypeNotAllowed error. 

```
from file_validation_decorator.file_validation import file_validation

with open('places_to_go.txt') as file:
    @file_validation(file, ['jpeg'], 0)
    def test():
        print('it works')

    test()
```