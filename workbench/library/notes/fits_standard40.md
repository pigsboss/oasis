<!-- page 1 of 75 -->

# Definition of the Flexible Image Transport System (FITS)

The FITS Standard Version 4.0: updated 2016 July 22 by the IAUFWG Original document publication date: 2016 July 22 Language-edited document publication date: 2018 August 13

FITS Working Group Commission 5: Documentation and Astronomical Data <sup>2</sup> International Astronomical Union [http://fits.gsfc.nasa.gov/iaufwg/](http://fits.gsfc.nasa.gov/iaufwg/)

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">1to be absorbed in Data Representation Working Group under new Commission B2</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">2 now Commission B2 Data and Documentation</span></small>

<!-- page 2 of 75 -->

<!-- page 3 of 75 -->

## Contents

## Contents

- 1 Introduction 1
- 1.1 Brief history of FITS 1
- 1.2 Version history of this document 1
- 1.3 Acknowledgments 2
- 2 Definitions, acronyms, and symbols 3
- 2.1 Conventions used in this document 3
- 2.2 Defined terms 3
- 3 FITS file organization 4
- 3.1 Overall file structure 4
- 3.2 Individual FITS Structures 4
- 3.3 Primary header and data unit 4
- 3.3.1 Primary header 5
- 3.3.2 Primary data array 5
- 3.4 Extensions 5
- 3.4.1 Requirements for conforming extensions 5
- 3.4.2 Standard extensions 5
- 3.4.3 Order of extensions 5
- 3.5 Special records (restricted use) 5
- 3.6 Physical blocking 6
- 3.6.1 Bit-stream devices 6
- 3.6.2 Sequential media 6
- 3.7 Restrictions on changes 6
- 4 Headers 6
- 4.1 Keyword records 6
- 4.1.1 Syntax 6
- 4.1.2 Components 6
- 4.2 Value 7
- 4.2.1 Character string 7
- 4.2.2 Logical 8
- 4.2.3 Integer number 8
- 4.2.4 Real floating-point number 8
- 4.2.5 Complex integer number 9
- 4.2.6 Complex floating-point number 9
- 4.2.7 Date 10
- 4.3 Units 10
- 4.3.1 Construction of units strings 10
- 4.3.2 Units in comment fields 10
- 4.4 Keywords 10
- 4.4.1 Mandatory keywords 10
- 4.4.2 Other reserved keywords 12
- 4.4.3 Additional keywords 16
- 5 Data representation 16
- 5.1 Characters 16
- 5.2 Integers 16
- 5.2.1 Eight-bit 16
- 5.2.2 Sixteen-bit 16
- 5.2.3 Thirty-two-bit 16
- 5.2.4 Sixty-four-bit 16
- 5.2.5 Unsigned integers 16
- 5.3 IEEE-754 floating point 16
- 5.4 Time 16

i

<!-- page 4 of 75 -->

- 6 Random-groups structure 16
- 6.1 Keywords 17
- 6.1.1 Mandatory keywords 17
- 6.1.2 Reserved keywords 17
- 6.2 Data sequence 17
- 6.3 Data representation 18
- 7 Standard extensions 18
- 7.1 Image extension 18
- 7.1.1 Mandatory keywords 18
- 7.1.2 Other reserved keywords 18
- 7.1.3 Data sequence 18
- 7.2 The ASCII-table extension 19
- 7.2.1 Mandatory keywords 19
- 7.2.2 Other reserved keywords 20
- 7.2.3 Data sequence 21
- 7.2.4 Fields 21
- 7.2.5 Entries 21
- 7.3 Binary-table extension 22
- 7.3.1 Mandatory keywords 22
- 7.3.2 Other reserved keywords 22
- 7.3.3 Data sequence 25
- 7.3.4 Data display 26
- 7.3.5 Variable-length arrays 27
- 7.3.6 Variable-length-array guidelines 28
- 8 World-coordinate systems 29
- 8.1 Basic concepts 29
- 8.2 World-coordinate-system representations 30
- 8.2.1 Alternative WCS axis descriptions 32
- 8.3 Celestial-coordinate-system representations 33
- 8.4 Spectral-coordinate-system representations 33
- 8.4.1 Spectral-coordinate reference frames 35
- 8.5 Conventional-coordinate types 36
- 9 Representations of time coordinates 36
- 9.1 Time values 37
- 9.1.1 ISO-8601 datetime strings 37
- 9.1.2 Julian and Besselian epochs 37
- 9.2 Time coordinate frame 37
- 9.2.1 Time scale 37
- 9.2.2 Time reference value 38
- 9.2.3 Time reference position 39
- 9.2.4 Time reference direction 40
- 9.2.5 Solar System ephemeris 41
- 9.3 Time unit 41
- 9.4 Time offset, binning, and errors 41
- 9.4.1 Time offset 41
- 9.4.2 Time resolution and binning 41
- 9.4.3 Time errors 42
- 9.5 Global time keywords 42
- 9.6 Other time-coordinate axes 43
- 9.7 Durations 43
- 9.8 Recommended best practices 43
- 9.8.1 Global keywords and overrides 43
- 9.8.2 Restrictions on alternate descriptions 43
- 9.8.3 Image time axes 44

ii

<!-- page 5 of 75 -->

- 10 Representations of compressed data 44
- 10.1 Tiled image compression 44
- 10.1.1 Required keywords 44
- 10.1.2 Other reserved keywords 44
- 10.1.3 Table columns 45
- 10.2 Quantization of floating-point data 46
- 10.2.1 Dithering algorithms 47
- 10.2.2 Preserving undefined pixels with lossy compression 47
- 10.3 Tiled table compression 48
- 10.3.1 Required keywords 48
- 10.3.2 Procedure for table compression 48
- 10.3.3 Compression directive keywords 49
- 10.3.4 Other reserved keywords 49
- 10.3.5 Supported compression algorithms for tables 49
- 10.3.6 Compressing variable-length array columns 49
- 10.4 Compression algorithms 50
- 10.4.1 Rice compression 50
- 10.4.2 Gzip compression 50
- 10.4.3 IRAF/PLIO compression 50
- 10.4.4 H-Compress algorithm 51
- A Syntax of keyword records 52
- B Suggested time-scale specification 53
- C Summary of keywords 54
- D ASCII text 56
- E IEEE floating-point formats 56
- E.1 Basic formats 56
- E.1.1 Single 57
- E.1.2 Double 57
- E.2 Byte patterns 57
- F Reserved extension type names 59
- F.1 Standard extensions 59
- F.2 Conforming extensions 59
- F.3 Other suggested extension names 59
- G MIME types 59
- G.1 MIME type 'application/fits' 59
- G.1.1 Recommendations for application writers 60
- G.2 MIME type 'image/fits' 60
- G.2.1 Recommendations for application writers 60
- G.3 File extensions 61
- H Past changes or clarifications to the formal definition of FITS 61
- H.1 Differences between the requirements in this Standard and the requirements in the original FITS papers. 61
- H.2 List of modification to the FITS Standard, Version 3.0 61
- H.3 List of modifications to the latest FITS Standard 62
- H.4 List of modifications for language editing 62
- I Random-number generator 63
- J CHECKSUM implementation guidelines 63
- J.1 Recommended CHECKSUM keyword implementation 63
- J.2 Recommended ASCII encoding algorithm 63
- J.3 Encoding example 64
- J.4 Incremental updating of the checksum 64
- J.5 Example C code for accumulating the checksum 65
- J.6 Example C code for ASCII encoding 65

iii

<!-- page 6 of 75 -->

- K Header inheritance convention 65
- L Green Bank convention 66
- References / Index 66

## List of Tables

- 1 Significant milestones in the development of FITS. 2
- 2 Version history of the Standard. 2
- 3 IAU-recommended basic units. 8
- 4 Additional allowed units. 9
- 5 Prefixes for multiples and submultiples. 10
- 6 Characters and strings allowed to denote mathematical operations. 11
- 7 Mandatory keywords for primary header. 11
- 8 Interpretation of valid BITPIX value. 11
- 9 Example of a primary array header. 12
- 10 Mandatory keywords in conforming extensions. 12
- 11 Usage of BZERO to represent non-default integer data types. 15
- 12 Mandatory keywords in primary header preceding random groups. 17
- 13 Mandatory keywords in IMAGE extensions. 18
- 14 Mandatory keywords in ASCII-table extensions. 19
- 15 Valid TFORMn format values in TABLE extensions. 19
- 16 Valid TDISPn format values in TABLE extensions. 20
- 17 Mandatory keywords in binary-table extensions. 23
- 18 Valid TFORMn data types in BINTABLE extensions. 23
- 19 Usage of TZEROn to represent non-default integer data types. 24
- 20 Valid TDISPn format values in BINTABLE extensions. 25
- 21 WCS and celestial coordinates notation. 30
- 22 Reserved WCS keywords (continues on next page) 31
- 23 Reserved celestial-coordinate-algorithm codes. 34
- 25 Reserved spectral-coordinate type codes. 35
- 24 Allowed values of RADESYSa. 35
- 26 Non-linear spectral algorithm codes. 36
- 27 Spectral reference systems. 36
- 28 Example keyword records for a 100-element array of complex values. 36
- 29 Conventional Stokes values. 36
- 30 Recognized Time Scale Values 38
- 31 Standard Time Reference Position Values 39
- 32 Compatibility of Time Scales and Reference Positions 40
- 33 Valid Solar System ephemerides 41
- 34 Recommended time units 41
- 35 Keywords for global time values 42
- 36 Valid mnemonic values for the ZCMPTYPE and ZCTYPn keywords 50
- 37 Keyword parameters for Rice compression 50
- 38 PLIO Instructions 51
- 39 Keyword parameters for H-compression 51
- C.1 Mandatory FITS keywords. 54
- C.2 Reserved FITS keywords. 54
- C.3 General reserved FITS keywords. 55
- D.1 ASCII character set 56
- E.1 Summary of format parameters. 57
- E.2 IEEE floating-point formats. 58

iv

<!-- page 7 of 75 -->

## 1. Introduction

An archival format must be utterly portable and self-describing, on the assumption that, apart from the transcription device, neither the software nor the hardware that wrote the data will be available when the data are read. ‘Preserving Scientific Data on our Physical Universe,’ p. 60. Steering Committee for the Study on the Long-Term Retention of Selected Scientific and Technical Records of the Federal Government, [US] National Research Council, National Academy Press 1995.

This document, hereafter referred to as the ‘Standard’, describes the Flexible Image Transport System (FITS), which is the standard archival data format for astronomical data sets. Although FITS was originally designed for transporting image data on magnetic tape (which accounts for the ‘I’ and ‘T’ in the name), the capabilities of the FITS format have expanded to accommodate more-complex data structures. The role of FITS has also grown from simply a way to transport data between different analysis software systems into the preferred format for data in astronomical archives, as well as the on-line analysis format used by many software packages.

This standard is intended as a formal codification of the FITS format, which has been endorsed by the International Astronomical Union (IAU) for the interchange of astronomical data (IAU 1983). It is fully consistent with all actions and endorsements of the IAU FITS Working Group (IAUFWG), which was appointed by Commission 5 of the IAU to oversee further development of the FITS format. In particular, this standard defines the organization and content of the header and data units for all standard FITS data structures: the primary array, the randomgroups structure, the image extension, the ASCII-table extension, and the binary-table extension. It also specifies minimum structural requirements and general principles governing the creation of new extensions. For headers, it specifies the proper syntax for keyword records and defines required and reserved keywords. For data, it specifies character- and numeric-value representations and the ordering of contents within the byte stream.

One important feature of the FITS format is that its structure, down to the bit level, is completely specified in documents (such as this standard), many of which have been published in refereed scientific journals. Given these documents, which are readily available in hard copy form in libraries around the world as well as in electronic form on the Internet, future researchers should be able to decode the stream of bytes in any FITS format data file. In contrast, many other current data formats are only implicitly defined by the software that reads and writes the files. If that software is not continually maintained so that it can be run on future computer systems, then the information encoded in those data files could be lost.

## 1.1. Brief history of FITS

The FITS format evolved out of the recognition that a standard format was needed for transferring astronomical images from one research institution to another. The first prototype developments of a universal interchange format that would eventually lead to the definition of the FITS format began in 1976 between Don Wells at KPNO and Ron Harten at the Netherlands Foundation for Research in Astronomy (NFRA). This need for

an image interchange format was raised at a meeting of the Astronomy section of the U.S. National Science Foundation in January 1979, which led to the formation of a task force to work on the problem. Most of the technical details of the first basic FITS agreement (with files consisting of only a primary header followed by a data array) were subsequently developed by Don Wells and Eric Greisen (NRAO) in March 1979. After further refinements, and successful image interchange tests between observatories that used widely different types of computer systems, the first papers that defined the FITS format were published in 1981 (Wells et al. 1981; Greisen & Harten 1981). The FITS format quickly became the de facto standard for data interchange within the astronomical community (mostly on nine-track magnetic tape at that time), and was officially endorsed by the IAU in 1982 (IAU 1983). Most national and international astronomical projects and organizations subsequently adopted the FITS format for distribution and archiving of their scientific data products. Some of the highlights in the developmental history of FITS are shown in Table 1.

## 1.2. Version history of this document

The fundamental definition of the FITS format was originally contained in a series of published papers (Wells et al. 1981; Greisen & Harten 1981; Grosbøl et al. 1988; Harten et al. 1988). As FITS became more widely used, the need for a single document to unambiguously define the requirements of the FITS format became apparent. In 1990, the NASA Science Office of Standards and Technology (NOST) at the Goddard Space Flight Center provided funding for a technical panel to develop the first version of this Standard document. As shown in Table 2, the NOST panel produced several draft versions, culminating in the first NOST standard document, NOST 100-1.0, in 1993. Although this document was developed under a NASA accreditation process, it was subsequently formally approved by the IAUFWG, which is the international control authority for the FITS format. The small update to the Standard in 1995 (NOST 100-1.1) added a recommendation on the physical units of header keyword values.

The NOST technical panel was convened a second time to make further updates and clarifications to the Standard, resulting in the NOST 100-2.0 version, which was approved by the IAUFWG in 1999 and published in 2001 (Hanisch et al. 2001). In 2005, the IAUFWG formally approved the variable-length array convention in binary tables, and a short time later approved support for the 64-bit integers data type. New versions of the Standard were released to reflect both of these changes (Versions IAUFWG 2.1 and IAUFWG 2.1b).

In early 2007 the IAUFWG appointed its own technical panel to consider further modifications and updates to the Standard. The changes proposed by this panel, which were ultimately approved in 2008 by the IAUFWG after a formal public review process, are shown in the Version 3.0 of the document, published in Pence et al. (2010).

Since 2006 a Registry for FITS conventions submitted by the community was established under the care of the IAUFWG at [http://fits.gsfc.nasa.gov/fits\_registry.html](http://fits.gsfc.nasa.gov/fits_registry.html). The Registry was intended as a repository of documentation of usages, which, although not endorsed as part of the FITS Standard, are otherwise perfectly legal usages of FITS. In 2014 a small team was formed to evaluate the possible incorporation of some

1

<!-- page 8 of 75 -->

Table 1: Significant milestones in the development of FITS.

| Date | Milestone | Section |
| --- | --- | --- |
| 1979 | InitialFITS Agreement and first interchange of files |  |
| 1981 | Published original (single HDU) definition (Wells et al. 1981) |  |
| 1981 | Published random-groups definition (Greisen &amp; Harten 1981) | Sect. 6 |
| 1982 | Formally endorsed by the IAU (IAU 1983) |  |
| 1988 | Defined rules for multiple extensions (Grosbøl et al. 1988) |  |
| 1988 | IAUFITS Working Group (IAUFWG) established |  |
| 1988 | Extended to include ASCII-table extensions (Harten et al. 1988) | Sect. 7.2 |
| 1988 | Formal IAU approval of ASCII tables (IAU 1988) | Sect. 7.2 |
| 1990 | Extended to include IEEE floating-point data (Wells &amp; Grosbøl 1990) | Sect. 5.3 |
| 1994 | Extended to multiple IMAGE-array extensions (Ponz et al. 1994) | Sect. 7.1 |
| 1995 | Extended to binary-table extensions (Cotton et al. 1995) | Sect. 7.3 |
| 1997 | Adopted four-digit-year date format (Bunclark &amp; Rots 1997) | Sect. 4.4.2 |
| 2002 | Adopted proposals for world-coordinate systems (Greisen &amp; Calabretta 2002) | Sect. 8 |
| 2002 | Adopted proposals for celestial coordinates (Calabretta &amp; Greisen 2002) | Sect. 8.3 |
| 2004 | Adopted MIME types forFITS data files (Allen &amp; Wells 2005) | App. G |
| 2005 | Extended to support variable-length arrays in binary tables | Sect. 7.3.5 |
| 2005 | Adopted proposals for spectral-coordinate systems (Greisen et al. 2006) | Sect. 8.4 |
| 2005 | Extended to include 64-bit integer data type | Sect. 5.2.4 |
| 2006 | Adopted WCS HEALPix projection (Calabretta &amp; Roukema 2007) | Sect. 8.3 |
| 2006 | EstablishedFITS convention registry |  |
| 2014 | Adopted proposals for time coordinates (Rots et al. 2015) | Sect. 9 |
| 2016 | Adopted proposals for compressed data | Sect. 10 |
| 2016 | Adopted various registered conventions | App. H.3 |
| 2018 | General language editing | App. H.4 |

Table 2: Version history of the Standard.

| Version | Date | Status |
| --- | --- | --- |
| NOST 100-0.1 | 1990 December | First Draft Standard |
| NOST 100-0.2 | 1991 June | Second Revised Draft Standard |
| NOST 100-0.3 | 1991 December | Third Revised Draft Standard |
| NOST 100-1.0 | 1993 June | NOST Standard |
| NOST 100-1.1 | 1995 September | NOST Standard |
| NOST 100-2.0 | 1999 March | NOST Standard |
| IAUFWG 2.1 | 2005 April | IAUFWG Standard |
| IAUFWG 2.1b | 2005 December | IAUFWG Standard |
| IAUFWG 3.0 | 2008 July | IAUFWG Standard |
| IAUFWG 4.0 | 2016 July | IAUFWG Standard (approved) |
| IAUFWG 4.0 | 2018 August | IAUFWG Standard (language-edited) |

conventions within the Standard, while another small team was in charge to update the Standard document with a summary of the WCS time representation (Rots et al. 2015), which in the meanwhile had been voted natively as part of the FITS Standard.

Details on the conventions that have been incorporated into this latest version of the Standard (CONTINUE long-string keywords, blank header space, CHECKSUM, column limits, tiled image and table compression) or only briefly mentioned (keyword inheritance and Green Bank conventions) are described in Appendix H.3, which also lists the corresponding affected sections of the Standard.

After the approval by the IAUFWG in July 2016 the Standard was subjected to a thorough language editing (with no impact on the technical prescriptions) before the final issue in 2018. Details about the language editing changes are provided in Appendix H.4.

The latest version of the Standard, as well as other information about the FITS format, can be obtained from the FITS Support Office website at [http://fits.gsfc.nasa.gov](http://fits.gsfc.nasa.gov). This website also contains the contact information for the Chairman

of the IAUFWG, to whom any questions or comments regarding this Standard should be addressed.

## 1.3. Acknowledgments

The members of the three technical panels that produced this Standard are shown below.

## First technical panel, 1990–1993

Robert J. Hanisch (Chair) Space Telescope Science Inst. Lee E. Brotzman Hughes STX Edward Kemper Hughes STX Barry M. Schlesinger Raytheon STX Peter J. Teuben University of Maryland Michael E. Van SteenbergNASA Goddard SFC Wayne H. Warren Jr. Hughes STX Richard A. White NASA Goddard SFC

**Second technical panel, 1994–1999** Robert J. Hanisch (Chair) Space Telescope Science Inst. Allen Farris Space Telescope Science Inst.

2

<!-- page 9 of 75 -->

| Eric W. Greisen | National Radio Astr. Obs. |
| --- | --- |
| William D. Pence | NASA Goddard SFC |
| Barry M. Schlesinger | Raytheon STX |
| Peter J. Teuben | University of Maryland |
| Randall W. Thompson | Computer Sciences Corp. |
| Archibald Warnock | A/WWW Enterprises |

## Third technical panel, 2007

| William D. Pence (Chair) | NASA Goddard SFC |
| --- | --- |
| Lucio Chiappetti | IASF Milano, INAF, Italy |
| Clive G. Page | University of Leicester, UK |
| Richard Shaw | National Optical Astr. Obs. |
| Elizabeth Stobie | University of Arizona |

## Dedicated task forces, 2013-2016

| Lucio Chiappetti | IASF Milano, INAF, Italy |
| --- | --- |
| Steve Allen | UCO Lick Observatory |
| Adam Dobrzycki | European Southern Observatory |
| William D. Pence | NASA Goddard SFC |
| Arnold Rots | Harvard Smithsonian CfA |
| Richard Shaw | National Optical Astr. Obs. |
| William T. Thompson | NASA Goddard SFC |

<table><tr><td colspan="2">Language editing, 2016-2018</td></tr><tr><td>Malcolm J. Currie</td><td>Rutherford Appleton Lab, UK</td></tr><tr><td>Lucio Chiappetti</td><td>IASF Milano, INAF, Italy</td></tr></table>

## 2. Definitions, acronyms, and symbols

## 2.1. Conventions used in this document

Terms or letters set in Courier typeface represent literal strings that appear in FITS files. In the case of keyword names, such as ‘NAXISn’, the lower-case letter represents a positive integer index number, generally in the range 1 to 999. The emphasized words must, shall, should, may, recommended, required, and optional in this document are to be interpreted as described in IETF standard, RFC 2119 (Bradner 1997).

## 2.2. Defined terms

Used to designate an ASCII space character.

ANSI American National Standards Institute.

Array A sequence of data values. This sequence corresponds to the elements in a rectilinear, n-dimensional matrix $( 1 \leq n \leq$ 999, or n = 0 in the case of a null array).

Array value The value of an element of an array in a FITS file, without the application of the associated linear transformation to derive the physical value.

ASCII American National Standard Code for Information Interchange.

ASCII character Any member of the seven-bit ASCII character set.

ASCII digit One of the ten ASCII characters ‘0’ through ‘9’, which are represented by decimal character codes 48 through 57 (hexadecimal 30 through 39).

ASCII NULL The ASCII character that has all eight bits set to zero.

ASCII space The ASCII character for space, which is represented by decimal 32 (hexadecimal 20).

ASCII text The restricted set of ASCII characters decimal 32 through 126 (hexadecimal 20 through 7E).

Basic FITS The FITS structure consisting of the primary header followed by a single primary data array. This is also known as Single Image FITS (SIF), as opposed to Multi-Extension FITS (MEF) files that contain one or more extensions following the primary HDU.

Big endian The numerical data format used in FITS files in which the most-significant byte of the value is stored first followed by the remaining bytes in order of significance.

Bit A single binary digit.

Byte An ordered sequence of eight consecutive bits treated as a single entity.

Card image An obsolete term for an 80-character keyword record derived from the 80-column punched computer cards that were prevalent in the 1960s and 1970s.

Character string A sequence of one or more of the restricted set of ASCII-text characters, decimal 32 through 126 (hexadecimal 20 through 7E).

Conforming extension An extension whose keywords and organization adhere to the requirements for conforming extensions defined in Sect. 3.4.1 of this Standard.

Data block A 2880-byte FITS block containing data described by the keywords in the associated header of that HDU.

Deprecate To express disapproval of. This term is used to refer to obsolete structures that should not be used in new FITS files, but which shall remain valid indefinitely.

Entry A single value in an ASCII-table or binary-table standard extension.

Extension A FITS HDU appearing after the primary HDU in a FITS file.

Extension type name The value of the XTENSION keyword, used to identify the type of the extension.

Field A component of a larger entity, such as a keyword record or a row of an ASCII-table or binary-table standard extension. A field in a table-extension row consists of a set of zero-or-more table entries collectively described by a single format.

File A sequence of one or more records terminated by an endof-file indicator appropriate to the medium.

FITS Flexible Image Transport System.

FITS block A sequence of 2880 eight-bit bytes aligned on 2880-byte boundaries in the FITS file, most commonly either a header block or a data block. Special records are another infrequently used type of FITS block. This block length was chosen because it is evenly divisible by the byte and word lengths of all known computer systems at the time FITS was developed in 1979.

FITS file A file with a format that conforms to the specifications in this document.

FITS structure One of the components of a FITS file: the primary HDU, the random-groups records, an extension, or, collectively, the special records following the last extension.

FITS Support Office The FITS information website that is maintained by the IAUFWG and is currently hosted at [http://fits.gsfc.nasa.gov](http://fits.gsfc.nasa.gov).

Floating point A computer representation of a real number.

Fraction The field of the mantissa (or significand) of a floatingpoint number that lies to the right of its implied binary point.

Group parameter value The value of one of the parameters preceding a group in the random-groups structure, without the application of the associated linear transformation.

3

<!-- page 10 of 75 -->

**HDU** Header and Data Unit. A data structure consisting of a header and the data the header describes. Note that an HDU may consist entirely of a header with no data blocks.

**Header** A series of keyword records organized within one or more header blocks that describes structures and/or data that follow it in the FITS file.

**Header block** A 2880-byte FITS block containing a sequence of thirty-six 80-character keyword records.

**Heap** The supplemental data area following the main data table in a binary-table standard extension.

**IAU** International Astronomical Union.

**IAUFWG** International Astronomical Union FITS Working Group.

**IEEE** Institute of Electrical and Electronic Engineers.

**IEEE NaN** IEEE Not-a-Number value; used to represent undefined floating-point values in FITS arrays and binary tables.

**IEEE special values** Floating-point number byte patterns that have a special, reserved meaning, such as −0, **±∞**, ±underflow, ±overflow, ±denormalized, ±NaN. (See Appendix E).

**Indexed keyword** A keyword name that is of the form of a fixed root with an appended positive integer index number.

**Keyword name** The first eight bytes of a keyword record, which contain the ASCII name of a metadata quantity (unless it is blank).

**Keyword record** An 80-character record in a header block consisting of a keyword name in the first eight characters followed by an optional value indicator, value, and comment string. The keyword record shall be composed only of the restricted set of ASCII-text characters ranging from decimal 32 to 126 (hexadecimal 20 to 7E).

**Mandatory keyword** A keyword that must be used in all FITS files or a keyword required in conjunction with particular FITS structures.

**Mantissa** Also known as significand. The component of an IEEE floating-point number consisting of an explicit or implicit leading bit to the left of its implied binary point and a fraction field to the right.

**MEF** Multi-Extension FITS, i.e., a FITS file containing a primary HDU followed by one or more extension HDUs.

**NOST** NASA/Science Office of Standards and Technology.

**Physical value** The value in physical units represented by an element of an array and possibly derived from the array value using the associated, but optional, linear transformation.

**Pixel** Short for ‘Picture element’; a single location within an array.

**Primary data array** The data array contained in the primary HDU.

**Primary HDU** The first HDU in a FITS file.

**Primary header** The first header in a FITS file, containing information on the overall contents of the file (as well as on the primary data array, if present).

**Random Group** A FITS structure consisting of a collection of groups’, where a group consists of a subarray of data and a set of associated parameter values. Random groups are deprecated for any use other than for radio interferometry data.

**Record** A sequence of bits treated as a single logical entity.

**Repeat count** The number of values represented in a field in a binary-table standard extension.

**Reserved keyword** An optional keyword that must be used only in the manner defined in this Standard.

**SIF** Single Image FITS, i.e., a FITS file containing only a primary HDU, without any extension HDUs. Also known as Basic FITS.

**Special records** A series of one or more FITS blocks following the last HDU whose internal structure does not otherwise conform to that for the primary HDU or to that specified for a conforming extension in this Standard. Any use of special records requires approval from the IAU FITS Working Group.

**Standard extension** A conforming extension whose header and data content are completely specified in Sect. 7 of this Standard, namely, an image extension, an ASCII-table extension, or a binary-table extension.

## 3. FITS file organization

## 3.1. Overall file structure

A FITS file shall be composed of the following FITS structures, in the order listed:

– Primary header and data unit (HDU).

– Conforming Extensions (optional).

– Other special records (optional, restricted).

A FITS file composed of only the primary HDU is sometimes referred to as a Basic FITS file, or a Single Image FITS (SIF) file, and a FITS file containing one or more extensions following the primary HDU is sometimes referred to as a Multi-Extension FITS (MEF) file.

Each FITS structure shall consist of an integral number of FITS blocks, which are each 2880 bytes (23040 bits) in length. The primary HDU shall start with the first FITS block of the FITS file. The first FITS block of each subsequent FITS structure shall be the FITS block immediately following the last FITS block of the preceding FITS structure.

This Standard neither imposes a limit on the total size of a FITS file, nor imposes a limit on the size of an individual HDU within a FITS file. Software packages that read or write data according to this Standard could be limited, however, in the size of files that are supported. In particular, some software systems have historically only supported files up to 2 bytes in size (approximately 2.1 × 10<sup>9</sup> bytes).

## 3.2. Individual FITS Structures

The primary HDU and every extension HDU shall consist of one or more 2880-byte header blocks immediately followed by an optional sequence of associated 2880-byte data blocks. The header blocks shall contain only the restricted set of ASCII-text characters, decimal 32 through 126 (hexadecimal 20 through 7E). The ASCII control characters with decimal values less than 32 (including the null, tab, carriage return, and line-feed characters), and the delete character (decimal 127 or hexadecimal 7F) must not appear anywhere within a header block.

## 3.3. Primary header and data unit

The first component of a FITS file shall be the primary HDU, which always contains the primary header and may be followed by the primary data array. If the primary data array has zero length, as determined by the values of the NAXIS and NAXISn

4

<!-- page 11 of 75 -->

![Image block](doc:5624dca/tier:standard/page:11/block:1)

Fig. 1: Arrays of more than one dimension shall consist of a sequence such that the index along Axis 1 varies most rapidly and those along subsequent axes progressively less rapidly.

keywords in the primary header (Sect. 4.4.1), then the primary HDU shall contain no data blocks.

## 3.3.1. Primary header

The header of a primary HDU shall consist of one or more header blocks, each containing a series of 80-character keyword records containing only the restricted set of ASCII-text characters. Each 2880-byte header block contains 36 keyword records. The last header block must contain the END keyword (defined in Sect. 4.4.1), which marks the logical end of the header. Keyword records without information (e.g., following the END keyword) shall be filled with ASCII spaces (decimal 32 or hexadecimal 20).

## 3.3.2. Primary data array

The primary data array, if present, shall consist of a single data array with from 1 to 999 dimensions (as specified by the NAXIS keyword defined in Sect. 4.4.1). The random-groups convention in the primary data array is a more-complicated structure and is discussed separately in Sect. 6. The entire array of data values are represented by a continuous stream of bits starting with the first bit of the first data block. Each data value shall consist of a fixed number of bits that is determined by the value of the BITPIX keyword (Sect. 4.4.1). Arrays of more than one dimension shall consist of a sequence such that the index along Axis 1 varies most rapidly, that along Axis 2 next most rapidly, and those along subsequent axes progressively less rapidly, with that along Axis m, where m is the value of NAXIS, varying least rapidly. There is no space or any other special character between the last value on a row or plane and the first value on the next row or plane of a multi-dimensional array. Except for the location of the first element, the array structure is independent of the FITS block structure. This storage order is shown schematically in Fig. 1 and is the same order as in multi-dimensional arrays in the Fortran programming language (ISO 2004). The index count along each axis shall begin with 1 and increment by 1 up to the value of the NAXISn keyword (Sect. 4.4.1).

If the data array does not fill the final data block, the remainder of the data block shall be filled by setting all bits to zero.

The individual data values shall be stored in big-endian byte order such that the byte containing the most-significant bits of the value appears first in the FITS file, followed by the remaining bytes, if any, in decreasing order of significance.

## 3.4. Extensions

## 3.4.1. Requirements for conforming extensions

All extensions, whether or not further described in this Standard, shall fulfill the following requirements to be in conformance with this FITS Standard. New extension types should be created only when the organization of the information is such that it cannot be handled by one of the existing extension types. A FITS file that contains extensions is commonly referred to as a multi-extension FITS (MEF) file.

## 3.4.1.1. Identity

Each extension type shall have a unique type name, specified in the header by the XTENSION keyword (Sect. 4.4.1). To preclude conflict, extension type names must be registered with the IAUFWG. The current list of registered extensions is given in Appendix F. An up-to-date list is also maintained on the FITS Support Office website.

## 3.4.1.2. Size specification

The total number of bits in the data of each extension shall be specified in the header for that extension, in the manner prescribed in Sect. 4.4.1.

## 3.4.2. Standard extensions

A standard extension is a conforming extension whose organization and content are completely specified in Sect. 7 of this Standard. Only one extension format shall be approved for each type of data organization.

## 3.4.3. Order of extensions

An extension may follow the primary HDU or another conforming extension. Standard extensions and other conforming extensions may appear in any order in a FITS file.

## 3.5. Special records (restricted use)

Special records are 2880-byte FITS blocks following the last HDU of the FITS file that have an unspecified structure that does not meet the requirements of a conforming extension. The first eight bytes of the special records must not contain the string ‘XTENSION’. It is recommended that they do not contain the string ‘SIMPLE ’. The contents of special records are not otherwise specified by this Standard.

Special records were originally designed as a way for the FITS format to evolve by allowing new FITS structures to be implemented. Following the development of conforming extensions, which provide a general mechanism for storing different types of data structures in FITS format in a well defined manner, the need for other new types of FITS data structures has been

5

<!-- page 12 of 75 -->

greatly reduced. Consequently, further use of special records is restricted and requires the approval of the IAU FITS Working Group.

## 3.6. Physical blocking

## 3.6.1. Bit-stream devices

For bit-stream devices, including but not restricted to logical file systems, FITS files shall be interpreted as a sequence of one or more 2880-byte FITS blocks, regardless of the physical blocking structure of the underlying recording media. When writing a FITS file on media with a physical block size unequal to the 2880-byte FITS block length, any bytes remaining in the last physical block following the end of the FITS file should be set to zero. Similarly, when reading FITS files on such media, any bytes remaining in the last physical block following the end of the FITS file shall be disregarded.

## 3.6.2. Sequential media

The FITS format was originally developed for writing files on sequential magnetic-tape devices. The following rules on how to write to sequential media (Grosbøl & Wells 1994) are now irrelevant to most current data-storage devices.

If physically possible, FITS files shall be written on sequential media in blocks that are from one to ten integer multiples of 2880 bytes in length. If this is not possible, the FITS file shall be written as a bit stream using the native block size of the sequential device. Any bytes remaining in the last block following the end of the FITS file shall be set to zero.

When reading FITS files on sequential media, any files shorter than 2880 bytes in length (e.g., ANSI tape labels) are not considered part of the FITS files and should be disregarded.

## 3.7. Restrictions on changes

Any structure that is a valid FITS structure shall remain a valid FITS structure at all future times. Use of certain valid FITS structures may be deprecated by this or future FITS Standard documents.

## 4. Headers

The first two sections of this chapter define the structure and content of header keyword records. Sect. 4.3 offers recommendations on how physical units should be expressed. The final section defines the mandatory and reserved keywords for primary arrays and conforming extensions.

## 4.1. Keyword records

## 4.1.1. Syntax

Each 80-character header keyword record shall consist of a keyword name, a value indicator (only required if a value is present), an optional value, and an optional comment. Keywords may appear in any order except where specifically stated otherwise in this Standard. It is recommended that the order of the keywords in FITS files be preserved during data processing operations because the designers of the FITS file may have used conventions that attach particular significance to the order of certain

keywords (e.g., by grouping sequences of COMMENT keywords at specific locations in the header, or appending HISTORY keywords in chronological order of the data processing steps or using CONTINUE keywords to generate long-string keyword values).

A formal syntax, giving a complete definition of the syntax of FITS keyword records, is given in Appendix A. It is intended as an aid in interpreting the text defining the Standard.

In earlier versions of this Standard a FITS keyword, assumed as an item whose value is to be looked up by name (and pre-sumably assigned to a variable) by a FITS-reading program, was associated one to one to a single header keyword record. With the introduction of continued (long-string) keywords (see Sect. 4.2.1.2), such FITS keywords may span more than one header keyword record, and the value shall be created by concatenation as explained in Sect. 4.2.1.2.

## 4.1.2. Components

## 4.1.2.1. Keyword name (Bytes 1 through 8)

The keyword name shall be a left justified, eight-character, space-filled, ASCII string with no embedded spaces. All digits 0 through 9 (decimal ASCII codes 48 to 57, or hexadecimal 30 to 39) and upper case Latin alphabetic characters ’A’ through’Z’ (decimal 65 to 90 or hexadecimal 41 to 5A) are permitted; lower-case characters shall not be used. The underscore (’ ’, decimal 95 or hexadecimal 5F) and hyphen (’-’, decimal 45 or hexadecimal 2D) are also permitted. No other characters are permitted.<sup>3</sup> For indexed keyword names that have a single positive integer index counter appended to the root name, the counter shall not have leading zeros (e.g., NAXIS1, not NAXIS001). Note that keyword names that begin with (or consist solely of) any combination of hyphens, underscores, and digits are legal.

## 4.1.2.2. Value indicator (Bytes 9 and 10)

If the two ASCII characters '= ' (decimal 61 followed by decimal 32) are present in Bytes 9 and 10 of the keyword record, this indicates that the keyword has a value field associated with it, unless it is one of the commentary keywords defined in Sect. 4.4.2 (i.e., a HISTORY, COMMENT, or completely blank keyword name), which, by definition, have no value.

## 4.1.2.3. Value/comment (Bytes 11 through 80)

In keyword records that contain the value indicator in Bytes 9 and 10, the remaining Bytes 11 through 80 of the record shall contain the value, if any, of the keyword, followed by optional comments. In keyword records without a value indicator, Bytes 9 through 80 should be interpreted as commentary text, however, this does not preclude conventions that interpret the content of these bytes in other ways.

The value field, when present, shall contain the ASCII-text representation of a literal string constant, a logical constant, or a numerical constant, in the format specified in Sect. 4.2. The value field may be a null field; i.e., it may consist entirely of

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">3 This requirement differs from the wording in the original FITS papers. See Appendix H.</span></small>

6

<!-- page 13 of 75 -->

spaces, in which case the value associated with the keyword is undefined.

The mandatory FITS keywords defined in this Standard must not appear more than once within a header. All other keywords that have a value should not appear more than once. If a keyword does appear multiple times with different values, then the value is indeterminate.

If a comment follows the value field, it must be preceded by a slash $( { \it \Psi } ^ { \prime } ) ^ { \prime }$ , decimal 47 or hexadecimal 2F).3 A space between the value and the slash is strongly recommended. The comment may contain any of the restricted set of ASCII-text characters, decimal 32 through 126 (hexadecimal 20 through 7E). The ASCII control characters with decimal values less than 32 (including the null, tab, carriage return, and line-feed characters), and the delete character (decimal 127 or hexadecimal 7F) must not appear anywhere within a keyword record.

## 4.2. Value

The structure of the value field depends on the data type of the value. The value field represents a single value and not an array of values.<sup>3</sup> The value field must be in one of two formats: fixed or free. The fixed-format is required for values of mandatory keywords and is recommended for values of all other keywords.

## 4.2.1. Character string

## 4.2.1.1 Single-record string keywords

A character-string value shall be composed only of the set of restricted ASCII-text characters, decimal 32 through 126 (hexadecimal 20 through 7E) enclosed by single-quote characters (“’”, decimal 39, hexadecimal 27). A single quote is represented within a string as two successive single quotes, e.g., O’HARA = 'O''HARA'. Leading spaces are significant; trailing spaces are not. This Standard imposes no requirements on the case sensitivity of character string values unless explicitly stated in the definition of specific keywords.

If the value is a fixed-format character string, the starting single-quote character must be in Byte 11 of the keyword record and the closing single quote must occur in or before Byte 80. Earlier versions of this Standard also required that fixed-format characters strings must be padded with space characters to at least a length of eight characters so that the closing quote character does not occur before Byte 20. This minimum characterstring length is no longer required, except for the value of the XTENSION keyword (e.g., 'IMAGE ' and 'TABLE '; see Sect. 7), which must be padded to a length of eight characters for backward compatibility with previous usage.

Free-format character strings follow the same rules as fixedformat character strings except that the starting single-quote character may occur after Byte 11. Any bytes preceding the starting quote character and after Byte 10 must contain the space character.

Note that there is a subtle distinction between the following three keywords.

$$
\begin{array}{l l} \text {KEYWORD1 = ''' } & / \text {null string keyword} \\ \text {KEYWORD2 = ' ' } & / \text {empty string keyword} \\ \text {KEYWORD3 = } & / \text {undefined keyword} \end{array}
$$

The value of KEYWORD1 is a null, or zero-length string whereas the value of the KEYWORD2 is an empty string (nominally a single space character because the first space in the string is significant, but trailing spaces are not). The value of KEYWORD3 is undefined and has an indeterminate data type as well, except in cases where the data type of the specified keyword is explicitly defined in this Standard.

The maximum length of a string value that can be represented on a single keyword record is 68 characters, with the opening and closing quote characters in Bytes 11 and 80, respectively. In general, no length limit fewer than 68 is implied for character-valued keywords.

Whenever a keyword value is declared ‘string’ or said to ‘contain a character string’, the length limits in this section apply. The next section applies when the value is declared ‘longstring’.

## 4.2.1.2 Continued string (long-string) keywords

Earlier versions of this Standard only defined single-record string keywords as described in the previous section. The Standard now incorporates a convention (originally developed for use in FITS files from high-energy astrophysics missions) for continuing arbitrarily long string values over a potentially unlimited sequence of multiple consecutive keyword records using the following procedure.

1. Divide the long-string value into a sequence of smaller substrings, each of which contains fewer than 68 characters. (Note that if the string contains any literal single-quote characters, then these must be represented as a pair of singlequote characters in the FITS-keyword value, and these two characters must both be contained within a single substring).

2. Append an ampersand character (’&’) to the end of each substring, except for the last substring. This character serves as a flag to FITS-reading software that this string value may be continued on the following keyword in the header.

3. Enclose each substring with single-quote characters. Non-significant space characters may occur between the ampersand character and the closing quote character.

4. Write the first substring as the value of the specified keyword.

5. Write each subsequent substring, in order, to a series of keywords that all have the reserved keyword name CONTINUE (see Sect. 4.4.2) in Bytes 1 through 8, and have space characters in Bytes 9 and 10 of the keyword record. The substring may be located anywhere in Bytes 11 through 80 of the keyword record and may be preceded by non-significant space characters starting in Byte 11. A comment string may follow the substring; if present, the comment string must be separated from the substring by a forward-slash character (’/’). Also, it is strongly recommended that the slash character be preceded by a space character.

The CONTINUE keyword must not be used with of any of the mandatory or reserved keywords defined in this Standard unless explicitly declared of type long-string.

The following keyword records illustrate a string value that is continued over multiple keyword records. (Note: the length of the substrings have been reduced to fit within the page layout.)

WEATHER = 'Partly cloudy during the evening $\pmb { \xi } \pmb { \xi } ^ { \dagger }$

7

<!-- page 14 of 75 -->

CONTINUE 'ollowed by cloudy skies overnight. $\pmb { \& }$ CONTINUE ' Low 21C. Winds NNE at 5 to 10 mph.'

If needed, additional space for the keyword comment field can be generated by continuing the string value with one or more null strings, as illustrated schematically below.

```txt
STRKEY = 'This keyword value is continued &'
CONTINUE ' over multiple keyword records.&'
CONTINUE '&' / The comment field for this
CONTINUE '&' / keyword is also continued
CONTINUE '' / over multiple records.
```

FITS-reading software can reconstruct the long-string value by following an inverse procedure of checking if the string value ends with the $\therefore g$ character and is immediately followed by a conforming CONTINUE keyword record. If both conditions are true, then concatenate the substring from the CONTINUE record onto the previous substring after first deleting the trailing $\therefore g$ character. Repeat these steps until all subsequent CONTINUE records have been processed.

Note that if a string value ends with the ’&’ character, but is not immediately followed by a CONTINUE keyword that conforms to all the previously described requirements, then the $\therefore g$ character should be interpreted as the literal last character in the string. Also, any ‘orphaned’ CONTINUE keyword records (formally not invalidating the FITS file, although likely representing an error with respect to what the author of the file meant) should be interpreted as containing commentary text in Bytes $9 -$ 80 (similar to a COMMENT keyword).

## 4.2.2. Logical

If the value is a fixed-format logical constant, it shall appear as an upper-case T or F in Byte 30. A logical value is represented in free-format by a single character consisting of an upper-case T or F as the first non-space character in Bytes 11 through 80.

## 4.2.3. Integer number

If the value is a fixed-format integer, the ASCII representation shall be right-justified in Bytes 11 through 30. An integer consists of a ’+’ (decimal 43 or hexadecimal 2B) $\mathbf { 0 } \mathbf { I } ^ { \mathrm { ~   ~ } ^ { \prime } } - \mathbf { \Lambda } ^ { \prime }$ (decimal 45 or hexadecimal 2D) sign, followed by one or more contiguous ASCII digits (decimal 48 to 57 or hexadecimal 30 to 39), with no embedded spaces. The leading ’+’ sign is optional. Leading zeros are permitted, but are not significant. The integer representation shall always be interpreted as a signed, decimal number. This Standard does not limit the range of an integer keyword value, however, software packages that read or write data according to this Standard could be limited in the range of values that are supported (e.g., to the range that can be represented by a 32-bit or 64-bit signed binary integer).

A free-format integer value follows the same rules as fixedformat integers except that the ASCII representation may occur anywhere within Bytes 11 through 80.

## 4.2.4. Real floating-point number

If the value is a fixed-format real floating-point number, the ASCII representation shall be right-justified in Bytes 11 through 30.

Table 3: IAU-recommended basic units.

<table><tr><td>Quantity</td><td>Unit</td><td>Meaning</td><td>Notes</td></tr><tr><td colspan="4">SI base &amp; supplementary units</td></tr><tr><td>length</td><td>m</td><td>meter</td><td></td></tr><tr><td>mass</td><td>kg</td><td>kilogram</td><td>g gram allowed</td></tr><tr><td>time</td><td>s</td><td>second</td><td></td></tr><tr><td>plane angle</td><td>rad</td><td>radian</td><td></td></tr><tr><td>solid angle</td><td>sr</td><td>steradian</td><td></td></tr><tr><td>temperature</td><td>K</td><td>kelvin</td><td></td></tr><tr><td>electric current</td><td>A</td><td>ampere</td><td></td></tr><tr><td>amount of substance</td><td>mol</td><td>mole</td><td></td></tr><tr><td>luminous intensity</td><td>cd</td><td>candela</td><td></td></tr><tr><td colspan="4">IAU-recognized derived units</td></tr><tr><td>frequency</td><td>Hz</td><td>hertz</td><td> $s^{-1}$ </td></tr><tr><td>energy</td><td>J</td><td>joule</td><td>N m</td></tr><tr><td>power</td><td>W</td><td>watt</td><td> $J\,s^{-1}$ </td></tr><tr><td>electric potential</td><td>V</td><td>volt</td><td> $J\,C^{-1}$ </td></tr><tr><td>force</td><td>N</td><td>newton</td><td>kg m  $s^{-2}$ </td></tr><tr><td>pressure, stress</td><td>Pa</td><td>pascal</td><td> $N\,m^{-2}$ </td></tr><tr><td>electric charge</td><td>C</td><td>coulomb</td><td>A s</td></tr><tr><td>electric resistance</td><td>Ohm</td><td>ohm</td><td> $V\,A^{-1}$ </td></tr><tr><td>electric conductance</td><td>S</td><td>siemens</td><td> $A\,V^{-1}$ </td></tr><tr><td>electric capacitance</td><td>F</td><td>farad</td><td> $C\,V^{-1}$ </td></tr><tr><td>magnetic flux</td><td>Wb</td><td>weber</td><td>V s</td></tr><tr><td>magnetic flux density</td><td>T</td><td>tesla</td><td> $Wb\,m^{-2}$ </td></tr><tr><td>inductance</td><td>H</td><td>henry</td><td> $Wb\,A^{-1}$ </td></tr><tr><td>luminous flux</td><td>lm</td><td>lumen</td><td>cd sr</td></tr><tr><td>illuminance</td><td>lx</td><td>lux</td><td> $lm\,m^{-2}$ </td></tr></table>

A floating-point number is represented by a decimal number followed by an optional exponent, with no embedded spaces. A decimal number shall consist of a $\text{" }+ \text{" }$ (decimal 43 or hexadecimal 2B) $\mathbf { 0 } \mathbf { I } ^ { \mathrm { ~   ~ } ^ { \prime } } - \mathbf { \Lambda } ^ { \prime }$ (decimal 45 or hexadecimal 2D) sign, followed by a sequence of ASCII digits containing a single decimal point $( \mathbf { \dot { \nabla } } \cdot \mathbf { \dot { \nabla } } )$ , representing an integer part and a fractional part of the floating-point number. The leading ’+’ sign is optional. At least one of the integer part or fractional part must be present. If the fractional part is present, the decimal point must also be present. If only the integer part is present, the decimal point may be omitted, in which case the floating-point number is indistinguishable from an integer. The exponent, if present, consists of an exponent letter followed by an integer. Letters in the exponential form $( ^ { \prime } \mathbf { E } ^ { \prime }$ or ${ { } ^ { \flat } \mathrm { D }   ^ { \flat } ) ^ { 4 } }$ shall be upper case. The full precision of 64-bit values cannot be expressed over the whole range of values using the fixed-format. This Standard neither imposes an upper limit on the number of digits of precision, nor any limit on the range of floating-point keyword values. Software packages that read or write data according to this Standard could be limited, however, in the range of values and exponents that are supported (e.g., to the range that can be represented by a 32-bit or 64-bit floatingpoint number).

A free-format floating-point value follows the same rules as a fixed-format floating-point value except that the ASCII representation may occur anywhere within Bytes 11 through 80.

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">’ ’</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">4 The ’D’ exponent form is traditionally used when representing values that have more decimals of precision or a larger magnitude than can be represented by a single-precision 32-bit floating-point number, but otherwise there is no distinction between E or D . ’ ’</span></small>

8

<!-- page 15 of 75 -->

Table 4: Additional allowed units.

<table><tr><td>Quantity</td><td>Unit</td><td>Meaning</td><td>Notes</td></tr><tr><td rowspan="4">plane angle</td><td>deg</td><td>degree of arc</td><td> $\pi/180$  rad</td></tr><tr><td>arcmin</td><td>minute of arc</td><td>1/60 deg</td></tr><tr><td>arcsec</td><td>second of arc</td><td>1/3600 deg</td></tr><tr><td>mas</td><td>milli-second of arc</td><td>1/3 600 000 deg</td></tr><tr><td rowspan="5">time</td><td>min</td><td>minute</td><td>60 s</td></tr><tr><td>h</td><td>hour</td><td>60 min = 3600 s</td></tr><tr><td>d</td><td>day</td><td>86 400 s</td></tr><tr><td>† a</td><td>year (Julian)</td><td>31 557 600 s (365.25 d), peta a(Pa) forbidden</td></tr><tr><td>† yr</td><td>year (Julian)</td><td>a is IAU-style</td></tr><tr><td rowspan="3">energy*</td><td>† eV</td><td>electron volt</td><td> $1.6021765 \times 10^{-19}$  J</td></tr><tr><td>‡ erg</td><td>erg</td><td> $10^{-7}$  J</td></tr><tr><td>Ry</td><td>rydberg</td><td> $\frac{1}{2}\left(\frac{2\pi e^{2}}{hc}\right)^{2}m_{e}c^{2}=13.605692$  eV</td></tr><tr><td rowspan="2">mass*</td><td>solMass</td><td>solar mass</td><td> $1.9891 \times 10^{30}$  kg</td></tr><tr><td>u</td><td>unified atomic mass unit</td><td> $1.6605387 \times 10^{-27}$  kg</td></tr><tr><td rowspan="6">luminosity length</td><td>solLum</td><td>Solar luminosity</td><td> $3.8268 \times 10^{26}$  W</td></tr><tr><td>‡ Angstrom</td><td>angstrom</td><td> $10^{-10}$  m</td></tr><tr><td>solRad</td><td>Solar radius</td><td> $6.9599 \times 10^{8}$  m</td></tr><tr><td>AU</td><td>astronomical unit</td><td> $1.49598 \times 10^{11}$  m</td></tr><tr><td>lyr</td><td>light year</td><td> $9.460730 \times 10^{15}$  m</td></tr><tr><td>† pc</td><td>parsec</td><td> $3.0857 \times 10^{16}$  m</td></tr><tr><td rowspan="4">events</td><td>count</td><td>count</td><td></td></tr><tr><td>ct</td><td>count</td><td></td></tr><tr><td>photon</td><td>photon</td><td></td></tr><tr><td>ph</td><td>photon</td><td></td></tr><tr><td rowspan="3">flux density</td><td>† Jy</td><td>jansky</td><td> $10^{-26}$  W m $^{-2}$  Hz $^{-1}$ </td></tr><tr><td>† mag</td><td>(stellar) magnitude</td><td></td></tr><tr><td>† R</td><td>rayleigh</td><td> $10^{10}/(4\pi)$  photons m $^{-2}$  s $^{-1}$  sr $^{-1}$ </td></tr><tr><td rowspan="4">magnetic field area</td><td>†‡ G</td><td>gauss</td><td> $10^{-4}$  T</td></tr><tr><td>pixel</td><td>(image/detector) pixel</td><td></td></tr><tr><td>pix</td><td>(image/detector) pixel</td><td></td></tr><tr><td>†‡ barn</td><td>barn</td><td> $10^{-28}$  m $^{2}$ </td></tr><tr><td colspan="4">Miscellaneous units</td></tr><tr><td rowspan="9"></td><td>D</td><td>debye</td><td> $\frac{1}{3} \times 10^{-29}$  C.m</td></tr><tr><td>Sun</td><td>relative to Sun</td><td>e.g., abundances</td></tr><tr><td>chan</td><td>(detector) channel</td><td></td></tr><tr><td>bin</td><td>numerous applications</td><td>(including the one-dimensional analog of pixel)</td></tr><tr><td>voxel</td><td>three-dimensional analog of pixel</td><td></td></tr><tr><td>† bit</td><td>binary information unit</td><td></td></tr><tr><td>† byte</td><td>(computer) byte</td><td>eight bits</td></tr><tr><td>adu</td><td>Analog-to-digital converter</td><td></td></tr><tr><td>beam</td><td>beam area of observation</td><td>as in Jy/beam</td></tr></table>

Notes. (†)Addition of prefixes for decimal multiples and submultiples are allowed. (<sup>‡</sup>)Deprecated in IAU Style Manual (McNally 1988) but still in use. (∗)Conversion factors from CODATA Internationally recommended values of the fundamental physical constants 2002 ([http://physics.nist.gov/cuu/Constants/](http://physics.nist.gov/cuu/Constants/)).

## 4.2.5. Complex integer number

There is no fixed-format for complex integer numbers.<sup>5</sup>

If the value is a complex integer number, the value must be represented as a real part and an imaginary part, separated by a comma and enclosed in parentheses e.g., (123, 45). Spaces may precede and follow the real and imaginary parts. The real and imaginary parts are represented in the same way as integers (Sect. 4.2.3). Such a representation is regarded as a single value for the complex integer number. This representation may be located anywhere within Bytes 11 through 80.

## 4.2.6. Complex floating-point number

There is no fixed-format for complex floating-point numbers.<sup>5</sup>

If the value is a complex floating-point number, the value must be represented as a real part and an imaginary part, separated by a comma and enclosed in parentheses, e.g., (123.23, -45.7). Spaces may precede and follow the real and imaginary parts. The real and imaginary parts are represented in the same way as floating-point values (Sect. 4.2.4). Such a representation is regarded as a single value for the complex floating-point number. This representation may be located anywhere within Bytes 11 through 80.

9

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">5 This requirement differs from the wording in the original FITS papers. See Appendix H.</span></small>

<!-- page 16 of 75 -->

## 4.2.7. Date

There is strictly no such thing as a data type for date valued keywords, however a pseudo data type of datetime is defined in Sect. 9.1.1 and must be used to write ISO-8601 datetime strings as character strings.

If a keyword needs to express a time in JD or MJD (see Sect. 9), this can be formatted as an arbitrary precision number, optionally separating the integer and fractional part as specified in Sect. 9.2.2.

## 4.3. Units

When a numerical keyword value represents a physical quantity, it is recommended that units be provided. Units shall be represented with a string of characters composed of the restricted ASCII-text character set. Unit strings can be used as values of keywords (e.g., for the reserved keywords BUNIT, and TUNITn), as an entry in a character-string column of an ASCII-table or binary-table extension, or as part of a keyword comment string (see Sect. 4.3.2, below).

The units of all FITS header keyword values, with the exception of measurements of angles, should conform with the recommendations in the IAU Style Manual (McNally 1988). For angular measurements given as floating-point values and specified with reserved keywords, the units should be degrees (i.e., deg). If a requirement exists within this Standard for the units of a keyword, then those units must be used.

The units for fundamental physical quantities recommended by the IAU are given in Table 3. Table 4 lists additional units that are commonly used in astronomy. Further specifications for time units are given in Sect. 9.3. The recommended plain-text form for the IAU-recognized base units are given in Column 2 of both tables.<sup>6</sup> All base units strings may be preceded, with no intervening spaces, by a single character (two for deca) taken from Table 5 and representing scale factors mostly in steps of $1 0 ^ { 3 } .$ Compound prefixes (e.g., ZYeV for $1 0 ^ { 4 5 } ~ \mathrm { e V ) } ^ { 3 }$ must not be used.

## 4.3.1. Construction of units strings

Compound units strings may be formed by combining strings of base units (including prefixes, if any) with the recommended syntax described in Table 6. Two or more base units strings (called str1 and str2 in Table 6) may be combined using the restricted set of (explicit or implicit) operators that provide for multiplication, division, exponentiation, raising arguments to powers, or taking the logarithm or square-root of an argument. Note that functions such as log actually require dimensionless arguments, so that log(Hz), for example, actually means log(x/1 Hz). The final units string is the compound string, or a compound of compounds, preceded by an optional numeric multiplier of the form $1 0 ^ { \% \% } k , 1 0 ^ { \% } k ,$ or 10±k where k is an integer, optionally surrounded by parentheses with the sign character required in the third form in the absence of parentheses. Creators of FITS files are encouraged to use the numeric multiplier only when the available standard scale factors of Table 5 will not suffice. Parentheses are used for symbol grouping and are strongly

Table 5: Prefixes for multiples and submultiples.

| Submult | Prefix | Char | Mult | Prefix | Char |
| --- | --- | --- | --- | --- | --- |
| $10^{-1}$ | deci | d | 10 | deca | da |
| $10^{-2}$ | centi | c | $10^{2}$ | hecto | h |
| $10^{-3}$ | milli | m | $10^{3}$ | kilo | k |
| $10^{-6}$ | micro | u | $10^{6}$ | mega | M |
| $10^{-9}$ | nano | n | $10^{9}$ | giga | G |
| $10^{-12}$ | pico | p | $10^{12}$ | tera | T |
| $10^{-15}$ | femto | f | $10^{15}$ | peta | P |
| $10^{-18}$ | atto | a | $10^{18}$ | exa | E |
| $10^{-21}$ | zepto | z | $10^{21}$ | zetta | Z |
| $10^{-24}$ | yocto | y | $10^{24}$ | yotta | Y |

recommended whenever the order of operations might be subject to misinterpretation. A space character implies multiplication, which can also be conveyed explicitly with an asterisk or a period. Therefore, although spaces are allowed as symbol separators, their use is discouraged. Note that, per IAU convention, case is significant throughout. The IAU style manual forbids the use of more than one slash $( { \textquotedblleft } / { \textquotedblright } )$ character in a units string. However, since normal mathematical precedence rules apply in this context, more than one slash may be used but is discouraged.

A unit raised to a power is indicated by the unit string followed, with no intervening spaces, by the optional symbols \*\* or followed by the power given as a numeric expression, called expr in Table 6. The power may be a simple integer, with or without sign, optionally surrounded by parentheses. It may also be a decimal number (e.g., 1.5, 0.5) or a ratio of two integers $( \mathrm { e . g . } ,   7 / 9 )$ , with or without sign, which must be surrounded by parentheses. Thus meters squared may be indicated by $\mathfrak { m } ^ { \check { \kappa } \check { \kappa } } ( 2 )$ $\mathrm{m}^{\mathrm{六六}}+2,\mathrm{m}+2,\mathrm{m}2,\mathrm{m}^{\mathrm{六}}2,\mathrm{m}^{\mathrm{六}}(+2)$ , etc. and per meter cubed may be indicated by $m ^ { x _ { x } } - 3 ,$ m-3, mˆ(-3), /m3, and so forth. Meters to the three-halves power may be indicated by m(1.5), mˆ(1.5), $\mathfrak { m } ^ { \check { \kappa } \check { \kappa } } ( 1 . 5 )$ , m(3/2), m\*\*(3/2), and $\mathfrak { m } ^ { \frown } ( 3 / 2 )$ , but not by ms/2 or m1.5.

## 4.3.2. Units in comment fields

If the units of the keyword value are specified in the comment of the header keyword, it is recommended that the units string be enclosed in square brackets (i.e., enclosed by ‘[’ and ‘]’) at the beginning of the comment field, separated from the slash $( { \textquotedblleft } / { \textquotedblright } )$ comment field delimiter by a single space character. An example, using a non-standard keyword, is

$\mathrm{EXPTIME}=1200./[\mathrm{s}]$ exposure time in seconds This widespread, but optional, practice suggests that square brackets should be used in comment fields only for this purpose. Nonetheless, software should not depend on units being expressed in this fashion within a keyword comment, and software should not depend on any string within square brackets in a comment field containing a proper units string.

## 4.4. Keywords

## 4.4.1. Mandatory keywords

Mandatory keywords are required in every HDU as described in the remainder of this subsection. They must be used only as described in this Standard. Values of the mandatory keywords must be written in fixed-format.

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">6 These tables are reproduced from the first in a series of papers on world-coordinate systems (Greisen & Calabretta 2002), which provides examples and expanded discussion.</span></small>

10

<!-- page 17 of 75 -->

Table 6: Characters and strings allowed to denote mathematical operations.

| String | Meaning |
| --- | --- |
| str1 str2 | Multiplication |
| str1*str2 | Multiplication |
| str1.str2 | Multiplication |
| str1/str2 | Division |
| str1**expr | Raised to the power expr |
| str1^expr | Raised to the power expr |
| str1expr | Raised to the power expr |
| log(str1) | Common Logarithm (to base 10) |
| ln(str1) | Natural Logarithm |
| exp(str1) | Exponential ($e^{str1}$) |
| sqrt(str1) | Square root |

Table 7: Mandatory keywords for primary header.

| Position | Keyword |
| --- | --- |
| 1 | SIMPLE = T |
| 2 | BITPIX |
| 3 | NAXIS |
| 4 | NAXISn, n = 1, ..., NAXIS |
|  | $\vdots$ |
|  | (other keywords) |
|  | $\vdots$ |
| last | END |

Table 8: Interpretation of valid BITPIX value.

| Value | Data represented |
| --- | --- |
| 8 | Character or unsigned binary integer |
| 16 | 16-bit two's complement binary integer |
| 32 | 32-bit two's complement binary integer |
| 64 | 64-bit two's complement binary integer |
| -32 | IEEE single-precision floating point |
| -64 | IEEE double-precision floating point |

## 4.4.1.1. Primary header

The SIMPLE keyword is required to be the first keyword in the primary header of all FITS files. The primary header must contain the other mandatory keywords shown in Table 7 in the order given. Other keywords must not intervene between the SIMPLE keyword and the last NAXISn keyword.

SIMPLE keyword. The value field shall contain a logical constant with the value T if the file conforms to this Standard. This keyword is mandatory for the primary header and must not appear in extension headers.<sup>7</sup> A value of F signifies that the file does not conform to this Standard.

BITPIX keyword. The value field shall contain an integer. The absolute value is used in computing the sizes of data structures. It shall specify the number of bits that represent a data value in the associated data array. The only valid values of BITPIX are

given in Table 8. Writers of FITS arrays should select a BITPIX data type appropriate to the form, range of values, and accuracy of the data in the array.

NAXIS keyword. The value field shall contain a non-negative integer no greater than 999 representing the number of axes in the associated data array. A value of zero signifies that no data follow the header in the HDU.

NAXISn keywords. The NAXISn keywords must be present for all values n = 1, . . . , NAXIS, in increasing order of n, and for no other values of n. The value field of this indexed keyword shall contain a non-negative integer representing the number of elements along Axis n of a data array. A value of zero for any of the NAXISn signifies that no data follow the header in the HDU (however, the random-groups structure described in Sect. 6 has NAXIS1 = 0, but will have data following the header if the other NAXISn keywords are non-zero). If NAXIS is equal to 0, there shall not be any NAXISn keywords.

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">7 This requirement differs from the wording in the original FITS papers. See Appendix H.</span></small>

END keyword. This keyword has no associated value. Bytes 9 through 80 shall be filled with ASCII spaces (decimal 32 or hexadecimal 20). The END keyword marks the logical end of the header and must occur in the last 2880-byte FITS block of the header.

The total number of bits in the primary data array, exclusive of fill that is needed after the data to complete the last 2880-byte data block (Sect. 3.3.2), is given by the following expression:

$$
N _ {\mathrm{bits}} = | \text {BITPIX} | \times (\text {NAXIS1} \times \text {NAXIS2} \times \dots \times \text {NAXISM}),\tag{1}
$$

where $N _ { \mathrm { b i t s } }$ must be non-negative and is the number of bits excluding fill, m is the value of NAXIS, and BITPIX and the NAXISn represent the values associated with those keywords. Note that the random-groups convention in the primary array has a morecomplicated structure whose size is given by Eq. 4. The header of the first FITS extension in the file, if present, shall start with the first FITS block following the data block that contains the last bit of the primary data array.

An example of a primary array header is shown in Table 9. In addition to the required keywords, it includes a few of the reserved keywords that are discussed in Sect. 4.4.2.

## 4.4.1.2. Conforming extensions

All conforming extensions, whether or not further specified in this Standard, must use the keywords defined in Table 10 in the order specified. Other keywords must not intervene between the XTENSION keyword and the GCOUNT keyword. The BITPIX, NAXIS, NAXISn, and END keywords are defined in Sect. 4.4.1.

XTENSION keyword. The value field shall contain a character string giving the name of the extension type. This keyword is mandatory for an extension header and must not appear in the primary header.<sup>7</sup> To preclude conflict, extension type names must be registered with the IAUFWG. The current list of registered extensions is given in Appendix F. An up-to-date list is also maintained on the FITS Support Office website.

11

<!-- page 18 of 75 -->

Table 9: Example of a primary array header.

<table><tr><td colspan="2">Keyword records</td></tr><tr><td>SIMPLE =</td><td>T / file does conform to FITS Standard</td></tr><tr><td>BITPIX =</td><td>16 / number of bits per data pixel</td></tr><tr><td>NAXIS =</td><td>2 / number of data axes</td></tr><tr><td>NAXIS1 =</td><td>250 / length of data axis 1</td></tr><tr><td>NAXIS2 =</td><td>300 / length of data axis 2</td></tr><tr><td>OBJECT = &#x27;Cygnus X-1&#x27;</td><td></td></tr><tr><td>DATE = &#x27;2006-10-22&#x27;</td><td></td></tr><tr><td>END</td><td></td></tr></table>

PCOUNT keyword. The value field shall contain an integer that shall be used in any way appropriate to define the data structure, consistent with Eq. 2. In IMAGE (Sect. 7.1) and TABLE (Sect. 7.2) extensions this keyword must have the value 0; in BINTABLE extensions (Sect. 7.3) it is used to specify the number of bytes that follow the main data table in the supplemental data area called the heap. This keyword is also used in the random-groups structure (Sect. 6) to specify the number of parameters preceding each array in a group.

GCOUNT keyword. The value field shall contain an integer that shall be used in any way appropriate to define the data structure, consistent with Eq. 2. This keyword must have the value 1 in the IMAGE, TABLE, and BINTABLE standard extensions defined in Sect. 7. This keyword is also used in the random-groups structure (Sect. 6) to specify the number of random groups present.

The total number of bits in the extension data array (exclusive of fill that is needed after the data to complete the last 2880- byte data block) is given by the following expression:

$$
\begin{array}{r l} N _ {\text {bits}} = & | \text {BITPIX} | \times \text {GCOUNT} \times \\ & (\text {PCOUNT} + \text {NAXIS1} \times \text {NAXIS2} \times \dots \times \text {NAXISM} m), \end{array}\tag{2}
$$

where $N _ { \mathrm { b i t s } }$ must be non-negative and is the number of bits excluding fill; m is the value of NAXIS; and BITPIX, GCOUNT, PCOUNT, and the NAXISn represent the values associated with those keywords. If $N _ { \mathrm { b i t s } }   >   \vec { 0 } ,$ then the data array shall be contained in an integral number of 2880-byte FITS data blocks. The header of the next FITS extension in the file, if any, shall start with the first FITS block following the data block that contains the last bit of the current extension data array.

## 4.4.2. Other reserved keywords

The reserved keywords described below are optional, but if present in the header they must be used only as defined in this Standard. They apply to any FITS structure with the meanings and restrictions defined below. Any FITS structure may further restrict the use of these keywords.

## 4.4.2.1. General descriptive keywords

DATE keyword. The value field shall contain a character string giving the date on which the HDU was created, in the form YYYY-MM-DD, or the date and time when the HDU was created, in the form YYYY-MM-DDThh:mm:ss[.sss. . . ], where YYYY shall be the four-digit calendar year number, MM the two-digit month number with January given by 01 and December by 12, and DD

Table 10: Mandatory keywords in conforming extensions.

| Position | Keyword |
| --- | --- |
| 1 | XTENSION |
| 2 | BITPIX |
| 3 | NAXIS |
| 4 | NAXISn, n = 1, ..., NAXIS |
| 5 | PCOUNT |
| 6 | GCOUNT |
|  | $\vdots$ |
|  | (other keywords) |
|  | $\vdots$ |
| last | END |

the two-digit day of the month. When both date and time are given, the literal T shall separate the date and time, hh shall be the two-digit hour in the day, mm the two-digit number of minutes after the hour, and ss[.sss. . . ] the number of seconds (two digits followed by an optional fraction) after the minute. Default values must not be given to any portion of the date/time string, and leading zeros must not be omitted. The decimal part of the seconds field is optional and may be arbitrarily long, so long as it is consistent with the rules for value formats of Sect. 4.2. Otherwise said, the format for DATE keywords written after January 1, 2000 shall be the ISO-8601 datetime form described in Sect. 9.1.1. See also Sect. 9.5.

The value of the DATE keyword shall always be expressed in UTC when in this format, for all data sets created on Earth.

The following format may appear on files written before January 1, 2000. The value field contains a character string giving the date on which the HDU was created, in the form DD/MM/YY, where DD is the day of the month, MM the month number with January given by 01 and December by 12, and YY the last two digits of the year, the first two digits being understood to be 19. Specification of the date using Universal Time is recommended but not assumed.

When a newly created HDU is substantially a verbatim copy of another HDU, the value of the DATE keyword in the original HDU may be retained in the new HDU instead of updating the value to the current date and time.

ORIGIN keyword. The value field shall contain a character string identifying the organization or institution responsible for creating the FITS file.

EXTEND keyword. The value field shall contain a logical value indicating whether the FITS file is allowed to contain conform-

12

<!-- page 19 of 75 -->

ing extensions following the primary HDU. This keyword may only appear in the primary header and must not appear in an extension header. If the value field is T then there may be conforming extensions in the FITS file following the primary HDU. This keyword is only advisory, so its presence with a value T does not require that the FITS file contains extensions, nor does the absence of this keyword necessarily imply that the file does not contain extensions. Earlier versions of this Standard stated that the EXTEND keyword must be present in the primary header if the file contained extensions, but this is no longer required.

BLOCKED keyword. This keyword is deprecated and should not be used in new FITS files. It is reserved primarily to prevent its use with other meanings. As previously defined, this keyword, if used, was required to appear only within the first 36 keywords in the primary header. Its presence with the required logical value of T advised that the physical block size of the FITS file on which it appears may be an integral multiple of the FITS block length and not necessarily equal to it.

## 4.4.2.2. Keywords describing observations

DATE-OBS keyword. The format of the value field for DATE-OBS keywords shall follow the prescriptions for the DATE keyword (Sect. 4.4.2 and Sect. 9.1.1 Either the four-digit year format or the two-digit year format may be used for observation dates from 1900 through 1999, although the four-digit format is recommended.

When the format with a four-digit year is used, the default interpretations for time should be UTC for dates beginning 1972-01-01 and UT before. Other date and time scales are permissible. The value of the DATE-OBS keyword shall be expressed in the principal time system or time scale of the HDU to which it belongs; if there is any chance of ambiguity, the choice should be clarified in comments. The value of DATE-OBS shall be assumed to refer to the start of an observation, unless another interpretation is clearly explained in the comment field. Explicit specification of the time scale is recommended. By default, times for TAI and times that run simultaneously with TAI, e.g., UTC and TT, will be assumed to be as measured at the detector (or, in practical cases, at the observatory). For coordinate times such as TCG, TCB, and TDB, the default shall be to include light-time corrections to the associated spatial origin, namely the geocenter for TCG and the Solar System barycenter for the other two. Conventions may be developed that use other time systems. Time scales are now discussed in detail in Sect. 9.2.1 and Table 30.

When the value of DATE-OBS is expressed in the two-digit year form, allowed for files written before January 1, 2000 with a year in the range 1900–1999, there is no default assumption as to whether it refers to the start, middle or end of an observation.

DATExxxx keywords. The value fields for all keywords beginning with the string DATE whose value contains date, and optionally time, information shall follow the prescriptions for the DATE-OBS keyword. See also Sect. 9.1.1 for the datetime format, and Sect. 9.5 for further global time keywords specified by the Standard.

TELESCOP keyword. The value field shall contain a character string identifying the telescope used to acquire the data associated with the header.

INSTRUME keyword. The value field shall contain a character string identifying the instrument used to acquire the data associated with the header.

OBSERVER keyword. The value field shall contain a character string identifying who acquired the data associated with the header.

OBJECT keyword. The value field shall contain a character string giving a name for the object observed.

## 4.4.2.3. Bibliographic keywords

AUTHOR keyword. The value field shall contain a character string identifying who compiled the information in the data associated with the header. This keyword is appropriate when the data originate in a published paper or are compiled from many sources.

REFERENC keyword. The value field shall contain a character string citing a reference where the data associated with the header are published. It is recommended that either the 19-digit bibliographic identifier<sup>8</sup> used in the Astrophysics Data System bibliographic databases ([http://adswww.harvard.edu/](http://adswww.harvard.edu/)) or the Digital Object Identifier ([http://doi.org](http://doi.org)) be included in the value string, when available (e.g., ’1994A&AS..103..135A’ or’doi:10.1006/jmbi.1998.2354’).

## 4.4.2.4. Commentary keywords

These keywords provide commentary information about the contents or history of the FITS file and may occur any number of times in a header. These keywords shall have no associated value even if the value indicator characters \`= ' appear in Bytes 9 and 10 (hence it is recommended that these keywords not contain the value indicator). Bytes 9 through 80 may contain any of the restricted set of ASCII-text characters, decimal 32 through 126 (hexadecimal 20 through 7E).

In earlier versions of this Standard continued string keywords (see Sect. 4.2.1.2) could be handled as commentary keywords if the relevant convention was not supported. Now CONTINUE keywords shall be honoured as specified in Sect. 4.2.1.2.

COMMENT keyword. This keyword may be used to supply any comments regarding the FITS file.

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">8 This bibliographic convention (Schmitz et al. 1995) was initially developed for use within NED (NASA/IPAC Extragalactic Database) and SIMBAD (operated at CDS, Strasbourg, France).</span></small>

13

<!-- page 20 of 75 -->

HISTORY keyword. This keyword should be used to describe the history of steps and procedures associated with the processing of the associated data.

Keyword field is blank. This keyword may be used to supply any comments regarding the FITS file. It is frequently used for aesthetic purposes to provide a break between groups of related keywords in the header.

A sequence of one or more entirely blank keyword records (consisting of 80 ASCII space characters) that immediately pre-cede the END keyword may be interpreted as non-significant fill space that may be overwritten when new keywords are appended to the header. This usage convention enables an arbitrarily large amount of header space to be preallocated when the FITS HDU is first created, which can help mitigate the potentially timeconsuming alternative of having to shift all the following data in the file by 2880 bytes to make room for a new FITS header block each time space is needed for a new keyword.

## 4.4.2.5. Keywords that describe arrays

These keywords are used to describe the contents of an array, either in the primary array, in an IMAGE extension (Sect. 7.1), or in a series of random groups (Sect. 6). They are optional, but if they appear in the header describing an array or groups, they must be used as defined in this section of this Standard. They shall not be used in headers describing other structures unless the meaning is the same as defined here.

BSCALE keyword. This keyword shall be used, along with the BZERO keyword, to linearly scale the array pixel values (i.e., the actual values stored in the FITS file) to transform them into the physical values that they represent using Eq. 3.

$$
\text {physical\_value} = \mathrm{BZERO} + \mathrm{BSCALE} \times \text {array\_value}.\tag{3}
$$

The value field shall contain a floating-point number representing the coefficient of the linear term in the scaling equation, the ratio of physical value to array value at zero offset. The default value for this keyword is 1.0. Before support for IEEE floatingpoint data types was added to FITS (Wells & Grosbøl 1990), this technique of linearly scaling integer values was the only way to represent the full range of floating-point values in a FITS array. This linear scaling technique is still commonly used to reduce the size of the data array by a factor of two by representing 32- bit floating-point physical values as 16-bit scaled integers.

BZERO keyword. This keyword shall be used, along with the BSCALE keyword, to linearly scale the array pixel values (i.e., the actual values stored in the FITS file) to transform them into the physical values that they represent using Eq. 3. The value field shall contain a floating-point number representing the physical value corresponding to an array value of zero. The default value for this keyword is 0.0.

Besides its use in representing floating-point values as scaled integers (see the description of the BSCALE keyword), the BZERO keyword is also used when storing unsigned-integer values in the FITS array. In this special case the BSCALE keyword shall have

the default value of 1.0, and the BZERO keyword shall have one of the integer values shown in Table 11.

Since the FITS format does not support a native unsigned integer data type (except for the unsigned eight-bit byte data type), the unsigned values are stored in the FITS array as native signed integers with the appropriate integer offset specified by the BZERO keyword value shown in the table. For the byte data type, the converse technique can be used to store signed byte values as native unsigned values with the negative BZERO offset. In each case, the physical value is computed by adding the offset specified by the BZERO keyword to the native data type value that is stored in the FITS file.<sup>9</sup>

BUNIT keyword. The value field shall contain a character string describing the physical units in which the quantities in the array, after application of BSCALE and BZERO, are expressed. These units must follow the prescriptions of Sect. 4.3.

BLANK keyword. This keyword shall be used only in headers with positive values of BITPIX (i.e., in arrays with integer data). Bytes 1 through 8 contain the string \`BLANK ' (ASCII spaces in Bytes 6 through 8). The value field shall contain an integer that specifies the value that is used within the integer array to represent pixels that have an undefined physical value.

If the BSCALE and BZERO keywords do not have the default values of 1.0 and 0.0, respectively, then the value of the BLANK keyword must equal the actual value in the FITS data array that is used to represent an undefined pixel and not the corresponding physical value (computed from Eq. 3). To cite a specific, common example, unsigned 16-bit integers are represented in a signed integer FITS array (with BITPIX = 16) by setting BZERO = 32768 and BSCALE = 1. If it is desired to use pixels that have an unsigned value (i.e., the physical value) equal to 0 to represent undefined pixels in the array, then the BLANK keyword must be set to the value -32768 because that is the actual value of the undefined pixels in the FITS array.

DATAMAX keyword. The value field shall always contain a floating-point number, regardless of the value of BITPIX. This number shall give the maximum valid physical value represented by the array (from Eq. 3), exclusive of any IEEE special values.

DATAMIN keyword. The value field shall always contain a floating-point number, regardless of the value of BITPIX. This number shall give the minimum valid physical value represented by the array (from Eq. 3), exclusive of any IEEE special values.

WCS keywords. An extensive set of keywords have been defined to describe the world coordinates associated with an array. These keywords are discussed separately in Sect. 8.

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">9 A more computationally efficient method of adding or subtracting the BZERO values is to simply flip the most-significant bit of the binary value. For example, using eight-bit integers, the decimal value 248 minus the BZERO value of 128 equals 120. The binary representation of 248 is 11111000. Flipping the most-significant bit gives the binary value 01111000, which is equal to decimal 120.</span></small>

14

<!-- page 21 of 75 -->

Table 11: Usage of BZERO to represent non-default integer data types.

<table><tr><td>BITPIX</td><td>Native data type</td><td>Physical data type</td><td colspan="2">BZERO</td></tr><tr><td>8</td><td>unsigned</td><td>signed byte</td><td>-128</td><td> $(-2^7)$ </td></tr><tr><td>16</td><td>signed</td><td>unsigned 16-bit</td><td>32768</td><td> $(2^{15})$ </td></tr><tr><td>32</td><td>signed</td><td>unsigned 32-bit</td><td>2147483648</td><td> $(2^{31})$ </td></tr><tr><td>64</td><td>signed</td><td>unsigned 64-bit</td><td>9223372036854775808</td><td> $(2^{63})$ </td></tr></table>

## 4.4.2.6. Extension keywords

The next three keywords were originally defined for use within the header of a conforming extension, however they also may appear in the primary header with an analogous meaning. If these keywords are present, it is recommended that they have a unique combination of values in each HDU of the FITS file.

EXTNAME keyword. The value field shall contain a character string to be used to distinguish among different extensions of the same type, i.e., with the same value of XTENSION, in a FITS file. Within this context, the primary array should be considered as equivalent to an IMAGE extension.

EXTVER keyword. The value field shall contain an integer to be used to distinguish among different extensions in a FITS file with the same type and name, i.e., the same values for XTENSION and EXTNAME. The values need not start with 1 for the first extension with a particular value of EXTNAME and need not be in sequence for subsequent values. If the EXTVER keyword is absent, the file should be treated as if the value were 1.

EXTLEVEL keyword. The value field shall contain an integer specifying the level in a hierarchy of extension levels of the extension header containing it. The value shall be 1 for the highest level; levels with a higher value of this keyword shall be subordinate to levels with a lower value. If the EXTLEVEL keyword is absent, the file should be treated as if the value were 1.

The following keyword is optional, but is reserved for use by the convention described in Appendix K. If present it shall appear in the extension header immediately after the mandatory keywords, and be used as described in the appendix.

INHERIT keyword. The value field shall contain a logical value of T or F to indicate whether or not the current extension should inherit the keywords in the primary header of the FITS file.

## 4.4.2.7 Data-integrity keywords

The two keywords described here provide an integrity check on the information contained in FITS HDUs.

DATASUM keyword. The value field of the DATASUM keyword shall consist of a character string that should contain the unsigned-integer value of the 32-bit ones’ complement checksum of the data records in the HDU (i.e., excluding the header

records). For this purpose, each 2880-byte FITS logical record should be interpreted as consisting of 720 32-bit unsigned integers. The four bytes in each integer must be interpreted in order of decreasing significance where the most-significant byte is first, and the least-significant byte is last. Accumulate the sum of these integers using ones’ complement arithmetic in which any overflow of the most-significant bit is propagated back into the least-significant bit of the sum.

The DATASUM value is expressed as a character string (i.e., enclosed in single-quote characters) because support for the full range of 32-bit unsigned-integer keyword values is problematic in some software systems. This string may be padded with non-significant leading or trailing blank characters or leading zeros. A string containing only one or more consecutive ASCII blanks may be used to represent an undefined or unknown value for the DATASUM keyword. The DATASUM keyword may be omitted in HDUs that have no data records, but it is preferable to include the keyword with a value of 0. Otherwise, a missing DATASUM keyword asserts no knowledge of the checksum of the data records. Recording in the comment field the ISO-8601- formatted Datetime (ISO 2004b) when the value of this keyword record is created or updated is recommended.

CHECKSUM keyword. The value field of the CHECKSUM keyword shall consist of an ASCII character string whose value forces the 32-bit ones’ complement checksum accumulated over the entire FITS HDU to equal negative 0. (Note that ones’s complement arithmetic has both positive and negative zero elements). It is recommended that the particular 16-character string generated by the algorithm described in Appendix J be used. A string containing only one or more consecutive ASCII blanks may be used to represent an undefined or unknown value for the CHECKSUM keyword.

The CHECKSUM keyword value must be expressed in fixed format, when the algorithm in Appendix J is used, otherwise the usage of fixed format is recommended. Recording in the comment field the ISO-8601-formatted Datetime when the value of this keyword record is created or updated is recommended.

If the CHECKSUM keyword exists in the header of the HDU and the accumulated checksum is not equal to −0, or if the DATASUM keyword exists in the header of the HDU and its value does not match the data checksum, then this provides a strong indication that the content of the HDU has changed subsequent to the time that the respective keyword value was computed. Such an invalid checksum may indicate corruption during a prior file copy or transfer operation, or a corruption of the physical media on which the file was stored. It may alternatively reflect an intentional change to the data file by subsequent data processing if the CHECKSUM value was not also updated.

15

<!-- page 22 of 75 -->

Normally both keywords will be present in the header if either is present, but this is not required. These keywords apply only to the HDU in which they are contained. If these keywords are written in one HDU of a multi-HDU FITS file then it is strongly recommended that they also be written to every other HDU in the file with values appropriate to each HDU in turn; in that case the checksum accumulated over the entire file will equal −0 as well. The DATASUM keyword must be updated before the CHECKSUM keyword. In general updating the two checksum keywords should be the final step of any update to either data or header records in a FITS HDU. It is highly recommended that if a FITS file is intended for public distribution, then the checksum keywords, if present, should contain valid values.

## 4.4.3. Additional keywords

New keywords may be devised in addition to those described in this Standard, so long as they are consistent with the generalized rules for keywords and do not conflict with mandatory or reserved keywords. Any keyword that refers to or depends upon the existence of other specific HDUs in the same or other files should be used with caution because the persistence of those HDUs cannot always be guaranteed.

## 5. Data representation

Primary and extension data shall be represented in one of the formats described in this section. FITS data shall be interpreted to be a byte stream. Bytes are in big-endian order of decreasing significance. The byte that includes the sign bit shall be first, and the byte that has the ones bit shall be last.

## 5.1. Characters

Each character shall be represented by one byte. A character shall be represented by its seven-bit ASCII (ANSI 1977) code in the low-order seven bits in the byte. The high-order bit shall be zero.

## 5.2. Integers

## 5.2.1. Eight-bit

Eight-bit integers shall be unsigned binary integers, contained in one byte with decimal values ranging from 0 to 255.

## 5.2.2. Sixteen-bit

Sixteen-bit integers shall be two’s complement signed binary integers, contained in two bytes with decimal values ranging from −32768 to +32767.

## 5.2.3. Thirty-two-bit

Thirty-two-bit integers shall be two’s complement signed binary integers, contained in four bytes with decimal values ranging from −2147483648 to +2147483647.

## 5.2.4. Sixty-four-bit

Sixty-four-bit integers shall be two’s complement signed binary integers, contained in eight bytes with decimal values ranging from −9223372036854775808 to +9223372036854775807.

## 5.2.5. Unsigned integers

The FITS format does not support a native unsigned integer data type (except for the unsigned 8-bit byte data type) therefore unsigned 16-bit, 32-bit, or 64-bit binary integers cannot be stored directly in a FITS data array. Instead, the appropriate offset must be applied to the unsigned integer to shift the value into the range of the corresponding signed integer, which is then stored in the FITS file. The BZERO keyword shall record the amount of the offset needed to restore the original unsigned value. The BSCALE keyword shall have the default value of 1.0 in this case, and the appropriate BZERO value, as a function of BITPIX, is specified in Table 11.

This same technique must be used when storing unsigned integers in a binary-table column of signed integers (Sect. 7.3.2). In this case the TSCALn keyword (analogous to BSCALE) shall have the default value of 1.0, and the appropriate TZEROn value (analogous to BZERO) is specified in Table 19.

## 5.3. IEEE-754 floating point

Transmission of 32- and 64-bit floating-point data within the FITS format shall use the ANSI/IEEE-754 standard (IEEE 1985). BITPIX = -32 and BITPIX = -64 signify 32- and 64-bit IEEE floating-point numbers, respectively; the absolute value of BITPIX is used for computing the sizes of data structures. The full IEEE set of number forms is allowed for FITS interchange, including all special values.

The BLANK keyword should not be used when BITPIX = -32 or -64; rather, the IEEE NaN should be used to represent an undefined value. Use of the BSCALE and BZERO keywords is not recommended.

Appendix E has additional details on the IEEE format.

## 5.4. Time

There is strictly no such thing as a data type for time valued data, but rules to encode time values are given in Sect. 9 and in more detail in Rots et al. (2015).

## 6. Random-groups structure

The random-groups structure allows a collection of ‘groups’, where a group consists of a subarray of data and a set of associated parameter values, to be stored within the FITS primary data array. Random groups have been used almost exclusively for applications in radio interferometry; outside this field, there is little support for reading or writing data in this format. Other than the existing use for radio interferometry data, the randomgroups structure is deprecated and should not be further used. For other applications, the binary-table extension (Sect. 7.3) provides a more extensible and better documented way of associating groups of data within a single data structure.

16

<!-- page 23 of 75 -->

Table 12: Mandatory keywords in primary header preceding random groups.

```txt
Position Keyword
1 SIMPLE = T
2 BITPIX
3 NAXIS
4 NAXIS1 = 0
5 NAXISn, n = 2, ..., value of NAXIS
    :
    (other keywords, which must include ...)
    GROUPS = T
    PCOUNT
    GCOUNT
    :
last END
```

## 6.1. Keywords

## 6.1.1. Mandatory keywords

The SIMPLE keyword is required to be the first keyword in the primary header of all FITS files, including those with randomgroups records. If the random-groups format records follow the primary header, the keyword records of the primary header must use the keywords defined in Table 12 in the order specified. No other keywords may intervene between the SIMPLE keyword and the last NAXISn keyword.

SIMPLE keyword. The keyword record containing this keyword is structured in the same way as if a primary data array were present (Sect. 4.4.1).

BITPIX keyword. The keyword record containing this keyword is structured as prescribed in Sect. 4.4.1.

NAXIS keyword. The value field shall contain an integer ranging from 1 to 999, representing one more than the number of axes in each data array.

NAXIS1 keyword. The value field shall contain the integer 0, a signature of random-groups format indicating that there is no primary data array.

NAXISn keywords (n = 2, . . . , value of NAXIS). The NAXISn keywords must be present for all values $n   =   2 ,   \ldots ,$ , NAXIS, in increasing order of n, and for no larger values of n. The value field shall contain an integer, representing the number of positions along Axis n − 1 of the data array in each group.

GROUPS keyword. The value field shall contain the logical constant T. The value T associated with this keyword implies that random-groups records are present.

PCOUNT keyword. The value field shall contain an integer equal to the number of parameters preceding each array in a group.

GCOUNT keyword. The value field shall contain an integer equal to the number of random groups present.

END keyword. This keyword has no associated value. Bytes 9 through 80 shall contain ASCII spaces (decimal 32 or hexadecimal 20).

The total number of bits in the random-groups records exclusive of the fill described in Sect. 6.2 is given by the following expression:

$$
\begin{array}{r l} N _ {\text {bits}} = & | \text {BITPIX} | \times \text {GCOUNT} \times \\ & (\text {PCOUNT} + \text {NAXIS2} \times \text {NAXIS3} \times \dots \times \text {NAXISM} m), \end{array}\tag{4}
$$

where $N _ { \mathrm { b i t s } }$ is non-negative and the number of bits excluding fill; m is the value of NAXIS; and BITPIX, GCOUNT, PCOUNT, and the NAXISn represent the values associated with those keywords.

## 6.1.2. Reserved keywords

PTYPEn keywords. The value field shall contain a character string giving the name of Parameter n. If the PTYPEn keywords for more than one value of n have the same associated name in the value field, then the data value for the parameter of that name is to be obtained by adding the derived data values of the corresponding parameters. This rule provides a mechanism by which a random parameter may have more precision than the accompanying data array elements; for example, by summing two 16-bit values with the first scaled relative to the other such that the sum forms a number of up to 32-bit precision.

PSCALn keywords. This keyword shall be used, along with the PZEROn keyword, when the n<sup>th</sup> FITS group parameter value is not the true physical value, to transform the group parameter value to the true physical values it represents, using Eq. 5. The value field shall contain a floating-point number representing the coefficient of the linear term in Eq. 5, the scaling factor between true values and group parameter values at zero offset. The default value for this keyword is 1.0.

PZEROn keywords. This keyword shall be used, along with the PSCALn keyword, when the n<sup>th</sup> FITS group parameter value is not the true physical value, to transform the group parameter value to the physical value. The value field shall contain a floating-point number, representing the true value corresponding to a group parameter value of zero. The default value for this keyword is 0.0. The transformation equation is as follows:

$$
\text {physical\_value} = \mathrm{PZERO} n + \mathrm{PSCAL} n \times \text {group\_param\_value}. \tag {5}
$$

## 6.2. Data sequence

Random-groups data shall consist of a set of groups. The number of groups shall be specified by the GCOUNT keyword in the associated header. Each group shall consist of the number of parameters specified by the PCOUNT keyword followed by an array with the number of elements $N _ { \mathrm { e l e m } }$ given by the following expression:

17

<!-- page 24 of 75 -->

$$
N _ {\mathrm{elem}} = (\text {NAXIS2} \times \text {NAXIS3} \times \dots \times \text {NAXISM}),\tag{6}
$$

where $N _ { \mathrm { e l e m } }$ is the number of elements in the data array in a group, m is the value of NAXIS, and the NAXISn represent the values associated with those keywords.

The first parameter of the first group shall appear in the first location of the first data block. The first element of each array shall immediately follow the last parameter associated with that group. The first parameter of any subsequent group shall immediately follow the last element of the array of the previous group. The arrays shall be organized internally in the same way as an ordinary primary data array. If the groups data do not fill the final data block, the remainder of the block shall be filled with zero values in the same way as a primary data array (Sect. 3.3.2). If random-groups records are present, there shall be no primary data array.

## 6.3. Data representation

Permissible data representations are those listed in Sect. 5. Parameters and elements of associated data arrays shall have the same representation. If more precision is required for an associated parameter than for an element of a data array, the parameter shall be divided into two or more addends, represented by the same value for the PTYPEn keyword. The value shall be the sum of the physical values, which may have been obtained from the group parameter values using the PSCALn and PZEROn keywords.

## 7. Standard extensions

A standard extension is a conforming extension whose organization and content are completely specified in this Standard. The specifications for the three currently defined standard extensions, namely,

1. IMAGE extensions;

2. TABLE ASCII-table extensions; and

3. BINTABLE binary-table extensions

are given in the following sections. A list of other conforming extensions is given in Appendix F.

## 7.1. Image extension

The FITS IMAGE extension is nearly identical in structure to the the primary HDU and is used to store an array of data. Multiple IMAGE extensions can be used to store any number of arrays in a single FITS file. The first keyword record in an IMAGE extension shall be XTENSION= 'IMAGE '.

## 7.1.1. Mandatory keywords

The XTENSION keyword is required to be the first keyword of all IMAGE extensions. The keyword records in the header of an image extension must use the keywords defined in Table 13 in the order specified. No other keywords may intervene between the XTENSION and GCOUNT keywords.

XTENSION keyword. The value field shall contain the character string 'IMAGE '.

Table 13: Mandatory keywords in IMAGE extensions.

| Position | Keyword |
| --- | --- |
| 1 | XTENSION=_'IMAGE_'&lt; |
| 2 | BITPIX |
| 3 | NAXIS |
| 4 | NAXISn, n = 1, ..., NAXIS |
| 5 | PCOUNT = 0 |
| 6 | GCOUNT = 1 |
|  | ⋮ |
|  | (other keywords ...) |
|  | ⋮ |
| last | END |

BITPIX keyword. The value field shall contain an integer. The absolute value is used in computing the sizes of data structures. It shall specify the number of bits that represent a data value. The only valid values of BITPIX are given in Table 8. Writers of IMAGE extensions should select a BITPIX data type appropriate to the form, range of values, and accuracy of the data in the array.

NAXIS keyword. The value field shall contain a non-negative integer no greater than 999, representing the number of axes in the associated data array. If the value is zero then the IMAGE extension shall not have any data blocks following the header.

NAXISn keywords. The NAXISn keywords must be present for all values n = 1, . . . , NAXIS, in increasing order of n, and for no other values of n. The value field of this indexed keyword shall contain a non-negative integer, representing the number of elements along Axis n of a data array. If the value of any of the NAXISn keywords is zero, then the IMAGE extension shall not have any data blocks following the header. If NAXIS is equal to 0 there should not be any NAXISn keywords.

PCOUNT keyword. The value field shall contain the integer 0.

GCOUNT keyword. The value field shall contain the integer 1; each IMAGE extension contains a single array.

END keyword. This keyword has no associated value. Bytes 9 through 80 shall be filled with ASCII spaces (decimal 32 or hexadecimal 20).

## 7.1.2. Other reserved keywords

The reserved keywords defined in Sect. 4.4.2 (except for EXTEND and BLOCKED) may appear in an image-extension header. The keywords must be used as defined in that section.

## 7.1.3. Data sequence

The data format shall be identical to that of a primary data array as described in Sect. 3.3.2.

18

<!-- page 25 of 75 -->

Table 14: Mandatory keywords in ASCII-table extensions.

```txt
Position Keyword
XTENSION=_'TABLE'\n2 BITPIX = 8
NAXIS = 2
NAXIS1
NAXIS2
PCOUNT = 0
GCOUNT = 1
TFIELDS
⋮
(other keywords, including (if TFIELDS is not zero) ...)
TTYPEn, n = 1, 2, ..., k, where k is the value of TFIELDS (recommended)
TBCOLn, n = 1, 2, ..., k, where k is the value of TFIELDS (required)
TFORMn, n = 1, 2, ..., k, where k is the value of TFIELDS (required)
⋮
last END
```

## 7.2. The ASCIl-table extension

The ASCII-table extension provides a means of storing catalogs and tables of astronomical data in FITS format. Each row of the table consists of a fixed-length sequence of ASCII characters divided into fields that correspond to the columns in the table. The first keyword record in an ASCII-table extension shall be $\mathrm{XTENSION}=\mathrm{\mu^{'}TABLE}_{\mathrm{\mu}\mathrm{\mu}}$

## 7.2.1. Mandatory keywords

The header of an ASCII-table extension must use the keywords defined in Table 14. The first keyword must be XTENSION; the seven keywords following XTENSION (BITPIX . . . TFIELDS) must be in the order specified with no intervening keywords.

XTENSION keyword. The value field shall contain the character string $\mathrm{TABLE}_{\mathrm{山山山}}$

BITPIX keyword. The value field shall contain the integer 8, denoting that the array contains ASCII characters.

NAXIS keyword. The value field shall contain the integer 2, denoting that the included data array is two-dimensional: rows and columns.

NAXIS1 keyword. The value field shall contain a non-negative integer, giving the number of ASCII characters in each row of the table. This includes all the characters in the defined fields plus any characters that are not included in any field.

NAXIS2 keyword. The value field shall contain a non-negative integer, giving the number of rows in the table.

PCOUNT keyword. The value field shall contain the integer 0.

GCOUNT keyword. The value field shall contain the integer 1; the data blocks contain a single table.

Table 15: Valid TFORMn format values in TABLE extensions.

| Field value | Data type |
| --- | --- |
| Aw | Character |
| Iw | Decimal integer |
| Fw.d | Floating-point, fixed decimal notation |
| Ew.d | Floating-point, exponential notation |
| Dw.d | Floating-point, exponential notation |

**Notes.** w is the width in characters of the field and d is the number of digits to the right of the decimal.

TFIELDS keyword. The value field shall contain a non-negative integer representing the number of fields in each row. The maximum permissible value is 999.

TBCOLn keywords. The TBCOLn keywords must be present for all values n = 1, . . . , TFIELDS and for no other values of n. The value field of this indexed keyword shall contain an integer specifying the column in which Field n starts. The first column of a row is numbered 1.

TFORMn keywords. The TFORMn keywords must be present for all values n = 1, . . . , TFIELDS and for no other values of n. The value field of this indexed keyword shall contain a character string describing the format in which Field n is encoded. Only the formats in Table 15, interpreted as Fortran (ISO 2004) input formats and discussed in more detail in Sect. 7.2.5, are permitted for encoding. Format codes must be specified in upper case. Other format editing codes common to Fortran such as repetition, positional editing, scaling, and field termination are not permitted. All values in numeric fields have a number base of ten (i.e., they are decimal); binary, octal, hexadecimal, and other representations are not permitted. The TDISPn keyword, defined in Sect. 7.2.2, may be used to recommend that a decimal integer value in an ASCII table be displayed as the equivalent binary, octal, or hexadecimal value.

19

<!-- page 26 of 75 -->

Table 16: Valid TDISPn format values in TABLE extensions.

| Field value | Data type |
| --- | --- |
| Aw | Character |
| Iw.m | Integer |
| Bw.m | Binary, integers only |
| Ow.m | Octal, integers only |
| Zw.m | Hexadecimal, integers only |
| Fw.d | Floating-point, fixed decimal notation |
| Ew.dEe | Floating-point, exponential notation |
| ENw.d | Engineering; E format with exponent multiple of three |
| ESw.d | Scientific; same as EN but non-zero leading digit if not zero |
| Gw.dEe | General; appears as F if significance not lost, else E. |
| Dw.dEe | Floating-point, exponential notation |

Notes. w is the width in characters of displayed values, m is the minimum number of digits displayed, d is the number of digits to right of decimal, and e is number of digits in exponent. The .m and Ee fields are optional.

END keyword. This keyword has no associated value. Bytes 9 through 80 shall contain ASCII spaces (decimal 32 or hexadecimal 20).

## 7.2.2. Other reserved keywords

In addition to the reserved keywords defined in Sect. 4.4.2 (except for EXTEND and BLOCKED), the following other reserved keywords may be used to describe the structure of an ASCII-table data array. They are optional, but if they appear within an ASCII-table extension header, they must be used as defined in this section of this Standard.

TTYPEn keywords. The value field for this indexed keyword shall contain a character string giving the name of Field n. It is strongly recommended that every field of the table be assigned a unique, case-insensitive name with this keyword, and it is recommended that the character string be composed only of upper- and lower-case letters, digits, and the underscore (’ ’, decimal 95, hexadecimal 5F) character. Use of other characters is not recommended because it may be difficult to map the column names into variables in some languages (e.g., any hyphens, ’\*’ or ’+’ characters in the name may be confused with mathematical operators). String comparisons with the TTYPEn keyword values should not be case sensitive (e.g., ’TIME’ and ’Time’ should be interpreted as the same name).

TUNITn keywords. The value field shall contain a character string describing the physical units in which the quantity in Field n, after any application of TSCALn and TZEROn, is expressed. Units must follow the prescriptions in Sect. 4.3.

TSCALn keywords. This indexed keyword shall be used, along with the TZEROn keyword, to linearly scale the values in the table Field n to transform them into the physical values that they represent using Eq. 7. The value field shall contain a floatingpoint number representing the coefficient of the linear term in the scaling equation. The default value for this keyword is 1.0. This keyword must not be used for A-format fields.

The transformation equation used to compute a true physical value from the quantity in Field n is

$$
\text {physical\_value} = \mathrm{TZEROn} + \mathrm{TSCALn} \times \text {field\_value}\tag{7}
$$

where field value is the value that is actually stored in that table field in the FITS file.

TZEROn keywords. This indexed keyword shall be used, along with the TSCALn keyword, to linearly scale the values in the table Field n to transform them into the physical values that they represent using Eq. 7. The value field shall contain a floating-point number representing the physical value corresponding to an array value of zero. The default value for this keyword is 0.0. This keyword must not be used for A-format fields.

TNULLn keywords. The value field for this indexed keyword shall contain the character string that represents an undefined value for Field n. The string is implicitly space filled to the width of the field.

TDISPn keywords. The value field of this indexed keyword shall contain a character string describing the format recommended for displaying an ASCII-text representation of of the contents of Field n. This keyword overrides the default display format given by the TFORMn keyword. If the table value has been scaled, the physical value, derived using Eq. 7, shall be displayed. All elements in a field shall be displayed with a single, repeated format. Only the format codes in Table 16, interpreted as Fortran (ISO 2004) output formats, and discussed in more detail in Sect. 7.3.4, are permitted for encoding. The format codes must be specified in upper case. If the Bw.m, Ow.m, and Zw.m formats are not readily available to the reader, the Iw.m display format may be used instead, and if the ENw.d and ESw.d formats are not available, Ew.d may be used.

The following four keywords may be used to specify minimum and maximum values in numerical columns of a FITS ASCII or binary table. These keywords must have the same data type as the physical values in the associated column (either an integer or a floating-point number). Any undefined elements in the column shall be excluded when determining the value of these keywords.

TDMINn keywords. The value field shall contain a number giving the minimum physical value contained in Column n of the table. This keyword is analogous to the DATAMIN keyword that is defined for arrays in Sect. 4.4.2.5.

20

<!-- page 27 of 75 -->

TDMAXn keywords. The value field shall contain a number giving the maximum physical value contained in Column n of the table. This keyword is analogous to the DATAMAX keyword that is defined for arrays in Sect. 4.4.2.5.

TLMINn keywords. The value field shall contain a number that specifies the minimum physical value in Column n that has a valid meaning or interpretation. The column is not required to actually contain any elements that have this value, and the column may contain elements with physical values less than TLMINn, however, the interpretation of any such out-of-range column elements is not defined.

TLMAXn keywords. The value field shall contain a number that specifies the maximum physical value in Column n that has a valid meaning or interpretation. The column is not required to actually contain any elements that have this value, and the column may contain elements with physical values greater than TLMAXn, however, the interpretation of any such out-of-range column elements is not defined.

The TLMINn and TLMAXn keywords are commonly used when constructing histograms of the data values in a column. For example, if a table contains columns that give the X and Y pixel location of a list of photons that were detected by a photoncounting device, then the TLMINn and TLMAXn keywords could be used respectively to specify the minimum and maximum values that the detector is capable of assigning to the X and Y columns.

## 7.2.3. Data sequence

The table is constructed from a two-dimensional array of ASCII characters. The row length and the number of rows shall be those specified, respectively, by the NAXIS1 and NAXIS2 keywords of the associated header. The number of characters in a row and the number of rows in the table shall determine the size of the character array. Every row in the array shall have the same number of characters. The first character of the first row shall be at the start of the data block immediately following the last header block. The first character of subsequent rows shall follow immediately the character at the end of the previous row, independent of the FITS block structure. The positions in the last data block after the last character of the last row of the table shall be filled with ASCII spaces.

## 7.2.4. Fields

Each row in the array shall consist of a sequence of from 0 to 999 fields, as specified by the TFIELDS keyword, with one entry in each field. For every field, the Fortran (ISO 2004) format of the information contained (given by the TFORMn keyword), the location in the row of the beginning of the field (given by the TBCOLn keyword), and (optionally, but strongly recommended) the field name (given by the TTYPEn keyword), shall be specified in the associated header. The location and format of fields shall be the same for every row. Fields may overlap, but this usage is not recommended. Only a limited set of ASCII character values may appear within any field, depending on the field type as specified below. There may be characters in a table row that

are not included in any field, (e.g., between fields, or before the first field or after the last field). Any seven-bit ASCII character may occur in characters of a table row that are not included in a defined field. A common convention is to include a space character between each field for added legibility if the table row is displayed verbatim. It is also permissible to add control characters, such as a carriage return or line-feed character, following the last field in each row as a way of formatting the table if it is printed or displayed by a text-editing program.

## 7.2.5. Entries

All data in an ASCII-table extension field shall be ASCII text in a format that conforms to the rules for fixed field input in Fortran (ISO 2004) format, as described below. The only possible formats shall be those specified in Table 15. If values of −0 and +0 need to be distinguished, then the sign character should appear in a separate field in character format. TNULLn keywords may be used to specify a character string that represents an undefined value in each field. The characters representing an undefined value may differ from field to field but must be the same within a field. Writers of ASCII tables should select a format for each field that is appropriate to the form, range of values, and accuracy of the data in that field. This Standard does not impose an upper limit on the number of digits of precision, nor any limit on the range of numeric values. Software packages that read or write data according to this Standard could be limited, however, in the range of values and exponents that are supported (e.g., to the range that can be represented by 32-bit or 64-bit binary numbers).

The value of each entry shall be interpreted as described in the following paragraphs.

Character fields. The value of a character-formatted (Aw) field is a character string of width w containing the characters in columns TBCOLn through TBCOLn + w − 1. The character string shall be composed of the restricted set of ASCII-text characters with decimal values in the range 32 through 126 (hexadecimal 20 through 7E).

Integer fields. The value of an integer-formatted (Iw) field is a signed decimal integer contained in Columns TBCOLn through TBCOLn + w − 1 consisting of a single optional sign $( + , , , , , )$ followed by one or more decimal digits (’0’ through ’9’). Non-significant space characters may precede and/or follow the integer value within the field. A blank field has value 0. All characters other than leading and trailing spaces, a contiguous string of decimal digits, and a single leading sign character are forbidden.

Real fields. The value of a real-formatted field (Fw.d, Ew.d, Dw.d) is a real number determined from the w characters from Columns TBCOLn through TBCOLn + w − 1. The value is formed by

1. discarding any trailing space characters in the field and rightjustifying the remaining characters,

2. interpreting the first non-space characters as a numeric string consisting of a single optional sign $( + \mathrm { ~ o r ~ } ^ { \prime } - )$ followed by one or more decimal digits $( \cdot 0 ^ { \cdot } )$ through ’9’) optionally containing a single decimal point $( \cdot )$ . The numeric string

21

<!-- page 28 of 75 -->

is terminated by the end of the right-justified field or by the occurrence of any character other than a decimal point (’.’) and the decimal integers (’0’ through ’9’). If the string contains no explicit decimal point, then the implicit decimal point is taken as immediately preceding the rightmost d digits of the string, with leading zeros assumed if necessary. The use of implicit decimal points is deprecated and is strongly discouraged because of the possibility that FITS-reading programs will misinterpret the data value. Therefore, real-formatted fields should always contain an explicit decimal point.

3. If the numeric string is terminated by a

(a) $\text{" }+ \text{" } \text{ OT } \text{" }- \text{" }$ , interpreting the following string as an exponent in the form of a signed decimal integer, or

(b) $\mathrm{E}', \mathrm{or}' \mathrm{D}'$ , interpreting the following string as an exponent of the form E or D followed by an optionally signed decimal integer constant.

4. The exponent string, if present, is terminated by the end of the right-justified string.

5. Characters other than those specified above, including embedded space characters, are forbidden.

The numeric value of the table field is then the value of the numeric string multiplied by ten (10) to the power of the exponent string, i.e., value = numeric string × 10(exponent string). The default exponent is zero and a blank field has value zero. There is no difference between the F, D, and E formats; the content of the string determines its interpretation. Numbers requiring more precision and/or range than the local computer can support may be represented. It is good form to specify a D format in TFORMn for a column of an ASCII table when that column will contain numbers that cannot be accurately represented in 32-bit IEEE binary format (see Appendix E).

## 7.3. Binary-table extension

The binary-table extension is similar to the ASCII table in that it provides a means of storing catalogs and tables of astronomical data in FITS format, however, it offers more features and provides more-efficient data storage than ASCII tables. The numerical values in binary tables are stored in more-compact binary formats rather than coded into ASCII, and each field of a binary table can contain an array of values rather than a simple scalar as in ASCII tables. The first keyword record in a binary-table extension shall be XTENSION= 'BINTABLE'.

## 7.3.1. Mandatory keywords

The XTENSION keyword is the first keyword of all binarytable extensions. The seven keywords following (BITPIX. . . TFIELDS) must be in the order specified in Table 17, with no intervening keywords.

XTENSION keyword. The value field shall contain the character string 'BINTABLE'.

BITPIX keyword. The value field shall contain the integer 8, denoting that the array is an array of eight-bit bytes.

NAXIS keyword. The value field shall contain the integer 2, denoting that the included data array is two-dimensional: rows and columns.

NAXIS1 keyword. The value field shall contain a non-negative integer, giving the number of eight-bit bytes in each row of the table.

NAXIS2 keyword. The value field shall contain a non-negative integer, giving the number of rows in the table.

PCOUNT keyword. The value field shall contain the number of bytes that follow the table in the supplemental data area called the heap.

GCOUNT keyword. The value field shall contain the integer 1; the data blocks contain a single table.

TFIELDS keyword. The value field shall contain a non-negative integer representing the number of fields in each row. The maximum permissible value is 999.

TFORMn keywords. The TFORMn keywords must be present for all values $n \; = \; 1 , \ldots ,$ TFIELDS and for no other values of n. The value field of this indexed keyword shall contain a character string of the form rTa. The repeat count r is the ASCII representation of a non-negative integer specifying the number of elements in Field n. The default value of r is 1; the repeat count need not be present if it has the default value. A zero element count, indicating an empty field, is permitted. The data type T specifies the data type of the contents of Field n. Only the data types in Table 18 are permitted. The format codes must be specified in upper case. For fields of type P or Q, the only permitted repeat counts are 0 and 1. The additional characters a are optional and are not further defined in this Standard. Table 18 lists the number of bytes each data type occupies in a table row. The first field of a row is numbered 1. The total number of bytes $n _ { \mathrm { { r o w } } }$ in a table row is given by

$$
n _ {\text {row}} = \sum_ {i = 1} ^ {\text {TFIELDS}} r _ {i} b _ {i}\tag{8}
$$

where $r _ { i }$ is the repeat count for Field $i , b _ { i }$ is the number of bytes for the data type in Field $i ,$ and TFIELDS is the value of that keyword, must equal the value of NAXIS1.

END keyword. This keyword has no associated value. Bytes 9 through 80 shall contain ASCII spaces (decimal 32 or hexadecimal 20).

## 7.3.2. Other reserved keywords

In addition to the reserved keywords defined in Sect. 4.4.2 (except for EXTEND and BLOCKED), the following other reserved keywords may be used to describe the structure of a binary-table

22

<!-- page 29 of 75 -->

Table 17: Mandatory keywords in binary-table extensions.

| Position | Keyword |
| --- | --- |
| 1 | XTENSION=,$'BINTABLE'$ |
| 2 | BITPIX = 8 |
| 3 | NAXIS = 2 |
| 4 | NAXIS1 |
| 5 | NAXIS2 |
| 6 | PCOUNT |
| 7 | GCOUNT = 1 |
| 8 | TFIELDS |
|  | $\vdots$(other keywords, including (if TFIELDS is not zero) ...) |
|  | TTYPEn, n = 1, 2, ..., k, where k is the value of TFIELDS (recommended) |
|  | TFORMn, n = 1, 2, ..., k, where k is the value of TFIELDS (required) |
|  | $\vdots$ |
| last | END |

Table 18: Valid TFORMn data types in BINTABLE extensions.

| TFORMn value | Description | Eight-bit Bytes |
| --- | --- | --- |
| 'L' | Logical | 1 |
| 'X' | Bit | † |
| 'B' | Unsigned byte | 1 |
| 'I' | 16-bit integer | 2 |
| 'J' | 32-bit integer | 4 |
| 'K' | 64-bit integer | 8 |
| 'A' | Character | 1 |
| 'E' | Single-precision floating point | 4 |
| 'D' | Double-precision floating point | 8 |
| 'C' | Single-precision complex | 8 |
| 'M' | Double-precision complex | 16 |
| 'P' | Array Descriptor (32-bit) | 8 |
| 'Q' | Array Descriptor (64-bit) | 16 |

Notes. (†) Number of eight-bit bytes needed to contain all bits.

data array. They are optional, but if they appear within a binarytable extension header, they must be used as defined in this section of this Standard.

TTYPEn keywords. The value field for this indexed keyword shall contain a character string giving the name of Field n. It is strongly recommended that every field of the table be assigned a unique, case-insensitive name with this keyword, and it is recommended that the character string be composed only of upper- and lower-case letters, digits, and the underscore (’ ’, decimal 95, hexadecimal 5F) character. Use of other characters is not recommended because it may be difficult to map the column names into variables in some languages (e.g., any hyphens, ’\*’ or ’+’ characters in the name may be confused with mathematical operators). String comparisons with the TTYPEn keyword values should not be case sensitive (e.g., ’TIME’ and ’Time’ should be interpreted as the same name).

TUNITn keywords. The value field shall contain a character string describing the physical units in which the quantity in Field n, after any application of TSCALn and TZEROn, is expressed. Units must follow the prescriptions in Sect. 4.3.

TSCALn keywords. This indexed keyword shall be used, along with the TZEROn keyword, to linearly scale the values in the table Field n to transform them into the physical values that they represent using Eq. 7. It must not be used if the format of Field n $\mathrm{is}^{\mathrm{T}} \mathrm{A}^{\mathrm{r}}, \mathrm{L}^{\mathrm{r}}, \mathrm{or}^{\mathrm{r}} \mathrm{x}^{\mathrm{r}}$ . For fields with all other data types, the value field shall contain a floating-point number representing the co-efficient of the linear term in Eq. 7, which is used to compute the true physical value of the field, or, in the case of the complex data types $\cdot _ { C ^ { \prime } }$ and $\text{" } \Pi  \text{" }$ , of the real part of the field, with the imaginary part of the scaling factor set to zero. The default value for this keyword is 1.0. For fields of type ’P’ or ’Q’, the values of TSCALn and TZEROn are to be applied to the values in the data array in the heap area, not the values of the array descriptor (see Sect. 7.3.5).

TZEROn keywords. This indexed keyword shall be used, along with the TSCALn keyword, to linearly scale the values in the table Field n to transform them into the physical values that they represent using Eq. 7. It must not be used if the format of Field n $\mathrm{is}^{\prime}, \mathrm{A}^{\prime}, \mathrm{L}^{\prime}, \mathrm{or}^{\prime} \mathrm{x}^{\prime}$ . For fields with all other data types, the value field shall contain a floating-point number representing the true physical value corresponding to a value of zero in Field n of the FITS file, or, in the case of the complex data types ${ } ^ { \prime } C ^ { \prime }$ and $`` M_{z}$ in the real part of the field, with the imaginary part set to zero. The default value for this keyword is 0.0. Equation 7 is used to compute a true physical value from the quantity in Field n. For fields of type ’P’ or ’Q’, the values of TSCALn and TZEROn are to be applied to the values in the data array in the heap area, not the values of the array descriptor (see Sect. 7.3.5).

In addition to its use in representing floating-point values as scaled integers, the TZEROn keyword is also used when storing unsigned integer values in the field. In this special case the TSCALn keyword shall have the default value of 1.0 and the TZEROn keyword shall have one of the integer values shown in Table 19.

Since the binary-table format does not support a native unsigned integer data type (except for the unsigned eight-bit ${ \bf \Psi ^ { \prime } B } ^ { \prime }$ column type), the unsigned values are stored in the field as native signed integers with the appropriate integer offset specified by the TZEROn keyword value shown in the table. For the byte column type, the converse technique can be used to store signed byte values as native unsigned values with the negative TZEROn

23

<!-- page 30 of 75 -->

Table 19: Usage of TZEROn to represent non-default integer data types.

<table><tr><td>TFORMn</td><td>Native data type</td><td>Physical data type</td><td colspan="2">TZEROn</td></tr><tr><td>&#x27;B&#x27;</td><td>unsigned</td><td>signed byte</td><td>-128</td><td>(-27)</td></tr><tr><td>&#x27;I&#x27;</td><td>signed</td><td>unsigned 16-bit</td><td>32768</td><td>(215)</td></tr><tr><td>&#x27;J&#x27;</td><td>signed</td><td>unsigned 32-bit</td><td>2147483648</td><td>(231)</td></tr><tr><td>&#x27;K&#x27;</td><td>signed</td><td>unsigned 64-bit</td><td>9223372036854775808</td><td>(263)</td></tr></table>

NAXIS2. This keyword shall not be used if the value of PCOUNT is 0. The use of this keyword is described in in Sect. 7.3.5.

offset. In each case, the physical value is computed by adding the offset specified by the TZEROn keyword to the native data type value that is stored in the table field.

TNULLn keywords. The value field for this indexed keyword shall contain the integer that represents an undefined value for Field n of Data Type B, I, J or K, or P or Q array-descriptor fields (Sect. 7.3.5) that point to B, I, J, or K integer arrays. The keyword must not be used if Field n is of any other data type. The value of this keyword corresponds to the table column values before applying any transformation indicated by the TSCALn and TZEROn keywords.

If the TSCALn and TZEROn keywords do not have the default values of 1.0 and 0.0, respectively, then the value of the TNULLn keyword must equal the actual value in the FITS file that is used to represent an undefined element and not the corresponding physical value (computed from Eq. 7). To cite a specific, common example, unsigned 16-bit integers are represented in a signed integer column (with $\mathrm{TFORMn} = \mathrm{~I}$ by setting $\mathrm{TZER0}_{n} = 32768$ and $\mathtt { T S C A L } n = 1$ If it is desired to use elements that have an unsigned value (i.e., the physical value) equal to 0 to represent undefined elements in the field, then the TNULLn keyword must be set to the value -32768 because that is the actual value stored in the FITS file for those elements in the field.

TDISPn keywords. The value field of this indexed keyword shall contain a character string describing the format recommended for displaying an ASCII-text representation of the contents of Field n. If the table value has been scaled, the physical value, derived using Eq. 7, shall be displayed. All elements in a field shall be displayed with a single, repeated format. For purposes of display, each byte of bit (Type X) and byte (Type B) arrays is treated as an unsigned integer. Arrays of Type A may be terminated with a zero byte. Only the format codes in Table 20, interpreted as Fortran (ISO 2004) output formats, and discussed in more detail in Sect. 7.3.4, are permitted for encoding. The format codes must be specified in upper case. If the Bw.m, Ow.m, and Zw.m formats are not readily available to the reader, the Iw.m display format may be used instead, and if the ENw.d and ESw.d formats are not available, Ew.d may be used. In the case of fields of Type P or Q, the TDISPn value applies to the data array pointed to by the array descriptor (Sect. 7.3.5), not the values in the array descriptor itself.

THEAP keyword. The value field of this keyword shall contain an integer providing the separation, in bytes, between the start of the main data table and the start of a supplemental data area called the heap. The default value, which is also the minimum allowed value, shall be the product of the values of NAXIS1 and

TDIMn keywords. The value field of this indexed keyword shall contain a character string describing how to interpret the contents of Field n as a multi-dimensional array with a format of $(l,m,n\ldots)$ , where $l , m , n , \ldots \mathrm { a r e }$ the dimensions of the array. The data are ordered such that the array index of the first dimension given (l) is the most rapidly varying, and that of the last dimension given is the least rapidly varying. The total number of elements in the array equals the product of the dimensions specified in the TDIMn keyword. The size must be less than or equal to the repeat count in the TFORMn keyword, or, in the case of columns that have a ’P’ or ’Q’ TFORMn data type, less than or equal to the array length specified in the variable-length array descriptor (see Sect. 7.3.5). In the special case where the variablelength array descriptor has a size of zero, then the TDIMn keyword is not applicable. If the number of elements in the array implied by the TDIMn is fewer than the allocated size of the array in the FITS file, then the unused trailing elements should be interpreted as containing undefined fill values.

A character string is represented in a binary table by a onedimensional character array, as described under ‘Character’ in the list of data types in Sect. 7.3.3. For example, a Fortran CHARACTER\*20 variable could be represented in a binary table as a character array declared as $\mathrm{TFORM} = 20\mathrm{A}$ . Arrays of strings, i.e., multi-dimensional character arrays, may be represented using the TDIMn notation. For example, i $\mathrm{TFORIn}=60\mathrm{A}$ and $\mathrm{TDINn} = (5,4,3)$ , then the entry consists of a 4 × 3 array of strings each comprising five characters.

The following four keywords may be used to specify minimum and maximum values in numerical columns of a FITS ASCII or binary table. These keywords must have the same data type as the physical values in the associated column (either an integer or a floating-point number). Any undefined elements in the column or any other IEEE special values in the case of floating-point columns shall be excluded when determining the value of these keywords.

TDMINn keywords. The value field shall contain a number giving the minimum physical value contained in Column n of the table. This keyword is analogous to the DATAMIN keyword that is defined for arrays in Sect. 4.4.2.5.

TDMAXn keywords. The value field shall contain a number giving the maximum physical value contained in Column n of the table. This keyword is analogous to the DATAMAX keyword that is defined for arrays in Sect. 4.4.2.5.

24

<!-- page 31 of 75 -->

Table 20: Valid TDISPn format values in BINTABLE extensions.

| Field Value | Data type |
| --- | --- |
| Aw | Character |
| Lw | Logical |
| Iw.m | Integer |
| Bw.m | Binary, integers only |
| Ow.m | Octal, integers only |
| Zw.m | Hexadecimal, integers only |
| Fw.d | Floating-point, fixed decimal notation |
| Ew.dEe | Floating-point, exponential notation |
| ENw.d | Engineering; E format with exponent multiple of three |
| ESw.d | Scientific; same as EN but non-zero leading digit if not zero |
| Gw.dEe | General; appears as F if significance not lost, else E. |
| Dw.dEe | Floating-point, exponential notation |

**Notes.** w is the width in characters of displayed values, m is the minimum number of digits displayed, d is the number of digits to right of decimal, and e is number of digits in exponent. The .m and Ee fields are optional.

TLMINn keywords. The value field shall contain a number that specifies the minimum physical value in Column n that has a valid meaning or interpretation. The column is not required to actually contain any elements that have this value, and the column may contain elements with physical values less than TLMINn, however, the interpretation of any such out-of-range column elements is not defined.

TLMAXn keywords. The value field shall contain a number that specifies the maximum physical value in Column n that has a valid meaning or interpretation. The column is not required to actually contain any elements that have this value, and the column may contain elements with physical values greater than TLMAXn, however, the interpretation of any such out-of-range column elements is not defined.

The TLMINn and TLMAXn keywords are commonly used when constructing histograms of the data values in a column. For example, if a table contains columns that give the X and Y pixel location of a list of photons that were detected by a photoncounting device, then the TLMINn and TLMAXn keywords could be used respectively to specify the minimum and maximum values that the detector is capable of assigning to the X and Y columns.

## 7.3.3. Data sequence

The data in a binary-table extension shall consist of a main data table, which may, but need not, be followed by additional bytes in the supplemental data area. The positions in the last data block after the last additional byte, or, if there are no additional bytes, the last character of the last row of the main data table, shall be filled by setting all bits to zero.

## 7.3.3.1. Main data table

The table is constructed from a two-dimensional byte array. The number of bytes in a row shall be specified by the value of the NAXIS1 keyword and the number of rows shall be specified by the NAXIS2 keyword of the associated header. Within a row, fields shall be stored in order of increasing column

number, as determined from the n of the TFORMn keywords. The number of bytes in a row and the number of rows in the table shall determine the size of the byte array. Every row in the array shall have the same number of bytes. The first row shall begin at the start of the data block immediately following the last header block. Subsequent rows shall begin immediately following the end of the previous row, with no intervening bytes, independent of the FITS block structure. Words need not be aligned along word boundaries.

Each row in the array shall consist of a sequence of from 0 to 999 fields as specified by the TFIELDS keyword. The number of elements in each field and their data type shall be specified by the TFORMn keyword in the associated header. A separate format keyword must be provided for each field. The location and format of fields shall be the same for every row. Fields may be empty, if the repeat count specified in the value of the TFORMn keyword of the header is 0. Writers of binary tables should select a format appropriate to the form, range of values, and accuracy of the data in the table. The following data types, and no others, are permitted.

Logical. If the value of the TFORMn keyword specifies Data Type ’L’, the contents of Field n shall consist of ASCII T indicating true or ASCII F, indicating false. A 0 byte (hexadecimal 00) indicates a NULL value.

Bit array. If the value of the TFORMn keyword specifies data type’X’, the contents of Field n shall consist of a sequence of bits starting with the most-significant bit; the bits following shall be in order of decreasing significance, ending with the least significant bit. A bit array shall be composed of an integral number of bytes, with those bits following the end of the data set to zero. No null value is defined for bit arrays.

Character. If the value of the TFORMn keyword specifies Data Type ’A’, Field n shall contain a character string of zero-ormore members, composed of the restricted set of ASCII-text characters. This character string may be terminated before the length specified by the repeat count by an ASCII NULL (hexadecimal code 00). Characters after the first ASCII NULL are not defined. A string with the number of characters specified by

25

<!-- page 32 of 75 -->

the repeat count is not NULL terminated. Null strings are defined by the presence of an ASCII NULL as the first character.

Unsigned 8-Bit integer. If the value of the TFORMn keyword specifies Data Type ’B’, the data in Field n shall consist of unsigned eight-bit integers, with the most-significant bit first, and subsequent bits in order of decreasing significance. Null values are given by the value of the associated TNULLn keyword. Signed integers can be represented using the convention described in Sect. 5.2.5.

16-Bit integer. If the value of the TFORMn keyword specifies Data Type ’I’, the data in Field n shall consist of two’s complement signed 16-bit integers, contained in two bytes. The mostsignificant byte shall be first (big-endian byte order). Within each byte the most-significant bit shall be first, and subsequent bits shall be in order of decreasing significance. Null values are given by the value of the associated TNULLn keyword. Unsigned integers can be represented using the convention described in Sect. 5.2.5.

32-Bit integer. If the value of the TFORMn keyword specifies Data Type ’J’, the data in Field n shall consist of two’s complement signed 32-bit integers, contained in four bytes. The mostsignificant byte shall be first, and subsequent bytes shall be in order of decreasing significance (big-endian byte order). Within each byte, the most-significant bit shall be first, and subsequent bits shall be in order of decreasing significance. Null values are given by the value of the associated TNULLn keyword. Unsigned integers can be represented using the convention described in Sect. 5.2.5.

64-Bit integer. If the value of the TFORMn keyword specifies Data Type ’K’, the data in Field n shall consist of two’s complement signed 64-bit integers, contained in eight bytes. The most-significant byte shall be first, and subsequent bytes shall be in order of decreasing significance. Within each byte, the most-significant bit shall be first, and subsequent bits shall be in order of decreasing significance (big-endian byte order). Null values are given by the value of the associated TNULLn keyword. Unsigned integers can be represented using the convention described in Sect. 5.2.5.

Single-precision floating point. If the value of the TFORMn keyword specifies Data Type ’E’, the data in Field n shall consist of ANSI/IEEE-754 (IEEE 1985) 32-bit floating-point numbers, in big-endian byte order, as described in Appendix E. All IEEE special values are recognized. The IEEE NaN is used to represent null values.

Double-precision floating point. If the value of the TFORMn keyword specifies Data Type ’D’, the data in Field n shall consist of ANSI/IEEE-754 (IEEE 1985) 64-bit double-precision floating-point numbers, in big-endian byte order, as described in Appendix E. All IEEE special values are recognized. The IEEE NaN is used to represent null values.

Single precision complex. If the value of the TFORMn keyword specifies Data Type ’C’, the data in Field n shall consist of a sequence of pairs of 32-bit single-precision floating-point numbers. The first member of each pair shall represent the real part of a complex number, and the second member shall represent the imaginary part of that complex number. If either member contains an IEEE NaN, the entire complex value is null.

Double-precision complex. If the value of the TFORMn keyword specifies Data Type ’M’, the data in Field n shall consist of a sequence of pairs of 64-bit double-precision floating-point numbers. The first member of each pair shall represent the real part of a complex number, and the second member of the pair shall represent the imaginary part of that complex number. If either member contains an IEEE NaN, the entire complex value is null.

Array descriptor. The repeat count on the P and Q arraydescriptor fields must either have a value of 0 (denoting an empty field of zero bytes) or 1. If the value of the TFORMn keyword specifies Data Type ’1P’, the data in Field n shall consist of one pair of 32-bit integers. If the value of the TFORMn keyword specifies Data Type ’1Q’, the data in Field n shall consist of one pair of 64-bit integers. The meaning of these integers is defined in Sect. 7.3.5.

## 7.3.3.2. Bytes following main table

The main data table may be followed by a supplemental data area called the heap. The size of the supplemental data area, in bytes, is specified by the value of the PCOUNT keyword. The use of this data area is described in Sect. 7.3.5.

## 7.3.4. Data display

The indexed TDISPn keyword may be used to describe the recommended format for displaying an ASCII-text representation of the contents of Field n. The permitted display format codes for each type of data (i.e., character strings, logical, integer, or real) are given in Table 20 and described below.

Character data. If the table column contains a character string (with TFORMn = ’rA’) then the TDISPn format code must be Aw, where w is the number of characters to display. If the character datum has length less than or equal to w, it is represented on output right-justified in a string of w characters. If the character datum has length greater than w, the first w characters of the datum are represented on output in a string of w characters. Character data are not surrounded by single- or double-quotation marks unless those marks are themselves part of the data value.

Logical data. If the table column contains logical data (with TFORMn = ’rL’) then the TDISPn format code must be Lw, where w is the width in characters of the display field. Logical data are represented on output with the character T for true or F for false right-justified in a space-filled string of w characters. A null value may be represented by a string of w space characters.

26

<!-- page 33 of 75 -->

Integer data. If the table column contains integer data (with $\mathtt { T F O \check { R M } } n = \mathtt { ' r X ' , ' r B ' , ' r I ' , ' r J ' , o r ' r K ' } )$ then the TDISPn format code may have any of these forms: Iw.m, Bw.m, Ow.m, or Zw.m. The default value of m is one and the ’.m’ is optional. The first letter of the code specifies the number base for the encoding with I for decimal (10), B for binary (2), O for octal (8), and Z for hexadecimal (16). Hexadecimal format uses the upper-case letters A through F to represent decimal values 10 through 15. The output field consists of w characters containing zero-or-more leading spaces followed by a minus sign if the internal datum is negative (only in the case of decimal encoding with the I format code), followed by the magnitude of the internal datum in the form of an unsigned-integer constant in the specified number base, with only as many leading zeros as are needed to have at least m numeric digits. Note that $\mathfrak { m } \leq \mathfrak { w }$ is allowed if all values are positive, but m < w is required if any values are negative. If the number of digits required to represent the integer datum exceeds w, then the output field consists of a string of w asterisk (\*) characters.

Real data. If the table column contains real data (with $\mathrm{TFORM} = \mathrm{~rE',~or~rD'}$ or contains integer data (with any of the TFORMn format codes listed in the previous paragraph), which are recommended to be displayed as real values (i.e., especially in cases where the integer values represent scaled physical values using Eq. 7), then the TDISPn format code may have any of these forms: Fw.d, Ew.dEe, Dw.dEe, ENw.d, or ESw.d. In all cases, the output is a string of w characters including the decimal point, any sign characters, and any exponent including the exponent’s indicators, signs, and values. If the number of digits required to represent the real datum exceeds w, then the output field consists of a string of w asterisk (\*) characters. In all cases, d specifies the number of digits to appear to the right of the decimal point.

The F format code output field consists of $\mathbf { w } - \mathbf { d } - 1$ characters containing zero-or-more leading spaces, followed by a minus sign if the internal datum is negative, followed by the absolute magnitude of the internal datum in the form of an unsignedinteger constant. These characters are followed by a decimal point $( \cdot )$ and d characters giving the fractional part of the internal datum, rounded by the normal rules of arithmetic to d fractional digits.

For the E and D format codes, an exponent is taken such that the fraction $0 . 1 \leq | \mathrm { d a t u m } | / 1 0 ^ { \mathrm { e x p o n e n t } } < 1 . 0$ . The fraction (with appropriate sign) is output with an F format of width $\mathtt { w - e - 2 }$ characters with d characters after the decimal followed by an E or D followed by the exponent as a signed e + 1 character integer with leading zeros as needed. The default value of e is 2 when the Ee portion of the format code is omitted. If the exponent value will not fit in e + 1 characters but will fit in e + 2 then the E (or D) is omitted and the wider field used. If the exponent value will not fit (with a sign character) in $\mathbf { e } + 2$ characters, then the entire w-character output field is filled with asterisks (\*).

The ES format code is processed in the same manner as the E format code except that the exponent is taken so that $1 . 0 \leq$ fraction < 10.

The EN format code is processed in the same manner as the E format code except that the exponent is taken to be an integer multiple of three and so that $\bar { 1 . 0 \leq }$ fraction < 1000.0. All real format codes have number base 10. There is no difference be-

tween E and D format codes on input other than an implication with the latter of greater precision in the internal datum.

The Gw.dEe format code may be used with data of any type. For data of type integer, logical, or character, it is equivalent to Iw, Lw, or Aw, respectively. For data of type real, it is equivalent to an F format (with different numbers of characters after the decimal) when that format will accurately represent the value and is equivalent to an E format when the number (in absolute value) is either very small or very large. Specifically, for real values outside the range $0 . 1 - 0 . 5 \times 1 0 ^ { - \mathbf { d } - 1 } \leq \mathrm { v a l u e } < 1 0 ^ { \mathbf { d } } -$ 0.5, it is equivalent to Ew.dEe. For real values within the above range, it is equivalent to $\mathtt { F w ^ { \prime } . d ^ { \prime } }$ followed by $2 + \mathbf { e }$ spaces, where $\mathbf{w}' = \mathbf{w} - \mathbf{e} - 2$ and $\mathbf { d } ^ { \prime } \; = \; \mathbf { d } - k$ for $k   =   0 , 1 , \ldots , \mathbf { d }$ if the real datum value lies in the range $1 0 ^ { k - 1 } \left( 1   -   0 . 5   \times   1 0 ^ { - \mathbf { d } } \right) \leq$ value ≤ 10k $\left( 1   -   0 . 5   \times   1 0 ^ { - \mathbf { d } } \right)$

Complex data. If the table column contains complex data (with $\mathrm{TF0RM} = \mathrm{rC}, \mathrm{or} \mathrm{rM}$ then they may be displayed with any of the real data formats as described above. The same format is used for the real and imaginary parts. It is recommended that the two values be separated by a comma and enclosed in parentheses with a total field width of 2w + 3.

## 7.3.5. Variable-length arrays

One of the most attractive features of binary tables is that any field of the table can be an array. In the standard case this is a fixed-size array, i.e., a fixed amount of storage is allocated in each row for the array data—whether it is used or not. This is fine so long as the arrays are small or a fixed amount of array data will be stored in each field, but if the stored array length varies for different rows, it is necessary to impose a fixed upper limit on the size of the array that can be stored. If this upper limit is made too large excessive wasted space can result and the binary-table mechanism becomes seriously inefficient. If the limit is set too low then storing certain types of data in the table could become impossible.

The variable-length array construct presented here was devised to deal with this problem. Variable-length arrays are implemented in such a way that, even if a table contains such arrays, a simple reader program that does not understand variablelength arrays will still be able to read the main data table (in other words a table containing variable-length arrays conforms to the basic binary-table standard). The implementation chosen is such that the rows in the main data table remain fixed in size even if the table contains a variable-length array field, allowing efficient random access to the main data table.

Variable-length arrays are logically equivalent to regular static arrays, the only differences being 1) the length of the stored array can differ for different rows, and 2) the array data are not stored directly in the main data table. Since a field of any data type can be a static array, a field of any data type can also be a variable-length array (excluding the Type P and Q variablelength array descriptors themselves, which are not a data type so much as a storage-class specifier). Other established FITS conventions that apply to static arrays will generally apply as well to variable-length arrays.

A variable-length array is declared in the table header with one of the following two special field data-type specifiers

$$
r \mathrm{Pt} (e _ {\max})
$$

27

<!-- page 34 of 75 -->

$$
r Q t (e _ {\max})
$$

where the ${ } ^ { \bullet } \mathbf { P } ^ { \bullet }$ or ’Q’ indicates the presence of an array descriptor (described below), the element count r should be 0, 1, or absent, t is a character denoting the data type of the array data (L, X, B, I, J, K, etc., but not P or Q), and $e _ { \mathrm { m a x } }$ is a quantity guaranteed to be equal to or greater than the maximum number of elements of type t actually stored in any row of the table. There is no built-in upper limit on the size of a stored array (other than the fundamental limit imposed by the range of the array descriptor, defined below); $e _ { \mathrm { m a x } }$ merely reflects the size of the largest array actually stored in the table, and is provided to avoid the need to preview the table when, for example, reading a table containing variable-length elements into a database that supports only fixed-size arrays. There may be additional characters in the TFORMn keyword following the $e _ { \mathrm { m a x } }$

For example,

$$
\text {TFORM8} = ^ {\prime} \mathrm{PB} (1 8 0 0) ^ {\prime} / \text {Variable byte array}
$$

indicates that Field 8 of the table is a variable-length array of type byte, with a maximum stored array length not to exceed 1800 array elements (bytes in this case).

The data for the variable-length arrays in a table are not stored in the main data table; they are stored in a supplemental data area, the heap, following the main data table. What is stored in the main data table field is an array descriptor. This consists of two 32-bit signed integer values in the case of ${ } ^ { \bullet } \mathbf { P } ^ { \bullet }$ array descriptors, or two 64-bit signed integer values in the case of ${ } ^ { \prime } \mathbb { Q } ^ { \prime }$ array descriptors: the number of elements (array length) of the stored array, followed by the zero-indexed byte offset of the first element of the array, measured from the start of the heap area. The meaning of a negative value for either of these integers is not defined by this Standard. Storage for the array is contiguous. The array descriptor for Field N as it would appear embedded in a table row is illustrated symbolically below.

$$
\dots \text {[Field} N - 1 \text {]} \text {[(nelem,offset)] [Field} N + 1 \text {]} \dots
$$

If the stored array length is zero, there is no array data, and the offset value is undefined (it should be set to zero). The storage referenced by an array descriptor must lie entirely within the heap area; negative offsets are not permitted.

A binary table containing variable-length arrays consists of three principal segments, as follows.

## [table header] [main data table] (optional gap) [heap area]

The table header consists of one or more 2880-byte header blocks with the last block indicated by the keyword END somewhere in the block. The main data table begins with the first data block following the last header block and is NAXIS1 × NAXIS2 bytes in length. The zero-indexed byte offset to the start of the heap, measured from the start of the main data table, may be given by the THEAP keyword in the header. If this keyword is missing then the heap begins with the byte immediately following main data table $( \mathbf { i . e . } ,$ , the default value of THEAP is NAXIS1 × NAXIS2). This default value is the minimum allowed value for the THEAP keyword, because any smaller value would imply that the heap and the main data table overlap. If the THEAP keyword has a value larger than this default value, then there is a gap between the end of the main data table and the start of the heap. The total length in bytes of the supplemental data area

following the main data table (gap plus heap) is given by the PCOUNT keyword in the table header.

For example, suppose a table contains five rows that are each 168 bytes long, with a heap area 3000 bytes long, beginning at an offset of 2880, thereby aligning the main data table and heap areas on data block boundaries (this alignment is not necessarily recommended but is useful for this example). The data portion of the table consists of three 2880-byte data blocks: the first block contains the 840 bytes from the five rows of the main data table followed by 2040 fill bytes; the heap completely fills the second block; the third block contains the remaining 120 bytes of the heap followed by 2760 fill bytes. PCOUNT gives the total number of bytes from the end of the main data table to the end of the heap, and in this example has a value of 2040 + 2880 + 120 = 5040. This is expressed in the table header as shown below.

```txt
NAXIS1 = 168 / Width of table row in bytes
NAXIS2 = 5 / Number of rows in table
PCOUNT = 5040 / Random parameter count
...
THEAP = 2880 / Byte offset of heap area
```

The values of TSCALn and TZEROn for variable-length array column entries are to be applied to the values in the data array in the heap area, not the values of the array descriptor. These keywords can be used to scale data values in either static or variablelength arrays.

## 7.3.6. Variable-length-array guidelines

While the above description is sufficient to define the required features of the variable-length array implementation, some hints regarding usage of the variable-length array facility might also be useful.

Programs that read binary tables should take care to not assume more about the physical layout of the table than is required by the specification. For example, there are no requirements on the alignment of data within the heap. If efficient runtime access is a concern one might want to design the table so that data arrays are aligned to the size of an array element. In another case one might want to minimize storage and forgo any efforts at alignment (by careful design it is often possible to achieve both goals). Variable-length array data may be stored in the heap in any order, i.e., the data for row N+1 are not necessarily stored at a larger offset than that for row N. There may be gaps in the heap where no data are stored. Pointer aliasing is permitted, i.e., the array descriptors for two or more arrays may point to the same storage location (this could be used to save storage if two or more arrays are identical).

Byte arrays are a special case because they can be used to store a ‘typeless’ data sequence. Since FITS is a machineindependent storage format, some form of machine-specific data conversion (byte swapping, floating-point format conversion) is implied when accessing stored data with types such as integer and floating, but byte arrays are copied to and from external storage without any form of conversion.

An important feature of variable-length arrays is that it is possible that the stored array length may be zero. This makes it possible to have a column of the table for which, typically, no data are present in each stored row. When data are present, the stored array can be as large as necessary. This can be useful when storing complex objects as rows in a table.

28

<!-- page 35 of 75 -->

Accessing a binary table stored on a random-access storage medium is straightforward. Since the rows of data in the main data table are fixed in size they can be randomly accessed given the row number, by computing the offset. Once the row has been read in, any variable-length array data can be directly accessed using the element count and offset given by the array descriptor stored in that row.

Reading a binary table stored on a sequential-access storage medium requires that a table of array descriptors be built up as the main data table rows are read in. Once all the table rows have been read, the array descriptors are sorted by the offset of the array data in the heap. As the heap data are read, arrays are extracted sequentially from the heap and stored in the affected rows using the back pointers to the row and field from the table of array descriptors. Since array aliasing is permitted, it might be necessary to store a given array in more than one field or row.

Variable-length arrays are more complicated than regular static arrays and might not be supported by some software systems. The producers of FITS data products should consider the capabilities of the likely recipients of their files when deciding whether or not to use this format, and as a general rule should use it only in cases where it provides significant advantages over the simpler fixed-length array format. In particular, the use of variable-length arrays might present difficulties for applications that ingest the FITS file via a sequential input stream, because the application cannot fully process any rows in the table until after the entire fixed-length table, and potentially the entire heap has been transmitted as outlined in the previous paragraph.

## 8. World-coordinate systems

Representations of the mapping between image coordinates and physical (i.e., world) coordinate systems (WCSs) may be represented within FITS HDUs. The keywords that are used to express these mappings are now rigorously defined in a series of papers on world-coordinate systems (Greisen & Calabretta 2002), celestial-coordinate systems (Calabretta & Greisen 2002), spectral-coordinate systems (Greisen et al. 2006), and timecoordinate systems (Rots et al. 2015). An additional spherical projection, called HEALPix, is defined in reference (Calabretta & Roukema 2007). These WCS papers have been formally approved by the IAUFWG and therefore are incorporated by reference as an official part of this Standard. The reader should refer to these papers for additional details and background information that cannot be included here. Various updates and corrections to the primary WCS papers have been compiled by the authors, and are reflected in this section. Therefore, where conflicts exist, the description in this Standard will prevail.

## 8.1. Basic concepts

Rather than store world coordinates separately for each datum, the regular lattice structure of a FITS image offers the possibility of defining rules for computing world coordinates at each point. As stated in Sect. 3.3.2 and depicted in Fig. 1, image array data are addressed via integral array indices that range in value from 1 to NAXISj on Axis j. Recognizing that image data values may have an extent, for example an angular separation, spectral channel width or time span, and thus that it may make sense to interpolate between them, these integral array indices

![Image block](doc:5624dca/tier:standard/page:35/block:8)

Fig. 2: A schematic view of converting pixel coordinates to world coordinates.

may be generalized to floating-point pixel coordinates. Integral pixel-coordinate values coincide with the corresponding array indices, while fractional pixel-coordinate values lie between array indices and thus imply interpolation. Pixel-coordinate values are defined at all points within the image lattice and outside it (except along conventional axes, see Sect. 8.5). They form the basis of the world-coordinate formalism in FITS depicted schematically in Fig. 2.

The essence of representing world-coordinate systems in FITS is the association of various reserved keywords with elements of a transformation (or a series of transformations), or with parameters of a projection function. The conversion from pixel coordinates in the data array to world coordinates is simply a matter of applying the specified transformations (in order) via the appropriate keyword values; conversely, defining a WCS for an image amounts to solving for the elements of the transformation matrix(es) or coefficients of the function(s) of interest and recording them in the form of WCS keyword values. The description of the WCS systems and their expression in FITS HDUs is quite extensive and detailed, but is aided by a careful choice of notation. Key elements of the notation are summarized in Table 21, and are used throughout this section. The formal definitions of the keywords appear in the following subsections.

The conversion of image pixel coordinates to world coordinates is a multi-step process, as illustrated in Fig. 2.

For all coordinate types, the first step is a linear transformation applied via matrix multiplication of the vector of pixelcoordinate elements, $p _ { j } ;$

$$
q _ {i} = \sum_ {j = 1} ^ {N} m _ {i j} (p _ {j} - r _ {j})\tag{9}
$$

where $r _ { j }$ are the pixel-coordinate elements of the reference point, j indexes the pixel axis, and i the world axis. The $m _ { i j }$ matrix

29

<!-- page 36 of 75 -->

Table 21: WCS and celestial coordinates notation.

| Variable(s) | Meaning | Related FITS keywords |
| --- | --- | --- |
| i | Index variable for world coordinates |  |
| j | Index variable for pixel coordinates |  |
| a | Alternative WCS version code |  |
| $p_j$ | Pixel coordinates |  |
| $r_j$ | Reference pixel coordinates | CRPIXja |
| $m_{ij}$ | Linear-transformation matrix | CDi_ja or PCi_ja |
| $s_i$ | Coordinate scales | CDELTia |
| (x,y) | Projection plane coordinates |  |
| (φ,θ) | Native longitude and latitude |  |
| (α,δ) | Celestial longitude and latitude |  |
| $(\phi_0,\theta_0)$ | Native longitude and latitude of the fiducial point | PVi_1a†, PVi_2a† |
| $(\alpha_0,\delta_0)$ | Celestial longitude and latitude of the fiducial point | CRVALia |
| $(\alpha_p,\delta_p)$ | Celestial longitude and latitude of the native pole |  |
| $(\phi_p,\theta_p)$ | Native longitude and latitude of the celestial pole | LONPOLEa (=PVi_3a†), LATPOLEa (=PVi_4a†) |

Notes. † Associated with Longitude Axis i.

is a non-singular, square matrix of dimension $N \times N ,$ where N is the number of world-coordinate axes. The elements $q _ { i }$ of the resulting intermediate pixel coordinate vector are offsets, in dimensionless pixel units, from the reference point along axes co-incident with those of the intermediate world coordinates. Thus, the conversion of $q _ { i }$ to the corresponding Intermediate-worldcoordinate Element x<sub>i</sub> is a simple scale:

$$
x _ {i} = s _ {i} q _ {i}.\tag{10}
$$

There are three conventions for associating FITS keywords with the above transformations. In the first formalism, the matrix elements $m _ { i j }$ are encoded in the $\mathbf { P } C i j$ keywords and the scale factors $s _ { i }$ are encoded in the CDELTi keywords, which must have non-zero values. In the second formalism Eqs. (9) and (10) are combined as

$$
x _ {i} = \sum_ {j = 1} ^ {N} (s _ {i} m _ {i j}) (p _ {j} - r _ {j})\tag{11}
$$

and the $\mathsf { C D } i j$ keywords encode the product $s _ { i } m _ { i j } .$ The third convention was widely used before the development of the two pre-viously described conventions and uses the CDELTi keywords to define the image scale and the CROTA2 keyword to specify a bulk rotation of the image plane. Use of the CROTA2 keyword is now deprecated, and instead the newer PCi j or $\mathsf { C D } i j$ keywords are recommended because they allow for skewed axes and fully general rotation of multi-dimensional arrays. The CDELTi and CROTA2 keywords may co-exist with the $\mathbf { \dot { C } } \mathrm { D } i j$ keywords (but the CROTA2 must not occur with the $\mathbf { P } C i _ { \mathcal { I } }$ keywords) as an aid to old FITS interpreters, but these keywords must be ignored by software that supports the CDi j keyword convention. In all these formalisms the reference pixel coordinates $r _ { j }$ are encoded in the CRPIXi keywords, and the world coordinates at the reference point are encoded in the CRVALi keywords. For additional details, see Greisen & Calabretta (2002).

The third step of the process, computing the final world co-ordinates, depends on the type of coordinate system, which is indicated with the value of the CTYPEi keyword. For some simple, linear cases an appropriate choice of normalization for the scale factors allows the world coordinates to be taken directly (or by applying a constant offset) from the $x _ { i }$ (e.g., some spectra).

In other cases it is more complicated, and may require the application of some non-linear algorithm (e.g., a projection, as for celestial coordinates), which may require the specification of additional parameters. Where necessary, numeric parameter values for non-linear algorithms must be specified via PVi m keywords and character-valued parameters will be specified via PSi m keywords, where m is the parameter number.

The application of these formalisms to coordinate systems of interest is discussed in the following sub-sections: Sect. 8.2 describes general WCS representations (see Greisen & Calabretta 2002), Sect. 8.3 describes celestial-coordinate systems (see Calabretta & Greisen 2002)), Sect. 8.4 describes spectralcoordinate systems (see Greisen et al. 2006), and Sect. 9 describes the representation of time coordinates (see Rots et al. 2015).

## 8.2. World-coordinate-system representations

A variety of keywords have been reserved for computing the coordinate values that are to be associated with any pixel location within an array. The full set is given in Table 22; those in most common usage are defined in detail below for convenience. Coordinate-system specifications may appear in HDUs that contain simple images in the primary array or in an IMAGE extension. Images may also be stored in a multi-dimensional vector cell of a binary table, or as a tabulated list of pixel locations (and optionally, the pixel value) in a table. In these last two types of image representations, the WCS keywords have a different naming convention, which reflects the needs of the tabular data structure and the eight-character limit for keyword lengths, but otherwise follow exactly the same rules for type, usage, and default values. See reference Calabretta & Greisen (2002) for example usage of these keywords. All forms of these reserved keywords must be used only as specified in this Standard.

In the case of the binary-table vector representation, it is possible that the images contained in a given column of the table have different coordinate transformation values. Table 9 of Calabretta & Greisen (2002) illustrates a technique (com-

30

<!-- page 37 of 75 -->

monly known as the “Green Bank Convention<sup>10</sup>”), which utilizes additional columns in the table to record the coordinatetransformation values that apply to the corresponding image in each row of the table. More information is provided in Appendix L.

The keywords given below constitute a complete set of fundamental attributes for a WCS description. Although their inclusion in an HDU is optional, FITS writers should include a complete set of keywords when describing a WCS. In the event that some keywords are missing, default values must be assumed, as specified below.

WCSAXES – [integer; default: NAXIS, or larger of WCS indices i or j]. Number of axes in the WCS description. This keyword, if present, must precede all WCS keywords except NAXIS in the HDU. The value of WCSAXES may exceed the number of pixel axes for the HDU.

CTYPEi – [string; indexed; default: ' ' (i.e. a linear, undefined axis)]. Type for the Intermediate-coordinate Axis i. Any co-ordinate type that is not covered by this Standard or an officially recognized FITS convention shall be taken to be linear. All non-linear coordinate system names must be expressed in ‘4–3’ form: the first four characters specify the coordinate type, the fifth character is a hyphen (‘-’), and the remaining three characters specify an algorithm code for computing the world coordinate value. Coordinate types with names of fewer than four characters are padded on the right with hyphens, and algorithm codes with fewer than three characters are padded on the right with blanks<sup>11</sup>. Algorithm codes should be three characters.

CUNITi – [string; indexed; default: ' ' (i.e., undefined)]. Physical units of CRVAL and CDELT for Axis i. Note that units should always be specified (see Sect. 4.3). Units for celestial coordinate systems defined in this Standard must be degrees.

CRPIXj – [floating point; indexed; default: 0.0]. Location of the reference point in the image for Axis j corresponding to rj in Eq. (9). Note that the reference point may lie outside the image and that the first pixel in the image has pixel coordinates (1.0, 1.0, . . .).

CRVALi – [floating point; indexed; default: 0.0]. Worldcoordinate value at the reference point of Axis i.

CDELTi – [floating point; indexed; default: 1.0]. Increment of the world coordinate at the reference point for Axis i. The value must not be zero.

CROTAi – [floating point; indexed; default: 0.0]. The amount of rotation from the standard coordinate system to a different coordinate system. Further use of this of this keyword is deprecated, in favor of the newer formalisms that use the CDi j or PCi j keywords to define the rotation.

PCi j – [floating point; defaults: 1.0 when i = j, 0.0 otherwise]. Linear transformation matrix between Pixel Axes j and Intermediate-coordinate Axes i. The PCi j matrix must not be singular.

CDi j – [floating point; defaults: 0.0, but see below]. Linear transformation matrix (with scale) between Pixel Axes j and Intermediate-coordinate Axes i. This nomenclature is

equivalent to PCi j when CDELTi is unity. The CDi j matrix must not be singular. Note that the CDi j formalism is an exclusive alternative to PCi j, and the CDi j and PCi j keywords must not appear together within an HDU.

In addition to the restrictions noted above, if any CDi j keywords are present in the HDU, all other unspecified CDi j keywords shall default to zero. If no CDi j keywords are present then the header shall be interpreted as being in PCi j form whether or not any PCi j keywords are actually present in the HDU.

Some non-linear algorithms that describe the transformation between pixel and intermediate-coordinate axes require parameter values. A few non-linear algorithms also require charactervalued parameters, e.g., table lookups require the names of the table extension and the columns to be used. Where necessary parameter values must be specified via the following keywords.

PVi m – [floating point]. Numeric parameter values for Intermediate-world-coordinate Axis i, where m is the parameter number. Leading zeros must not be used, and m may have only values in the range 0 through 99, and that are defined for the particular non-linear algorithm.

PSi m – [string]. Character-valued parameters for Intermediateworld-coordinate Axis i, where m is the parameter number. Leading zeros must not be used, and m may have only values in the range 0 through 99, and that are defined for the particular non-linear algorithm.

The following keywords, while not essential for a complete specification of an image WCS, can be extremely useful for readers to interpret the accuracy of the WCS representation of the image.

CRDERi – [floating point; default: 0.0]. Random error in Coordinate i, which must be non-negative.

CSYERi – [floating point; default: 0.0]. Systematic error in Coordinate i, which must be non-negative.

These values should give a representative average value of the error over the range of the coordinate in the HDU. The total error in the coordinates would be given by summing the individual errors in quadrature.

## 8.2.1. Alternative WCS axis descriptions

In some cases it is useful to describe an image with more than one coordinate type<sup>12</sup>. Alternative WCS descriptions may be added to the header by adding the appropriate sets of WCS keywords, and appending to all keywords in each set an alphabetic code in the range A through Z. Keywords that may be used in this way to specify a coordinate system version are indicated in Table 22 with the suffix a. All implied keywords with this encoding are reserved keywords, and must only be used in FITS HDUs as specified in this Standard. The axis numbers must lie in the range 1 through 99, and the coordinate parameter m must lie in the range 0 through 99, both with no leading zeros.

The primary version of the WCS description is that specified with a as the blank character<sup>13</sup>. Alternative axis descriptions are

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">10 Named after a meeting held in Green Bank, West Virginia, USA in 1989 to develop standards for the interchange of single-dish radioastronomy data.</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">12 Examples include the frequency, velocity, and wavelength along a spectral axis (only one of which, of course, could be linear), or the position along an imaging detector in both meters and degrees on the sky.</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">11 Example: ’RA---UV ’.</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">13 There are a number of keywords (e.g. ijPCna) where the a could be pushed off the eight-character keyword name for plausible values of i,</span></small>

31

<!-- page 38 of 75 -->

Table 22: Reserved WCS keywords (continues on next page)

<table><tr><td rowspan="2">Keyword Description</td><td rowspan="2">Global</td><td rowspan="2">Image</td><td colspan="2">BINTABLE vector</td><td colspan="2">Pixel list</td></tr><tr><td>Primary</td><td>Alternative</td><td>Primary</td><td>Alternative</td></tr><tr><td>Coordinate dimensionality</td><td></td><td>WCSAXESa</td><td colspan="2">WCAXna</td><td colspan="2">...</td></tr><tr><td>Axis type</td><td></td><td>CTYPEia</td><td>iCTYPn</td><td>iCTYna</td><td>TCTYPn</td><td>TCTYna</td></tr><tr><td>Axis units</td><td></td><td>CUNITia</td><td>iCUNIn</td><td>iCUNna</td><td>TCUNIn</td><td>TCUNna</td></tr><tr><td>Reference value</td><td></td><td>CRVALia</td><td>iCRVLn</td><td>iCRVna</td><td>TCRVLn</td><td>TCRVna</td></tr><tr><td>Coordinate increment</td><td></td><td>CDELTia</td><td>iCDLTn</td><td>iCDEna</td><td>TCDLTn</td><td>TCDENa</td></tr><tr><td>Reference point</td><td></td><td>CRPIXja</td><td>jCRPXn</td><td>jCRPna</td><td>TCRPXn</td><td>TCRPna</td></tr><tr><td> $Coordinate\ rotation^1$ </td><td></td><td>CROTAi</td><td colspan="2">iCROTn</td><td colspan="2">TCROTn</td></tr><tr><td> $Transformation\ matrix^2$ </td><td></td><td>PCi_ja</td><td colspan="2">ijPCna</td><td colspan="2">TPCn_ka or TPn_ka</td></tr><tr><td> $Transformation\ matrix^2$ </td><td></td><td>CDi_ja</td><td colspan="2">ijCDna</td><td colspan="2">TCDn_ka or TCn_ka</td></tr><tr><td>Coordinate parameter</td><td></td><td>PVi_ma</td><td colspan="2">iPVn_ma or iNn_ma</td><td colspan="2">TPVn_ma or TVn_ma</td></tr><tr><td>Coordinate parameter array</td><td></td><td>...</td><td colspan="2">iNn_Xa</td><td colspan="2">...</td></tr><tr><td>Coordinate parameter</td><td></td><td>PSi_ma</td><td colspan="2">iPSn_ma or iSn_ma</td><td colspan="2">TPSn_ma or TSn_ma</td></tr><tr><td>Coordinate name</td><td></td><td>WCSNAMEa</td><td colspan="2">WCSNna</td><td colspan="2">WCSna or TWCSna</td></tr><tr><td>Coordinate axis name</td><td></td><td>CNAMEia</td><td colspan="2">iCNAna</td><td colspan="2">TCNAna</td></tr><tr><td>Random error</td><td></td><td>CRDERia</td><td colspan="2">iCRDna</td><td colspan="2">TCRDna</td></tr><tr><td>Systematic error</td><td></td><td>CSYERia</td><td colspan="2">iCSYna</td><td colspan="2">TCSYna</td></tr><tr><td>WCS cross-reference target</td><td></td><td>...</td><td colspan="2">WCSTna</td><td colspan="2">...</td></tr><tr><td>WCS cross reference</td><td></td><td>...</td><td colspan="2">WCSXna</td><td colspan="2">...</td></tr><tr><td>Coordinate rotation</td><td></td><td>LONPOLEa</td><td colspan="2">LONPna</td><td colspan="2">LONPna</td></tr><tr><td>Coordinate rotation</td><td></td><td>LATPOLEa</td><td colspan="2">LATPna</td><td colspan="2">LATPna</td></tr><tr><td>Coordinate epoch</td><td></td><td>EQUINOXa</td><td colspan="2">EQUIna</td><td colspan="2">EQUIna</td></tr><tr><td> $Coordinate\ epoch^3$ </td><td>EPOCH</td><td></td><td colspan="2">EPOCH</td><td colspan="2">EPOCH</td></tr><tr><td>Reference frame</td><td> $RADECSYS^4$ </td><td>RADESYSa</td><td colspan="2">RADEna</td><td colspan="2">RADEna</td></tr><tr><td>Line rest frequency (Hz)</td><td> $RESTFREQ^4$ </td><td>RESTFRQa</td><td colspan="2">RFRQna</td><td colspan="2">RFRQna</td></tr><tr><td>Line rest vacuum wavelength (m)</td><td></td><td>RESTWAVa</td><td colspan="2">RWAVna</td><td colspan="2">RWAVna</td></tr><tr><td>Spectral reference frame</td><td></td><td>SPECSYSa</td><td colspan="2">SPECna</td><td colspan="2">SPECna</td></tr><tr><td>Spectral reference frame</td><td></td><td>SSYSOBSa</td><td colspan="2">SOBSna</td><td colspan="2">SOBSna</td></tr><tr><td>Spectral reference frame</td><td></td><td>SSYSSRCa</td><td colspan="2">SSRCna</td><td colspan="2">SSRCna</td></tr><tr><td>Observation X (m)</td><td> $OBSGEO-X^5$ </td><td></td><td colspan="2">OBSGXn</td><td colspan="2">OBSGXn</td></tr><tr><td>Observation Y (m)</td><td> $OBSGEO-Y^5$ </td><td></td><td colspan="2">OBSGYn</td><td colspan="2">OBSGYn</td></tr><tr><td>Observation Z (m)</td><td> $OBSGEO-Z^5$ </td><td></td><td colspan="2">OBSGZn</td><td colspan="2">OBSGZn</td></tr><tr><td>Radial velocity ( $m\ s^{-1}$ )</td><td></td><td>VELOSYSa</td><td colspan="2">VSYSna</td><td colspan="2">VSYSna</td></tr><tr><td>Redshift of source</td><td></td><td>ZSOURCEa</td><td colspan="2">ZSOUna</td><td colspan="2">ZSOUna</td></tr><tr><td>Angle of true velocity</td><td></td><td>VELANGLa</td><td colspan="2">VANGna</td><td colspan="2">VANGna</td></tr><tr><td colspan="7">Date-time related keywords (see Sect.9)</td></tr><tr><td>Date of HDU creation</td><td>DATE</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="4">Date/time of observation</td><td>DATE-OBS</td><td></td><td colspan="2">DOBSn</td><td colspan="2">DOBSn</td></tr><tr><td>MJD-OBS</td><td></td><td colspan="2">MJDOBn</td><td colspan="2">MJDOBn</td></tr><tr><td>BEPOCH</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>JEPOCH</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="2">Average date/time of observation</td><td>DATE-AVG</td><td></td><td colspan="2">DAVGn</td><td colspan="2">DAVGn</td></tr><tr><td>MJD-AVG</td><td></td><td colspan="2">MJDAn</td><td colspan="2">MJDAn</td></tr><tr><td rowspan="3">Start date/time of observation</td><td>DATE-BEG</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>MJD-BEG</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>TSTART</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td rowspan="3">End date/time of observation</td><td>DATE-END</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>MJD-END</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>TSTOP</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Net exposure duration</td><td>XPOSURE</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Wall-clock exposure duration</td><td>TELAPSE</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Time scale</td><td>TIMESYS</td><td>CTYPEia</td><td>iCTYPn</td><td>iCTYna</td><td>TCTYPn</td><td>TCTYna</td></tr><tr><td>Time zero point (MJD)</td><td> $MJDREF^6$ </td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Time zero point (JD)</td><td> $JDREF^6$ </td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Time zero point (ISO)</td><td>DATEREF</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Reference position</td><td>TREFPOS</td><td></td><td colspan="2">TRPOSn</td><td colspan="2">TRPOSn</td></tr><tr><td>Reference direction</td><td>TREFDIR</td><td></td><td colspan="2">TRDIRn</td><td colspan="2">TRDIRn</td></tr><tr><td>Solar System ephemeris</td><td>PLEPHEM</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Time unit</td><td>TIMEUNIT</td><td>CUNITia</td><td>iCUNIn</td><td>iCUNna</td><td>TCUNIn</td><td>TCUNna</td></tr><tr><td>Time offset</td><td>TIMEOFFS</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Time absolute error</td><td>TIMSYER</td><td>CSYERia</td><td>iCSYEn</td><td>iCSYna</td><td>TCSYn</td><td>TCSYna</td></tr><tr><td>Time relative error</td><td>TIMRDER</td><td>CRDERia</td><td>iCRDEN</td><td>iCRDna</td><td>TCRDn</td><td>TCRDna</td></tr><tr><td>Time resolution</td><td>TIMEDEL</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Time location in pixel</td><td>TIMEPIXR</td><td></td><td></td><td></td><td></td><td></td></tr><tr><td>Phase-axis zero point</td><td></td><td>CZPHSia</td><td>iCZPHn</td><td>iCZPna</td><td>TCZPHn</td><td>TCZPna</td></tr><tr><td>Phase-axis period</td><td></td><td>CPERIIa</td><td>iCPERn</td><td>iCPRna</td><td>TCPERn</td><td>TCPRna</td></tr></table>

32

<!-- page 39 of 75 -->

Table 22 (continued)

**Notes.** The indices j and i are pixel and intermediate-world-coordinate axis numbers, respectively. Within a table, the index n refers to a column number, and m refers to a coordinate parameter number. The index k also refers to a column number. The indicator a is either blank (for the primary coordinate description) or a character A through Z that specifies the coordinate version. See the text.

(1) CROTAi form is deprecated but still in use. It must not be used with PC i j, PV i m, and PS i m.(2) PCi j and CDi j forms of the transformation matrix are mutually exclusive, and must not appear together in the same HDU. (3) EPOCH is deprecated. Use EQUINOX instead. (4) These eight-character keywords are deprecated; the seven-character forms, which can include an alternate version code letter at the end, should be used instead. (5) For the purpose of time reference position, geodetic latitude/longitude/elevation OBSGEO-B, OBSGEO-L, OBSGEO-H or an orbital-ephemeris keyword OBSORBIT can be also used (see Sect. 9.2.3). (6) [M]JDREF can be split in integer and fractional values [M]JDREFI and [M]JDREFF as explained in Sect. 9.2.2.

Table 23: Reserved celestial-coordinate-algorithm codes.

<table><tr><td rowspan="2">Code</td><td colspan="2">Default</td><td rowspan="2">Properties1</td><td rowspan="2">Projection name</td></tr><tr><td> $\phi_0$ </td><td> $\theta_0$ </td></tr><tr><td colspan="5">Zenithal (azimuthal) projections</td></tr><tr><td>AZP</td><td>0°</td><td>90°</td><td>Sect. 5.1.1</td><td>Zenithal perspective</td></tr><tr><td>SZP</td><td>0°</td><td>90°</td><td>Sect. 5.1.2</td><td>Slant zenithal perspective</td></tr><tr><td>TAN</td><td>0°</td><td>90°</td><td>Sect. 5.1.3</td><td>Gnomonic</td></tr><tr><td>STG</td><td>0°</td><td>90°</td><td>Sect. 5.1.4</td><td>Stereographic</td></tr><tr><td>SIN</td><td>0°</td><td>90°</td><td>Sect. 5.1.5</td><td>Slant orthographic</td></tr><tr><td>ARC</td><td>0°</td><td>90°</td><td>Sect. 5.1.6</td><td>Zenithal equidistant</td></tr><tr><td>ZPN</td><td>0°</td><td>90°</td><td>Sect. 5.1.7</td><td>Zenithal polynomial</td></tr><tr><td>ZEA</td><td>0°</td><td>90°</td><td>Sect. 5.1.8</td><td>Zenithal equal-area</td></tr><tr><td>AIR</td><td>0°</td><td>90°</td><td>Sect. 5.1.9</td><td>Airy</td></tr><tr><td colspan="5">Cylindrical projections</td></tr><tr><td>CYP</td><td>0°</td><td>0°</td><td>Sect. 5.2.1</td><td>Cylindrical perspective</td></tr><tr><td>CEA</td><td>0°</td><td>0°</td><td>Sect. 5.2.2</td><td>Cylindrical equal area</td></tr><tr><td>CAR</td><td>0°</td><td>0°</td><td>Sect. 5.2.3</td><td>Plate carrée</td></tr><tr><td>MER</td><td>0°</td><td>0°</td><td>Sect. 5.2.4</td><td>Mercator</td></tr><tr><td colspan="5">Pseudo-cylindrical and related projections</td></tr><tr><td>SFL</td><td>0°</td><td>0°</td><td>Sect. 5.3.1</td><td>Samson-Flamsteed</td></tr><tr><td>PAR</td><td>0°</td><td>0°</td><td>Sect. 5.3.2</td><td>Parabolic</td></tr><tr><td>MOL</td><td>0°</td><td>0°</td><td>Sect. 5.3.3</td><td>Mollweide</td></tr><tr><td>AIT</td><td>0°</td><td>0°</td><td>Sect. 5.3.4</td><td>Hammer-Aitoff</td></tr><tr><td colspan="5">Conic projections</td></tr><tr><td>COP</td><td>0°</td><td> $\theta_a$ </td><td>Sect. 5.4.1</td><td>Conic perspective</td></tr><tr><td>COE</td><td>0°</td><td> $\theta_a$ </td><td>Sect. 5.4.2</td><td>Conic equal-area</td></tr><tr><td>COD</td><td>0°</td><td> $\theta_a$ </td><td>Sect. 5.4.3</td><td>Conic equidistant</td></tr><tr><td>COO</td><td>0°</td><td> $\theta_a$ </td><td>Sect. 5.4.4</td><td>Conic orthomorphic</td></tr><tr><td colspan="5">Polyconic and pseudoconic projections</td></tr><tr><td>BON</td><td>0°</td><td>0°</td><td>Sect. 5.5.1</td><td>Bonne&#x27;s equal area</td></tr><tr><td>PCO</td><td>0°</td><td>0°</td><td>Sect. 5.5.2</td><td>Polyconic</td></tr><tr><td colspan="5">Quad-cube projections</td></tr><tr><td>TSC</td><td>0°</td><td>0°</td><td>Sect. 5.6.1</td><td>Tangential spherical cube</td></tr><tr><td>CSC</td><td>0°</td><td>0°</td><td>Sect. 5.6.2</td><td>COBE quadrilateralized spherical cube</td></tr><tr><td>QSC</td><td>0°</td><td>0°</td><td>Sect. 5.6.3</td><td>Quadrilateralized spherical cube</td></tr><tr><td colspan="5">HEALPix grid projection</td></tr><tr><td>HPX</td><td>0°</td><td>0°</td><td>Sect.  $6^2$ </td><td>HEALPix grid</td></tr></table>

(1) Refer to the indicated section in Calabretta & Greisen (2002) for a detailed description. (2) This projection is defined in Calabretta & Roukema (2007).

optional, but must not be specified unless the primary WCS description is also specified. If an alternative WCS description is specified, all coordinate keywords for that version must be given even if the values do not differ from those of the primary version. Rules for the default values of alternative coordinate descriptions

are the same as those for the primary description. The alternative descriptions are computed in the same fashion as the primary coordinates. The type of coordinate depends on the value of CTYPEia, and may be linear in one of the alternative descriptions and non-linear in another.

The alternative version codes are selected by the FITS writer; there is no requirement that the codes be used in alphabetic se-

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">j, k, n, and m. In such cases a is still said to be ‘blank’ although it is not the blank character.</span></small>

33

<!-- page 40 of 75 -->

quence, nor that one coordinate version differ in its parameter values from another. An optional keyword WCSNAMEa is also defined to name, and otherwise document, the various versions of WCS descriptions.

WCSNAME $\mathrm { i } a - \mathrm { l }$ [string; default for $a \cdot \mathbin { \mathaccent \cdot \cup } \mathbin { \mathaccent \cdot \cup } \left( \mathrm { i . e . } \right.$ , blank, for the primary WCS, else a character A through $\mathbf { Z }$ that specifies the coordinate version]. Name of the world-coordinate system represented by the WCS keywords with the suffix a. Its primary function is to provide a means by which to specify a particular WCS if multiple versions are defined in the HDU.

## 8.3. Celestial-coordinate-system representations

The conversion from intermediate world coordinates $( x , y )$ in the plane of projection to celestial coordinates involves two steps: a spherical projection to native longitude and latitude (φ, θ), defined in terms of a convenient coordinate system (i.e., native spherical coordinates), followed by a spherical rotation of these native coordinates to the required celestial coordinate system $( \alpha , \delta )$ The algorithm to be used to define the spherical projection must be encoded in the CTYPEi keyword as the threeletter algorithm code, the allowed values for which are specified in Table 23 and defined in references Calabretta & Greisen (2002) and Calabretta & Roukema (2007). The target celestialcoordinate system is also encoded into the left-most portion of the CTYPEi keyword as the coordinate type.

For the final step, the parameter LONPOLEa must be specified, which is the native longitude of the celestial pole, $\phi _ { p }$ . For certain projections (such as cylindricals and conics, which are less commonly used in astronomy), the additional keyword LATPOLEa must be used to specify the native latitude of the celestial pole. See Calabretta & Greisen (2002) for the transformation equations and other details.

The accepted celestial-coordinate systems are: the standard equatorial (RA-- and DEC-), and others of the form xLON and xLAT for longitude-latitude pairs, where x is G for Galactic, E for ecliptic, H for helioecliptic and S for supergalactic coordinates. Since the representation of planetary-, lunar-, and solarcoordinate systems could exceed the 26 possibilities afforded by the single character x, pairs of the form yzLN and yzLT may be used as well.

RADESYSa – [string; default: ’FK4’, ’FK5’, or ’ICRS’: see below]. Name of the reference frame of equatorial or ecliptic coordinates, whose value must be one of those specified in Table 24. The default value is ${ \tt F K 4 }$ if the value of $\mathtt { E Q U I N O X } a \; < \; 1 9 8 4 . 0 , \; \mathtt { ^ { \prime } F K } 5 \; \mathtt { ^ { \prime } } \; \mathtt { i f } \; \mathtt { ^ { \prime } E Q U I N O X } \mathtt { ^ { \prime } } a \; \geq \; 1 9 8 4 . 0 ,$ o r $\mathrm { { ^ { \prime } I C R S ^ { \prime } } }$ if ’EQUINOX’a is not given.

EQUINOXa – [floating point; default: see below]. Epoch of the mean equator and equinox in years, whose value must be non-negative. The interpretation of epoch depends upon the value of RADESYSa if present: Besselian if the value is ${ \tt F K 4 }$ $\mathrm{or} ^{\prime} \mathrm{FK}4-\mathrm{NO}-\mathrm{E}$ , Julian if the value is $\text{" } FK5 " ;$ and not applicable if the value is $\mathrm { { ^ { \prime } I C R S ^ { \prime } } }$ or ’GAPPT’.

EPOCH – [floating point]. This keyword is deprecated and should not be used in new FITS files. It is reserved primarily to prevent its use with other meanings. The EQUINOX keyword shall be used instead. The value field of this keyword was previously defined to contain a floating-point number giving the equinox in years for the celestial-coordinate system in which positions are expressed.

DATE-OBS – [floating point]. This reserved keyword is defined in Sect. 4.4.2.

MJD-OBS – [floating point; default: DATE-OBS if given, otherwise no default]. Modified Julian Date $( \mathrm { J D } - 2 , 4 0 0 , 0 0 0 . 5 )$ of the observation, whose value corresponds (by default) to the start of the observation, unless another interpretation is explained in the comment field. No specific time system (e.g. UTC, TAI, etc.) is defined for this or any of the other timerelated keywords. It is recommended that the TIMESYS keyword, as defined in Sect. 9.2.1 be used to specify the time system. See also Sect. 9.5.

LONPOLEa – [floating point; default: $\phi _ { 0 }$ if $\delta _ { 0 }   \geq   \theta _ { 0 } ,   \phi _ { 0 }   +   1 8 0 ^ { \circ }$ otherwise]. Longitude in the native coordinate system of the celestial system’s north pole. Normally, $\phi _ { 0 }$ is zero unless a non-zero value has been set for PVi 1a, which is associated with the longitude axis. This default applies for all values of $\theta _ { 0 } ,$ including $\theta _ { 0 }   =   9 0 ^ { \circ }$ , although the use of non-zero values of $\theta _ { 0 }$ are discouraged in that case.

LATPOLEa – [floating point; default: $9 0 ^ { \circ }$ , or no default if $( \theta _ { 0 } , \delta _ { 0 } , \phi _ { p } - \phi _ { 0 } ) = ( 0 , 0 , \pm 9 0 ^ { \circ } ) ]$ . Latitude in the native coordinate system of the celestial system’s north pole, or equivalently, the latitude in the celestial-coordinate system of the native system’s north pole. This keyword may be ignored or omitted in cases where LONPOLEa completely specifies the rotation to the target celestial system.

## 8.4. Spectral-coordinate-system representations

This section discusses the conversion of intermediate world co-ordinates to spectral coordinates with common axes such as frequency, wavelength, and apparent radial velocity (represented here with the coordinate variables $\nu , \lambda ,$ or v). The key point for constructing spectral WCS in FITS is that one of these coordinates must be sampled linearly in the dispersion axis; the others are derived from prescribed, usually non-linear transformations. Frequency and wavelength axes may also be sampled linearly in their logarithm.

Following the convention for the CTYPEia keyword, when i is the spectral axis the first four characters must specify a code for the coordinate type; for non-linear algorithms the fifth character must be a hyphen, and the next three characters must specify a predefined algorithm for computing the world coordinates from the intermediate physical coordinates. The coordinate type must be one of those specified in Table 25. When the algorithm is linear, the remainder of the CTYPEia keyword must be blank. When the algorithm is non-linear, the three-letter algorithm code must be one of those specified in Table 26. The relationships between the basic physical quantities $\nu , \lambda ,$ and $\nu _ { z }$ as well as the relationships between various derived quantities are given in reference Greisen et al. (2006).

The generality of the algorithm for specifying the spectralcoordinate system and its representation suggests that some additional description of the coordinate may be helpful beyond what can be encoded in the first four characters of the CTYPEia keyword; CNAMEia is reserved for this purpose. Note that this keyword provides a name for an axis in a particular WCS, while the WCSNAMEa keyword names the particular WCS as a whole. In order to convert between some form of radial velocity and either frequency or wavelength, the keywords RESTFRQa and RESTWAVa, respectively, are reserved.

34

<!-- page 41 of 75 -->

Table 24: Allowed values of RADESYSa.

| Value | Definition |
| --- | --- |
| 'ICRS' | International Celestial Reference System |
| 'FK5' | Mean place, new (IAU 1984) system |
| 'FK4'1 | Mean place, old (Bessel-Newcomb) system |
| 'FK4-NO-E'1 | Mean place: but without eccentricity terms |
| 'GAPPT' | Geocentric apparent place, IAU 1984 system |

(1) New FITS files should avoid using these older reference systems.

CNAMEia – [string; default: default: ' ' (i.e. a linear, undefined axis)]. Spectral-coordinate description that must not exceed 68 characters in length.

RESTFRQa – [floating point; default: none]. Rest frequency of the of the spectral feature of interest. The physical unit must be Hz.

RESTWAVa – [floating point; default: none]. Vacuum rest wavelength of the of the spectral feature of interest. The physical unit must be m.

One or the other of RESTFRQa or RESTWAVa should be given when it is meaningful to do so.

## 8.4.1. Spectral-coordinate reference frames

Frequencies, wavelengths, and apparent radial velocities are always referred to some selected standard of rest (i.e., reference frame). While the spectra are obtained they are, of necessity, in the observer’s rest frame. The velocity correction from topocentric (the frame in which the measurements are usually made) to standard reference frames (which must be one of those given in Table 27) are dependent on the dot product with time-variable velocity vectors. That is, the velocity with respect to a standard reference frame depends upon direction, and the velocity (and frequency and wavelength) with respect to the local standard of rest is a function of the celestial coordinate within the image. The keywords SPECSYSa and SSYSOBSa are reserved and, if used, must describe the reference frame in use for the spectralaxis coordinate(s) and the spectral reference frame that was held constant during the observation, respectively. In order to compute the velocities it is necessary to have the date and time of the observation; the keywords DATE-AVG and MJD-AVG are reserved for this purpose. See also Sect. 9.5.

DATE-AVG – [string; default: none]. Calendar date of the midpoint of the observation, expressed in the same way as the DATE-OBS keyword.

MJD-AVG – [floating point; default: none]. Modified Julian Date (JD − 2,400,000.5) of the mid-point of the observation.

SPECSYSa – [string; default: none]. The reference frame in use for the spectral-axis coordinate(s). Valid values are given in Table 27.

SSYSOBSa – [string; default: ’TOPOCENT’]. The spectral reference frame that is constant over the range of the non-spectral world coordinates. Valid values are given in Table 27.

The transformation from the rest frame of the observer to a standard reference frame requires a specification of the location on Earth<sup>14</sup> of the instrument used for the observation in order to

Table 26: Non-linear spectral algorithm codes.

| $Code^1$ | Regularly sampled in | Expressed as |
| --- | --- | --- |
| F2W | Frequency | Wavelength |
| F2V |  | Apparent radial velocity |
| F2A |  | Air wavelength |
| W2F | Wavelength | Frequency |
| W2V |  | Apparent radial velocity |
| W2A |  | Air wavelength |
| V2F | Apparent radial vel. | Frequency |
| V2W |  | Wavelength |
| V2A |  | Air wavelength |
| A2F | Air wavelength | Frequency |
| A2W |  | Wavelength |
| A2V |  | Apparent radial velocity |
| LOG | Logarithm | Any four-letter type code |
| GRI | Detector | Any type code from Table 25 |
| GRA | Detector | Any type code from Table 25 |
| TAB | Not regular | Any four-letter type code |

(1) Characters 6 through 8 of the value of the keyword CTYPEia.

calculate the diurnal Doppler correction due to the Earth’s rotation. The location, if specified, shall be represented as a geocentric Cartesian triple with respect to a standard ellipsoidal geoid at the time of the observation. While the position can often be specified with an accuracy of a meter or better, for most purposes positional errors of several kilometers will have negligible impact on the computed velocity correction. For details, see reference Greisen et al. (2006).

OBSGEO-X – [floating point; default: none]. X−coordinate (in meters) of a Cartesian triplet that specifies the location, with respect to a standard, geocentric terrestrial reference frame, where the observation took place. The coordinate must be valid at the epoch MJD-AVG or DATE-AVG.

OBSGEO-Y – [floating point; default: none]. Y−coordinate (in meters) of a Cartesian triplet that specifies the location, with respect to a standard, geocentric terrestrial reference frame, where the observation took place. The coordinate must be valid at the epoch MJD-AVG or DATE-AVG.

OBSGEO-Z – [floating point; default: none]. Z−coordinate (in meters) of a Cartesian triplet that specifies the location, with respect to a standard, geocentric terrestrial reference frame, where the observation took place. The coordinate must be valid at the epoch MJD-AVG or DATE-AVG.

Information on the relative radial velocity between the observer and the selected standard of rest in the direction of the celestial reference coordinate may be provided, and if so shall be given by the VELOSYSa keyword. The frame of rest defined with respect to the emitting source may be represented in FITS; for this reference frame it is necessary to define the velocity with respect to some other frame of rest. The keywords SPECSYSa and ZSOURCEa are used to document the choice of reference frame and the value of the systemic velocity of the source, respectively.

SSYSSRCa – [string; default: none]. Reference frame for the value expressed in the ZSOURCEa keyword to document the systemic velocity of the observed source. Value must be one of those given in Table 27 except for ’SOURCE’.

VELOSYSa – [floating point; default: none]. Relative radial velocity between the observer and the selected standard of rest

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">14 The specification of location for an instrument on a spacecraft in flight requires an ephemeris; keywords that might be required in this circumstance are not defined here.</span></small>

35

<!-- page 42 of 75 -->

Table 25: Reserved spectral-coordinate type codes.

| $\text {Code}^1$ | Type | Symbol | Associated variable | Default units |
| --- | --- | --- | --- | --- |
| FREQ | Frequency | ν | ν | Hz |
| ENER | Energy | E | ν | J |
| WAVN | Wavenumber | κ | ν | $m^{-1}$ |
| VRAD | Radio $velocity^2$ | V | ν | $m s^{-1}$ |
| WAVE | Vacuum wavelength | λ | λ | m |
| VOPT | Optical $velocity^2$ | Z | λ | $m s^{-1}$ |
| ZOPT | Redshift | z | λ | ... |
| AWAV | Air wavelength | $λ_a$ | $λ_a$ | m |
| VELO | Apparent radial velocity | ν | ν | $m s^{-1}$ |
| BETA | Beta factor (v/c) | β | ν | ... |

(1) Characters 1 through 4 of the value of the keyword CTYPEia.(<sup>2</sup>) By convention, the ‘radio’ velocity is given by $c ( \nu _ { 0 } - \nu ) / \nu _ { 0 }$ and the ‘optical’ velocity is given by $c ( \lambda - \lambda _ { 0 } ) / \lambda _ { 0 }$

Table 28: Example keyword records for a 100-element array of complex values.

Table 27: Spectral reference systems.

| Value | Definition |
| --- | --- |
| 'TOPOCENT' | Topocentric |
| 'GEOCENTR' | Geocentric |
| 'BARYCENT' | Barycentric |
| 'HELIOCEN' | Heliocentric |
| 'LSRK' | Local standard of rest (kinematic) |
| 'LSRD' | Local standard of rest (dynamic) |
| 'GALACTOC' | Galactocentric |
| 'LOCALGRP' | Local Group |
| 'CMBDIPOL' | Cosmic-microwave-background dipole |
| 'SOURCE' | Source rest frame |

Notes. These are the allowed values of the SPECSYSa, SSYSOBSa, and SSYSSRCa keywords.

in the direction of the celestial reference coordinate. Units must be m $\mathrm { s } ^ { - 1 }$ . The CUNITia keyword is not used for this purpose since the WCS Version a might not be expressed in velocity units.

ZSOURCEa – [floating point; default: none]. Radial velocity with respect to an alternative frame of rest, expressed as a unitless redshift (i.e., velocity as a fraction of the speed of light in vacuum). Used in conjunction with SSYSSRCa to document the systemic velocity of the observed source.

VELANGLa – [floating point; default:+90.]. In the case of relativistic velocities (e.g., a beamed astrophysical jet) the transverse velocity component is important. This keyword may be used to express the orientation of the space velocity vector with respect to the plane of the sky. See Appendix A of reference Greisen et al. (2006) for further details.

## 8.5. Conventional-coordinate types

The first FITS paper (Wells et al. 1981) listed a number of ‘suggested values’ for the CTYPEi keyword. Two of these have the attribute the associated world coordinates can assume only integer values and that the meaning of these integers is only defined by convention. The first ‘conventional’ coordinate is $\mathrm{CTYPE}_{i a} = \mathrm{COMPLEX}$ to specify that complex values (i.e., pairs of real and imaginary components) are stored in the data array (along with an optional weight factor). Thus, the complex axis of the data array will contain two values (or three if the weight is

<table><tr><td colspan="3">Keyword records</td></tr><tr><td>SIMPLE</td><td>=</td><td>T</td></tr><tr><td>BITPIX</td><td>=</td><td>-32</td></tr><tr><td>NAXIS</td><td>=</td><td>2</td></tr><tr><td>NAXIS1</td><td>=</td><td>2</td></tr><tr><td>NAXIS2</td><td>=</td><td>100</td></tr><tr><td>CTYPE1</td><td>= &#x27;COMPLEX&#x27;</td><td></td></tr><tr><td>CRVAL1</td><td>=</td><td>0.</td></tr><tr><td>CRPIX1</td><td>=</td><td>0.</td></tr><tr><td>CDELT1</td><td>=</td><td>1.</td></tr><tr><td>END</td><td></td><td></td></tr></table>

Table 29: Conventional Stokes values.

| Value | Symbol | Polarization |
| --- | --- | --- |
| 1 | 'I' | Standard Stokes unpolarized |
| 2 | 'Q' | Standard Stokes linear |
| 3 | 'U' | Standard Stokes linear |
| 4 | 'V' | Standard Stokes circular |
| -1 | 'RR' | Right-right circular |
| -2 | 'LL' | Left-left circular |
| -3 | 'RL' | Right-left cross-circular |
| -4 | 'LR' | Left-right cross-circular |
| -5 | 'XX' | X parallel linear |
| -6 | 'YY' | Y parallel linear |
| -7 | 'XY' | XY cross linear |
| -8 | 'YX' | YX cross linear |

specified). By convention, the real component has a coordinate value of 1, the imaginary component has a coordinate value of 2, and the weight, if any, has a coordinate value of 3. Table 28 illustrates the required keywords for an array of 100 complex values (without weights).

The second conventional coordinate is CTYPEia = ’STOKES’ to specify the polarization of the data. Conventional values, their symbols, and polarizations are given in Table 29.

## 9. Representations of time coordinates

Time as a dimension in astronomical data presents challenges for its representation in FITS files. This section formulates the representation of the time axis, or possibly multiple time axes,

36

<!-- page 43 of 75 -->

into the world-coordinate system (WCS) described in Sect. 8. Much of the basic structure is employed, while extensions are developed to cope with the differences between time and spatial dimensions; notable amongst these differences is the huge dynamic range, covering the highest resolution timing relative to the age of the universe.

The precision with which any time stamp conforms to any conventional time scale is highly dependent on the characteristics of the acquiring system. The definitions of many conventional time scales vary over their history along with the precision that can be attributed to any time stamp. The meaning of any time stamp may be ambiguous if a time scale is used for dates prior to its definition by a recognized authority, or for dates after that definition is abandoned. However, common sense should prevail: the precision in the description of the time coordinate should be appropriate to the accuracy of the temporal information in the data.

## 9.1. Time values

The three most common ways to specify time are: ISO-8601 (ISO 2004b), Julian Date (JD), or Modified Julian Date (MJD = JD − 2, 400, 000.5; see IAU 1997). Julian Dates are counted from Julian proleptic calendar date 1 January 4713 BCE at noon, or Gregorian proleptic calendar date 24 November 4714 BCE, also at noon. For an explanation of the calendars, see Rots et al. (2015). Even though it is common to think of certain representations of time as absolute, time values in FITS files shall all be considered relative: elapsed time since a particular reference point in time. It may help to view the “absolute” values as merely relative to a globally accepted zero point. For a discussion of the precision required to represent time values in floating-point numbers, see Rots et al. (2015).

## 9.1.1. ISO-8601 datetime strings

FITS datetime strings conform to a subset of ISO-8601 (which in itself does not imply a particular time scale) for several timerelated keywords (Bunclark & Rots 1997), such as DATE-xxxx. Here datetime will be used as a pseudo data type to indicate its use, although its values must be written as a character string in’A’ format. The full specification for the format of the datetime string has been:

$$
\text {CCYY - MM - DD} [ \text {Thh:mm:ss[.s...]} ]
$$

in which all of the time part may be omitted (just leaving the date) or the decimal seconds may be omitted. Leading zeros must not be omitted and timezone designators are not allowed. This definition is extended to allow five-digit years with a mandatory sign, in accordance with ISO-8601. That is, one shall use either the unsigned four-digit year format, or the signed fivedigit year format shown below.

$$
[ \pm C ] C C Y Y - M M - D D [ T h h: m m: s s [. s \dots ] ]
$$

Note the following.

– In counting years, ISO-8601 follows the convention of including Year Zero. Consequently, for negative year numbers there is an offset of one from BCE dates, which do not recognize a Year Zero. Thus Year 1 corresponds to 1 CE, Year 0 to 1 BCE, Year −1 to 2 BCE, and so on.

– The earliest date that may be represented in the four-digit year format is ’0000-01-01T00:00:00’ (in the year 1 BCE); the latest date is ’9999-12-31T23:59:59’. This representation of time is tied to the Gregorian calendar. In conformance with the present ISO-8601:2004(E) standard (ISO 2004b) dates prior to 1582 must be interpreted according to the proleptic application of the rules of Gregorius XIII. For dates not covered by that range the use of Modified Julian Date (MJD) or Julian Date (JD) numbers or the use of the signed five-digit year format is recommended.

– In the five-digit year format the earliest and latest dates are’-99999-01-01T00:00:00’ (i.e., −100 000 BCE) and’+99999-12-31T23:59:59’.

– The origin of JD can be written as:

’-04713-11-24T12:00:00’.

– In the UTC time scale the integer part of the seconds field runs from 00 to 60 (in order to accommodate leap seconds); in all other time scales the range is 00 to 59.

– The ISO-8601 datetime data type is not allowed in imageaxis descriptions since CRVAL is required to be a floatingpoint value.

– ISO-8601 datetime does not imply the use of any particular time scale (see Sect. 9.2.1).

– As specified by Bunclark & Rots (1997), time zones are explicitly not supported in FITS and, consequently, appending the letter ’Z’ to a FITS ISO-8601 string is not allowed. The rationale for this rule is that its role in the ISO standard is that of a time-zone indicator, not a time-scale indicator. As the concept of a time zone is not supported in FITS, the use of time-zone indicator is inappropriate.

## 9.1.2. Julian and Besselian epochs

In a variety of contexts epochs are provided with astronomical data. Until 1976 these were commonly based on the Besselian year (see Sect. 9.3), with standard epochs B1900.0 and B1950.0. After 1976 the transition was made to Julian epochs based on the Julian year of 365.25 days, with the standard epoch J2000.0. They are tied to the ET and TDB time scales, respectively. Note that the Besselian epochs are scaled by the variable length of the Besselian year (see Sect. 9.3 and its cautionary note, which also applies to this context). The Julian epochs are easier to calculate, as long as one keeps track of leap days.

## 9.2. Time coordinate frame

## 9.2.1. Time scale

The time scale defines the temporal reference frame, and is specified in the header in one of a few ways, depending upon the context. When recorded as a global keyword, the time scale shall be specified by the following keyword.

TIMESYS – [string; default: ’UTC’]. The value field of this keyword shall contain a character-string code for the time scale of the time-related keywords. The recommended values for this keyword in Table 30 have well-defined meanings, but other values may be used. If this keyword is absent, ’UTC’ must be assumed.

In relevant contexts (e.g., time axes in image arrays, table columns, or random groups) TIMESYS may be overridden by a

37

<!-- page 44 of 75 -->

time scale recorded in CTYPEia, its binary-table equivalents, or PTYPEi (see Table 22).

The keywords TIMESYS, CTYPEia, TCTYPn, and TCTYna or binary-table equivalent may assume the values listed in Table 30. In addition, for backward compatibility, all except TIMESYS and PTYPEi may also assume the value ’TIME’ (case-insensitive), whereupon the time scale shall be that recorded in TIMESYS or, in its absence, its default value, ’UTC’. As noted above, local time scales other than those listed in Table 30 may be used, but their use should be restricted to alternate coordinates in order that the primary coordinates will always refer to a properly recognized time scale.

See Rots et al. (2015), Appendix A, for a detailed discussion of the various time scales. In cases where high-precision timing is important one may append a specific realization, in parentheses, to the values in the table; e.g., ’TT(TAI)’, ’TT(BIPM08)’,’UTC(NIST)’. Note that linearity is not preserved across all time scales. Specifically, if the reference position remains unchanged (see Sect. 9.2.3), the first ten, with the exception of’UT1’, are linear transformations of each other (excepting leap seconds), as are ’TDB’ and ’TCB’. On average $\mathbf { \partial } ^ { 2 } \mathbf { T } \mathbf { C } \mathbf { B } ^ { \prime }$ runs faster than ’TCG’ by approximately $1 . 6 \times 1 0 ^ { - 8 } ]$ but the transformation from ’TT’ or ’TCG’ (which are linearly related) is to be achieved through a time ephemeris as provided by Irwin & Fukushima (1999).

The relations between coordinate time scales and their dynamical equivalents have been defined as:

$$
T (\mathrm{TCG}) = T (\mathrm{TT}) + L _ {\mathrm{G}} \times 8 6 4 0 0 \times (J D (\mathrm{TT}) - J D _ {0})
$$

$$
T (\mathrm{TDB}) = T (\mathrm{TCB}) - L _ {\mathrm{B}} \times 8 6 4 0 0 \times (J D (\mathrm{TCB}) - J D _ {0}) + T D B _ {0},
$$

where:

T is in seconds

$$
L _ {\mathrm{G}} = 6. 9 6 9 2 9 0 1 3 4 \times 1 0 ^ {- 1 0}
$$

$$
L _ {\mathrm{B}} = 1. 5 5 0 5 1 9 7 6 8 \times 1 0 ^ {- 8}
$$

$$
J D _ {0} = 2 4 4 3 1 4 4. 5 0 0 3 7 2 5
$$

$$
T D B _ {0} = - 6. 5 5 \times 1 0 ^ {- 5} \mathrm{s}.
$$

Linearity is virtually guaranteed since images and individual table columns do not allow more than one reference position to be associated with them, and since there is no overlap between reference positions that are meaningful for the first nine time scales on the one hand, and for the barycentric ones on the other. All use of the GMT time scale in FITS files shall be taken to have its zero point at midnight, conformant with UT, including dates prior to 1925. For high-precision timing prior to 1972, see Rots et al. (2015), Appendix A.

Some time scales in use are not listed in Table 30 because they are intrinsically unreliable or ill-defined. When used, they should be tied to one of the existing scales with appropriate specification of the uncertainties; the same is true for free-running clocks. However, a local time scale such as MET (Mission Elapsed Time) or OET (Observation Elapsed Time) may be defined for practical reasons. In those cases the time reference value (see Sect. 9.2.2) shall not be applied to the values, and it is strongly recommended that such time scales be provided as alternate time scales, with a defined conversion to a recognized time scale.

It is useful to note that while UT1 is, in essence, an angle (of the Earth’s rotation – i.e., a clock), the others are SI-second counters (chronometers); UTC, by employing leap seconds, serves as a bridge between the two types of time scales.

Table 30: Recognized Time Scale Values

| Value | Meaning |
| --- | --- |
| 'TAI' | (International Atomic Time): atomic-time standard maintained on the rotating geoid |
| 'TT' | (Terrestrial Time; IAU standard): defined on the rotating geoid, usually derived as TAI + 32.184 s |
| 'TDT' | (Terrestrial Dynamical Time): synonym for TT (deprecated) |
| 'ET' | (Ephemeris Time): continuous with TT; should not be used for data taken after 1984-01-01 |
| 'IAT' | synonym for TAI (deprecated) |
| 'UT1' | (Universal Time): Earth rotation time |
| 'UTC' | (Universal Time, Coordinated; default): runs synchronously with TAI, except for the occasional insertion of leap seconds intended to keep UTC within 0.9 s of UT1; as of 2015-07-01 UTC = TAI - 36 s |
| 'GMT' | (Greenwich Mean Time): continuous with UTC; its use is deprecated for dates after 1972-01-01 |
| $UT()^1$ | (Universal Time, with qualifier): for high-precision use of radio-signal distributions between 1955 and 1972; see Rots et al. (2015), Appendix A |
| 'GPS' | (Global Positioning System): runs (approximately) synchronously with TAI; GPS ≈ TAI - 19 s |
| 'TCG' | (Geocentric Coordinate Time): TT reduced to the geocenter, corrected for the relativistic effects of the Earth's rotation and gravitational potential; TCG runs faster than TT at a constant rate |
| 'TCB' | (Barycentric Coordinate Time): derived from TCG by a four-dimensional transformation, taking into account the relativistic effects of the gravitational potential at the barycenter (relative to that on the rotating geoid) as well as velocity time-dilation variations due to the eccentricity of the Earth's orbit, thus ensuring consistency with fundamental physical constants; Irwin &amp; Fukushima (1999) provide a time ephemeris |
| 'TDB' | (Barycentric Dynamical Time): runs slower than TCB at a constant rate so as to remain approximately in step with TT; runs therefore quasi-synchronously with TT, except for the relativistic effects introduced by variations in the Earth's velocity relative to the barycenter. When referring to celestial observations, a pathlength correction to the barycenter may be needed, which requires the Time Reference Direction used in calculating the pathlength correction. |
| 'LOCAL' | for simulation data and for free-running clocks. |

<sup>1</sup>Specific realization codes may be appended to these values, in parentheses; see the text. For a more-detailed discussion of time scales, see Rots et al. (2015), Appendix A.

## 9.2.2. Time reference value

The time reference value is not required to be present in an HDU. However, if the time reference point is specified explicitly it must be expressed in one of ISO-8601, JD, or MJD. These reference values must only be applied to time values associated with one of the recognized time scales listed in Table 30, and that time scale must be specified explicitly or implicitly as explained in Sect. 9.2.1.

The reference point in time, to which all times in the HDU are relative, shall be specified through one of three keywords specified below.

38

<!-- page 45 of 75 -->

MJDREF – [floating-point]; default: 0.0] The value field of this keyword shall contain the value of the reference time in MJD.

JDREF – [floating-point; default: none] The value field of this keyword shall contain the value of the reference time in JD.

DATEREF – [datetime; default: none] The value field of this keyword shall contain a character-string representation of the reference time in ISO-8601 format.

MJDREF and JDREF may, for clarity or precision reasons, be split into two keywords holding the integer and fractional parts separately.

MJDREFI – [integer; default: 0] The value field of this keyword shall contain the integer part of reference time in MJD.

MJDREFF – [floating-point; default: 0.0] The value field of this keyword shall contain the fractional part of reference time in MJD.

JDREFI – [integer; default: none] The value field of this keyword shall contain the integer part of reference time in JD.

JDREFF – [floating-point; default: none] The value field of this keyword shall contain the fractional part of reference time in JD.

If [M]JDREF and both [M]JDREFI and [M]JDREFF are present, the integer and fractional values shall have precedence over the single value. If the single value is present with one of the two parts, the single value shall have precedence. In the following, MJDREF and JDREF refer to their literal meaning or the combination of their integer and fractional parts. If a header contains more than one of these keywords, JDREF shall have precedence over DATEREF and MJDREF shall have precedence over both the others. If none of the three keywords is present, there is no problem as long as all times in the HDU are expressed in ISO-8601; otherwise MJDREF = 0.0 must be assumed. If TREFPOS = ’CUSTOM’ (Sect. 9.2.3), it is legitimate for none of the reference-time keywords to be present, as one may assume the data are from a simulation. Note that the value of the reference time has global validity for all time values, but it does not have a particular time scale associated with it.

## 9.2.3. Time reference position

An observation is an event in space-time. The reference position specifies the spatial location at which the time is valid, either where the observation was made or the point in space for which light-time corrections have been applied. When recorded as a global keyword, the time reference position shall be specified by the following keyword.

TREFPOS – [string; default: ’TOPOCENTER’]. The value field of this keyword shall contain a character-string code for the spatial location at which the observation time is valid. The value should be one of those given in Table 31. This keyword shall apply to time-coordinate axes in images as well.

In binary tables, different columns may represent completely different Time Coordinate Frames. However, each column can have only one time reference position, thus guaranteeing linearity (see Sect. 9.2.1).

TRPOSn – [string; default: ’TOPOCENTER’] The value field of this keyword shall contain a character-string code for the spatial location at which the observation time is valid. This table keyword shall override TREFPOS.

The reference position value may be a standard location (such as ’GEOCENTER’ or ’TOPOCENTER’) or a point in space defined by specific coordinates. In the latter case one should be aware that a (three-dimensional) spatial-coordinate frame needs to be defined that is likely to be different from the frame(s) with which the data are associated. Note that ’TOPOCENTER’ is only moderately informative if no observatory location is provided or indicated. The commonly allowed standard values are shown in Table 31. Note that for the gaseous planets the barycenters of their planetary systems, including satellites, are used for obvious reasons. While it is preferable to spell the location names out in full, in order to be consistent with the practice of Greisen et al. (2006) the values are allowed to be truncated to eight characters. Furthermore, in order to allow for alternative spellings, only the first three characters of all these values shall be considered significant. The value of the keyword shall be case-sensitive.

Table 31: Standard Time Reference Position Values

<table><tr><td> $Value^1$ </td><td>Meaning</td></tr><tr><td>&#x27;TOPOCENTER&#x27;</td><td>Topocenter: the location from where the observation was made (default)</td></tr><tr><td>&#x27;GEOCENTER&#x27;</td><td>Geocenter</td></tr><tr><td>&#x27;BARYCENTER&#x27;</td><td>Barycenter of the Solar System</td></tr><tr><td>&#x27;RELOCATABLE&#x27;</td><td>Relocatable: to be used for simulation data only</td></tr><tr><td>&#x27;CUSTOM&#x27;</td><td>A position specified by coordinates that is not the observatory location</td></tr><tr><td colspan="2">Less-common, but allowed standard values</td></tr><tr><td>&#x27;HELIOCENTER&#x27;</td><td>Heliocenter</td></tr><tr><td>&#x27;GALACTIC&#x27;</td><td>Galactic center</td></tr><tr><td>&#x27;EMBARYCENTER&#x27;</td><td>Earth-Moon barycenter</td></tr><tr><td>&#x27;MERCURY&#x27;</td><td>Center of Mercury</td></tr><tr><td>&#x27;VENUS&#x27;</td><td>Center of Venus</td></tr><tr><td>&#x27;MARS&#x27;</td><td>Center of Mars</td></tr><tr><td>&#x27;JUPITER&#x27;</td><td>Barycenter of the Jupiter system</td></tr><tr><td>&#x27;SATURN&#x27;</td><td>Barycenter of the Saturn system</td></tr><tr><td>&#x27;URANUS&#x27;</td><td>Barycenter of the Uranus system</td></tr><tr><td>&#x27;NEPTUNE&#x27;</td><td>Barycenter of the Neptune system</td></tr></table>

**Notes.** (<sup>1</sup>)Recognized values for TREFPOS, TRPOSn; only the first three characters of the values are significant and Solar System locations are as specified in the ephemerides.

The reader is cautioned that time scales and reference positions cannot be combined arbitrarily if one wants a clock that runs linearly at TREFPOS. Table 32 provides a summary of compatible combinations. ’BARYCENTER’ should only be used in conjunction with time scales ’TDB’ and ’TCB’, and should be the only reference position used with these time scales. With proper care ’GEOCENTER’, ’TOPOCENTER’, and’EMBARYCENTER’ are appropriate for the first ten time scales in Table 30. However, relativistic effects introduce a (generally linear) scaling in certain combinations; highly eccentric spacecraft orbits are the exceptions. Problems will arise when using a reference position on another Solar System body (including’HELIOCENTER’). Therefore, it is recommended to synchronize

39

<!-- page 46 of 75 -->

Table 32: Compatibility of Time Scales and Reference Positions

<table><tr><td rowspan="2">Reference Position</td><td colspan="5">Time scale $^{1}$ </td></tr><tr><td>TT, TDT TAI, IAT GPS UTC, GMT</td><td>TCG</td><td>TDB</td><td>TCB</td><td>LOCAL</td></tr><tr><td>&#x27;TOPOCENTER&#x27;</td><td>t</td><td>ls</td><td></td><td></td><td></td></tr><tr><td>&#x27;GEOCENTER&#x27;</td><td>ls</td><td>c</td><td></td><td></td><td></td></tr><tr><td>&#x27;BARYCENTER&#x27;</td><td></td><td></td><td>ls</td><td>c</td><td></td></tr><tr><td>&#x27;RELOCATABLE&#x27;</td><td></td><td></td><td></td><td></td><td>c</td></tr><tr><td>Other $^{2}$ </td><td>re</td><td>re</td><td></td><td></td><td></td></tr></table>

**Notes.** (<sup>1</sup>)Legend (combination is not recommended if there is no entry); c: correct match; reference position coincides with the spatial origin of the space-time coordinates; t: correct match on Earth’s surface, otherwise usually linear scaling; **ls**: linear relativistic scaling; **re**: non-linear relativistic scaling. (<sup>2</sup>)All other locations in the Solar System.

the local clock with one of the time scales defined on the Earth’s surface, $\text{" } TT  \text{" , }  \text{" } TA  \text{" , }  \text{" } GPS  \text{" , or }  \text{" } UTC  \text{" }$ (in the last case: beware of leap seconds). This is common practice for spacecraft clocks. Locally, such a clock will not appear to run at a constant rate, because of variations in the gravitational potential and in motions with respect to Earth, but the effects can be calculated and are probably small compared with errors introduced by the alternative: establishing a local time standard.

In order to provide a complete description, ’TOPOCENTER’ requires the observatory’s coordinates to be specified. There are three options: (a) the ITRS Cartesian coordinates defined in Sect. 8.4.1 (OBSGEO-X, OBSGEO-Y, OBSGEO-Z), which are strongly preferred; (b) a geodetic latitude/longitude/elevation triplet (defined below); or (c) a reference to an orbit-ephemeris file. A set of geodetic coordinates is recognized by the following keywords.

OBSGEO-B – [floating-point] The value field of this keyword shall contain the latitude of the observation in deg, with North positive.

OBSGEO-L – [floating-point] The value field of this keyword shall contain the longitude of the observation in deg, with East positive.

OBSGEO-H – [floating-point] The value field of this keyword shall contain the altitude of the observation in meters.

An orbital-ephemeris file can instead be specified.

OBSORBIT – [string] The value field of this keyword shall contain the character-string URI, URL, or the name of an orbitephemeris file.

Beware that only one set of coordinates is allowed in a given HDU. Cartesian ITRS coordinates are the preferred coordinate system; however, when using these in an environment requiring nanosecond accuracy, one should take care to distinguish between meters consistent with TCG or with TT. If one uses geodetic coordinates, the geodetic altitude OBSGEO-H is measured with respect to the IAU 1976 ellipsoid, which is defined as having a semi-major axis of 6 378 140 m and an inverse flattening of 298.2577.

A non-standard location indicated by ’CUSTOM’ must be specified in a manner similar to the specification of the observatory location (indicated by ’TOPOCENTER’). One should be

careful with the use of the ’CUSTOM’ value and not confuse it with ’TOPOCENTER’, as use of the latter imparts additional information on the provenance of the data.

ITRS coordinates $( X { , } Y { , } Z )$ may be derived from geodetic co-ordinates $( L { , } B { , } H )$ through:

$$
X = (N (B) + H) \cos (L) \cos (B)
$$

$$
Y = (N (B) + H) \sin (L) \cos (B)
$$

$$
Z = (N (B) (1 - e ^ {2}) + H) \sin (B)
$$

where:

$$
N (B) = \frac {a}{\sqrt {1 - e ^ {2} \sin^ {2} (B)}}
$$

$$
e ^ {2} = 2 f - f ^ {2}
$$

a is the semi-major axis, and f is the inverse of the inverse flattening. Nanosecond precision in timing requires that OBSGEO-[BLH] be expressed in a geodetic reference frame defined after 1984 in order to be sufficiently accurate.

## 9.2.4. Time reference direction

If any pathlength corrections have been applied to the time stamps (i.e., if the reference position is not ’TOPOCENTER’ for observational data), the reference direction that is used in calculating the pathlength delay should be provided in order to maintain a proper analysis trail of the data. However, this is useful only if there is also information available on the location from where the observation was made (the observatory location). The direction will usually be provided in a spatial-coordinate frame that is already being used for the spatial metadata, although it is conceivable that multiple spatial frames are involved, e.g., spherical ICRS coordinates for celestial positions, and Cartesian FK5 for spacecraft ephemeris. The time reference direction does not by itself provide sufficient information to perform a fully correct transformation; however, within the context of a specific analysis environment it should suffice.

The uncertainty in the reference direction affects the errors in the time stamps. A typical example is provided by barycentric corrections where the time error is related to the position error:

$$
t _ {\mathrm{err}} (\mathrm{ms}) \leq 2. 4 p o s _ {\mathrm{err}} (\mathrm{arcsec}).
$$

The reference direction is indicated through a reference to specific keywords. These keywords may hold the reference direction explicitly or (for data in BINTABLE extensions) indicate columns holding the coordinates. In event lists where the individual photons are tagged with a spatial position, those coordinates may have been used for the reference direction and the reference will point to the columns containing these coordinate values. The time reference direction shall be specified by the following keyword.

TREFDIR – [string] The value field of this keyword shall contain a character string composed of: the name of the keyword containing the longitudinal coordinate, followed by a comma, followed by the name of the keyword containing the latitudinal coordinate. This reference direction shall apply to time-coordinate axes in images as well.

40

<!-- page 47 of 75 -->

In binary tables, different columns may represent completely different Time Coordinate Frames. However, also in that situation the condition holds that each column can have only one Time Reference Direction. Hence, the following keyword may override TREFDIR.

TRDIRn – [string] The value field of this keyword shall contain a character string consisting of the name of the keyword or column containing the longitudinal coordinate, followed by a comma, followed by the name of the keyword or column containing the latitudinal coordinate. This reference direction shall apply to time-coordinate axes in images as well.

## 9.2.5. Solar System ephemeris

If applicable, the Solar System ephemeris used for calculating pathlength delays should be identified. This is particularly pertinent when the time scale is ’TCB’ or ’TDB’. The ephemerides that are currently most often used are those from JPL (2014a,b).

The Solar System ephemeris used for the data (if required) shall be indicated by the following keyword.

PLEPHEM – [string; default: ’DE405’] The value field of this keyword shall contain a character string that should represent a recognized designation for the Solar System ephemeris. Recognized designations for JPL Solar System ephemerides that are often used are listed in Table 33.

Table 33: Valid Solar System ephemerides

| Value | Reference |
| --- | --- |
| 'DE200' | Standish (1990); considered obsolete, but still in use |
| 'DE405' | Standish (1998); default |
| 'DE421' | Folkner, et al. (2009) |
| 'DE430' | Folkner, et al. (2014) |
| 'DE431' | Folkner, et al. (2014) |
| 'DE432' | Folkner, et al. (2014) |

Future ephemerides in this series shall be accepted and recognized as they are released. Additional ephemerides designations may be recognized by the IAUFWG upon request.

## 9.3. Time unit

When recorded as a global keyword, the unit used to express time shall be specified by the following keyword.

TIMEUNIT – [string; default: ’s’] The value field of this keyword shall contain a character string that specifies the time unit; the value should be one of those given in Table 34. This time unit shall apply to all time instances and durations that do not have an implied time unit (such as is the case for JD, MJD, ISO-8601, J and B epochs). If this keyword is absent, $\mathbf { \nabla } _ { \mathbf { S } } \mathbf { \nabla } ^ { \prime }$ shall be assumed.

In an appropriate context, e.g., when an image has a time axis, TIMEUNIT may be overridden by the CUNITia keywords and their binary-table equivalents (see Table 22).

The specification of the time unit allows the values defined in Greisen & Calabretta (2002), shown in Table 34, with the addition of the century. See also Sect. 4.3 for generalities about units.

Table 34: Recommended time units

<table><tr><td>Value</td><td>Definition</td></tr><tr><td>&#x27;s&#x27;</td><td>second (default)</td></tr><tr><td>&#x27;d&#x27;</td><td>day (= 86,400 s)</td></tr><tr><td>&#x27;a&#x27;</td><td>(Julian) year (= 365.25 d)</td></tr><tr><td>&#x27;cy&#x27;</td><td>(Julian) century (= 100 a)</td></tr><tr><td colspan="2">The following values are also acceptable.</td></tr><tr><td>&#x27;min&#x27;</td><td>minute (= 60 s)</td></tr><tr><td>&#x27;h&#x27;</td><td>day (= 86,400 s)</td></tr><tr><td>&#x27;yr&#x27;</td><td>(Julian) year (= &#x27;a&#x27; = 365.25 d)</td></tr><tr><td>&#x27;ta&#x27;</td><td>tropical year</td></tr><tr><td>&#x27;Ba&#x27;</td><td>Besselian year</td></tr></table>

The use of ’ta’ and ’Ba’ is not encouraged, but there are data and applications that require the use of tropical years or Besselian epochs (see Sect. 9.1.2). The length of the tropical year, ’ta’, in days is:

$$
\begin{array}{r l} 1 \text {ta} = & 3 6 5. 2 4 2 1 9 0 4 0 2 1 1 2 3 6 - 0. 0 0 0 0 0 6 1 5 2 5 1 3 4 9 T \\ & - 6. 0 9 2 1 \times 1 0 ^ {- 1 0} T ^ {2} + 2. 6 5 2 5 \times 1 0 ^ {- 1 0} T ^ {3} (\mathrm{d}) \end{array}
$$

where T is in Julian centuries since J2000, using time scale TDB. The length of the Besselian year in days is:

$$
1 \mathrm{Ba} = 3 6 5. 2 4 2 1 9 8 7 8 1 7 - 0. 0 0 0 0 0 7 8 5 4 2 3 T (\mathrm{d})
$$

where T is in Julian centuries since J1900, using time scale ET, although for these purposes the difference with TDB is negligible.

Readers are cautioned that the subject of tropical and Besselian years presents a particular quandary for the specification of standards. The expressions presented here are the most accurate available, but are applicable for use when creating data files (which is strongly discouraged), rather than for interpreting existing data that are based upon these units. However, there is no guarantee that the authors of the data applied these particular definitions. Users are therefore advised to pay close attention and attempt to ascertain what the authors of the data really used.

## 9.4. Time offset, binning, and errors

## 9.4.1. Time offset

A uniform clock correction may be applied in bulk with the following single keyword.

TIMEOFFS – [floating-point; default: 0.0] The value field of this keyword shall contain the value of the offset in time that shall be added to the reference time, given by one of: MJDREF, JDREF, or DATEREF.

The time offset may serve to set a zero-point offset to a relative time series, allowing zero-relative times, or just higher pre-cision, in the time stamps. Its default value is zero. The value of this keyword affects the values of TSTART, and TSTOP, as well as any time pixel values in a binary table. However, this construct may only be used in tables and must not be used in images.

41

<!-- page 48 of 75 -->

## 9.4.2. Time resolution and binning

The resolution of the time stamps (the width of the time sampling function) shall be specified by the following keyword.

TIMEDEL – [floating-point] The value field of this keyword shall contain the value of the time resolution in the units of TIMEUNIT. This construct, when present, shall only be used in tables and must not be used in images.

In tables this may, for instance, be the size of the bins for timeseries data or the bit precision of the time-stamp values.

When data are binned in time bins (or, as a special case, events are tagged with a time stamp of finite precision) it is important to know to the position within the bin (or pixel) to which the time stamp refers. Coordinate values normally correspond to the center of all pixels (see Sect. 8.2); yet clock readings are effectively truncations, not rounded values, and therefore correspond to the lower bound of the pixel.

TIMEPIXR – [floating-point; default: 0.5] The value field of this keyword shall contain the value of the position within the pixel, from 0.0 to 1.0, to which the time-stamp refers. This construct, when present, shall only be used in tables and must not be used in images.

A value of 0.0 may be more common in certain contexts, e.g. when truncated clock readings are recorded, as is the case for almost all event lists.

## 9.4.3. Time errors

The absolute time error is the equivalent of a systematic error, shall be given by the following keyword.

TIMSYER – [floating-point; default: 0.] The value field of this keyword shall contain the value of the absolute time error, in units of TIMESYS.

This keyword may be overridden, in appropriate context (e.g., time axes in image arrays or table columns; by the CSYERia keywords and their binary-table equivalents (see Table 22).

The relative time error specifies accuracy of the time stamps relative to each other. This error will usually be much smaller than the absolute time error. This error is equivalent to a random error, and shall be given by the following keyword.

TIMRDER – [floating-point; default: 0.] The value field of this keyword shall contain the value of the relative time error, i.e. the random error between time stamps, in units of TIMESYS.

This keyword may be overridden, in appropriate context (e.g., time axes in image arrays or table columns; by the CRDERia keywords and their binary-table equivalents (see Table 22).

## 9.5. Global time keywords

The time keywords in Table 35 are likely to occur in headers even when there are no time axes in the data. Except for DATE, they provide the top-level temporal bounds of the data in the HDU. As noted before, they may also be implemented as table columns. Keywords not previously described are defined below; all are included in the summary Table 22.

Table 35: Keywords for global time values

| Keyword | Notes |
| --- | --- |
| DATE | Defined in Sect. 4.4.2. |
| DATE-OBS | Defined in Sect. 4.4.2. Keyword value was not restricted to mean the start time of an observation, and has historically also been used to indicate some form of mean observing date and time. To avoid ambiguity use DATE-BEG instead. |
| DATE-BEG | Defined in this section. |
| DATE-AVG | Defined in Sect. 8.4.1. The method by which average times should be calculated is not defined by this Standard. |
| DATE-END | Defined in this section. |
| MJD-OBS | Defined in Sect. 8.3. |
| MJD-BEG | Defined in this section. |
| MJD-AVG | Defined in Sect. 8.4.1. The method by which average times should be calculated is not defined by this Standard. |
| MJD-END | Defined in this section. |
| TSTART | Defined in this section. |
| TSTOP | Defined in this section. |

DATE-BEG – [datetime] The value field of this keyword shall contain a character string in ISO-8601 format that specifies the start time of data acquisition in the time system specified by the TIMESYS keyword.

DATE-END – [datetime] The value field of this keyword shall contain a character string in ISO-8601 format that specifies the stop time of data acquisition in the time system specified by the TIMESYS keyword.

MJD-BEG – [floating-point] The value field of this keyword shall contain the value of the MJD start time of data acquisition in the time system specified by the TIMESYS keyword.

MJD-END – [floating-point] The value field of this keyword shall contain the value of the MJD stop time of data acquisition in the time system specified by the TIMESYS keyword.

TSTART – [floating-point] The value field of this keyword shall contain the value of the start time of data acquisition in units of TIMEUNIT, relative to MJDREF, JDREF, or DATEREF and TIMEOFFS, in the time system specified by the TIMESYS keyword.

TSTOP – [floating-point] The value field of this keyword shall contain the value of the stop time of data acquisition in units of TIMEUNIT, relative to MJDREF, JDREF, or DATEREF and TIMEOFFS, in the time system specified by the TIMESYS keyword.

The alternate-axis equivalent keywords for BINTABLE extensions, DOBSn, MJDOBn, DAVGn, and MJDAn, as defined in Table 22, are also allowed. Note that of the above only TSTART and TSTOP are relative to the time reference value. As in the case of the time reference value (see Sect. 9.2.2), the JD values supersede DATE values, and MJD values supersede both, in cases where conflicting values are present.

It should be noted that, although they do not represent global time values within an HDU, the CRVALia and CDELTia keywords, and their binary-table equivalents (see Table 22), also represent (binary) time values. They should be handled with the same care regarding precision when combining them with the time reference value, as any other time value.

42

<!-- page 49 of 75 -->

Finally, Julian and Besselian epochs (see Sects. 9.1.2 and 9.3) may be expressed by these two keywords – to be used with great caution, as their definitions are more complicated and hence their use more prone to confusion.

JEPOCH – [floating-point] The value field of this keyword shall contain the value of the Julian epoch, with an implied time scale of ’TDB’.

BEPOCH – [floating-point] The value field of this keyword shall contain the value of the Besselian epoch, with an implied time scale of ’ET’.

When these epochs are used as time stamps in a table column, their interpretation will be clear from the context. When the keywords appear in the header without obvious context, they must be regarded as equivalents of DATE-OBS and MJD-OBS, i.e., with no fixed definition as to what part of the dataset they refer.

## 9.6. Other time-coordinate axes

There are a few coordinate axes that are related to time and that are accommodated in this Standard: (temporal) phase, timelag, and frequency. Phase results from folding a time series on a given period, and can appear in parallel with time as an alternate description of the same axis. Timelag is the coordinate of cross- and auto-correlation spectra. The temporal frequency is the Fourier transform equivalent of time and, particularly, the coordinate axis of power spectra; spectra where the dependent variable is the electromagnetic field are excluded here, but see Greisen et al. (2006). These coordinate axes shall be specified by giving CTYPEi and its binary-table equivalents one of the values: ’PHASE’, ’TIMELAG’, or ’FREQUENCY’.

Timelag units are the regular time units, and the basic unit for frequency is ’Hz’. Neither of these two coordinates is a linear or scaled transformation of time, and therefore cannot appear in parallel with time as an alternate description. That is, a given vector of values for an observable can be paired with a coordinate vector of time, or timelag, or frequency, but not with more than one of these; the three coordinates are orthogonal.

Phase can appear in parallel with time as an alternate description of the same axis. Phase shall be recorded in the following keywords.

CZPHSia – [floating-point] The value field of this keyword shall contain the value of the time at the zero point of a phase axis. Its units may be ’deg’, ’rad’, or ’turn’.

CPERIia – [floating-point] The value field of this keyword, if present shall contain the value of the period of a phase axis. This keyword can be used only if the period is a constant; if that is not the case, this keyword should either be absent or set to zero.

CZPHSia may instead appear in binary-table forms TCZPHn, TCZPna, iCZPHn, and iCZPna. CPERIia may instead appear in binary-table forms TCPERn, TCPRna, iCPERn, and iCPRna. The phase, period, and zero point shall be expressed in the globally valid time reference frame and unit as defined by the global keywords (or their defaults) in the header.

## 9.7. Durations

There is an extensive collection of header keywords that indicate time durations, such as exposure times, but there are many

pitfalls and subtleties that make this seemingly simple concept treacherous. Because of their crucial role and common use, keywords are defined below to record exposure and elapsed time.

XPOSURE – [floating-point] The value field of this keyword shall contain the value for the effective exposure duration for the data, corrected for dead time and lost time in the units of TIMEUNIT. If the HDU contains multiple time slices, this value shall be the total accumulated exposure time over all slices.

TELAPSE – [floating-point] The value field of this keyword shall contain the value for the amount of time elapsed, in the units of TIMEUNIT, between the start and the end of the observation or data stream.

Durations must not be expressed in ISO-8601 format, but only as actual durations (i.e., numerical values) in the units of the specified time unit.

Good-Time-Interval (GTI) tables are common for exposures with gaps in them, particularly photon-event files, as they make it possible to distinguish time intervals with “no signal detected” from “no data taken.” GTI tables in BINTABLE extensions must contain two mandatory columns, START and STOP, and may contain one optional column, WEIGHT. The first two define the interval, the third, with a value between 0 and 1, the quality of the interval; i.e., a weight of 0 indicates a Bad-Time-Interval. WEIGHT has a default value of 1. Any time interval not covered in the table shall be considered to have a weight of zero.

## 9.8. Recommended best practices

The following guidelines should be helpful in creating data products with a complete and correct time representation.

– The presence of the informational DATE keyword is strongly recommended in all HDUs.

– One or more of the informational keywords DATE-xxxx and/or MJD-xxxx should be present in all HDUs whenever a meaningful value can be determined. This also applies, e.g., to catalogs derived from data collected over a well-defined time range.

– The global keyword TIMESYS is strongly recommended.

– The global keywords MJDREF or JDREF or DATEREF are recommended.

– The remaining informational and global keywords should be present whenever applicable.

– All context-specific keywords shall be present as needed and required by the context of the data.

## 9.8.1. Global keywords and overrides

For reference to the keywords that are discussed here, see Table 22. The globally applicable keywords listed in Sect. B of the table serve as default values for the corresponding C\* and TC\* keywords in that same section, but only when axis and column specifications (including alternate coordinate definitions) use a time scale listed in Table 30, or when the corresponding CTYPE or TTYPE keywords are set to the value ’TIME’. Any alternate coordinate specified in a non-recognized time scale assumes the value of the axis pixels or the column cells, optionally modified by applicable scaling and/or reference value keywords; see also Sect. 9.2.1.

43

<!-- page 50 of 75 -->

## 9.8.2. Restrictions on alternate descriptions

An image will have at most one time axis as identified by having the CTYPEi value of ’TIME’ or one of the values listed in Table 30. Consequently, as long as the axis is identified through CTYPEi, there is no need to have axis-number identification on the global time-related keywords. It is expressly prohibited to specify more than one time reference position on this axis for alternate time-coordinate frames, since this would give rise to complicated model-dependent non-linear relations between these frames. Hence, time scales ’TDB’ and ’TCB’ (or ’ET’, to its precision) may be specified in the same image, but cannot be combined with any of the first nine time scales in Table 30; those first nine can be expressed as linear transformations of each other, too, provided the reference position remains unchanged. Time scale ’LOCAL’ is by itself, intended for simulations, and should not be mixed with any of the others.

## 9.8.3. Image time axes

Sect. 8.2 requires keywords CRVALia to be numeric and they cannot be expressed in ISO-8601 format. Therefore it is required that CRVALia contain the elapsed time in units of TIMEUNIT or CUNITia, even if the zero point of time is specified by DATEREF. If the image does not use a matrix for scaling, rotation, and shear (Greisen & Calabretta 2002), CDELTia provides the numeric value for the time interval. If the PC form of scaling, rotation, and shear (Greisen & Calabretta 2002) is used, CDELTia provides the numeric value for the time interval, and PCi j, where i = j = the index of the time axis (in the typical case of an image cube with Axis 3 being time, $i \; = \; j \; = \; 3 )$ would take the exact value 1, the default (Greisen & Calabretta 2002). When the CDi j form of mapping is used, CDi j provides the numeric value for the time interval. If one of the axes is time and the matrix form is used, then the treatment of the PCi ja (or CDi ja) matrices involves at least a Minkowsky metric and Lorentz transformations (as contrasted with Euclidean and Galilean).

## 10. Representations of compressed data

Minimizing data volume is important in many contexts, particularly for publishers of large astronomical data collections. The following sections describe compressed representations of data in FITS images and BINTABLE extensions that preserve metadata and allow for full or partial extraction of the original data as necessary. The resulting FITS file structure is independent of the specific data-compression algorithm employed. The implementation details for some compression algorithms that are widely used in astronomy are defined in Sect. 10.4, but other compression techniques could also be supported. See the FITS convention by White et al. (2013) for details of the compression techniques, but beware that the specifications in this Standard shall supersede those in the registered convention.

Compression of FITS files can be beneficial for sites that store or distribute large quantities of data; the present section provides a standard framework that addresses such needs. As implementation of compression/decompression codes can be quite complex, not all software for reading and writing FITS is nec-

essarily expected to support these capabilities. External utilities are available to compress and decompress FITS files<sup>15</sup>.

## 10.1. Tiled image compression

The following describes the process for compressing n−dimensional FITS images and storing the resulting byte stream in a variable-length column in a FITS binary table, and for preserving the image header keywords in the table header. The general principle is to first divide the n−dimensional image into a rectangular grid of subimages or “tiles.” Each tile is then compressed as a block of data, and the resulting compressed byte stream is stored in a row of a variable-length column in a FITS binary table (see Sect. 7.3). By dividing the image into tiles it is possible to extract and decompress subsections of the image without having to decompress the whole image. The default tiling pattern treats each row of a two-dimensional image (or higher-dimensional cube) as a tile, such that each tile contains NAXIS1 pixels. This default may not be optimal for some applications or compression algorithms, so any other rectangular tiling pattern may be defined using keywords that are defined below. In the case of relatively small images it may suffice to compress the entire image as a single tile, resulting in an output binary table containing a single row. In the case of three-dimensional data cubes, it may be advantageous to treat each plane of the cube as a separate tile if application software typically needs to access the cube on a plane-by-plane basis.

## 10.1.1. Required keywords

In addition to the mandatory keywords for BINTABLE extensions (see Sect. 7.3.1) the following keywords are reserved for use in the header of a FITS binary-table extension to describe the structure of a valid compressed FITS image. All are mandatory.

ZIMAGE – [logical; value T] The value field of this keyword shall contain the logical value T to indicate that the FITS binary-table extension contains a compressed image, and that logically this extension should be interpreted as an image rather than a table.

ZCMPTYPE – [string; default: none] The value field of this keyword shall contain a character string giving the name of the algorithm that was used to compress the image. Only the values given in Table 36 are permitted; the corresponding algorithms are described in Sect. 10.4. Other algorithms may be added in the future.

ZBITPIX – [integer; default: none] The value field of this keyword shall contain an integer that gives the value of the BITPIX keyword in the uncompressed FITS image.

ZNAXIS – [integer; default: none] The value field of this keyword shall contain an integer that gives the value of the NAXIS keyword (i.e., the number of axes) in the uncompressed FITS image.

ZNAXISn – [integer; indexed; default: none) The value field of these keywords shall contain a positive integer that gives the value of the corresponding NAXISn keywords (i.e., the size of Axis n) in the uncompressed FITS image.

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">15 e.g. fpack/funpack, see [https://heasarc.gsfc.nasa.gov/fitsio/fpack/](https://heasarc.gsfc.nasa.gov/fitsio/fpack/)</span></small>

44

<!-- page 51 of 75 -->

The comment fields for the BITPIX, NAXIS, and NAXISn keywords in the uncompressed image should be copied to the corresponding fields in the ZBITPIX, ZNAXIS, and ZNAXISn keywords.

## 10.1.2. Other reserved keywords

The compressed image tiles must be stored in the binary table in the same order that the first pixel in each tile appears in the FITS image; the tile containing the first pixel in the image must appear in the first row of the table, and the tile containing the last pixel in the image must appear in the last row of the binary table. The following keywords are reserved for use in describing compressed images stored in BINTABLE extensions; they may be present in the header, and their values depend upon the type of image compression employed.

ZTILEn – [integer; indexed; default: 1 for n > 1] The value field of these keywords (where n is a positive integer index that ranges from 1 to ZNAXIS) shall contain a positive integer representing the number of pixels along Axis n of the compressed tiles. Each tile of pixels must be compressed separately and stored in a row of a variable-length vector column in the binary table. The size of each image dimension (given by ZNAXISn) need not be an integer multiple of ZTILEn, and if it is not, then the last tile along that dimension of the image will contain fewer image pixels than the other tiles. If the ZTILEn keywords are not present then the default “row-by-row” tiling will be assumed, i.e., ZTILE1 = ZNAXIS1, and the value of all the other ZTILEn keywords must equal 1.

ZNAMEi – [string; indexed; default: none] The value field of these keywords (where i is a positive integer index starting with 1) shall supply the names of up to 999 algorithmspecific parameters that are needed to compress or decompress the image. The order of the compression parameters may be significant, and may be defined as part of the description of the specific decompression algorithm.

ZVALi – [string; indexed; default: none] The value field of these keywords (where i is a positive integer index starting with 1) shall contain the values of up to 999 algorithm-specific parameters with the same index i. The value of ZVALi may have any valid FITS data type.

ZMASKCMP – [string; default: none] The value field of this keyword shall contain the name of the image compression algorithm that was used to compress the optional null-pixel data mask. This keyword may be omitted if no null-pixel data masks appear in the table. See Sect. 10.2.2 for details.

ZQUANTIZ – [string; default: ’NO DITHER’] The value field of this keyword shall contain the name of the algorithm that was used to quantize floating-point image pixels into integer values, which were then passed to the compression algorithm as discussed further in Sect. 10.2. If this keyword is not present, the default is to assume that no dithering was applied during quantization.

ZDITHER0 – [integer; default: none] The value field of this keyword shall contain a positive integer (that may range from 1 to 10000 inclusive) that gives the seed value for the random dithering pattern that was used when quantizing the floatingpoint pixel values. This keyword may be absent if no dithering was applied. See Sect. 10.2 for further discussion.

The following keywords are reserved to preserve a verbatim copy of the value and comment fields for keywords in the original uncompressed FITS image that were used to describe its structure. These optional keywords, when present, shall be used when reconstructing an identical copy of the original FITS HDU of the uncompressed image. They should not appear in the compressed image header unless the corresponding keywords were present in the uncompressed image.

ZSIMPLE – [logical; value T] The value field of this keyword must contain the value of the original SIMPLE keyword in the uncompressed image.

ZEXTEND – [string] The value field of this keyword must contain the value of the original EXTEND keyword in the uncompressed image.

ZBLOCKED – [logical] The value field of this keyword must contain the value of the original BLOCKED keyword in the uncompressed image.

ZTENSION – [string] The value field of this keyword must contain the original XTENSION keyword in the uncompressed image.

ZPCOUNT – [integer] The value field of this keyword must contain the original PCOUNT keyword in the uncompressed image.

ZGCOUNT – [integer] The value field of this keyword must contain the original GCOUNT keyword in the uncompressed image.

ZHECKSUM – [string] The value field of this keyword must contain the original CHECKSUM keyword (see Sect. 4.4.2.7) in the uncompressed image.

ZDATASUM – [string] The value field of this keyword must contain the original DATASUM keyword (see Sect. 4.4.2.7) in the uncompressed image.

The ZSIMPLE, ZEXTEND, and ZBLOCKED keywords must not be used unless the original uncompressed image was contained in the primary array of a FITS file. The ZTENSION, ZPCOUNT, and ZGCOUNT keywords must not be used unless the original uncompressed image was contained in an IMAGE extension.

The FITS header of the compressed image may contain other keywords. If a FITS primary array or IMAGE extension is compressed using the procedure described here, it is strongly recommended that all the keywords (including comment fields) in the header of the original image, except for the mandatory keywords mentioned above, be copied verbatim and in the same order into the header of the binary-table extension that contains the compressed image. All these keywords will have the same meaning and interpretation as they did in the original image, even in cases where the keyword is not normally expected to occur in the header of a binary-table extension (e.g., the BSCALE and BZERO keywords, or the world-coordinate-system keywords such as CTYPEn, CRPIXn, and CRVALn).

## 10.1.3. Table columns

Two columns in the FITS binary table are defined below to contain the compressed image tiles; the order of the columns in the table is not significant. One of the table columns describes optional content; but when this column appears it must be used as defined in this section. The column names (given by the TTYPEn

45

<!-- page 52 of 75 -->

keyword) are reserved; they are shown here in upper-case letters, but case is not significant.

COMPRESSED DATA – [variable-length; required] Each row of this column must contain the byte stream that is generated as a result of compressing the corresponding image tile. The data type of the column (as given by the TFORMn keyword) must be one of ’1PB’, ’1PI’, or ’1PJ’ (or the equivalent’1QB’, ’1QI’, or ’1QJ’), depending on whether the compression algorithm generates an output stream of 8-bit bytes, or integers of 16, or 32 bits respectively.

When using the quantization method to compress floatingpoint images that is described in Sect. 10.2, it sometimes may not be possible to quantize some of the tiles (e.g., if the range of pixels values is too large or if most of the pixels have the same value and hence the calculated RMS noise level in the tile is close to zero). There also may be other rare cases where the nominal compression algorithm cannot be applied to certain tiles. In these cases, an alternate technique may be used in which the raw pixel values are losslessly compressed with the Gzip algorithm.

GZIP COMPRESSED DATA [variable-length; optional] If the raw pixel values in an image tile are losslessly compressed with the Gzip algorithm, the resulting byte stream must be stored in this column (with a ’1PB’ or ’1QB’ variable-length arraycolumn format). The corresponding COMPRESSED DATA column for these tiles must contain a null pointer (i.e., the pair of integers that constitute the descriptor for the column must both have the value zero: see Sect. 7.3.5).

The compressed data columns described above may use either the ’1P’ or ’1Q’ variable-length array FITS column format if the size of the heap in the compressed FITS file is < 2.1 GB. If the the heap is larger than 2.1 GB, then the ’1Q’ format (which uses 64-bit pointers) must be used.

When using the optional quantization method described in Sect. 10.2 to compress floating-point images, the following columns are required.

ZSCALE – [floating-point; optional] This column shall be used to contain linear scale factors that, along with ZZERO, transform the floating-point pixel values in each tile to integers via,

$$
I _ {i} = \text {round} \left(\frac {F _ {i} - \text {ZZERO}}{\text {ZSCALE}}\right)\tag{12}
$$

where $I _ { i }$ and $F _ { i }$ are the integer and (original) floating-point values of the image pixels, respectively, and the round function rounds the result to the nearest integer value.

ZZERO – [floating-point; optional] This column shall be used to contain zero-point offsets that are used to scale the floatingpoint pixel values in each tile to integers via Eq. 12.

Do not confuse the ZSCALE and ZZERO columns with the BSCALE and BZERO keywords (defined in Sect. 4.4.2) that may be present in integer FITS images. Any such integer images should normally be compressed without any further scaling, and the BSCALE and BZERO keywords should be copied verbatim into the header of the binary table containing the compressed image.

Some images contain undefined pixel values; in uncompressed floating-point images these pixels have an IEEE NaN

value. However, these pixel values will be altered when using the quantization method described in Sect. 10.2 to compress floating-point images. The value of the undefined pixels may be preserved in the following way.

ZBLANK – [integer; optional] When present, this column shall be used to store the integer value that represents undefined pixels in the scaled integer array. The recommended value for ZBLANK is −2147483648, the largest negative 32-bit integer. If the same null value is used in every tile of the image, then ZBLANK may be given in a header keyword instead of a table column; if both a keyword and a table column named ZBLANK are present, the values in the table column must be used. If there are no undefined pixels in the image then ZBLANK is not required to be present either as a table column or a keyword.

If the uncompressed image has an integer data type (ZBITPIX > 0) then the value of undefined pixels is given by the BLANK keyword (see Sect. 5.3), which should be used instead of ZBLANK.

When using some compression techniques that do not exactly preserve integer pixel values, it may be necessary to store the location of the undefined pixels prior to compressing the image. The locations may be stored in an image mask, which must itself be compressed and stored in a table column with the following definition. See Sect. 10.2.2 for more details.

NULL PIXEL MASK – [integer array; optional] When present, this column shall be used to store, in compressed form, an image mask with the same original dimensions as the uncompressed image, that records the location of the undefined pixels. The process defined in Sect. 10.2.2 shall be used to construct the compressed pixel mask.

Additional columns may be present in the table to supply other parameters that relate to each image tile. However, these parameters should not be recorded in the image HDU when the uncompressed image is restored.

## 10.2. Quantization of floating-point data

While floating-point format images may be losslessly compressed, noisy images often do not compress very well. Higher compression can only be achieved by removing some of this noise without losing the useful information content. One commonly used technique for reducing the noise is to scale the floating-point values into quantized integers using Eq. 12, and using the ZSCALE and ZZERO columns to record the two scaling coefficients that are used for each tile. Note that the absence of these two columns in a tile-compressed floating-point image is an indication that the image was not scaled, and was instead losslessly compressed.

An effective scaling algorithm for preserving a specified amount of noise in each pixel value is described by White & Greenfield (1999) and by Pence et al. (2009). With this method, the ZSCALE value (which is numerically equal to the spacing between adjacent quantization levels) is calculated to be some fraction, Q, of the RMS noise as measured in background regions of the image. Pence et al. (2009) shows that the number of binary bits of noise that are preserved in each pixel value is given by log<sub>2</sub>(Q) + 1.792. The Q value directly affects the

46

<!-- page 53 of 75 -->

compressed file size: decreasing Q by a factor of two will decrease the file size by about one bit per pixel. In order to achieve the greatest amount of compression, one should use the smallest value of Q that still preserves the required amount of photometric and astrometric precision in the image.

A potential problem when applying this scaling method to astronomical images, in particular, is that it can lead to a systematic bias in the measured intensities in faint parts of the image. As the image is quantized more coarsely, the measured intensity of the background regions of the sky will tend to be biased towards the nearest quantize level. One very effective technique for minimizing this potential bias is to dither the quantized pixel values by introducing random noise during the quantization process. So instead of simply scaling every pixel value in the same way using Eq. 12, the quantized levels are randomized by using this slightly modified equation:

$$
I _ {i} = \text {round} \left(\frac {F _ {i} - \text {ZZERO}}{\text {ZSCALE}} + R _ {i} - 0. 5\right)\tag{13}
$$

where $R _ { i }$ is a random number between 0.0 and 1.0, and 0.5 is subtracted so that the mean quantity equals 0. Then restoring the floating-point value, the same $R _ { i }$ is used with the inverse formula:

$$
F _ {i} = ((I _ {i} - R _ {i} + 0. 5) * \text {ZSCALE}) + \text {ZZERO}.\tag{14}
$$

This “subtractive dithering” technique has the effect of dithering the zero point of the quantization grid on a pixel-by-pixel basis without adding any actual noise to the image. The net effect of this is that the mean (and median) pixel value in faint regions of the image more closely approximate the value in the original unquantized image than if all the pixels are scaled without dithering.

The key requirement when using this subtractive-dithering technique is that the exact same random-number sequence must be used when quantizing the pixel values to integers, and when restoring them to floating-point values. While most computer languages supply a function for generating random numbers, these functions are not guaranteed to generate the same sequence of numbers every time. An algorithm for generating a repeatable sequence of pseudo-random numbers is given in Appendix I; this algorithm must be used when applying a subtractive dither.

## 10.2.1. Dithering algorithms

The ZQUANTIZ keyword, if present, must have one of the following values to indicate the type of quantization, if any, that was applied to the floating-point image for compression.

’NO DITHER’ – No dithering was performed; the floating-point pixels were simply quantized using Eq. 12. This option shall be assumed if the ZQUANTIZ keyword is not present in the header of the compressed floating-point image.

’SUBTRACTIVE DITHER 1’ – The basic subtractive dithering was performed, the algorithm for which is described below. Note that an image quantized using this technique can still be unquantized using the simple linear scaling function given by Eq. 12, at the cost of introducing slightly more noise in the image than if the full subtractive-dithering algorithm were applied.

’SUBTRACTIVE DITHER $2   ^ { \circ } - 1$ his dithering algorithm is identical to that for ’SUBTRACTIVE DITHER 1’, except that any

pixels in the floating-point image that are exactly equal to 0.0 are represented by the reserved value −2147483647 in the quantized integer array. When the image is subsequently decompressed and unscaled, these pixels must be restored to their original value of 0.0. This dithering option is useful if the zero-valued pixels have special significance to the data analysis software, so that the value of these pixels must not be dithered.

The process for generating a subtractive dither for a floatingpoint image is the following.

1. Generate a sequence of 10000 single-precision floating-point random numbers, RN, with a value between 0.0 and 1.0. Since it could be computationally expensive to generate a unique random number for every pixel of large images, simply cycle through this look-up table of random numbers.

2. Choose an integer in the range 1 to 10000 to serve as an initial seed value for creating a unique sequence of random numbers from the array that was calculated in the previous step. The purpose of this is to reduce the chances of applying the same dithering pattern to two images that are subsequently subtracted from each other (or co-added), because the benefits of randomized dithering are lost if all the pixels are dithered in phase with each other. The exact method for computing this seed integer is not important as long as the value is chosen more or less randomly.

3. Write the integer seed value that was selected in the previous step as the value of the ZDITHER0 keyword in the header of the compressed image. This value is required to recompute the same dithering pattern when decompressing the image.

4. Before quantizing each tile of the floating-point image, calculate an initial value for two offset parameters, $I _ { 0 }$ and $I _ { 1 } ,$ with the following formulae:

$$
I _ {0} = \operatorname{mod} (N _ {\text {tile}} - 1 + \text {ZDITHER0,10000})
$$

$$
I _ {1} = \mathrm{INT} (\mathrm{RN} (I _ {0}) * 5 0 0.)\tag{15}
$$

(16)

where $N _ { \mathrm { t i l e } }$ is the row number in the binary table that is used to store the compressed bytes for that tile, ZDITHER0 is that value of that keyword, and $\mathrm { R N } ( I _ { 0 } )$ is the value of the $I _ { 0 } ^ { \mathrm { { i h } } }$ random number in the sequence that was computed in the first step. Note that $I _ { 0 }$ has a value in the range 0 to 9999 and $I _ { 1 }$ has a value in the range 0 to 499. This method for computing $I _ { 0 }$ and $I _ { 1 }$ was chosen so that a different sequence of random numbers is used to compress successive tiles in the image, and so that the sequence of $I _ { 1 }$ values has a length of order 100-million elements before repeating.

5. Now quantize each floating-point pixel in the tile using Eq. 13 and using random number RN(I<sub>1</sub>) for the first pixel. Increment the value of $I _ { 1 }$ for each subsequent pixel in the tile. If I<sub>1</sub> reaches the upper limit of 500, then increment the value of $I _ { 0 }$ and recompute $I _ { 1 }$ from Eq. 16. If $I _ { 0 }$ also reaches the upper limit of 10000, then reset $I _ { 0 }$ to $0 .$

If the floating-point pixel has an IEEE NaN value, then it is not quantized or dithered but instead is set to the reserved integer value specified by the ZBLANK keyword. For consistency, the value of $I _ { 1 }$ should also be incremented in this case even though it is not used.

6. Compress the array of quantized integers using the lossless algorithm that is specified by the ZCMPTYPE keyword (use’RICE 1’ by default).

47

<!-- page 54 of 75 -->

7. Write the compressed byte stream into the COMPRESSED DATA column in the appropriate row of the binary table corresponding to that tile.

8. Write the linear scaling and zero-point values that were used in Eq. 13 for that tile into the ZSCALE and ZZERO columns, respectively, in the same row of the binary table.

9. Repeat Steps 4 through 8 for each tile of the image.

## 10.2.2. Preserving undefined pixels with lossy compression

The undefined pixels in integer images are flagged by a reserved BLANK value and will be preserved if a lossless compression algorithm is used. (ZBLANK is used for undefined pixels in floatingpoint images.) If the image is compressed with a lossy algorithm, then some other technique must be used to identify the undefined pixels in the image. In this case it is recommended that the undefined pixels be recorded with the following procedure.

1. Create an integer data mask with the same dimensions as the image tile.

2. For each undefined pixel in the image, set the corresponding mask pixels to 1 and all the other pixels to 0.

3. Compress the mask array using a lossless algorithm such as PLIO or Gzip, and record the name of that algorithm with the keyword ZMASKCMP.

4. Store the compressed byte stream in a variable-length-array column called NULL PIXEL MASK in the table row corresponding to that image tile.

The data mask array pixels should have the shortest integer data type that is supported by the compression algorithm (i.e., usually eight-bit bytes). When decompressing the image tile, the software must check if the corresponding compressed data mask exists with a length greater than 0, and if so, decompress the mask and set the corresponding undefined pixels in the image array to the value given by the BLANK keyword.

## 10.3. Tiled table compression

The following section describes the process for compressing the content of BINTABLE columns. Some additional details of BINTABLE compression may be found in Pence et al. (2013), but the specifications in this Standard shall supersede those in the registered convention. The uncompressed table may be subdivided into tiles, each containing a subset of rows, then each column of data within each tile is extracted, compressed, and stored as a variable-length array of bytes in the output compressed table. The header keywords from the uncompressed table, with only a few limited exceptions, shall be copied verbatim to the header of the compressed table. The compressed table must itself be a valid FITS binary table (albeit one where the contents cannot be interpreted without decompressing the contents) that contains the same number and order of columns as in the uncompressed table, and that contains one row for each tile of rows in the uncompressed table. Only the compression algorithms specified in Sect. 10.3.5 are permitted.

## 10.3.1. Required keywords

With only a few exceptions noted below, all the keywords and corresponding comment fields from the uncompressed table must be copied verbatim, in order, into the header of the com-

pressed table. Note in particular that the values of the reserved column descriptor keywords TTYPEn, TUNITn, TSCALn, TZEROn, TNULLn, TDISPn, and TDIMn, as well as all the column-specific WCS keywords defined in the FITS Standard, must have the same values and data types in both the original and in the compressed table, with the understanding that these keywords apply to the uncompressed data values.

The only keywords that must not be copied verbatim from the uncompressed table header to the compressed table header are the mandatory NAXIS1, NAXIS2, PCOUNT, and TFORMn keywords, and the optional CHECKSUM, DATASUM (see Sect. 4.4.2.7), and THEAP keywords. These keywords must necessarily describe the contents and structure of the compressed table itself. The original values of these keywords in the uncompressed table must be stored in a new set of reserved keywords in the compressed table header. Note that there is no need to preserve a copy of the GCOUNT keyword because the value is always equal to 1 for BINTABLE extensions. The complete set of keywords that have a reserved meaning within a tile-compressed binary table are given below.

ZTABLE – [logical; value: T] The value field of this keyword shall be T to indicate that the FITS binary-table extension contains a compressed BINTABLE, and that logically this extension should be interpreted as a tile-compressed binary table.

ZNAXIS1 – [integer; default: none] The value field of this keyword shall contain an integer that gives the value of the NAXIS1 keyword in the original uncompressed FITS table header. This represents the width in bytes of each row in the uncompressed table.

ZNAXIS2 – [integer; default: none] The value field of this keyword shall contain an integer that gives the value of the NAXIS2 keyword in the original uncompressed FITS table header. This represents the number of rows in the uncompressed table.

ZPCOUNT – [integer; default: none] The value field of this keyword shall contain an integer that gives the value of the PCOUNT keyword in the original uncompressed FITS table header.

ZFORMn – [string; indexed; default: none] The value field of these keywords shall contain the character-string values of the corresponding TFORMn keywords that defines the data type of Column n in the original uncompressed FITS table.

ZCTYPn – [string; indexed; default: none] The value field of these keywords shall contain the character-string value mnemonic name of the algorithm that was used to compress Column n of the table. The only permitted values are given in Sect. 10.3.5, and the corresponding algorithms are described in Sect. 10.4.

ZTILELEN – [integer; default: none] The value field of this keyword shall contain an integer representing the number of rows of data from the original binary table that are contained in each tile of the compressed table. The number of rows in the last tile may be fewer than in the previous tiles. Note that if the entire table is compressed as a single tile, then the compressed table will only contains a single row, and the ZTILELEN and ZNAXIS2 keywords will have the same value.

48

<!-- page 55 of 75 -->

## 10.3.2. Procedure for table compression

The procedure for compressing a FITS binary table consists of the following sequence of steps.

## 1. Divide table into tiles (optional)

In order to limit the amount of data that must be managed at one time, large FITS tables may be divided into tiles, each containing the same number of rows (except for the last tile, which may contain fewer rows). Each tile of the table is compressed in order, and each is stored in a single row in the output compressed table. There is no fixed upper limit on the allowed tile size, but for practical purposes it is recommended that it not exceed 100 MB.

## 2. Decompose each tile into the component columns

FITS binary tables are physically stored in row-by-row sequential order, such that the data values for the first row in each column are followed by the values in the second row, and so on (see Sect. 7.3.3). Because adjacent columns in binary tables can contain very non-homogeneous types of data, it can be challenging to efficiently compress the native stream of bytes in the FITS tables. For this reason, the table is first decomposed into its component columns, and then each column of data is compressed separately. This also allows one to choose the most-efficient compression algorithm for each column.

## 3. Compress each column of data

Each column of data must be compressed with one of the lossless compression algorithms described in Sect. 10.4. If the table is divided into tiles, then the same compression algorithm must be applied to a given column in every tile. In the case of variable-length array columns (where the data are stored in the table heap: see Sect. 7.3.5), each individual variable-length vector must be compressed separately.

## 4. Store the compressed bytes

The compressed stream of bytes for each column must be written into the corresponding column in the output table. The compressed table must have exactly the same number and order of columns as the input table, however, the data type of the columns in the output table will all have a variable-length byte data type, with TFORMn = ’1QB’. Each row in the compressed table corresponds to a tile of rows in the uncompressed table.

In the case of variable-length array columns, the array of descriptors that point to each compressed variable-length array, as well as the array of descriptors from the input uncompressed table, must also be compressed and written into the corresponding column in the compressed table. See Sect. 10.3.6 for more details.

## 10.3.3. Compression directive keywords

The following compression-directive keywords, if present in the header of the table to be compressed, are reserved to provide guidance to the compression software on how the table should be compressed. The compression software should attempt to obey these directives, but if that is not possible the software may disregard them and use an appropriate alternative. These keywords are optional, but must be used as specified below.

– FZTILELN – [integer] The value field of this keyword shall contain an integer that specifies the requested number of table rows in each tile that are to be compressed as a group.

– FZALGOR – [string] The value field of this keyword shall contain a character string giving the mnemonic name of the algorithm that is requested to be used by default to compress every column in the table. The permitted values are given in Sect. 10.3.5.

– FZALGn – [string; indexed] The value fields of these keywords shall contain a character string giving the mnemonic name of the algorithm that is requested to compress Column n of the table. The current allowed values are the same as for the FZALGOR keyword. The FZALGn keyword takes precedence over FZALGOR in determining which algorithm to use for a particular column if both keywords are present.

## 10.3.4. Other reserved keywords

The following keywords are reserved to store a verbatim copy of the value and comment fields for specific keywords in the original uncompressed BINTABLE. These keywords, if present, should be used to reconstruct an identical copy of the uncompressed BINTABLE, and should not appear in the compressed table header unless the corresponding keywords were present in the uncompressed BINTABLE.

ZTHEAP – [integer; default: none] The value field of this keyword shall contain an integer that gives the value of the THEAP keyword if present in the original uncompressed FITS table header.

ZHECKSUM – [string; default: none] The value field of this keyword shall contain a character string that gives the value of the CHECKSUM keyword (see Sect. 4.4.2.7) in the original uncompressed FITS HDU.

ZDATASUM – [string; default: none] The value field of this keyword shall contain a character string that gives the value of the DATASUM keyword (see Sect. 4.4.2.7) in the original uncompressed FITS HDU.

## 10.3.5. Supported compression algorithms for tables

The permitted algorithms for compressing BINTABLE columns are ’RICE 1’, ’GZIP 1’, and ’GZIP 2’ (plus ’NOCOMPRESS’), which are lossless and are described in Sect. 10.4. Lossy compression could be allowed in the future once a process is defined to preserve the details of the compression.

## 10.3.6. Compressing variable-length array columns

Compression of BINTABLE tiles that contain variable-length array (VLA) columns requires special consideration because the array values in these columns are not stored directly in the table, but are instead stored in a data heap, which follows the main table (see Sect. 7.3.5). The VLA column in the original, uncompressed table only contains descriptors, which comprise two integers that give the size and location of the arrays in the heap. When decompressing, these descriptor values will be needed to write the decompressed VLAs back into the same location in the heap as in the original uncompressed table. Thus, the following

49

<!-- page 56 of 75 -->

process must be followed, in order, when compressing a VLA column within a tile. Refer to Pence et al. (2013) for additional details.

## 1. For each VLA in the column:

– read the array from the input table, and compress it using the algorithm specified by ZCTYP for this VLA column;

– write the resulting byte stream to the heap of the compressed table; and

– store (or append) the descriptors to the compressed byte stream (which must be 64-bit Q-type) in a temporary array.

2. Append the VLA descriptors from the uncompressed table (which may be either Q-type or P-type) to the temporary array of VLA descriptors for the compressed table.

3. Compress the combined array of descriptors using’GZIP 1’, and write that byte stream into the corresponding VLA column in the output table, so that the compressed array is appended to the heap.

When decompressing a VLA column, two stages of decompression must be performed in order.

1. Decompress the combined array of descriptors using the Gzip algorithm.

2. For each descriptor to a compressed array:

– read the compressed VLA from the compressed table, and decompress it using the algorithm specified by ZCTYP for this VLA column; and

– write it to the correct location in the decompressed table.

## 10.4. Compression algorithms

Table 36: Valid mnemonic values for the ZCMPTYPE and ZCTYPn keywords

| Value | Sect. | Compression Type |
| --- | --- | --- |
| 'RICE_1' | 10.4.1 | Rice algorithm for integer data |
| 'GZIP_1' | 10.4.2 | Combination of the LZ77 algorithm and Huffman coding, used in GNU Gzip |
| 'GZIP_2' | 10.4.2 | Like 'GZIP_1', but with reshuffled byte values |
| 'PLIO_1' | 10.4.3 | IRAF PLIO algorithm for integer data |
| 'HCOMPRESS_1' | 10.4.4 | H-compress algorithm for two-dimensional images |
| 'NOCOMPRESS' |  | The HDU remains uncompressed |

The name of the permitted algorithms for compressing FITS HDUs, as recorded in the ZCMPTYPE keyword, are listed in Table 36; if other types are later supported, they must be registered with the IAUFWG to reserve the keyword values. Keywords for the parameters of supported compression algorithms have also been reserved, and are described with each algorithm in the subsections below. If alternative compression algorithms require keywords beyond those defined below, they must also be registered with the IAUFWG to reserve the associated keyword names.

## 10.4.1. Rice compression

When $\mathtt { Z C M P T Y P E } = \mathtt { ^ { \prime } R I C E _ { - } I }$ , the Rice algorithm (Rice et al. 1993) shall be used for data (de)compression. When selected, the keywords in Table 37 should also appear in the header with one of the values indicated. If these keywords are absent, then their default values must be used. The Rice algorithm is lossless, but can only be applied to integer-valued arrays. It offers a significant performance advantage over the other compression techniques (see White et al. 2013).

Table 37: Keyword parameters for Rice compression

<table><tr><td rowspan="2">Keyword</td><td colspan="2">Values</td><td rowspan="2">Meaning</td></tr><tr><td>Permitted</td><td>Default</td></tr><tr><td>ZNAME1</td><td>&#x27;BLOCKSIZE&#x27;</td><td>-</td><td>Size of block in pixels</td></tr><tr><td>ZVAL1</td><td>16, 32</td><td>32</td><td>No. of pixels in a block</td></tr><tr><td>ZNAME2</td><td>&#x27;BYTEPIX&#x27;</td><td>-</td><td>Size of pixel value in bytes</td></tr><tr><td>ZVAL2</td><td>1, 2, 4, 8</td><td>4</td><td>No. of eight-bit bytes per original pixel value</td></tr></table>

## 10.4.2. Gzip compression

When ZCMPTYPE = ’GZIP 1’, the Gzip algorithm shall be used for data (de)compression. There are no algorithm parameters, so the keywords ZNAMEn and ZVALn should not appear in the header. The Gzip algorithm is used in the free GNU software compression utility of the same name. It was created by J.- L. Gailly and M. Adler, based on the DEFLATE algorithm (Deutsch 1996), which is a combination of LZ77 (Ziv & Lempel 1977) and Huffman coding. The Unix gzip program accepts an integer parameter that provides a trade between optimization for speed (1) and compression ratio (9), which does not affect the format of the resultant data stream. The selection of this parameter is an implementation detail that is not covered by this Standard.

When ZCMPTYPE = ’GZIP 2’, the gzip2 algorithm shall be used for data (de)compression. The gzip2 algorithm is a variation on ’GZIP 1’. There are no algorithm parameters, so the keywords ZNAMEn and ZVALn should not appear in the header. In this case the bytes in the array of data values are shuffled so that they are arranged in order of decreasing significance before being compressed. For example, a five-element contiguous array of two-byte (16-bit) integer values, with an original big-endian byte order of:

$$
A _ {1} A _ {2} B _ {1} B _ {2} C _ {1} C _ {2} D _ {1} D _ {2} E _ {1} E _ {2}
$$

will have the following byte order after shuffling:

$$
A _ {1} B _ {1} C _ {1} D _ {1} E _ {1} A _ {2} B _ {2} C _ {2} D _ {2} E _ {2},
$$

where $A _ { 1 } , B _ { 1 } , C _ { 1 } , D _ { 1 }$ , and $E _ { 1 }$ are the most-significant bytes from each of the integer values. Byte shuffling shall only be performed for integer or floating-point numeric data types; logical, bit, and character types must not be shuffled.

## 10.4.3. IRAF/PLIO compression

When ZCMPTYPE = ’PLIO 1’. the IRAF PLIO algorithm shall be used for data (de)compression. There are no algorithm parameters, so the keywords ZNAMEn and ZVALn should not appear in

50

<!-- page 57 of 75 -->

the header. The PLIO algorithm was developed to store integervalued image masks in a compressed form. The compression algorithm used is based on run-length encoding, with the ability to dynamically follow level changes in the image, in principle allowing a 16-bit encoding to be used regardless of the image depth. However, this algorithm has only been implemented in a way that supports image depths of no more than 12 bits; therefore ’PLIO 1’ must only be used for integer image types with values between 0 and $2 ^ { 2 \check { 4 } }$

The compressed line lists are stored as variable-length arrays of type short integer (16 bits per list element), regardless of the mask depth. A line list consists of a series of simple instructions, which are executed in sequence to reconstruct a line of the mask. Each 16-bit instruction consists of the sign bit (not used), a threebit opcode, and twelve bits of data, as depicted below.

| +-- | +---- | +---- | +---- | + |
| --- | --- | --- | --- | --- |
| \|16\| | 15 | 13\|12 | 1\| |  |
| +-- | +---- | +---- | +---- | + |
| \| | \|opcode | \| | data | \| |
| +-- | +---- | +---- | +---- | + |

The significance of the data depends upon the instruction. In order to reconstruct a mask line, the application executing these instructions is required to keep track of two values, the current high value and the current position in the output line. The detailed operation of each instruction is given in Table 38.

Table 38: PLIO Instructions

| Instr. | Opcode | Meaning |
| --- | --- | --- |
| 'ZN' 'HN' | '00''04' | Zero the next Noutput pixels. Set the next N output pixels to the current high value. |
| 'PN' | '05' | Zero the next N - 1 output pixels, and set Pixel Nto the current high value. |
| 'SH' | '05' | Set the high value (absolute rather than in-cremental), taking the high 15 bits from the next word in the instruction stream, and the low 12 bits from the current data value. |
| 'IH,DH' | '02,03' | Increment ('IH') or decrement ('DH') the current high value by the data value. The current position is not affected. |
| 'IS,DS' | '06,07' | Increment ('IS') or decrement ('DS') the current high value by the data value, and step, i.e., output one high value. |

The high value must be set to 1 at the beginning of a line, hence the ’IH,DH’ and ’IS,DS’ instructions are not normally needed for Boolean masks.

## 10.4.4. H-Compress algorithm

When ZCMPTYPE = ’HCOMPRESS 1’, the H-compress algorithm shall be used for data (de)compression. The algorithm was described by White (1992), and can be applied only to images with two dimensions. Briefly, the compression method is to apply, in order:

1. a wavelet transform called the H-transform (a Haar transform generalized to two dimensions), followed by

2. a quantization that discards noise in the image while retaining the signal on all scales, and finally

3. a quadtree coding of the quantized coefficients.

The H-transform is a two-dimensional generalization of the Haar transform. The H-transform is calculated for an image of size $2 ^ { N } \times 2 ^ { N }$ as follows.

1. Divide the image up into blocks of 2 × 2 pixels. Call the four pixel values in a block $a _ { 0 0 } , a _ { 1 0 } , a _ { 0 1 }$ , and $a _ { 1 1 }$

2. For each block compute four coefficients:

$$
\begin{array}{l} h _ {0} = (a _ {1 1} + a _ {1 0} + a _ {0 1} + a _ {0 0}) / (\text {SCALE} * \sigma) \\ h _ {x} = (a _ {1 1} + a _ {1 0} - a _ {0 1} - a _ {0 0}) / (\text {SCALE} * \sigma) \\ h _ {y} = (a _ {1 1} - a _ {1 0} + a _ {0 1} - a _ {0 0}) / (\text {SCALE} * \sigma) \\ h _ {c} = (a _ {1 1} - a _ {1 0} - a _ {0 1} + a _ {0 0}) / (\text {SCALE} * \sigma) \end{array}
$$

where SCALE is an algorithm parameter defined below, and σ characterizes the RMS noise in the uncompressed image.

3. Construct a $2 ^ { N - 1 } \times 2 ^ { N - 1 }$ image from the $h _ { 0 }$ values for each 2 ×2 block. Divide that image up into 2 ×2 blocks and repeat the above calculation. Repeat this process N times, reducing the image in size by a factor of two at each step, until only one h<sub>0</sub> value remains.

This calculation can be easily inverted to recover the original image from its transform. The transform is exactly reversible using integer arithmetic. Consequently, the program can be used for either lossy or lossless compression, with no special approach needed for the lossless case.

Noise in the original image is still present in the H-transform, however. To compress noisy images, each coefficient can be divided by SCALE ∗ σ, where SCALE ∼ 1 is chosen according to how much loss is acceptable. This reduces the noise in the transform to 0.5/SCALE, so that large portions of the transform are zero (or nearly zero) and the transform is highly compressible.

There is one user-defined parameter associated with the H-Compress algorithm: a scale factor to the RMS noise in the image that determines the amount of compression that can be achieved. It is not necessary to know what scale factor was used when compressing the image in order to decompress it, but it is still useful to record it. The keywords in Table 39 should be recorded in the header for this purpose.

Table 39: Keyword parameters for H-compression

<table><tr><td rowspan="2">Keyword</td><td colspan="2">Values</td><td rowspan="2">Meaning</td></tr><tr><td>Permitted</td><td>Default</td></tr><tr><td>ZNAME1</td><td>&#x27;SCALE&#x27;</td><td>&#x27;-&#x27;</td><td>Scale factor</td></tr><tr><td>ZVAL1</td><td>0.0 or larger</td><td>0.0</td><td>Scaling of the RMS noise; 0.0 yields lossless compression</td></tr></table>

Scale Factor – The floating-point scale parameter (whose value is stored in Keyword ZVAL1) determines the amount of compression; higher values result in higher compression, but with greater loss of information. SCALE = 0.0 is a special case that yields lossless compression, i.e. the decompressed image has exactly the same pixel values as the original image. $\mathrm { S C A L E } > 0 . \dot { 0 }$ leads to lossy compression, where SCALE determines how much of the noise is discarded.

51

<!-- page 58 of 75 -->

## Appendix A: Syntax of keyword records

This appendix is not part of the FITS Standard but is included for convenient reference.

```lisp
:= means 'is defined to be'
X | Y means one of X or Y
(no ordering relation is implied)
[X] means that X is optional
X... means X is repeated one or more times
'B' means the ASCII character B
'A'-'Z' means one of the ASCII characters A
through Z in the ASCII collating
sequence, as shown in Appendix D
\0xnn means the ASCII character associated
with the hexadecimal code nn
{...} expresses a constraint or a comment
(it immediately follows the syntax rule)
```

The following statements define the formal syntax used in FITS free-format keyword records, as well as for long-string keywords spanning more than one keyword record).

```txt
FITS_keyword :=
    single_record_keyword |
    long_string_keyword

single_record_keyword :=
    FITS_keyword_record

FITS_keyword_record :=
    FITS_commentary_keyword_record |
    FITS_value_keyword_record

FITS_commentary_keyword_record :=
    COMMENT_keyword [ascii_text_char...] |
    HISTORY_keyword [ascii_text_char...] |
    BLANKFIELD_keyword [ascii_text_char...] |
    keyword_field anychar_but_equal
        [ascii_text_char...] |
    keyword_field '=' anychar_but_space
        [ascii_text_char...]
{Constraint: The total number of characters in a FITS_commentary_keyword_record must be exactly equal to 80.}

FITS_value_keyword_record :=
    keyword_field value_indicator [space...] [value]
        [space...] [comment]
{Constraint: The total number of characters in a FITS_value_keyword_record must be exactly equal to 80.}
{Comment: If the value field is not present, the value of the FITS keyword is not defined.}

long_string_keyword :=
    initial_kwd_record [continuation_kwd_record...]
    last_continuation_record
{Comment: the value of a long_string_keyword is reconstructed by concatenating the partial_string_values of the initial_kwd_record and of any continuation_kwd_records in the order they occur, and the character_string_value of the
```

```txt
last_continuation_record.

initial_kwd_record :=
    keyword_field value_indicator [space...]
    [partial_string_value] [space...] [comment]
{Constraint: The total number of characters in an initial_kwd_record must be exactly equal to 80.}

continuation_kwd_record :=
    CONTINUE_keyword [space...]
    [partial_string_value] [space...] [comment]
{Constraint: The total number of characters in a continuation_kwd_record must be exactly equal to 80.}

last_continuation_record :=
    CONTINUE_keyword [space...]
    [character_string_value] [space...] [comment]
{Constraint: The total number of characters in a last_continuation_record must be exactly equal to 80.}

keyword_field :=
    [keyword_char...] [space...]
{Constraint: The total number of characters in the keyword_field must be exactly equal to 8.}

keyword_char :=
    'A'-'Z' | '0'-'9' | '_' | '-''

COMMENT_keyword :=
    'C' 'O' 'M' 'M' 'E' 'N' 'T' space

HISTORY_keyword :=
    'H' 'I' 'S' 'T' 'O' 'R' 'Y' space

BLANKFIELD_keyword :=
    space space space space space space space

CONTINUE_keyword :=
    'C' 'O' 'N' 'T' 'I' 'N' 'U' 'E'

value_indicator :=
    '=' space

space :=
    ' ',

comment :=
    '/' [ascii_text_char...]

ascii_text_char :=
    space-'sim'

anychar_but_equal :=
    space-'<' | '>'-'sim'

anychar_but_space :=
    '!_'sim'

value :=
    character_string_value | logical_value |
    integer_value | floating_value |
```

52

<!-- page 59 of 75 -->

```tcl
complex_integer_value | complex_floating_value

character_string_value :=
    begin_quote [string_text_char...] end_quote
{Constraint: The begin_quote and end_quote are not part of the
character-string value but only serve as delimiters. Leading
spaces are significant; trailing spaces are not.}

partial_string_value :=
    begin_quote [string_text_char...] ampersand end_quote
{Constraint: The begin_quote, end_quote, and ampersand are not
part of the character-string value but only serve respectively as
delimiters or continuation indicator. }

begin_quote :=
    quote

end_quote :=
    quote
{Constraint: The ending quote must not be immediately fol-
lowed by a second quote.}

quote :=
    \0x27

ampersand :=
    '&'

string_text_char :=
    ascii_text_char
{Constraint: A string_text_char is identical to an ascii_text_char
except for the quote char; a quote char is represented by two
successive quote chars.}

logical_value :=
    'T' | 'F'

integer_value :=
    [sign] digit [digit...]
{Comment: Such an integer value is interpreted as a signed
decimal number. It may contain leading zeros.}

sign :=
    '-' | '+''

digit :=
    '0'-'9'

floating_value :=
    decimal_number [exponent]
decimal_number :=
    [sign] [integer_part] ['.' [fraction_part]]
{Constraint: At least one of the integer_part and fraction_part
must be present.}

integer_part :=
    digit | [digit...]

fraction_part :=
    digit | [digit...]
```

```python
exponent :=
    exponent_letter [sign] digit [digit...]

exponent_letter :=
    'E' | 'D'

complex_integer_value :=
    '(' [space...] real_integer_part [space...] ',' [space...]
    imaginary_integer_part [space...] ')')

real_integer_part :=
    integer_value

imaginary_integer_part :=
    integer_value

complex_floating_value :=
    '(' [space...] real_floating_part [space...] ',' [space...]
    imaginary_floating_part [space...] ')'

real_floating_part :=
    floating_value

imaginary_floating_part :=
    floating_value
```

## Appendix B: Suggested time-scale specification

The content of this appendix has been superseded by Sect. 9 of the formal Standard, which derives from Rots et al. (2015).

53

<!-- page 60 of 75 -->

## Appendix C: Summary of keywords

This appendix is not part of the FITS Standard, but is included for convenient reference.

All of the mandatory and reserved keywords that are defined in the Standard, except for the reserved WCS keywords that are discussed separately in Sect. 8, are listed in Tables C.1, C.2, and C.3. An alphabetical list of these keywords and their definitions is available online: [http://heasarc.gsfc.nasa.gov/docs/fcg/standard\_dict.html](http://heasarc.gsfc.nasa.gov/docs/fcg/standard_dict.html).

Table C.1: Mandatory FITS keywords for the structures described in this document.

| Primary HDU | Conforming extension | Image extension | ASCII-table extension | Binary-table extension | Compressed $images^6$ | Compressed $tables^6$ | Random-groups records |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SIMPLE | XTENSION | $XTENSION^1$ | $XTENSION^2$ | $XTENSION^3$ | ZIMAGE =T | ZTABLE =T | SIMPLE |
| BITPIX | BITPIX | BITPIX | BITPIX = 8 | BITPIX = 8 | ZBITPIX | ZNAXIS1 | BITPIX |
| NAXIS | NAXIS | NAXIS | NAXIS = 2 | NAXIS = 2 | ZNAXIS | ZNAXIS2 | NAXIS |
| $NAXISn^4$ | $NAXISn^4$ | $NAXISn^4$ | NAXIS1 | NAXIS1 | ZNAXISn | ZPCOUNT | NAXIS1 = 0 |
| END | PCOUNT | PCOUNT = 0 | NAXIS2 | NAXIS2 | ZCMPTYPE | ZFORMn | $NAXISn^4$ |
|  | GCOUNT | GCOUNT = 1 | PCOUNT = 0 | PCOUNT |  | ZCTYPn | GROUPS = T |
|  | END |  | GCOUNT = 1 | GCOUNT = 1 |  | ZTILELEN | PCOUNT |
|  |  |  | TFIELDS | TFIELDS |  |  | GCOUNT |
|  |  |  | $TFORMn^5$ | $TFORMn^5$ |  |  | END |
|  |  |  | $TBCOLn^5$ | END |  |  |  |
|  |  |  | END |  |  |  |  |

$\mathrm{XTENSION= \text{、 }^{\prime} IMAE}_{上上上}$ for the image extension. ${ \tt ^ { ( 2 ) } X T E N S I O N { = } \sqcup ^ { \intercal } T A B L E _ { \sqcup \sqcup \sqcup ^ { \intercal } } }$ for the ASCII-table extension. ( )XTENSION= 'BINTABLE' for the binary-table extension. (<sup>4</sup>)Runs from 1 through the value of NAXIS.(<sup>5</sup>)Runs from 1 through the value of TFIELDS.(<sup>6</sup>)Required in addition to the mandatory keywords for binary tables.

Table C.2: Reserved FITS keywords for the structures described in this document.

|  | $All^1$HDUs | $Array^2$HDUs | ASCII-table extension | Binary-table extension | Compressed images | Compressed tables | Random-groups records |
| --- | --- | --- | --- | --- | --- | --- | --- |
| DATE | EXTNAME | BSCALE | TSCALn | TSCALn | ZTILEn | FZTILELN | PTYPEn |
| DATE-OBS | EXTVER | BZERO | TZEROn | TZEROn | ZNAMEi | FZALGOR | PSCALn |
| ORIGIN | EXTLEVEL | BUNIT | TNULLn | TNULLn | ZVALi | FZALGn | PZEROn |
| AUTHOR | EQUINOX | BLANK | TTYPEn | TTYPEn | ZMASKCMP |  |  |
| REFERENC | $EPOCH^3$ | DATAMAX | TUNITn | TUNITn | ZQUANTIZ |  |  |
| COMMENT | $BLOCKED^3$ | DATAMIN | TDISPn | TDISPn | ZDITHER0 |  |  |
| HISTORY | $EXTEND^4$ |  | TDMAXn | TDIMn | ZSIMPLE | ZTHEAP |  |
| GOODSUSD | TELESCOP |  | TDMINn | THEAP | ZEXTEND |  |  |
| OBJECT | INSTRUME |  | TLMAXn | TDMAXn | ZBLOCKED |  |  |
| OBSERVER |  |  | TLMINn | TDMINn | ZTENSION |  |  |
| CONTINUE |  |  |  | TLMAXn | ZPCOUNT |  |  |
| $INHERIT ^5$ |  |  |  | TLMINn | ZGCOUNT |  |  |
| CHECKSUM |  |  |  |  | ZHECKSUM | ZHECKSUM |  |
| DATASUM |  |  |  |  | ZDATASUM | ZDATASUM |  |

54

<!-- page 61 of 75 -->

(<sup>1</sup>)Deprecated.

Table C.3: General reserved FITS keywords described in this document.

| Production | Bibliographic | Commentary | Observation |
| --- | --- | --- | --- |
| DATE | AUTHOR | COMMENT | DATE-OBS |
| ORIGIN | REFERENC | HISTORY | TELESCOP |
| BLOCKED$^{1}$ |  | OOOOOOO | INSTRUME |
|  |  |  | OBSERVER |
|  |  |  | OBJECT |
|  |  |  | EQUINOX |
|  |  |  | EPOCH$^{1}$ |

55

<!-- page 62 of 75 -->

Table D.1: ASCII character set.

<table><tr><td colspan="3">ASCII control</td><td colspan="9">ASCII text</td></tr><tr><td>dec</td><td>hex</td><td>char</td><td>dec</td><td>hex</td><td>char</td><td>dec</td><td>hex</td><td>char</td><td>dec</td><td>hex</td><td>char</td></tr><tr><td>0</td><td>00</td><td>NUL</td><td>32</td><td>20</td><td>SP</td><td>64</td><td>40</td><td>@</td><td>96</td><td>60</td><td>`</td></tr><tr><td>1</td><td>01</td><td>SOH</td><td>33</td><td>21</td><td>!</td><td>65</td><td>41</td><td>A</td><td>97</td><td>61</td><td>a</td></tr><tr><td>2</td><td>02</td><td>STX</td><td>34</td><td>22</td><td>&quot;</td><td>66</td><td>42</td><td>B</td><td>98</td><td>62</td><td>b</td></tr><tr><td>3</td><td>03</td><td>ETX</td><td>35</td><td>23</td><td>#</td><td>67</td><td>43</td><td>C</td><td>99</td><td>63</td><td>c</td></tr><tr><td>4</td><td>04</td><td>EOT</td><td>36</td><td>24</td><td>$</td><td>68</td><td>44</td><td>D</td><td>100</td><td>64</td><td>d</td></tr><tr><td>5</td><td>05</td><td>ENQ</td><td>37</td><td>25</td><td>%</td><td>69</td><td>45</td><td>E</td><td>101</td><td>65</td><td>e</td></tr><tr><td>6</td><td>06</td><td>ACK</td><td>38</td><td>26</td><td>&amp;</td><td>70</td><td>46</td><td>F</td><td>102</td><td>66</td><td>f</td></tr><tr><td>7</td><td>07</td><td>BEL</td><td>39</td><td>27</td><td>&#x27;</td><td>71</td><td>47</td><td>G</td><td>103</td><td>67</td><td>g</td></tr><tr><td>8</td><td>08</td><td>BS</td><td>40</td><td>28</td><td>(</td><td>72</td><td>48</td><td>H</td><td>104</td><td>68</td><td>h</td></tr><tr><td>9</td><td>09</td><td>HT</td><td>41</td><td>29</td><td>)</td><td>73</td><td>49</td><td>I</td><td>105</td><td>69</td><td>i</td></tr><tr><td>10</td><td>0A</td><td>LF</td><td>42</td><td>2A</td><td>*</td><td>74</td><td>4A</td><td>J</td><td>106</td><td>6A</td><td>j</td></tr><tr><td>11</td><td>0B</td><td>VT</td><td>43</td><td>2B</td><td>+</td><td>75</td><td>4B</td><td>K</td><td>107</td><td>6B</td><td>k</td></tr><tr><td>12</td><td>0C</td><td>FF</td><td>44</td><td>2C</td><td>,</td><td>76</td><td>4C</td><td>L</td><td>108</td><td>6C</td><td>l</td></tr><tr><td>13</td><td>0D</td><td>CR</td><td>45</td><td>2D</td><td>-</td><td>77</td><td>4D</td><td>M</td><td>109</td><td>6D</td><td>m</td></tr><tr><td>14</td><td>0E</td><td>SO</td><td>46</td><td>2E</td><td>.</td><td>78</td><td>4E</td><td>N</td><td>110</td><td>6E</td><td>n</td></tr><tr><td>15</td><td>0F</td><td>SI</td><td>47</td><td>2F</td><td>/</td><td>79</td><td>4F</td><td>O</td><td>111</td><td>6F</td><td>o</td></tr><tr><td>16</td><td>10</td><td>DLE</td><td>48</td><td>30</td><td>0</td><td>80</td><td>50</td><td>P</td><td>112</td><td>70</td><td>p</td></tr><tr><td>17</td><td>11</td><td>DC1</td><td>49</td><td>31</td><td>1</td><td>81</td><td>51</td><td>Q</td><td>113</td><td>71</td><td>q</td></tr><tr><td>18</td><td>12</td><td>DC2</td><td>50</td><td>32</td><td>2</td><td>82</td><td>52</td><td>R</td><td>114</td><td>72</td><td>r</td></tr><tr><td>19</td><td>13</td><td>DC3</td><td>51</td><td>33</td><td>3</td><td>83</td><td>53</td><td>S</td><td>115</td><td>73</td><td>s</td></tr><tr><td>20</td><td>14</td><td>DC4</td><td>52</td><td>34</td><td>4</td><td>84</td><td>54</td><td>T</td><td>116</td><td>74</td><td>t</td></tr><tr><td>21</td><td>15</td><td>NAK</td><td>53</td><td>35</td><td>5</td><td>85</td><td>55</td><td>U</td><td>117</td><td>75</td><td>u</td></tr><tr><td>22</td><td>16</td><td>SYN</td><td>54</td><td>36</td><td>6</td><td>86</td><td>56</td><td>V</td><td>118</td><td>76</td><td>v</td></tr><tr><td>23</td><td>17</td><td>ETB</td><td>55</td><td>37</td><td>7</td><td>87</td><td>57</td><td>W</td><td>119</td><td>77</td><td>w</td></tr><tr><td>24</td><td>18</td><td>CAN</td><td>56</td><td>38</td><td>8</td><td>88</td><td>58</td><td>X</td><td>120</td><td>78</td><td>x</td></tr><tr><td>25</td><td>19</td><td>EM</td><td>57</td><td>39</td><td>9</td><td>89</td><td>59</td><td>Y</td><td>121</td><td>79</td><td>y</td></tr><tr><td>26</td><td>1A</td><td>SUB</td><td>58</td><td>3A</td><td>:</td><td>90</td><td>5A</td><td>Z</td><td>122</td><td>7A</td><td>z</td></tr><tr><td>27</td><td>1B</td><td>ESC</td><td>59</td><td>3B</td><td>;</td><td>91</td><td>5B</td><td>[</td><td>123</td><td>7B</td><td>{</td></tr><tr><td>28</td><td>1C</td><td>FS</td><td>60</td><td>3C</td><td>&lt;</td><td>92</td><td>5C</td><td>\</td><td>124</td><td>7C</td><td>|</td></tr><tr><td>29</td><td>1D</td><td>GS</td><td>61</td><td>3D</td><td>=</td><td>93</td><td>5D</td><td>]</td><td>125</td><td>7D</td><td>}</td></tr><tr><td>30</td><td>1E</td><td>RS</td><td>62</td><td>3E</td><td>&gt;</td><td>94</td><td>5E</td><td>^</td><td>126</td><td>7E</td><td>~</td></tr><tr><td>31</td><td>1F</td><td>US</td><td>63</td><td>3F</td><td>?</td><td>95</td><td>5F</td><td>_</td><td>127</td><td>7F</td><td> $DEL^1$ </td></tr></table>

1 Not ASCII Text

## Appendix D: ASCII text

This appendix is not part of the FITS Standard; the material in it is based on the ANSI standard for ASCII (ANSI 1977) and is included here for informational purposes.)

In Table D.1, the first column is the decimal and the second column the hexadecimal value for the character in the third column. The characters hexadecimal 20 to 7E (decimal 32 to 126) constitute the subset referred to in this document as the restricted set of ASCII-text characters.

## Appendix E: IEEE floating-point formats

The material in this appendix is not part of this Standard; it is adapted from the IEEE-754 floating-point standard (IEEE 1985) and provided for informational purposes. It is not intended to be a comprehensive description of the IEEE formats; readers should refer to the IEEE standard.)

FITS recognizes all IEEE basic formats, including the special values.

## E.1. Basic formats

Numbers in the single and double formats are composed of the following three fields:

1. a one-bit sign s,

2. a biased exponent $e = E + b i a s .$ , and

3. a fraction $f = \bullet b_{1}b_{2}\cdots b_{p - 1}$

The range of the unbiased exponent E shall include every integer between two values $E _ { m i n }$ and $E _ { m a x } ,$ inclusive, and also two other reserved values $E _ { m i n } - 1$ to encode ±0 and denormalized numbers, and $E _ { m a x } { + } 1$ to encode **±∞** and NaNs. The foregoing parameters are given in Table E.1. Each nonzero numerical value has just one encoding. The fields are interpreted as follows.

56

<!-- page 63 of 75 -->

Table E.1: Summary of format parameters.

<table><tr><td rowspan="2">Parameter</td><td colspan="4">Format</td></tr><tr><td>Single</td><td>Single extended</td><td>Double</td><td>Double extended</td></tr><tr><td>p</td><td>24</td><td>≥ 32</td><td>53</td><td>≥ 64</td></tr><tr><td> $E_{max}$ </td><td>+127</td><td>≥ +1023</td><td>+1023</td><td>≥ +16383</td></tr><tr><td> $E_{min}$ </td><td>-126</td><td>≤ -1022</td><td>-1022</td><td>≤ -16382</td></tr><tr><td>Exponent bias</td><td>+127</td><td>unspecified</td><td>+1023</td><td>unspecified</td></tr><tr><td>Exponent width in bits</td><td>8</td><td>≥ 11</td><td>11</td><td>≥ 15</td></tr><tr><td>Format width in bits</td><td>32</td><td>≥ 43</td><td>64</td><td>≥ 79</td></tr></table>

Fig. E.1: Single Format. msb means most-significant bit, lsb means least-significant bit

| 1 | 8 | 23 | ....widths |
| --- | --- | --- | --- |
| s | e | f |  |
| msb | lsb | msb | lsb ....order |

Fig. E.2: Double Format. msb means most-significant bit, lsb means least-significant bit

| 1 | 11 | 52 | ....widths |
| --- | --- | --- | --- |
| s | e | f |  |
| msb | lsb | msb | lsb ....order |

## E.1.1. Single

A 32-bit single-format number X is divided as shown in Fig. E.1. The value v of X is inferred from its constituent fields.

1. If e = 255 and f , 0, then v is NaN regardless of s.

2. If e = 255 and f = 0, then v = (−1)<sup>s</sup>∞.

$$
\text {If} 0 <   e <   2 5 5, \text {then} v = (- 1) ^ {s} 2 ^ {e - 1 2 7} (1 \bullet f).
$$

4. $\mathrm { I f }   e = 0$ and f , 0, then $v = ( - 1 ) ^ { s } 2 ^ { e - 1 2 6 } ( 0 \bullet f )$ (denormalized numbers).

5. If e = 0 and f = 0, then v = (−1)s<sub>0</sub> (zero).

## E.1.2. Double

A 64-bit double-format number X is divided as shown in Fig. E.2. The value v of X is inferred from its constituent fields.

1. I $\mathbf { f }   e = 2 0 4 7$ and f , 0, then v is NaN regardless of s.

2. $\mathrm{If} e = 2047 \mathrm{and} f = 0, \mathrm{then} v = (-1)^s \infty.$

3. $\mathrm { I f } \; 0 < e < 2 0 4 7 , \mathrm { t h e n } \; \nu = ( - 1 ) ^ { s } 2 ^ { e - 1 0 2 3 } ( 1 \bullet f ) .$

4. If e = 0 and f , 0, then $v = ( - 1 ) ^ { s } 2 ^ { e - 1 0 2 2 } ( 0 \bullet f )$ (denormalized numbers).

5. If e = 0 and f = 0, then v = (−1)s<sub>0</sub> (zero).

## E.2. Byte patterns

Table E.2 shows the types of IEEE floating-point value, whether regular or special, corresponding to all double- and single-precision hexadecimal byte patterns.

57

<!-- page 64 of 75 -->

Table E.2: IEEE floating-point formats.

| IEEE value | Double precision | Single precision |
| --- | --- | --- |
| +0 | 00000000000000000 | 00000000 |
| denormalized | 00000000000000001 | 00000001 |
|  | to | to |
|  | 000FFFFFFF | 007FFFFF |
| positive underflow | 00100000000000000 | 00800000 |
| positive numbers | 00100000000000001 | 00800001 |
|  | to | to |
|  | 7FEFFFFFFF | 7F7FFFFE |
| positive overflow | 7FEFFFFFFF | 7F7FFFFF |
| +∞ | 7FF00000000000000 | 7F800000 |
| NaN$^1$ | 7FF00000000000001 | 7F800001 |
|  | to | to |
|  | 7FFFFFFF | 7FFFFFFF |
| -0 | 8000000000000000 | 80000000 |
| negative | 8000000000000001 | 80000001 |
| denormalized | to | to |
|  | 800FFFFFFF | 807FFFFF |
| negative underflow | 8010000000000000 | 80800000 |
| negative numbers | 8010000000000001 | 80800001 |
|  | to | to |
|  | FFEFFFFFFF | FF7FFFFE |
| negative overflow | FFEFFFFFFF | FF7FFFFF |
| -∞ | FFF00000000000000 | FF800000 |
| NaN$^1$ | FFF00000000000001 | FF800001 |
|  | to | to |
|  | FFFFFFF | FFFFFFF |

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">1 Certain values may be designated as quiet NaN (no diagnostic when used) or signaling (produces diagnostic when used) by particular implementations.</span></small>

58

<!-- page 65 of 75 -->

## Appendix F: Reserved extension type names

This appendix is not part of the FITS Standard, but is included for informational purposes. It describes the extension type names registered as of the date this Standard was issued.) A current list is available from the FITS Support Office website at [http://fits.gsfc.nasa.gov](http://fits.gsfc.nasa.gov).

## F.1. Standard extensions

These three extension types have been approved by the IAUFWG and are defined in Sect. 7 of this Standard document as well as in the indicated Astronomy and Astrophysics journal articles.

'IMAGE ' – This extension type provides a means of storing a multi-dimensional array similar to that of the FITS primary header and data unit. Approved as a standard extension in 1994 (Ponz et al. 1994).

'TABLE ' – This ASCII-table extension type contains rows and columns of data entries expressed as ASCII characters. Approved as a standard extension in 1988 (Harten et al. 1988).

'BINTABLE' – This binary-table extension type provides a more-flexible and efficient means of storing data structures than is provided by the TABLE extension type. The table rows can contain a mixture of numerical, logical, and character data entries. In addition, each entry is allowed to be a single-dimensioned array. Numeric data are kept in binary formats. Approved as a standard extension in 1994 (Cotton et al. 1995).

## F.2. Conforming extensions

These conventions meet the requirements for a conforming extension as defined in in Sect. 3.4.1 of this Standard, however they have not been formally approved or endorsed by the IAUFWG.

– 'IUEIMAGE' – This name was given to the prototype of the IMAGE extension type and was primarily used in the IUE project data archive from approximately 1992 to 1994. Except for the name, the format is identical to the IMAGE extension.

'A3DTABLE' – This name was given to the prototype of the BINTABLE extension type and was primarily used in the AIPS data processing system developed at NRAO from about 1987 until it was replaced by BINTABLE in the early 1990s. The format is defined in the ‘Going AIPS’ manual (Cotton et al. 1990), Chapter 14. It is very similar to the BINTABLE type except that it does not support the variablelength-array convention.

'FOREIGN ' – This extension type is used to put a FITS wrapper about an arbitrary file, allowing a file or tree of files to be wrapped up in FITS and later restored to disk. A full description of this extension type is given in the Registry of FITS conventions on the FITS Support Office website.

'DUMP ' – This extension type can be used to store a stream of binary-data values. The only known use of this extension type is to record telemetry header packets for data from the Hinode mission. The more-general FOREIGN extension type could also be used to store this type of data.

## F.3. Other suggested extension names

There have been occasional suggestions for other extension names that might be used for other specific purposes. These include a COMPRESS extension for storing compressed images, a FITS extension for hierarchically embedding entire FITS files within other FITS files, and a FILEMARK extension for representing the equivalent of an end-of-file mark on magnetic-tape media. None of these extension types have been implemented or used in practice, therefore these names are not reserved. These extension names (or any other extension name not specifically mentioned in the previous sections of this appendix) should not be used in any FITS file without first registering the name with the IAU FITS Working Group.

## Appendix G: MIME types

This appendix is not part of the FITS Standard, but is included for informational purposes.

RFC 4047 (Allen & Wells 2005) describes the registration of the Multipurpose Internet Mail Extensions (MIME) sub-types application/fits’ and ‘image/fits’ to be used by the international astronomical community for the interchange of FITS files. The MIME type serves as a electronic tag or label that is transmitted along with the FITS file that tells the receiving application what type of file is being transmitted. The remainder of this appendix has been extracted verbatim from the RFC 4047 document.

The general nature of the full FITS Standard requires the use of the media type ‘application/fits’. Nevertheless, the principal intent for a great many FITS files is to convey a single data array in the primary HDU, and such arrays are very often two-dimensional images. Several common image viewing applications already display single-HDU FITS files, and the prototypes for virtual-observatory projects specify that data provided by web services be conveyed by the data array in the primary HDU. These uses justify the registration of a second media type, namely ‘image/fits’, for files that use the subset of the Standard described by the original FITS Standard paper. The MIME type ‘image/fits’ may be used to describe FITS primary HDUs that have other than two dimensions, however it is expected that most files described as ‘image/fits’ will have two-dimensional (NAXIS = 2) primary HDUs.

## G.1. MIME type 'application/fits'

A FITS file described with the media type ‘application/fits’ should conform to the published standards for FITS files as determined by convention and agreement within the international FITS community. No other constraints are placed on the content of a file described as ‘application/fits’.

A FITS file described with the media type application/fits’ may have an arbitrary number of conforming extension HDUs that follow its mandatory primary header and data unit. The extension HDUs may be one of the standard types (IMAGE, TABLE, and BINTABLE) or any other type that satisfies the ‘Requirements for conforming extensions’ (Sect. 3.4.1). The primary HDU or any IMAGE extension may contain zero to 999 dimensions with zero-or-more pixels along each dimension.

59

<!-- page 66 of 75 -->

The primary HDU may use the random-groups convention, in which the dimension of the first axis is zero and the keywords GROUPS. PCOUNT and GCOUNT appear in the header. NAXIS1 = 0 and GROUPS = T is the signature of random groups; see Sect. 6.

## G.1.1. Recommendations for application writers

An application intended to handle ‘application/fits’ should be able to provide a user with a manifest of all of the HDUs that are present in the file and with all of the keyword/value pairs from each of the HDUs.

An application intended to handle ‘application/fits’ should be prepared to encounter extension HDUs that contain either ASCII or binary tables, and to provide a user with access to their elements.

An application that can modify FITS files or retrieve FITS files from an external service should be capable of writing such files to a local storage medium.

Complete interpretation of the meaning and intended use of the data in each of the HDUs typically requires the use of heuristics that attempt to ascertain which local conventions were used by the author of the FITS file.

As examples, files with media type ‘application/fits might contain any of the following contents.

– An empty primary HDU (containing zero data elements) followed by a table HDU that contains a catalog of celestial objects.

– An empty primary HDU followed by a TABLE HDU that encodes a series of time-tagged photon events from an exposure using an X-ray detector.

– An empty primary HDU followed by a series of IMAGE HDUs containing data from an exposure taken by a mosaic of CCD detectors.

– An empty primary HDU followed by a series of TABLE HDUs that contain a snapshot of the state of a relational database.

– A primary HDU containing a single image along with keyword/value pairs of metadata.

– A primary HDU with NAXIS1 = 0 and GROUPS = T followed by random-groups data records of complex fringe visibilities.

## G.2. MIME type image/fits

A FITS file described with the media type ‘image/fits’ should have a primary HDU with positive integer values for the NAXIS and NAXISn keywords, and hence should contain at least one pixel. Files with four or more non-degenerate axes (NAXISn > 1) should be described as ‘application/fits’, not as ‘image/fits’. (In rare cases it may be appropriate to describe a NULL image – a dataless container for FITS keywords, with NAXIS = 0 or NAXISn = 0 – or an image with four or more non-degenerate axes as ‘image/fits’ but this usage is discouraged because such files may confuse simple image-viewer applications.)

FITS files declared as ‘image/fits’ may also have one or more conforming extension HDUs following their primary HDUs. These extension HDUs may contain standard, non-linear, world-coordinate system (WCS) information in the form of tables or images. The extension HDUs may also contain other,

non-standard metadata pertaining to the image in the primary HDU in the forms of keywords and tables.

A FITS file described with the media type ‘image/fits’ should be principally intended to communicate the single data array in the primary HDU. This means that ‘image/fits should not be applied to FITS files containing multi-exposureframe mosaic images. Also, random-groups files must be described as ‘application/fits’ and not as ‘image/fits’.

A FITS file described with the media type ‘image/fits’ is also valid as a file of media type ‘application/fits’. The choice of classification depends on the context and intended usage.

## G.2.1. Recommendations for application writers

An application that is intended to handle ‘image/fits’ should be able to provide a user with a manifest of all of the HDUs that are present in the file and with all of the keyword/value pairs from each of the HDUs. An application writer may choose to ignore HDUs beyond the primary HDU, but even in this case the application should be able to present the user with the keyword/value pairs from the primary HDU.

Note that an application intended to render ‘image/fits for viewing by a user has significantly more responsibility than an application intended to handle, e.g., ’image/tiff’ or’image/gif’. FITS data arrays contain elements that typically represent the values of a physical quantity at some coordinate location. Consequently they need not contain any pixel rendering information in the form of transfer functions, and there is no mechanism for color look-up tables. An application should provide this functionality, either statically using a more- or lesssophisticated algorithm, or interactively allowing a user various degrees of choice.

Furthermore, the elements in a FITS data array may be integers or floating-point numbers. The dynamic range of the data-array values may exceed that of the display medium and the eye, and their distribution may be highly non-uniform. Logarithmic, square-root, and quadratic transfer functions along with histogram-equalization techniques have proved helpful for rendering FITS data arrays. Some elements of the array may have values that indicate that their data are undefined or invalid; these should be rendered distinctly. Via WCS Paper I (Greisen & Calabretta 2002) the Standard permits CTYPEn = ’COMPLEX’ to assert that a data array contains complex numbers (future revisions might admit other elements such as quaternions or general tensors).

Three-dimensional data arrays (NAXIS = 3 with NAXIS1, NAXIS2, and NAXIS3 all greater than 1) are of special interest. Applications intended to handle ‘image/fits’ may default to displaying the first two-dimensional plane of such an image cube, or they may default to presenting such an image in a fashion akin to that used for an animated GIF, or they may present the data cube as a mosaic of ‘thumbnail’ images. The time-lapse movie-looping display technique can be effective in many instances, and application writers should consider offering it for all three-dimensional arrays.

An ‘image/fits’ primary HDU with NAXIS = 1 is describing a one-dimensional entity such as a spectrum or a time series. Applications intended to handle ‘image/fits’ may default to displaying such an image as a graphical plot rather than as a two-dimensional picture with a single row.

60

<!-- page 67 of 75 -->

An application that cannot handle an image with dimensionality other than two should gracefully indicate its limitations to its users when it encounters NAXIS = 1 or NAXIS = 3 cases, while still providing access to the keyword/value pairs.

FITS files with degenerate axes (i.e., one or more NAXISn = 1) may be described as ‘image/fits’, but the first axes should be non-degenerate (i.e., the degenerate axes should be the highest dimensions). An algorithm designed to render only two-dimensional images will be capable of displaying such an $\mathrm{NAXIS} = 3 \mathrm{or} \mathrm{NAXIS} = 4 \mathrm{FITS}$ array that has one or two of the axes consisting of a single pixel, and an application writer should consider coding this capability into the application. Writers of new applications that generate FITS files intended to be described as ‘image/fits’ should consider using the WCSAXES keyword (Greisen et al. 2006) to declare the dimensionality of such degenerate axes, so that NAXIS can be used to convey the number of non-degenerate axes.

## G.3. File extensions

The FITS Standard originated in the era when files were stored and exchanged via magnetic tape; it does not prescribe any nomenclature for files on disk. Various sites within the FITS community have long-established practices where files are pre-sumed to be FITS by context. File extensions used at such sites commonly indicate content of the file instead of the data format.

In the absence of other information it is reasonably safe to presume that a file name ending in ‘.fits’ is intended to be a FITS file. Nevertheless, there are other commonly used extensions; e.g., ‘.fit’, ‘.fts’, and many others not suitable for listing in a media type registration.

## Appendix H: Past changes or clarifications to the formal definition of FITS

This appendix is not part of the FITS Standard, but is included for informational purposes.

## H.1. Differences between the requirements in this Standard and the requirements in the original FITS papers.

1. Sect. 4.1.2: The original FITS definition paper (Wells et al. 1981) disallows lower-case letters in the keyword name, but does not specify what other characters may or may not appear in the name.

2. Sect. 4.1.2: The slash between the value and comment is ‘recommended’ in the original paper (Wells et al. 1981) whereas the Standard requires that it be present, which is consistent with the prescription of Fortran list-directed input.

3. Sect. 4.2: The original paper (Wells et al. 1981) speculated that FITS would eventually support the full range of flexibility that is allowed by Fortran list-directed input, including dimensioned parameters. The Standard restricts the value field to a single value, not an array.

4. Sect. 4.2.5 and Sect. 4.2.6: The original paper (Wells et al. 1981) defined a fixed format for complex keyword values, with the real part right justified in Bytes 11 through 30 and the imaginary part right justified in Bytes 31 through 50. There are no known FITS files that use this fixed format. The Standard does not define a fixed format for complex keyword values. Instead, complex values are represented in

conformance with the rules for Fortran list-directed input, namely, with the real and imaginary parts separated by a comma and enclosed in parentheses.

5. Sect. 4.4.1.1 and Sect. 4.4.1.2: The paper that defines generalized extensions (Grosbøl et al. 1988) does not prohibit the appearance of the SIMPLE keyword in extensions nor the XTENSION keyword in the primary header.

## H.2. List of modification to the FITS Standard, Version 3.0

After the IAUFWG officially approved Version 3.0 of the FITS Standard in 2008, the following additional corrections, clarifications, or format modifications have been made to the document.

1. Two typographical errors in Table 21 (previously Table 8.1) were corrected. The last two lines of the third column should read ‘LONPOLEa (= PVi 3a)’ and ‘LATPOLEa (= PVi 4a)’), instead of PVi 1a and PVi 2a, respectively. (October 2008)

2. The LATEX text source document was reformatted to conform to the Astronomy & Astrophysics journal page style (June 2010). The visible changes include the following.

– The tables, figures, equations, and footnotes are numbered sequentially throughout the entire the document, instead of sequentially within each chapter.

– The citations use the standard ‘Author (year)’ format instead of being referenced by a sequential number. Also, the ‘Bibliography’ section at the end of the document has been replaced by a ‘References’ section in which the citations are listed alphabetically by author.

3. The following minor corrections or clarifications were made during the refereeing process after submitting Version 3.0 of the FITS Standard for publication in the Astronomy & Astrophysics journal (July 2010).

– A sentence was added to the end of Sect. 1.2: ‘This website also contains the contact information for the Chairman of the IAUFWG, to whom any questions or comments regarding this Standard should be addressed.

– A ‘Section’ column was added to Table 1 to reference the relevant section of the document.

– The wording of the second sentence in Sect. 4.1.1 was revised from ‘Except where specifically stated otherwise in this standard, keywords may appear in any order.’ to ‘Keywords may appear in any order except where specifically stated otherwise in this Standard.

– A sentence was added to the end of the ‘Keyword name subsection in Sect. 4.1.2: ‘Note that keyword names that begin with (or consist solely of) any combination of hyphens, underscores, and digits are legal.’

– A footnote to the description of the REFERENC keyword in Sect. 4.4.2 was added: ‘This bibliographic convention (Schmitz 1995) was initially developed for use within NED (NASA/IPAC Extragalactic Database) and SIMBAD (operated at CDS, Strasbourg, France).

– In Sect. 7.3.4, the phrase ‘TFORMn format code’ was corrected to read ‘TDISPn format code’ (in four places).

– The wording in the ‘Expressed as’ column in Table 26 for the LOG, GRI, GRA, and TAB spectral algorithm codes was clarified.

– In Table C.2 the EXTNAME, EXTVER, and EXTLEVEL keywords were moved under the ‘All HDUs’ column because they are now allowed in the primary array header.

61

<!-- page 68 of 75 -->

– The last paragraph of Sect. 4.1.2.3 was corrected to state that the ASCII-text characters have hexadecimal values 20 through 7E, not 41 through 7E.

## H.3. List of modifications to the latest FITS Standard

1. The representation of time coordinates has been incorporated by reference from Rots et al. (2015) and is summarized in Sect. 9. Cross-references have been inserted in pre-existing sections of the Standard (namely in Sects. 4.2.7, 4.3, 4.4.2.1, 4.4.2.2 and 5.4, as well as in various places of Sect. 8, such as Sect. 8.3 and Sect. 8.4.1). New keywords are listed in a rearranged Table 22. Contextually an erratum was applied in Sect. 8.4.1: keywords OBSGEO-[XYZ] were incorrectly marked as OBSGEO-[XYZ]a; the TAI-UTC difference in Table 30 was updated with respect to Rots et al. (2015) taking into account the latest leap second; the possibility of introducing more sources for the Solar System ephemerides was re-worded (at the end of Sect.9.2.5 and in Table 31).

2. The continued string keywords described in Sect. 4.2.1.2 were originally introduced as a FITS convention during 1994, and registered in 2007. The text of the original convention is reported at [http://fits.gsfc.nasa.gov/registry/continue\_keyword.html](http://fits.gsfc.nasa.gov/registry/continue_keyword.html). The differences with this Standard concern the following.

– In the convention, the LONGSTRN keyword was used to signal the possible presence of long strings in the HDU. The use of this keyword is no longer required or recommended.

– Usage of the convention was not recommended for reserved or mandatory keywords. Now it is explicitly forbidden unless keywords are explicitly declared longstring.

– To avoid ambiguities in the application of the previous clause, the declaration of string keywords in Sects. 8, 9 and 10 has been reset from the generic ‘character’ to ‘string’.

– It is also explicitly clarified there is no limit to the number of continuation records.

– The description of continued comment field is new.

3. The blank header space convention described in Sect. 4.4.2.4 was used from 1996, and registered in 2014. The text of the original convention is reported at [http://fits.gsfc.nasa.gov/registry/headerspace.html](http://fits.gsfc.nasa.gov/registry/headerspace.html). It included a recommendation about using the convention in a controlled environment, which does not appear in this Standard.

4. The INHERIT keyword described in Sect. 4.4.2.6 was originally introduced as a FITS convention in 1995, and registered in 2007. The text of the original convention is reported at [http://fits.gsfc.nasa.gov/registry/inherit.html](http://fits.gsfc.nasa.gov/registry/inherit.html). See also references and practical considerations therein. The differences with the present document concern a more-precise RFC 2119 compliant wording in a couple of sentences in Appendix K.

5. The checksum keywords described in Sect. 4.4.2.7 were originally introduced as a FITS convention during 1994, and registered in 2007. The text of the original convention is reported at [http://fits.gsfc.nasa.gov/registry/checksum.html](http://fits.gsfc.nasa.gov/registry/checksum.html). The differences with this Standard concern:

– the omission of some additional implementation guidelines, and

– the omission of a discussion on alternate algorithms and relevant additional references.

6. The table keywords described in Sect. 7.2.2 and 7.3.2 were originally introduced as a FITS convention during 1993, and registered in 2006. The text of the original convention is reported at [http://fits.gsfc.nasa.gov/registry/colminmax.html](http://fits.gsfc.nasa.gov/registry/colminmax.html). The differences with this Standard are as follows.

– The exclusion of undefined or IEEE special values when computing maximum and minimum is now mandatory while it was optional.

– The original text included the possibility of using the fact TDMINn were greater than TDMAXn (or TLMINn greater than TLMAXn) as an indication the values were undefined. This clause has been removed

– The original text contained usage examples and additional minor explanatory details.

7. The Green Bank convention, mentioned in Sect. 8.2 and described in Appendix L, has been in use since 1989, and was registered in 2010. The text of the registered convention is reported at [http://fits.gsfc.nasa.gov/registry/greenbank/greenbank.pdf](http://fits.gsfc.nasa.gov/registry/greenbank/greenbank.pdf) and contains some additional details about the history of the convention.

8. The conventions for compressed data described in Sect. 10. were originally introduced as a couple of FITS conventions registered in 2007 and 2013. The text of the original conventions is reported at [http://fits.gsfc.nasa.gov/registry/tilecompression.html](http://fits.gsfc.nasa.gov/registry/tilecompression.html) for compressed images and at [http://fits.gsfc.nasa.gov/registry/tiletablecompression.html](http://fits.gsfc.nasa.gov/registry/tiletablecompression.html) for compressed binary tables. The differences with this Standard are listed below.

– In Sect. 10.3.3 the original text for FZALGn mentioned the possibility that, ‘If the column cannot be compressed with the requested algorithm (e.g., if it has an inappropriate data type), then a default compression algorithm will be used instead.’ But there is no default algorithm. This is irrelevant for the Standard.

– In Sect. 10.4 the alias ’RICE ONE’ is not adopted in the Standard as a synonym for ’RICE 1’.

– In Sect. 10.4.3 a sentence was left out about requiring additional instructions in PLIO to make it work for more then 2<sup>12</sup> bits, since we aren’t allowing this possibility in the Standard.

– In Sect. 10.4.4 the reference to a ‘smoothing flag’ was dropped.

– Also in Sect. 10.4.4 the scale factor is now floating point, while it was originally integer.

– In Table 36 (and Sect. 10.3.5) the ’NOCOMPRESS’ algorithm is explicitly mentioned.

## H.4. List of modifications for language editing

1. Apply systematically LATEX macros for keyword names and values, and for RFC 2119 expressions, according to instructions reported in the LATEX source preamble (for future editors of the Standard).

2. The acronym FITS is always indicated in italics.

3. Use italics systematically for RFC 2119 obligations and recommendations.

62

<!-- page 69 of 75 -->

4. Apply consistent use of italic and typewriter fonts, and ’ quotation marks around literal keyword values. Correct other minor LATEX issues.

5. Apply systematic capitalization of the names of specific entities, where appropriate. These include Standard (when referring to the FITS Standard document), Version (where numbered), Byte, Column, Parameter, Field, and Axis. Start some words with a lower-case letter that previously began with a capital letter.

6. Address other typographical issues, such as the insertion of commas in several places, adding a few non-breaking spaces, and better handling of references to sections, etc.

7. Several cases of minor rewording.

8. Express small numbers in letter form (one to nine), not in numerals (1 to 9), wherever sensible. However, there is the customary exception for normalization in sentences and headings that also contain numbers greater than nine.

9. Compound nouns are systematically hyphenated to highlight the correct grouping (and hence meaning) of the components. This includes the attributive references to ASCII-table, binary-table, and random-groups.

10. Improve the aesthetics of some tables.

## Appendix I: Random-number generator

This appendix is not part of the FITS Standard, but is included for informational purposes.

The portable random-number generator algorithm below is from Park & Miller (1988). This algorithm repeatedly evaluates the function

$$
s e e d = (a * s e e d) \bmod m
$$

where the values of a and m are shown below, but it is implemented in a way to avoid integer overflow problems.

int random\_generator(void) {

/\* initialize an array of random numbers \*/

```c
int ii;
    double a = 16807.0;
    double m = 2147483647.0;
    double temp, seed;
    float rand_value[10000];

    /* initialize the random numbers */
    seed = 1;
    for (ii = 0; ii < N_RANDOM; ii++) {
        temp = a * seed;
        seed = temp -m * ((int) (temp / m) );
        /* divide by m for value between 0 and 1 */
        rand_value[ii] = seed / m;
    }
}
```

If implemented correctly, the 10 000<sup>th</sup> value of seed will equal 1 043 618 065.

## Appendix J: CHECKSUM implementation guidelines

This appendix is not part of the FITS Standard, but is included for informational purposes.

## J.1. Recommended CHECKSUM keyword implementation

The recommended CHECKSUM keyword algorithm described here generates a 16-character ASCII string that forces the 32-bit ones’ complement checksum accumulated over the entire FITS HDU to equal negative 0 (all 32 bits equal to 1). In addition, this string will only contain alphanumeric characters within the ranges 0–9, A–Z, and a–z to promote human readability and transcription. If the present algorithm is used, the CHECKSUM keyword value must be expressed in fixed format, with the starting single-quote character in Column 11 and the ending single-quote character in Column 28 of the FITS keyword record, because the relative placement of the value string within the keyword record affects the computed HDU checksum. The steps in the algorithm are as follows.

1. Write the CHECKSUM keyword into the HDU header with an initial value consisting of 16 ASCII zeros (’0000000000000000’) where the first single-quote character is in Column 11 of the FITS keyword record. This specific initialization string is required by the encoding algorithm described in Sect. J.2. The final comment field of the keyword, if any, must also be written at this time. It is recommended that the current date and time be recorded in the comment field to document when the checksum was computed.

2. Accumulate the 32-bit ones’ complement checksum over the FITS logical records that make up the HDU header in the same manner as was done for the data records by interpreting each 2880-byte logical record as 720 32-bit unsigned integers.

3. Calculate the checksum for the entire HDU by adding (using ones’ complement arithmetic) the checksum accumulated over the header records to the checksum accumulated over the data records (i.e., the previously computed DATASUM keyword value).

4. Compute the bit-wise complement of the 32-bit total HDU checksum value by replacing all 0 bits with 1 and all 1 bits with 0.

5. Encode the complement of the HDU checksum into a 16- character ASCII string using the algorithm described in Sect. J.2

6. Replace the initial CHECKSUM keyword value with this 16- character encoded string. The checksum for the entire HDU will now be equal to negative 0.

## J.2. Recommended ASCIl encoding algorithm

The algorithm described here is used to generate an ASCII string, which, when substituted for the value of the CHECKSUM keyword, will force the checksum for the entire HDU to equal negative 0. It is based on a fundamental property of ones’ complement arithmetic that the sum of an integer and the negation of that integer (i.e, the bitwise complement formed by replacing all 0 bits with 1s and all 1 bits with 0s) will equal negative 0 (all bits set to 1). This principle is applied here by constructing a 16-character string, which, when interpreted as a byte stream of four 32-bit integers, has a sum that is equal to the complement of the sum accumulated over the rest of the HDU. This algorithm also ensures that the 16 bytes that make up the four integers all have values that correspond to ASCII alpha-numeric characters in the range 0–9, A–Z, and a–z.

63

<!-- page 70 of 75 -->

Fig. J.1: Only ASCII alpha-numeric characters are used to encode the checksum – punctuation is excluded

| 030 | 131 | 232 | 333 | 434 | 535 | 636 | 737 | 838 | 939 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| :3a | ;3b | &lt;3c | =3d | >3e | ?3f | @40 | A41 | B42 | C43 |
| D44 | E45 | F46 | G47 | H48 | I49 | J4a | K4b | L4c | M4d |
| N4e | O4f | P50 | Q51 | R52 | S53 | T54 | U55 | V56 | W57 |
| X58 | Y59 | Z5a | [5b | \\5c] | ]5d | ^5e | _5f | '60 | a61 |
| b62 | c63 | d64 | e65 | f66 | g67 | h68 | i69 | j6a | k6b |
| l6c | m6d | n6e | o6f | p70 | q71 | r72 |  |  |  |

1. Begin with the ones’ complement (replace 0s with 1s and 1s with 0s) of the 32-bit checksum accumulated over all the FITS records in the HDU after first initializing the CHECKSUM keyword with a fixed-format string consisting of 16 ASCII zeros (’0000000000000000’).

2. Interpret this complemented 32-bit value as a sequence of four unsigned eight-bit integers, A, B, C, and D, where A is the most-significant byte and D is the least-significant byte. Generate a sequence of four integers, A1, A2, A3, A4, that are all equal to A divided by 4 (truncated to an integer if necessary). If A is not evenly divisible by 4, add the remainder to A1. The key property to note here is that the sum of the four new integers is equal to the original byte value (e.g., $A = A 1 + A 2 + A 3 + A \dot { 4 } )$ . Perform a similar operation on B, C, and D, resulting in a total of 16 integer values, four from each of the original bytes, which should be rearranged in the following order:

## A1 B1 C1 D1 A2 B2 C2 D2 A3 B3 C3 D3 A4 B4 C4 D4.

Each of these integers represents one of the 16 characters in the final CHECKSUM keyword value. Note that if this byte stream is interpreted as four 32-bit integers, the sum of the integers is equal to the original complemented checksum value.

3. Add 48 (hex 30), which is the value of an ASCII zero character, to each of the 16 integers generated in the previous step. This places the values in the range of ASCII alphanumeric characters ’0’ (ASCII zero) to ’r’. This offset is effectively subtracted back out of the checksum when the initial CHECKSUM keyword value string of 16 ASCII 0s is replaced with the final encoded checksum value.

4. To improve human readability and transcription of the string, eliminate any non-alphanumeric characters by considering the bytes a pair at a time (e.g., A1 + A2, A3 + A4, B1 + B2, etc.) and repeatedly increment the first byte in the pair by 1 and decrement the second byte by 1 as necessary until they both correspond to the ASCII value of the allowed alphanumeric characters 0–9, A–Z, and a–z shown in Figure J.1. Note that this operation conserves the value of the sum of the four equivalent 32-bit integers, which is required for use in this checksum application.

5. Cyclically shift all 16 characters in the string one place to the right, rotating the last character (D4) to the beginning of the string. This rotation compensates for the fact that the fixed format FITS character-string values are not aligned on fourbyte word boundaries in the FITS file. (The first character of the string starts in Column 12 of the header card image, rather than Column 13).

6. Write this string of 16 characters to the value of the CHECKSUM keyword, replacing the initial string of 16 ASCII zeros.

To invert the ASCII encoding, cyclically shift the 16 characters in the encoded string one place to the left, subtract the hex 30 offset from each character, and calculate the checksum by interpreting the string as four 32-bit unsigned integers. This can be used, for instance, to read the value of CHECKSUM into the software when verifying or updating a HDU.

## J.3. Encoding example

This example illustrates the encoding algorithm given in Sect. J.2 Consider a FITS HDU whose ones’ complement checksum is 868229149, which is equivalent to hex 33C0201D. This number was obtained by accumulating the 32-bit checksum over the header and data records using ones’ complement arithmetic after first initializing the CHECKSUM keyword value to’0000000000000000’. The complement of the accumulated checksum is 3426738146, which is equivalent to hex CC3FDFE2. The steps needed to encode this hex value into ASCII are shown schematically below.

<table><tr><td colspan="4">Byte</td><td colspan="14">Preserve byte alignment</td><td></td><td></td></tr><tr><td>A</td><td>B</td><td>C</td><td>D</td><td>A1</td><td>B1</td><td>C1</td><td>D1</td><td>A2</td><td>B2</td><td>C2</td><td>D2</td><td>A3</td><td>B3</td><td>C3</td><td>D3</td><td>A4</td><td>B4</td><td>C4</td><td>D4</td></tr><tr><td>CC</td><td>3F</td><td>DF</td><td>E2 -&gt;</td><td>33</td><td>0F</td><td>37</td><td>38</td><td>33</td><td>0F</td><td>37</td><td>38</td><td>33</td><td>0F</td><td>37</td><td>38</td><td>33</td><td>0F</td><td>37</td><td>38</td></tr><tr><td>+</td><td colspan="3">remainder</td><td>0</td><td>3</td><td>3</td><td>2</td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr><tr><td></td><td colspan="3">= hex</td><td>33</td><td>12</td><td>3A</td><td>3A</td><td>33</td><td>0F</td><td>37</td><td>38</td><td>33</td><td>0F</td><td>37</td><td>38</td><td>33</td><td>0F</td><td>37</td><td>38</td></tr><tr><td></td><td colspan="3">+ 0 offset</td><td>30</td><td>30</td><td>30</td><td>30</td><td>30</td><td>30</td><td>30</td><td>30</td><td>30</td><td>30</td><td>30</td><td>30</td><td>30</td><td>30</td><td>30</td><td>30</td></tr><tr><td></td><td colspan="3">= hex</td><td>63</td><td>42</td><td>6A</td><td>6A</td><td>63</td><td>3F</td><td>67</td><td>68</td><td>63</td><td>3F</td><td>67</td><td>68</td><td>63</td><td>3F</td><td>67</td><td>68</td></tr><tr><td></td><td colspan="3">ASCII</td><td>c</td><td>B</td><td>j</td><td>j</td><td>c</td><td>?</td><td>g</td><td>h</td><td>c</td><td>?</td><td>g</td><td>h</td><td>c</td><td>?</td><td>g</td><td>h</td></tr><tr><td colspan="20">Eliminate punctuation characters</td></tr><tr><td colspan="4">initial values</td><td>c</td><td>B</td><td>j</td><td>j</td><td>c</td><td>?</td><td>g</td><td>h</td><td>c</td><td>?</td><td>g</td><td>h</td><td>c</td><td>?</td><td>g</td><td>h</td></tr><tr><td></td><td colspan="3">.</td><td>c</td><td>C</td><td>j</td><td>j</td><td>c</td><td>&gt;</td><td>g</td><td>h</td><td>c</td><td>@</td><td>g</td><td>h</td><td>c</td><td>&gt;</td><td>g</td><td>h</td></tr><tr><td></td><td colspan="3">.</td><td>c</td><td>D</td><td>j</td><td>j</td><td>c</td><td>=</td><td>g</td><td>h</td><td>c</td><td>A</td><td>g</td><td>h</td><td>c</td><td>=</td><td>g</td><td>h</td></tr><tr><td></td><td colspan="3">.</td><td>c</td><td>E</td><td>j</td><td>j</td><td>c</td><td>&lt;</td><td>g</td><td>h</td><td>c</td><td>B</td><td>g</td><td>h</td><td>c</td><td>&lt;</td><td>g</td><td>h</td></tr><tr><td></td><td colspan="3">.</td><td>c</td><td>F</td><td>j</td><td>j</td><td>c</td><td>;</td><td>g</td><td>h</td><td>c</td><td>C</td><td>g</td><td>h</td><td>c</td><td>;</td><td>g</td><td>h</td></tr><tr><td></td><td colspan="3">.</td><td>c</td><td>G</td><td>j</td><td>j</td><td>c</td><td>:</td><td>g</td><td>h</td><td>c</td><td>D</td><td>g</td><td>h</td><td>c</td><td>:</td><td>g</td><td>h</td></tr><tr><td colspan="4">final values</td><td>c</td><td>H</td><td>j</td><td>j</td><td>c</td><td>9</td><td>g</td><td>h</td><td>c</td><td>E</td><td>g</td><td>h</td><td>c</td><td>9</td><td>g</td><td>h</td></tr></table>

final string "hcHjjc9ghcEghc9g" (rotate 1 place to the right)

In this example Byte B1 (originally ASCII B) is shifted higher (to ASCII H) to balance Byte B2 (originally ASCII ?) being shifted lower (to ASCII 9). Similarly, Bytes B3 and B4 are shifted by opposing amounts. This is possible because the two sequences of ASCII punctuation characters that can occur in encoded checksums are both preceded and followed by longer sequences of ASCII alphanumeric characters. This operation is purely for cosmetic reasons to improve readability of the final string.

This is how these CHECKSUM and DATASUM keywords would appear in a FITS header (with the recommended time stamp in the comment field).

## J.4. Incremental updating of the checksum

The symmetry of ones’ complement arithmetic also means that after modifying a FITS HDU, the checksum may be incrementally updated using simple arithmetic without accumulating the checksum for portions of the HDU that have not changed. The

64

<!-- page 71 of 75 -->

new checksum is equal to the old total checksum plus the checksum accumulated over the modified records, minus the original checksum for the modified records.

An incremental update provides the mechanism for end-to-end checksum verification through any number of intermediate processing steps. By calculating rather than accumulating the intermediate checksums, the original checksum test is propagated through to the final data file. On the other hand, if a new checksum is accumulated with each change to the HDU, no information is preserved about the HDU’s original state.

The recipe for updating the CHECKSUM keyword following some change to the HDU is: $C ^ { \prime } ~ = ~ C   -   m ^ { ' } +   m ^ { \prime }$ , where C and C′represent the HDU’s checksum (that is, the complement of the CHECKSUM keyword) before and after the modification and m and m′are the corresponding checksums for the modified FITS records or keywords only. Since the CHECKSUM keyword contains the complement of the checksum, the correspondingly complemented form of the recipe is more directly useful: $\widetilde { { } ^ { \prime } C ^ { \prime } } = \widetilde { { } ^ { \prime } } ( \widetilde { C + { } ^ { \prime } m + m ^ { \prime } } )$ , where ˜ (tilde) denotes the (ones’) complement operation. See Braden et al. (1988); Mallory & Kullberg (1990); Rijsinghani (1994). Note that the tilde on the right hand side of the equation cannot be distributed over the contents of the parentheses due to the dual nature of zero in ones’ complement arithmetic (Rijsinghani 1994).

## J.5. Example C code for accumulating the checksum

The ones’ complement checksum is simple and fast to compute. This routine assumes that the input records are a multi-ple of four bytes long (as is the case for FITS logical records), but it is not difficult to allow for odd length records if necessary. To use this routine, first initialize the CHECKSUM keyword to ’0000000000000000’ and initialize sum32 = 0, then step through all the FITS logical records in the FITS HDU.

```c
void checksum (
    unsigned char *buf, /* Input array of bytes to be checksummed */
        /* (interpret as 4-byte unsigned ints) */
    int length,      /* Length of buf array, in bytes */
        /* (must be multiple of 4) */
    unsigned int *sum32) /* 32-bit checksum */
{
/*
Increment the input value of sum32 with the 1's complement sum
accumulated over the input buf array.
*/
unsigned int hi, lo, hicarry, locarry, i;

/* Accumulate the sum of the high-order 16 bits and the */
/* low-order 16 bits of each 32-bit word, separately. */
/* The first byte in each pair is the most significant. */
/* This algorithm works on both big and little endian machines.*/
hi = (*sum32 >> 16);
lo = *sum32 & 0xFFFF;
for (i=0; i < length; i+=4) {
    hi += ((buf[i] << 8) + buf[i+1]);
    lo += ((buf[i+2] << 8) + buf[i+3]);
}

/* fold carry bits from each 16 bit sum into the other sum */
hicarry = hi >> 16;
locarry = lo >> 16;
while (hicarry || locarry) {
    hi = (hi & 0xFFFF) + locarry;
    lo = (lo & 0xFFFF) + hicarry;
    hicarry = hi >> 16;
    locarry = lo >> 16;
}

/* concatenate the full 32-bit value from the 2 halves */
*sum32 = (hi << 16) + lo;
}
```

## J.6. Example C code for ASCIl encoding

This routine encodes the complement of the 32-bit HDU checksum value into a 16-character string. The byte alignment of the string is permuted one place to the right for FITS to left justify the string value starting in Column 12.

```c
unsigned int exclude[13] = {0x3a, 0x3b, 0x3c, 0x3d, 0x3e, 0x3f, 0x40,
        0x5b, 0x5c, 0x5d, 0x5e, 0x5f, 0x60 };

int offset = 0x30;                      /* ASCII 0 (zero) */
unsigned long mask[4] = { 0xff000000, 0xff0000, 0xff00, 0xff };

void char_encode (
  unsigned int value, /* 1's complement of the checksum     */
                  /*     value to be encoded         */
  char *ascii)       /* Output 16-character encoded string */
{
    int byte, quotient, remainder, ch[4], check, i, j, k;
    char asc[32];

    for (i=0; i < 4; i++) {
      /* each byte becomes four */
      byte = (value & mask[i]) >> ((3 - i) * 8);
      quotient = byte / 4 + offset;
      remainder = byte % 4;
      for (j=0; j < 4; j++)
        ch[j] = quotient;

      ch[0] += remainder;

      for (check=1; check;)     /* avoid ASCII punctuation */
        for (check=0, k=0; k < 13; k++)
          for (j=0; j < 4; j+=2)
            if (ch[j]==exclude[k] || ch[j+1]==exclude[k]) {
                ch[j]++;
                ch[j+1]--;
                check++;
            }

      for (j=0; j < 4; j++)     /* assign the bytes */
        asc[4*j+i] = ch[j];
    }

    for (i=0; i < 16; i++)     /* permute the bytes for FITS */
      ascii[i] = asc[(i+15)%16];

    ascii[16] = 0;                 /* terminate the string */
}
```

## Appendix K: Header inheritance convention

This appendix is not part of the FITS Standard, but is included for informational purposes.

The reserved Boolean INHERIT keyword described in Sect. 4.4.2.6 is optional, but if present it shall appear in the extension header immediately after the mandatory keywords. The INHERIT keyword must not appear in the primary header. Keyword inheritance provides a mechanism to store keywords in the primary HDU, and have them be shared by one or more extensions in the file. This mechanism minimizes duplication (and maintenance) of metadata in multi-extension FITS files.

It should only be used in FITS files that have a null primary array (e.g., with NAXIS = 0). to avoid possible confusion if arrayspecific keywords (e.g., BSCALE and BZERO) were to be inherited.

When an application reads an extension header with INHERIT = T, it should merge the keywords in the current extension with the primary header keywords. The exact merging mechanism is left up to the application. The mandatory primary array keywords (e.g., BITPIX, NAXIS, and NAXISn) and any COMMENT, HISTORY, and blank keywords in the primary header must not be inherited. It is assumed also that the table-specific keywords described in Sect. 7.2 and 7.3, and the table-specific

65

<!-- page 72 of 75 -->

WCS keywords described in Sect. 8, cannot be inherited since they will never appear in the primary header. If the same keyword is present in both the primary header and the extension header, the value in the extension header shall take precedence. If INHERIT = F in an extension header, the keywords from the primary header should not be inherited.

An application that merely reads a FITS file is authorized by INHERIT = T to look in the primary HDU for an expected keyword not found in the current HDU. However if the application writes out a modified file, it has to be very careful to avoid unwanted duplication of keywords, and preserve the separation of primary and extension headers. If an application modifies the value of an inherited keyword while processing an extension HDU, then it is recommended to write the modified value of that keyword into the extension header, leaving the value of the keyword in the primary header unchanged. The primary array keywords should only be modified when the intent is to explicitly change the value that will subsequently be inherited in the extensions.

Also if the FITS file is read in sequentially (e.g., from tape or Internet downloads), the reader would need to cache the primary header in case it turns out that a later extension in the file uses the INHERIT keyword.

## Appendix L: Green Bank convention

This appendix is not part of the FITS Standard, but is included for informational purposes.

The Green Bank convention was developed at a meeting in October 1989 at the US National Radio Astronomy Observatory in Green Bank, West Virginia, to discuss the use of FITS for single-dish radio-astronomy data, and has since been widely used in conjunction with the SDFITS convention<sup>16</sup>. It was devised primarily to record WCS keywords independently for each row of a table containing an image array column, but subsequently it has found more-general application.

The basic idea is that of expanding header keywords into binary-table columns, and vice versa, of collapsing unvarying binary-table columns into header keywords.

For example, the standard header keyword DATE-OBS, which records the date and time of observation, could be expanded into a column with TTYPE $ln = \mathrm{DATE} - \mathrm{DBS}$ to record the date and time independently for each row of a binary table. Conversely, a binary-table column with $\mathrm{TTYPEn}=\mathrm{HOMIDTY}$ containing the same value in each row, could be collapsed into a keyword, HUMIDITY, that recorded the constant value.

When the Green Bank convention is used (and arguably otherwise), a keyword should not coexist with a column of the same name within a single binary table. Should this situation occur, the column value takes precedence over the keyword.

When expanding keywords into columns, the Green Bank convention applies to all FITS keywords that may appear in a binary table except for the following, most of which describe the structure or identity of a binary table HDU: XTENSION, BITPIX, NAXIS, NAXISn, PCOUNT, GCOUNT, TFIELDS, EXTNAME, EXTVER, EXTLEVEL, TTYPEn, TFORMn, TUNITn, TSCALn, TZEROn, TNULLn, TDISPn, THEAP, TDIMn, DATE, ORIGIN, COMMENT, HISTORY, CONTINUE, and END.

In order to collapse a column into a keyword, the name of the column (given by TTYPEn) must be a valid keyword name, and

the column’s constant value must be amenable to representation as a valid keyvalue.

Software that implements the Green Bank convention must take into account the possibility that any “keyword” (apart from those on the proscribed list), such as DATE-OBS, may change value from row to row of a table. Moreover, when searching the header for a particular keyword, it must first consider the values of the TTYPEn keywords in case the desired keyword has been expanded as a column. Likewise, it must consider each header keyword potentially as a collapsed column, so that a request for the value in a particular row or rows of the non-existent HUMIDITY column would be satisfied by the value of the HUMIDITY keyword.

## References

**Note:** Many of these FITS references are available electronically from the NASA Astrophysics Data System (ADS) and/or the FITS Support Office websites at [http://adswww.harvard.edu](http://adswww.harvard.edu) and [http://fits.gsfc.nasa.gov/fits\_documentation.html](http://fits.gsfc.nasa.gov/fits_documentation.html).

Allen, S. & Wells, D. 2005, IETF RFC 4047, http://www.ietf.org/rfc/rfc4047.tx

ANSI 1977, American National Standard for Information Processing: Code for Information Interchange, ANSI X3.4–1977 (ISO 646) New York: American National Standards Institute, Inc.

Braden, R. T., Borman, D.A., and Partridge, C. 1988 ACM Computer Communication Review, 19, no. 2, 86, IETF RFC 1071, [https://tools.ietf.org/html/rfc1071](https://tools.ietf.org/html/rfc1071)

Bradner, S. 1997, IETF RFC 2119, [http://www.ietf.org/rfc/rfc2119.txt](http://www.ietf.org/rfc/rfc2119.txt)

Bunclark, P. & Rots, A. 1997, Precise re-definition of DATE-OBS Keyword encompassing the millennium, [http://fits.gsfc.nasa.gov/year2000.html](http://fits.gsfc.nasa.gov/year2000.html)

Calabretta, M. R. & Greisen, E. W. 2002, A&A, 395, 1077

Calabretta, M. R. & Roukema, B. F. 2007, MNRAS, 381, 865

Cotton, W. D., Tody, D. B., & Pence, W. D. 1995, A&AS, 113, 159

Cotton, W. D., et al. 1990, Going AIPS: A Programmer’s Guide to the NRAO Astronomical Image Processing System, Charlottesville: NRAO

Deutsch P. 1996, RFC 1951, Network Working Group; available online: [http://tools.ietf.org/html/rfc1951](http://tools.ietf.org/html/rfc1951)

Folkner, W. M., Williams, J. G., & Boggs, D. H. 2009, Interplanetary Network Progress Report 42-178, available online: [http://tmo.jpl.nasa.gov/progress\_report/42-178/178C.pdf](http://tmo.jpl.nasa.gov/progress_report/42-178/178C.pdf)

Folkner, W. M. et al. 2014, Interplanetary Network Progress Report 42-196, available online: [http://ipnpr.jpl.nasa.gov/progress\_report/42-196/196C.pdf](http://ipnpr.jpl.nasa.gov/progress_report/42-196/196C.pdf)

Greisen, E. W. & Calabretta, M. R. 2002, A&A, 395, 1061

Greisen, E. W., Calabretta, M. R., Valdes, F. G., & Allen, S. L. 2006, A&A, 446, 747

Greisen, E. W. & Harten, R. H. 1981, A&AS, 44, 371

Grosbøl, P., Harten, R. H., Greisen, E. W., & Wells, D. C. 1988, A&AS, 73, 359

Grosbøl, P. & Wells, D. C. 1994, Blocking of Fixed-block Sequential Media and Bitstream Devices, [http://fits.gsfc.nasa.gov/blocking94.html](http://fits.gsfc.nasa.gov/blocking94.html)

Hanisch, R., et al. 2001, A&A, 376, 359

Harten, R. H., Grosbøl, P., Greisen, E. W., & Wells, D. C. 1988, A&AS, 73, 365

IAU 1983, Transactions of the IAU, XVIIIB, 45

IAU 1988, Transactions of the IAU, XXB, 51

IAU 1997, Resolution B1 of the XXIIIrd General Assembly – Transactions of the IAU Vol. XXIII B, Ed. J. Andersen, (Dordrecht: Kluwer). Available online: http://www.iau.org/static/resolutions/IAU1997 French.pdf

IEEE 1985, American National Standard – IEEE Standard for Binary Floating Point Arithmetic, ANSI/IEEE 754–1985, New York: American National Standards Institute, Inc.

Irwin, A. W. & Fukushima, T. A. 1999, A&A348, 642

ISO 2004, Information technology – Programming languages – Fortran, ISO/ IEC 1539-1:2004, Geneva: International Organization for Standardization

ISO 2004b, International Standard ISO 8601:2004(E), Data elements and interchange formats – Information interchange – Representation of dates and times

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">16 [http://fits.gsfc.nasa.gov/registry/sdfits.html](http://fits.gsfc.nasa.gov/registry/sdfits.html)</span></small>

66

<!-- page 73 of 75 -->

NASA/JPL Planetary Ephemerides 2014a, available online: [http://ssd.jpl.nasa.gov/?ephemerides](http://ssd.jpl.nasa.gov/?ephemerides)

NASA/JPL Solar and Planetary Ephemerides 2014b, available online: [http://ssd.jpl.nasa.gov/?planet\_eph\_export](http://ssd.jpl.nasa.gov/?planet_eph_export)

Mallory, T. & Kullberg, A. 1990, IETF RFC 1141, [https://tools.ietf.org/html/rfc1141](https://tools.ietf.org/html/rfc1141)

McNally, D., ed. 1988, Transactions of the IAU, Proceedings of the Twentieth General Assembly (Dordrecht: Kluwer)

Park, X. & Miller, X. 1988, Comm. ACM, 31, Issue 10, 1192; available online: [http://dl.acm.org/citation.cfm?id=63042](http://dl.acm.org/citation.cfm?id=63042)

Pence, W. D., Seaman, R., & White, R. L. 2009, PASP, 121, 414

Pence, W. D., Chiappetti, L., Page, C. G., Shaw, R. A., & Stobie, E. 2010, A&A, 524, A42

Pence, W. D., Seaman, R., & White, R. L. 2013, Tiled Table Convention for Compressing FITS Binary Tables, FITS Support Office; available online: [http://fits.gsfc.nasa.gov/registry/tiletablecompression.html](http://fits.gsfc.nasa.gov/registry/tiletablecompression.html)

Ponz, J. D., Thompson, R. W., & Muñoz, J. R. 1994, A&AS, 105, 53

Rice, R. F., Yeh, P.-S., & Miller, W. H. 1993, in Proc. 9th AIAA Computing in Aerospace Conf., AIAA-93-4541-CP, American Institute of Aeronautics and Astronautics

Rijsinghani, A. (ed.) 1994, IETF RFC 1624, [https://tools.ietf.org/html/rfc1624](https://tools.ietf.org/html/rfc1624)

Rots, A. H., Bunclark, P. S., Calabretta, M. R., Allen, S. L., Manchester, R. N. & Thompson, W. T. 2015, A&A, 574, A36

Schmitz, M., et al. 1995, Information & On-line data in Astronomy, eds. D. Egret & M. A. Albrecht (Kluwer Academic Pub.), 259

Standish, E. M. 1990, A&A, 233, 252

Standish, E. M. 1998, JPL Memo IOM 312.F-98-048

Wells, D. C., Greisen, E. W., & Harten, R. H. 1981, A&AS, 44, 363

Wells, D. C. & Grosbøl, P. 1990, Floating Point Agreement for FITS, [http://fits.gsfc.nasa.gov/fp89.txt](http://fits.gsfc.nasa.gov/fp89.txt)

White, R. L. 1992, in Proceedings of the NASA Space and Earth Science Data Compression Workshop, ed. J. C. Tilton, Snowbird, UT; available online: [https://archive.org/details/nasa\_techdoc\_19930016742](https://archive.org/details/nasa_techdoc_19930016742)

White, R. L., & Greenfield, P. 1999, in ADASS VIII, ASP Conf. Ser. 172, eds. D. M. Mehringer, R. L. Plante, & D. A. Roberts (San Francisco: ASP), 125

White, R. L., Greenfield, P., Pence, W., Tody, D. & Seaman, R. 2013, Tiled Image Convention for Storing Compressed Images in FITS Binary Tables, FITS Support Office; available online: [http://fits.gsfc.nasa.gov/registry/tilecompression.html](http://fits.gsfc.nasa.gov/registry/tilecompression.html)

Ziv, J., & Lempel, A. 1977, IEEE Transactions on Information Theory, 23 (3), 337

67

<!-- page 74 of 75 -->

## Index

N<sub>bits</sub> , 11, 12, 17

angular units, 10, 31 ANSI, 3, 56 ANSI, IEEE, 16, 26 array descriptor, 22–24, 26–29 array size, 11, 12, 17 array value, 3, 4, 14, 20 array, multi-dimensional, 5, 24, 30, 59 array, variable-length, 1, 24, 27–29, 59 ASCII character, 3, 16, 19, 21, 56 ASCII table, 19 ASCII text, 3–5, 7, 13, 21, 25, 56 ASCII, ANSI, 66 AUTHOR, 13

binary table, 4, 16, 22, 54 BITPIX, 11, 12, 14, 16–19, 22 BLANK, 14, 16 blocking, 6 BSCALE, 14, 16 BUNIT, 14 byte order, 5, 16, 26 BZERO, 14, 16

case sensitivity, 6, 7, 10, 20, 23 character string, 3, 7, 21, 24, 25 checksum, 15, 45, 48, 49, 62–65 COMMENT, 6, 13 complex data, 9, 23, 26, 27 compressed binary tables, 48, 54, 62 compressed images, 44, 54, 62 compression algorithms, 44, 49, 50 compression, lossy, 48 conforming extension, 3–5 CONTINUE, 6, 7, 62 coordinate systems, 29

DATAMAX, 14 DATAMIN, 14 DATE, 12, 42 DATE-OBS, 13, 42 DATExxxx, 13, 42 deprecate, 3, 4, 6, 9, 13, 16, 22, 30, 31, 34 dithering, 47 durations, 43

END, 5, 11, 17, 18, 20, 22, 28 EPOCH, 34 EQUINOX, 34 EXTEND, 12 extension, 3–5, 15, 16, 59, 61 extension registration, 5, 11 extension type name, 3, 5, 11, 15 extension, conforming, 3–5 extension, standard, 4, 5 EXTLEVEL, 15 EXTNAME, 15 EXTVER, 15

field, empty, 22, 25, 26 file size, 4 fill, 5, 6, 11, 18, 20, 21, 24, 25, 28 FITS structure, 3, 4, 6, 12 floating-point, 8, 26, 56 floating-point FITS agreement, 67 floating-point, complex, 9, 26 format, data, 16 format, fixed, 7 format, free, 7, 8, 52 format, keywords, 7 Fortran, 5, 19–21, 24, 66

GCOUNT, 12, 17–19, 22 Green Bank convention, 31, 62, 66 group parameter value, 3, 17, 18 GROUPS, 17 GTI tables, 43 Gzip compression, 50

H-compress algorithm, 51 HDU, 4, 11 HDU, extension, 3, 4 HDU, primary, 3–5 header space, preallocation, 14, 62 heap, 4, 12, 22–24, 26, 28 HISTORY, 6, 14 hyphen, 6, 20, 23, 31, 34

IAU, 1, 4, 66 IAU Style Manual, 10, 67 IAUFWG, 1, 4–6, 11, 29, 41, 59 IEEE floating-point, 16 IEEE special values, 4, 14, 16, 56 image extension, 18 INHERIT, 15, 62, 65 INSTRUME, 13 integer, 16-bit, 16, 26 integer, 32-bit, 16, 26 integer, 64-bit, 16, 26 integer, complex, 9 integer, eight-bit, 16, 26 integer, unsigned, 14, 16, 23, 26 ISO-8601 date, 37

## JD, 37

keyword record, 5, 6 keyword, commentary, 6, 13 keyword, indexed, 4, 6, 11 keyword, mandatory, 7, 10, 17–19, 22, 54 keyword, new, 16 keyword, order, 11, 17, 19 keyword, required, 4, 10, 11, 17, 18, 22, 44, 48 keyword, reserved, 4, 12, 17, 18, 20, 22, 30, 31, 42, 45, 49, 54 keyword, valid characters, 6

logical value, 8, 25, 26

68

<!-- page 75 of 75 -->

magnetic tape, 6 min and max in columns, keywords, 20, 24, 62 MJD, 37

NaN, IEEE, 16, 26, 56, 57 NAXIS, 4, 5, 11, 12, 17–19, 22 NAXIS1, 17, 19, 21, 22, 24, 25, 28 NAXIS2, 19, 21, 22, 24, 25, 28 NAXISn, 5, 11, 12, 17, 18 NULL, ASCII, 3, 25

OBJECT, 13 OBSERVER, 13 order, byte, 5, 16, 26 order, extensions, 5 order, FITS structures, 4 order, keyword, 6, 11, 17, 19 ORIGIN, 12

PCOUNT, 12, 17–19, 22, 28 phase, 43 physical value, 3, 4, 14, 17, 18, 20, 23 PLIO compression, 50 primary data array, 3–5, 17, 18 primary header, 3, 4, 11, 17 PSCALn, 17, 18 PTYPEn, 17, 18 PZEROn, 17, 18

quantization of data, 46, 63

random groups, 3, 16, 17 random-groups, 14 random-groups array, 17 REFERENC, 13 repeat count, 4, 22, 25 Rice compression, 50

scaling, data, 17, 18, 20, 23 sign bit, 16 sign character, 8, 21 SIMPLE, 5, 11, 17 slash, 7, 10 solar system ephemeris, 41 special records, 3–5 special values, IEEE, 26 standard extension, 4, 5

TABLE, 19 TBCOLn, 19 TDIMn, 24 TDISPn, 20, 24 TELESCOP, 13 TFIELDS, 19, 22 TFORMn, 19, 22, 25, 26, 28 THEAP, 24, 28 time, 12, 13, 34, 36, 37 time keywords, 42 time reference, 38 time reference direction, 40 time reference position, 39 time resolution, 42 time scale, 37, 38

time units, 41 time, universal, 12, 38 timelag, 43 TIMESYS, 37 TNULLn, 20, 21, 24, 26 TSCALn, 20, 23, 28 TTYPEn, 20, 23 TUNITn, 20, 23 two’s complement, 16, 26 TZEROn, 20, 23, 28

underscore, 6, 20, 23 units, 4, 10, 14, 20, 23, 31, 36

value, 6, 7, 12 value, undefined, 7, 14, 16, 20, 21, 24, 60 variable-length array, 1, 24, 27–29, 59 variable-length arrays, compression, 49

WCS, 29 WCS, celestial, 34 WCS, spectral, 34 WCS, timing, 36, 62

XTENSION, 3, 5, 11, 15, 18, 19, 22

69