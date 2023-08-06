# cirrus-volume
Some happy little volumes

![Perhaps making slightly fewer happy accidents](assets/bob.gif)

### Installation

```bash
pip install cirrus-volume
```

### THE RULES  
You cannot write to a CirrusVolume unless you've passed it:
1. A set of sources from which it was created (e.g., another CloudVolume path or a freeform justification like "tracer annotation"). This must be formatted as a `List[str]`, and any sources that haven't been logged previously will be added to the current sources field of the provenance file
2. The motivation for creating the volume (`str`) has been passed or previously logged. A volume can have multiple motivation notes.
3. A `Process` (a code environment & parameters as defined by [provenance-tools](https://github.com/ZettaAI/provenance-tools). The process will be logged unless another process with the same task description and parameters has already been logged.

### Usage
Aside from the rules above, CirrusVolumes should work the same way other CloudVolumes do.

If you only need to read data from a volume, your workflow should not change at all.
```python3
import cirrusvolume as cv
v = cv.CloudVolume(cloudpath)
v[bbox]
```

However, if you'd like to write to a CirrusVolume you'll need to add a few extra lines.
```python3
v[bbox] = data
#-> AssertionError: Need to define sources, motivation and process in order to write to this volume
```

Sources describe source data for this volume. These can be a freeform justification if this volume doesn't depend on another CloudVolume
```python3
sources_freeform = ['tracer annotation']
sources_cloudvolume = [other_cloudpath]
```

The motivation describes a reason for creating this volume. This can be boilerplate for a processing pipeline, but can be very important for research applications.
```python3
motivation = 'We go to the moon because it is hard!'
```

Lastly, the process specifies what you're writing/modifying and how it was generated. This consists of a description of the task (i.e., what you're currently doing), any parameters involved, and a code environment that captures the state of the code used to do it. A lot of the work of figuring out the code environment is performed by [provenance-tools](https://github.com/ZettaAI/provenance-tools).
```python3
import provenancetools as pt
python_github_env = pt.PythonGithubEnv('.')  # path to the github repo directory
docker_env = pt.DockerEnv(imagename, tag, containerID)  # docker container metadata

process = pt.Process('giving a demo of cirrus-volume',
                     {'meta_level': 5},
                     python_github_env)
```

Once you've defined these fields, you can either pass them to the CirrusVolume when you create it, or add them as attributes later.
```python3
# Defining the metadata at initialization
write_volume = cv.CloudVolume(cloudpath,
                              sources=sources_cloudvolume,
                              motivation=motivation,
                              process=demo_process)
write_volume[bbox] = data
```
```python3
# Adding the metadata afterwards
v.sources = sources_cloudvolume
v.motivation = motivation
v.process = demo_process
v[bbox] = data
```
