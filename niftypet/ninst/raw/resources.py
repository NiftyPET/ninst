"""Resources file for NiftyPET NIPET and NIMPA etc."""
__author__ = ("Pawel J. Markiewicz", "Casper O. da Costa-Luis")
__copyright__ = "Copyright 2018-20"

from math import ceil, pi

try:
    from numpy import array
except ImportError:

    def array(x):
        return x


# > logging represented by an integer: 10, 20, 30... for DEBUG, INFO, WARNING...
# > as it is in Python package logging, which is also used here.
LOG = 20


# Radioisotope look-up table
riLUT = {
    "Ge68": {"BF": 0.891, "thalf": 270.9516 * 24 * 60 * 60},
    "Ga68": {"BF": 0.891, "thalf": 67.71 * 60},
    "F18": {"BF": 0.967, "thalf": 109.77120 * 60},
    "C11": {"BF": 0.998, "thalf": 20.38 * 60},
    "O15": {"BF": 0.999, "thalf": 122.2416},
}

# -----------------------------------------------------
# The name and path to the NiftyPET tools (software)
DIRTOOLS = "NiftyPET_tools"
MSVC_VRSN = "Visual Studio 12 2013 Win64"
CMAKE_TLS_PAR = ""  # -DUSE_SSE=OFF'
# PATHTOOLS = os.path.join('/chosen/path/', DIRTOOLS)
# > path to Python wrapper of Vinci
VINCIPATH = ""

# > path to reference images for testing NiftyPET
REFPATH = ""
# -----------------------------------------------------

# -----------------------------------------------------
# DO NOT MODIFY BELOW--DONE AUTOMATICALLY
# # # start GPU properties # # #
# # # end GPU properties # # #

# paths to apps and tools needed by NiftyPET
# # # start NiftyPET tools # # #
# # # end NiftyPET tools # # #
# -----------------------------------------------------

# > enable Agg for plotting images in PDF
ENBLAGG = False

# > enable XNAT module
ENBLXNAT = False

# =================================================================================================


def get_gpu_constants(Cnt=None):
    """Return a dictionary of GPU related constants"""
    if Cnt is None:
        Cnt = {}

    for k in [
        "DEV_ID",  # device id; used for choosing the GPU device for calculations
        "CC_ARCH",  # chosen device architectures for NVCC compilation
    ]:
        val = globals().get(k)
        if val is not None:
            Cnt[k.replace("_", "")] = val

    return Cnt


# =================================================================================================
def get_setup(Cnt=None):
    """Return a dictionary of GPU, mu-map hardware and third party set-up."""
    if Cnt is None:
        Cnt = {}

    Cnt["LOG"] = LOG

    Cnt["VERBOSE"] = False

    # > enable XNAT module
    Cnt["ENBLXNAT"] = ENBLXNAT

    # > enable Agg for plotting images in PDF
    Cnt["ENBLAGG"] = ENBLAGG

    # > compile DCM2NIIX, otherwise download a compiled version for the system used
    Cnt["CMPL_DCM2NIIX"] = False

    # > electron radius **2
    Cnt["R02"] = 7.940787449825884e-26

    # > speed of light
    Cnt["CLGHT"] = 29979245800  # cm/s

    # the name of the folder for NiftyPET tools
    Cnt["DIRTOOLS"] = DIRTOOLS

    # additional paramteres for compiling tools with cmake
    Cnt["CMAKE_TLS_PAR"] = CMAKE_TLS_PAR

    # Microsoft Visual Studio Compiler version
    Cnt["MSVC_VRSN"] = MSVC_VRSN

    # GPU related setup
    Cnt = get_gpu_constants(Cnt)

    for k in [
        "PATHTOOLS",
        "RESPATH",  # image processing setup
        "REGPATH",
        "DCM2NIIX",
        "HMUDIR",  # hardware mu-maps
        "VINCIPATH",
        "REFPATH",  # > testing
    ]:
        val = globals().get(k)
        if val is not None:
            Cnt[k] = val

    return Cnt


# =================================================================================================
# ========================== SIEMENS microPET SCANNER C O N S T A N T S ===========================


