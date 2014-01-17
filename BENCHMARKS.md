This benchmark was executed on a 2012 macbook and used 200k colors from the XKCD color list. Processing of the raw lab values into objects / matrices was not included in the timings. For the full pickled lab matrix see http://lyst-classifiers.s3.amazonaws.com/color/lab-colors.pk

|method  |  delta_e | delta_e_matrix|
|:-------|---------:|--------------:|
|cie1976 | 3.256    | 0.018         |
|cie1994 | 3.787    | 0.058         |
|cmc     | 4.265    | 0.06          |
|cie2000 | 5.563    | 0.213         |

On large data-sets the vectorized version is an order of magnitude faster
