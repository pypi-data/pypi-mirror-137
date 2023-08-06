# Coscine Python SDK

![Coscine](data/logo.png)

[Coscine](https://coscine.rwth-aachen.de/) is an integration platform for
research data hosted at RWTH Aachen University.  
For more information about Coscine visit the official [Landing Page](https://coscine.de/).

## About

This python3.x package provides an SDK for interfacing with Coscine. It is maintained and
developed by the community and should not be regarded as an official service of RWTH Aachen.
You can use the package to integrate Coscine in your python applications and easily:
- create, edit or delete projects and resources
- invite and manage project members
- upload and download files, resources and projects
- manage your metadata

Even if you plan on using the API directly in a programming language of your choice,
you might want to take a look at this module as it provides you with a handy
debug mode which logs all requests and responses made in the communication with coscine.
This makes it simple to understand how certain workflows should be implemented or why
something in your implementation might not work.

## Showcase

Here is a sneak peek of what the module is able to do.

```python
import coscine

token: str = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
client = coscine.Client(token)

project = client.project("My Project")
print(project.name)
print(project.id)

resource = project.resource("My Project Resource")
print(resource.name)
print(resource.pid)

resource.download(path="./datascience/")

files = resource.objects()
for file in files:
	print(file.name)
```

## Documentation

Documentation and installation instructions can be found in the 
[src/examples](./src/examples) directory. The sourcecode has been thoroughly documented
with python DOCstrings.

## Contact

To report bugs, request features or resolve questions open an issue inside
of the current git repository.

To contribute code and help improve this package fork the repository and
open a merge request.

## License

This project is Open Source Software and licensed
under the terms of the MIT License.
```
The MIT License (MIT)
Copyright © 2018-2021 RWTH Aachen University

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```