# File Validation Decorator
A decorator for validating file types and sizes. If the validation fails, an Exception will be raised and the code will stop before reaching the function you are decorating. A successful validation will execute the function being decorated - business as usual.

![Alt_Text](https://source.unsplash.com/Q9y3LRuuxmg)

---

## Example Of A Successful File Validation
Successful file validations allow the function that is being decorated to execute. **The first parameter defined in your function needs to be the file object.**
```
from file_validation_decorator.file_validation import file_validation

@file_validation(accepted_file_extensions=['txt'], accepted_mime_types=['text/plain'])
def hello(file):
    print('Hello World!')

with open('test.txt', 'r') as file:
    hello(file)
```

## Example Of A File That Is Too Large In Size
The decorator is provided a file size of .000001 and will raise a FileSizeExceeded error.
```
from file_validation_decorator.file_validation import file_validation

@file_validation(accepted_file_extensions=['txt'], max_file_size=.000001)
def hello(file):
    print('Hello World!')

with open('test.txt', 'r') as file:
    hello(file)
```

## Example Of A File Extension That Is Not Allowed
The example file being uploaded here is a .txt but a text file is not provided in the accepted file extensions list. This will raise a FileTypeNotAllowed error. 

```
from file_validation_decorator.file_validation import file_validation

@file_validation(accepted_file_extensions=['jpeg'])
def hello(file):
    print('Hello World!')

with open('test.txt', 'r') as file:
    hello(file)
```

## Exceptions 

- **FileExtensionNotAllowed** - *Raised when the file's extension is not found in the list of accepted_file_extensions*


- **FileTypeNotAllowed** - *Raised when the file's type is not found in the list of accepted_file_types*


- **FileMimeTypeNotAllowed** - *Raised when the file's mime type is not found in the list of accepted_mime_types*


- **FileSizeExceeded** - *Raised when the file's size is larger than the max_file_size* 
