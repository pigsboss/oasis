<!-- page 1 of 12 -->

arXiv:1510.04556v5 [astro-ph.IM] 13 Dec 2019

manuscript no. oifits\_norm\_v2 December 16, 2019

c ESO 2019

# OIFITS 2: the 2<sup>nd</sup> version of the data exchange standard for optical interferometry ⋆

**Duvert, Gilles**<strong><sup>1</sup></strong>, 2**, Young, John**<strong><sup>3</sup></strong>**, Hummel, Christian**<strong><sup>4</sup></strong>

**1 Univ. Grenoble Alpes, IPAG, F-38000 Grenoble, France.** ⋆⋆

**2 CNRS, IPAG, F-38000 Grenoble, France.**

**3 Cavendish Laboratory, University of Cambridge, J J Thomson Avenue, Cambridge, UK.** ⋆⋆⋆

**4 European Southern Observatory, Karl-Schwarzschild-Str. 2, 85748 Garching** ⋆⋆⋆⋆

page 1 of 12

**Received; Accepted**

## ABSTRACT

**This paper describes version 2 of the Optical Interferometry exchange Format (OIFITS), the standard for exchanging calibrated data from optical (visible or infrared) interferometers. This IAU-endorsed standard has been in use for 10 years at most of the past and current optical interferometer projects, including COAST, NPOI, IOTA, CHARA, VLTI, PTI and the Keck interferometer. Software is available for reading, writing and merging OIFITS files. This version 2 provides definitions of additional data tables (for example for polarisation measurements), addressing the needs of future interferometric instruments. Also included are data columns for a more rigorous description of measurement errors and their correlations. In that, this document is a step towards the design of a common data model for optical interferometry. Finally, the main OIFITS header is expanded with several new keywords summarising the content to allow doing data base searches.**

**Key words. methods: data analysis – techniques: interferometric – instrumentation: interferometers – techniques: image processing – virtual observatory tools**

## 1. Introduction

**The exchange of data from optical and infrared interferometers between researchers has been greatly simplified by adopting a common format defined by Pauls et al. (2005) and now known as OIFITS version 1.**

**Since then, new interferometric instruments have introduced new capabilities such as sensitivity to polarisation, and new imaging techniques for multi-channel data have been developed that require the source spectrum – both of which were not contemplated in the first version of this format. Furthermore, as modern data archives such as the ESO Science Archive (Dolensky et al. 2008) require the presence of keywords in the FITS headers to enable searches based on, for example, target and instrument, such keywords need to be defined specifically for Optical Interferometry (OI).**

**Therefore, a revision of the standard became desirable (Young et al. 2008) and improvements have been discussed for two years on the JMMC forum at www.jmmc.fr/twiki/bin/view/Jmmc/OIFITSTwoProject.**

**The proposed enhancements have been endorsed by the former IAU Commission 54 and are described in the following text, including the formal definition of all extension tables, revised or not, for completeness. The reference for the new format shall consist of the original paper by Pauls et al. (2005) and this work.**

**In the following, the use of words like “must” and “should” follow the best current practice outlined in Bradner (1997).**

## 2. Purpose and Scope

**By defining and maintaining a common data format, we hope to encourage the development of common software for the analysis of data from optical interferometers, and to facilitate the exchange of data between di**ff**erent research groups.**

