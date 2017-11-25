## Description

This is a simple Python script that generates an **SFZ** sampled instrument from samples created by the **Auto Sampler** plugin. Auto Sampler is available in Apple's [Mainstage 3](http://www.apple.com/mainstage/).

## About Auto Sampler

**Auto Sampler** is a plugin that converts hardware and software synthesizers into sampled instruments. Currently, it's availably only in Apple's [MainStage 3](http://www.apple.com/mainstage/).

**Mainstage** is a music software from Apple that lets you use your virtual instruments in live performance. It ships with the same [massive collection of plugins and sounds](http://www.apple.com/mainstage/plugins-and-sounds/) as Logic X Pro and has a very modest price.

Auto Sampler can sample your:

- hardware instruments - see [this great tutorial](https://441k.com/sampling-synths-with-auto-sampler-in-mainstage-3-26c506eb27a0) by Brian Li
- Audio Unit-based virtual instruments
- VST instruments - MainStage does not support VSTs so you'll have to use [ReWire](https://en.wikipedia.org/wiki/ReWire) or [Soundflower](https://github.com/mattingalls/Soundflower)
- iOS synths using [studiomux](http://midimux.com) or [musicIO](http://musicioapp.com)

## Creating SFZ instruments

Let's sample MainStage's Alchemy with a Hopeful Synth patch selected.

![Auto Sampler](images/autosampler.png)

After the sampling process is finished, we can go to `~/Music/Audio Music Apps/Samples/Auto Sampled/Hopeful Synth` and check what's inside:

```
Hopeful Synth-C1-127-ER7P.aif
Hopeful Synth-C1-32-5WTD.aif
Hopeful Synth-C1-64-HEDA.aif
Hopeful Synth-C1-95-BBHS.aif
Hopeful Synth-F#1-127-3B17.aif
Hopeful Synth-F#1-32-ZEQH.aif
Hopeful Synth-F#1-64-W5M9.aif
Hopeful Synth-F#1-95-MZC1.aif
Hopeful Synth-C2-127-NQI7.aif
Hopeful Synth-C2-32-679X.aif
Hopeful Synth-C2-64-NEEL.aif
Hopeful Synth-C2-95-3WD5.aif
...
```

As you can see, our samples have meaningful, machine-readable file names in the following format:

```<instrument name>-<note>-<velocity>-<random id>.aif```
	
So, we can parse these file names and generate an SFZ instrument based on these samples.

## Usage
```
$ python autosampler2sfz.py [-h] [-n <name>] [-w] [-d] [-o <output_dir>] <samples_dir>

Arguments:
  -h	Prints out this help message
  -n	The name of the SFZ instrument. If not specified, the name of <samples_dir> will be used.
  -w	Convert samples to .wav files
  -d	Downsample to 16 bits per sample
  -o	The output directory. If not specified, the files will be saved to the current directory.
```

## Example

After creating a new sampled instrument with Auto Sampler, you can find your samples in `~/Music/Audio Music Apps/Samples/Auto Sampled/<instrument name>`.
	
So, to create an SFZ instrument one can use the following command:

```$ python autosampler2sfz.py -o ~/Desktop ~/Music/Audio\ Music\ Apps/Samples/Auto\ Sampled/<instrument name>```
	
The instrument(.sfz and a folder containing samples) will be saved to the desktop.

## Conversion to SF2

If you need to convert your SFZ sampled instrument to SF2, you can do it with [Polyphone](http://polyphone-soundfonts.com/en/).

Please note that Polyphone supports only [WAV](https://en.wikipedia.org/wiki/WAV) files so you will need to convert your samples to .wav (see -w option).

## Software samplers with SFZ support

- [tw16x](http://www.tx16wx.com) (Mac, Win)
- [sforzando](https://www.plogue.com/products/sforzando/) (Mac, Win)
- [Auria Pro](http://auriaapp.com/Products/auria) (iOS)
- [MultitrackStudio](http://www.multitrackstudio.com) (Mac, Win, iOS)
- [Caustic](http://www.singlecellsoftware.com/caustic) (iOS)
