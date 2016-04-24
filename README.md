## Description

This is a simple Python script that generates an **SFZ** sampled instrument from samples created by the **Auto Sampler** plugin. Auto Sampler is available in Apple's [Mainstage 3](http://www.apple.com/mainstage/).

## Usage
```
$ python autosampler2sfz.py [-h] [-n <name>] [-o <output_dir>] <samples_dir>

Arguments:
  -h	Prints out this help message.
  -n	The name of the SFZ instrument. If not specified, the name of <samples_dir> will be used.
  -o	The output directory. If not specified, the files will be saved to the current directory.
```

## Example

After creating a new sampled instrument with Auto Sampler, you can find your samples in `~/Music/Audio Music Apps/Samples/Auto Sampled/<instrument name>`.
	
So, to create an SFZ instrument one can use the following command:

```$ python autosampler2sfz.py -o ~/Desktop ~/Music/Audio\ Music\ Apps/Samples/Auto\ Sampled/<instrument name>```
	
The instrument(.sfz and a folder containing samples) will be saved to the desktop.

## Conversion to SF2

If you need to convert your SFZ sampled instrument to SF2, you can do it with [Polyphone](http://www.polyphone.fr).

Please note that Polyphone supports only [WAV](https://en.wikipedia.org/wiki/WAV) files while Auto Sampler-generated samples are [AIFF](https://en.wikipedia.org/wiki/Audio_Interchange_File_Format) files. I will try to implement optional conversion from .aif to .wav later. In the meantime, you can convert your samples to .wav using one of the numerous existing audio editors and then open the .sfz file in your favorite plain-text editor and change all .aif extensions to .wav