**The format was initially intended to only support the storage of calibrated, time-averaged data, and this is still its purpose today. Fully supporting other uses, such as describing raw data, observational history, data reduction recipes, etc. . . will require the development of a specific Data Model in the framework of the Virtual Observatory (VO, see** [**http://www.ivoa.net**](http://www.ivoa.net)**), which is beyond the scope of this paper.**

**However, even since version 1, the information stored in the OIFITS format was not entirely devoid of information about the instrument and interferometric array used. Practice, in particular for the AMBER instrument of VLTI (Petrov et al. 2007), has shown that OIFITS is adequate for storing semi-calibrated observations. Those are time series of instantaneous interferometric observables where instrumental bias has been removed and where error bars account for instrumental noise, known as level one (L1) data in the VO jargon.**

**Although the format presented here defines new keywords and tables that allow a more detailed description of the measured data, they are intended only for storing fully calibrated data: time averaged data, with all atmospheric and instrumental biases removed, known as L2 data in the VO jargon. Astronomers should use only fully calibrated OIFITS data to make inferences about the intrinsic brightness distribution of the observed target.**

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">⋆ We request that comments and suggestions related to OIFITS be directed to the OLBIN email list. (See [http://www.jmmc.fr/olbin-forum](http://www.jmmc.fr/olbin-forum) for information on how to subscribe and post to the list.)</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">⋆⋆ Correspondence: Gilles.Duvert@univ-grenoble-alpes.fr ⋆⋆⋆ Correspondence: jsy1001@mrao.cam.ac.uk</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">⋆⋆⋆⋆ Correspondence: chummel@eso.org</span></small>

Article number,

<!-- page 2 of 12 -->

manuscript no. oifits\_norm\_v2

**Interferometers are generally polarizing devices, but useful polarized optical interferometric observables have not been defined yet. However, we felt compelled to introduce some support for polarisation information. Without loss of generality, considering a number (hereafter NPOL) of distinct polarisation states for the observations leads to measurement of NPOL times all the interferometric observables. For example, if a Wollaston prism is used to make measurements on two orthogonal polarisation axes, we have NPOL=2.**

**In this document, we aim to keep the revised OIFITS tables compatible with their version 1. The only supplementary requirement for polarisation handling is that a distinct INSNAME must be assigned to each of the NPOL polarisations. A new optional OI\_INSPOL table is introduced. This table serves two purposes:**

**– It stores the polarisation transfer function of each beam for each INSNAME in the general form of Jones matrices (see Sect. 7.3).**

**– It serves as a hub for defining a relationship between all the polarized INSNAMEs. The intention is that, if this table is present, the data referenced by OI\_INSPOL (via INSNAME) shall be kept together during merging, copying or splitting of OIFITS files (unless the intention is to select a subset of the polarisations).**

**OIFITS version 2 provides an optional table to store the correlations between interferometric observables, whether in wavelength, baseline, or time. By analogy with the INSNAME keyword, we introduce a CORRNAME keyword that uniquely references a table, OI\_CORR, containing the sparse matrix representation of the correlations between selected observables of the dataset.**

**Finally, a drawback of OIFITS version 1 is also tackled here, namely the fact that the OI\_VIS table could contain several kinds of data, which were not distinguished in the earlier format: correlated flux, di**ff**erential (chromatic) visibilities and phases, or simply linear visibilities.**

**A reference implementation of this version of OIFITS has been developed by one of us (J. Young) in C, available at** [**https://github.com/jsy1001/oifitslib**](https://github.com/jsy1001/oifitslib)**. We anticipate that implementations in other languages (IDL, Python, Java. . . ) will be available in the near future.**

## 3. Definitions and Assumptions

**In this section we only present definitions related to new quantities stored by the format, and refer the reader to Pauls et al. (2005) for all other definitions and assumptions. In this text the word “error” refers to the square root of a (temporal, spatial, theoretical. . . ) variance.**

## 3.1. Differential Chromatic Visibility

**Di**ff**erential chromatic visibility (in Table 7) is defined here as the ratio of visibility amplitudes**

$$
V _ {\mathrm{diff}} (u, v, \lambda) = \frac {| V (u , v , \lambda) |}{| V _ {\mathrm{ref}} (u , v , \lambda) |}  ,\tag{1}
$$

**where** $| V _ { \mathrm { r e f } } ( u , \nu , \lambda ) |$ **is referred to as the** reference visibility **which is computed as a function of one or more** reference channels. **Thus, we consider here normalisation only to a reference derived from the data values themselves, rather than from model predictions. Such normalisation can be useful in cases where absolute**

**calibration cannot be achieved, but where spectral features relative to a continuum level are not a**ff**ected. One therefore needs to know, for each wavelength channel, which other channel had been used as reference. In case multiple channels have been used as the reference, the order of a wave-number polynomial function used to interpolate the reference visibility for the channel to be normalized shall be specified. The default order is zero, equivalent to a simple average**

$$
| V _ {\mathrm{ref}} (u, v, \lambda) | = <   | V (u, v, \lambda) | > _ {\Delta \lambda}.\tag{2}
$$

## 3.2. Differential Chromatic Phase

**Di**ff**erential chromatic phase (Millour et al. 2006) (see Table 7), is a phase di**ff**erence between two wavelengths. An additional calibration step often applied to di**ff**erential chromatic phase is to remove a wave-number slope or a higher-order polynomial from the observed phase** $\phi ( u , \nu , \lambda ) = \arg V ( u , \nu , \lambda )$

$$
\phi_ {\mathrm{diff}} (u, v, \lambda) = \phi (u, v, \lambda) - \phi_ {\mathrm{ref}} (u, v, \lambda) - \frac {\eta}{\lambda} - \frac {\zeta}{\lambda^ {2}} + \dots ,\tag{3}
$$

**where** $\phi _ { \mathrm { r e f } } ( u , \nu , \lambda ) = \arg V _ { \mathrm { r e f } } ( u , \nu , \lambda )$ is the phase at some ade**quately chosen reference channel that can, as in Eq. 1, be an average over multiple physical wavelength channels.**

## 3.3. Noise model for complex visibility

**Complex visibilities are the result of a coherent average which has removed the systematic phase noise induced by the atmosphere, either enabled by a fringe tracker, or o**ffl**ine analysis of dispersed fringes. At the level of estimates of the complex visibility from raw frames of the interferograms, the real and imaginary parts are uncorrelated (such as frames from an ABCD beam combiner, see Benisty et al. (2009)). The calibration of the averaged product causes the noise ellipse to be elongated, as amplitude and phase are subject to di**ff**erent sources of systematic error. For this reason, version 1 of the standard implemented an amplitude and phase representation of the (average calibrated) complex visibilities. Upcoming new instruments such as GRAV-ITY (Eisenhauer et al. 2011) will allow visibility phases to be tied to a phase reference (nearby star), providing a data reduction chain of complex visibilities without ever converting them to modulus of the amplitude and phase. For that reason, we propose a new revision of the OI\_VIS table which includes, in addition to the existing columns, optional storage for the real and imaginary parts of complex visibilities and their errors.**

Table 1. Keywords in OIFITS binary extension table headers.

| Keyword | Req. | Reason | Example |
| --- | --- | --- | --- |
| $TTPEn^{(1)}$ | yes | name of the column | T3PHIERR |
| $TUNITn^{(1)}$ | $yes^{(2)}$ | unit of datum | deg |
| $TDIMn^{(1)}$ | no | dimensionality of the data | (3,4) |
| DATASUM | no |  |  |
| CHECKSUM | no |  |  |

Notes. (1) “n” stands for the column number. (2) may be absent for unitless columns such as indexes.

Article number, page 2 of 12

<!-- page 3 of 12 -->

Duvert, Gilles, Young, John, Hummel, Christian: OIFITS 2

Table 2. OIFITS main header keywords. Keywords in bold face are standard FITS keywords. The type column gives the format in C-style notation, where %c is a single character, %s a string, %d is an integer number and %.xf is a real value with x decimal digits. Fixed values are written textually in the type column. This applies to the other Tables in this document. The third column indicates whether the keyword is required or not.

<table><tr><td>Keyword</td><td>Type</td><td>Req?</td><td>Description</td><td>Example</td></tr><tr><td>SIMPLE</td><td>T</td><td>yes</td><td>Standard FITS format</td><td></td></tr><tr><td>BITPIX</td><td>%d</td><td>yes</td><td>Number of bits per data pixel</td><td></td></tr><tr><td>NAXIS</td><td>%d</td><td>yes</td><td>Number of data  $axes^{(1)}$ </td><td>0</td></tr><tr><td>EXTEND</td><td>T</td><td>yes</td><td>Extensions may be present</td><td></td></tr><tr><td>ORIGIN</td><td>%s</td><td>yes</td><td>Institution responsible of file creation</td><td>ESO</td></tr><tr><td>DATE</td><td>%s</td><td>yes</td><td>Date the HDU was written</td><td>2015-01-13T16:12:56.57</td></tr><tr><td>DATE-OBS</td><td>%s</td><td>yes</td><td>Start date of observation</td><td>2014-10-15T18:33:26.06</td></tr><tr><td>CONTENT</td><td>%s</td><td>yes</td><td>Must contain only the string “OIFITS2” $^{(2)}$ </td><td>OIFITS2</td></tr><tr><td>AUTHOR</td><td>%s</td><td>no</td><td>As defined in FITS norm</td><td></td></tr><tr><td>DATASUM</td><td>%s</td><td>no</td><td>HDU  $datasum^{(6)}$ </td><td></td></tr><tr><td>CHECKSUM</td><td>%s</td><td>no</td><td>HDU  $checksum^{(6)}$ </td><td></td></tr><tr><td colspan="5">Keywords set to “MULTI” for heterogenous content of the OIFITS (see text)</td></tr><tr><td>TELESCOP</td><td>%s</td><td>yes</td><td>A generic identification of the  $ARRAY^{(3)}$ </td><td>CHARA</td></tr><tr><td>INSTRUME</td><td>%s</td><td>yes</td><td>A generic identification of the  $instrument^{(3)}$ </td><td>VEGA</td></tr><tr><td>OBSERVER</td><td>%s</td><td>yes</td><td>Who acquired the  $data^{(3)}$ </td><td>S.M.Eisenstein</td></tr><tr><td>OBJECT</td><td>%s</td><td>yes</td><td>Object  $Identifier^{(3)}$ </td><td>HD123456</td></tr><tr><td>INSMODE</td><td>%s</td><td>yes</td><td>Instrument  $mode^{(3)}$ </td><td>Low_JHK</td></tr><tr><td>REFERENC</td><td>%s</td><td>no</td><td>Bibliographic  $reference^{(3)}$ </td><td>2017A&amp;A...597A...8D</td></tr><tr><td>PROG_ID</td><td>%s</td><td>no</td><td>Program  $ID^{(3)}$ </td><td>094.A-1234</td></tr><tr><td>PROCSOFT</td><td>%s</td><td>no</td><td>Versioned Data Reduction  $Software^{(3,4)}$ </td><td>pndrs 2.6</td></tr><tr><td>OBSTECH</td><td>%s</td><td>no</td><td> $Technique\ of\ observation^{(3,5)}$ </td><td>SCAN, ABCD-PH, PH_REF...</td></tr><tr><td colspan="5">Suggested supplementary keywords for “atomic” observations (see text)</td></tr><tr><td>RA</td><td>%f</td><td>no</td><td>Target Right Ascension at mean EQUINOX (deg)</td><td></td></tr><tr><td>DEC</td><td>%f</td><td>no</td><td>Target Declination at mean EQUINOX (deg)</td><td></td></tr><tr><td>EQUINOX</td><td>%.1f</td><td>no</td><td>Standard FK5 (years)</td><td>2000.0</td></tr><tr><td>RADECSYS</td><td>%s</td><td>no</td><td>Coordinate reference frame</td><td>FK5</td></tr><tr><td>SPECSYS</td><td>%s</td><td>no</td><td>Reference frame for spectral coord.</td><td>TOPOCENTR</td></tr><tr><td>TEXPTIME</td><td>%f</td><td>no</td><td>Maximum elapsed time for data point (s)</td><td></td></tr><tr><td>MJD-OBS</td><td>%.8f</td><td>no</td><td>Start of observations (MJD)</td><td></td></tr><tr><td>MJD-END</td><td>%.8f</td><td>no</td><td>End of observations (MJD)</td><td></td></tr><tr><td>BASE_MIN</td><td>%f</td><td>no</td><td>Minimum projected baseline length (m)</td><td>16.01</td></tr><tr><td>BASE_MAX</td><td>%f</td><td>no</td><td>Maximum projected baseline length (m)</td><td>100.12</td></tr><tr><td>WAVELMIN</td><td>%f</td><td>no</td><td>Minimum wavelength (nm)</td><td>1200</td></tr><tr><td>WAVELMAX</td><td>%f</td><td>no</td><td>Maximum wavelength (nm)</td><td>1600</td></tr><tr><td>NUM_CHAN</td><td>%d</td><td>no</td><td>Total number of spectral channels</td><td>32</td></tr><tr><td>SPEC_RES</td><td>%f</td><td>no</td><td>Reference spectral resolution ( $\lambda/\Delta_{\lambda}$ )</td><td>38323.56</td></tr><tr><td>VIS2ERR</td><td>%f</td><td>no</td><td>Representative  $V^{2}$  error (%)</td><td>5.3</td></tr><tr><td>VISPHERR</td><td>%f</td><td>no</td><td>Representative Diff. Vis. Phase error (deg)</td><td>1.08</td></tr><tr><td>T3PHIERR</td><td>%f</td><td>no</td><td>Representative Closure Phase error (deg)</td><td>32.65</td></tr></table>

Notes. (1) Should be “0” unless a FITS image or cube is present after the main header. (2) Mandatory. Identifies the FITS file as an OIFITS version 2 file. (3) These are bookeeping keywords. Some of them can be inferred from the headers of the tables contained in the OIFITS file. If the file is of “atomic” type (see text), all these keyords must be filled up by the relevant value. If the OIFITS acts as a container for heterogenous data and thus more than one value of the keyword would be needed, use “MULTI”. (4) Data Reduction Software (DRS) with version identification. (5) Identifiers for OBSTECH are not standardized here. (6) see Sect. 4.

## 4. OIFITS File Structure

**OIFITS files must comply with the FITS standard (Hanisch et al. 2001), where shall be found acronyms and symbols not defined in this document. OIFITS files use binary table extensions following the primary header-data unit. Data types for each column are defined by the value of the TFORMn keywords in each extension headers. This version introduces the use of the data type J (32 bit integers).**

**In addition to the mandatory FITS binary extension keywords defined in Hanisch et al. (2001), the keywords described in Table 1 must be present in the table headers. We recommend the use of DATASUM and CHECKSUM**

**in the main header and all table headers, as described in** [http://fits.gsfc.nasa.gov/registry/checksum/checksum.pdf](http://fits.gsfc.nasa.gov/registry/checksum/checksum.pdf)**TUNITn values are mandatory for all columns except those representing unitless values (such as STA\_INDEX), which are represented by the FITS null string (all spaces). Any other keyword is expected to be ignored by OIFITS readers. The FITS format defines a null value for each supported data type. The OIFITS format uses these type-dependent null values to identify individual data as being unmeasured, invalid, etc. . . and this document refers to such values as NULL.**

Article number,

page 3 of 12

<!-- page 4 of 12 -->

manuscript no. oifits\_norm\_v2

## 4.1. Primary Header

**While the primary header was minimal in OIFITS version 1, we have added in Table 2 three small sets of keywords. They add ancillary information on, for example, the provenance of the OIFITS file itself, (ORIGIN, AUTHOR), of the data (TELESCOP, INSTRUME, REFERENC, PROG\_ID), on the observational method used (INSMODE, PROCSOFT, OBSTECH).**

**It is customary now to add in a FITS primary header other keywords enabling quick searches for observations matching certain criteria in a database or archive of OIFITS files, such as the JMMC’s optical interferometry database, at** [**http://oidb.jmmc.fr/index.html**](http://oidb.jmmc.fr/index.html)**. For example, the information about minimum and maximum baseline lengths used in the OIFITS file may be important for selecting only data resolving a target or providing a good** uv**-coverage for imaging. As the majority of instruments now provide data for multiple wavelength channels, the wavelength range recorded is a useful search parameter, as is the spectral resolution. Finally, the maximum elapsed time for a data point can be important information when searching for data on a wide binary where fringe smearing is a concern. These values are easily computable on-the-fly from the tables contained in the OIFITS file, since the amount of (reduced) data in an OIFITS file is still small.**

**For OIFITS writers needing to add such ancillary information in the main header, we suggest using the additional keywords listed in Table 2. These keywords are intended primarily for “atomic” OIFITS (one target, one instrument and instrument mode, one observing date, etc. . . ) where there is no need to describe multiple (keyword value MULTI) observations. It is out of the scope of this document to further normalize the main header keywords for cases where the OIFITS file is**

Table 3. OI\_TARGET (revision 2)

<table><tr><td>Label</td><td>Data Type</td><td>Description</td></tr><tr><td colspan="3">Keywords</td></tr><tr><td>OI_REVN</td><td>2</td><td>Revision number: 2</td></tr><tr><td colspan="3">Column Headings (one row for each source)</td></tr><tr><td>TARGET_ID</td><td>I (1)</td><td>Index number. Must be ≥ 1</td></tr><tr><td>TARGET</td><td>A (32)</td><td>Target name(2)</td></tr><tr><td>RAEP0</td><td>D (1)</td><td>R.A. at mean EQUINOX (deg)</td></tr><tr><td>DECEP0</td><td>D (1)</td><td>DEC. at mean EQUINOX (deg)</td></tr><tr><td>EQUINOX</td><td>E (1)</td><td>Equinox(1)</td></tr><tr><td>RA_ERR</td><td>D (1)</td><td>Error in R.A. (deg)</td></tr><tr><td>DEC_ERR</td><td>D (1)</td><td>Error in Decl. (deg)</td></tr><tr><td>SYSVEL</td><td>D (1)</td><td>Systemic radial velocity (m s-1)</td></tr><tr><td>VELTYP</td><td>A (8)</td><td>Reference for radial velocity: (&quot;LSR&quot;, &quot;GEOCENTR&quot;, etc.)</td></tr><tr><td>VELDEF</td><td>A (8)</td><td>Definition of radial velocity: (&quot;OPTICAL&quot;, &quot;RADIO&quot;)</td></tr><tr><td>PMRA</td><td>D (1)</td><td>Proper motion in R.A. (deg yr-1)</td></tr><tr><td>PMDEC</td><td>D (1)</td><td>Proper motion in Decl. (deg yr-1)</td></tr><tr><td>PMRA_ERR</td><td>D (1)</td><td>Error of proper motion in R.A. (deg yr-1)</td></tr><tr><td>PMDEC_ERR</td><td>D (1)</td><td>Error of proper motion in Decl. (deg yr-1)</td></tr><tr><td>PARALLAX</td><td>E (1)</td><td>Parallax (deg)</td></tr><tr><td>PARA_ERR</td><td>E (1)</td><td>Error in parallax (deg)</td></tr><tr><td>SPECTYP</td><td>A (32)</td><td>Spectral type(2)</td></tr><tr><td>CATEGORY</td><td>A (3)</td><td>(optional) &quot;CAL&quot; or &quot;SCI&quot;</td></tr></table>

Notes. (1) The use of EQUINOX = 2000.0 is recommended. (2) strings of length lesser than 32 are allowed for backwards compatibility, but should trigger a warning on reading the file.

**a container of heterogenous data, those properties being more related to the problems of database management than to a physical description of interferometric observables. Nevertheless, see** [**http://www.eso.org/sci/observing/phase3/p3sdpstd.pdf**](http://www.eso.org/sci/observing/phase3/p3sdpstd.pdf)**for a candidate standardisation of such ancillary keywords.**

## 4.2. Table content

**A valid OI exchange-format FITS file must contain one (and only one) OI\_TARGET table, one or more OI\_ARRAY tables, one or more OI\_WAVELENGTH tables, plus any number of the data tables: OI\_VIS, OI\_VIS2, or OI\_T3. Each data table must refer to an OI\_WAVELENGTH and OI\_ARRAY table that are present in the file. The requirement for the presence of an OI\_ARRAY table was not part of version 1 of the format. All other new tables are optional. The revision number of the revised tables is equal to two, while it is equal to one for the new tables. Any future changes will require increments in the revision numbers of the altered tables.**

**If multiple tables of the same EXTNAME are present, each of them must have a unique value of the EXTVER keyword, as mandated by the FITS standard.**

**The tables can appear in any order. Other header-data units may appear in the file, provided their EXTNAMEs do not begin with “OI\_”. Each instance of a table defined here must contain all the listed columns and header keywords, in no particular order.**

**Any of the tables may have extra keywords or columns beyond those defined in the standard. It would facilitate the addition of new keywords and columns in future releases of the standard if the non-standard keywords and column names were given a particular prefix, such as “NS\_”, to avoid conflicts.**

## 5. Target and instrument information tables

## 5.1. OI\_TARGET (revision 2)

**Keywords for the OI\_TARGET table are listed in Table 3. The only di**ff**erences from revision 1 are the optional additional column giving the category assigned to a target for the purpose of calibrating the data, and the recommendation to use EQUINOX 2000 for coordinates.**

**It is standard practice to interleave observations of science targets (SCI category) with observations of targets of known angular size (CAL category), to allow to calibrate the interferometric observables for the science objects. The optional column CATEGORY has been introduced for convenience as a reminder of the initial intent for observing each target. Its presence does not imply any particular data reduction level for the data stored in the other tables.**

## 5.2. OI\_ARRAY (revision 2)

**Keywords for the OI\_ARRAY table are listed in Table 4. As defined, the OI\_ARRAY tables are mostly aimed at groundbased interferometry with separated telescopes but could be used for other cases depending on the value of the FRAME keyword. Each OI\_ARRAY table in a file must have a unique value for ARRNAME. The stations involved in any of the interferometric observables stored in the other tables of a single OIFITS are identified via the STA\_INDEX column. To be valid, an OIFITS file shall be written so that every combination of ARRNAME and STA\_INDEX must refer to a unique OI\_ARRAY entry that is present in the file.**

Article number, page 4 of 12

<!-- page 5 of 12 -->

Duvert, Gilles, Young, John, Hummel, Christian: OIFITS 2

Table 4. OI\_ARRAY (revision 2)

<table><tr><td>Label</td><td>Data Type</td><td>Description</td></tr><tr><td colspan="3">Keywords</td></tr><tr><td>OI_REVN</td><td>2</td><td>Revision number: 2</td></tr><tr><td>ARRNAME</td><td>%s</td><td>Array name, for cross-referencing</td></tr><tr><td>FRAME</td><td>%s</td><td>Coordinate frame</td></tr><tr><td>ARRAYX</td><td>%f</td><td></td></tr><tr><td>ARRAYY</td><td>%f</td><td>Array center coordinates (m)</td></tr><tr><td>ARRAYZ</td><td>%f</td><td></td></tr><tr><td colspan="3">Column Headings (one row for each array element)</td></tr><tr><td>TEL_NAME</td><td>A (16)</td><td>Telescope name</td></tr><tr><td>STA_NAME</td><td>A (16)</td><td>Station name</td></tr><tr><td>STA_INDEX</td><td>I (1)</td><td>Station number. Must be ≥ 1</td></tr><tr><td>DIAMETER</td><td>E (1)</td><td>Element diameter (m)</td></tr><tr><td>STAXYZ</td><td>D (3)</td><td>Station coordinates w.r.t. array center (m)</td></tr><tr><td>FOV</td><td>D (1)</td><td>Photometric field of view (arc sec)</td></tr><tr><td>FOVTYPE</td><td>A (6)</td><td>Model for FOV: “FWHM” or “RADIUS”</td></tr></table>

**Several interferometric observables stored in the OIFITS format are expressed as a ratio of a correlated flux to an incoherent flux. The area on the sky contributing to the latter is the photometric field of view (PFOV), and would typically be the PSF of a telescope in the array, the acceptance cone of an optical fiber, the di**ff**raction pattern of a pinhole spatial filter. . . Therefore, we have added two columns to the OI\_ARRAY table, FOV, which gives the radius of PFOV and FOVTYPE, which specifies whether the PFOV radial profile is Gaussian or rectangular.**

**The interferometric field of view (IFOV), over which photons received contribute to the correlated flux, is smaller than the PFOV, especially for co-axial Michelson beam combiners. In this case, the IFOV can be computed for each (**u, v**) data point with the information from the OI\_WAVELENGTH table, since** in this case $\begin{array} { r } { \mathrm { I F O V } \; = \; \frac { \lambda ^ { 2 } } { B \times \Delta _ { \lambda } } , } \end{array}$ **where** λ **is the wavelength,** $\Delta _ { \lambda }$ **the spectral width and** B **the projected baseline length. The IFOV is also limited by the integration time, which, if too long, will cause fringe smearing for image pixels far away from the phase center.**

## Coordinate frame

**If the FRAME keyword has the value GEOCENTRIC, then the coordinates are given in an earth-centered, earth-fixed, Cartesian reference frame. The origin of the coordinates is the earth’s center of mass. The** z **axis is parallel to the direction of the conventional origin for polar motion. The** x **axis is parallel to the direction of the intersection of the Greenwich meridian with the mean astronomical equator. The** y **axis completes the right-handed, orthogonal coordinate system.**

**We add an alternative value for FRAME, namely SKY, for data from sparse aperture masks, where the** x **axis points East, the** y **axis North and the** z **axis completes the right-handed coordinate frame (the aperture mask rotates with the sky). In this case, the ARRAYX, ARRAYY, and ARRAYZ coordinates must be zero.**

## 5.3. OI\_WAVELENGTH (revision 2)

**Keywords for the OI\_WAVELENGTH table are listed in Table 5. This table was introduced in the first version of the format to store the e**ff**ective wavelength and bandwidth for each spectral channel of an instrument (identified by the INSNAME keyword). The number of spectral channels in the instrument is the number**

**of rows in this table, that is, the NAXIS2 value, referred to as NWAVE in this document.**

**In this revision, we introduce the possibility of storing purely monochromatic values (EFF\_BAND**=**0) in OI\_WAVELENGTH, since such a table can be referenced, via the INSNAME keyword, by a new table, OI\_FLUX, which may contain monochromatic spectra (see Sect. 7.1).**

## Name of detector

**Each OI\_WAVELENGTH table in a file must have a unique value for INSNAME. Particular attention to this point is recommended when aggregating OIFITS files which may have similar INSNAME values but di**ff**erent channel wavebands.**

## Wavelengths

**Each OI\_WAVELENGTH table describes either the spectral response of detector(s) with a number of spectral channels (traditional use defined in version 1 of the format), or the wavelengths of a monochromatic spectrum. In the latter case, EFF\_WAVE contains the spectrum’s wavelengths and the EFF\_BAND values are all zeros. In the former case, each table gives the observation wavelengths for one or more of the data tables (OI\_VIS, OI\_VIS2, OI\_T3), and will often correspond to a single physical detector.**

**The EFF\_WAVE column shall contain the best available estimate of the e**ff**ective wavelength of each spectral channel, and the EFF\_BAND column shall contain the best available estimate of the e**ff**ective half-power bandwidth. These estimates should include the e**ff**ect of the earth’s atmosphere, but not the spectrum of the target. (The e**ff**ect of the target spectrum should be taken into account as part of any model-fitting or mapping process, in other words, the target spectrum is part of the model.)**

## 6. Data Tables

**The tables containing observed data are the OI\_VIS2, OI\_VIS, OI\_T3 and OI\_FLUX tables.**

## 6.1. Properties shared by all data tables

Start date of observations

**This shall be a UTC date in the format YYYY-MM-DD, for example** $1997-07-28$ **. In OIFITS version 2 only MJD and DATE-OBS must be used to express time. The TIME column is retained only for backwards compatibility and must contain zeros . The value in the MJD column shall be the mean UTC time of the measurement expressed as a modified Julian Day.**

Table 5. OI\_WAVELENGTH (revision 2)

<table><tr><td>Label</td><td>Data Type</td><td>Description</td></tr><tr><td colspan="3">Keywords</td></tr><tr><td>OI_REVN</td><td>2</td><td>Revision number: 2</td></tr><tr><td>INSNAME</td><td>%s</td><td>Name of detector, for cross-referencing</td></tr><tr><td colspan="3">Column Headings (one row for each wavelength channel)</td></tr><tr><td>EFF_WAVE</td><td>E (1)</td><td>Effective wavelength of channel (m)</td></tr><tr><td>EFF_BAND</td><td>E (1)</td><td>Effective bandpass of channel (m)</td></tr></table>

Article number,

page 5 of 12

<!-- page 6 of 12 -->

manuscript no. oifits\_norm\_v2

## Integration time

**The exchange format will normally be used for interchange of time-averaged data. The “integration time” INT\_TIME is therefore the length of time over which the data were averaged to yield the given data point. In order that this information is useful when computing the e**ff**ect of fringe smearing in the case of imaging distant companions or large structures, INT\_TIME shall correspond to the time elapsed between the first and last recorded interferograms (frames) averaged to obtain a given data point.**

## Cross-referencing

**Cross-referencing between FITS tables is not a generic feature of the FITS format, but is necessary for correct description of the interferometric data. When writing OIFITS tables, particular care must be taken to maintain the cross-references. Specifically, each data table must refer:**

**– to a particular OI\_WAVELENGTH table describing the wavelength channels for the measurements, via the INSNAME keyword; and**

**– to an OI\_ARRAY table, via the ARRNAME keyword; and**

**– optionally, to the OI\_INSPOL table containing the same INSNAME; and**

**– optionally, to an OI\_CORR table via the CORRNAME keyword.**

**There is a second level of cross-referencing possible, between table elements. Indeed, interferometric observables stored in an OIFITS file are physically associated: a phase closure in T3PHI, for example, can be the argument of the closure of three complex values whose squared norms are stored in three rows of the VIS2DATA column. Usually, the MJD column contains the same timestamp for all the simultaneous – therefore, related – observables, and su**ffi**ces to link them. It should be stressed however that, according to the definition of MJD above, timestamps for two related observables can di**ff**er: values in an OIFITS being averaged and calibrated, the number of raw data used in the average, or the calibration process, may change the mean UTC time of the measurement even between related observables.**

**Data producers that want to add a more direct link than MJD between related quantities in di**ff**erent tables can add a non-standard column in the relevant tables, such as a NS\_DATAINDEX column of TFORMn value ’J’, containing integer hash numbers.**

## Flag

**If a value in this vector is true, the corresponding datum must be ignored in all analysis.**

## 6.2. OI\_VIS2 (revision 2)

**Keywords for the OI\_VIS2 table are listed in Table 6.**

## Data arrays

**NWAVE is the number of spectral channels, given by the NAXIS2 keyword of the relevant OI\_WAVELENGTH table.**

## UV coordinates

**UCOORD, VCOORD give the (**u, v**) coordinates in meters of the point in the UV plane associated with the vector of visibilities. The data points may be averages over some region of the UV plane,**

**but the current version of the standard says nothing about the averaging process.**

## 6.3. OI\_VIS (revision 2)

**Keywords for the OI\_VIS table are listed in Table 7. This table has been used in the past to store the amplitude and phase of visibilities obtained through phase-preserving coherent integration. This revision intends to enable storage of complex co-herent fluxes, visibilities and di**ff**erential chromatic visibilities, uniquely identified so they can be modeled without ambiguity.**

## New keywords and columns

**There are four new keywords in the header, AMPTYP, PHITYP, AMPORDER, and PHIORDER.**

**AMPTYP defines the type of data stored in VISAMP: absolute, differential or correlated flux. In the last case the usual TUNITn FITS keyword must be used to specify the flux unit (such as photon, count, Jy, adu, see footnote 1).**

**PHITYP is one of absolute or differential. The default for AMPTYP and PHITYP, if not present, is absolute.**

**If AMPTYP or PHITYP is differential, the newly-defined data column VISREFMAP must be present since this column contains the channel number(s) whose combination defines the reference channel used in computing the VISAMP and VISPHI values. The** i<sup>th</sup> **row of the 2-D matrix VISREFMAP specifies the reference channels for channel** i**. (In FITS the first dimension corresponds to the most rapidly varying index, also known as columnmajor ordering. This internal ordering is usually hidden by the low-level FITS libraries such as cfitsio.)**

**The combination of the channels in VISREFMAP defaults to a simple average, unless a polynomial fit of some order is defined through AMPORDER or PHIORDER.**

**If both VISAMP and VISPHI are di**ff**erential, VISREFMAP shall apply to both. VISREFMAP must be present if either VISTYP or PHITYP is differential. If VISREFMAP is absent, neither can be di**ff**erential.**

**OI\_VIS revision 2 implements new optional columns RVIS and IVIS allowing the storage of complex visibilities or complex fluxes in (Real, Imaginary) representation rather than amplitude and phase. RVIS, IVIS and their associated errors RVISERR and IVISERR may be omitted. Their unit is given by the standard table header TUNITn keywords. Covariances between elements of the RVIS and IVIS vectors can be stored using the general OI\_CORR sparse correlation matrix mechanism via the CORRINDX\_RVIS and CORRINDX\_IVIS columns.**

## Data arrays

**As in revision 1, FLAG applies to VISAMP, VISAMPERR, VISPHI and VISPHIERR. VISAMP and VISPHI, as well as their associated errors VISAMPERR and VISPHIERR, can be NULL in the cases where the flag mechanism is not applicable, for example, if the instrument computes only VISPHI, or if flagging some incorrect VISAMP values would flag otherwise good VISPHI values. Similarly, if some values of RVIS or IVIS or RVISERR or IVISERR are meaningless, NULL values are to be used instead.**

**NWAVE is the number of spectral channels, given by the NAXIS2 keyword of the relevant OI\_WAVELENGTH table.**

Article number, page 6 of 12

<!-- page 7 of 12 -->

Duvert, Gilles, Young, John, Hummel, Christian: OIFITS 2

Table 6. OI\_VIS2 (revision 2)

<table><tr><td>Label</td><td>Data Type</td><td>Description</td></tr><tr><td colspan="3">Keywords</td></tr><tr><td>OI_REVN</td><td>2</td><td>Revision number: 2</td></tr><tr><td>DATE-OBS</td><td>%s</td><td>UTC start date of observations</td></tr><tr><td>ARRNAME</td><td>%s</td><td>Identifies corresponding OI_ARRAY</td></tr><tr><td>INSNAME</td><td>%s</td><td>Identifies corresponding OI_WAVELENGTH table</td></tr><tr><td>CORRNAME</td><td>%s</td><td>(optional) Identifies corresponding OI_CORR table</td></tr><tr><td colspan="3">Column Headings (one row for each measurement)</td></tr><tr><td>TARGET_ID</td><td>I (1)</td><td>Target number as index into OI_TARGET table</td></tr><tr><td>TIME</td><td>D (1)</td><td>Zero. For backwards compatibility</td></tr><tr><td>MJD</td><td>D (1)</td><td>Modified Julian Day</td></tr><tr><td>INT_TIME</td><td>D (1)</td><td>Integration time (s)</td></tr><tr><td>VIS2DATA</td><td>D (NWAVE)</td><td>Squared Visibility</td></tr><tr><td>VIS2ERR</td><td>D (NWAVE)</td><td>Error in Squared Visibility</td></tr><tr><td>CORRINDX_VIS2DATA</td><td>J (1)</td><td>(optional) Index into correlation matrix for 1st VIS2DATA element</td></tr><tr><td>UCOORD</td><td>D (1)</td><td>U coordinate of the data (m)</td></tr><tr><td>VCOORD</td><td>D (1)</td><td>V coordinate of the data (m)</td></tr><tr><td>STA_INDEX</td><td>I (2)</td><td>Station numbers contributing to the data</td></tr><tr><td>FLAG</td><td>L (NWAVE)</td><td>Flag</td></tr></table>

## UV coordinates

**UCOORD, VCOORD give the (**u, v**) coordinates in meters of the point in the UV plane associated with the vector of visibilities – see Sect. 3 for details. The data points may be averages over some region of the UV plane, but the current version of the standard says nothing about the averaging process.**

## 6.4. OI\_T3 (revision 2)

**Keywords for the OI\_T3 table are listed in Table 8.**

## Data arrays

**FLAG marks both the corresponding bispectrum amplitude (T3AMP) and phase (T3PHI) as invalid. To mark only the amplitude or phase as invalid, the relevant data values must be replaced by NULL (with FLAG remaining as false). If the dataset does not provide triple product amplitudes at all, T3AMP and T3AMPERR must contain only NULL values.**

**NWAVE is the number of spectral channels, given by the NAXIS2 keyword of the relevant OI\_WAVELENGTH table.**

## Triple product UV coordinates

**The U1COORD, V1COORD, U2COORD, and V2COORD columns contain the (**u, v**) coordinates of the bispectrum point in meters. U3COORD and V3COORD are not given since** u<sub>1</sub> + u<sub>2</sub> + u3 = $0   ,   v_{1} + v_{2} + v_{3} = 0$ . The corresponding data points may be av**erages in (bi-) spatial frequency space, but this version of the standard does not attempt to describe the averaging process.**

## 7. Optional Tables

## 7.1. OI\_FLUX (revision 1)

**OIFITS version 2 introduces this optional table intended as a container for raw or calibrated flux measurements. Corresponding wavelengths are referenced with the INSNAME keyword. The content of the table depends on the single-character keyword**

**header CALSTAT. Keywords for the OI\_FLUX table are listed in Table 9. FLUXDATA and FLUXERR are in units of their corresponding TUNIT, which must be present**<strong><sup>1</sup></strong>.

**If CALSTAT is C (Calibrated), the fluxes listed are fluxcalibrated spectra obtained with the interferometric instrument itself, if it provides such a measurement, or with another instrument. In both cases this spectrum is useful for modeling sources with physical emission components where it provides the constraint of the total flux. The spectrum is the spectrum of the object and does not depend on the telescope used: the table shall not contain ARRNAME and STA\_INDEX.**

**If CALSTAT is U (Uncalibrated), ARRNAME and the STA\_INDEX column must be present, and the flux stored in FLUXDATA is the flux measured on the telescope of array ARRNAME indicated by STA\_INDEX. In this case, the table shall not contain FOV and FOVTYPE. (The field of view is given in the OI\_WAVELENGTH table referenced by INSNAME.)**

## Data arrays

**NWAVE is the number of distinct channels, given by the NAXIS2 keyword of the relevant OI\_WAVELENGTH table.**

## 7.2. OI\_CORR (revision 1)

**There is a need to describe correlations between any kinds of OIFITS observables, over a limited timespan (hours at most) determined by the calibration procedures. For an example where such correlations are derived, see Perrin (2003).**

**The following addition to the standard allows the definition of a set of correlated real-valued data {**x<sub>i</sub>**} that may span multiple OIFITS tables, of any type. Data may be correlated in wavelength, baseline, or time. Correlations between di**ff**erent kinds of observable can also be described. An OIFITS file may contain multiple such sets, to accommodate merging of multiple data**

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">1 See Appendix B.1 of the IVOA Spectral Data Model document available at [http://www.ivoa.net/documents/SpectralDM](http://www.ivoa.net/documents/SpectralDM) for examples. A FITS empty string (a minimum of eight whitespaces) is a valid value for a TUNIT keyword.</span></small>

Article number,

page 7 of 12

<!-- page 8 of 12 -->

manuscript no. oifits\_norm\_v2

Table 7. OI\_VIS (revision 2)

<table><tr><td>Label</td><td>Data Type</td><td>Description</td></tr><tr><td colspan="3">Keywords</td></tr><tr><td>OI_REVN</td><td>2</td><td>Revision number: 2</td></tr><tr><td>DATE-OBS</td><td>%s</td><td>UTC start date of observations</td></tr><tr><td>ARRNAME</td><td>%s</td><td>Identifies corresponding OI_ARRAY</td></tr><tr><td>INSNAME</td><td>%s</td><td>Identifies corresponding OI_WAVELENGTH table</td></tr><tr><td>CORRNAME</td><td>%s</td><td>(optional†) Identifies corresponding OI_CORR table</td></tr><tr><td>AMPTYP</td><td>%s</td><td>(optional†) “absolute”, “differential”, “correlated flux”</td></tr><tr><td>PHITYP</td><td>%s</td><td>(optional†) “absolute”, “differential”</td></tr><tr><td>AMPORDER</td><td>%d</td><td>(optional†) Polynomial fit order for differential chromatic amplitudes</td></tr><tr><td>PHIORDER</td><td>%d</td><td>(optional†) Polynomial fit order for differential chromatic phases</td></tr><tr><td colspan="3">Column Headings (one row for each measurement)</td></tr><tr><td>TARGET_ID</td><td>I (1)</td><td>Target number as index into OI_TARGET table</td></tr><tr><td>TIME</td><td>D (1)</td><td>Zero. For backwards compatibility</td></tr><tr><td>MJD</td><td>D (1)</td><td>Modified Julian Day</td></tr><tr><td>INT_TIME</td><td>D (1)</td><td>Integration time (s)</td></tr><tr><td>VISAMP</td><td>D (NWAVE)</td><td>Visibility amplitude</td></tr><tr><td>VISAMPERR</td><td>D (NWAVE)</td><td>Error in visibility amplitude</td></tr><tr><td>CORRINDX_VISAMP</td><td>J (1)</td><td>(optional) Index into correlation matrix for 1st VISAMP element</td></tr><tr><td>VISPHI</td><td>D (NWAVE)</td><td>Visibility phase in degrees</td></tr><tr><td>VISPHIERR</td><td>D (NWAVE)</td><td>Error in visibility phase in degrees</td></tr><tr><td>CORRINDX_VISPHI</td><td>J (1)</td><td>(optional) Index into correlation matrix for 1st VISPHI element</td></tr><tr><td>VISREFMAP</td><td>L (NWAVE,NWAVE)</td><td>(optional†) Matrix of indexes for establishing the reference channels (see text).</td></tr><tr><td>RVIS</td><td>D (NWAVE)</td><td>(optional) Complex coherent flux (Real) in units of TUNITn</td></tr><tr><td>RVISERR</td><td>D (NWAVE)</td><td>(optional) Error on RVIS</td></tr><tr><td>CORRINDX_RVIS</td><td>J (1)</td><td>(optional) Index into correlation matrix for 1st RVIS element</td></tr><tr><td>IVIS</td><td>D (NWAVE)</td><td>(optional) Complex coherent flux (Imaginary) in units of TUNITn</td></tr><tr><td>IVISERR</td><td>D (NWAVE)</td><td>(optional) Error on IVIS</td></tr><tr><td>CORRINDX_IVIS</td><td>J (1)</td><td>(optional) Index into correlation matrix for 1st IVIS element</td></tr><tr><td>UCOORD</td><td>D (1)</td><td>U coordinate of the data (m)</td></tr><tr><td>VCOORD</td><td>D (1)</td><td>V coordinate of the data (m)</td></tr><tr><td>STA_INDEX</td><td>I (2)</td><td>Station numbers contributing to the data</td></tr><tr><td>FLAG</td><td>L (NWAVE)</td><td>Flag</td></tr></table>

Note. † The conditional use of these keywords is discussed in Sect. 6.3.

**sets. The correlations are described by a sparse dimensionless correlation matrix**

$$
C _ {i j} = \frac {\sigma_ {i j} ^ {2}}{\sqrt {\sigma_ {i} ^ {2} \sigma_ {j} ^ {2}}},\tag{4}
$$

**which is stored in a new OI\_CORR table (Table 10). The co-variance matrix can straightforwardly be obtained from the correlation matrix using the standard deviations** $\sqrt { \sigma _ { i } ^ { 2 } }$ from the data tables, such as VIS2ERR in OI\_VIS2 which is the standard devi**ation of the squared visibility.**

**Because the number of potentially correlated data is rela**tively large – of order $1 0 ^ { 4 } ;$ a six-element interferometer mea**suring squared visibilities, triple amplitudes and closure phases in 100 spectral channels for two hours with an observing cadence of 20 minutes would generate a number of data NDATA**=**33,000 – and at the same time many of these correlations are not significant, we have adopted a sparse representation of the correlation matrix. Only non-zero elements of the NDATA×NDATA matrix are stored as triplets** $\{ i , j , C _ { i j } \}$ **. Since** $C _ { i j } = C _ { j i }$ **and** $C _ { i i }   =   1$ **, we adopt the convention of only storing elements with** $j > i .$ **The indices** i **and** j **are stored as signed 32-bit integers (J type code in TFORMn). (The indices are all positive but unsigned integers can only be represented in FITS by specifying an o**ff**set using the BZERO keyword.)**

**Each of the data tables in a correlated data set shall have a keyword CORRNAME that is used to look up the corresponding OI\_CORR table. The correspondence between the position of a value in a data table and its index into the correlation matrix is given by the following new columns: CORRINDX\_VISAMP, CORRINDX\_VISPHI, CORRINDX\_RVIS and CORRINDX\_IVIS in OI\_VIS, CORRINDX\_VIS2DATA in OI\_VIS2, CORRINDX\_T3AMP and CORRINDX\_T3PHI in OI\_T3 and CORRINDX\_FLUXDATA in OI\_FLUX. These columns are all of data type J(1) and contain values ≥ 1. If all of the data in a table are uncorrelated, the CORRNAME keyword and all of the CORRINDX\_\* columns shall be omitted. If some of the table data are correlated, correlation matrix indices shall be specified for all of the data in the table, but the zero-valued correlations shall be omitted from the OI\_CORR table.**

**Taking the example of an OI\_VIS2 table whith correlated values, the (single) CORRINDX\_VIS2DATA value in a particular row in OI\_VIS2 gives the index into the correlation matrix for the first element of the VIS2DATA vector of this row, which contains NWAVE values for the defined spectral channels. The index for the** j**th value of the data vector is given by (CORRINDX\_** $\mathtt { V I S 2 D A T A + } j - 1 )$ **. In other words, an element in the correlation matrix with indices** $( i , j )$ **gives the value of the correlation between the VIS2DATA measurement in the row of the referencing OI\_VIS2 with the largest CORRINDX\_VIS2DATA value** ir **less than or equal to** i **and channel index** $( i   -   i _ { r }   +   1 )$ **and the**

Article number,

page 8 of 12

<!-- page 9 of 12 -->

Duvert, Gilles, Young, John, Hummel, Christian: OIFITS 2

Table 8. OI\_T3 (revision 2)

<table><tr><td>Label</td><td>Data Type</td><td>Description</td></tr><tr><td colspan="3">Keywords</td></tr><tr><td>OI_REVN</td><td>2</td><td>Revision number: 2</td></tr><tr><td>DATE-OBS</td><td>%s</td><td>UTC start date of observations</td></tr><tr><td>ARRNAME</td><td>%s</td><td>Identifies corresponding OI_ARRAY</td></tr><tr><td>INSNAME</td><td>%s</td><td>Identifies corresponding OI_WAVELENGTH table</td></tr><tr><td>CORRNAME</td><td>%s</td><td>(optional) Identifies corresponding OI_CORR table</td></tr><tr><td colspan="3">Column Headings (one row for each measurement)</td></tr><tr><td>TARGET_ID</td><td>I (1)</td><td>Target number as index into OI_TARGET table</td></tr><tr><td>TIME</td><td>D (1)</td><td>Zero. For backwards compatibility</td></tr><tr><td>MJD</td><td>D (1)</td><td>Modified Julian Day</td></tr><tr><td>INT_TIME</td><td>D (1)</td><td>Integration time (s)</td></tr><tr><td>T3AMP</td><td>D (NWAVE)</td><td>Triple Product Amplitude</td></tr><tr><td>T3AMPERR</td><td>D (NWAVE)</td><td>Error in Triple Product Amplitude</td></tr><tr><td>CORRINDX_T3AMP</td><td>J (1)</td><td>(optional) Index into correlation matrix for 1st T3AMP element</td></tr><tr><td>T3PHI</td><td>D (NWAVE)</td><td>Triple Product Phase in degrees</td></tr><tr><td>T3PHIERR</td><td>D (NWAVE)</td><td>Error in Triple Product Phase in degrees</td></tr><tr><td>CORRINDX_T3PHI</td><td>J (1)</td><td>(optional) Index into correlation matrix for 1st T3PHI element</td></tr><tr><td>U1COORD</td><td>D (1)</td><td>U coordinate of baseline AB of the triangle (m)</td></tr><tr><td>V1COORD</td><td>D (1)</td><td>V coordinate of baseline AB of the triangle (m)</td></tr><tr><td>U2COORD</td><td>D (1)</td><td>U coordinate of baseline BC of the triangle (m)</td></tr><tr><td>V2COORD</td><td>D (1)</td><td>V coordinate of baseline BC of the triangle (m)</td></tr><tr><td>STA_INDEX</td><td>I (3)</td><td>Station numbers contributing to the data</td></tr><tr><td>FLAG</td><td>L (NWAVE)</td><td>Flag</td></tr></table>

Table 9. OI\_FLUX (revision 1)

<table><tr><td>Label</td><td>Data Type</td><td>Description</td></tr><tr><td colspan="3">Keywords</td></tr><tr><td>OI_REVN</td><td>1</td><td>Revision number: 1</td></tr><tr><td>DATE-OBS</td><td>%s</td><td>UTC start date of observations</td></tr><tr><td>INSNAME</td><td>%s</td><td>Identifies corresponding OI_WAVELENGTH table</td></tr><tr><td>ARRNAME</td><td>%s</td><td>(optional†) Identifies corresponding OI_ARRAY table</td></tr><tr><td>CORRNAME</td><td>%s</td><td>(optional) Identifies corresponding OI_CORR table</td></tr><tr><td>FOV</td><td>%f</td><td>(optional†) Area on sky over which flux is integrated (arc sec)</td></tr><tr><td>FOVTYPE</td><td>%s</td><td>(optional†) Model for FOV: “FWHM” or “RADIUS”</td></tr><tr><td>CALSTAT</td><td>%c</td><td>“C”: Spectrum is calibrated, “U”: uncalibrated</td></tr><tr><td colspan="3">Column Headings (one row for each source)</td></tr><tr><td>TARGET_ID</td><td>I (1)</td><td>Target number as index into OI_TARGET table</td></tr><tr><td>MJD</td><td>D (1)</td><td>Modified Julian Day</td></tr><tr><td>INT_TIME</td><td>D (1)</td><td>Integration time (s)</td></tr><tr><td>FLUXDATA</td><td>D (NWAVE)</td><td>Flux in units of TUNITn</td></tr><tr><td>FLUXERR</td><td>D (NWAVE)</td><td>Corresponding flux error</td></tr><tr><td>CORRINDX_FLUXDATA</td><td>J (1)</td><td>(optional) Index into correlation matrix for 1st FLUXDATA element</td></tr><tr><td>STA_INDEX</td><td>I (1)</td><td>(optional†) Station number contributing to the data</td></tr><tr><td>FLAG</td><td>L (NWAVE)</td><td>Flag</td></tr></table>

Note. † The conditional use of these keywords is discussed in Sect. 7.1.

**measurement in OI\_VIS2 obtained in the same way using index** j **instead of** i**. Therefore, the indices implied by the CORRINDX values shall be unique within the correlated data set. The other CORRINDX columns give the correlation matrix index for the first element of the similarly-named, real-valued data column. An example of use is described in Appendix A.**

## 7.3. OI\_INSPOL (revision 1)

**In general, each input beam contributing to the correlated flux on a baseline is polarized to some extent, either by design or by the unavoidable e**ff**ects of partially-polarizing elements in the optical train of the interferometer. Although polaro-interferometric observations in the optical and infrared range are possible, there is no good example yet of true polaro-interferometric observations which provided a measurement of the source’s Stokes parameters. It is thus out of the scope of this document to standardize polaro-interferometric calibrated data. However, we feel**

Article number,

page 9 of 12

<!-- page 10 of 12 -->

manuscript no. oifits\_norm\_v2

**compelled to provide a way to note in the OIFITS format that the measurements were subject to instrumental polarisation, and, in the case of simultaneous or related measurements in various states of polarisation, provide an internal link between the classical observables of OIFITS and the instrumental polarisation state in which they were obtained. This new table is purely instrumental and named OI\_INSPOL.**

**In order to ensure backwards compatibility with current OIFITS readers, we identify each functional polarisation state by a di**ff**erent INSNAME. For example, data taken through a Wollaston prism (two orthogonal linear polarisations) provides two statistically independent series of interferograms. Each serie will produce OI observables, perfectly valid independently of the other. It is just a matter of bookkeeping to note that one serie was taken with horizontal polarisation through the Wollaston and the other through the vertical polarisation. The new OI\_INSPOL table is the central hub that links all the INSNAMEs (all the polarized measurements). Keywords for the OI\_INSPOL table are listed in Table 11.**

**The OI\_INSPOL table uses the Jones matrix representation as a beam-based description of how the optical system operates on the source’s light. This formalism does not permit the description of the depolarizing e**ff**ects that could occur between the telescope(s) and the recording of the interferogram. However, being an operator on the electrical field of the light, it allows to describe the e**ff**ects on the complex coherence betwen two beams.**

**The OI\_INSPOL table stores a Jones matrix for each wavelength, time interval, and polarisation state as cross-referenced via the INSNAME column. The four complex elements of the Jones matrix are stored in the columns JXX, JYY, JXY and JYX. These values are beam-based, and can be in principle measured or modeled as a function of time. In the simplest case, a polarizer in front of the camera would record only one polarisation, or a Wollaston in the same place would permit recording of two orthogonally polarized interferograms. Then OI\_INSPOL would serve only to describe the ORIENTation of the polarisation state of the INSNAME (or INSNAMEs) interferometric data. More complicated cases, in particular a time-varying instrumental polarisation due to rotation of a polarizing element, are possible. The MJD\_OBS and MJD\_END values can describe any variation of the complex Jones matrices independently of the time-tagging of data contained the other tables. Table 12 shows a few examples of Jones matrices for simple polarizers. The sign of the imaginary parts must be given in the theoretical framework where the wave function used in propagation equations of light reads exp(**kz − iωt**) (Lawson 2000, p. 10).**

**OI\_INSPOL is an optional table: if OI\_INSPOL is present, it must encompass at least all the time entries and baselines present**

Table 10. OI\_CORR (revision 1)

<table><tr><td>Label</td><td>Data Type</td><td>Description</td></tr><tr><td colspan="3">Keywords</td></tr><tr><td>OI_REVN</td><td>1</td><td>Revision number: 1</td></tr><tr><td>CORRNAME</td><td>%s</td><td>Name of correlated data set(1)</td></tr><tr><td>NDATA</td><td>%d</td><td>Size of the correlation matrix</td></tr><tr><td colspan="3">Column Headings, one row for each non-zero element</td></tr><tr><td>IINDX</td><td>J(1)</td><td>First index of correlation matrix element</td></tr><tr><td>JINDX</td><td>J(1)</td><td>Second index of correlation matrix element</td></tr><tr><td>CORR</td><td>D(1)</td><td>Matrix element (IINDX,JINDX)</td></tr></table>

Article number, page 10 of 12

Notes. (1) this name cross-references one or more tables in the file.

**in all the other tables referenced by all the values stored in its INSNAME column. OI\_INSPOL is also experimental: OIFITS readers or writers should make provision for the possible augmentation of this table in future releases.**

## 7.4. Guidelines for other tables

**It may be useful to incorporate other tables in an OIFITS file. For example, there might be one that contains instrument specific information, such as the backend configuration. Another optional table could contain information relevant to astrometry. The only requirement imposed by the format is that EXTNAMEs of additional tables must not begin with “OI\_”.**

## 8. Summary

**Drawing on experience from a dozen years of community use, we have revised the OIFITS data format to:**

**– address the needs of the new interferometric instruments that will routinely produce images, adding ancillary data and tables useful for image reconstruction purposes;**

**– provide a rigorous description of the interferometric observables and how they are computed, especially in the case of di**ff**erential observables;**

**– provide a rigorous description of measurement errors and their correlation;**

**– tentatively take into account simple polarisation properties of the instrument;**

**– pave the way to a more formal description of the optical interferometry Data Model, as developed for radio interferometry for example.**

**– add bookkeeping keywords necessary to feed the emerging databases of optical interferometry measurements.**

**This has been done while guaranteeing backward compatibility with version 1, ensuring continuous use of older software without changes. There are already a few libraries available for reading and writing this format, and we expect that it will soon be used by the end data products of the PIONIER, GRAVITY and MATISSE instruments, and receive wide support from the optical interferometry community.**

## References

Benisty, M., Berger, J.-P., Jocou, L., et al. 2009, A&A, 498, 601

Bradner, S., IETF publication, RFC 21 [http://www.ietf.org/rfc/rfc2119.txt](http://www.ietf.org/rfc/rfc2119.txt)

Dolensky, M., Chéreau, F., Delgado, M., et al. 2008, Astronomical Data Analysis Software and Systems XVII, 394, 235

Eisenhauer, F., Perrin, G., Brandner, W., et al. 2011, The Messenger, 143, 16

Hanisch, R. J., Farris, A., Greisen, E. W., Pence, W. D., Schlesinger, B. M., Teuben, P. J., Thompson, R. W., & Warnock, A. 2001, A&A, 376, 359

Lawson, P. R. (ed.) 2000, Principles of Long Baseline Stellar Interferometry (Pasadena: NASA, JPL, CIT)

Millour, F., Vannier, M., Petrov, R. G., et al. 2006, EAS Publications Series, 22, 379

Pauls, T. A., Young, J. S., Cotton, W. D., & Monnier, J. D. 2005, PASP, 117, 1255

Perrin, G. 2003, A&A, 400, 1173

Petrov, R. G. , Malbet, F. , Weigelt, G. et al. 2007, A&A, 464, 1

Young, J. S., Cotton, W. D., Gässler, W., et al. 2008, Proc. SPIE, 7013, 70134H

<!-- page 11 of 12 -->

Duvert, Gilles, Young, John, Hummel, Christian: OIFITS 2

Table 11. OI\_INSPOL (revision 1)

<table><tr><td>Label</td><td>Data Type</td><td>Description</td></tr><tr><td colspan="3">Keywords</td></tr><tr><td>OI_REVN</td><td>1</td><td>Revision number: 1</td></tr><tr><td>NPOL</td><td>%d</td><td>Number of Polarisation Types in this table</td></tr><tr><td>ARRNAME</td><td>%s</td><td>Identifies corresponding OI_ARRAY</td></tr><tr><td>ORIENT</td><td>%s</td><td>Orientation of the Jones Matrix, could be “NORTH” (for on-sky orientation), or “LABORATORY”</td></tr><tr><td>MODEL</td><td>%s</td><td>A string keyword that describe the way the Jones matrix is estimated</td></tr><tr><td colspan="3">Column Headings, one row for each source</td></tr><tr><td>TARGET_ID</td><td>I (1)</td><td>Target number as index into OI_TARGET table</td></tr><tr><td>INSNAME</td><td>A</td><td>INSNAME of this polarisation</td></tr><tr><td>MJD_OBS</td><td>D (1)</td><td>Modified Julian Day, start of time lapse</td></tr><tr><td>MJD_END</td><td>D (1)</td><td>Modified Julian Day, end of time lapse</td></tr><tr><td>JXX</td><td>C (NWAVE)</td><td>Complex Jones Matrix component along X axis.</td></tr><tr><td>JYY</td><td>C (NWAVE)</td><td>Complex Jones Matrix component along Y axis</td></tr><tr><td>JXY</td><td>C (NWAVE)</td><td>Complex Jones Matrix component between X and Y axis</td></tr><tr><td>JYX</td><td>C (NWAVE)</td><td>Complex Jones Matrix component between Y and X axis</td></tr><tr><td>STA_INDEX</td><td>I (1)</td><td>Station number for the above matrices</td></tr></table>

## Appendix A: On the use of Correlation Matrices in OIFITS

**We describe here a concrete example of the use of OI\_CORR. Consider a dataset comprising two OI\_VIS2 tables and two OI\_T3 tables, as shown in Table 13. Each table contains observations made simultaneously on three baselines in four wavelength channels. Depending on how we want to express the correlations between some of the observables within these tables, we will use di**ff**erent OI\_CORR tables (with unique CORRNAMEs).**

**If we need to express the spectral correlations of the T3AMP measurements only, we would write a 4×4 full correlation matrix for each OI\_T3 table. These two matrices can be written as two sparse matrices in two separate OI\_CORR tables, “T1” and “T2” (one per OI\_T3). The value of CORRINDX\_T3AMP would be 1 for both OI\_T3 tables as shown in Table 13 in the lower diagonal cells.**

**If we need to express the time and baseline correlations between the VIS2DATA measurements only, we have 2 × 3 ×** 4 = **24 measurements in the two OI\_VIS2 tables (12 per table), requiring a 24 × 24 correlation matrix. The correlations between these measurements would be expressed as a single OI\_CORR table (“V”) with NDATA** = **24. In this example, the CORRINDX\_VIS2DATA values for each row in OI\_VIS2 are also given in the lower diagonal cells of Table 13.**

**As T3AMP measurements share baselines with VIS2DATA measurements, we could give the correlations between T3AMP and VIS2 measurements in a single OI\_CORR table. In this case, non-zero correlations would be contained in a matrix of NDATA** = **24** + **2 × 4** = **32 rows and columns, the indices CORRINDX\_VIS2DATA and CORRINDX\_T3AMP are now given in**

Table 12. Basic Jones Matrix Examples. See text for the sign of imaginary parts.

| Polarizer | JXX | JXY | JYX | JYY |
| --- | --- | --- | --- | --- |
| Linear, Horizontal | (1,0) | (0,0) | (0,0) | (0,0) |
| Linear, Vertical | (0,0) | (0,0) | (0,0) | (1,0) |
| Linear, ±45 deg | (0.5,0) | (±0.5,0) | (±0.5,0) | (0.5,0) |
| Circular, Right | (0.5,0) | (0,0.5) | (0,-0.5) | (0.5,0) |
| Circular, Left | (0.5,0) | (0,-0.5) | (0,0.5) | (0.5,0) |

**the upper diagonal cells of Table 13 and all data tables would reference the same OI\_CORR table (“V&T”).**

Acknowledgements. **Initial development of the format was done under the auspices of the IAU Working Group on Optical and infrared Interferometry. Version 2 has been pursued by the (discontinued) IAU Commission 54 and JMMC, with the active participation of many community interferometrists, in particular: Fabien Baron, Philippe Bério, Laurent Bourgès, Leonard Burtscher, Alain Chelli, Pierre Cruzalèbes, Mike Ireland, Charleen Kemps, Brian Kloppenborg, Sylvestre Lacour, Vincent Lapeyrere, Jean-Baptiste le Bouquin, Guillaume Mella, Florentin Millour, John Monnier, Jörg-Uwe Pott, Antony Schutz, Michel Tallon, Theo ten Brummelaar, Eric Thiébaut. We thank I. Percheron, A. Dobrzycki and our anonymous referee for many useful comments. This work has benefitted of the support of the European Community’s Seventh Framework Programme (FP7**/**2013-2016) under Grant Agreement 312430 (OPTICON) and of the French ANR POLCA, ANR-10-BLAN-0511.**

Article number,

page 11 of 12

<!-- page 12 of 12 -->

manuscript no. oifits\_norm\_v2

Table 13. This table gives an example of a set of data comprising two OI\_T3 tables obtained at two different times, for four channels on three baselines, and the corresponding VIS2DATA measurements, also in two OI\_VIS2 tables. There are three cases examined in the text (Appendix A), which lead to four different OI\_CORR tables. (The corresponding CORRNAME is given for each.)

<table><tr><td rowspan="2">MJD</td><td rowspan="2">CORRNAME</td><td rowspan="2">CORRINDX</td><td rowspan="2">STA_INDEX</td><td> $\lambda_1$ </td><td> $\lambda_2$ </td><td> $\lambda_3$ </td><td> $\lambda_4$ </td></tr><tr><td colspan="4">T3</td></tr><tr><td colspan="8">Table OI_T3 #1</td></tr><tr><td>1.0</td><td>“T1” “V&amp;T”</td><td>1</td><td>1</td><td>1 2 3</td><td> $T3_{\lambda_1}^{mjd=1.0}$ </td><td> $T3_{\lambda_2}^{mjd=1.0}$ </td><td> $T3_{\lambda_3}^{mjd=1.0}$ </td></tr><tr><td colspan="8">Table OI_T3 #2</td></tr><tr><td>2.0</td><td>“T2” “V&amp;T”</td><td>1</td><td>5</td><td>1 2 3</td><td> $T3_{\lambda_1}^{mjd=2.0}$ </td><td> $T3_{\lambda_2}^{mjd=2.0}$ </td><td> $T3_{\lambda_3}^{mjd=2.0}$ </td></tr><tr><td colspan="8">⋮</td></tr><tr><td rowspan="2">MJD</td><td rowspan="2">CORRNAME</td><td rowspan="2">CORRINDX</td><td rowspan="2">STA_INDEX</td><td> $\lambda_1$ </td><td> $\lambda_2$ </td><td> $\lambda_3$ </td><td> $\lambda_4$ </td></tr><tr><td colspan="4">VIS2DATA</td></tr><tr><td colspan="8">Table OI_VIS2 #1</td></tr><tr><td>1.0</td><td>“V” “V&amp;T”</td><td>1</td><td>9</td><td>1 2</td><td> $V2_{12,\lambda_1}^{mjd=1.0}$ </td><td> $V2_{12,\lambda_2}^{mjd=1.0}$ </td><td> $V2_{12,\lambda_3}^{mjd=1.0}$ </td></tr><tr><td>1.0</td><td>“V” “V&amp;T”</td><td>5</td><td>13</td><td>2 3</td><td> $V2_{23,\lambda_1}^{mjd=1.0}$ </td><td> $V2_{23,\lambda_2}^{mjd=1.0}$ </td><td> $V2_{23,\lambda_3}^{mjd=1.0}$ </td></tr><tr><td>1.0</td><td>“V” “V&amp;T”</td><td>9</td><td>17</td><td>1 3</td><td> $V2_{13,\lambda_1}^{mjd=1.0}$ </td><td> $V2_{13,\lambda_2}^{mjd=1.0}$ </td><td> $V2_{13,\lambda_3}^{mjd=1.0}$ </td></tr><tr><td colspan="8">Table OI_VIS2 #2</td></tr><tr><td>2.0</td><td>“V” “V&amp;T”</td><td>13</td><td>21</td><td>1 2</td><td> $V2_{12,\lambda_1}^{mjd=2.0}$ </td><td> $V2_{12,\lambda_2}^{mjd=2.0}$ </td><td> $V2_{12,\lambda_3}^{mjd=2.0}$ </td></tr><tr><td>2.0</td><td>“V” “V&amp;T”</td><td>17</td><td>25</td><td>2 3</td><td> $V2_{23,\lambda_1}^{mjd=2.0}$ </td><td> $V2_{23,\lambda_2}^{mjd=2.0}$ </td><td> $V2_{23,\lambda_3}^{mjd=2.0}$ </td></tr><tr><td>2.0</td><td>“V” “V&amp;T”</td><td>21</td><td>29</td><td>1 3</td><td> $V2_{13,\lambda_1}^{mjd=2.0}$ </td><td> $V2_{13,\lambda_2}^{mjd=2.0}$ </td><td> $V2_{13,\lambda_3}^{mjd=2.0}$ </td></tr></table>

Article number,

page 12 of 12