# clat

Command Line Analysis Tools: A collection of tools for doing data analysis.

This project started out as a small collection of example scripts to learn about using Python for simple
data analysis at the command line and grew into a collection of utilities I have found useful.

## Installation

Install this tool using `pip`:

    $ pip install clat

## Usage

`clat` consists of several different commands, all named with the `clat-` prefix. For example, `clat-avg` computes the average of a set of numbers. It behaves like a standard UNIX filter program.

```bash
set 10 | clat-avg
5.5
```

There are scripts for computing the sum, standard deviation, generating histograms, plotting, and more. To see a list of available tools, just type `clat-` and then press `<TAB>` a couple of times. All commands
accept the `--help` option.


### Filters

`clat` includes commands for computing the sum, average, standard deviation, root mean square, and uncertainty (standard error of the mean) for a stream of data. These commands read data from standard input and behave
like a normal UNIX filter (`grep`,`cut`,`sort`,etc). For example:

<!---
tag: filter-examples
snippet-compiler:
  options:
    compiler-command: bash {file}
-->
```bash
echo -e '1\n2\n3' | clat-sum
echo -e '1\n2\n3' | clat-avg
echo -e '1\n2\n3' | clat-stddev
echo -e '1\n2\n3' | clat-rms
echo -e '1\n2\n3' | clat-unc
```
<!---
tag: filter-examples
-->
```bash
6.0
2.0
1.0
2.160246899469287
0.5773502691896258
```

### Generators

Sometimes it is useful to be able to generate some data at the command line. For example, creating a test function to use with some other analysis tool or check that your plotting program is working. 
In the past I have used `seq` with `gawk` to do this, but it gets clumsy. The `clat-func` command was created to make this easier. For example, to generate a Gaussian function from -1 to 1, you could do this
<!---
tag: func-example-1
snippet-compiler:
  options:
    compiler-command: bash {file}
-->
```bash
clat-func --x-min -1 --x-max 1 --n 20 --y "exp( -({x}/0.2)**2 ) "
```
<!---
tag: func-example-1
-->
```bash
-1.0 1.3887943864964021e-11
-0.8947368421052632 2.032802578425745e-09
-0.7894736842105263 1.7098030687941603e-07
-0.6842105263157895 8.26400593449372e-06
-0.5789473684210527 0.00022952436120824522
-0.4736842105263158 0.003663199685231906
-0.368421052631579 0.033595881277480345
-0.26315789473684215 0.17705374665950163
-0.1578947368421053 0.5361889303292543
-0.052631578947368474 0.9330914390145757
0.05263157894736836 0.9330914390145759
0.1578947368421053 0.5361889303292543
0.26315789473684204 0.17705374665950185
0.36842105263157876 0.033595881277480484
0.4736842105263157 0.003663199685231916
0.5789473684210527 0.00022952436120824522
0.6842105263157894 8.264005934493735e-06
0.7894736842105261 1.7098030687941723e-07
0.894736842105263 2.0328025784257597e-09
1.0 1.3887943864964021e-11
```
CAREFUL!! This script uses Pythons `eval(...)` function to evaluate the arguments passed to the various options so that you can use expressions. For example:
<!---
tag: func-example-2
snippet-compiler:
  options:
    compiler-command: bash {file}
-->
```bash
clat-func --x-min 0 --x-max 2*pi --n 10 --y "sin({x})"
```
<!---
tag: func-example-2
-->
```bash
0.0 0.0
0.6981317007977318 0.6427876096865393
1.3962634015954636 0.984807753012208
2.0943951023931953 0.8660254037844387
2.792526803190927 0.34202014332566893
3.490658503988659 -0.3420201433256687
4.1887902047863905 -0.8660254037844383
4.886921905584122 -0.9848077530122081
5.585053606381854 -0.6427876096865395
6.283185307179586 -2.4492935982947064e-16
```

That means you should only run this with TRUSTED input. You have been warned...


### Plotting

The `clat-plot` command can be used to quickly plot some data at the command line. It reads from standard input and uses Gnuplot to generate the graph.

<!---
tag: plot-example-1
snippet-compiler:
  options:
    compiler-command: bash {file}
-->
```bash
clat-func --x-min 0 --x-max 2*pi --n 100 --y "sin({x})" | clat-plot -i
```
This will open a plot window with this graph
![](./doc/figures/example-plot.png)
