#!/bin/bash

if [ -z "${LEPHAREDIR+x}" ]; then
    export LEPHAREDIR='/pbs/throng/lsst/users/jocheval/Intern2022_PhotoZ/LEPHARE'
fi
if [ -z "${LEPHAREWORK+x}" ]; then
    export LEPHAREWORK='/pbs/throng/lsst/users/jocheval/Intern2022_PhotoZ/LEPHARELSST'
fi
if [ -z "${OMP_NUM_THREADS+x}" ]; then
    export OMP_NUM_THREADS='10'
fi

if [ -z "${CAT_FILE_IN+x}" ]; then
    export CAT_FILE_IN='DC2_VALID_CAT_IN.in'
fi

if [ ! -d "$LEPHAREWORK" ]; then
  mkdir -p "$LEPHAREWORK/lib_bin"
  mkdir "$LEPHAREWORK/lib_mag"
  mkdir "$LEPHAREWORK/filt"
else
  if [ ! -d "$LEPHAREWORK/lib_bin" ] ; then
    mkdir "$LEPHAREWORK/lib_bin"
  fi
  if [ ! -d "$LEPHAREWORK/lib_mag" ] ; then
    mkdir "$LEPHAREWORK/lib_mag"
  fi
  if [ ! -d "$LEPHAREWORK/filt" ] ; then
    mkdir "$LEPHAREWORK/filt"
  fi
fi

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
$LEPHAREDIR/source/zphota -c LSST.para -CAT_IN "$CAT_FILE_IN" -CAT_TYPE LONG -CAT_OUT zphot_long.out -AUTO_ADAPT YES
#$LEPHAREDIR/source/zphota -c LSST.para -CAT_IN train_DC2_VALID_CAT_IN.in -CAT_TYPE LONG -CAT_OUT train_zphot_long.out -AUTO_ADAPT YES
#$LEPHAREDIR/source/zphota -c LSST.para -CAT_IN COSMOS.in -CAT_OUT zphot_short.out -ZPHOTLIB VISTA_COSMOS_FREE,ALLSTAR_COSMOS,QSO_COSMOS -AUTO_ADAPT YES

## a python script is available to perform a quick diagnostics
echo "Plots"
python figuresLPZ.py zphot_long.out
#python figuresLPZ.py train_zphot_long.out
