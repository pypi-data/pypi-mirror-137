# Magic Directories

An experimental plugin for passing data in directories in between steps.

**Warning: this package is highly experimental.**

## Installation

```bash
pip install metaflow-plugin-magicdir
```

## Usage

You can use `@magicdir` to pass local directories between metaflow steps.  This will also work remotely.

```py
#flow.py
from metaflow import FlowSpec, step
from metaflow.plugins import magicdir

class MagicDirFlow(FlowSpec):

    @magicdir(dir='mydir')
    @step
    def start(self):
        with open('mydir/output1', 'w') as f:
            f.write('hello world')
        with open('mydir/output2', 'w') as f:
            f.write('hello world again')
        self.next(self.end)

    @magicdir(dir='mydir')
    @step
    def end(self):
        print('first', open('mydir/output1').read())
        print('second', open('mydir/output1').read())

if __name__ == "__main__":
    MagicDirFlow()
```

If you run the above flow, you will see the following output:

```bash
> python flow.py run --with batch

2022-02-05 12:49:51.503 Workflow starting (run-id 11):
2022-02-05 12:49:51.511 [11/start/1 (pid 65038)] Task is starting.
2022-02-05 12:49:52.157 [11/start/1 (pid 65038)] Task finished successfully.
2022-02-05 12:49:52.165 [11/end/2 (pid 65046)] Task is starting.
2022-02-05 12:49:52.724 [11/end/2 (pid 65046)] first hello world
2022-02-05 12:49:52.799 [11/end/2 (pid 65046)] second hello world
2022-02-05 12:49:52.800 [11/end/2 (pid 65046)] Task finished successfully.
2022-02-05 12:49:52.801 Done!
```
