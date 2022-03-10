#!/bin/bash

export LEPHAREDIR='/pbs/throng/lsst/users/jocheval/MYLEPHARE/LEPHARE'
export LEPHAREWORK='/pbs/throng/lsst/users/jocheval/MYLEPHARE/LEPHARELSST'
export OMP_NUM_THREADS='10'

echo "Filter"
$LEPHAREDIR/source/filter -c LSST.para

## read the galaxy templates (as used in Ilbert et al. 2013)and store them in `$LEPHAREWORK/lib_bin`

echo "Templates"
$LEPHAREDIR/source/sedtolib -t G -c LSST.para

## use the galaxy templates + filters to derive a library of predicted magnitudes and store it in `$LEPHAREWORK/lib_mag` (the parameters correspond to enabling emission lines correlated to UV light + free factor in scaling these lines, mo$
echo "Magnitudes"
$LEPHAREDIR/source/mag_gal -t G -c LSST.para 

## finally proceed to photometric redshift estimation
echo "Estimation"
$LEPHAREDIR/source/zphota -c LSST.para -CAT_IN DC2_VALID_CAT_IN.in -CAT_TYPE LONG -CAT_OUT zphot_long.out -AUTO_ADAPT YES
#$LEPHAREDIR/source/zphota -c LSST.para -CAT_IN COSMOS.in -CAT_OUT zphot_short.out -ZPHOTLIB VISTA_COSMOS_FREE,ALLSTAR_COSMOS,QSO_COSMOS -AUTO_ADAPT YES

## a python script is available to perform a quick diagnostics
echo "Plots"
python figuresLPZ.py zphot_long.out

