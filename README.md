# singlemerge
A small python script to merge multiple lines of a single file using a key field

## Getting Started

This project provides a simple and portable python script which can be used to merge the lines of a single file
by using a key field


### Prerequisites

Python 3 installation


### Installing

Just copy the file simpleMail.py to your preferred working directory and call it with their Python 3 interpreter

```
cp src/simpleMail.py YOUR_DIRECTORY
```

### Execution

```
python simpleMail.py [ARGS]
```

Where the arguments are:
```
required arguments:
  -t SEPARATOR, --separator SEPARATOR
                        The field separator for input/output file
                        
  -i FILE, --input FILE
                        The input file to be processed
                        
  -k FIELD_NUM, --key-field FIELD_NUM
                        The field num to be used as merging key
                        
optional arguments:

  -o FILE, --output FILE
                        The output file to be generated.
                        
  -m [FIELD ...], --merge-field [FIELD ...]
                        List of fields concatenate
                        
  -f SEPARATOR, --merge-separator SEPARATOR
                        The separator for concatenated lines
                        
  -v FIELD STRING, --sum-value FIELD STRING
                        The field to concatenate
                        
  -s true|false, --skip-header true|false
                        true to skip the first line of the file, false otherwise. Default = "false"

  -h, --help            show thes help message and exit
```

It's important to note that the input file must be sorted in the key field before using this script, otherwise it will not work correctly.


#### Examples

Suppose you have a file named "input.txt" with the following content:
```
0,cat,cake
0,dog,bread
0,elephant,cookie
1,rocket,sky
1,planet,earth
2,audio,book
```

Then, by executing the following command:
```
python src/singlemerge.py -i ~/test -t , -k 1 -m 2 3 -f -
```

It will produce the following output:
```
0,cat-dog-elephant,cake-bread-cookie
1,rocket-planet,sky-earth
2,audio,book
```

The provided command informed the script to separate the fields by comma, look at the first field for key and merge the content of fields 2 and 3 with dash

It's possible to execute the script without merging all fields:
```
python src/singlemerge.py -i ~/test -t , -k 1 -m 3 -f -
```

In this case, the program will just merge the field 3 and keep the last line of field 2, producing the result below:
```
0,elephant,cake-bread-cookie
1,planet,sky-earth
2,audio,book
```


## Authors

* **Jonathan Gangi** - *Initial work* - [JAVGan](https://github.com/JAVGan/)


## License

This project is licensed under the GNU LESSER GENERAL PUBLIC LICENSE v2.1 - see the [LICENSE](LICENSE) file for details



