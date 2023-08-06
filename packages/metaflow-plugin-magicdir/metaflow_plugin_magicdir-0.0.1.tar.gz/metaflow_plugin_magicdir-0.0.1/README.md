# Magic Directories

An experimental plugin for passing data in directories in between steps.

**Warning: this package is highly experimental.**

## Installation

```bash
pip install metaflow
```

## Usage

You can use `@magicdir` to pass local directories between metaflow steps.  This will also work remotely.

```py
#flow.py
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

If you run the above flow, you will see:

```bash
python flow.py run --with batch
```