def get_mcr_constants():
    """
    Put all the constants together in a dictionary for the microPET
    """

    # > get the baseline setup as well as GPU and third party setups
    Cnt = get_setup()

    # > update with the key constants
    Cnt.update(
        {
            "ISOTOPE": "F18",
            # > perform decay correction (True/False)
            "DCYCRR": True,
            # > bootstrap option for histogramming
            "BTP": 0,  # 1:non parametric bootstrap, 2: parametric bootstrap (recommended)
            "BTPRT": 1.0,  # Ratio of bootstrapped/original events (enables downsampling)
            # > bytes per event in list mode data
            "BPE": 4,
            # > LM header offset in bytes (for mMR it is in a separate DICOM format)
            "LMOFF": 0,
            # > crystal angle
            "ALPHA": 0.714286 * pi / 180,  # 2*pi/NCRS,
            # > number of rings (axially) and crystals (transaxially)
            "NRNG": 64,
            # > number of crystals transaxially
            "NCRS": 504,
            # > reduced number of crystals by the gaps (dead crystals)
            "NCRSR": 448,
            # > number of buckets for singles
            "NBCKT": 224,
            # number of direct sinograms (i.e., for segment 0)
            "NSEG0": 127,
            # > crystal gap period
            "TGAP": 9,
            # > crystal gap offset (used for getting the sino gaps right at the position)
            "OFFGAP": 1,
            # > axial crystal width
            "AXR": 0.40625,
            # > ring radius
            "R": 32.8,
            # > coincidence time window [ps]
            "CWND": 5859.38e-12,
            # > depth of interaction
            "DOI": 0.67,
            # > no of sinos in a segment out of 11 segments
            "SEG": array([127, 115, 115, 93, 93, 71, 71, 49, 49, 27, 27]),
            # > minimum and maximum ring difference for each segment
            "MNRD": array([-5, -16, 6, -27, 17, -38, 28, -49, 39, -60, 50]),
            "MXRD": array([5, -6, 16, -17, 27, -28, 38, -39, 49, -50, 60]),
            # > hardware mu-maps
            "HMULIST": [],
        }
    )

    # > update with sinogram constants
    Cnt.update(
        {
            # > number of angular indexes in a 2D sinogram
            "NSANGLES": 252,
            # > number of bin indexes in a 2D sinogram
            "NSBINS": 344,
            "Naw": -1,  # number of total active bins per 2D sino
            # > number of sinos in span-11
            "NSN11": 837,
            # number of sinos in span-1
            "NSN1": 4084,
            # number of sinos in span-1 with no MRD limit
            "NSN64": Cnt["NRNG"] ** 2,
            # > maximum ring difference RD
            "MRD": 60,
            # span-1 (1), span-11 (11), ssrb (0)
            "SPN": 11,
            # > squared radius of the transaxial field of view
            "TFOV2": 890.0,  # squared radius of TFOV
            # > limit axial extension by defining start and end ring
            # > only works with span-1 (Cnt['SPN']==1)
            "RNG_STRT": 0,
            "RNG_END": Cnt["NRNG"],
            # > effective ring radius accounting for the depth of interaction
            "R_RING": Cnt["R"] + Cnt["DOI"],
            "R_2": float("{0:.6f}".format((Cnt["R"] + Cnt["DOI"]) ** 2)),
            # > inverse of the radius
            "IR_RING": float("{0:.6f}".format((Cnt["R"] + Cnt["DOI"]) ** -1)),
            # ------------------------------------------------------
            # > transaxial projection parameters (should be in
            # > with the parameters as defined in def.h for C files)
            # > parameters for each transaxial LOR
            "NTT": 10,
            # > all voxels intersected by a given LOR
            "NTV": 1807,
            # ------------------------------------------------------
        }
    )

    # > update with image voxel constants
    # Reference image size (usually the default from Siemens)
    # and GPU dimensions for optimal execution
    Cnt.update(
        SO_IMZ=127,
        SO_IMY=344,
        SO_IMX=344,
        SO_VXX=0.208626,
        SO_VXY=0.208626,
        SO_VXZ=0.203125,
        SZ_IMZ=127,
        SZ_IMY=320,
        SZ_IMX=320,
        SZ_VOXY=0.208626,
        SZ_VOXZ=0.203125,
        # SO_IMZ = 127,
        # SO_IMY = 384,
        # SO_IMX = 384,
        # SO_VXX = 0.1669,
        # SO_VXZ = 0.203125,
        # SO_VXY = 0.1669,
        # SZ_IMZ = 127,
        # SZ_IMY = 384,
        # SZ_IMX = 384,
        # SZ_VOXY = 0.1669,
        # SZ_VOXZ = 0.203125,
        # target scale factors for scatter mu-map and emission image respectively
        TRGTSCT=[0.5, 0.33],
    )

    # > update with image voxel constants
    Cnt.update(
        {
            # > resolution modelling sigma
            "SIGMA_RM": 0,
            # > radius PSF kernel size used in CUDA convolution
            "RSZ_PSF_KRNL": 8,
            # > affine and image size for the reconstructed image,
            # > assuming the centre of voxels in mm
            "AFFINE": array(
                [
                    [
                        -10 * Cnt["SO_VXX"],
                        0.0,
                        0.0,
                        5.0 * Cnt["SO_IMX"] * Cnt["SO_VXX"],
                    ],
                    [
                        0.0,
                        10 * Cnt["SO_VXX"],
                        0.0,
                        -5.0 * Cnt["SO_IMY"] * Cnt["SO_VXX"],
                    ],
                    [
                        0.0,
                        0.0,
                        10 * Cnt["SO_VXZ"],
                        -5.0 * Cnt["SO_IMZ"] * Cnt["SO_VXZ"],
                    ],
                    [0.0, 0.0, 0.0, 1.0],
                ]
            ),
            "IMSIZE": array([Cnt["SO_IMZ"], Cnt["SO_IMY"], Cnt["SO_IMX"]]),
            # > inverse size
            "SZ_VOXZi": round(1 / Cnt["SZ_VOXZ"], 6),
        }
    )


