# LAMA

The following description is adapted from the LAMA README (thanks to Silvia Richter, Matthias Westphal and Malte Helmert). 

Version: May 4, 2011 (updated translator compared to Jan and Aug 2010 and April 2010, bug fix in FF heuristic since Dec 2010)

### License:
LAMA was written by Silvia Richter and Matthias Westphal, copyright (c) 2008 NICTA and Matthias Westphal. Distributed under the GNU General Public License (GPL, see separate licence file). This program uses source code of the Fast Downward planner, (c) 2003-2004 by Malte Helmert and Silvia Richter. Permission to redistribute this code under the terms of the GPL has been granted.

**Note of Caution:** Please be aware that LAMA has bugs. In particular the component responsible for parsing and translating the PDDL input has known problems. However, for all classical (i.e. non-numerical, no preferences etc.) tasks from past international planning competitions, formulations exist that LAMA can parse. E.g.: for Airport, use the STRIPS formulation. For Freecell (IPC 2002), the untyped variant. For Philosophers, Optical Telegraph and PSR, use the ADL variant with derived predicates. For Mprime and Assembly, domain files are included in this distribution in the `bench-patch` directory which correct known bugs of the competition files (Mprime) or features not supported by LAMA (Assembly).

If you encounter further problems, please email me at silvia.richter@nicta.com.au. The lama/translate directory also contains a patch that can be applied to skip the invariant generation step in the translator component. This eliminates many problems and may be helpful e.g. if you are interested in using the framework of LAMA with a heuristic other than the landmark heuristic.

Lastly, I would be happy to know if you are using LAMA. Just drop me a short email at the above address. Then I can also inform you about bug fixes and new versions.

The following description is adapted from the Fast Downward README (thanks to Malte Helmert).

## Structure

LAMA runs in three separate phases: translation, knowledge compilation, and search. These are partitioned into three separate programs.  The three directories `translate` `preprocess` and `search` contain these programs.

## Documentation

1. A comprehensive description of LAMA can be found in the JAIR article "The LAMA Planner: Guiding Cost-Based Anytime Planning with Landmarks" by Silvia Richter and Matthias Westphal (2010), which is included in the `doc` directory under `lama-jair10.pdf`. A brief description of the planner is furthermore given in `lama-short.pdf` in the same directory. 
2. The AIJ article "Concise finite-domain representations for PDDL planning tasks" by Malte Helmert (2009) describes the translation component in detail. The description is somewhat idealized, as the actual implementation has some limitations in dealing with some ADL features. Still, the article provides a fairly good description of what the translator does (or should do, at any rate). `sas-format.txt` in the `doc` directory is a description of the translator output format. You will only need this if you want to use SAS+ tasks/multi-valued planning tasks within your own planner.
4. `pre-format.txt` in the "doc" directory is a description of the output format of the knowledge compilation component (`preprocess`). You will only need this if you want to use the preprocessed multi-valued planning task information within your own planner.

The following description is adapted from the README from the LAMA fork by Sebastian Sardina.

# Build & Installation

Parts of the planner are implemented in C++, and parts are implemented in Python. The C++ code was only tested under g++ and uses hash tables from the original STL which are part of the g++ libraries but not of the C++ standard. So if you want to make the planner run under a different C++ environment, you will need to adjust the parts of the planner that use these features.

To build and install LAMA, you can use the provided install script:

```shell
$ ./install.sh
```

By default, the resulting excutables and libraries are placed under `lama-planner/` folder. To change that, edit the installation script and change `INSTALL_DIR` variable.

## Running the Planner

LAMA runs in three separate phases: _translation_, _knowledge compilation_, and _search_. These are partitioned into three separate programs. The three directories `lama/translate`, `lama/preprocess` and
`lama/search` contain these programs.

To run the planner, you can simply use the Bash script `lama-planner`:

```shell
$ ./lama-planner/bin/lama-planner <domain_path> <problem_path> <result_path> <landmark_path>
```

Where `<domain_path>` should lead to the PDDL domain file, the `<problem_path>` should lead to the PDDL problem file, and the `<result_path>` should lead to an output file, to which the found plans will be written to. The `<landmark_path>` is optional, if provided, the landmark graph will be written to this file.

This script contains the settings used for LAMA during IPC-6. For other possible arguments modify the run script accordingly. The search component of the planner understands four options which can be combined in any way:

* `l`: Use the landmark heuristic.
* `L`: Use preferred operators of the landmark heuristic.
* `f`: Use the FF heuristic.
* `F`: Use helpful actions ("preferred operators" of the FF heuristic).

At least one heuristic (`l` or `f`) must be used; on average, using all features of the planner (`lLfF`) appears to produce the best results, which is therefore the default in the `lama-planner` script.

The planner can be told to run in iterated mode (keep searching for better solutions) using option `i`. Note that in this case, the planner may never stop (unless it can exhaust the search space) and needs to be aborted at some point.

By default, the first solution is found using best-first search, later search iterations use weighted A*. In order to use weighted A* for the first iteration as well, use option `w`.

Or, you can _run the three steps of LAMA separately_ (e.g., if you want to re-use output from earlier translation/pre-processing steps):

First, run:

```shell
$ /path/to/lama-planner/translate/translate.py domain.pddl problem.pddl
```

The translator will write its result to a file called `output.sas`, which serves as an input to the next phase, knowledge compilation. The translator also writes a file called `test.groups`, which is some sort of translation key (see `sas-format.txt` in the documentation directory mentioned above). This second file is not needed by the planner, but might help you understand what the translated task looks like. It also writes a file called `all.groups` which is needed by the landmark heuristic.

Second, run:

```shell
$ /path/to/lama-planner/preprocess/preprocess < output.sas
```

This will run the knowledge compilation component, writing its output to the file aptly named `output.out`.

Finally, run:

```shell
$ /path/to/lama-planner/search/search <args>  < output.out
```

This runs the search component of the planner. On success, it will write a file called `sas_plan` containing the plan.


# Forked

For citing the original LAMA planner please use:
```bib.tex
Silvia  Richter  and  Matthias  Westphal.  “The  LAMA  Planner:  GuidingCost-Based Anytime Planning with Landmarks”. In:Journal of ArtificialIntelligence Research. Vol. 39. 2010, pp. 127–177.
```

### Minor changes
To add install script and fix some deprecation issues.
- Adds an `install` script, based on https://github.com/ssardina-research/planning-lama
  - Change folder for intermediate and result files to `tmp`
- Changed `<depend package="base/types"/>` to `<depend package="base/cmake"/>` in `manifest.xml`
- Added a `ROOT` directory in `plan.in` line 4
- Added a `python3` call in `plan.in` line 11
- Changed `<tr1/functional>` import to `<functional>` in `lama/search/landmark_types.h`
- Changed `time.clock()` to `time.process_time()` in `lama/translate/invariant_finder.py`
- Added cleanup to move temporary files created during planning to the `tmp` folder


## New content
We want to use the landmark extraction component to use the landmarks in our custom planner. Therefore, we added the following:
- `write()` and `write_node()` functions in `landmark_graph.cc` and `landmark_graph.h`, which are almost the same as `dump` but instead write to a file `tmp/landmarks.out`
- call the `write` function from `planner.cc`
- added another script to only generate landmarks, which calls the `search/generator.cc` for compilation and writes landmarks to a given file 
- added extra parameter to write landmark graph to, besides the `tmp/landmarks.out`
