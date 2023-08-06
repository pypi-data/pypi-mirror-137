Beyond apriori. CleverMiner is a Python implementation of GUHA procedures that extends apriori in many ways. In general, apriori is looking for rules {ItemSet} -> {Item} (Base, prob). GUHA goes further and instead of items (boolean attributes), list of categorial attributes and combination of values is searched on left and right hand side. Moreover, GUHA has much more possibilites and several other procedures.

Note this is a preliminary release for education use. Please see notes.

To run cleverminer procedures, use dataframe with categorical variables only. Cleverminer prepares **ALL** variables and values for future reuse.

What's new:

0.0.84 - optimizations for conjunctions
0.0.85 - bugfixes (row_count), checking input structure
0.0.86 - bugfixes (space search for optimized branch, able to switch off optimization, minimal cedent length bug for optimized search)
0.0.87 - support for 'one category' added
0.0.88 - print of task summary, hypo listing and individual hypothesis