# =================================================================================================
# ============================ SIEMENS mMR SCANNER C O N S T A N T S ==============================

# Hardware (CT-based) mu-maps, which come with the mMR scanner.
# The names may be different
hrdwr_mu_mmr = [
    "umap_HNMCL_10606489.v.hdr",  # (1) Head and neck lower coil
    "umap_HNMCU_10606489.v.hdr",  # (2) Head and neck upper coil
    "umap_SPMC_10606491.v.hdr",  # (3) Spine coil
    "umap_PT_2291734.v.hdr",  # (4) Table
]


def get_mmr_constants():
    """
    Put all the constants together in a dictionary
    """

    # > get the baseline setup as well as GPU and third party setups
    Cnt = get_setup()

    # > update with the key constants
    Cnt.update(
        {
            "ISOTOPE": "F18",
            # > perform decay correction (True/False)
            "DCYCRR": True,
            # > bootstrap option for histogramming
            "BTP": 0,  # 1:non parametric bootstrap, 2: parametric bootstrap (recommended)
            "BTPRT": 1.0,  # Ratio of bootstrapped/original events (enables downsampling)
            # > bytes per event in list mode data
            "BPE": 4,
            # > LM header offset in bytes (for mMR it is in a separate DICOM format)
            "LMOFF": 0,
            # > crystal angle
            "ALPHA": 0.714286 * pi / 180,  # 2*pi/NCRS,
            # > number of rings (axially) and crystals (transaxially)
            "NRNG": 64,
            # > number of crystals transaxially
            "NCRS": 504,
            # > reduced number of crystals by the gaps (dead crystals)
            "NCRSR": 448,
            # > number of buckets for singles
            "NBCKT": 224,
            # number of direct sinograms (i.e., for segment 0)
            "NSEG0": 127,
            # > crystal gap period
            "TGAP": 9,
            # > crystal gap offset (used for getting the sino gaps right at the position)
            "OFFGAP": 1,
            # > axial crystal width
            "AXR": 0.40625,
            # > ring radius
            "R": 32.8,
            # > coincidence time window [ps]
            "CWND": 5859.38e-12,
            # > depth of interaction
            "DOI": 0.67,
            # > no of sinos in a segment out of 11 segments
            "SEG": array([127, 115, 115, 93, 93, 71, 71, 49, 49, 27, 27]),
            # > minimum and maximum ring difference for each segment
            "MNRD": array([-5, -16, 6, -27, 17, -38, 28, -49, 39, -60, 50]),
            "MXRD": array([5, -6, 16, -17, 27, -28, 38, -39, 49, -50, 60]),
            # > hardware mu-maps
            "HMULIST": hrdwr_mu_mmr,
        }
    )

    # > update with sinogram constants
    Cnt.update(
        {
            # > number of angular indexes in a 2D sinogram
            "NSANGLES": 252,
            # > number of bin indexes in a 2D sinogram
            "NSBINS": 344,
            "Naw": -1,  # number of total active bins per 2D sino
            # > number of sinos in span-11
            "NSN11": 837,
            # number of sinos in span-1
            "NSN1": 4084,
            # number of sinos in span-1 with no MRD limit
            "NSN64": Cnt["NRNG"] ** 2,
            # > maximum ring difference RD
            "MRD": 60,
            # span-1 (1), span-11 (11), ssrb (0)
            "SPN": 11,
            # > squared radius of the transaxial field of view
            "TFOV2": 890.0,  # squared radius of TFOV
            # > limit axial extension by defining start and end ring
            # > only works with span-1 (Cnt['SPN']==1)
            "RNG_STRT": 0,
            "RNG_END": Cnt["NRNG"],
            # > effective ring radius accounting for the depth of interaction
            "R_RING": Cnt["R"] + Cnt["DOI"],
            "R_2": float("{0:.6f}".format((Cnt["R"] + Cnt["DOI"]) ** 2)),
            # > inverse of the radius
            "IR_RING": float("{0:.6f}".format((Cnt["R"] + Cnt["DOI"]) ** -1)),
            # ------------------------------------------------------
            # > transaxial projection parameters (should be in
            # > with the parameters as defined in def.h for C files)
            # > parameters for each transaxial LOR
            "NTT": 10,
            # > all voxels intersected by a given LOR
            "NTV": 1807,
            # ------------------------------------------------------
        }
    )

    # > update with image voxel constants
    # Reference image size (usually the default from Siemens)
    # and GPU dimensions for optimal execution
    Cnt.update(
        SO_IMZ=127,
        SO_IMY=344,
        SO_IMX=344,
        SO_VXX=0.208626,
        SO_VXY=0.208626,
        SO_VXZ=0.203125,
        SZ_IMZ=127,
        SZ_IMY=320,
        SZ_IMX=320,
        SZ_VOXY=0.208626,
        SZ_VOXZ=0.203125,
        # SO_IMZ = 127,
        # SO_IMY = 384,
        # SO_IMX = 384,
        # SO_VXX = 0.1669,
        # SO_VXZ = 0.203125,
        # SO_VXY = 0.1669,
        # SZ_IMZ = 127,
        # SZ_IMY = 384,
        # SZ_IMX = 384,
        # SZ_VOXY = 0.1669,
        # SZ_VOXZ = 0.203125,
        # target scale factors for scatter mu-map and emission image respectively
        TRGTSCT=[0.5, 0.33],
    )

    # > update with image voxel constants
    Cnt.update(
        {
            # > resolution modelling sigma
            "SIGMA_RM": 0,
            # > radius PSF kernel size used in CUDA convolution
            "RSZ_PSF_KRNL": 8,
            # > affine and image size for the reconstructed image,
            # > assuming the centre of voxels in mm
            "AFFINE": array(
                [
                    [
                        -10 * Cnt["SO_VXX"],
                        0.0,
                        0.0,
                        5.0 * Cnt["SO_IMX"] * Cnt["SO_VXX"],
                    ],
                    [
                        0.0,
                        10 * Cnt["SO_VXX"],
                        0.0,
                        -5.0 * Cnt["SO_IMY"] * Cnt["SO_VXX"],
                    ],
                    [
                        0.0,
                        0.0,
                        10 * Cnt["SO_VXZ"],
                        -5.0 * Cnt["SO_IMZ"] * Cnt["SO_VXZ"],
                    ],
                    [0.0, 0.0, 0.0, 1.0],
                ]
            ),
            "IMSIZE": array([Cnt["SO_IMZ"], Cnt["SO_IMY"], Cnt["SO_IMX"]]),
            # > inverse size
            "SZ_VOXZi": round(1 / Cnt["SZ_VOXZ"], 6),
        }
    )

    # ------------------------------------------------------
    # S C A T T E R
    # > discretisation of the scatter angle spectrum for scatter LUT
    NCOS = 256

    # > cosine of max allowed scatter angle
    COSUPSMX = 0.725  # 0.58 #0.722 #Elow = E511/(2-cos(upsmx))

    # > scatter axial ring definition
    sct_irng = [0, 10, 19, 28, 35, 44, 53, 63]

    # -------Scatter image size in x,y,z directions
    # > transmission image
    SS_IMX = int(ceil(Cnt["TRGTSCT"][0] * Cnt["SO_IMX"]) // 2 * 2)
    SS_IMY = int(ceil(Cnt["TRGTSCT"][0] * Cnt["SO_IMY"]) // 2 * 2)
    SS_IMZ = int(ceil(Cnt["TRGTSCT"][0] * Cnt["SO_IMZ"]) // 2 * 2 - 1)
    SS_VXY = round((Cnt["SO_VXY"] * Cnt["SO_IMX"]) / SS_IMX, 6)
    SS_VXZ = round((Cnt["SO_VXZ"] * Cnt["SO_IMZ"]) / SS_IMZ, 6)
    IS_VXZ = round(1 / SS_VXZ, 6)

    # > emission image
    SSE_IMX = int(ceil(Cnt["TRGTSCT"][1] * Cnt["SO_IMX"]) // 2 * 2)
    SSE_IMY = int(ceil(Cnt["TRGTSCT"][1] * Cnt["SO_IMY"]) // 2 * 2)
    SSE_IMZ = int(ceil(Cnt["TRGTSCT"][1] * Cnt["SO_IMZ"]) // 2 * 2 + 1)
    SSE_VXY = round((Cnt["SO_VXY"] * Cnt["SO_IMX"]) / SSE_IMX, 6)
    SSE_VXZ = round((Cnt["SO_VXZ"] * Cnt["SO_IMZ"]) / SSE_IMZ, 6)
    # -------

    # > update with scatter constants
    Cnt.update(
        {
            # > scatter mu-map image size
            "SS_IMZ": SS_IMZ,
            "SS_IMY": SS_IMY,
            "SS_IMX": SS_IMX,
            "SS_VXZ": SS_VXZ,
            "SS_VXY": SS_VXY,
            "IS_VXZ": IS_VXZ,
            # > scatter emission image size
            "SSE_IMZ": SSE_IMZ,
            "SSE_IMY": SSE_IMY,
            "SSE_IMX": SSE_IMX,
            "SSE_VXZ": SSE_VXZ,
            "SSE_VXY": SSE_VXY,
            # > mu-map and emission image scaling [z,y,x]
            "SCTSCLEM": [
                float(SSE_IMZ) / Cnt["SO_IMZ"],
                float(SSE_IMY) / Cnt["SO_IMY"],
                float(SSE_IMX) / Cnt["SO_IMX"],
            ],
            "SCTSCLMU": [
                float(SS_IMZ) / Cnt["SO_IMZ"],
                float(SS_IMY) / Cnt["SO_IMY"],
                float(SS_IMX) / Cnt["SO_IMX"],
            ],
            # > idealised crystal surface (used for scatter modelling)
            "SRFCRS": 0.1695112,
            # > lower energy threshold (detection)
            "LLD": 430000,
            # > regular photon energy
            "E511": 511008,
            # > energy resolution
            "ER": 0.0,  # 0.154
            # > scatter ring indices
            "SIRNG": sct_irng,
            # > number of rings for scatter modelling
            "NSRNG": len(sct_irng),
            # > discretisation of the scatter angle spectrum for scatter LUT
            "NCOS": NCOS,
            "COSUPSMX": COSUPSMX,
            # > cosine step
            "COSSTP": (1 - COSUPSMX) / (NCOS - 1),
            # > inverse of cosine step
            "ICOSSTP": (NCOS - 1) / (1 - COSUPSMX),
            # > intensity emission image threshold to be considered for scatter modelling
            "ETHRLD": 0.05,
        }
    )
    # ---------------------------------------------------------

    # --- Time of Flight ---
    # > size of TOF bin in [ps]
    TOFBINS = 390e-12

    # > update with time-of-flight constants
    Cnt.update(
        {
            # > number of TOF bins
            "TOFBINN": 1,
            # > TOF bin width [ps]
            "TOFBINS": TOFBINS,
            # > size of TOF BIN in cm of travelled distance
            "TOFBIND": TOFBINS * Cnt["CLGHT"],
            # > inverse of the above
            "ITOFBIND": 1 / (TOFBINS * Cnt["CLGHT"]),
        }
    )

    # ---------------------------------------------------------

    return Cnt
