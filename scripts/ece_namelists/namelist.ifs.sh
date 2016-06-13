# namelist.ifs.sh

# Set coupling frequencies for ocean and chemistry coupling
(( ${cpl_freq_atm_oce_sec:-} )) && NFRCO=$(( cpl_freq_atm_oce_sec / ifs_time_step_sec )) || NFRCO=0
(( ${cpl_freq_atm_ctm_hrs:-} )) && NFRCO_CHEM=$(( cpl_freq_atm_ctm_hrs * 3600 / ifs_time_step_sec )) || NFRCO_CHEM=0

# Switch off warm ocean parametrisation for coupled runs
(( NFRCO > 0 )) && LEOCWA=FALSE || LEOCWA=TRUE

# Switch on/off TM5 feedback to IFS
(( ${tm5_fdbck_o3:-}   )) && LTM5O3=TRUE  || LTM5O3=FALSE
(( ${tm5_fdbck_ch4:-}  )) && LTM5CH4=TRUE || LTM5CH4=FALSE
(( ${tm5_fdbck_aero:-} )) && LTM5AER=TRUE || LTM5AER=FALSE

# Switch on/off SPPT and set the ensemble member number (defaults to zero)
has_config sppt && LSPSDT=TRUE || LSPSDT=FALSE
NENSFNB=${ifs_ensemble_forecast_number:-0}

cat << EOF
&NAMRES
    NFRRES         = 1,
    NRESTS         = -1,-$(( leg_end_sec / 3600 )),
/
&NAERAD
    NRPROMA        = 0,
    LCMIP5         = ${ifs_cmip5},
    CMIP5DATADIR   = "${ini_data_dir}/ifs/cmip5-data",
    NCMIP5FIXYR    = ${ifs_cmip5_fixyear},
    NRCP           = ${ifs_cmip5_rcp},
    LHVOLCA        = TRUE,
    LTM5O3         = ${LTM5O3},
    LTM5CH4        = ${LTM5CH4},
    LTM5AER        = ${LTM5AER},
/
&NAEPHY
    LEPHYS         = TRUE,
    LEVDIF         = TRUE,
    LESURF         = TRUE,
    LECOND         = TRUE,
    LECUMF         = TRUE,
    LEPCLD         = TRUE,
    LEEVAP         = TRUE,
    LEVGEN         = TRUE,
    LESSRO         = TRUE,
    LECURR         = FALSE,
    LEGWDG         = TRUE,
    LEGWWMS        = TRUE,
    LEOCWA         = ${LEOCWA},
    LEOZOC         = TRUE,
    LEQNGT         = TRUE,
    LERADI         = TRUE,
    LERADS         = TRUE,
    LESICE         = TRUE,
    LEO3CH         = FALSE,
    LEDCLD         = TRUE,
    LDUCTDIA       = FALSE,
    LWCOU          = FALSE,
    LWCOU2W        = TRUE,
    NSTPW          = 1,
    RDEGREW        = 1.5,
    RSOUTW         = -81.0,
    RNORTW         = 81.0,
/
&NAMPAR1
    LSPLIT         = TRUE,
    NFLDIN         = 0,
    NFLDOUT        = 50,
    NSTRIN         = 1,
/
&NAMPAR0
    LSTATS         = TRUE,
    LDETAILED_STATS= FALSE,
    LSYNCSTATS     = FALSE,
    LSTATSCPU      = FALSE,
    NPRNT_STATS    = 32,
    LBARRIER_STATS = FALSE,
    LBARRIER_STATS2= FALSE,
    NPROC          = ${ifs_numproc},
    NOUTPUT        = 1,
    MP_TYPE        = 2,
    MBX_SIZE       = 128000000,
/
&NAMDYNCORE
    LAQUA          = FALSE,
/
&NAMDYN
    TSTEP          = ${ifs_time_step_sec}.0,
    LMASCOR        = TRUE,
    LMASDRY        = TRUE,
/
&NAMNMI
    LASSI          = FALSE,
/
&NAMIOS
    CFRCF          = "rcf",
    CIOSPRF        = "srf",
/
&NAMFPG
/
&NAMCT0
    LNHDYN         = FALSE,
    NCONF          = 1,
    CTYPE          = "fc",
    CNMEXP         = "test",
    CFCLASS        = "se",
    LECMWF         = TRUE,
    LARPEGEF       = FALSE,
    LFDBOP         = FALSE,
    LFPOS          = TRUE,
    LSMSSIG        = FALSE,
    LSPRT          = TRUE,
    LSLAG          = TRUE,
    LTWOTL         = TRUE,
    LVERTFE        = TRUE,
    LAPRXPK        = TRUE,
    LOPT_SCALAR    = TRUE,
    LPC_FULL       = FALSE,
    LPC_CHEAP      = FALSE,
    LPC_NESC       = FALSE,
    LPC_NESCT      = FALSE,
    LSLPHY         = TRUE,
    LRFRIC         = TRUE,
    LFPSPEC        = FALSE,
    N3DINI         = 0,
    NSTOP          = $(( leg_end_sec / ifs_time_step_sec )),
    NFRDHP         = ${ifs_ddh_freq},
    NFRSDI         = ${ifs_di_freq},
    NFRGDI         = ${ifs_di_freq},
    NFRPOS         = ${ifs_output_freq},
    NFRHIS         = ${ifs_output_freq},
    NFRMASSCON     = $(( 6 * 3600 / ifs_time_step_sec )),
    NPOSTS         = 0,
    NHISTS         = 0,
    NMASSCONS      = 0,
    NFRCO          = ${NFRCO},
    NFRCO_CHEM     = ${NFRCO_CHEM},
    NFRDHFZ        = 48,
    NDHFZTS        = 0,
    NDHFDTS        = 0,
    LWROUTLAST     = ${ifs_lastout},
