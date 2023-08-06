# HIRO Batch Client

This is a client library to access data of the HIRO Graph. It is meant for uploads of huge
batches of data in parallel.

This library depends on the package "hiro-graph-client". - (PyPI: [hiro-graph-client](https://pypi.org/project/hiro-graph-client/), GitHub: [hiro-client-python](https://github.com/arago/hiro-client-python)) 

For more information about HIRO Automation, look at https://www.arago.co/

## Quickstart

To use this library, you will need an account at https://id.arago.co/ and access to an OAuth Client-Id and Client-Secret
to access the HIRO Graph. See also https://developer.hiro.arago.co.

Most of the documentation is done in the sourcecode.

### HiroGraphBatch Examples

#### Example 1

Example to use the batch client to process a batch of requests:

```python
from hiro_graph_client import PasswordAuthTokenApiHandler
from hiro_batch_client import HiroGraphBatch

hiro_batch_client: HiroGraphBatch = HiroGraphBatch(
    api_handler=PasswordAuthTokenApiHandler(
        root_url="https://core.arago.co",
        username='',
        password='',
        client_id='',
        client_secret=''
    )
)

# See code documentation about the possible commands and their attributes.
# For another variant of a valid data structure, see the example below.
commands: list = [
    {
        "handle_vertices": {
            "ogit/_xid": "haas1000:connector1:machine1"
        }
    },
    {
        "handle_vertices": {
            "ogit/_xid": "haas1000:connector2:machine2"
        }
    }
]

query_results: list = hiro_batch_client.multi_command(commands)

print(query_results)
```

#### Example 2

Example to use the batch client to process a batch of requests with callbacks for each result:

```python
from typing import Any, Iterator

from hiro_graph_client import AbstractTokenApiHandler, PasswordAuthTokenApiHandler
from hiro_batch_client import HiroGraphBatch, HiroResultCallback


class RunBatch(HiroResultCallback):
    hiro_batch_client: HiroGraphBatch

    def __init__(self, api_handler: AbstractTokenApiHandler):
        self.hiro_batch_client = HiroGraphBatch(
            callback=self,
            api_handler=api_handler)

    def result(self, data: Any, code: int) -> None:
        """
        This (abstract) method gets called for each command when results are available
        """
        print('Data: ' + str(data))
        print('Code: ' + str(code))

    def run(self, command_iter: Iterator[dict]):
        self.hiro_batch_client.multi_command(command_iter)


batch_runner: RunBatch = RunBatch(
    api_handler=PasswordAuthTokenApiHandler(
        root_url="https://core.arago.co",
        username='',
        password='',
        client_id='',
        client_secret=''
    )
)

# See code documentation about the possible commands and their attributes. This is a more compact notation of the
# same list of commands from the example above. Both variants are allowed.
commands: list = [
    {
        "handle_vertices": [
            {
                "ogit/_xid": "haas1000:connector1:machine1"
            },
            {
                "ogit/_xid": "haas1000:connector2:machine2"
            }
        ]
    }
]

batch_runner.run(commands)
```

## TokenApiHandler

See documentation for the [hiro-graph-client](https://pypi.org/project/hiro-graph-client/). The TokenApiHandlers are
used in exactly the same way here.

Example:

```python
from hiro_graph_client import EnvironmentTokenApiHandler
from hiro_batch_client import HiroGraphBatch

hiro_batch_client: HiroGraphBatch = HiroGraphBatch(
    api_handler=EnvironmentTokenApiHandler(
        root_url="https://core.arago.co"
    )
)

```

## Batch Client "HiroGraphBatch"

It is recommended to use the included HiroGraphBatch client when uploading large quantities of data into the HIRO Graph.
This client handles parallel upload of data and makes creating vertices with their edges and attachments easier.

The HiroGraphBatch expects a list of commands with their respective attribute payload as input. The method to run such a
batch is always `HiroGraphBatch.multi_command`.

See examples from [HiroGraphBatch](#hirographbatch) above.

### Input data format

The data format for input of `HiroGraphBatch.multi_command` is a list. This method iterates over this list and treats
each dict it finds as a key-value-pair with the name of a command as key and either a single dict of attributes, or a
list of multiple attribute dicts as value(s) for this command.

These commands are run in parallel across up to eight threads by default, so their order is likely to change in the
results. Commands given in these command lists should therefore never depend on each other. See the documentation on the
constructor `HiroGraphBatch.__init__` for more information.

The following two (bad!) examples are equivalent:

```python
commands: list = [
    {
        "create_vertices": {
            "ogit/_xid": "haas1000:connector1:machine1"
        }
    },
    {
        "handle_vertices": {
            "ogit/_xid": "haas1000:connector2:machine2"
        }
    },
    {
        "handle_vertices": {
            "ogit/_xid": "haas1000:connector3:machine3"
        }
    },
    {
        "delete_vertices": {
            "ogit/_xid": "haas1000:connector1:machine1"
        }
    },
    {
        "delete_vertices": {
            "ogit/_xid": "haas1000:connector2:machine2"
        }
    },
    {
        "delete_vertices": {
            "ogit/_xid": "haas1000:connector3:machine3"
        }
    }
]
```

```python
commands: list = [
    {
        "create_vertices": [
            {
                "ogit/_xid": "haas1000:connector1:machine1"
            }
        ],
        "handle_vertices": [
            {
                "ogit/_xid": "haas1000:connector2:machine2"
            },
            {
                "ogit/_xid": "haas1000:connector3:machine3"
            }
        ],
        "delete_vertices": [
            {
                "ogit/_xid": "haas1000:connector1:machine1"
            },
            {
                "ogit/_xid": "haas1000:connector2:machine2"
            },
            {
                "ogit/_xid": "haas1000:connector3:machine3"
            }
        ]
    }
]
```

These examples are bad, because delete_vertices depends on create/handle_vertices (there has to be a vertex first before
it can be deleted). You should call `HiroGraphBatch.multi_command` twice in this case:

```python
commands1: list = [
    {
        "create_vertices": [
            {
                "ogit/_xid": "haas1000:connector1:machine1"
            }
        ],
        "handle_vertices": [
            {
                "ogit/_xid": "haas1000:connector2:machine2"
            },
            {
                "ogit/_xid": "haas1000:connector3:machine3"
            }
        ]
    }
]

commands2: list = [
    {
        "delete_vertices": [
            {
                "ogit/_xid": "haas1000:connector1:machine1"
            },
            {
                "ogit/_xid": "haas1000:connector2:machine2"
            },
            {
                "ogit/_xid": "haas1000:connector3:machine3"
            }
        ]
    }
]

query_results = []

query_results.extend(hiro_batch_client.multi_command(commands1))
query_results.extend(hiro_batch_client.multi_command(commands2))
```

#### IOCarrier

When uploading attachments into the HIRO Graph, it is best practice streaming that data when possible. To avoid having
many open IO connections when uploading many files for instance, children of the class `AbstractIOCarrier` can be
implemented and used. Children that derive from this class open their IO just before the upload and close it immediately
afterwards.

This library provides a class `BasicFileIOCarrier` for file operations.

See [Example for add_attachments](#add_attachments).

### Result data format

Result values contain dicts that carry all information about the executed commands. The order of the results is
independent of the order in which the input data has been submitted.

One dict has the following structure:

```python
result: dict = {
    "status": "success|fail",
    "entity": "vertex|edge|timeseries|attachment|undefined",
    "action": "create|update|delete|undefined",
    "order": 0  # order of the commands in which they were sent to the graph. 
    "data": {
        "<On success>": "<Data of the result of the command.>",
        "<On fail>": "<Dict with a copy of the original data of the command.>"
    }
}
```

These dicts are collected in a list when no callback is configured, see [Example 1](#example-1), or given back in the
callback method as `data`, see [Example 2](#example-2).

Example of a list result:

```python
query_results: list = [
    {
        "status": "success",
        "entity": "vertex",
        "action": "create",
        "order": 0,
        "data": {
            "ogit/_created-on": 1601030883647,
            "ogit/_xid": "machine4",
            "ogit/_organization": "ckeckyxi60c8k0619otx9i5tq_ckeckyxi60c8o0619fsizblds",
            "/admin_contact": "info@admin.co",
            "ogit/name": "machine 4",
            "ogit/_modified-on": 1601030883647,
            "ogit/_id": "ckeckz5un0chl0619fyskvn2a_ckfi4g85b8vak06191dxpaqn0",
            "ogit/_creator": "ckeckyxi60c8k0619otx9i5tq_ckeckzivg0d2f0619o3guv8o1",
            "ogit/MARS/Machine/class": "Linux",
            "ogit/_graphtype": "vertex",
            "ogit/_owner": "ckeckyxi60c8k0619otx9i5tq_ckeckyxi60c8m061999q77xdb",
            "ogit/_v-id": "1601030883647-9oRXX8",
            "ogit/_v": 1,
            "ogit/MARS/Machine/ram": "2G",
            "ogit/_modified-by-app": "cju16o7cf0000mz77pbwbhl3q_ckecksfda040q06190ygwv4jz",
            "ogit/_is-deleted": false,
            "ogit/_creator-app": "cju16o7cf0000mz77pbwbhl3q_ckecksfda040q06190ygwv4jz",
            "ogit/_modified-by": "ckeckyxi60c8k0619otx9i5tq_ckeckzivg0d2f0619o3guv8o1",
            "ogit/_scope": "ckeckyxi60c8k0619otx9i5tq_ckeckz5un0chl0619fyskvn2a",
            "ogit/_type": "ogit/MARS/Machine"
        }
    },
    {
        "status": "success",
        "entity": "vertex",
        "action": "create",
        "order": 1,
        "data": {
            "ogit/_created-on": 1601030883847,
            "ogit/_xid": "machine5",
            "ogit/_organization": "ckeckyxi60c8k0619otx9i5tq_ckeckyxi60c8o0619fsizblds",
            "/admin_contact": "contact@admin.co",
            "ogit/name": "machine 5",
            "ogit/_modified-on": 1601030883847,
            "ogit/_id": "ckeckz5un0chl0619fyskvn2a_ckfi4g8av8vap0619okulfydq",
            "ogit/_creator": "ckeckyxi60c8k0619otx9i5tq_ckeckzivg0d2f0619o3guv8o1",
            "ogit/MARS/Machine/class": "Linux",
            "ogit/_graphtype": "vertex",
            "ogit/_owner": "ckeckyxi60c8k0619otx9i5tq_ckeckyxi60c8m061999q77xdb",
            "ogit/_v-id": "1601030883847-3TyBFf",
            "ogit/_v": 1,
            "ogit/MARS/Machine/ram": "4G",
            "ogit/_modified-by-app": "cju16o7cf0000mz77pbwbhl3q_ckecksfda040q06190ygwv4jz",
            "ogit/_is-deleted": false,
            "ogit/_creator-app": "cju16o7cf0000mz77pbwbhl3q_ckecksfda040q06190ygwv4jz",
            "ogit/_modified-by": "ckeckyxi60c8k0619otx9i5tq_ckeckzivg0d2f0619o3guv8o1",
            "ogit/_scope": "ckeckyxi60c8k0619otx9i5tq_ckeckz5un0chl0619fyskvn2a",
            "ogit/_type": "ogit/MARS/Machine"
        }
    },
    {
        "status": "fail",
        "entity": "vertex",
        "action": "create",
        "order": 2,
        "data": {
            "error": "HTTPError",
            "code": 500,
            "message": "500 Internal Server Error: Unspecified exception.",
            "original_data": {
                "ogit/_xid": "machine6",
                "ogit/_type": "ogit/MARS/Machine",
                "ogit/MARS/Machine/class": "Linux",
                "ogit/name": "machine 5A",
                "ogit/MARS/Machine/ram": "8G",
                "/admin_contact": "info@admin.co"
            }
        }
    },
    {
        "status": "fail",
        "entity": "vertex",
        "action": "create",
        "order": 3,
        "data": {
            "error": "HTTPError",
            "code": 500,
            "message": "500 Internal Server Error: Unspecified exception.",
            "original_data": {
                "ogit/_xid": "machine7",
                "ogit/_type": "ogit/MARS/Machine",
                "ogit/MARS/Machine/class": "Linux",
                "ogit/name": "machine 4A",
                "ogit/MARS/Machine/ram": "4G",
                "/admin_contact": "contact@admin.co"
            }
        }
    }
]
```

### Commands

The following command keywords for the commands list structure are implemented in the HiroGraphBatch client:

---

#### create_vertices

Create a batch of vertices via
https://core.arago.co/help/specs/?url=definitions/graph.yaml#/[Graph]_Entity/post_new__type_

* `ogit/_type` must be present in each of the attribute dicts.

* Attribute keys that start with `=`, `+` or `-` denote map value entries. These values have to be in the correct format
  according to https://developer.hiro.arago.co/7.0/documentation/api/list-api/.

* Attributes of the format `"xid:[attribute_name]": "[ogit/_xid]"` are resolved to `"[attribute_name]": "[ogit/_id]"` by
  querying HIRO before executing the main command.

  This can be especially handy when creating issues:

  An attribute in the form `"xid:ogit/Automation/originNode": "ogit:xid:of:the:desired:vertex"` would resolve this
  attribute to `"ogit/Automation/originNode": "ogitidofthedesiredvertex1_abcdefghijklmnopqrstuvw12"` in the issue vertex
  to create.

Example payload for four new vertices:

```python
commands: list = [
    {
        "create_vertices": [
            {
                "ogit/_xid": "machine4",
                "ogit/_type": "ogit/MARS/Machine",
                "ogit/MARS/Machine/class": "Linux",
                "ogit/name": "machine 4",
                "ogit/MARS/Machine/ram": "2G",
                "/admin_contact": "info@admin.co"
            },
            {
                "ogit/_xid": "machine5",
                "ogit/_type": "ogit/MARS/Machine",
                "ogit/MARS/Machine/class": "Linux",
                "ogit/name": "machine 5",
                "ogit/MARS/Machine/ram": "4G",
                "/admin_contact": "contact@admin.co"
            },
            {
                "ogit/_xid": "machine6",
                "ogit/_type": "ogit/MARS/Machine",
                "ogit/MARS/Machine/class": "Linux",
                "ogit/name": "machine 5A",
                "ogit/MARS/Machine/ram": "8G",
                "/admin_contact": "info@admin.co"
            },
            {
                "ogit/_xid": "machine7",
                "ogit/_type": "ogit/MARS/Machine",
                "ogit/MARS/Machine/class": "Linux",
                "ogit/name": "machine 4A",
                "ogit/MARS/Machine/ram": "4G",
                "/admin_contact": "contact@admin.co"
            }
        ]
    }
]
```

---

#### update_vertices

Update a batch of vertices via
https://core.arago.co/help/specs/?url=definitions/graph.yaml#/[Graph]_Entity/post__id_

* Either `ogit/_id` or `ogit/_xid` must be present in each of the attribute dicts.

* Attribute keys that start with `=`, `+` or `-` denote map value entries. These values have to be in the correct format
  according to https://developer.hiro.arago.co/7.0/documentation/api/list-api/.

* Attributes of the format `"xid:[attribute_name]": "[ogit/_xid]"` are resolved to `"[attribute_name]": "[ogit/_id]"` by
  querying HIRO before executing the main command.

Example payload to update four vertices:

```python
commands: list = [
    {
        "update_vertices": [
            {
                "ogit/_xid": "machine4",
                "ogit/name": "machine one",
                "ogit/MARS/Machine/ram": "4G"
            },
            {
                "ogit/_xid": "machine5",
                "ogit/name": "machine two",
                "ogit/MARS/Machine/ram": "16G"
            },
            {
                "ogit/_xid": "machine6",
                "ogit/name": "machine three",
                "ogit/MARS/Machine/ram": "16G",
                "/admin_contact": None
            },
            {
                "ogit/_id": "cju16o7cf0000mz77pbwbhf8d_ckm1z9o2m08km0781s2s7abce",
                "ogit/MARS/Machine/class": "Linux",
                "ogit/name": "machine three backup",
                "ogit/MARS/Machine/ram": "8G"
            }
        ]
    }
]
```

`"/admin_contact": None` from above would remove this attribute from the found vertex.

---

#### handle_vertices

Create or update a batch of vertices depending on the data provided in their attributes.

If the attributes for a vertex definition contain `ogit/_id` or `ogit/_xid`, an existing vertex will be updated when it
can be found. If these attributes are missing or no such vertex can be found but `ogit/_type` is given, a new vertex of
this type will be created.

The data structures are the same as in [create_vertices](#create_vertices) and [update_vertices](#update_vertices)
above.

Example:

```python
commands: list = [
    {
        "handle_vertices": [
            {
                "ogit/_xid": "machine4",
                "ogit/name": "machine one",
                "ogit/MARS/Machine/ram": "4G"
            },
            {
                "ogit/_xid": "machine5",
                "ogit/_type": "ogit/MARS/Machine",
                "ogit/name": "machine two",
                "ogit/MARS/Machine/ram": "16G"
            },
            {
                "ogit/_xid": "machine6",
                "ogit/name": "machine three",
                "ogit/MARS/Machine/ram": "16G",
                "/admin_contact": None
            },
            {
                "ogit/_id": "cju16o7cf0000mz77pbwbhf8d_ckm1z9o2m08km0781s2s7abce",
                "ogit/MARS/Machine/class": "Linux",
                "ogit/name": "machine three backup",
                "ogit/MARS/Machine/ram": "8G"
            }
        ]
    }
]
```

`"/admin_contact": None` from above would remove this attribute from the found vertex.

---

#### handle_vertices_combined

Same as [handle_vertices](#handle_vertices) above, but also collect additional information about edge connections,
timeseries, data attachments and linked automation issues that might be given in their attributes.

The execution of this command has two stages:

1) Use the vertex attributes and execute [handle_vertices](#handle_vertices) on _all_ vertices given, ignoring all
   attributes that start with `_`. Store the `ogit/_id`s of the handled vertices for stage two.
2) When stage one is finished, take those remaining attributes, reformat them if necessary and
   execute [create_edges](#create_edges),   [add_timeseries](#add_timeseries), [add_attachments](#add_attachments) or,
   for the automation issues, [handle_vertices](#handle_vertices)
   with them, using the `ogit/_id`s of the associated vertices from stage one.

Each stage executes its activities in parallel, so what has been written about dependencies
at [Input Data Format](#input-data-format) still applies for each stage.

The following additional attributes are supported:

`_edge_data`:

* Edge attributes are given as a list with a key `_edge_data`. This list contains dicts with the following attributes:
    * `verb`: (required) Verb for that edge for the vertex of the current row.
    * `direction`: ("in"/"out") from the view of the current vertex. "in" points towards, "out"
      points away from the current vertex. Default is "out" if this key is missing.
    * One of the following keys is required to find the vertex to connect to:
        * `vertex_id`: ogit/_id of the other vertex.
        * `vertex_xid`: ogit/_xid of the other vertex.

  See also [create_edges](#create_edges), but take note, that the structure of `_edge_data` is reformatted internally to
  match the data needed for create_edges.

Example for edge data:

```python
commands: list = [
    {
        "handle_vertices_combined": [
            {
                "ogit/_xid": "crew:NCC-1701-D:picard",
                "ogit/_type": "ogit/Forum/Profile",
                "ogit/name": "Jean-Luc Picard",
                "ogit/Forum/username": "Picard",
                "_edge_data": [
                    {
                        "verb": "ogit/Forum/mentions",
                        "direction": "out",
                        "vertex_xid": "crew:NCC-1701-D:data"
                    },
                    {
                        "verb": "ogit/Forum/mentions",
                        "direction": "out",
                        "vertex_xid": "crew:NCC-1701-D:worf"
                    }
                ]
            },
            {
                "ogit/_xid": "crew:NCC-1701-D:worf",
                "ogit/_type": "ogit/Forum/Profile",
                "ogit/name": "Worf",
                "ogit/Forum/username": "Worf",
                "_edge_data": [
                    {
                        "verb": "ogit/subscribes",
                        "direction": "out",
                        "vertex_xid": "crew:NCC-1701-D:picard"
                    }
                ]
            },
            {
                "ogit/_xid": "crew:NCC-1701-D:data",
                "ogit/_type": "ogit/Forum/Profile",
                "ogit/name": "Data",
                "ogit/Forum/username": "Data",
                "_edge_data": [
                    {
                        "verb": "ogit/Forum/mentions",
                        "direction": "out",
                        "vertex_xid": "crew:NCC-1701-D:worf"
                    },
                    {
                        "verb": "ogit/subscribes",
                        "direction": "in",
                        "vertex_xid": "crew:NCC-1701-D:worf"
                    }
                ]
            }
        ]
    }
]
```

`_timeseries_data`:

* Timeseries attributes are given as a list with a key `_timeseries_data`. This list contains dicts of
    * `timestamp` for epoch in ms.
    * `value` for the timeseries value.

  See also [add_timeseries](#add_timeseries), but take note, that the key of the list is called just `items` there.

Example for timeseries data:

```python
commands: list = [
    {
        "handle_vertices_combined": [
            {
                "ogit/_xid": "crew:NCC-1701-D:picard",
                "ogit/_type": "ogit/Forum/Profile",
                "ogit/name": "Jean-Luc Picard",
                "ogit/Forum/username": "Picard",
                "_timeseries_data": [
                    {
                        "timestamp": "1440035678000",
                        "value": "Sighs"
                    },
                    {
                        "timestamp": "1440035944000",
                        "value": "Make it so!"
                    }
                ]
            },
            {
                "ogit/_xid": "crew:NCC-1701-D:worf",
                "ogit/_type": "ogit/Forum/Profile",
                "ogit/name": "Worf",
                "ogit/Forum/username": "Worf",
                "_timeseries_data": [
                    {
                        "timestamp": "1440035678000",
                        "value": "Grunts"
                    },
                    {
                        "timestamp": "1440035944000",
                        "value": "Aye captain"
                    }
                ]
            }
        ]
    }
]
```

`_content_data`:

* Content attributes are given as a dict with a key `_content_data` which contains:
    * `data`: Content to upload. This can be anything the Python library `requests` supports as attribute `data=`
      in  `requests.post(data=...)`. If you set an IO object as data, it will be streamed. Also take a look at the
      class `AbstractIOCarrier` to transparently handle opening and closing of IO sources - see [IOCarrier](#iocarrier).
    * `mimetype`: (optional) Content-Type of the content.

  See also [add_attachments](#add_attachments)

Example for content/attachment data:

```python
commands: list = [
    {
        "handle_vertices_combined": [
            {
                "ogit/_xid": "attachment:arago:test:0:lorem-ipsum",
                "ogit/_type": "ogit/Attachment",
                "ogit/name": "test text",
                "ogit/type": "text",
                "_content_data": {
                    "mimetype": "text/plain",
                    "data": "Auch gibt es niemanden, der den Schmerz an sich liebt, sucht oder wünscht, nur, weil er Schmerz ist, es sei denn, es kommt zu zufälligen Umständen, in denen Mühen und Schmerz ihm große Freude bereiten können.\n\nUm ein triviales Beispiel zu nehmen, wer von uns unterzieht sich je anstrengender körperlicher Betätigung, außer um Vorteile daraus zu ziehen? Aber wer hat irgend ein Recht, einen Menschen zu tadeln, der die Entscheidung trifft, eine Freude zu genießen, die keine unangenehmen Folgen hat, oder einen, der Schmerz vermeidet, welcher keine daraus resultierende Freude nach sich zieht? Auch gibt es niemanden, der den Schmerz"
                }
            },
            {
                "ogit/_xid": "attachment:arago:test:1:lorem-ipsum",
                "ogit/_type": "ogit/Attachment",
                "ogit/name": "text text from IO",
                "ogit/type": "text",
                "_content_data": {
                    "mimetype": "text/plain",
                    "data": BasicFileIOCarrier('<filename>')
                }
            }
        ]
    }
]
```

`_issue_data`:

* Connected issues are given as a dict or a list of dicts using the key `_issue_data` which contains the attributes for
  one or more `ogit/Automation/AutomationIssue`. Attributes of the issue can be set freely inside `_issue_data` (
  i.e. `ogit/_scope`, `ogit/_owner` or process variables like `/ProcessIssue` etc.).
    * The following attributes will always be set, overwriting any other values given:
        * `ogit/_type`: Will be set automatically to `ogit/Automation/AutomationIssue`.
        * `ogit/Automation/originNode`: Will be set to the `ogit/_id` of the vertex that has been created in stage 1).

  __Note__

  This method is meant as a convenience to create `ogit/Automation/AutomationIssue` linked to the vertex created just
  before in stage 1). If you want to connect the `ogit/Automation/AutomationIssue` to another vertex, create the issues
  as vertices on their own and do not use `handle_vertices_combined` but `create_vertices` for them. To find
  the `ogit/Automation/originNode` of a vertex with an unknown `ogit/_id`, you can use the attribute
  key `xid:ogit/Automation/originNode` to find the vertex via its `ogit/_xid`. See [create_vertices](#create_vertices)
  for more information about that special key.

See also [create_vertices](#create_vertices)

Example for issue data:

```python
commands: list = [
    {
        "handle_vertices_combined": [
            {
                "ogit/_xid": "crew:NCC-1701-D:picard",
                "ogit/_type": "ogit/Forum/Profile",
                "ogit/name": "Jean-Luc Picard",
                "ogit/Forum/username": "Picard",
                "_issue_data": {
                    "ogit/subject": "Handle Worf.",
                    "/ProcessIssue": "processme"
                }
            },
            {
                "ogit/_xid": "crew:NCC-1701-D:worf",
                "ogit/_type": "ogit/Forum/Profile",
                "ogit/name": "Worf",
                "ogit/Forum/username": "Worf",
                "_issue_data": [
                    {
                        "ogit/subject": "Listen to Picard.",
                        "/ProcessIssue": "processme"
                    },
                    {
                        "ogit/subject": "Obey Picard.",
                        "/ProcessIssue": "processme"
                    }
                ]
            }
        ]
    }
]
```

Any of the special attributes above can be combined into one data structure for this command if needed:

```python
commands: list = [
    {
        "handle_vertices_combined": [
            {
                "<vertex attribute>": "<some value>",
                "_edge_data": {
                },
                "_timeseries_data": {
                },
                "_content_data": {
                }
                "_issue_data": {
                }
            }
        ]
    }
]
```

---

#### delete_vertices

Delete a batch of vertices via
https://core.arago.co/help/specs/?url=definitions/graph.yaml#/[Graph]_Entity/delete__id_

Either `ogit/_id` or `ogit/_xid` must be present in each of the attribute dicts.

Example to delete four vertices:

```python
commands: list = [
    {
        "delete_vertices": [
            {
                "ogit/_xid": "machine4"
            },
            {
                "ogit/_xid": "machine5"
            },
            {
                "ogit/_xid": "machine6"
            },
            {
                "ogit/_id": "cju16o7cf0000mz77pbwbhf8d_ckm1z9o2m08km0781s2s7abce"
            }
        ]
    }
]
```

---

#### create_edges

Connect vertices via
https://core.arago.co/help/specs/?url=definitions/graph.yaml#/[Graph]_Verb/post_connect__type_

Each attribute dict needs the following keys:

* `from:ogit/_id` or `from:ogit/_xid`
* `verb`: The ogit verb for the edge
* `to:ogit/_id` or `to:ogit/_xid`

Example:

```python
commands: list = [
    {
        "create_edges": [
            {
                "from:ogit/_xid": "crew:NCC-1701-D:worf",
                "verb": "ogit/subscribes",
                "to:ogit/_xid": "crew:NCC-1701-D:picard"
            },
            {
                "from:ogit/_xid": "crew:NCC-1701-D:worf",
                "verb": "ogit/subscribes",
                "to:ogit/_xid": "crew:NCC-1701-D:data"
            },
            {
                "from:ogit/_xid": "crew:NCC-1701-D:picard",
                "verb": "ogit/Forum/mentions",
                "to:ogit/_xid": "crew:NCC-1701-D:data"
            },
            {
                "from:ogit/_xid": "crew:NCC-1701-D:picard",
                "verb": "ogit/Forum/mentions",
                "to:ogit/_xid": "crew:NCC-1701-D:worf"
            },
            {
                "from:ogit/_xid": "crew:NCC-1701-D:data",
                "verb": "ogit/Forum/mentions",
                "to:ogit/_xid": "crew:NCC-1701-D:worf"
            }
        ]
    }
]
```

---

#### delete_edges

Delete connections between vertices via
https://core.arago.co/help/specs/?url=definitions/graph.yaml#/[Graph]_Verb/delete__id_

The data structure of the payload is the same as with [create_edges](#create_edges).

Example:

```python
commands: list = [
    {
        "delete_edges": [
            {
                "from:ogit/_xid": "crew:NCC-1701-D:worf",
                "verb": "ogit/subscribes",
                "to:ogit/_xid": "crew:NCC-1701-D:picard"
            },
            {
                "from:ogit/_xid": "crew:NCC-1701-D:worf",
                "verb": "ogit/subscribes",
                "to:ogit/_xid": "crew:NCC-1701-D:data"
            },
            {
                "from:ogit/_xid": "crew:NCC-1701-D:picard",
                "verb": "ogit/Forum/mentions",
                "to:ogit/_xid": "crew:NCC-1701-D:data"
            },
            {
                "from:ogit/_xid": "crew:NCC-1701-D:picard",
                "verb": "ogit/Forum/mentions",
                "to:ogit/_xid": "crew:NCC-1701-D:worf"
            },
            {
                "from:ogit/_xid": "crew:NCC-1701-D:data",
                "verb": "ogit/Forum/mentions",
                "to:ogit/_xid": "crew:NCC-1701-D:worf"
            }
        ]
    }
]
```

---

#### add_timeseries

Add timeseries data to a vertex with "ogit/_type" of "ogit/Timeseries" via
https://core.arago.co/help/specs/?url=definitions/graph.yaml#/[Storage]_Timeseries/post__id__values

Each attribute dict needs the following keys:

* `ogit/_id` or `ogit/_xid` with valid ids for vertices.
* `items` a list of timeseries items for this vertex, containing dicts of:
    * `timestamp` for epoch in ms.
    * `value` for the timeseries value.

Example:

```python
commands: list = [
    {
        "add_timeseries": [
            {
                "ogit/_xid": "machine4",
                "items": [
                    {
                        "timestamp": "1440035678000",
                        "value": "Value 4A"
                    },
                    {
                        "timestamp": "1440035944000",
                        "value": "Value 4B"
                    }
                ]
            },
            {
                "ogit/_xid": "machine5",
                "items": [
                    {
                        "timestamp": "1440035678000",
                        "value": "Value 5A"
                    },
                    {
                        "timestamp": "1440035944000",
                        "value": "Value 5B"
                    }
                ]
            }
        ]
    }
]
```

---

#### add_attachments

Add binary data to a vertex with "ogit/_type" of "ogit/Attachment" by using
https://core.arago.co/help/specs/?url=definitions/graph.yaml#/[Storage]_Blob/post__id__content

* `ogit/_id`or `ogit/_xid`
* `_content_data`: A dict with the following keys:
    * `data`: Content to upload. This can be anything the Python library `requests` supports as attribute `data=`
      in  `requests.post(data=...)`. If you set an IO object as data, it will be streamed. Also take a look at the
      class `AbstractIOCarrier` to transparently handle opening and closing of IO sources - see [IOCarrier](#iocarrier).
    * `mimetype`: (optional) Content-Type of the content.

Example:

```python
commands: list = [
    {
        "add_attachments": [
            {
                "ogit/_xid": "attachment:arago:test:0:lorem-ipsum",
                "_content_data": {
                    "mimetype": "text/plain",
                    "data": "Auch gibt es niemanden, der den Schmerz an sich liebt, sucht oder wünscht, nur, weil er Schmerz ist, es sei denn, es kommt zu zufälligen Umständen, in denen Mühen und Schmerz ihm große Freude bereiten können.\n\nUm ein triviales Beispiel zu nehmen, wer von uns unterzieht sich je anstrengender körperlicher Betätigung, außer um Vorteile daraus zu ziehen? Aber wer hat irgend ein Recht, einen Menschen zu tadeln, der die Entscheidung trifft, eine Freude zu genießen, die keine unangenehmen Folgen hat, oder einen, der Schmerz vermeidet, welcher keine daraus resultierende Freude nach sich zieht? Auch gibt es niemanden, der den Schmerz"
                }
            },
            {
                "ogit/_xid": "attachment:arago:test:1:lorem-ipsum",
                "_content_data": {
                    "mimetype": "text/plain",
                    "data": BasicFileIOCarrier('<filename>')
                }
            }
        ]
    }
]
```

