This benchmark was executed on a 2012 macbook and used 1 million colors from the XKCD color list. Processing of the raw lab values into objects / matrices was not included in the timings. For the full pickled lab matrix see http://lyst-classifiers.s3.amazonaws.com/color/lab-colors.pk

|method  |  delta_e | delta_e_matrix|
|--------|---------:|--------------:|
|cie1976 | 16.87    | 0.10          |
|cie1994 | 19.28    | 0.33          |
|cmc     | 21.99    | 0.58          |
|cie2000 | 27.28    | 1.06          |

On large data-sets the vectorized version is an order of magnitude faster