/
&NAMDDH
    BDEDDH(1,1)    = 4.0,1.0,0.0,50.0,0.0,49.0,
    NDHKD          = 120,
    LHDZON         = FALSE,
    LHDEFZ         = FALSE,
    LHDDOP         = FALSE,
    LHDEFD         = FALSE,
    LHDGLB         = TRUE,
    LHDPRG         = TRUE,
    LHDHKS         = TRUE,
/
&NAMGFL
    LTRCMFIX       = TRUE,
    NERA40         = 0,
    YQ_NL%LGP      = TRUE,
    YQ_NL%LSP      = FALSE,
    YL_NL%LGP      = TRUE,
    YI_NL%LGP      = TRUE,
    YA_NL%LGP      = TRUE,
    YO3_NL%LGP     = FALSE,
    YQ_NL%LGPINGP  = TRUE,
    YL_NL%LQM      = TRUE,
    YI_NL%LQM      = TRUE,
    YR_NL%LQM      = TRUE,
    YS_NL%LQM      = TRUE,
    YQ_NL%LMASSFIX = TRUE,
    YL_NL%LMASSFIX = TRUE,
    YI_NL%LMASSFIX = TRUE,
    YR_NL%LMASSFIX = TRUE,
    YS_NL%LMASSFIX = TRUE,
    YCDNC_NL%LGP   = TRUE,
    YICNC_NL%LGP   = TRUE,
    YRE_LIQ_NL%LGP = TRUE,
    YRE_ICE_NL%LGP = TRUE,
    YCDNC_NL%CNAME = "CDNC",
    YICNC_NL%CNAME = "ICNC",
    YRE_LIQ_NL%CNAME ="Reff_liq",
    YRE_ICE_NL%CNAME ="Reff_ice",
/
&NAMFPC
    CFPFMT         = "MODEL",
    NFP3DFT        = 1,
    MFP3DFT        = 60,
    NFP3DFV        = 1,
    MFP3DFV        = 133,
    NFP2DF         = 3,
    MFP2DF         = 129,134,152,
    NFPPHY         = 82,
    MFPPHY         = 8,31,32,33,34,35,36,37,38,39,40,41,42,44,45,49,50,57,58,59,78,79,123,129,136,137,139,141,142,143,144,145,146,147,148,151,159,164,165,166,167,168,169,170,172,175,176,177,178,179,180,181,182,183,186,187,188,189,195,196,197,198,201,202,205,208,209,210,211,212,213,228,229,230,231,232,235,236,238,243,244,245,
    NRFP3S         = 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91
    NFP3DFS        = 11,
    MFP3DFS        = 54,129,130,131,132,133,135,157,246,247,248
    RFP3P          = 100000.,92500.,85000.,70000.,60000.,50000.,40000.,30000.,25000.,20000.,15000.,10000.,7000.,5000.,3000.,2000.,1000.,700.,500.,300.,200.,100.,
    RFPCORR        = 60000.,
    NFP3DFP        = 8,
    MFP3DFP        = 129,130,131,132,133,135,138,157,
    RFP3H          = 2.,
    NFP3DFH        = 2,
    MFP3DFH        = 133,157,
    LFITP          = TRUE,
    LFITT          = FALSE,
    LFITV          = FALSE,
    NFPCLI         = 0,
    LFPQ           = FALSE,
    LASQ           = FALSE,
    LTRACEFP       = FALSE,
/
&NAMFPD
/
&NAMDIM
    NPROMA         = 0,
    NUNDEFLD       = 0,
/
&NAMVAR
    LMODERR        = FALSE,
    LJCDFI         = FALSE,
    LUSEJCDFI      = FALSE,
/
&NAMMCC
    LMCCIEC        = TRUE,
    LMCCEC         = TRUE,
    LMCC04         = TRUE,
    NOACOMM        = 5,
    LMCCICEIC      = FALSE,
/
&NAMPPC
    LRSACC         = TRUE,
/
EOF

# Use special gravity wave drag parametrisation for T255L91
case ${ifs_grid} in

T255L91)
cat << EOF
&NAMGWWMS
    GFLUXLAUN=0.002,
    ZLAUNCHP=45000,
    LOZPR=true,
    NGAUSS=4,
    GGAUSSB=1.0,
/
&NAMGWD
    GTENLIM=0.02,
/
EOF
;;

# Use default parametrisation for all other grids
*)
cat << EOF
&NAMGWWMS
/
&NAMGWD
/
EOF
;;
esac

