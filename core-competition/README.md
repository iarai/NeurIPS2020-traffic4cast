![t4c20logo](https://github.com/iarai/NeurIPS2020-traffic4cast/blob/master/t4c20logo.png)

# Traffic4cast 2020 - core competition

The Traffic4cast 2020 competition aims to explore some of these findings in depth. Our core challenge will be similar to Traffic4cast 2019, 
but will cover a wider range of cities and will encourage including complementary information.

To solve the core challenge, algorithms must make predictions for all the cities, where city-dependent parameters can be applied. 
Participants can investigate differences and similarities in traffic patterns between the cities, and explore master models trained 
on multiple cities. This year we introduce new static and dynamic features, such as street map properties, points of interest, weather, 
air pollution, and special events. The bonus challenges invite participants to explore which traffic attributes have the greatest impact.

## The data.
You can get obtain our competition's data if you follow instructions on [here](https://www.iarai.ac.at/traffic4cast/). It consists of a 
compressed file for each city that forms part of this core challenge. As a tip of the hat to our 2019 competition, we start again with
the cities of Berlin, Moscow and Istanbul and, like in 2019, we aggregate all our data in the same 100mx100m fashion and maintain the same
grid resolution of 495x436 pixels for each city.

For each city, we provide a training set of 181 full training days (repesenting the first half year of 2019), a validation set containing 18 
full dayus and a test set that will challenge participants to make 500 predictions of up to 1h into the future of real valued data, 
spread over 163 days.

Moreover, we will provide a static file that for each city, named `<City name>_static_2019.h5` which contains a `(495,436,7)` tensor.
The first 2 channels are a representation of the junction count (see details below) while the next 5 encode the number of eating, 
drinking and entertainment places, the number of hospitals, the number of parking places, the number of shops and the number of public 
transport venues in that order.

The training set for each city consists of 181 h5 files each being a compressed representation of a `(288,495,436,9)` tensor. As last year,
the first 3 dimensions encode the 5-min time bin, width and hight of each "image". The first two of the 9 channels encode the aggregated
volume and average speed of all underlying probes whose heading is between `0` and `90` degrees (i.e. NE), the next two the same aggregation
of volume and speed for all probes heading SE, the following two for SW and NW, respectively. The last channel is an encoding of recorded
road incidents.

For each city, we provide a `tar` file with with the city name in captial letters and the following folder structure:
```
+ -- <CITY NAME>  + -- CITY_NAME_static_2019.h5
	   	  + -- training --  + -- 2019-01-01_<city name>_9ch.h5
				    + -- 2019-01-02_<city name>_9ch.h5
						...
				    + -- 2019-12-31_<city name>_9ch.h5
		  + -- validation-- + -- 2019-07-01_<city name>_9ch.h5
				    + -- 2019-07-11_<city name>_9ch.h5
						...
				    + -- 2019-12-18_<city name>_9ch.h5
		  + -- testing      + -- 2019-07-02_test.h5
				    + -- 2019-07-03_test.h5
						...
				    + -- 2019-12-31_test.h5

```
Any file `<date>_test.h5` in the testing set contains a tensor of size `(m,12,495,436,9)` where `m` is variable, being the number of
predictions our competition is challenging our participants to make on that day. The `12` indicates that we give 12 successive "images" of
our 5min interval time bins, spanning a total of 1h. We will ask participants to predict 5min, 10min and 15min into the future, but and this is new this year, also 30min, 45min and 60min. Participants will the submit a directory for each city containing the same file names as the files in the testing data set, but encoding a tensor of dimension `(m,6,495,436,8)` reflecting the 6 time predictions and the fact that we do not ask participants to predict the incident channel - solely the probe data channels.

It might be helpful to "see" the movies one can make from our data. Here is a short clip of our ![incidents feed](https://github.com/iarai/NeurIPS2020-traffic4cast/blob/master/core-competition/incidents.mp4) for some day and a clip of the ![volume channel heading NE](https://github.com/iarai/NeurIPS2020-traffic4cast/blob/master/core-competition/NEmovie.mp4).


## The metric

Like last year, our core competition will keep to simple MSE, even though we are in full knowledge that this metric is crude at best.
The hunt for a better metric still excites us and we might well explore that theme in one of our bonus challenges.

## Helper scripts and files

We provide the following scripts in the hope that they might prove helpful to contestants to get up and close with the data. They are in
the `\util` subfolder and are presented here in their alphabetical order.


#### compare_h5.py

Determines whether two tensors with `uint8` entries in compressed h5 files are the same. The two files are input with the flags `-l` and `-r` (for LHS and RHS),
respectively. 

**Example:**
```
> python3 compare_h5.py -l BERLIN/training/2019-01-01_berlin_9ch.h5 -r BERLIN/training/2019-01-01_berlin_9ch.h5
True

> python3 compare_h5.py -l BERLIN/training/2019-01-01_berlin_9ch.h5 -r BERLIN/training/2019-01-02_berlin_9ch.h5
False
``` 
Evidently these examples are somewhat useless, but this method has its charms when auditing results and splicing our data.

#### extract_channel.py

Reads in a tensor (provided via the `-i` flag) and extracts a tensor slice specified via the `-c` option of the last dimension.
The result is then written back into an h5 file, the name of which is provided by the `-o` flag.

**Example:**
```
> python3 extract_channel.py -i BERLIN/training/2019-01-01_berlin_9ch.h5 -c 3 -o out.h5
> python3 h5shape.py -i out.h5
(288, 495, 436, 1)
```

#### extract_time_range.py

This method can extract a sub-tensor along given indicies of the first dimension (which we, based on our training and validation 
but not testing data, associated with "time"). The input is flagged via `-i` and output is written to an h5 file 
(provided by the `-o` flag). The indicies to extract are provide by one or repeated use of the `-c` flag.

**Example:**

```
> python3 extract_time_range.py -i BERLIN/dynamic/2019-01-01_berlin_9ch.h5 -c 0 -c 1 -c 2 -o first_15min_of_year.h5
> python3 h5shape.py -i first_15min_of_year.h5
(3, 495, 436, 9)
```
An example where the first dimension is not really time is the following.
```
> python3 extract_time_range.py -i BERLIN/BERLIN_static_2019 -c 0 -c 1 -o junction_count_layers.h5
``` 

#### h5shape.py

Displays the dimension of a tensor encoded in an h5 file provided via the `-i` flag.

**Example:**
```
> python3 h5shape.py -i BERLIN/training/2019-06-05_berlin_9ch.h5
(288, 495, 436, 9)
```

#### splice-test-tensor.py

This is similar to `extract_time_range.py` but only works on one channel and reshapes the resulting tensor to get rid of
the formerly first dimension. 

** Example **
```
> python3 h5shape.py -i BERLIN/testing/2019-07-30i_test.py
(3, 12, 495, 436, 9)
> python3 splice-test-tensor.py -i BERLIN/testing/2019-07-30_test.py -c 0 -o out.py
> python3 h5shape -i out.py
(12, 495, 436, 9)
```

Moreover, the files `test-slots.json` and `val_dates.json` map the tensors in the test set to their real world timeslot. Last year,
we provided our test set in the same format as our training and validation data for each data but with wihtheld data zeroed out.
This year we have opted for this more conceise representation.

`test_slots.json` consists of an array of one hash whose value is an (ordered) array. The hash key contains the testing date and the
associated value contains the 5min time bin number (0-287) when the test data will start (running for 11 further 5min intervals).

Lastly, `util.py` houses some simple commonly used functions.

#### tc2i.py

Given an input tensor of 4 dimensions `(t, x, y, c)` this will output a sequence of greyscale images indexed
by `t`, each of size `x` and `y` for a given fixed `c` that can either be provided (via the `-c`) option or is
already provided by the tensor shape if `c=1`. 
These images are saved under the file stub given by the `-s` option with the rolling index number appended.
Moreover, the `-f` option allows to multiply each tensor entry by a constant, with the values being
again clipped to between 0 - 255.

**Example:**
The following generates a movie of the incidents channel for Moscow on the 5th of May 2019. The individual images
are in the folder `\images`
```
> mkdir images
> python3 tc2i.py -i BERLIN/training/2019-05-05_berlin_9ch.h5 -c 8 -s images/img
> ffmmpeg -i images/img_%03d.png incident-movie.gif
```
and the following generates a movie of the volume of all NE heading probes on that day clip-scaled by 3.
```
> mkdir NEimages
> python3 tc2i.py -i BERLIN/training/2019-05-05_berlin_9ch.h5 -c 0 -s NEimages/img -f 3
> ffmpeg -i NEimages/img_%03d.png berlin_ne_vol.mp4
```


