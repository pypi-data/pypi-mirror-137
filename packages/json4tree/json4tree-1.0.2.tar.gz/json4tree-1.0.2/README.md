# json4tree
Makes any JSON compatible with [D3's hierarchy or tree chart formats](https://d3js.org).

## Installation
Since this tool is exclusively `Python3`, you'll need `pip3` to install:
```
pip3 install json4tree
```
You can also download and install the package directly from [PyPi](https://pypi.org/project/json4tree/).
## Usage
If your `Python3` library is included in your path, try running `json4tree` directly from the command line:

```bash
# if you have your Python3 scripts added to your path, use this one:
json4tree input.json output.json

# otherwise, use this one:
python3 -m json4tree input.json output.json
```
If you need to import it as a module in your `Python3` script, do it [like so](https://raw.githubusercontent.com/robertjamison/json4tree/main/samples/example.py):
```python
# import the necessary modules
import json
import json4tree

# import your JSON data
infile = open("input.json", "r")
json_file = json.load(infile)
infile.close()

# create a new handler
converter = json4tree.handler(json_file)

# You can either print your results...
converter.results

# Or you can save your results
outfile = open("output.json", "w")
outfile.write(converter.results)
outfile.close()
```
## Examples
Here is an example [input file](https://raw.githubusercontent.com/robertjamison/json4tree/main/samples/input.json) from [Merriam-Webster's Dictionary API](https://www.dictionaryapi.com/products/json) and the resulting [output file](https://raw.githubusercontent.com/robertjamison/json4tree/main/samples/output.json).