cat << EOF
&NAEAER
/
&NALBAR
/
&NALORI
/
&NAM_DISTRIBUTED_VECTORS
/
&NAM926
/
&NAMAFN
/
&NAMANA
/
&NAMARPHY
/
&NAMCA
/
&NAMCAPE
/
&NAMCFU
/
&NAMCHK
/
&NAMCHET
/
&NAMCLDP
    NCLDDIAG   = 0,
    RLCRITSNOW = 3.0E-5,
    RVICE      = 0.13,
    RTAUMEL    = 7200.0,
    RSNOWLIN2  = 0.035,
    RCLCRIT    = 0.4E-3,
    NCLOUDACT  = 1,
    NAERCLD    = 41,
/
&NAMCLTC
/
&NAMCOM
/
&NAMCOS
/
&NAMCTAN
/
&NAMCUMF
    ENTRORG = 1.5E-4,
    ENTRDD  = 3.0E-4,
    RPRCON  = 1.2E-3,
    DETRPEN = 0.75E-4,
    RMFDEPS = 0.3,
/
&NAMCUMFS
/
&NAMCT1
/
&NAMCVA
/
&NAMDFHD
/
&NAMDFI
/
&NAMDIF
/
&NAMDIMO
/
&NAMDMSP
/
&NAMDPHY
/
&NAMDYNA
/
&NAMEMIS_CONF
/
&NAMENKF
/
&NAMFA
/
&NAMFFT
/
&NAMFPDY2
/
&NAMFPDYH
/
&NAMFPDYP
/
&NAMFPDYS
/
&NAMFPDYT
/
&NAMFPDYV
/
&NAMFPEZO
/
&NAMFPF
/
&NAMFPIOS
/
&NAMFPPHY
/
&NAMFPSC2
/
&NAMFPSC2_DEP
/
&NAMFY2
/
&NAMGEM
/
&NAMGMS
/
&NAMGOES
/
&NAMGOM
/
&NAMGRIB
    NENSFNB = ${NENSFNB},
/
&NAMGWD
/
&NAMGWWMS
/
&NAMHLOPT
/
&NAMINI
/
&NAMIOMI
/
&NAMJBCODES
/
&NAMJFH
/
&NAMJG
/
&NAMJO
/
&NAMKAP
/
&NAMLCZ
/
&NAMLEG
/
&NAMLFI
/
&NAMMCUF
/
&NAMMETEOSAT
/
&NAMMTS
/
&NAMMTSAT
/
&NAMMTT
/
&NAMMUL
/
&NAMNASA
/
&NAMNN
/
&NAMNPROF
/
&NAMNUD
/
&NAMOBS
/
&NAMONEDVAR
/
&NAMOPH
/
&NAMPARAR
/
&NAMPHY
/
&NAMPHY0
/
&NAMPHY1
/
&NAMPHY2
/
&NAMPHY3
/
&NAMPHYDS
/
&NAMPONG
/
&NAMRAD15
/
&NAMRCOEF
/
&NAMRINC
/
&NAMRIP
/
&NAMSCC
/
&NAMSCEN
/
&NAMSCM
/
&NAMSENS
/
&NAMSIMPHL
/
&NAMSKF
/
&NAMSPSDT
    LSPSDT          = ${LSPSDT},
    LCLIP_SPEC_SDT  = TRUE,
    LCLIP_GRID_SDT  = TRUE,
    LWRITE_ARP      = FALSE,
    LUSESETRAN_SDT  = TRUE,
    LRESETSEED_SDT  = FALSE,
    NSCALES_SDT     = 3,
    CSPEC_SHAPE_SDT ='WeaverCourtier',
    SDEV_SDT        = 0.52,0.18,0.06,
    TAU_SDT         = 2.16E4,2.592E5,2.592E6,
    XLCOR_SDT       = 500.E3,1000.E3,2000.E3,
    XCLIP_RATIO_SDT = 1.8,
    LTAPER_BL0      = TRUE,
    XSIGMATOP       = 0.87,
    XSIGMABOT       = 0.97,
    LTAPER_ST0      = TRUE,
    XPRESSTOP_ST0   = 50.E2,
    XPRESSBOT_ST0   = 100.E2,
    LQPERTLIMIT2    = TRUE,
/
&NAMSTA
/
&NAMSTOPH
/
&NAMTCWV
/
&NAMTESTVAR
/
&NAMTLEVOL
/
&NAMTOPH
/
&NAMTOVS
/
&NAMTRAJP
/
&NAMTRANS
/
&NAMTRM
/
&NAMVARBC
/
&NAMVARBC_AIREP
/
&NAMVARBC_ALLSKY
/
&NAMVARBC_RAD
/
&NAMVARBC_TCWV
/
&NAMVARBC_TO3
/
&NAMVAREPS
/
&NAMVDOZ
/
&NAMVFP
/
&NAMVRTL
/
&NAMVV1
/
&NAMVV2
/
&NAMVWRK
/
&NAMXFU
/
&NAMZDI
/
&NAPHLC
/
&NAV1IS
/
EOF
