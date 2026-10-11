<!-- page 1 of 86 -->

arXiv:astro-ph/0307036v1 2 Jul 2003

REVIEW ARTICLE

# Optical Interferometry in Astronomy

**John D. Monnier**†

**University of Michigan Astronomy Department, 941 Dennison Building, 500 Church Street, Ann Arbor MI 48109**

**Abstract. Here I review the current state of the field of optical stellar interferometry, concentrating on ground-based work although a brief report of space interferometry missions is included. We pause both to reflect on decades of immense progress in the field as well as to prepare for a new generation of large interferometers just now being commissioned (most notably, the CHARA, Keck and VLT Interferometers). First, this review summarizes the basic principles behind stellar interferometry needed by the lay-physicist and general astronomer to understand the scientific potential as well as technical challenges of interferometry. Next, the basic design principles of practical interferometers are discussed, using the experience of past and existing facilities to illustrate important points. Here there is significant discussion of current trends in the field, including the new facilities under construction and advanced technologies being debuted. This decade has seen the influence of stellar interferometry extend beyond classical regimes of stellar diameters and binary orbits to new areas such as mapping the accretion disks around young stars, novel calibration of the Cepheid Period-Luminosity relation, and imaging of stellar surfaces. The third section is devoted to the major scientific results from interferometry, grouped into natural categories reflecting these current developments. Lastly, I consider the future of interferometry, highlighting the kinds of new science promised by the interferometers coming on-line in the next few years. I also discuss the longer-term future of optical interferometry, including the prospects for space interferometry and the possibilities of large-scale ground-based projects. Critical technological developments are still needed to make these projects attractive and affordable.**

†

Email: monnier@umich.edu

<!-- page 2 of 86 -->

Optical Interferometry in Astronomy

2

## 1. Introduction

**This review will introduce the theory, technique, and scientific goals of optical stellar interferometry. By combining light collected by widely-separated telescopes, interferometrists can overcome the diffraction-limit of an individual telescope. The** angular resolution achieved by current instruments is indeed astounding, $<   5 \times 1 0 ^ { - 9 }$ **radians (1 milli-arcsecond), as are the engineering feats of maintaining sub-micron optical stability and coherence over hundreds of meters of pathlength while controlling polarization and dispersion over broad wavelength bandpasses. New capabilities are being applied in a wide variety of astrophysics contexts, including fundamental stellar parameters, novel ways to measure distances to stars, probing star formation and evolution, direct detection of extrasolar planets, and resolving cores of the nearest active galactic nuclei and brightest quasars. This current work is pointing the way towards next generation facilities, and I will close with a discussion of efforts to bring the angular resolution advantages of interferometers into space.**

## 1.1. Scope of Review

**The history of stellar interferometry spans more than a century, and a proper documentation of the rich history is beyond the scope of this review (see Lawson, 2000a, for a historical overview of the field). The main purpose of this review will be to summarize the current state of the field of optical interferometry, including past scientific and engineering lessons, current astronomical motivations, and future goals and performance expectations. Interested readers may want to consult earlier reviews which tend to emphasize other topics, especially Shao and Colavita (1992a) and Quirrenbach (2001). In order to restrict the length, I will concentrate on longbaseline optical interferometry, giving only passing description to diffraction-limited single-aperture experiments (e.g., Speckle Interferometry, Aperture Masking, Adaptive Optics). Further, I consider “optical interferometry” in a restricted sense to mean the light from the separate telescopes are brought together using optics, as opposed to heterodyne interferometry whereby the radiation at each telescope is coherently detected before interference (although I will discuss briefly the important cases of the Intensity Interferometer and heterodyne interferometry using** $\mathrm { C O _ { 2 } }$ **lasers). In practice then, “optical interferometry” is limited to visible and infrared wavelengths, and I will not discuss recent advances in mm-wave and sub-mm interferometry.**

## 1.2. The Organization of Review

**This review is divided into 4 major sections. The first reviews the basic theory behind optical interferometry and image reconstruction through a turbulent atmosphere. The second section explains the basic designs of interferometers and core modern technologies which make them work, including descriptions of current facilities. Major scientific results are outlined in the third section. The last section forecasts near-future science**

<!-- page 3 of 86 -->

Optical Interferometry in Astronomy

3

**potential as well as the long-term prospects of optical interferometry on the ground and in space.**

## 1.3. Nomenclature

**In this review, “optical” does not indicate the visible portion of the electromagnetic spectrum only, but generally refers to how the light is manipulated (using optics); in the context of interferometry, this will limit our discussion to wavelengths from the blue (∼ 0.4µm) to the near-infrared (1-5µ) and mid-infrared (8-12µm). Typical angular units used in this paper are “milli-arcseconds”, or mas, where an arcsecond is the standard 1/3600 of a degree of angle. Astronomers often use the magnitude scale to discuss the wavelength-dependent flux density (power per unit area per unit bandwidth) from an astronomical source, where the bright star Vega (α Lyrae) is defined as 0 mag (corresponding to a 10000K blackbody); the magnitude scale is logarithmic such that every factor of 10 brightness decrease corresponds to a flux “magnitude” increase of 2.5 (e.g., a contrast ratio of 10 astronomical magnitudes is a factor of 10**<strong><sup>4</sup></strong>**). In addition, the unit Jansky (Jy) is often used for measuring the flux density of astronomical objects,** $1 ~ \mathrm { J y } = 1 0 ^ { - 2 6 } W m ^ { - 2 } H z ^ { - 1 }$

**A number of other basic astronomical units are used herein. The distance between the Earth and Sun is one astronomical unit, 1** $\mathrm { A U }   \simeq   1 . 5 \times 1 0 ^ { 1 1 } \mathrm { m }$ **. Stellar distances are given in units of parsecs (1 parsec is the distance to a star exhibiting a parallax angle of 1 arcsecond): written in terms of other common units of length, 1 pc** $\simeq 3 . 0 9 \times 1 0 ^ { 1 6 } \mathrm { m } { \sim 3 . 2 6 }$ **light years.**

**Lastly, I want to alert the reader (in advance) to Table 2 which will define all the interferometer acronyms used throughout the text.**

## 2. Basic Principles of Stellar Interferometry

**This section will review the basic principles of stellar interferometry. More detailed discussions of optical interferometry issues can be found in the recent published proceedings of the Michelson Summer School, “Principles of Long Baseline Stellar Interferometry” edited by P. Lawson (Lawson, 2000b), and the proceedings of the 2002 Les Houches Eurowinter school edited by G. Perrin and F. Malbet (Perrin and Malbet, 2002); earlier such collections also continue to play an important reference role (e.g., Perley et al., 1986; Lagrange et al., 1997). Other “classic” texts on the subjects of radio interferometry and optics are Thompson et al. (2001), Born and Wolf (1965), and Goodman (1985).**

## 2.1. Basics of Stellar Interferometry

**The basic principles behind stellar interferometry should be familiar to any physicist, founded on the wave properties of light as first observed by Thomas Young in 1803.**

<!-- page 4 of 86 -->

Optical Interferometry in Astronomy

4

![Image block](doc:b6a1ff8/tier:standard/page:4/block:3)

Figure 1. Young’s two-slit interference experiment (monochromatic light) is presented to illustrate the basic principles behind stellar interferometry. On the left is the case for a single point source, while the case on the right is for a double source with the angular distance being half the fringe spacing. Note, the interference pattern shown represents the intensity distribution, not the electric field.

**This result is widely known through Young’s “two-slit experiment,” although two slits were not used in the original 1803 work.**

**2.1.1. Young’s Two-slit Experiment In the classical setup, monochromatic light from a distant (“point”) source impinges upon two slits, schematically shown in the left panel of Figure 1. The subsequent illumination pattern is projected onto a screen and a pattern of fringes is observed. This idealized model is realized in a practical interferometer by receiving light at two separate telescopes and bringing the light together in a beam combination facility for interference (this will be discussed fully in §3; e.g., see Figure 10).** The interference is, of course, due to the wave nature of light á la Huygens; the electric **field at each slit (telescope) propagating to the screen with different relative path lengths, and hence alternately constructively and destructively interfering at different points along the screen. One can easily write down the condition for constructive interference; the fringe spatial frequency (fringes per unit angle) of the intensity distribution on the screen is proportional to the projected slit separation, or baseline b, in units of the observing wavelength λ (see Figure 1). That is,**

$$
\text {Fringe Spacing} \equiv \Delta \Theta = \frac {\lambda}{b} \text {radians}\tag{1}
$$

$$
\text {Fringe Spatial Frequency} \equiv u = \frac{b}{\lambda} \text {radians}^{-1}\tag{2}
$$

**Imagine another point source of light (of equal brightness, but incoherent with the first) located at an angle of** $\lambda / ( 2 b )$ **f**rom the first source (see right of panel of **Figure 1). The two illumination patterns are out of phase with one another by 180**◦,

<!-- page 5 of 86 -->

Optical Interferometry in Astronomy

5

**hence cancelling each other out and presenting a uniformly illuminated screen. Clearly such an interfering device (an “interferometer”) can be useful in studying the brightness distribution of a distant “stellar” object. This application of interferometry was first proposed by Fizeau in 1868 (Fizeau, 1868) and successfully applied by Michelson to measure the angular diameters of Jupiter’s moons (Michelson, 1890, 1891) in 1891 and later (with Pease in 1921) to measure the first angular size of a star beyond the Sun (Michelson and Pease, 1921) (see §3.1 for further details on the early history of optical interferometry).**

**2.1.2. Angular Resolution The ability to discern the two components of a binary star system is often used to gauge the spatial resolution of an instrument, be it a conventional imaging telescope or a separated-element interferometer. Classical diffraction theory has established the “Rayleigh Criterion” for defining the (diffraction-limited) resolution of a filled circular aperture of diameter D:**

$$
\text {Resolution of Telescope} \equiv \Delta \Theta_ {\text {telescope}} = 1. 2 2 \frac {\lambda}{D} \text {radians}\tag{3}
$$

**This criterion corresponds to the angular separation on the sky when one stellar component is centered on the first null in the diffraction pattern of the other; the binary is then said to be resolved. A similar criterion can be defined for an interferometer: an equal brightness binary is resolved by an interferometer if the fringe contrast goes to zero at the longest baseline. As motivated in the last paragraph, this occurs when the** angular separation is $\frac { \lambda } { 2 b }$ **,** where b is the baseline. Hence,

$$
\text {Resolution of Interferometer} \equiv \Delta \Theta_ {\text {interferometer}} = \frac {\lambda}{2 b} \text {radians}\tag{4}
$$

**While these two criteria are somewhat arbitrary, they are useful for estimating the angular resolution of an optical system and are in widespread use by the astronomical community.**

**2.1.3. Complex Visibility One can be more quantitative in interpreting the fringe patterns observed with an interferometer. The fringe contrast is historically called the visibility and, for the simple (two-slit) interferometer considered here, can be written as**

$$
V = \frac {I _ {\max} - I _ {\min}}{I _ {\max} + I _ {\min}} = \frac {\text {Fringe Amplitude}}{\text {Average Intensity}}\tag{5}
$$

**where** $I _ { \mathrm { m a x } }$ **and** $I _ { \mathrm { m i n } }$ **denote the maximum and minimum intensity of the fringes. Hence, the left and right fringe patterns of Figure 1 have visibilities of one and zero respectively.**

**The Van Cittert-Zernike Theorem (see Thompson et al., 2001, for complete discussion and proof) relates the contrast of an interferometer’s fringes to a unique Fourier component of the impinging brightness distribution. In fact, the visibility is exactly proportional to the amplitude of the image Fourier component corresponding to** the (spatial) fringe spatial frequency defined above $( u = b / \lambda \mathrm { r a d } ^ { - 1 } )$ **. Also, the phase of the fringe pattern is equal to the Fourier phase of the same spatial frequency component.**

<!-- page 6 of 86 -->

Optical Interf

6

![Chart block](doc:b6a1ff8/tier:standard/page:6/block:3)

Figure 2. This figure shows simple one-dimensional images and their corresponding visibility curves. The left panels are the images while the right panels correspond to the Fourier amplitudes, i.e. the visibility amplitudes. Note that “large” structure in image-space result in “small” structure in visibility-space.

**The Van Cittert-Zernike Theorem can be expressed concisely in mathematical terms. Consider that the astronomical target emits light at frequency ν over only a very small portion of the sky with specific intensity** $I _ { \nu } ( \theta , \phi )$ **, so small that the spherical** coordinates $\theta _ { 0 } + \delta \theta$ and $\phi _ { 0 } + \delta \phi$ can be interpreted as Cartesian coordinates $x _ { \Omega }$ and $y _ { \Omega }$ centered around $\theta _ { 0 }$ **and** $\phi _ { 0 }$ **on the plane of the sky. We can write the interferometer response (amplitude and phase of the fringes) as the frequency-dependent complex** visibility $\tilde { \mathcal { V } } _ { \nu } ( u , v )$ **,** defined as the Fourier Transform of the brightness distribution $I _ { \nu } ( \vec { r _ { \Omega } } )$ normalized so that $\begin{array} { r } { \tilde { \mathcal { V } } ( \frac { \vec { D } } { \lambda } = 0 ) = 1 } \end{array}$

$$
| \mathcal {V} _ {\nu} (\frac {\vec {D}}{\lambda}) | e ^ {- i \phi_ {V _ {\nu}}} = \frac {\int_ {\delta \Omega} d x _ {\Omega}   d y _ {\Omega}   I _ {\nu} (r _ {\vec {\Omega}}) e ^ {- 2 \pi i \left(\frac {\vec {D}}{\lambda} \cdot r _ {\vec {\Omega}}\right)}}{\underbrace {\int_ {\delta \Omega} d x _ {\Omega}   d y _ {\Omega}   I _ {\nu} (r _ {\vec {\Omega}})} _ {\text {Total Specific Flux}}}\tag{6}
$$

**using the following notation:**

$$
\left| \begin{array}{c} r _ {\vec {\Omega}} = (x _ {\Omega}, y _ {\Omega}) \\ \frac {\vec {D}}{\lambda} \equiv \text {the baseline vector} \vec {D} \text {projected onto the plane} \\ \quad \text {of the sky in units of wavelength} \lambda \\ = (u, v) \quad [ \text {Common Notation} ] \end{array} \right|\tag{7}
$$

**Figure 2 shows some simple examples of one-dimensional images and the corresponding visibility curves. The top panels show the case of an equal binary**

<!-- page 7 of 86 -->

Optical Interferometry in Astronomy

7

**system, where both components are unresolved. The periodicity in the visibility-space corresponds to the binary separation. The middle set of panels is representative of a compact, but resolved, source (such as a star surrounded by an optically-thick dust shell). The small image size means there is more high spatial frequency information, and this is why the corresponding visibility curve is non-zero even at high resolution. Lastly, the bottom panels show an image of a unresolved star (with 10% of the total flux) surrounded by larger-scale structure (this is expected when a star is surrounded by an optically-thin envelope of dust). The large-scale structure (containing 90% of the total flux) can be seen to be “resolved” on short baselines (at low spatial frequency), while the point-source remains unresolved out to the highest spatial frequency. Note that the visibility plateaus at 0.10, corresponding to the fraction of the total flux which is left unresolved. This is easy to understand since the Fourier Transform is linear; that is, the (complex) visibility of a point-source and extended structure is equal to the visibility of the point-source plus the visibility of the extended structure separately. This property of linearity is very helpful in interpreting simple visibility curves.**

**Most astronomical objects are not one-dimensional, and the two-dimensional space** of spatial frequencies is called the Fourier Plane, or the $( \mathrm { u , } \mathrm { v } )$ plane, named after the $( \mathrm { u , } \mathrm { v } )$ **coordinates defined in Eq.7. Further, in general we must consider both the visibility amplitude and the visibility phase. For example, consider the equal binary system depicted in Figure 3. The complex visibility can be easily written by choosing the origin midway between the two components. Note the abrupt phase jump when the visibility amplitude goes through a null. These discontinuities are smoothed out when the two components are not precisely equal.**

## 2.2. Atmospheric Problems

**An incoming plane wave from a stellar source is corrupted as it propagates through the turbulent atmosphere. Variations in the column density of air along different paths cause the effective pathlength to vary, introducing wavefront distortion. If these distortions become a significant fraction of a wavelength across the aperture of a telescope, the size of the image formed will not be diffraction-limited by the primary mirror, but rather by the coherence scale of the incoming wavefront. The transverse distance over which one expects rms pathlength difference to be** $\lambda / 2 . 4$ **has been defined as the Fried parameter and is denoted by** $\mathrm { r _ { 0 } } ( \lambda )$ **(Fried, 1965); hence telescope apertures larger than** $\mathrm { r _ { 0 } } ( \lambda )$ **can expect significant degradation of image quality (when observing at wavelength λ) due to atmospheric effects. In fact, for an** $\mathrm { r _ { 0 } }$ **diameter circular patch, the rms phase error is ∼1.03 radians.** $At  $\lambda =$500 nm, $\mathrm { r _ { 0 } }$$ **is typically 10 cm (toward zenith) at average observing sites and hence even small telescopes can not be used at their diffraction limit in the visible. In such cases, the observed angular size of a point source will be determined** entirely by $\mathrm { r _ { 0 } } ( \lambda )$ at a given wavelength, and is known as the seeing disk size, $\Theta _ { \mathrm { s e i n g } } ( \lambda )$ The Kolmogorov theory of turbulence (Kolmogorov, 1961) predicts that $\mathrm { r } _ { 0 } ( \lambda )   \propto   \lambda ^ { 6 / 5 }$ and hence the seeing size, $\Theta _ { \mathrm { s e e i n g } } ( \lambda )   \propto   \frac { \lambda } { r _ { 0 } ( \lambda ) }   \propto   \lambda ^ { - 1 / 5 }$ **, is only weakly dependent on the**

<!-- page 8 of 86 -->

Optical Interferometry in Astronomy

8

![Image block](doc:b6a1ff8/tier:standard/page:8/block:3)

Figure 3. This figure shows the complex visibility for an equal binary system in the 2-dimension (u,v) plane. With the above choice for the phase center, the Fourier phases can be represented simply. Notice the abrupt phase jumps when the visibility amplitude goes through a null. This figure is reproduced through the courtesy of the NASA/Jet Propulsion Laboratory, California Institute of Technology, Pasadena, California (Monnier, 2000).

**wavelength (Fried, 1965). An example of the phase delays associated with a snapshot of Kolmogorov turbulence can be seen in Figure 4 for 12-m square, corresponding roughly to the size of the largest telescopes today (e.g., the Keck telescopes).**

**Another consequence of turbulence is that the image distortion varies across the sky, although stars located close together suffer similar seeing effects. The angle over which image distortions are correlated is called the “isoplanatic” angle, and is only a few arcseconds in the visible and about an arcminute in the near-infrared. This angle is determined by the vertical distribution of the turbulence – obviously low-level turbulence would induce correlated image distortions over larger sky angles than the same turbulent layer located higher up in the atmosphere. The isoplanatic angle is a critical parameter for the field-of-view of adaptive optics systems which actively sense and correct for atmospheric turbulence in realtime using a deformable mirror.**

**Another important atmospheric diagnostic is the coherence time, t**<strong><sub>0</sub></strong>**. Typically, one assumes a “frozen” turbulence model in which the atmospheric density perturbations are assumed constant over the time it takes wind to blow them across a given aperture (also known as Taylor’s hypothesis of frozen turbulence). This motivates a convenient estimate for the coherence time:** $t _ { 0 } ( \lambda ) \equiv r _ { 0 } ( \lambda ) / v _ { \mathrm { w i n d } }$ **, where** $v _ { \mathrm { w i n d } }$ **is the wind speed. At most sites, wind speeds are** ${ \sim } 1 0   \mathrm { m   s ^ { - 1 } }$ **and so** $t _ { 0 } \sim 1 0$ **ms at 500 nm. Further discussion of atmospheric turbulence and degradation of astronomical images can be found in Kolmogorov (1961), Roddier (1981), and Roddier et al. (1982).**

<!-- page 9 of 86 -->

Optical Interferometry in Astronomy

9

![Chart block](doc:b6a1ff8/tier:standard/page:9/block:3)

Figure 4. This figure shows a typical realization of Kolmogorov turbulence $\left(  r _{0} = 50    cm at   \lambda = 2.2   \mu m  \right)$ ; each solid contour line represents $\frac { \lambda } { 2 }$ of wavefront distortion. Some areas of the aperture show coherent areas larger than $\mathrm { r _ { 0 } }   ,$ and some much smaller; $\mathrm { r _ { 0 } }$ is a statistical property of atmospheric turbulence and wavefront perturbations occur over a wide range of scales.

**These parameters,** $\mathrm { r _ { 0 } ( \lambda ) }$ **an**d $\mathrm { t } _ { 0 } ( \lambda )$ **,** are extremely important for the design of an interferometer, because the value of $\mathrm { r _ { 0 } }$ limits the useful size of the collecting aperture, **while** $\mathrm { t } _ { 0 }$ **limits the coherent integration time. Both of these are crucial for predicting an interferometer sensitivity to faint objects and much debate surrounds the best estimates for these parameters at various sites (e.g., Dyck and Howell, 1983; Roddier et al., 1990; ten Brummelaar, 1994; Treuhaft et al., 1995). This topic is revisited in §3.4 when I discuss the limiting magnitude of current interferometers.**

**It is well-known that** $\mathrm { r _ { 0 } } ( \lambda )$ **and** $\mathrm{t}_{0}(\lambda)$ **depend greatly on the observing site, and we now consider the unique seeing conditions of Mauna Kea, Hawaii, as an example. The coherence scale is unusually long due to the highly laminar flow of the Pacific winds over the peak of the mountain (elevation 4200 m);** $\mathrm { r _ { 0 } }$ **usually lies between 10 and 40 cm at 500 nm (Wizinowich, 1999). However, the fast winds of the overhead jet stream result in very short coherence times:** $\mathrm { t _ { 0 } }$ **between 1.5 and 10 ms (Wizinowich, 1999). It should be emphasized that seeing is notoriously difficult to characterize due to large variations in time (both on short time scales as well as seasonal ones) as evidenced by the large range of** $\mathrm{r}_{0}(\lambda = 500   nm)$ **and** $\mathrm{t}_{0}(\lambda = 500   nm)$ **values just given.**

**2.2.1. Atmospheric Phase Errors The fluctuating amount of integrated atmospheric pathlength above each telescope introduce wavefront time delays which show up as phase shifts in the measured fringes in an interferometer, as illustrated in Figure 5. In this figure, an optical interferometer is represented again by a Young’s two-slit experiment, as**

<!-- page 10 of 86 -->

Optical Interferometry in Astronomy

10

![Image block](doc:b6a1ff8/tier:standard/page:10/block:3)

Figure 5. Atmospheric time delays or phase errors at telescopes cause fringe shifts, as can be seen through analogy with Young’s two-slit experiment. This figure is reproduced through the courtesy of the NASA/Jet Propulsion Laboratory, California Institute of Technology, Pasadena, California (Monnier, 2000).

**discussed earlier in this section. The spatial frequency of these fringes is determined by** the distance between the slits (in units of the wavelength of the illuminating radiation) **However if the pathlength above one slit is changed (due to a pocket of warm air moving across the aperture, for example), the interference pattern will be shifted by an amount depending on the difference in pathlength of the two legs in this simple interferometer. If the extra pathlength is half the wavelength, the fringe pattern will shift by half a fringe, or π radians. The phase shift is completely independent of the slit (telescope) separation, and only depends on slit-specific (telescope-specific) phase delays.**

**The most obvious impact of atmospheric phase delays is that the assumptions of the van Cittert-Zernike theorem no longer apply, and that the measure fringe phase can no longer be associated with the Fourier phase of the sky brightness distribution (the fringe amplitude retains its original meaning, since phase changes do not change the measured fringe amplitudes for short exposures). The corruption of this phase information has serious consequences, since imaging of non-centrosymmetric objects rely on the Fourier phase information encoded in this intrinsic phase of interferometer fringes. Without this information, imaging can not be done except for simple objects such as disks or round stars. Fortunately, a number of strategies have evolved to circumvent these difficulties.**

**2.2.2. Phase Referencing Possible methods for recovering this phase information using phase referencing techniques are discussed in Chapter 9 (written by A. Quirrenbach) of “Principles of Long Baseline Stellar Interferometry (Lawson, 2000b). Few scientific results have resulted from phase referencing techniques to date, but this is expected to**

<!-- page 11 of 86 -->

Optical Interferometry in Astronomy

11

**change over the coming decade as sophisticated new instruments are being deployed. Here, I mention a few of the most promising methods:**

**(i) Nearby sources. If a bright point reference source (or source with well-known structure) lies within an isoplanatic patch (see Quirrenbach, 2000), then its fringes will act as a probe of the atmospheric conditions. By measuring the instantaneous phases of fringes from the bright reference source, one can correct the corrupted phases on a neaby “target” source. This has been applied to narrow-angle astrometry where fringe phase information is used for determining precise relative positions of nearby stars (Shao and Colavita, 1992b; Colavita et al., 1999; Lane et al., 2000a); see Figure 31 for some preliminary results published by the Palomar Testbed Interferometer. While it would be very valuable to use an artificial guide star for phase-referencing a long baseline interferometer, current laser beacons are too spatially extended (resolved) to produce interferometric fringes.**

**(ii) ∆Φ Monitoring. In the millimeter and sub-millimeter, phase shifts caused by fluctuations in atmospheric water vapor column density can be monitored by observing its line emission. This information can be used to phase-compensate the interferometer, allowing longer coherent integrations and accurate fringe phase determination on the target (Wiedner 1998, and references therein). In the midinfrared, strategies to actively monitor ground-level turbulence using temperature sensors are being explored by the Infrared Spatial Interferometer group (Short et al., 2002) at Mt. Wilson motivated by recent atmospheric studies (e.g., Bester et al. 1992). Townes (2002) recently proposed that realtime-monitoring of Rayleigh or Raman backscattering might be used to correct for atmospheric column density variations in the context of optical interferometers, but this method has not yet been validated.**

**(iii) Multi-wavelength. Another possibility is to observe a target at multiple wavelengths and to use data from one part of the spectrum to calibrate another. For example, one might use fringes formed by the continuum emission to phase reference a spectral line (e.g., Vakili et al. 1997). To use this method, one must assume knowledge about the brightness distribution at one of the wavelengths being used.**

**Currently, phase referencing is not possible with most current beam combiners in operation, either due to low spectral resolution or limited field-of-view. In order to recover phase information, one must one must make use of the closure phases.**

**2.2.3. Closure Phases Consider Figure 6 in which a phase delay is introduced above Telescope 2 of a 3-telescope array. As discussed in the last section, this additional delay causes a phase shift in the fringe detected between telescopes 1-2. Note that a phase shift is also induced for fringes between telescopes 2-3; however, this phase shift is equal and opposite to the one for telescopes 1-2. Hence, the sum of three fringe phases, between 1-2, 2-3, and 3-1, is insensitive to the phase delay above telescope 2. This**

<!-- page 12 of 86 -->

Optical Interferometry in Astronomy

12

![Image block](doc:b6a1ff8/tier:standard/page:12/block:3)

Figure 6. This figure explains the principle behind closure phase analysis. Phase errors introduced at any telescope causes equal but opposite phase shifts, canceling out in the closure phase (figure after Readhead et al. 1988). This figure is reproduced through the courtesy of the NASA/Jet Propulsion Laboratory, California Institute of Technology, Pasadena, California (Monnier, 2000).

**argument holds for arbitrary phase delays above any of the three telescopes. In general, the sum of three phases around a closed triangle of baselines, the closure phase, is a good interferometric observable; that is, it is independent of telescope-specific phase shifts induced by the atmosphere or optics.**

**The idea of closure phase was first introduced to compensate for poor phase stability in early radio VLBI work (Jennison 1958). Application at higher frequencies was first mentioned by Rogstad (1968), but only much later carried out in the visible/infrared through aperture masking experiments (Baldwin et al. 1986a; Haniff et al. 1987a; Readhead et al. 1988; Haniff et al. 1989). Currently three separateelement interferometers have succeeded in obtaining closure phase measurements in the visible/infrared, first at COAST (Baldwin et al. 1996a), soon after at NPOI (Benson et al. 1997a), and most recently at IOTA (Traub, 2002).**

**How can these closure phases be used to figure out the Fourier phases which are needed to allow an image to be reconstructed? Each closure triangle phase can be thought of as a single linear equation relating three different Fourier phases (assuming none of the baselines are identical), which we desire to solve for; hence, we must count the number of linear equations available and compare to the number of unknowns. For N telescopes, there are “N choose 3,”** $\begin{array} { r } { \binom { N } { 3 } \; = \; \frac { \stackrel { \bullet } { ( N ) ( N - 1 ) ( N - 2 ) } } { \stackrel { \bullet } { ( 3 ) ( 2 ) } } } \end{array}$ **, possible closing triangles. However, there are only** $\begin{array} { r } { \binom { N } { 2 } = \frac { ( N ) ( N - 1 ) } { 2 } } \end{array}$ **independent Fourier phases; clearly not all the closure phases can be independent. The number of independent closure phases is only** $\begin{array} { r } { \binom { N - 1 } { 2 } \; \stackrel { \sim } { = } \; \frac { ( N - 1 ) ( N - 2 ) } { 2 } } \end{array}$ **, equivalent to holding one telescope fixed and forming all possible**

<!-- page 13 of 86 -->

Optical Interferometry in Astronomy

13

Table 1. Phase information contained in the closure phases alone

| Number of Telescopes | Number of Fourier Phases | Number of Closing Triangles | Number of Independent Closure Phases | Percentage of Phase Information |
| --- | --- | --- | --- | --- |
| 3 | 3 | 1 | 1 | 33% |
| 7 | 21 | 35 | 15 | 71% |
| 21 | 210 | 1330 | 190 | 90% |
| 27 | 351 | 2925 | 325 | 93% |
| 50 | 1225 | 19600 | 1176 | 96% |

**triangles with that telescope (as discussed by Readhead et al., 1988). The number of independent closure phases is always less than the number of phases one would like to determine, but the percent of phase information retained by the closure phases improves as the number of telescopes in the array increases. Table 1 lists the number of Fourier phases, closing triangles, independent closure phases, and recovered percentage of phase information for telescope arrays of 3 to 50 elements. For example, approximately 90% of the phase information is recovered with a 21 telescope interferometric array (e.g., Readhead et al. 1988). As discussed in the next section, this phase information can be coupled with other image constraints (e.g., finite size and positivity) to reconstruct the source brightness distribution.**

**In addition to the mathematical (linear algebra) interpretation of closure phases, there are a few other important properties worth noting.**

**• For sources with point-symmetry (otherwise known as centro-symmetry), all the closure phases are either 0**◦ **or 180**◦**. It is easy to prove this by imagining the image-center (“phase-center”) at the point of centro-symmetry.**

**• Closure phases are not sensitive to an overall translation of image. A translation is indistinguishable from atmospheric phase delays for any given closing triangle.**

**• The closure phases are independent of telescope-specific phase errors, however non-zero closure phases from a point source can result from having non-closing triangles and phase delays in the beam combiner (e.g., for a three-telescope pair-wise beam combiner).**

## 2.3. Image Reconstruction

**While very few images have been made by today’s optical interferometers, new telescope arrays are now being commissioned which will make true imaging interferometry straightforward. Because these new imaging capabilities are likely to have significant impacts over the next decade, I wish to review the basic principles of apertures synthesis imaging. However, I will restrain myself from excessive elaboration here, and instead refer the interested reader to the extensive radio interferometry literature, especially regarding “Very Long Baseline Interferometry (VLBI).”**

<!-- page 14 of 86 -->

Optical Interferometry in Astronomy

14

**While modeling visibility and closure phase data with simple models is useful, one would like to make an image unbiased by theoretical expectations. Since any image can be alternatively represented by its Fourier components, the collection of all “interesting” components can allow the interferometric data to be inverted, thus reconstructing an estimation of the image brightness distribution. The collection of a large number of Fourier components is greatly aided by increasing the number of telescopes, since independent combinations of telescopes increase with the number of telescopes to the** second power $\left( { \frac { ( N ) ( N { - } 1 ) } { 2 } } \right.$ **; see last section)**

**With a large number of measurements, images of arbitrary complexity should be attainable using visible/infrared interferometers and reliable closure phase measurements. The importance of “filling up” the (u,v) plane with measurements when imaging is discussed more fully in §2.4.3. The next subsections will discuss strategies currently employed based on the techniques of VLBI in the radio.**

**2.3.1. Guiding Principles The goals of an image reconstruction procedure can be stated quite simply: find an image which fits both the visibility amplitudes and closure phases within experimental uncertainties. However in practice, there are an infinite number of candidate images which satisfy these criteria, because interferometric data is always incomplete and noisy. Furthermore, the closure phases can not be used to unambiguously arrive at Fourier phase estimates as stated above, even under ideal noisefree conditions.**

**Additional constraints must be imposed to “select” an image as the best-estimate of the true brightness distribution (to “regularize” this ill-posed inverse problem). These constraints introduce correlations in the Fourier amplitudes and phases, and essentially remove degrees of freedom from our inversion problem. Some of the most common (and reasonable) constraints are described below.**

**• Limited Field-of-View. This constraint is always imposed in aperture synthesis imaging, even for a fully-phased array (e.g., VLA). Limiting the field-of-view introduces correlations in the complex visibility in the (u,v) plane. This is a consequence of the Convolution Theorem, a multiplication in image-space is equivalent to a convolution in the corresponding Fourier-space.**

**• Positive-Definite. Since brightness distributions can not be negative, this is a sensible constraint (although not appropriate in some cases, such as for reconstruction of Stokes/polarization components or imaging spectral line absorption). While clearly limiting the range of “allowed” complex visibilities, there are few obvious, intuitive effects in the Fourier-plane; one is that the visibility amplitude is maximum at zero spatial frequency. The Maximum Entropy Method (see §2.3.3) naturally incorporates this constraint.**

**• “Smoothness.” The Maximum Entropy Method (MEM), for instance, selects the “smoothest” image consistent with the data. See §2.3.3 for more discussion of MEM.**

<!-- page 15 of 86 -->

Optical Interferometry in Astronomy

15

**• a priori Information. One can incorporate previously known information to constrain the possible image reconstructions. For instance, a low resolution image may be available from a single-dish telescope. Another commonly encountered example is point source embedded in nebulosity; one might want the reconstruction algorithm to take into account that the source at the center is point-like from theoretical arguments.**

**For a phased interferometric array (e.g., the Very Large Array) where the Fourier phases are directly measured (avoiding the need for closure phases), one can use a number of aperture synthesis techniques to produce an estimate of an image based on sparsely sampled Fourier components. These procedures basically remove artifacts, i.e. sidelobes, of the interferometer’s point-source response arising from uncomplete sampling of the (u,v) plane. These procedures do not incorporate closure phases, but work by inverting the Fourier amplitudes and phases to make an image.** A **brief explanation of the popular algorithms CLEAN and MEM follow with additional references for the interested reader. See Perley et al. (1986) for essays on these topics aimed at radio astronomers.**

2.3.2. CLEAN Originally described by Högbom (1974), CLEAN has been traditionally **the most popular algorithm for image reconstruction in the radio because it is both computationally efficient and intuitively understandable. Given a set of visibility amplitudes and phases over a finite region of the Fourier plane, the “true” image can be estimated by simply setting all other spatial frequencies to zero and taking the (inverse) Fourier Transform. As one might expect, this process leads to a whole host of image artifacts, most damaging being positive and negative “sidelobes” resulting from non-complete coverage of the Fourier plane; we call this the “dirty map.” The unevenly-filled Fourier plane can be thought of as a product of a completely-sampled Fourier plane (which we desire to determine) and a spatial frequency mask which is equal to 1 where we have data and 0 elsewhere. Since multiplication in Fourier space is identical to convolution in image space, we can take the Fourier transform of the spatial frequency mask to find this convolving function; we call this the “dirty beam.” Now the image reconstruction problem can be recast as a “deconvolution” of the dirty map with the dirty beam.**

**The dirty map is CLEANed by subtracting the dirty beam (scaled to some fraction of the map peak) from the brightest spot in the dirty map. This removes sidelobe structure and artifacts from the dirty map. Repeating this process with dirty beams of ever decreasing amplitudes leads to a series of delta-functions which, when combined, fit the interferometric data. For visualization, this map of point sources is convolved with a Gaussian function whose FWHM values are the same as the dirty beam; this removes high spatial resolution information beyond the classic “Rayleigh” criterion cutoff. One major weakness with CLEAN is that this smoothing changes the visibility amplitudes, hence the CLEANed image no longer strictly fits the interferometric data, especially the spatial frequency information near the diffraction limit. Another weakness is that**

<!-- page 16 of 86 -->

Optical Interferometry in Astronomy

16

**CLEAN does not directly use the known uncertainties in the visibility data, and hence there is no natural method to weight the high SNR data more than the low SNR data during image reconstruction. Further discussion of various implementations of CLEAN can be found in Clark (1980), Schwab (1984), Cornwell (1983), and Chapter 7 of Perley et al. (1986) by T. Cornwell.**

**2.3.3. MEM The maximum entropy method (MEM) makes better use of the highest spatial frequency information by finding the smoothest image consistent with the interferometric data. While enforcing positivity and conserving the total flux in the frame, “smoothness” is estimated here by a global scalar quantity** $\mathrm { S } ,$ **the “entropy.” If** $f _ { i }$ **i**s the fraction of the total flux in pixel i, then $\begin{array} { r } { S = - \sum _ { i } f _ { i } } \end{array}$ ln $\frac { f _ { i } } { I _ { i } }$ after the thermodynamic quantity; $I _ { i }$ **i**s known as the image prior and must be specified by the user. The MEM map $f _ { i }$ will tend toward $I _ { i }$ when there is little (or noisy) data to constrain the fit. Often $I _ { i }$ **i**s assumed to be a uniformly bright background, however one can use other image **priors if additional information is available, such as the overall size of the source which may be known from previous observations.**

**Mathematically, MEM solves the multi-dimensional (N=number of pixels) constrained minimization problem which only recently has become computationally** realizable on desktop computers. Maintaining an adequate fit to the data $( \Sigma \chi ^ { 2 } \sim$ **number of degrees of freedom), MEM reconstructs an image with maximum S. MEM image reconstructions always contain some spatial frequency information beyond the diffraction limit in order to keep the image as “smooth” as possible consistent with the data. Because of this, images typically have maximum spatial resolution a few times smaller than the typical Rayleigh-type resolution encountered with CLEAN (“superresolution”). Further discussions of MEM and related Bayesian methods can be found in Pina and Puetter (1992), Narayan and Nityananda (1986), Skilling and Bryan (1984), Gull and Skilling (1983), and Sivia (1987).**

**Unfortunately, MEM images also suffer from some characteristic artifacts and biases. Photometry of MEM-deconvolved images is necessarily biased because of the positivity constraint; any noise or uncertainty in the imaging appears in the background of the reconstruction instead of the source, systematically lowering the estimated fluxes of compact sources. Also, fields containing a point source embedded in extended emission often show structure reminiscent of Airy rings, the location of the rings being influenced by the wavelength of the observation and not inherent to the astrophysical source. Fortunately, these imaging artifacts are greatly alleviated for asymmetric structures, when closure phases and not the visibility amplitudes play a dominant role in shaping the reconstructed morphology.**

**2.3.4. Including Closure Phase Information The above algorithms were originally designed to use Fourier amplitudes and phases, not closure phases. In order to use these algorithms, one has to come up a way to estimate the Fourier phases, when only the closure phases are available. Early image reconstruction algorithms incorporated closure**

<!-- page 17 of 86 -->

Optical Interferometry in Astronomy

17

![Image block](doc:b6a1ff8/tier:standard/page:17/block:3)

Figure 7. This is a flow diagram for a incorporating closure phase information into CLEAN/MEM aperture synthesis imaging algorithms based on the “self-calibration” procedure of Cornwell and Wilkinson (1981). This figure is reproduced through the courtesy of the NASA/Jet Propulsion Laboratory, California Institute of Technology, Pasadena, California (Monnier, 2000).

**phase information by using an iterative scheme (Thompson et al. 1986; Readhead and Wilkinson 1978). The following steps summarize this process:**

**(i) Start with a Fourier “phase model” based on either prior information or setting all phases to zero.**

**(ii) Determine candidate phases by using some values from the “phase model” and enforcing all the (self-consistent) closure phase relations (see §2.2.3).**

**(iii) Using CLEAN or MEM, perform aperture synthesis mapping on the given visibilities and candidate phases. At this stage, image constraints such as positivity and/or finite support are applied.**

**(iv) Use this image as a basis for a new “phase model.”**

**(v) Go to step 2 and repeat until the process converges to a stable image solution.**

**Cornwell and Wilkinson (1981) introduced a modification of the above scheme by explicitly solving for the telescope-specific errors as part of the reconstruction step. Hence the measured (corrupted) Fourier phases are fit using a combination of intrinsic phases (which are used for imaging using CLEAN/MEM) plus telescope phase errors. In this scheme, the closure phases are not explicitly fit, but rather are conserved in the procedure since varying telescope-specific errors can not change any of the closure phases. Figure 7 shows a flow diagram for this procedure; thoughtful consideration is required in order to fully understand the power and elegance of self-calibration, affectionately known as “self-cal.”**

<!-- page 18 of 86 -->

Optical Interferometry in Astronomy

18

**Self-calibration works remarkably well for large number of telescopes, but requires reasonably high signal-to-noise ratio (SNR>**∼**5) complex visibilities. Once the SNR decreases below this point, the method completely fails. The conceptualization of solving for telescope-specific errors, while useful for the radio, is not applicable for visible/infrared interferometry where the good observables are the closure phases themselves, not corrupted Fourier phases. This is because the time-scale for phase variations in the visible/infrared is much less than a second, as opposed to minutes/hours in the radio.**

**Of course, the self-calibration iteration loop can be sidestepped altogether by fitting directly to all the data, the visibility amplitudes and closure phases, using MEM or some other regularization scheme. This would have the added advantage of allowing all the measurement errors to be properly addressed, theoretically resulting in the optimal image reconstruction. Buscher (1994) suggested this approach, but there has been little demonstrated progress in this method to date. I anticipate revived activity as more interferometers with “imaging” capability begin to produce data.**

**2.3.5. Speckle Interferometry Another related interferometric technique which permits diffraction-limited observation through a turbulent atmosphere using a single filled aperture telescope is “speckle interferometry,” the promise of which was first realized by Labeyrie (1970a) in 1970. In §2.2, I claimed that observed angular size of a point source will be determined entirely by r**<strong><sub>0</sub></strong> **at a given wavelength, and is known as the seeing** disk size, $\Theta _ { \mathrm { s e e i n g } }$ . However, this is only true for a long-exposure image. A single short**exposure image of a star actually consists of a network of small “speckles” extending** over $\Theta _ { \mathrm { s e e i n g } }$

**In the original formulation of speckle interferometry, short exposures of an astrophysical object are made to freeze this “speckling” induced by the turbulent atmosphere. The amount of high-resolution structure in the speckle pattern, as quantified by its power spectrum, is a measure of two things: 1) the quality of the atmospheric seeing, and 2) the high resolution structure in the object of interest. Observing a nearby point-source star allows the calibration of the seeing contribution and thus the extraction of interferometric visibility measurements out to the diffraction limit of the telescope (i.e., the longest baseline). In analyzing this situation, one can think of many virtual subapertures (with size equal to the coherence length** $\mathbf { r } _ { 0 } )$ **spread across the full telescope, with fringes forming between all the subaperture pairs. After the original formulation by Labeyrie, it was discovered that the Fourier phases could also be estimated from such data (e.g., Knox and Thompson, 1974; Weigelt, 1977).**

**Speckle interferometry data is often reduced using the “bispectrum,” which permits a direct inversion from the estimated Fourier amplitudes and phases. The bispectrum** $\tilde { B } _ { i j k }   =   \tilde { \mathcal { V } } _ { i j } \tilde { \mathcal { V } } _ { j k } \tilde { \mathcal { V } } _ { k i }$ **is formed through triple products of the complex visibilities around a closed triangle, where** $i j k$ **specifies the three aperture locations on the pupil of the telescope. One can see the bispectrum is a complex quantity, and that the bispectrum phase is identical to the closure phase. Interestingly, the use of the bispectrum for**

<!-- page 19 of 86 -->

Optical Interferometry in Astronomy

19

**reconstructing diffraction-limited images was developed independently (Weigelt 1977; Hofmann and Weigelt 1993) of the closure phase techniques, and the connection between the approaches realized only later (Roddier, 1986; Cornwell, 1987).**

## 2.4. Other Important Considerations

**2.4.1. Coherency The tolerance for matching pathlengths in an interferometer depend on the desired spectral bandwidth. In the limit of monochromatic light, such as for a laser, interference will occur even when pathlengths of an interferometer are highly mismatched. For broadband (“white”) light, the number of fringes in an interferogram** is equal to the inverse of the fractional bandwidth: $\begin{array} { r } { N _ { \mathrm { f r i n g e s } } \; \sim \; \frac { \lambda } { \Delta \lambda } } \end{array}$ **Hence, for broad band observations (∼20% bandwidth) interference is only efficient if the pathlengths are matched to within a wavelength or so – a stringent requirement.**

**2.4.2. Field-of-View One consequence of the short coherency envelope for broadband observations is a limitation on the field-of-view. Bandwidth-smearing, as it is called, limits the field-of-view to be equal to the fringe-spacing × the number of fringes in** the coherency envelope (see last subsection), $\begin{array} { r } { \mathrm { F O V } \sim \frac { \lambda } { \mathrm { B a s e l i n e } } \times \frac { \lambda } { \Delta \lambda } } \end{array}$ **radians. This “field of-view” is thus baseline-dependent, leading to confusing interpretations of data for extended sources. While this effect can be modeled, it should be avoided by using a spectrometer to limit the bandwidth of individual observing channels.**

**Another common limitation of the field-of-view is the primary beam of an individual telescope. For most kinds of beam-combiners, flux outside the diffraction-limited beam is rejected (spatial filtering is described more fully in §3.5.1). For most astronomical objects observed by interferometers, this is not a serious problem since long integrations by (low-resolution) individual telescopes can be used to confirm that no significant flux arises from outside the primary beam. For an imaging interferometer, one would like to use narrow enough bandwidths so that bandwidth-smearing (on the longest baselines) is small enough so that the entire primary beam can be mapped. The requirement for** this is approximately: $\begin{array} { r } { \frac { \lambda } { \Delta \lambda } \sim \frac { \mathrm { L o n g e s t ~ B a s e l i n e } } { \mathrm { T e l e s c o p e ~ D i a m e t e r } } } \end{array}$

**Of course, having a wide field-of-view would be useful for many studies, such as measuring proper motions of stars at the galactic center. As discussed later, a wide field of-view (beyond the primary beam) can only be achieved in a so-called Fizeau combiner. The Large Binocular Telescope Interferometer is the only interferometer currently being built which will have this unique and potentially very powerful faculty.**

**2.4.3. Filling the** $( u , v )$ **Plane The ability to make an image depends most strongly on the filled fraction of the (u,v) plane. Recall that the visibility amplitude and phase measured by an interferometer is directly related to a single component of the Fourier Transform of the object brightness distribution. If the object brightness is specified on coordinates of Right Ascension (pointing East) and Declination (pointing North), then the reciprocal Fourier space has axes referred to as (u,v). Following astronomical**

<!-- page 20 of 86 -->

Optical Interferometry in Astronomy

20

**notation, the positive u-axis typically points to the left on a diagram, just as rightascension coordinates increase towards the left (East).**

**For a fixed geometry of telescope locations, the Fourier coverage varies as the star rises and sets, and as a function of the star’s declination and the interferometer’s latitude. Figure 8 shows the Fourier coverage of three actual interferometers (number of telescopes 3, 6, and 21 for IOTA, CHARA, and Keck aperture masking respectively) for a declination** $4 5 ^ { \circ }$ **object spanning 3 hours before and after transit (assuming monochromatic light). In aperture masking, the pupil plane of a single telescope is split up into sub-pupils which are allowed to combine, just like a long-baseline interferometer. It is obvious that that the coverage increases rapidly with number of telescopes. It is not so obvious that the number of closure phases/triangles also rapidly increases with array size (equivalent to filling up the hyper-volume** $\left( \mathrm { u _ { 1 } , } \mathrm { v _ { 1 } , } \mathrm { u _ { 2 } , } \mathrm { v _ { 2 } } \right)$ **with closure triangles; see Table 1). Tuthill and Monnier (2000) studied how imaging fidelity and dynamic range are affected by differing amounts of Fourier coverage using real data. Obviously for imaging it is absolutely critical to collect as much coverage as possible, and suitable array design is further discussed in §3.2.**

## 3. Basic Designs of Stellar Interferometers

## 3.1. Brief Historical Overview

**Here I give only a brief historical overview of progress in stellar interferometry drawn partially from the review by Lawson (2000a); I refer the interested reader to the above article for more information.**

**Modern interferometry can be traced back to 19th century France. Hippolyte Fizeau first outlined in 1868 the basic concept of stellar interferometry, how interference of light could be used to measure the sizes of stars. The first attempts to apply this technique,** akin to modern-day “aperture masking,” were carried out by E. Stéphan soon thereafter, **although the telescopes of the time had insufficient resolution to resolve even the largest stars.**

**Albert Michelson developed a more complete mathematical framework for stellar interferometry in 1890; while apparently Michelson was unaware of Fizeau’s earlier work, more historical investigation is needed to establish this definitively. Along with Pease, Michelson (Michelson and Pease, 1921) eventually succeeded in measuring the diameter of α Orionis (Betelgeuse) in 1920-21 using the Mt.** Wilson $1 0 0 ^ { \circ }$ **telescope (following earlier measurements of Jupiter’s moons; Michelson, 1890, 1891). Interestingly, Michelson needed a baseline longer than** $1 0 0 ^ { \prime \prime }$ **in order to resolve Betelgeuse (uniform disk diameter ∼47 mas), and acquired one by installing a 20-foot interferometer beam on the Cassegrain cage as illustrated in Figure 9, reproduced here from their original paper. Following the success of the 20-foot interferometer, Pease (with Hale) constructed a 50-foot interferometer (on Mt.** Wilson, but separate from the $1 0 0 ^ { \circ }$ **telescope); although some results were reported, this experiment was not very successful.**

<!-- page 21 of 86 -->

![Chart block](doc:b6a1ff8/tier:standard/page:21/block:1)

Figure 8. Example of $\left( \mathrm { u , } \mathrm { v } \right)$ plane coverage for different interferometers. The top panels show the interferometer array configurations, while the bottom panels show the corresponding $( \mathrm { u , } \mathrm { v } )$ plane coverage. For the IOTA and CHARA interferometers, I have assumed a source at $4 5 ^ { \circ }$ declination observed for three hours both before and after transit. The right-most panels show instantaneous “snapshot” coverage for an optimized 21-telescope array, a geometry actually used in the Keck aperture masking experiment (Tuthill et al., 2000c). Note that the circles in the top plot are not to the same scale as the individual telescopes diameters but have been enlarged.

Optical Interferometry in Astronomy

21

**Due to its generally outstanding atmospheric conditions, Mt. Wilson continued to be a choice site for interferometry projects, subsequently hosting the Mark III, ISI, and CHARA interferometers.**

**Following the disappointing results from the 50-foot interferometer, it would be decades before significant developments inspired new activity in the optical arena. Meanwhile, advances in radar during World War II spurred rapid development of radio interferometry. We refer the reader to Thompson et al. (2001) for a discussion of the development of radio interferometry beginning with the first radio interferometer built by Ryle and Vonberg in 1946.**

**The unexpected success of “intensity interferometry” would inspire a host of new projects. The basic principle behind the intensity interferometer was laid out in Hanbury Brown and Twiss (1956a), and describes how correlations of intensities (not electric fields) can be used to measure stellar diameters. First results were reported soon thereafter (Hanbury Brown and Twiss, 1956b), leading to the development of the**

<!-- page 22 of 86 -->

Optical Interferometry in Astronomy

22

![Image block](doc:b6a1ff8/tier:standard/page:22/block:3)

Figure 9. This diagram from Michelson and Pease (1921, Figure 1) illustrates how a 20-foot interferometer beam was installed on the Mt. Wilson 100” telescope in order to create, for the first time, an interferometer capable of measuring the diameter of stars beyond the Sun. Figure reproduced by permission of the AAS.

**Narrabri Intensity Interferometer. With a 188 m longest baseline and blue-sensitivity, this project had a profound and lasting impact on the field of optical interferometry, measuring dozens of hot-star diameters (e.g., Brown et al., 1967a,b; Davis et al., 1970; Hanbury Brown et al., 1970, 1974a). The small bandwidths attainable with Intensity Interferometry limited the technique to the brightest stars, and pushed the development of so-called “direct detection” schemes, where the light is combined before detection to allow large observing bandwidths. This group would go on to develop the SUSI interferometer.**

**Dr. Charles Townes, inventor of the maser, began a novel interferometer project during this same time period at University of California at Berkeley. He used heterodyne receivers as in radio interferometry, but the local oscillators were** $\mathrm { C O _ { 2 } }$ **lasers operating at frequencies of ∼27 THz (or ∼10 µm wavelength), orders of magnitude higher than radio or microwave oscillators. First experiments were performed using the twin McMath auxiliary telescopes (separation 5.5 m) at Kitt Peak, AZ; first fringes were obtained on the limb of Mercury in 1974 (Johnson et al., 1974) and on stars in 1976 (Sutton et al., 1977, 1978, 1979, 1982) where cool dust shells were detected around many late type stars. heterodyne detection also suffers from bandwidth limitations (like Intensity Interferometry) as well as additional noise contribution from laser shot-noise, which becomes progressively worse at higher frequencies. The Townes group went on to develop the ISI interferometer on Mt. Wilson.**

**Other mid-infrared efforts also are worthy of note. An independent project at Arizona using a kind of aperture masking on a single large telescope (using direct**

<!-- page 23 of 86 -->

Optical Interferometry in Astronomy

23

**detection) took place almost simultaneously with the Townes’ experiments (McCarthy and Low, 1975; McCarthy et al., 1977, 1978). In France, Jean Gay and collaborators pursued long-baseline interferometry, both through heterodyne detection (e.g., Gay and Journet, 1973; Assus et al., 1979) and later direct detection efforts (e.g., Rabbia et al., 1990).**

**Long-baseline interferometry on a star by directly combining the electric fields before photon detection (“direct detection”) was first accomplished in 1974 by Labeyrie (1975), using a 12-m baseline. This continued the long history of interferometry innovation in France (starting from Fizeau), and many important experiments have followed. I note that “Speckle Interferometry” was first described by Labeyrie (1970b) and these ideas were also very influential to the field. However, I will largely limit this review to separate-element, or long-baseline, interferometry, and will omit comments on speckle. Following this 1974 demonstration in Nice, the project moved to the Plateau** de Calern site and become known as the Interféromètre à 2 Télescopes (I2T). The I2T **made measurements in the visible (e.g., Blazit et al., 1977) and in the near-infrared (di Benedetto and Conti, 1983; di Benedetto, 1985). The Grand I2T (GI2T, Mourard et al., 1994) began soon thereafter and was developed in parallel with the I2T on the same plateau, but with larger telescopes (1.5 m) and longer maximum baselines (up to 65 m).**

**At a time when it was a struggle to simply get two telescope interferometers working, considering the array of telescopes needed for imaging was indeed far-fetched. Thus, imaging using optical interferometry began with aperture masking experiments on large single-aperture telescopes (in the tradition of Michelson). In aperture masking, a pattern of holes (size <**∼**r**<strong><sub>0</sub></strong> **in diameter) is cut in a plate and placed in the pupil plane of a large telescope. The interference pattern formed thus simulates one from an array of telescopes combined like a Young’s multi-slit experiment. Baldwin et al. (1986b) and Haniff et al. (1987b) showed how aperture masking in the visible yield data identical to that expected for an imaging array, and produced images of binary stars using closurephase imaging. This group, based at the University of Cambridge, England, would soon begin developing the COAST interferometer, which would succeed in producing the first image with an aperture synthesis optical array (Baldwin et al., 1996b). Infrared aperture masking at the Keck Telescope (Tuthill et al., 2000c) also grew out of work from this group in collaboration with the U.C. Berkeley ISI team, and excited unexpected imaging results from this work have led to much enthusiasm for developing infrared imaging capabilities for long-baseline interferometers such as CHARA and VLTI.**

**There is one remaining important interferometer lineage to mention, one which led to the modern development of “fringe-tracking” interferometers such as the NPOI, PTI, and Keck Interferometers, as well as numerous experimental innovations. The Massachusetts Institute of Technology and the Naval Research Laboratory built and operated a series of prototype interferometers, named the Mark I, Mark II, and the Mark III. Shao and Staelin (1980) reported the first successful active fringe-tracking results, and this group has been most active at pushing the use of interferometers for precision astrometry. The Mark III was located on Mt. Wilson and was a fully**

<!-- page 24 of 86 -->

Optical Interferometry in Astronomy

24

**automated interferometer operating in the visible with baselines up to 20 m (Shao et al., 1988). The high efficiency allowed many astronomical programs to be carried out until it was shut down in about 1993, and is widely considered one of the most productive interferometers to date. Numerous articles were published covering areas of astrometry, angular diameters, precision binary orbits, and limb-darkening (e.g., Mozurkewich et al., 1988; Hutter et al., 1989; Mozurkewich et al., 1991; Armstrong et al., 1992; Hummel et al., 1995; Quirrenbach et al., 1996).**

**I should also mention the prototype interferometer IRMA (Infra-Red Michelson Array), built at University of Wyoming (Dyck et al., 1993). While this instrument did not operate for very long, those involved were largely responsible for initial success with infrared observing at IOTA and have had lasting impacts at a number of other currently operating U.S. facilities, including NPOI, PTI, and Keck Interferometers.**

**This section was meant to introduce historical interferometers (ones no longer in operation) which have had a lasting impact on the field, and I have left descriptions of currently operating interferometers to §3.6. As discussed in the opening, this review is not meant to document all the important results from these first generation facilities, but rather to give appropriate historical background for understanding the current stateof-the-field.**

## 3.2. Overview of Interferometer Design

**Compare Young’s two-slit experiment (Figure 1) to what you see in Figure 10. We see telescopes instead of slits and a beam combiner (with relay optics) instead of a screen for viewing the fringes. In a real interferometer, we must use delay lines to compensate for geometrical delay introduced by sidereal motion of a star across the sky; in this way, we “point” the interferometer at the target. In order to successfully interfere light together, each interferometer will have many subsystems, and in this review we will describe the state-of-the-art developments for the Telescopes, the Relay Optics, the Delay Lines, and the Beam Combination.**

**Before discussing each of the critical subsystems, the importance of the physical placement of the telescopes for imaging will be discussed. Many of these issues are discussed in more detail by Mozurkewich (2000), and here we consider array design from the perspective of imaging, not for specialized purposes such as nulling or astrometry.**

**If there were no practical constraints and telescopes could be placed optimally, one could consider many possibilities. Studies have been published considering distributions based on optimizing uniformity of (u,v) coverage using three-fold symmetric patterns** (used in Keck aperture masking, Golay, 1971), Reuleaux triangles (used for the Sub **Millimeter Array, Keto, 1997), a spiral zoom array (considered for the Atacama Large Millimeter Array, see ALMA memos #216, 260, 283, and 291), and a Y-shaped array (adopted by the Very Large Array). While the first three of these methods offer better Fourier coverage than the Y-shaped array, the “imaging” interferometers of NPOI and CHARA both use a Y-shaped array – why?**

<!-- page 25 of 86 -->

Optical Interferometry in Astronomy

25

![Image block](doc:b6a1ff8/tier:standard/page:25/block:3)

Figure 10. This schematic illustrates the major subsystems of a modern optical interferometer: the Telescopes, the Relay Optics, the Delay Lines, and the Beam Combination.

**For the VLA, an important reason for using a a Y-shaped array was a practical one; it was easy to move the telescopes along railroad tracks in order to cheaply and easily reconfigure the array geometry. While optical telescopes in arrays do not generally run on tracks (except at IOTA), the desire to transport light to a central facility (see §3.3.2) leads one to a Y-shaped geometry where the three-arms of the array are defined by vacuum pipes which relay beams from the telescopes to the delay lines and combiners. The NPOI interferometer (shown here in Figure 11) has many stations along the three vacuum arms where telescopes can be located, thus creating a flexible, reconfigurable system capable of pursuing many astronomical programmes. Another theoretical benefit of this design is that many telescopes can be arranged along each arm allowing “baseline bootstrapping” for imaging highly resolved targets, a technique where strong fringes measured between close-by telescopes are used to “phase-up” the fringes on the longer baselines.**

## 3.3. Critical Subsystems Technologies

**3.3.1. Telescopes All interferometers need light collectors of some kind. In many cases, simple “siderostats” are used, whereby a steerable flat mirror directs starlight either directly to the interferometer or first through a beam-compressor (“afocal” telescope).**

<!-- page 26 of 86 -->

Optical Interferometry in Astronomy

26

![Image block](doc:b6a1ff8/tier:standard/page:26/block:3)

Figure 11. Overhead view of the NPOI interferometer array, to show the Y-shaped array layout, defined by vacuum pipes extending out to many possible siderostat “pads,” or stations. Photograph reproduced with permission of the Naval Research Laboratory.

**A siderostat has limited sky coverage and makes polarization measurement difficult (due to the changing, non-normal reflection angles off the flat), but is thought to offer a more stable structure for minimizing vibrations and pivot-point drifts for accurate astrometry. More recent interferometers, such as CHARA, VLTI, and Keck, have chosen traditional altitude-azimuth (“alt-az”) telescope designs which give full-sky coverage and potentially salvaging polarization work. In addition, all interferometer telescopes have incorporated fast “tip-tilt” guiding which tracks (and corrects) fast jitter of the stellar image, usually using visible-light “quad-cell” detectors. This corrects the first-order term of the wavefront perturbations, aligning the wavefronts to allow for stable beam combination.**

**Without high-order adaptive optics, there is little use for a telescope aperture much larger than the atmospheric coherence length** $r _ { 0 }$ **(see §2.2). Hence, most telescopes in today’s interferometers are small by “modern” (8-m class) telescope standards. Dedicated visible-light interferometers (e.g., NPOI, SUSI) have telescope apertures around 12-14 cm in diameter; near-infrared interferometers (e.g., PTI, IOTA, COAST) have apertures diameters around 45 cm. The recently-built CHARA interferometer includes 1 m apertures which can take advantage of excellent seeing conditions in the**

<!-- page 27 of 86 -->

Optical Interferometry in Astronomy

27

**infrared, and could benefit from adaptive optics correction; the Keck and VLT auxiliary telescopes were specified to be 1.8 m for similar reasons. However, interferometry is not just for “small” telescopes anymore, since the world’s largest telescopes, the two Keck telescopes and also the four VLT telescopes, are now part of the new generation of optical interferometers. As of 2002, only the Keck Interferometer has observed using adaptive optics, although the VLT Interferometer will soon possess this capability. See Table 3 for a summary of telescope apertures of today’s interferometers.**

**3.3.2. Relay Optics, Delay Lines, & Metrology After being collected by the telescopes, the light must be directed to a central facility for beam combination. While it may seem trivial to set up a series of mirrors for this purpose, there are many subtle issues that must be addressed. Traub (1988) discussed how the geometry of the relay optics must not corrupt the relative polarization of the beams, due to differential phase shifts between the s- and p-wave reflections from the mirror surfaces for non-normal incidence. One must pay attention to the issues of mirror and window coatings as well as geometry.**

**In addition, due to the long path lengths between the telescope and central beam combining facility, significant differential chromatic dispersion occurs if the light is propagating in air. In order to combine broad bandwidths, one must either transport the light through a vacuum or construct a dispersion compensator (Tango, 1990; ten Brummelaar, 1995), whereby wedges of glass are inserted into the beam to compensate for air’s index of refraction; a combination of partial vacuum plus dispersion compensation is also possible. The size of the mirrors in this optics chain is also important for limiting the effect of diffraction (Horton et al., 2001), and often also sets the field-of-view of the interferometer. Lastly, because of the many reflections, high reflectivity of the relay optics must be maintained to maximize throughput and sensitivity; a side-benefit of evacuated relay optics is that the mirrors stay clean.**

**Because of the Earth’s rotation, the apparent position of an astronomical object is constantly changing. In order to track this sidereal motion, a movable delay line is needed to compensate for changing geometrical delay between wavefronts reaching any two telescopes. The diagram in Figure 10 shows this delay line as a right-angle retroreflector, although most interferometers do not actually use this geometry. The requirements on this system are amazingly stringent: nanometer-level precision moving at high speeds** $\left( >   1   \mathrm { c m / s } \right)$ **and over long distances (>100 m) – a dynamic range of** $> 1 0 ^ { 1 0 } !$

**By far the most popular architecture today for the moving delay line is based on the solution implemented by the Mark III interferometer (Shao et al., 1988; Colavita et al., 1991). The retroreflection is produced by focusing the incoming beam to a point coincident with a small flat mirror (attached to a piezo-electric stack), which reflects and re-collimated; a practical optical system is illustrated in Figure 12. This mirror system is mounted on a flexible stage which can be translated using a voice coil. Lastly, this whole stage is mounted on a wheeled-cart, which is driven on a rail by linear motors. This system has three nested feedback loops, driven by laser metrology: precise sub-**

<!-- page 28 of 86 -->

Optical Interferometry in Astronomy

28

![Image block](doc:b6a1ff8/tier:standard/page:28/block:3)

Figure 12. Diagram of the most standard delay line architecture used in optical interferometry, originally from the Mark III interferometer. Figure reproduced from Shao et al. (1988, Figure 4) with permission of ESO.

**wavelength control is maintained by the piezo-driven small mirror, when this mirror exceeds its normal operating range (∼50µm) then offsets are given to the voice-coil stage, and so on. This basic architecture is in use at most interferometers built in the last 10 years; alternate delay lines include floating dihedrals mirrors on an air table (IOTA) and moving the beam combination table itself (GI2T).**

**3.3.3. Beam Combination & Fringe Modulation Once the beams have been delivered to a central combination facility and have been properly delayed, there are many ways to actually do the interference. Here I discuss image-plane and pupil-plane combination (also know as “Fizeau” and “Michelson” combination, respectively), along with spatial versus temporal modulation of the fringes themselves.**

**Figure 13 show these two different ways of detecting fringes in a two-element interferometer. In one case, an imaging system is used to fill the image plane with the equivalent of Young’s fringes. As one moves along the image plane, there is a different relative delay between the interfering beams, and hence the modulation (fringes). In this scheme, there is no need to actively modulate the fringes; in fact, atmospheric turbulence will introduce relative delays and cause the fringe pattern to “slide” back and forth, smearing out the fringes on short time-scales if not stabilized. This combination scheme most closely follows the “two-slit” interferometer analogy developed in earlier sections.**

**The second scheme, and currently the most common one, is pupil-plane combination, or “Michelson”-style combination. Interestingly, this method is named after Michelson, not because of his stellar interferometry work (which used “Fizeau” combination, see §3.1), but because of the interferometer used in the Michelson-Morley experiment. In this method, the wavefronts from the two collimated telescope beams are overlapped on a 50/50 beamsplitter. Depending on the phase relationship of the waves, differing amounts of energy will be transmitted or reflected at the beamsplitter. Single-pixel detectors can then be used to measure the energy on both sides of the beamsplitter (the sum of which is conserved). The popular adoption of this method**

<!-- page 29 of 86 -->

Optical Interferometry in Astronomy

29

Beam Combination Schemes

![Image block](doc:b6a1ff8/tier:standard/page:29/block:4)

Figure 13. Diagram of Image-plane and Pupil-plane beam combination techniques. The left panel shows image-plane, or Fizeau combination, where light from the two telescopes are brought together in an image plane to interfere, just like Young’s two-slit experiment. The right panel shows how pupil-plane (or “Michelson”) interferometry superimposes the two collimated beams at a beam-splitter. By modulating the time delay of one beam with respect to the other (e.g., with the delay line), the interference can be modulated and fringes detected using single-pixel detectors.

**results largely from the signal-to-noise benefits of using single pixel detectors. In order to measure the amplitude of the coherence, a dither mirror (often in the delay line) sweeps through a linear pathlength difference of many wavelengths. The white-light fringe, or interferogram, can then be recorded, as long as the scanning takes place faster than an atmospheric coherence time.**

**When dealing with an array of telescopes, there are more options. ten Brummelaar (1993) outlined some forward-looking beam combiner designs in the context of the CHARA array and useful articles by Mozurkewich (2000) and Mariotti et al. (1992) also contain extended discussion on the subject; here I only mention the highlights. The image-plane method can be extended to arbitrary number of telescopes, as long as the spacings between the beams are non-redundant, so that each beam-pair will have a unique fringe spatial frequency in the image-plane. Labeyrie (1996) elaborates on the concept of pupil densification, an idea finding increasing application in modern interferometry. The pupil-plane method can also be extended, either by combining the beams “pair-wise” or “all-in-one.” In a pairwise-scheme, each telescope beam is split using beamsplitters and then various combinations are created to measure all the baselines. In the all-in-one scheme, more than two beams are superimposed and the fringes from different pairs are distinguished by modulating the delays such that each baseline pair has a unique fringe temporal frequency in the readout. There are methods**

<!-- page 30 of 86 -->

Optical Interferometry in Astronomy

30

**which combine pair-wise with all-in-one and are called “partial-pairwise.” Each method has its advantages and disadvantages, depending on the availability of focal plane arrays, the level of readnoise vs. photon noise, the required calibration precision, etc. However, in general, “pair-wise” detection is the worst method for large number of telescope because the light has to be split more times (see Buscher, 1988, although beware of some important simplifications made in this analysis).**

**Coherent beam combination can be discussed more generally depending whether the interference occurs in the image/pupil plane and whether the telescope beams are co-axial or multi-axial. I refer the reader to the influential internal ESO report by Mariotti et al. (1992), which explains and defines the useful vocabulary in common use by the European interferometry community.**

**We contrast the many imperfect beam combination strategies in the optical with those adopted in radio interferometry. At radio and microwave frequencies, the signals from each telescope can be split and re-amplified without introducing additional noise after the initial coherent detection (radio interferometers do not operate close to the Poisson limit). Hence, a pair-wise combination scheme can be employed without any loss in signal-to-noise ratio. In addition, the electric field at each telescope can be truly cross-correlated with that from all others leading to a kind of Fourier Transform spectroscopy. Further, this can all be done using digital electronics after fast digitization of the signals. For more information, see the description of the Hat Creek mm-wave correlator by Urry et al. (1985). At the end of this process, the digital correlators can recover all baselines with arbitrary spectral resolution without lost sensitivity – a dramatically superior situation than possible in the photon-starved visible and infrared regime!**

**3.3.4. Fringe Tracking An increasingly popular and powerful capability for optical interferometry is called “Fringe Tracking.” To do so, the white-light fringe has to be actively tracked because atmospheric fluctuations cause the location of the fringe to vary by up to hundreds of microns on sub-second time scales. There are two levels of tracking these fringes, one is called “coherencing” and the other is called “fringe tracking,” although these terms are often used rather loosely.**

**In “coherencing,” the interferometer control system will track the interferogram location to a precision of a few wavelengths. In a scanning interferometer, this will be sufficient to keep the full interferogram within the scanning range of the delay line. In an image-plane combiner, this will ensure you are near the peak of the white-light fringe (inside the coherence envelope set by the spectral bandpass). This can be done on a rather leisurely timescale, since large optical path distance (OPD) fluctuations tend to occur of slower time scale: update rates of ∼1 Hz are sufficient except for the worst seeing conditions.**

**True “Fringe Tracking” (also called “co-phasing”) requires tracking OPD fluctuations within a small fraction of wavelength in real-time, and hence requires orders of magnitude faster response (a time scale which depends on the wavelength and**

<!-- page 31 of 86 -->

Optical Interferometry in Astronomy

31

**seeing conditions). In the most common implementation (the “ABCD” method; see Shao and Staelin, 1977), two beams are combined pairwise while a mirror is stepped at quarter-wavelength intervals. The broadband white-light fringe is detected at one of the beamsplitter outputs, and fringe data is recorded synchronous with the dither mirror, resulting in four measurements (A,B,C,D) representing four different fringe phases. A discrete Fourier Transform (effectively) can be rapidly applied to the data, resulting in a fringe phase estimate. This offset can be sent to the interferometer delay line control system to nearly instantaneously correct for atmospheric turbulence (details in Shao et al., 1988; Colavita, 1999). The light from the other beamsplitter output is usually dispersed and multi-wavelength data is collected. I also refer the reader to Lawson (2000), where the ABCD method (and other “phase” estimators) or compared to to “Group Delay” tracking methods, which use phase measurements at different wavelengths to measure interferometer delay offsets.**

**Historically speaking, active fringe tracking has been important only for the Mark III interferometers and its successors (NPOI, PTI, Keck Interferometer). One reason fringe tracking has not been more widely pursued is because the sensitivity limit of a fringe tracking interferometer is less than fringe-envelope scanning interferometer. This is because very short integration times are required to stay on the fringe and hence the source must be fairly bright; in the fringe envelope scanning method, one has to only keep the interferogram in the scanning range and thus any given fringe measurement can have a lower signal-to-noise ratio. In practice, this amounts to sensitivity difference of a few magnitudes.**

**As interferometers become more powerful and seek greater capabilities, fringe tracking is becoming a standard feature. High spectral resolution interferometry data is possible with fringe tracking systems, because a broadband white-light fringe can be used for fringe tracking while the remaining output channels can be dispersed. Normally, this data would have very low signal-to-noise ratio, but if the fringe tracking essentially “freezes” the turbulence, the dispersed fringes can be detected by integrating on the detector much longer than the typical atmospheric coherence time. Hence, fringe tracking is a kind of “adaptive optics” for interferometry.**

**3.3.5. Detectors The most desired properties for detectors used in optical interferometry are low noise and high readout speed, two qualities usually not found at the same time. At the beginning of optical interferometry, the only visible-light detector was photographic film and infrared detectors were only just invented. Detectors have made incredible advances over the last few decades, and are operating near their fundamental limit in most wavelength regimes (the near-infrared is a notable exception).**

**After years of struggling with custom-built photon-counting cameras for visible light interferometry work, such as the PAPA camera (Papaliolios et al., 1985; Lawson, 1994) and intensified CCDs (e.g., Blazit, 1987; Foy, 1988), commercial devices are being sold aimed at the adaptive optics market which have high quantum efficiencies (>50%), kilohertz frame times, and read noise of only a few electrons (fast readout CCDs). For**

<!-- page 32 of 86 -->

Optical Interferometry in Astronomy

32

**beam combinations schemes where single pixel detectors are suitable, Avalanche Photo-Diodes (APDs) have as high quantum efficiency as CCDs but can photon-count at rates up to 10 MHz, although the best commercial devices seem to have an expensive tendency to stop working. This covers wavelengths from the blue to approximately the silicon cutoff (∼1 µm).**

**In the near-infrared (1-5µm), there has been amazing progress this decade. After early work with single-element detectors (e.g, using material InSb), modern** interferometers have taken advantage of technology development at Rockwell in near **IR focal plane arrays made of HgCdTe, such as the NICMOS3, PICNIC, and HAWAII chips. These arrays have high quantum efficiency (>70%) and can be clocked at ∼MHz pixel rates with as low as 15 e- readnoise. While not optimal, this represents orders-of magnitude improvement over photodiodes and has allowed new kinds of astronomical sources to be observed (most notably, young stellar objects). The noise can be further reduced by reading each pixel many times, a novel mode known as “non-destructive” readout. Hence, by reading a pixel n times before resetting, one can reduce the effective** readnoise by approximately ${ \sqrt { n } } ,$ **for n<**∼**20. Interferometry benefits greatly from this capability, since only a few pixels need be readout, allowing large number of “reads” to be made in a short period of time (interferometry reference Millan-Gabet et al., 1999a).**

**Traditionally, the HgCdTe detectors had a cutoff wavelength of 2.5µm, but recent Molecular Beam Epitaxy (MBE) processes allow this cutoff to be tuned to much longer (or shorter) wavelengths (allegedly even beyond 5µm). For a 2.5µm cutoff, these detectors must be operated at liquid nitrogen temperatures (77 K) in order not to be saturated with dark current from thermally-generated electrons. An important recent development is that Raytheon has begun to compete with Rockwell in this market, and we can hope for even greater advances in HgCdTe arrays in the coming years as well as possibly even price reductions.**

**Other materials, such as InSb, can be used for even longer wavelength performance. At 5µm and longer wavelengths, thermal background levels are sufficiently high that these detectors must be readout very rapidly, and can usually work in backgroundlimited mode (despite >500 e- readnoise). This means that Poisson fluctuations in the thermal background flux dominate over other sources of noise (e.g., read noise); the only way to reduce the effect of this background noise is to increase the quantum efficiency of the detector or to reduce the thermal background load on the detector. Various companies have sold focal plane arrays in the “mid-infrared” (∼8-25µm) over the years, and are not all independent efforts after a complicated series of company sales (e.g., Hughes, Santa Barbara Research Center, Raytheon, Boeing). Recently Raytheon has been offering Si:As Impurity Band Conduction (IBC) 320x280 focal plane arrays, which also operate at the background-limit. These detectors must be cooled below 77 K to avoid high dark currents, and generally use liquid Helium. Uniquely, the ISI interferometer uses a single-element HgCdTe photodiode with high signal level (using** $\mathrm { C O _ { 2 } }$ **laser local oscillator) which have up to 25% quantum efficiency and a 5 GHz output bandwidth.**

<!-- page 33 of 86 -->

Optical Interferometry in Astronomy

33

**3.3.6. System Control It is not trivial to control all the important subsystems of an interferometer. Many current interferometers (e.g., ISI, IOTA, PTI, Keck, VLTI) use the VME realtime architecture under the vxworks operating system (Wind Rivers). This allows different subsystems to be easily synchronized at the millisecond (or better) level. VME systems are fairly expensive, and some groups (in particular, CHARA) have adopted the RT (RealTime) Linux OS running on networked personal computers.**

## 3.4. Sensitivity

**Optical interferometers are orders-of-magnitude less sensitive than single-dish telescopes. At visible wavelengths where sensitivity is the worst, current interferometers have a similar limiting magnitude as the human eye (e.g., V mag ∼6 at NPOI). In this section, we explore the current and future sensitivities of optical interferometers.**

**3.4.1. What sets the limiting magnitude? There are three major problems which limit the sensitivity of today’s interferometers: the atmosphere, optical transmission, detector/background noise.**

**The sensitivity is most dramatically limited by the atmosphere which restrict the coherent aperture size and coherent integration time. We can use the notion of a coherent volume of photons which can be used for interferometry, with dimensions set entirely by the atmosphere. The coherent colume has dimensions of** $r _ { 0 } \times r _ { 0 } \times c \tau _ { 0 }$ **, and hence is very sensitive to the seeing. Consider average seeing conditions in the visible** $( r _ { 0 }   \sim   1 0   \mathrm { c m }$ $t _ { 0 }   \sim   1 0   \mathrm { m s } )$ **,** we can estimate a limiting magnitude by requiring at least 10 photons to be in this coherent volume. Assuming a bandwidth of 100 nm, 10 photons $( \lambda \sim$ **550 nm) in the above coherent volume corresponds to a V magnitude of 12.6, which is more than 10 magnitudes brighter than faint sources observed by today’s 8-m class telescope. Because the atmospheric coherence length and time scale approximately like** $\lambda ^ { \frac { 6 } { 5 } }$ for Kolmogorov turbulence, the coherent volume ∝ $\lambda ^ { \frac { 1 8 } { 5 } }$

**Current interferometers can not achieve this limiting magnitude because of additional problems. The most important in the visible is low optical throughput due to the large number of reflections between the telescopes and the final detector. The number of reflections easily exceeds 10 and is often closer to 20. Even with high quality coatings of 97% reflectivity, we see that ∼50% of the light would be lost after 20 bounces** $( 0 . 9 7 ^ { 2 0 }   =   . 5 4 )$ **. In practice, current interferometers have visible-light transmission between 1% and 10%, due the fact that coatings degrade with time, the need for dichroics and filters with relatively high losses, and some diffractive losses during beam transport. Of course, detectors also do not have 100% quantum efficiency. The COAST interferometer has achieved the faintest limiting magnitude in the visible of ∼9 mag, by optimizing throughput, detector quantum efficiency, and bandwidth (as another example, the NPOI interferometer which fringe-tracks and uses narrower** bandwidths has a limiting magnitude around ∼6)

**Throughput issues can be improved multiple ways. Lawrence Livermore Laboratory**

<!-- page 34 of 86 -->

Optical Interferometry in Astronomy

34

**is researching new coatings for mirrors which will have >**∼**99% reflectivity at most nearand mid-infrared wavelengths. In addition, simplified beam trains with few reflections are being designed for next generation interferometers. Lastly, the use of fiber and integrated optics could potentially lead to high throughput systems in the future; these developments are discussed more fully in §3.5.**

**The last major limitation is noise associated with the detection. Some visible light detectors, such as the photon-counting Avalanche Photo-Diodes, are almost perfect in this regard, boasting very low “dark counts”** $( { < } 1 0 0 ~ \mathrm { c t / s } )$ **and high quantum efficiency. However, this is not true in the infrared. Even the best infrared detectors have** ${ \sim } 1 0   \mathrm { ~ e ^ { - } }$ **noise per read. While normal (incoherent) astronomers can afford to integrate for minutes or hours to collect photons, interferometrists must readout pixels within the atmospheric coherence time and thus are strongly limited by readnoise. As one moves further into the infrared** $(5-10 \mu  m)$ **, then thermal background fluctuations dominate the noise budget. Again, the relatively short coherence times of atmospheric turbulence directly result in a poor limiting magnitude compared to incoherent detection (i.e., photometry). The best published near-infrared performance of a two-element interferometer was reported by IOTA (Millan-Gabet et al., 1999a) using a NICMOS3 detector: J mag (1.25µm) 6.9, H mag (1.65µm) 6.9, and K’ mag (2.2µm) 6.2, where J, H are dominated by readnoise and K’ is dominated by fluctuations of the thermal background. Soon, these limiting magnitudes will be eclipsed by the adaptive-opticscorrected Keck and VLT Interferometers which should be able to observe fainter than 10th magnitude.**

**There is not much experience yet with mid-infrared observations using direct detection. The ISI heterodyne interferometer has observed stars as faint as ∼360 Jy (LkHα,101 Tuthill et al., 2002), corresponding to a N band mag of ∼-2.2, limited largely by narrow bandwidths** $( \Delta \lambda \sim 0 . 0 0 2 \mu \mathrm { m } )$ **. The VLTI mid-IR instrument MIDI will be capable of broadband combination and is forecast to have a limiting magnitude of ∼1 Jy (N band mag ∼4) using the 8 m VLT telescopes (assuming the thermal background fluctuations can be well-calibrated for systematic errors). Shortly before this article went to press, VLTI reported first fringes with the MIDI instrument.**

**A number of new technologies are being explored to push down the limiting magnitude of optical interferometers, and some of these are described in the next section.**

## 3.5. New Technologies and Techniques

**One exciting aspect to the field of optical interferometry is the aggressive implementation of new technologies to extend the limits of the sensitivity and calibration precision. In this section, I will discuss new developments which are impacting optical interferometry.**

**3.5.1. Spatial Filtering and Single-mode Fibers The idea to use single-mode fibers in optical interferometry was originated by Froehly (1982), and work began to implement these ideas in both France (e.g., Connes et al., 1987; Reynaud et al., 1992), and in the**

<!-- page 35 of 86 -->

Optical Interferometry in Astronomy

35

![Image block](doc:b6a1ff8/tier:standard/page:35/block:3)

Figure 14. This figure shows how the FLUOR beam combiner uses spatial filtering and photometric monitoring to allow precision calibration of fringe visibilities. Figure reproduced from Coude Du Foresto et al. (1997, Figure1) with permission of ESO.

**United States (Shaklan and Roddier, 1987; Shaklan, 1989). Following initial fringe detection in 1991 using the Kitt Peak McMath telescopes (Coude du Foresto and Ridgway, 1992), the FLUOR experiment as implemented on the IOTA interferometer was a real breakthrough; the amazing improvement in calibration precision was documented in Coude Du Foresto et al. (1997) and Perrin et al. (1998). Currently, the advantages of spatial filtering are being implemented at virtually all interferometers, and here I briefly explain why it is so important.**

**Figure 14 shows a schematic of a fiber-based interferometer, as sketched by Coude Du Foresto et al. (1997). When coupling starlight into a single-mode fiber, the coupling efficiency depends on how coherent the wavefront is from an individual telescope (Shaklan and Roddier, 1988). A single mode fiber thus essentially converts phase errors across the telescope pupil into amplitude fluctuations in the fiber. Once coupled into the single-mode fiber, the light can be partially split in order to monitor the amount of coupled light (“photometric” outputs), and also can be interfered with light from another fiber using a coupler, the fiber equivalent of a beamsplitter. The transfer function of the fiber coupler is very stable and not dependent on the atmosphere; only the input coupling efficiency at each fiber is dependent on the atmosphere. Hence, the visibility** can be measured very precisely $( { < } 0 . 4 \%$ uncertainty on $\mathrm { V ^ { 2 } }$ **reported by Perrin, 2003) by measuring the fringe amplitude and calibrating with the “photometric” signals.**

**This method strongly mitigates the dominant source of calibration error in most optical interferometers, the changing atmosphere. The atmospheric turbulence must be monitored in some way when observing with an interferometer, since the coherence between two wavefronts from two telescopes strongly depends on seeing. However, this is not easy to measure with a typical interferometer in realtime, and hence one must**

<!-- page 36 of 86 -->

Optical Interferometry in Astronomy

36

**settle for interleaving “science” targets with “calibrator” sources to calibrate seeing drifts during the night. With fibers, the changing seeing conditions directly cause variations in the fiber coupling efficiencies which are monitored in realtime and corrected for. Figure 15 shows near-infrared visibility data on the calibrator star α Boo using both “conventional” interferometry and the FLUOR fiber optics beam combiner. The improvement to calibration is indeed dramatic and has had far-reaching effects on the direction of the whole field of optical interferometry.**

**There are other ways to implement these calibration advantages than the FLUOR method shown in Figure 14. Monnier (2001) showed how the signal-to-noise can be somewhat improved by using an asymmetric coupler instead of separate photometric signals. Also, Keen et al. (2001) compared single-mode fibers with spatial filtering by small pinholes in order to determine which method is superior under different conditions.**

![Chart block](doc:b6a1ff8/tier:standard/page:36/block:5)

![Chart block](doc:b6a1ff8/tier:standard/page:36/block:6)

Figure 15. (left panel) a. This figure shows visibility data for α Boo by the CERGA interferometer (diamonds) and the IRMA interferometer (squares), and originally appeared in the Publications of the Astronomical Society of the Pacific (Copyright 1993, Astronomical Society of the Pacific; Dyck et al., 1993, reproduced with permission of the Editors). b. The incredible gain in calibration using spatial filtering and photometric monitoring is evident in this figure reproduced from Perrin et al. (1998, Figure 2a) with permission from ESO.

**I should emphasize that there are many problems and limitations associated with using single-mode fibers, most notably low coupling efficiencies, high dispersion and poor polarization stability. Such problems have kept fiber optics from playing an important role for beam transport (Simohamed and Reynaud, 1997), and currently fibers are used only for beam combining and spatial filtering at specific wavelengths. For instance, silica-based (telecom) fibers can generally only be used at J (1.25µm) and H (1.65µm) bands; the FLUOR experiment utilized Fluoride glass fibers which can transmit at K band (2.2µm) and beyond. Advances in the field of photonic crystals and photonic bandgap materials could lead to new fibers with low dispersion and high transmission for new interferometry applications, and should be aggressively pursued.**

<!-- page 37 of 86 -->

Optical Interferometry in Astronomy

37

**3.5.2. Integrated Optics While combining two telescopes together is straightforward using fiber optics, it becomes very difficult for multiple telescopes. This is because the light has be split many times, combined together many times, and the fiber lengths must be precisely matched and maintained to correct for differential chromatic dispersion and birefringence effects.**

**An elegant solution to this problem, while maintaining the advantages of spatial filtering, is the use of integrated optics, the photonics analog to integrated circuits. P. Kern and an active group centered at Grenoble Observatory have pioneered this technique (e.g., Kern et al., 1997; Malbet et al., 1999; Berger et al., 1999) and it is finding successful application at a number of observatories, including IOTA (Berger et al., 2001) and VLTI. In these combiners, many fibers can be mated to a small planar element with miniature waveguides etched in place to manipulate the light (split, combine, etc). Dozens of beamsplitting and combinations can all be fit into a few square centimeters** and never needs re-aligned!

**While integrated optics can solve the problem of how to combine many beams using guided optics, it has similar difficulties as fibers of poor transmission, limited wavelength coverage, dispersion, and birefringence. While the commercial applications for integrated optics in telecommunications has driven much of the innovation in this field, the astronomy community must actively engage with the photonics engineers to design custom components which can overcome the remaining problems for nextgeneration “astronomical-grade” devices.**

**3.5.3. Adaptive Optics One critical advance to improve the sensitivity of infrared interferometers is the application of adaptive optics on large aperture telescopes. Generally, visible light photons are used to measure the wavefront distortions in realtime, allowing them to be corrected using a deformable mirror. Once the aperture is “phasedup,” the entire (much larger!) coherent volume can be used for the infrared fringe detection. This method has already been applied on the Keck Interferometer, where AO systems on the individual 10 m telescopes now allow observations approaching K mag 10 (and should allow even fainter objects eventually). The major drawback for this is that there must be a “bright” visible guide star in the isoplanatic patch for the AO system to use for wavefront sensing, not possible for obscured sources such as Young Stellar Objects and dusty evolved stars where the visible source is often too faint (a few AO systems do have infrared wavefront sensors to mitigate this problem, e.g. Brandner et al., 2002). The maturation of laser guide star adaptive optics will allow this gain in coherent volume for all infrared observing eventually. Of course, building future interferometers at the most excellent sites (even in space) will be an increasing priority.**

**3.5.4. Phase Referencing Phase Referencing is a kind of adaptive optics for interferometry, where a bright reference star is used to measure and correct for atmospheric time delays. This technique is used in radio interferometry to allow long coherent integrations on targets, via a fast switching scheme.**

<!-- page 38 of 86 -->

Optical Interferometry in Astronomy

38

**Unfortunately, the short atmospheric coherence times make a switching scheme difficult to implement. A different approach pursued by the Palomar Testbed Interferometer is to use a “dual star module”, where light from two stars are selected and observed simultaneously using different delay lines. This allows both relative astrometry and phase referencing to be achieved.**

**Very few results have been published on this technique so far, although the technique is being implemented at the Keck Interferometer and is planned for VLTI. First results from PTI have been published (Lane and Colavita, 1999; Lane et al., 2000a; Lane and Colavita, 2003), reporting extending the atmospheric coherence time to 250 ms and visibility calibration precision of 3-7%. Development of this technique will allow very faint limiting magnitudes, for a small set of sources located within an isoplanatic patch** $\left( {\sim} 30 \right)$ **of a bright star.**

**Another method called “differential phase” is being applied soon, where fringes at one wavelength are basically used to stabilize fringes at all the others. When a source shows significant wavelength-dependent structure, this technique should prove very powerful. This is discussed further in the context of extrasolar planet detection in §5.1.3.**

**3.5.5. Spectroscopy Very little has been done in the area of interferometric observations on spectral lines. The best science results will be reviewed in the next section, however here I wanted to mention recent developments. Bedding et al. (1994) discussed methods for combining aperture masking with spectroscopy, and the design of the MAPPIT instrument offers lessons for long-baseline interferometrists. G. Weigelt and collaborators have developed a spectrometer for use on two element interferometers, which allows near-infrared molecular bandheads of CO and** $\mathrm { H _ { 2 } O }$ **to be spatially probed (e.g. Weigelt et al., 2000; Hofmann, 2002). More interestingly, the AMBER instrument for the VLTI will boast three different spectral resolutions (up to R ∼10000 across the infrared), making observations of individual lines possible (e.g., Petrov et al., 2000). While the GI2T has had high spectral resolution for years, a number of other visiblelight interferometers, including NPOI and COAST, have modified their combiners to allow Hα interferometry, following the fascinating results of the GI2T in the 1990s (e.g., Vakili et al., 1998); see §4.2.1 for more discussion on this.**

**3.5.6. New Detectors Single-pixel visible light detectors are nearly ideal in their performance (e.g., APDs). However, new detectors exist with many of the same advantages of APDs, but which can also measure the energy of each detected photon (Superconducting Tunnel Junction detectors, Peacock et al., 1997). Although limited to maximum count rates of ∼10 KHz, current STJ devices offer high quantum efficiency, timing accuracy, and about ∼12% bandwidth energy resolution in the visible and have been used on the sky (Perryman et al., 2001). One obstacle for this technology is that most astronomers want large-format focal plane arrays with millions of pixels, and present arrays are ∼6×6 pixels. These STJ arrays are small, but large enough to be be**

<!-- page 39 of 86 -->

Optical Interferometry in Astronomy

39

**quite interesting for optical interferometry; this work should be strongly encouraged.**

**For some type of interferometer combiners (e.g., high-resolution spectrometers or 6-telescope imaging), many pixels are needed; unfortunately, APDs and STJs are not economical for this and CCDs typically still have larger readnoise for fast frame rates. In this regard, a new development by Marconi may be interesting (Mackay et al., 2001). They have produced a kind of “photon-counting” CCD, which implements on-chip avalanche gain stages in order to amplify single electrons into large signals. Tubbs et al. (2002) report the first use of these new detectors in astronomy, and the results are promising for interferometry (the COAST interferometer is currently adapting such a device for their work).**

**Because of the relatively high readnoise for near-infrared detectors, improvements in the next decade could easily extend the sensitivity of interferometers by a factor of 10. The AOMUX detector program by Rockwell has just begun, and has the goal of a few electron readnoise at high frame rates. Keeping pace with these developments will remain a high priority for optical interferometry.**

**There are also some developments to create photon-counting near-infrared detectors, equivalent to Avalanche Photo-Diodes. Sometimes called SSPMs (Solid State Photo-Multipliers), Eikenberry et al. (1996) described one experiment. Currently, the main drawback with these devices is the low quantum efficiency, a few percent. Alternatively, Superconducting Tunnel Junctions can also be used in the near-infrared for photon-counting.**

**3.5.7. Nulling Another interferometric technique gaining application is nulling. By introducing an achromatic 180**◦ **phase shift in one beam, the white-light fringe can be turned into a white-light null (Bracewell, 1978). This has obvious applications for extra-solar planet searches and zodiacal dust disk characterizations, since removing the bright central star is essential for detecting faint circumstellar material and companions. The only astronomical results from nulling have come from aperture masking style experiments (e.g., Hinz et al., 1998; Hinz, 2001; Hinz et al., 2001b), and have encouraged aggressive follow-up experiments. In particular, the Keck Interferometer is pursuing a mid-infrared nulling project (Serabyn and Colavita, 2001) and nulling is a central operational mode for the Large Binocular Telescope Interferometer (Hinz et al., 2001a).**

## 3.6. Current and Future Facilities

**In Tables 2 & 3, I have summarized all the current and planned facilities (groundbased). Further discussion of the current field, including documentation of the rising trend of publications, can be found in Ridgway (2000) where I have found some of the information for these summary tables. We note that links to all these interferometers can be found on the well-established “Optical Long-Baseline Interferometry News” website, maintained by Peter Lawson at NASA-JPL (**[**http://olbin.jpl.nasa.gov**](http://olbin.jpl.nasa.gov)**).**

**Each of the currently operating interferometers have unique capabilities and**

<!-- page 40 of 86 -->

Optical Interferometry in Astronomy

40

**achievements of note. The GI2T and ISI Interferometers are the longest operating interferometers, both beginning work in the 1980s; notably, the GI2T has uniquely pursued observing of Hα emission (and remains the only direct detection interferometer with general high spectral resolution capabilities) and the ISI is the only (published) mid-infrared interferometer. The COAST and NPOI interferometers are currently best optimized for imaging, having incorporated 5 and 6 telescopes respectively into their arrays. IOTA is noted for groundbreaking fiber optics and detector development in the infrared. NPOI and PTI have incorporated elaborate internal metrology to enable ambitious astrometry goals. SUSI has the capability of 640 m baselines and is one of the only interferometers in the southern hemisphere. Strong progress from the MIRA-I array marks Japan’s recent efforts in long baseline interferometry.**

**Recent developments include new infrared and visible combiners for the IOTA (first integrated optics success with stars Berger et al., 2001) and GI2T interferometers, third telescope upgrade projects for the ISI and IOTA interferometers, 6-telescope operation by NPOI and 5-telescopes for COAST, and first fringes from the Keck, VLTI, MIRA, and CHARA interferometers. SUSI has also commissioned a new “red” table, allowing packet-scanning interferometry using APDs. The FLUOR combiner, so successfully used on the IOTA interferometer, has been moved to CHARA, and we can expect excellent results soon to take advantage of the greater resolution and sensitivity.**

**Indeed, it has been a busy decade for construction and implementation. It is apparent in Table 3 that the current and next generation interferometers boast significantly larger and more numerous telescope apertures and baselines, and promise to deliver significant new results. In the area of imaging, CHARA and NPOI will have 6 telescopes spread over hundreds of meters, to allow imaging capabilities at milliarcsecond resolution. The VLTI and Keck Interferometers will have >**∼**100 m baselines with adaptive optics corrected primary mirrors, allowing many new kinds of science to be pursued. In particular, we can expect the first extragalactic sources, bright AGN and quasars, to be measured at near-infrared wavelengths very soon (probably before this article goes to press). These new developments are further discussed in §5.**

**Lastly, I will mention recent progress on the next generation of interferometers. The OHANA project has carried out initial experiments to couple light from Mauna Kea telescopes into single-mode fibers, the first step in a plan to link the giant telescopes of the Hawaii into a powerful optical interferometer. Major construction for the Large Binocular Telescope (and Interferometer) has been progressing for many years and is in an advanced stage now. Importantly, the final design plans for the Magdalena Ridge Observatory are shaping up and site work for the ∼10 telescope optical array is expected to begin soon. You can find more information on these ambitious projects in the interferometer summary tables as well.**

**The next section will review the currently exciting results from optical interferometry, and give some indication of how the new facilities will impact many areas of astrophysics.**

<!-- page 41 of 86 -->

Tab le 2 . C urrent and Fut ure O pt ical Interferometers : B asics ( ∗ indicates “in planning” )

| Acronym | Full Name | Lead Institution(s) | Location | Start |
| --- | --- | --- | --- | --- |
| CHARA | Center for High Angular Resolution Astronomy | Georgia State University | Mt. Wilson, CA, USA | 2000 |
| COAST | Cambridge Optical Aperture Synthesis Telescope | Cambridge University | Cambridge, England | 1992 |
| GIZT | Grand Interferometre à 2 Telescopes | Observatoire Cote D'Azur | Plateau de Calern, France | 1985 |
| IOTA | Infrared-Optical Telescope Array | Smithsonian Astrophysical Observatory, Univ. of Massachusetts (Amherst) | Mt. Hopkins, AZ, USA | 1993 |
| ISI | Infrared Spatial Interferometer | Univ. of California at Berkeley | Mt. Wilson, CA, USA | 1988 |
| Keck-I | Keck Interferometer (Keck-I to Keck-II) | NASA-JPL | Mauna Kea, HI, USA | 2001 |
| MIRA-I | Mitake Infrared Array | National Astronomical Observatory, Japan | Mitaka Campus, Tokyo, Japan | 1998 |
| NPOI | Navy Prototype Optical Interferometer | Naval Research Laboratory, U.S. Naval Observatory | Flagstaff, AZ, USA | 1994 |
| PTI | Palomar Testbed Interferometer | NASA-JPL | Mt. Palomar, CA, USA | 1996 |
| SUSI | Sydney University Stellar Interferometer | Sydney University | Narrabri, Australia | 1992 |
| VLTI-UT | VLT Interferometer (Unit Telescopes) | European Southern Observatory | Paranal, Chile | 2001 |
| Keck* | Keck Auxiliary Telescope Array | NASA-JPL | Mauna Kea, HI, USA | ~2004? |
| LBTI* | Large Binocular Telescope Interferometer | LBT Consortium | Mt. Graham, AZ, USA | ~2006 |
| MRO* | Magdalena Ridge Observatory | Consortium of New Mexico Institutions, Cambridge University | Magdalena Ridge, NM, USA | ~2007 |
| OHANA* | Optical Hawaiian Array for Nanoradian Astronomy | Consortium (mostly French Institutions, Mauna Kea Observatories, others) | Mauna Kea, HI, USA | ~2006 |
| VLTI-AT* | VLT Interferometer (Auxiliary Telescopes) | European Southern Observatory | Paranal, Chile | ~2004 |

Optical Interferometry in Astronomy

41

<!-- page 42 of 86 -->

Optical Interferometry in Astronomy

42

Table 3. Current and Future Optical Interferometers: Capabilities (∗ indicates planned capabilities)

<table><tr><td rowspan="2">Acronym</td><td colspan="2">Telescope</td><td rowspan="2">Maximum Baseline (m)</td><td rowspan="2">Wavelength Coverage</td></tr><tr><td>Number</td><td>Size (m)</td></tr><tr><td>CHARA</td><td>6*</td><td>1.0</td><td>330</td><td>visible*, near-IR</td></tr><tr><td>COAST</td><td>5</td><td>0.40</td><td>47 (100*)</td><td>visible &amp; near-IR</td></tr><tr><td>GI2T</td><td>2</td><td>1.52</td><td>65</td><td>visible, near-IR</td></tr><tr><td>IOTA</td><td>3</td><td>0.45</td><td>38</td><td>visible, near-IR, 4μm</td></tr><tr><td>ISI</td><td>3*</td><td>1.65</td><td>85 (&gt;100*)</td><td>mid-IR</td></tr><tr><td>Keck-I</td><td>2</td><td>10.0</td><td>85</td><td>near-IR, mid-IR*</td></tr><tr><td>MIRA-I</td><td>2</td><td>0.25</td><td>30</td><td>visible</td></tr><tr><td>NPOI</td><td>6</td><td>0.12</td><td>64 (&gt;250*)</td><td>visible</td></tr><tr><td>PTI</td><td>3</td><td>0.40</td><td>110</td><td>near-IR</td></tr><tr><td>SUSI</td><td>2</td><td>0.14</td><td>64 (640*)</td><td>visible</td></tr><tr><td>VLTI-UT</td><td>4</td><td>8.0</td><td>130</td><td>near-IR, mid-IR</td></tr><tr><td>Keck*</td><td>4*</td><td>1.8</td><td>140* ?</td><td>near-IR</td></tr><tr><td>LBTI*</td><td>2*</td><td>8.4</td><td>23*</td><td>near-IR, mid-IR</td></tr><tr><td>MRO*</td><td>~10</td><td>~1.5</td><td>~1000</td><td>visible, near-IR</td></tr><tr><td>OHANA*</td><td>~6</td><td>3.5-10</td><td>~1000</td><td>near-IR</td></tr><tr><td>VLTI-AT*</td><td>3*</td><td>1.8</td><td>202</td><td>near-IR, mid-IR</td></tr></table>

## 4. Summary of Major Scientific Results

**This section is divided up into two major areas: astrophysics of stars and of circumstellar environments. Optical interferometers have made substantial contributions in each, and I will outline recent progress.**

## 4.1. Stellar Astrophysics

**Optical interferometry has made the greatest impact in the area stellar astrophysics, in particular the study of nearby single stars. This is not surprising, given the limited nature of single-baseline interferometers and the limited sensitivity of first-generation instruments. In the last decades of work, an impressive diversity of investigations have been carried out and here we document the most successful work.**

**4.1.1. Stellar Diameters and Effective Temperatures One of the earliest identified applications for optical interferometry was directly measuring the effective temperature scale of stars. The effective temperature is defined such that**

$$
L = 4 \pi \sigma R ^ {2} T _ {\mathrm{eff}} ^ {4}\tag{8}
$$

**where σ is the Stephan-Boltzman constant, R is the radius of the star, and L is the total bolometric luminosity. Hence, by measuring the angular size of a star and the apparent luminosity, the effective temperature can be directly calculated. The above equation**

<!-- page 43 of 86 -->

Optical Interferometry in Astronomy

43

**is often rearranged in terms of directly observable quantities (independent of distance estimate):**

$$
T _ {\mathrm{eff}} = 2 3 4 1 (F _ {\mathrm{bol}} / \theta_ {R} ^ {2}) ^ {1 / 4}\tag{9}
$$

where $F _ { \mathrm { b o l } }$ is the total bolometric flux (in $1 0 ^ { - 8 } e r g s c m ^ { - 2 } s ^ { - 1 } )$ **and** $\theta _ { R }$ **is the angular diameter in milliarcseconds. Empirical calibration of the effective temperature as a function of spectral type is important since** $T _ { \mathrm { e f f } }$ **is considered a fundamental parameter of a star, appearing throughout stellar astrophysics most notably on the Hertzsprung-Russell diagram.**

**The survey of stellar diameters using intensity interferometry by Hanbury Brown et al. (1974a) still serves as the best resource for the effective temperature scale of hot main sequence stars. The technique of lunar occultations has traditionally been the other main method for high-resolution measurements of stellar sizes, as represented by the classic paper by Ridgway et al. (1980).**

**There are now more than a hundred interferometer diameter measurements, and this progress is marked in Figure 16. Here we see one of the first major results from Michelson interferometry from the I2T/CERGA interferometer (di Benedetto and Rabbia, 1987), the effective temperature scale of giants. Next to it, is a more recent version of the same diagram showing the increase in the number of diameter measurements, compiled by van Belle et al. (1999). The effective temperature scale for late-type stars is now well-established, and available diameter data has been generated by many interferometers (e.g., Mozurkewich et al., 1991; Dyck et al., 1996; Perrin et al., 1998; Nordgren et al., 1999). A recent cross-comparison found the datasets from different groups to be statistically consistent (Nordgren et al., 2001); but for the latest spectral types, the visible photosphere is affected by TiO absorption and it is believed that infrared sizes are more representative of the “true” photospheric extent (e.g., Dyck and Nordgren, 2002).**

**While giant stars have made easy targets for interferometers due to their large angular sizes and high luminosities, the census of lower-mass dwarf stars and hotter main sequence stars remain incomplete. The PTI interferometer recently made first contributions to the study of K- and M-dwarfs by measuring the diameters of 5 such stars (Lane et al., 2001), although greater precision (<**∼**1% diameter errors) is needed to stringently test theoretical models. The first scientific result from the VLTI interferometer recently contributed to this precious, limited dataset of M-dwarf diameters (Segransan et al., 2003), also finding sizes consistent with theory but lacking precision. To date, there are no published diameters with baselines as long as the Narrabri Intensity Interferometer (188m), although the CHARA interferometer did record fringes on a 330m baseline in 2001. The new long baseline capabilities of CHARA, NPOI, and SUSI should allow progress in some of these areas in the near future.**

**4.1.2. Limb-Darkening, Atmospheric Structure Measuring a so-called “uniform-disk (UD)” diameter only requires a single visibility data point for an isolated star, by fitting**

<!-- page 44 of 86 -->

Optical Interferometry in Astronomy

44

![Chart block](doc:b6a1ff8/tier:standard/page:44/block:3)

![Chart block](doc:b6a1ff8/tier:standard/page:44/block:4)

Figure 16. (left panel) a. This figure shows one of the first major Michelson interferometer results (by the CERGA/I2T interferometer), the effective temperature relations for giants by di Benedetto and Rabbia (1987, see their Figure 1), reproduced here with permission of ESO. (right panel) b. Here is reproduced Figure 2a from van Belle et al. (1999), with permission from the AAS, showing the huge increase in the number of diameter measurements that now can be used for empirically determining the effective temperature scale of giants. The X-axis label $``V-K''$ refers to the brightness of the star at V-band $\left( \lambda_{0} =  0.55 \mu  m  \right)$ compared to K-band $\left( \lambda_{0}  =  2.2 \mu  m  \right)$ redder stars have larger V-K color.

**a one-parameter model. However, stellar photospheres are known to limb-darkened due to optical depth effects, and thus UD diameters must be corrected to yield the correct physical photospheric size. The first attempts to directly measure this was done using the intensity interferometer on the A1V star Sirius A (Hanbury Brown et al., 1974b), however the results suffered from large errors and were not very definitive. Other attempts have been made based on looking for wavelength-dependent angular diameters, a sign of limb-darkening (e.g., Ridgway et al., 1982; Mozurkewich et al., 1991).**

**The visibility curve of a uniform-disk star is related to the first Bessel function, and contains an ever decreasing series of lobes, separated by nulls, as one observes with increasing angular resolution (see Figure 15 for a plot of the first two lobes of this curve). The main difficulty for limb-darkening studies is that the first “lobe” of the visibility pattern for a star is insensitive to limb-darkening effects (mathematically, it probes only the 2nd moment of the brightness distribution; see Lachaume, 2003); measurements beyond for the first null must be made to unambiguously detect limb-darkening effects (see Figure 17 for representative visibility curves). However, the fringe contrasts at high spatial resolution are necessarily low, and thus it has been difficult to measure these effects. Precise measurements of Arcturus (α Boo, K1III) were made by Quirrenbach et al. (1996) using the Mark III employing a novel phase-referencing method to increase the signal-to-noise near the visibility null; they found reasonable agreement with model expectations.**

**The NPOI interferometer succeeded the Mark III, and expanded the wavelength phase-referencing techniques (using strong fringes at one wavelength to allow coherent**

<!-- page 45 of 86 -->

Optical Interferometry in Astronomy

45

**integrations on weak fringes). Hajian et al. (1998) used these advantages first for limb darkening studies, followed more recently by Wittkowski et al. (2001). The latter paper presented data with spatial frequencies sampled well before and after the null and these exemplary results are reprinted here in Figure 17. Again, the atmospheric models were found to be in reasonable agreement with the interferometry results. A new generation of precision tests of stellar atmospheres are now being pursued using detailed radiative transfer modeling coupled with thoughtful interferometer measurements at specific wavelengths and with specific baseline coverage (e.g., Aufdenberg et al., 2002).**

![Chart block](doc:b6a1ff8/tier:standard/page:45/block:4)

Figure 17. This figure shows recent results from the NPOI interferometer, which has been optimized to investigate effects of limb-darkening on stellar profiles. A portion of Figure 3 from Wittkowski et al. (2001) has been reproduced here, with permission from EDP Sciences, showing that models accurately predict the amount of limb-darkening observed in this K5 star.

**Until recently, most interferometers had only 2-elements and had difficulty to directly measure the two-dimensional shape of stellar photospheres. In most cases, one assumes the star is circularly symmetric in order to interpret visibility data taken at differently projected baselines. The Palomar Testbed Interferometer made the serendipitous, although not unexpected in retrospect (Hanbury Brown et al., 1967), discovery that that the rapidly rotating star Altair is not circular. Figure 18 shows the oblate spheroid model of this source developed by van Belle et al. (2001). The oblateness is caused by centrifugal “bulging” along the equator and these measurements offer an independent measure of the projected stellar rotational velocity v sin i. While red giants and supergiants had been known to deviate from circular symmetric (see §4.1.5), this is the first main sequence star found to be non-circular; future “imaging” work should allow new probes of other rotational effects, such as gravity-darkening.**

**In addition to standard limb-darkening profiles, one has to be concerned with the effects of molecular lines formed in the photospheres of cool giants (mostly M spectral types), especially for the Mira variables. It has been known for quite some time (first from speckle interferometry) that evolved stars appear much larger when observed in narrow spectral channels coincident with deep TiO bands in the visible regime (e.g.,**

<!-- page 46 of 86 -->

Optical Interferometry in Astronomy

46

![Chart block](doc:b6a1ff8/tier:standard/page:46/block:3)

Figure 18. Oblate Spheroid Model for the photosphere of Altair, based on PTI data (from Figure 6 of van Belle et al., 2001), reproduced here with permission of the AAS.

**Labeyrie et al., 1977). The origin of this extension is obvious: at the observing wavelength, the optical depth unity surface is at greater distance from the star, and hence the apparent size is noticeably larger. Quirrenbach et al. (1993b) made the first systematic study of this effect for late-type stars covering a range of spectral types,and these results are shown here in Figure 19a.**

**A more recent, and unexpected, discovery in this vein is that molecules with transitions in the near-infrared are causing large increases in the apparent sizes also. The effect of (most likely) unappreciated** $\mathrm { H _ { 2 } O }$ **lines in the coolest M-stars was uncovered by many groups using different approaches at about the same time. Perrin et al. (1999) detected hints of these effects, finding puzzling deviations from a uniform disk for the O-rich Mira R Leo. Tuthill et al. (2000a) found that R Aqr, another O-rich Mira, was dramatically larger at 3.1 µm than at shorter wavelengths (an effect seen also in other O-rich Miras, Tuthill et al., 1999c). First results with an L’ band (3.75µm) combiner at IOTA also found a large diameter increase compared to shorter wavelengths (Mennesson et al., 1999).**

**A possible explanation for this effect was separately noted by researchers analyzing data from the Infrared Space Observatory (ISO), finding new water features in this part of the spectrum (e.g., Tsuji et al., 1997; Matsuura et al., 2002). Another recent analysis (Jacob and Scholz, 2002) coupled a dynamical model to a simple radiative transfer model and found complex (time-variable) visibility curves due to molecular effects in the near-IR. Mennesson et al. (2002) have collected data from multiple infrared bands (e.g., Chagnon et al., 2002), arguing the presence of “extended gaseous layers” around O-rich miras; see the dramatic difference in near-infrared sizes observed for R Aqr in the right panel of Figure 19.**

**Thompson et al. (2002) have expanded these studies by measuring the sizes of O-rich and C-rich miras using narrow spectral channels** $\left( \Delta \lambda \sim 0.1 \mu  m  \right)$ **from** $2.0-2.4\mu m$ **. While they report O-rich miras are larger near the edges of the band, a different behavior is observed for C-rich stars; this tentatively confirms the role of O-bearing molecules (e.g.,**

<!-- page 47 of 86 -->

Optical Interferometry in Astronomy

47

$\mathrm { H _ { 2 } O ) }$ **. Moving further into the infrared, Weiner et al. (2000) (following earlier work by Bester et al., 1996) actually find stars to be larger in true 11.15µm continuum channels** (using the ISI interferometer) than at 2.2µm, a somewhat confusing result since the near **IR wavelengths are expected to be significantly contaminated by molecular effects. I am aware of even more results which have not made it to press yet (e.g., adaptive optics at the Subaru Telescope, narrow-band IOTA interferometry), and anticipate rapid progress in this area over the coming years.**

![Chart block](doc:b6a1ff8/tier:standard/page:47/block:4)

![Chart block](doc:b6a1ff8/tier:standard/page:47/block:5)

Figure 19. (left panel) a. This figure shows the Mark III compendium of results measuring photospheric diameters in and out of strong TiO bands (reproduced from Figure 2 of Quirrenbach et al., 1993b, with permission of the AAS). Redder stars (later spectral types) show greater atmospheric extensions in TiO. (right panel) b. This figure shows the most recent data illustrating that Mira stars have strongly wavelength-dependent diameters (reproduced from Figure 2 of Mennesson et al., 2002, with permission of the AAS). The two curves were fit to visibility data taken at 2.2µm and at ∼4µm, and show a greater than factor of two increase in angular size between these two wavelengths.

**4.1.3. Pulsating Stellar Atmospheres As discussed earlier, the “continuum” photospheric size is important for calculating a meaningful effective temperature scale. Another important consequence of angular diameter work is specific to variable stars: the average physical size should reveal whether a star is pulsating in the fundamental or first-overtone mode. Distance estimates have been combined with interferometry data to estimate physical diameters; these studies typically found “large” sizes consistent with first-overtone pulsation in most cases (e.g., Haniff et al., 1995; van Leeuwen et al., 1997; Whitelock and Feast, 2000), although some sources were found to be fundamental pulsators. This is at odds with both non-linear pulsation models of Miras (Bessell et al., 1996) as well as the persuasive study of variables in the Large Magellanic Cloud by Wood and Sebo (1996). If visible and near-infrared diameters are indeed contaminated by molecular absorption as indicated by recent interferometric results discussed in the last section, it is possible that the true continuum diameters are small enough to be consistent with fundamental mode pulsation. The pulsation mode question of Miras has been debated and “settled” many times, and still more work is needed for a definitive**

<!-- page 48 of 86 -->

Optical Interferometry in Astronomy

48

**answer.**

**Pulsating stars, especially the Mira variables (period ∼ 1 year), are also expected to have large changes in the photospheric diameters as the luminosity varies (e.g., Bessell et al., 1989; Ya’Ari and Tuchman, 1996). However, because of the difficulty in obtaining a uniform dataset over many years, it is only recently that good pulsation curves of diameters have become available.**

**While first hints of phase-dependent diameter changes were reported based on a statistical analysis of IOTA data (van Belle et al., 1996), the first definitive detection of diameter pulsation came from the COAST group for the O-rich mira R Leo (Burns et al., 1998), where a 35% change in diameter was reported. In Figure 20a, we show more recent results for** $\chi \: \mathrm { C y g }$ **(also from COAST) with better temporal sampling of the pulsation curve (Young et al., 2000b). Most recently, Weiner et al. (2003) report the first detection of pulsation at mid-infrared wavelengths, in this case for Mira variable o Ceti.**

**The most significant recent developments are coming from the Ph.D. dissertation of Thompson at PTI. The high level of automation of the PTI has allowed systematic observations of a large number of Miras at all pulsational phases, and these data are presented in Thompson (2002). A first look at the data has been published, and one result from Thompson et al. (2002) appears in Figure 20b; the diameter of this star has been measured at many phases of the pulsation, providing an unprecedented opportunity to test non-linear pulsation models. The full analysis of the PTI dataset will shed light on pulsation characteristics as a function of spectral type (O-rich, C-rich Miras) and wavelength, and we look forward to more of this work in the near future.**

![Chart block](doc:b6a1ff8/tier:standard/page:48/block:7)

![Chart block](doc:b6a1ff8/tier:standard/page:48/block:8)

Figure 20. Pulsation curves for two different Mira Variables (at different wavelengths). (left panel) This panel shows the large amplitude pulsation of the S-Mira χ Cyg seen at 905nm by COAST, although no obvious pulsations were seen at 1290 nm (see Figure 2a in Young et al., 2000b, reproduced here with permission of Blackwell Publishing). (right panel) Here we see a well-sampled 2.2µm pulsation curve (both open and filled plot symbols) for the O-rich Mira S Lac, from a recent PTI campaign (see Figure 2 in Thompson et al., 2002, reproduced with permission of the AAS).

<!-- page 49 of 86 -->

Optical Interferometry in Astronomy

49

**4.1.4. Cepheid Pulsations Calibrate Period-Luminosity Relation Although phe nomenologically related to measurements of pulsating AGB stars, observations of Cepheids are quite distinct in their scientific goals. As has been discussed in Sasselov and Karovska (1994) and earlier (e.g., Davis, 1976), optical interferometry will play an important role in independently calibrating the Cepheid distance scale, a crucial element of the cosmic distance ladder. By measuring the changing diameter of a nearby Cepheid and the coeval radial velocity curve through a pulsation cycle, the distance can be directly inferred via the Baade-Wesselink method. A flurry of initial results have appeared from GI2T (Mourard et al., 1997), NPOI (Armstrong et al., 2001), IOTA (Kervella et al., 2001), and PTI (the first definitive detection of Cepheid pulsation; Lane et al., 2000b). However, most current published reports only weakly detect the pulsation, and defini tive results will require longer baselines and/or much higher signal-to-noise ratio fringe measurements.**

![Chart block](doc:b6a1ff8/tier:standard/page:49/block:4)

![Chart block](doc:b6a1ff8/tier:standard/page:49/block:5)

Figure 21. These data show the most recent pulsation curves for two Cepheid variables, $\eta \; \mathrm { A q l }$ and ζ Gem. The data was taken by the PTI interferometer at 1.65µm and, when combined with radial velocity data, result in the most accurate distances to these important primary distance indicators. This figure reproduced from Lane et al. (2002, see Figure 1), with permission from the AAS.

**This field is rapidly developing, both observationally and theoretically. PTI workers recently published a second Cepheid results paper (Lane et al., 2002), and these remarkable data are reprinted here in Figure 21. The derived Cepheid distances indeed agree with those measured from the Hipparcos parallax satellite, but the interferometer results are more precise. The distance uncertainty is now as (or more) affected by our uncertainty in physics of the stellar atmospheres; fortunately, Marengo et al. (2002) report timely theoretical studies of wavelength- and pulsational-phase-dependent variations in Cepheid limb-darkening and emphasize the need for careful calibration in order to interpret interferometry data accurately. With new observing campaigns underway at most interferometers, we can expect a rapid development here to really pin down the pulsational properties of Cepheids in the visible and near-infrared. In the near future, we can expect the best calibrated Cepheid distance scale to be interferometric.**

<!-- page 50 of 86 -->

Optical Interferometry in Astronomy

50

**4.1.5. Imaging Stellar Surfaces As discussed in §3.1, the Cambridge group began interferometry research by using (visible-light) aperture masking on the William Herschel Telescope (WHT) in the Canary Islands (Baldwin et al., 1986b; Haniff et al., 1987b) while developing the COAST interferometer. Interferometric imaging was performed and early results showed bright features (strong departure from circular symmetry) on the surface of Betelgeuse (Buscher et al., 1990), confirming some previous reports (e.g., Roddier and Roddier, 1983). No long-baseline (separate-element) interferometer would be able to investigate the nature of these features for years, and the Cambridge masking group has spent more than a decade since thoroughly investigating “hotspots” on red supergiants and giants.**

**Over the last decade, it was shown that asymmetries are common (although not omnipresent) around red supergiants and giants at visible wavelengths (Wilson et al., 1992; Tuthill et al., 1997, 1999a), that these hotspots vary on a timescale of months (Wilson et al., 1997), and that the asymmetries become less-pronounced (even disappearing) into the infrared (Young et al., 2000a). The first image of a stellar photosphere using the COAST interferometer showed a featureless Betelgeuse (Burns et al., 1997).**

**The hotspots were originally interpreted quite literally, as “hot” patches on the photosphere from upwellings of large convective elements (Schwarzschild, 1975). However, Young et al. (2000a) introduced a new paradigm which is illustrated in Figure 22. If the bright features were indeed caused by literal hotspots, one would not expect the features to complete disappear in the near-infrared. Here, we see illustrated a model where the photosphere is surrounded by a molecular blanket (e.g., TiO) which is optically thick in the visible, but not in the infrared (>**∼**1µm). Inhomogeneities (possibly caused by large-scale convection) allow visible light to escape out of opacity holes. The results of Dyck and Nordgren (2002) indirectly support this model, by showing that even “continuum” visible diameters appear contaminated by TiO for late M-stars.**

**4.1.6. Binary Stars & Stellar Evolution Binary stars have been an indispensable tool for astronomers for centuries. Visual and spectroscopic observations yield reliable mass estimates and form the bedrock of stellar evolution theory (e.g., Eggen, 1967). The advent of speckle interferometry and optical long-baseline interferometry has led to a remarkable increase in the data quality and volume of binaries, including many short period binaries for the first time (e.g., McAlister, 1985; Hartkopf et al., 2001). This work allows unprecedented tests of stellar evolution models on a case-by-case basis, through sub-1% precision of stellar parameters.**

**In addition to the compelling science, the simple nature of their brightness distribution have made binary stars prime targets for most optical interferometers. Because of the high spatial resolution, these binaries tend to have short periods and thus full orbital elements can be determined by tracking the orbit. Not surprisingly, the first aperture synthesis images by the COAST and NPOI interferometers were of binary systems, and these first results are reproduced here in Figure 23. With sufficient**

<!-- page 51 of 86 -->

Optical Interferometry in Astronomy

51

# Multi-Wavelength Images of Betelgeuse (Alpha Orionis)

![Image block](doc:b6a1ff8/tier:standard/page:51/block:4)

Figure 22. This figure shows a summary of the results from Young et al. (2000a), the most comprehensive investigation of the origin of surface hotspots on evolved stars. This synthesis shows nearly coeval images at different wavelengths of the surface of Betelgeuse using a combination of WHT aperture masking and the COAST interferometer. Surface structures (“hotspots”) apparent at visible wavelengths disappear when imaged in the infrared. The bottom-right panel shows the schematic model offered by these authors, where the hotspots are caused not by literally “hot” patches on the photospheric surface, but rather are caused by “opacity holes” in the molecular envelope (e.g., TiO) which allow visible light to escape in a patchy pattern. Figures appear here with permission of J. Young.

**angular resolution, interferometry yields the angular diameters of the components in addition to the binary separation vector and flux ratio.**

**While earlier papers had concentrated on individual systems, Hummel et al. (1995) presented orbits of 8 systems with separations between 3 and 10 milliarcseconds using the Mark III interferometer. For some of the systems, precise mass and luminosity determinations allowed testing of stellar evolution models.**

**In order to rigorously test stellar evolutionary models, the highest precision in parameters is needed. This requires combining data from multiple instruments and techniques in a global fit, and concomitant attention must be paid to systematic errors.**

<!-- page 52 of 86 -->

Optical Interferometry in Astronomy

52

![Image block](doc:b6a1ff8/tier:standard/page:52/block:3)

Figure 23. Baby Pictures: First true aperture synthesis images using long-baseline optical interferometry. (left panel) a. The binary star Capella reconstructed at two epochs using the COAST interferometer (see Figure 2 of Baldwin et al., 1996b, reproduced with permission of ESO). (right panel) Six epochs of Mizar A seen by the NPOI interferometer (see Figure 4 of Benson et al., 1997b, reproduced with permission of the AAS).

**Ideally, the orbital elements are fit directly to the visibility data and velocities, as implemented by Hummel et al. (1998) and Boden et al. (1999). In Figure 24, the results from a study of o Leo by Hummel et al. (2001) is presented. This study stands out because it combines interferometry data from the Mark III, NPOI, and PTI interferometers, as well as radial velocity data, resulting in mass uncertainties of only ∼0.5%. Stellar evolution isochrones can be put to a serious test for this system.**

**While long-baseline interferometers allow very close binaries to be partially resolved (closest is probably 0.002” binary TZ Tri; Koresko et al., 1998) and wide systems to be characterized with incredible precision, this is not always very important. The most interesting science lies often in measuring unusual binary systems for the first time, such as the metal-poor double-lined binary system HD 195987 (Torres et al., 2002). Attractive targets for next generation of interferometer observations include systems with short-lived components such as Wolf-Rayet stars or Young Stellar Objects, since much less is already known about the masses of these objects.**

**Lastly, the push for high dynamic range imaging of binary stars has obvious implications for detecting low-mass companions, even extrasolar planets, around nearby stars. This topic will be discussed further in §5.1.3**

<!-- page 53 of 86 -->

Optical Interferometry in Astronomy

53

![Chart block](doc:b6a1ff8/tier:standard/page:53/block:3)

![Chart block](doc:b6a1ff8/tier:standard/page:53/block:4)

Figure 24. Precision binary parameters can be derived by combining interferometry and spectroscopy, as shown here for o Leo by Hummel et al. (2001). The left panel shows the derived orbit and data from multiple interferometers and the right panel shows a matching stellar isochrone along with the effective temperatures and luminosities of the two components (see Figures 10 & 11 in Hummel et al., 2001, reproduced with permission of the AAS).

## 4.2. Circumstellar Environments

**Interferometers can also be used to probe the environments around stars, both at visible light and infrared wavelengths. As the sensitivity of facilities increase, lower surface brightness features can be measured, opening up new avenues of research. Advances in interferometric imaging are particularly relevant here, since gas and dust around stars might not be distributed uniformly and may be changing in time. While there has not been true imaging accomplished by long baseline interferometers in this area yet, we have included some of the unexpected recent results from Keck aperture masking (Tuthill et al., 2000c). While equally impressive results have also appeared using adaptive optics and speckle interferometry (in particular by the Weigelt group), we highlight the masking results because the observing methods and data reduction closely parallel that of optical interferometry and more truly reflect future capabilities; they directly motivate excitement in the potential of interferometric imaging with milli-arcsecond resolution and point in new scientific directions.**

**4.2.1. Hα Envelopes around Hot Stars While almost all the early visible interferometers focused on angular diameters and binary stars, an interesting exception was observations of the bright Hα line around Be stars. This emission was expected to be more extended, and thus more easily resolvable, than the tiny photosphere itself. The envelope of** $\gamma$ **Cas was first resolved by Thom et al. (1986) using the I2T, and Mourard et al. (1989) saw evidence for an envelope in rotation by inspecting multiple spectral channels across the line itself using the GI2T. With a good range of baselines, the Mark III was able to detect definite asymmetries in** $\gamma$ **Cas and** $\zeta$ **Tau (Quirrenbach et al., 1993a, 1994); for the latter, the maximum entropy method was used to visualize the data as a “phase-less” image and this result is shown in Figure 25a. This data**

<!-- page 54 of 86 -->

![Image block](doc:b6a1ff8/tier:standard/page:54/block:1)

Optical Interferometry in Astronomy

54

**lacked Fourier phase information, and thus can not qualify as a true aperture synthesis image; nonetheless, the maximum entropy procedure provided an innovative and useful tool for visualizing this asymmetric envelope.**

**The high spectral resolution of GI2T later also uncovered asymmetric emission in these Be star envelopes in Hα (Stee et al., 1995), and observed in other lines too (Stee et al., 1998). Figure 25b shows results from Vakili et al. (1998) (see also Berio et al., 1999) which proposed that the emission line region is very one-sided and time-variable. The asymmetry in this figure was derived from the behavior of the Fourier phases and amplitudes across the line profile; this amounts to a kind of phase-referencing where the continuum emission surrounding the Hα emission is used as a reference signal allowing the Fourier phases to be recovered. The origin of this “one-armed oscillation” could result from radiative effects, the presence of a companion, or dynamical behavior in a non-spherical potential; these interesting results should be confirmed and explored by the current generation of imaging interferometers.**

![Chart block](doc:b6a1ff8/tier:standard/page:54/block:6)

![Chart block](doc:b6a1ff8/tier:standard/page:54/block:7)

Figure 25. Spectral line observations in Hα around Be stars have found extended, asymmetric envelopes; the full potential of these kind of investigations remain untapped. (left panel) a. Here we reproduce the “image” of the Hα envelope of ζ Tau from Mark III data (Figure 3 from Quirrenbach et al., 1994). (right panel) b. These schematic illustrations of the same envelope at two later dates were based on data from the GI2T interferometer (see Figure 4 from Vakili et al., 1998). Both figures are reproduced with permission of ESO.

**4.2.2. Accretion Disks and Young Stellar Objects There has been surprising and rapid progress in studies of how dense accretion disks evolve around pre-main sequence stars. Just five years ago, simple accretion scenarios incorporating passively-heated flared disks (e.g., Hillenbrand et al., 1992; Hartmann et al., 1993; Chiang and Goldreich, 1997) were widely accepted, adequate to explain the spectral energy distributions (SEDs) of most (low-mass) T Tauri stars and the higher-mass Herbig Ae/Be systems. However, recent observations with higher spatial resolution suggest a richer set of phenomena,**

<!-- page 55 of 86 -->

Optical Interferometry in Astronomy

55

**and has produced much excitement. Direct observational links are now even being made connecting the fields of star formation and planet formation, focusing on how accretion disks evolve into protoplanetary disks and finally to debris disks and planets.**

![Chart block](doc:b6a1ff8/tier:standard/page:55/block:4)

![Chart block](doc:b6a1ff8/tier:standard/page:55/block:5)

![Chart block](doc:b6a1ff8/tier:standard/page:55/block:6)

Figure 26. (left panel) This figure shows the first Herbig Ae/Be star visibility curve ever measured (see Figure 1 by Millan-Gabet et al., 1999b). The IOTA data of AB Aur at 1.6µm (H-band) and 2.2µm (K’-band) indicated a much larger dust shell or disk than expected from accretion disk models (dash-dotted curves). (right panel) The first classical T Tauri stars were observed by the PTI interferometer and also showed larger than expected infrared sizes. Here is the original data for T Tau itself, an important source but whose analysis is complicated by uncertain calibration due to the presence of a nearby companion in the interferometer field-of-view (see Figure 1a by Akeson et al., 2000a). Both figures are reproduced with permission of the AAS.

**Infrared interferometry is playing an important role in elucidating the earliest stages of planetary formation by probing the density and temperature structure of the disks presumably before planets form. Malbet et al. (1998) reported the first resolved Young Stellar Object (YSO), using near-infrared data from the PTI interferometer; the source was FU Ori, a rare type of T Tauri whose emission is dominated by accretion luminosity, and the disk size was found to be roughly consistent with expectations.**

**The first “normal” YSO to be resolved with an optical interferometer was the Herbig Ae/Be star AB Aur, and Millan-Gabet et al. (1999b) found the near-IR emission to be much larger than expected using the IOTA interferometer. These young massive stars have high luminosities, and thus were the brightest/easiest type of young star to study initially. These workers published a survey of 15 total Herbig Ae/Be stars which strongly reinforced the initial finding of large near-IR sizes (Millan-Gabet, 1999; Millan-Gabet et al., 2001). Also, they found no evidence for disk structures – intriguingly all the initial data were consistent with spherical distributions of dust. The much-awaited measurements of classical T Tauri stars would come soon thereafter from the Palomar Testbed Interferometer (Akeson et al., 2000a, 2002). The few T Tauris measured also showed near-IR emission a few times larger than expected from accretion disk models. Figure 26 shows the visibility data from these important papers for AB Aur and T Tau.**

**While infrared imaging of YSOs has only recently become possible with new 3+ telescope arrays (and nothing published yet), aperture masking on the Keck telescope**

<!-- page 56 of 86 -->

Optical Interferometry in Astronomy

56

**was able to resolve two of the brightest examples. Tuthill et al. (2001, 2002) imaged the bright source LkHα 101 and found a bright ring of emission, interpreting it as the hot dust at the inner edge of an accretion disk. While the size was larger than expected for a geometrically-thin, optically-thick disk model (e.g., Hillenbrand et al., 1992), the position of the inner edge was consistent with dust evaporating at temperatures above ∼1500 K when illuminated by direct stellar radiation (the standard paradigm for dust shells around evolved stars; see Rowan-Robinson and Harris, 1982; Dyck et al., 1984). Further this relation could explain the “large” sizes seen by IOTA and PTI. Figure 27a shows images of LkHα 101 and also of emission-line star MWC 349 by the Keck aperture maskers. We note that a subsequent LkHα 101 paper (Tuthill et al., 2002) included the first mid-IR measurements of a YSO disk size (using the ISI interferometer), and also reported unexpected changes in the LkHα 101 disk emission.**

![Chart block](doc:b6a1ff8/tier:standard/page:56/block:4)

![Chart block](doc:b6a1ff8/tier:standard/page:56/block:5)

Figure 27. (left panel) a. Aperture masking interferometry was used at the Keck telescope to create these 2.2µm images of disks around YSOs. The left panel shows the LkHα 101 dust disk with evidence of a central hole (Tuthill et al., 2001), while the right panel reveals the MWC 349A disk viewed nearly edge-on (Danchi et al., 2001). (right panel) b. Compendium of measured sizes of Herbig Ae/Be and T Tauri systems with comparison to theoretical dust sublimation radii (from Figure 1 of Monnier and Millan-Gabet, 2002, reproduced with permission of the AAS). Observed sizes are typically many times larger than expected from “classical” accretion disk models (dotted line). The number of YSO measurements will rapidly grow with the current size surveys at the Keck and VLT Interferometers.

**The first results of nulling interferometry observations of Herbig Ae/Be stars (see §3.5.7) have been recently published. By masking a single large aperture, Hinz et al. (2001b) found the spatial extent of three sources to be unresolved using a ∼4 m nulling baseline, an unexpected result. Interestingly, the same simple disk models which underpredicted the near-infrared sizes were shown to over-predict the mid-IR sizes. Clearly, more data is needed to determine what models are appropriate for disks around young stellar objects – none of the “standard” ones seem to work at near- or mid-infrared wavelengths when it comes to spatial observations (the spectral energy distributions can be fit by a number of models).**

<!-- page 57 of 86 -->

Optical Interferometry in Astronomy

57

**Recently, Monnier and Millan-Gabet (2002) summarized the current literature of near-infrared disk sizes, and one of the figures appear here as Figure 27b. As indicated above, the most interesting fact is that nearly all the disks measured are many times larger than expected from “standard” disk models (geometrically-thin and optically thick disks), indicating a large dust-free central cavity. A few theorists are incorporating these results into their models, and I recommend the papers of Natta et al. (2001) and Dullemond et al. (2001) for further discussion. Understanding how planetary systems eventually form out of these disks will not be possible until we are more certain of the initial physical conditions of material within a few AU of young stars. There is a survey already underway at the Keck Interferometer (and planned soon for the VLTI) to include many more T Tauri and Herbig Ae/Be stars, and we can look forward to more developments in this exciting area.**

**4.2.3. Dust Shells & Molecules in Evolved Stars Long before the dusty disks around young stars could be observed, interferometry techniques were used to characterize dust shells around evolved stars. I briefly mentioned the early history of this work in the mid-infrared in §3.1, and the capabilities of 3 m telescopes were exploited in a series of near-infrared speckle measurements in the 1980s (see especially Dyck et al., 1984).**

![Chart block](doc:b6a1ff8/tier:standard/page:57/block:5)

![Chart block](doc:b6a1ff8/tier:standard/page:57/block:6)

Figure 28. (left panel) This figure shows temporal changes in the IK Tau visibility curve probing the dust shell at 11.15µm as shown by Hale et al. (1997, Figure 3). (right panel) These changes can be visualized through a maximum entropy reconstruction of the dust shell, reproduced here from Figure 4 of Hale et al. (1997). Both figures are reproduced with permission of the AAS.

**The most important paper on dust shells was published by Danchi et al. (1994), reporting mid-infrared observations of 13 evolved stars by the ISI interferometer. The data were fitted by radiative transfer models of dust shells, which strongly indicated that mass-loss appeared continuous around some stars and episodic around others. At the time, mass-loss on the AGB was still considered to be spherically-symmetric and continuous, and these results began to dislodge this simplified picture.**

**Subsequent papers concentrated on detailed modeling of individual sources, as the evidence for non-uniform outflows (Monnier et al., 1997) and deviations from sphericalsymmetry (Lopez et al., 1997) accumulated. Hale et al. (1997) found time-variable**

<!-- page 58 of 86 -->

Optical Interferometry in Astronomy

58

**features in the visibility curve of the O-rich mira IK Tau, and attributed it to moving dust shells expanding in the outflow. Figure 28 shows the visibility data and a maximum entropy reconstruction to help visualize the change in the dust shell morphology; as for the “image” of ζ Tau by Quirrenbach et al. (1994), these radial profiles were reconstructed from phase-less data and so do not necessarily represent a true “image.” The changes were consistent with the expected outflow speeds (derived from maser observations), and allowed an independent distance estimate to this source.**

**The idea that mass-loss is not uniform in time nor necessarily spherically symmetric found confirmation using other related techniques. At the same time, near-infrared speckle and aperture masking were being pursued on the new 8-m class telescopes. Imaging of the carbon star IRC +10216 revealed an incredibly inhomogeneous and asymmetric dust shell (Haniff and Buscher, 1998; Weigelt et al., 1998; Tuthill et al., 2000c), and enough data has been collected to see the dust structures evolve with time; I reproduce a figure from Tuthill et al. (2000c) which exploits the diffraction-limit of the world’s largest telescope to image the details of this nebula (see Figure 29). For readers interested in near-infrared imaging of dust shells using speckle interferometry and aperture masking, I refer the reader to many recent papers by the Weigelt group and the Keck masking team, which will not be reviewed here.**

**Another recent area of progress is the successful combination of high spectral resolution with high spatial resolution in the mid-infrared. A filterbank spectrometer was constructed and installed on the ISI interferometer allowing interferometry data to be collected on mid-infrared absorption lines (Monnier et al., 2000c,a,b). Polyatomic molecules such as ammonia and silane form in dense outflows of evolved stars, but at orders of magnitude greater abundance than expected (e.g., Keady and Ridgway, 1993). This mystery was partially solved when the ISI found that the molecules form much further out in the flow than expected, possibly related (for the case of Silane) to the depletion of SiS onto grains (Bieging and Tafalla, 1993). This work highlights the potential for studying cosmochemistry using interferometry.**

**4.2.4. Colliding Winds While no Wolf-Rayet dust shells have yet to be observed using a long-baseline interferometer, the discovery of pinwheel nebulae around these stars by Tuthill et al. (1999b) and Monnier et al. (1999) using Keck aperture masking represents a new direction for the current generation of infrared imaging interferometers. An example of the spiral pattern seen in the visibility data of WR 104 is shown in Figure 30; from this data (and the closure phases) images can be reconstructed showing a beautiful spiral structure which appears to rotate on the sky with a period ∼243 days. These spinning, spiral dust shells result from dust formation at the interface of two colliding winds in a Wolf-Rayet and O-star binary.**

**These sources are usually obscured by local dust and thus are faint visible sources (V>**∼**15). The faint V magnitudes make these targets difficult not only for adaptive optics systems, but also for all current interferometers (except the ISI) which use visible-light detectors for star tracking and tip-tilt correction. This limitation hopefully will be**

<!-- page 59 of 86 -->

Optical Interferometry in Astronomy

59

![Image block](doc:b6a1ff8/tier:standard/page:59/block:3)

Figure 29. Shows temporal evolution of the inhomogeneous and clumpy dust shell around carbon star IRC +10216 as seen at 2.2µm using Keck aperture masking (Figure 1 from Tuthill et al., 2000b, reproduced with permission of the AAS).

**eliminated at some facilities by using an infrared star-tracker (for example, IOTA has plans along these lines).**

## 5. The Future

## 5.1. Exciting Trends and Near-Future Science Potential

**As has been said before, now is a practical time for reviewing the major achievements of optical interferometry, for we are entering a new era boasting facilities with significantly greater sensitivity, angular resolution, spectral resolution, and wavelength-coverage. In this section, I will give my views of some of the new capabilities and the expected science returns.**

**One important trend that must be bolstered is the inclusion of theorists and modellers in the observations and interpretations of interferometry data. In many areas, the interferometry observations are outstripping the ready tools for analysis. For example, the wavelength-dependent and time-dependent diameters of AGB stars require a combination of time-dependent hydrodynamical atmospheres and sophisticated radiative transfer codes, a problem very challenging even with today’s supercomputers.**

<!-- page 60 of 86 -->

Optical Interferometry in Astronomy

60

![Chart block](doc:b6a1ff8/tier:standard/page:60/block:3)

![Image block](doc:b6a1ff8/tier:standard/page:60/block:4)

Figure 30. (left panels) a. These figures show the 2.2µm visibility curves, 1-D and 2-D, of WR 104 observed by Keck aperture masking. (right panel) b. This figure shows four epochs of imaging of WR 104 showing a morphology consistent with an Archimedean spiral rotating at a uniform rate (from Monnier, 1999, Figure 13.6)

**Understanding the hotspots seen on the surfaces of stars will required 3-dimensional simulations of stellar convection. Accretion disk physics around young stars should include magnetic fields and demand thoughtful considerations of gas and dust physics in a 2-D or 3-D context. Dust production in colliding winds is very poorly understood, and poses a formidable numerical simulation problem. While tackling these difficult physical problems will require the new high-resolution data from optical interferometers, it is also true that input from the modellers and theorists is needed to guide and suggest experiments and observing strategies.**

**Another general comment is that increasing the angular resolution usually means probing ever decreasing physical scales. Since interferometers often probe scales smaller than an AU, significant changes in time are expected for even small characteristic velocities (∼km/s). This poses both a risk and an opportunity: a risk since data must be taken rapidly and efficiently to accurately capture snapshots of ever-evolving and changing environs, and an opportunity to include dynamics and time-evolution into our models and understanding. Observing the dynamics of circumstellar and/or stellar environments allow new physics to be understood, physics that usually can not be unambiguously reconstructed from typical datasets. Thus, I hope that new dynamical information will break theoretical stalemates which paralyze a number of fields. Interferometers have the opportunity to revolutionize the way we think of the universe: from distant “frozen” images of the past, to a dynamic and engaging unfolding of the present.**

<!-- page 61 of 86 -->

Optical Interferometry in Astronomy

61

**5.1.1. New Long Baselines New long baselines will allow unprecedented high resolution measurements on select sources. With sub-milliarcsecond resolution, one can measure the diameters of “small” sources which have largely eluded current surveys, such as hot stars and nearby low-mass stars. Distortions in the photospheric shapes of rapidly rotating stars or binary stars in nearly Roche-lobe filling systems can be directly detected. Limb-darkening studies of important objects, such as Cepheids, can be accomplished to put the Cepheid distance scale of firm direct footing. Further, long baselines make a variety of exoplanet studies possible, such as directly detecting 51 Peg B-like planets (“Hot” jupiters) or resolving planetary transits across the stellar disk. The NPOI, CHARA, and SUSI interferometers will possess the longest baselines in the near-term, while future projects such as the MRO or ’OHANA (on Mauna Kea, HI) might someday extend the resolution below even 0.10 milliarcseconds with >1 km baselines.**

**5.1.2. Imaging Imaging with optical interferometry is currently tedious at best, and can only investigate simple objects such as resolved photospheres or binary stars. The 6- telescope systems of NPOI and CHARA will soon possess the capability of (comparably) excellent “snapshot” coverage, allowing more complicated and higher dynamic range imaging of select targets. The CHARA array can not be reconfigured and hence will only image well targets with the appropriately-sized structures – for a maximum baseline of ∼330 m at 1.65µm, the optimum size scale is a few milliarcseconds. The NPOI interferometer can be reconfigured to “fill-in” the (u,v)-plane completely over time, and be adjusted for individual sources to optimally measure the needed visibility and closure phase information. In the longer term, the auxiliary telescope array at the VLTI and the proposed outrigger telescopes at Keck will allow even fainter infrared targets to be observed. For imaging, the MRO is currently the most ambitious project in the works, hoping to include >10 telescopes, which would make it the premiere imaging interferometer in the world.**

**Good imaging capabilities would open up new avenues of research, especially in studies of the circumstellar environments at infrared wavelengths. The ability to study disks around young stars and the time evolution of gaps, rings, or other structures would revolutionize our understanding of planet formation. At visible wavelengths, imaging spots on the surfaces of other stars is a major goal, and would allow solar physics to be applied in detail to other stars for the first time.**

**The unexpected discoveries of Keck aperture masking justify our optimism that imaging will uncover many new phenomena that currently are hidden unnoticed in spectral energy distributions. For example, the Wolf-Rayet dust spirals (see Figure 30) have only been observed in a few systems, and represent a new area of study when imaging interferometric arrays are fully commissioned.**

**However, current imaging work using COAST, NPOI, and IOTA interferometers suffer from the lack of dedicated software resources. Unfortunately, the decades of software development in radio interferometry can not be fully leveraged for optical**

<!-- page 62 of 86 -->

Optical Interferometry in Astronomy

62

**interferometry, since radio work now relies largely on phase-referencing techniques not generally available in the optical. New imaging software is needed which can take into account the unique nature of optical interferometry data as well as the different nature of our target sources. The recent adoption of a common data exchange format, defined by the COAST and NPOI interferometer teams, represent an important first step towards these goals (see** [**http://www.mrao.cam.ac.uk/∼jsy1001/exchange/**](http://www.mrao.cam.ac.uk/~jsy1001/exchange/)**).**

**5.1.3. Precision Interferometry This is a rapidly developing area since the advent of single-mode fibers for spatial filtering and “dual-star” phase referencing. When a model of the astronomical source is well-known, then incredibly precise measurements are possible. The most potential for this is in the general area of binary stars, where the stars either are point sources or partially-resolved uniform-disks. The case of detecting an exosolar planet is included in this category, since it can be considered as very high dynamic-range imaging of a faint companion.**

**While there are open questions in binary evolution and stellar astrophysics which demand such high precision, a more popular reason to pursue “Precision Interferometry” is towards detection of extrasolar planets around nearby stars. There are many ways this can be manifested, and I will outline a few of these.**

**Narrow-angle astrometry is a comparatively “classical” way to detect an exosolar planet. Akin to the doppler shift-radial velocity method, precision astrometry attempts to detect the minute wobble of the parent star as a planet proceeds in its orbit. This can be done by monitoring the angular distance between a star and a background reference star. In this case, the target star is normally quite bright and used for phase-referencing to a faint star projected within an isoplanatic patch from the target (<**∼**30”). Lane et al. (2000a) reported the first measurements of this kind using the PTI (see Figure 31). For reference, the motion of Saturn and Jupiter perturb the Sun ∼1 milliarcsecond as viewed from 10 pc. This technique will be applied by the Keck Interferometer and the VLTI interferometer for a planet survey, and there is talk of pursuing this in Antarctica where the isoplanatic patch is larger and the coherence times longer (e.g., Lloyd et al., 2002; Swain, 2002).**

**Another method also being aggressively pursued by the Keck and VLTI interferometers is a multi-wavelength approach to find massive exoplanets by detecting a very slight photocenter shift between different infrared bands due to hypothesized absorption bands in the planet’s atmosphere (i.e., the differential phase method; e.g., Akeson and Swain, 1999; Lopez and Petrov, 2000). This method has the advantage of using the bright target star as its own phase reference. However, recent studies of line-of-sight variability of atmospheric water vapor (Akeson et al., 2000b) indicate that differential chromatic dispersion might be more difficult to calibrate for differential phase methods than originally expected.**

**Precision measurements of closure phases can also be used to detect faint companions, a method which has not received as much attention. As described earlier in this review (§2.2.3), the closure phase is formed by summing the interferometer phases**

<!-- page 63 of 86 -->

Optical Interferometry in Astronomy

63

![Chart block](doc:b6a1ff8/tier:standard/page:63/block:3)

Figure 31. State-of-the-art narrow-angle astrometry of the binary 61 Cyg by the PTI. For a period of one week, the residual astrometric error in declination was ∼100 microarcseconds. Figure printed with permission of SPIE, originally appearing in Lane et al. (2000a).

**on three baselines around a triangle of telescopes, and this quantity is immune to atmospheric phase delays. The lack of attention to precision closure phase methods is understandable since few interferometers possess the requisite minimum of three telescopes. Monnier (2002) and Segransan (2002) recently discussed how closure phases are immune to dominant calibration problems of differential phase and that they can also be used to solve for all the parameters of a binary system without needing to measure any visibility amplitudes. For reference, a typical closure phase for a binary with brightness ratio of 10**<strong><sup>4</sup></strong>**is ∼0.01 degrees as long as the component separation is resolved by the interferometer – the same magnitude effect as for differential phase methods.**

**Current published measurement precision of closure phases is only 0.5 to 5 degrees (Tuthill et al., 2000c; Benson et al., 1997b; Young et al., 2000a). Improving the three orders of magnitudes needed to detect even the brightest possible exoplanet is a daunting challenge. While there are surely unconsidered systematic effects (perhaps due to birefringence or drifts in optical alignment) which will degrade the sensitivity of the precision closure phase technique, the lack of any “showstopper” effects, like differential atmospheric dispersion for the differential phase methods, strongly argues for the further development of the closure phase technique.**

**5.1.4. Nulling Another approach being pursued for planet detection is nulling (Bracewell, 1978). The initial nulling experiments with the MMT (Hinz et al., 1998) have continued (Hinz, 2001), and ultimately will be applied on the Large Binocular Telescope Interferometer (Hinz et al., 2001a). This project is still many years away, but**

<!-- page 64 of 86 -->

Optical Interferometry in Astronomy

64

**offer an alternative approach to the “precision” phase methods above.**

**In the nearer term, the Keck Interferometer will be applying nulling in the midinfrared in order to measure and characterize the zodiacal dust around nearby stars. This source of infrared radiation is expected to be the dominant background for an eventual space-based planet detection interferometer, the so-called “Terrestrial Planet Finder” mission (more information in §5.2). Serabyn and Colavita (2001) describe the “fully symmetric” nulling combiner being implemented on the Keck Interferometer, and initial on-sky tests are expected to begin in 2003. A more complete description of the observing strategy and expected sensitivity has been documented in Kuchner and Serabyn (2003).**

**Nulling can also be applied on large single-apertures, and then are called nulling coronagraphs. New clever designs in coronagraphy are competing with nulling interferometry for space mission concepts to detect terrestial planets around other stars, and I recommend interesting papers on optimally-shaped and apodized pupils (Spergel, 2002; Nisenson and Papaliolios, 2001), bandpass-limited image-masks (Kuchner and Traub, 2002), and phase-mask-based approaches (e.g., Guyon et al., 1999; Rouan et al., 2000).**

**5.1.5. Spectroscopy There have been only a few significant results combining spectroscopy and interferometry; fortunately, this is about to change. The nearinfrared AMBER instrument, slated to arrive at the VLTI interferometer in 2003, will combine three telescope beams together and disperse the light with 3 different spectral resolutions, the maximum is R>**∼**10000. This resolution will allow interferometry on individual spectral lines in the 1-2.5µm regime, opening up shock-excited emission lines, CO-absorption/emission features, and even emission from YSO jets to be probed in novel and exciting ways for the first time. We can expect the value of interferometric observations to be greatly enhanced by these new capabilities.**

**5.1.6. Polarimetry Imaging stars in polarized light with interferometers also promise fascinating new insights into many areas of astrophysics, although this capability is difficult to implement with current interferometers. Vakili et al. (2002) discuss interesting applications of combining the high spectral resolution of AMBER with polarimetry, and highlight the new capabilities for imaging scattered light and potentially even measuring stellar magnetic fields from the Zeeman effect. Experimental efforts (Rousselet-Perraut et al., 1997) in this area have been very limited compared to the theoretical progress (Rousselet-Perraut et al., 2000); this situation should be remedied soon.**

**5.1.7. New Observables Along with greater spectral coverage and more telescopes come new interferometric observables. While §5.1.3 discussed possible applications of differential phase and differential closure phase, there are other interferometric observables yet to be exploited for precision interferometry.**

<!-- page 65 of 86 -->

Optical Interferometry in Astronomy

65

**Measuring the diameter of a star by precisely locating the first null of the visibility pattern is immune to amplitude calibration errors. This could be done by using a well-calibrated spectrograph to search for the null, either measuring fringe amplitudes or looking for the signature phase-flip across the null (e.g., Mozurkewich, private communication). This technique is similar to the method of A. Michelson in measuring the diameter of Betelgeuse (Michelson and Pease, 1921), where the baseline was adjusted in order to find the visibility minimum as detected by his eyes.**

**The closure amplitude (requires sets of 4 telescopes) is an important quantity in radio interferometry to compensate for unstable amplifier gains and varying antenna efficiencies that can be linked to individual telescopes (e.g., Readhead et al., 1980). Closure amplitudes are not practical for current optical interferometers partially because most fringe amplitude variations are not caused by telescope-specific gain changes but rather by changing coherence (e.g., due to changing atmosphere). However, the introduction of spatial filtering (e.g., single-mode fibers) should make the closure amplitude a useful tool for optical interferometry soon (see discussion in Monnier, 2000).**

**Necessarily, most new observables have yet to be used in practice or described in print. I mention here a few possibilities that this author has considered to encourage future experimentation. For instance, it may be possible to use closure amplitudes in the case when fringe jitter causes loss of visibility contrast in a fringe-tracking interferometer, due to the way in which small random phase errors degrade coherence. Also, the Closure Differential Phase is a recently defined quantity (Monnier, 2002), introduced to overcome one limitation of current phase-referencing techniques, namely, that differential phase (and differential closure phase) methods requires assumptions about the source structure of the phase calibrator.**

**5.1.8. Sensitivity (iKeck and VLTI) Another area where we expect immediate progress is in observing new classes of faint objects for the first time. The Keck and VLTI interferometers will have the capability of observing sources as faint as K∼11 magnitude (down to K∼20 with phase referencing), opening up extragalactic sources for the first time. By the time this review is printed, I expect that the first optical interferometric observations of the core of an Active Galactic Nuclei (AGN) will be announced. Size measurements of AGN should offer new constraints on models of the infrared continuum and, when coupled with high spectral resolution, could determine the physical origin of observed broad line regions and possibly even measure dynamical black hole masses.**

**In terms of galactic sources, this increase in sensitivity will allow a broad census of sources to be taken, including YSOs spanning a broad range of ages, luminosities, and distances and binary systems of all masses. For instance, infrared observations of pre-main-sequence binaries allow unique probes of the evolution of binary fraction (e.g., Ghez et al., 1993) as well as important measurements of masses of young stellar objects (Tamazian et al., 2002). I expect interferometer observations to play an increasingly important role in this area as the sensitivity increases.**

**Of course the additional sensitivity will permit new projects too, such as tracking**

<!-- page 66 of 86 -->

Optical Interferometry in Astronomy

66

**the motions of stars orbiting the black hole at the center of the Milky Way with an order of magnitude greater precision than possible today with single-aperture telescopes** (e.g., Schödel et al., 2002). Precision astrometry may allow even new tests of General **Relativity near super massive black holes at the center of nearby galaxies.**

**In addition, the MIDI instrument for the VLTI will allow sensitive measurements in the mid-infrared for the first time. While the ISI interferometer pioneered interferometry in this wavelength range, MIDI+VLTI will be first to probe a wide range of sources with resolution of ∼0.”01 and down to N∼4 mag (>**∼ **100× fainter than the ISI). Midinfrared observations are sensitive to emission from relatively cool dust and can peer through thicker layers of dust than possible in the visible or near-infrared. There are great possibilities for advancing our understanding of young and evolved stars both, and studying dust distributions in a variety of environments.**

## 5.2. Space Interferometry

**The greatest limitations to optical interferometers arise from atmospheric turbulence. It dramatically limits the sensitivity, the ability to do imaging, and forces the engineering to be clumsy and complicated. Space is naturally an ideal place for interferometry, with no atmosphere to corrupt the phase nor limit the coherent integration time. And long baselines are obviously possible by combining light intercepted by separate spacecraft flying in formation.**

**5.2.1. Critical Technologies Needed In order to successfully build space interferometers, many technologies must first be developed. To this day, there has not been any dedicated space interferometer flown (except for the Fine Guidance Sensors on the Hubble Space Telescopes; e.g. Franz et al., 1991).**

**For interferometers deployed on a single structure, one has to contend with truss vibrations, thermal and gravitational gradients, and an unusually large number of mechanisms (failures of which could end the mission). There are issues with propellant and power consumption for maneuvering the array to point around the sky. The Space Interferometry Mission (SIM) is in advanced planning stages and is being designed to measure accurate positions of stars with micro-arcsecond resolution. SIM is a “simple” 2-element interferometer on a deployable truss (∼10 m maximum baseline), and will be the first space mission to attempt space interferometry.**

**Ultimately, one would want to have baselines much longer than ∼10 meters, and this will require separate, free-flying spacecraft. For a space interferometer consisting of “free-flyers,” there are other problems. For instance, maintaining the physical distances between space telescopes to sub-micron tolerances is indeed a challenge. Probably this can not be done; however by monitoring the spacecraft drifts in real-time using laser metrology, the changing distances can be compensated for by onboard (short) delay lines. Some engineering missions have been proposed to test ideas, but have yet to really getoff-the-ground (e.g., the NASA Starlight mission was recently cancelled). NASA and**

<!-- page 67 of 86 -->

Optical Interferometry in Astronomy

67

**ESA should give such a test mission a high priority since the science potential for a free-flyer interferometer is so much greater than for one limited to a single structure.**

**5.2.2. Review of Current NASA & ESA Missions There are a number of mission concepts involving space interferometry being considered by NASA and the European Space Agency (ESA). As mentioned before, the only one in advanced design stages is the NASA Space Interferometry Mission (SIM). In Table 4, I summarize some of the missions that are being proposed, and their main science drivers. Considering the unreliability of expected launch dates, I have omitted these from the table – it is unlikely any of these will fly before 2010 (2020?).**

**NASA and ESA have spent much energy on designing missions to detect Earth like planets around nearby stars, and to measure their crude reflectance (or emission) spectra. With luck, an extrasolar planet spectrum could encode distinctive atmospheric spectral features indicating the presence of life (biomarkers) on the distant planet (e.g., Woolf et al., 2002). While originally envisioned as an infrared interferometer mission, concepts involving a visible-light coronagraph have been proposed lately. This mission is known at the Terrestrial Planet Finder (TPF) in NASA, and as IRSI-Darwin at ESA. The summary table also includes a few TPF follow-on missions, such as “Life Finder.” These missions are very futuristic, and testify to NASA’s ebullient imagination.**

**Another area of interest is imaging the far-infrared and sub-millimeter sky at high angular resolution using space interferometry. These wavelengths are difficult to access from the ground due to water absorption in the atmosphere. Because of this, the angular resolution of current observations are very limited (∼30”); compared to all other wavelengths, the sky has been surveyed with the lowest resolution in the far-IR.**

**The proposed NASA mission “Submillimeter Probe of the Evolution of Cosmic Structure” (SPECS) would be a separate-telescope space interferometer (possibly tethered together and not “free-flying”) designed to map the sky with great sensitivity at a resolution comparable to that currently achievable at other wavelengths. (∼0.010”). This would avoid the confusion-limited regime encountered by current low-angularresolution galaxy count surveys, and allow the evolution of cosmic structure to be investigated back to high redshift. The SPIRIT mission is meant as a precursor to SPECS to test out various aspects on a single platform.**

**The X-ray community has also proposed a space interferometer, which would boast micro-arcsecond resolution and be capable of studying the hot material at the event horizon of nearby Black Holes. Bolstered by successful lab experiments (Cash et al., 2000), plans for a free-flying x-ray interferometer called the Micro-Arcsecond X-ray Imaging Mission (MAXIM) have begun. Controlling distances between macroscopic mirrors to picometer-precision, as is needed for X-ray interferometry, is indeed a daunting challenge. However, a MAXIM precursor mission with only a few meter baseline would have orders of magnitude greater resolution than the Chandra X-ray telescope and stands some chance of being flown.**

<!-- page 68 of 86 -->

Optical Interferometry in Astronomy

68

Table 4. Proposed Space Interferometers

| Acronym | Full Name &amp; Primary Science Drivers |
| --- | --- |
| SIM (NASA) | Space Interferometry MissionPrecision astrometry; exosolar planets |
| FKSI (NASA) | Fourier-Kelvin Space InterferometerFind Jovian planets (nuller); map circumstellar disks |
| SMART-3 (ESA) | SMART-3Test free-flying concept for ESA IRSI-Darwin mission |
| IRSI-Darwin (ESA) | Infra-Red Space Interferometer (one concept: Darwin)Image terrestrial planets (IR nuller); measure spectra |
| TPF (NASA) | Terrestrial Planet FinderImage terrestrial planets (IR nuller); measure spectra |
| SPIRIT (NASA) | Space Infrared Interferometry TrailblazerFar-IR, sub-mm galaxy counts; precursor to SPECS |
| SPECS (NASA) | Submillimeter Probe of the Evolution of Cosmic StructureHigh-resolution map of High-Z universe (far-IR, sub-mm) |
| SI (NASA) | Stellar ImagerImage surfaces of stars (visible, ultraviolet) |
| MAXIM (NASA) | Micro-Arcsecond X-ray Imaging MissionMap black hole accretion disks and event horizons (X-rays) |
| MAXIM Pathfinder (NASA) | MAXIM PathfinderDemonstrate feasibility of X-ray interferometry; achieve 100 μ-arcsecond resolution |
| LF (NASA) | Life FinderSearch for biomarkers in planet spectra; TPF extension |
| PI (NASA) | Planet ImagerImage surfaces of terrestrial planets, 25x25 pixels(requires 6000km baselines, futuristic!) |

## 5.3. Future Ground-based Interferometers

**While it is interesting to speculate about the future of space interferometry, we recognize that it will be expensive, difficult, and slow-paced. In the next 10 or 20 years, we can expect more affordable and rapid progress to be possible from the ground. In this concluding section, I review some of the necessary characteristics of an Optical Very Large Array (OVLA). Ridgway (2000) discusses many of these considerations, and I refer the reader to his interesting report for further details.**

**5.3.1. Design Goals The main design goal of a next-generation optical interferometer array will be to allow the ordinary astronomer to observe a wide-range of targets without requiring extensive expert knowledge in interferometer observations. An imaging interferometer with great sensitivity could fulfill this promise by providing finished images, the most intuitive data format currently in use. It will not be a specialty instrument with narrow science drivers, but a general purpose facility to advance our understanding in a wide range of astrophysical areas.**

<!-- page 69 of 86 -->

Optical Interferometry in Astronomy

69

**5.3.2. Optical Very Large Array One way to achieve this design goal is to scale up the existing arrays. Simply put, this main goal will require an array with a large number of telescopes (>**∼**20 to allow reliable aperture synthesis imaging) and with large-aperture telescopes corrected by adaptive optics (preferably using laser guide stars for full-sky coverage), allowing a reasonably faint limiting magnitude (roughly speaking, brighter than ∼15th magnitude in the infrared with no phase referencing).**

**This array would likely be reconfigurable, like the radio VLA, to allow different angular resolutions to be investigated. The longest baselines should cover a few kilometers (∼0.1 milli-arcsecond resolution in the near-IR). The main limitation of such a system will be a small field-of-view, typically limited to the diffraction-limited beam of an individual telescope (for 10-m class telescopes, the instantaneous field of view would be only about ∼50 milliarcseconds) – although mosaicing would be possible, as in the radio. There are schemes which can image a larger field simultaneously, but are probably not very practical.**

**With an even larger (billion-dollar) budget, one can partially combine the goals of interferometry with the community priority for a 30 m diameter telescope. This clever idea was recently proposed by R. Angel and colleagues at the University of Arizona. In their “20/20” scheme, light from two extremely large telescopes (diameter >20 meters) would be combined in a Fizeau combination scheme, patterned after the Large Binocular Telescope, maintaining the entire field-of-view (∼30”, limited by atmospheric turbulence) with the resolution of the two-element interferometer. Further, this scheme maximizes raw collecting area and would boast potentially incredible sensitivity (>20 mag!). One demanding feature of this design is that the two 20+ m telescopes would have to smoothly move along a track in real-time to maintain the large field-of-view; this may not be impossible, but is surely an interesting complication. Further, the imaging advantages of this system only work when the two-telescope baseline is 5-10× as large as the telescope diameter, and hence the “20/20” interferometer would have maximum baselines of only a few hundred meters at most, not much better than current interferometer arrays. While granting that this system could allow much fainter objects to be observed, this option would cost many times more than a dedicated OVLA system described above.**

**5.3.3. Technological Obstacles Needed to be Overcome If optical interferometry is to continue its impressive growth over the coming decades, important breakthroughs must be made in critical areas. Here, I briefly list a few obvious improvements which would make an OVLA more affordable.**

**The main advance needed to make the OVLA affordable will be the development of “cheap” large aperture telescopes with adaptive optics. Currently, it costs millions of dollars to build even a 4 m-class telescope – without adaptive optics. Advances in lightweight mirrors with adaptive optics designed-in from the beginning may change the economics of the situation.**

**Another area which could revolutionize optical interferometry is advances in**

<!-- page 70 of 86 -->

Optical Interferometry in Astronomy

70

**photonic bandgap fiber materials (e.g., Mueller et al., 2002). These materials offer possibility of extremely wide-bandwidth, low dispersion and low-loss single-mode fibers, which could open up the possibility of practical fiber delay lines. Such an advance would greatly simplify the optical beam-train and engineering of an optical interferometer, making projects such as ’OHANA straightforward. This would put optical interferometry on more similar footing as radio interferometry, where cable delay lines (either coaxial or fiber) are routinely used.**

**Combining dozens of telescopes may not be practical using bulk optics, and solutions involving integrated optics should be pursued. The main limitation of this technology is restricted wavelength coverage, currently only proven shortward of 2.2 µm. Development of materials (e.g., lithium niobate) and fabrication processes that can extend the coverage into the thermal infrared (1-5µm) would mean that a general purpose interferometer could be built around an integrated optics combiner. Work is currently underway in Europe towards this end, in particular in pursuit of mid-infrared nulling capabilities for the ESA IRSI-Darwin mission (Haguenauer and others, 2002).**

**Lastly, improved infrared detectors are crucial to maximizing the scientific output of a future interferometer. It has already been discussed here (see §3.3.5) that near-infrared detectors remain limited by avoidable detector “read” noise, and a future OVLA must have better detectors.**

## 6. Conclusion

**After decades of development, optical interferometry is now poised to play a major role in mainstream astronomy. The emergence of well-funded interferometer “facilities,” in particular the Very Large Telescope Interferometer and the Keck Interferometer, promise to revolutionize the impact of high-resolution observations in many areas of astrophysics. Clearly, the main beneficiaries will be stellar astrophysics and galactic astronomy, in particular the areas of star and planet formation, fundamental stellar properties, and all stages of stellar evolution. In addition, we can look forward to the first extragalactic results.**

**Although the Keck and VLT interferometers hold immense promise, the field is currently driven forward by the activities of many other smaller groups, and scientific results will be dominated by these workers for the near future. While many experimental (astro)physics fields have matured to the point where future progress rests in “big science” collaborations and national research centers (e.g., NASA), optical interferometry represents one of the few healthy and active “experimental astrophysics” endeavors left in astronomy where university-based groups continue to make important technical innovations and astronomical discoveries.**

**It is widely acknowledged that astronomy as a whole is experiencing a golden age of progress, spurred on by observational advances across the electromagnetic spectrum. Optical Interferometry has expanded in response to its own promising initial results, and we in the field look forward to exploiting the significant infrastructure buildup just now**

<!-- page 71 of 86 -->

REFERENCES

71

**being completed. I hope that the next review of optical interferometry will vindicate my optimism in the field, and that the pioneering discoveries reported here presage even grander exploits. It is safe to predict that the next decade will be critical to the field of high-resolution optical astronomy, since the scientific impact of current facilities will wholly determine whether the substantial funding required for an “Optical” Very Large Array can be justified to the international astronomical community.**

## Acknowledgments

**Firstly, I must apologize for omitting many important works due to space constraints, especially in the areas of speckle interferometry. I thank J.-P. Berger, R. Millan-Gabet, and P. Lena for a careful reading of the manuscript and important suggestions. Also, I acknowledge useful conversations with E. Pedretti, A. Boden, P. Tuthill, and F. Malbet. Lastly, I recognize formative discussions with S. Ridgway, C. Haniff, D. Buscher, and D. Mozurkewich, whose ideas have helped shape my perspective of the field of optical interferometry, especially on the future of an OVLA.**

## References

Akeson, R. L., Ciardi, D. R., van Belle, G. T., and Creech-Eakman, M. J. (2002). Constraints on Circumstellar Disk Parameters from Multiwavelength Observations: T Tauri and SU Aurigae. ApJ, 566:1124–1131.

Akeson, R. L., Ciardi, D. R., van Belle, G. T., Creech-Eakman, M. J., and Lada, E. A. (2000a). Infrared Interferometric Observations of Young Stellar Objects. ApJ, 543:313–317.

Akeson, R. L. and Swain, M. R. (1999). Differential phase mode with the Keck Interferometer. In ASP Conf. Ser. 194: Working on the Fringe: Optical and IR Interferometry from Ground and Space, pages 89–+.

Akeson, R. L., Swain, M. R., and Colavita, M. M. (2000b). Differential phase technique with the Keck Interferometer. In Proc. SPIE Vol. 4006, p. 321-327, Interferometry in Optical Astronomy, Pierre J. Lena; Andreas Quirrenbach; Eds., volume 4006, pages 321–327.

Armstrong, J. T., Hummel, C. A., Quirrenbach, A., Buscher, D. F., Mozurkewich, D., Vivekanand, M., Simon, R. S., Denison, C. S., Johnston, K. J., Pan, X.-P., Shao, M., and Colavita, M. M. (1992). The orbit of Phi Cygni measured with long-baseline optical interferometry - Component masses and absolute magnitudes. AJ, 104:2217–2223.

Armstrong, J. T., Nordgren, T. E., Germain, M. E., Hajian, A. R., Hindsley, R. B., Hummel, C. A., Mozurkewich, D., and Thessin, R. N. (2001). Diameters of δ Cephei and η Aquilae Measured with the Navy Prototype Optical Interferometer. AJ, 121:476–481.

Assus, P., Choplin, H., Corteggiani, J. P., Cuot, E., Gay, J., Journet, A., Merlin, G., and Rabbia, Y. (1979). The CERGA infrared interferometer. Journal of Optics, 10:345–350.

Aufdenberg, J. P., Hauschildt, P. H., Baron, E., Nordgren, T. E., Burnley, A. W., Howarth, I. D., Gordon, K. D., and Stansberry, J. A. (2002). The Spectral Energy Distribution and Mass-Loss Rate of the A-Type Supergiant Deneb. ApJ, 570:344–368.

Baldwin, J., Beckett, M., Boysen, R., Burns, D., Buscher, D., Cox, G., Haniff, C., Mackay, C., Nightingale, N., Rogers, J., Scheuer, P., Scott, T., Tuthill, P., Warner, P., Wilson, D., and Wilson, R. (1996a). The first images from an optical aperture synthesis array: mapping of capella with coast at two epochs. A&A, 306:L13–+.

<!-- page 72 of 86 -->

REFERENCES

72

Baldwin, J. E., Beckett, M. G., Boysen, R. C., Burns, D., Buscher, D. F., Cox, G. C., Haniff, C. A., Mackay, C. D., Nightingale, N. S., Rogers, J., Scheuer, P. A. G., Scott, T. R., Tuthill, P. G., Warner, P. J., Wilson, D. M. A., and Wilson, R. W. (1996b). The first images from an optical aperture synthesis array: mapping of Capella with COAST at two epochs. A&A, 306:L13+.

Baldwin, J. E., Haniff, C. A., Mackay, C. D., and Warner, P. J. (1986a). Closure phase in high-resolution optical imaging. Nature, 320:595–597.

Baldwin, J. E., Haniff, C. A., Mackay, C. D., and Warner, P. J. (1986b). Closure phase in high-resolution optical imaging. Nature, 320:595–597.

Bedding, T. R., Robertson, J. G., and Marson, R. G. (1994). An optical interferometer with wavelength dispersion. A&A, 290:340–348.

Benson, J., Hutter, D., Elias, N. M., I., Bowers, P. F., Johnston, K. J., Hajian, A. R., Armstrong, J. T., Mozurkewich, D., Pauls, T. A., Rickard, L. J., Hummel, C. A., White, N. M., Black, D., and Denison, C. (1997a). Multichannel optical aperture synthesis imaging of lambda1 ursae majoris with the navy prototype optical interferometer. AJ, 114:1221–1226.

Benson, J. A., Hutter, D. J., Elias, N. M., Bowers, P. F., Johnston, K. J., Hajian, A. R., Armstrong, J. T., Mozurkewich, D., Pauls, T. A., Rickard, L. J., Hummel, C. A., White, N. M., Black, D., and Denison, C. S. (1997b). Multichannel optical aperture synthesis imaging of lambda1 URSAE majoris with the Navy prototype optical interferometer. AJ, 114:1221–1226.

Berger, J. P., Haguenauer, P., Kern, P., Perraut, K., Malbet, F., Schanen, I., Severi, M., Millan-Gabet, R., and Traub, W. (2001). Integrated optics for astronomical interferometry. IV. First measurements of stars. A&A, 376:L31–L34.

Berger, J. P., Rousselet-Perraut, K., Kern, P., Malbet, F., Schanen-Duport, I., Reynaud, F., Haguenauer, P., and Benech, P. (1999). Integrated optics for astronomical interferometry. II. First laboratory white-light interferograms. A&AS, 139:173–177.

Berio, P., Stee, P., Vakili, F., Mourard, D., Bonneau, D., Chesneau, O., Le Mignant, N. T. D., and Hirata, R. (1999). Interferometric insight into gamma Cassiopeiae long-term variability. A&A, 345:203–210.

Bessell, M. S., Brett, J. M., Wood, P. R., and Scholz, M. (1989). The effects of photospheric extension upon the spectra of M-type Mira variables. A&A, 213:209–225.

Bessell, M. S., Scholz, M., and Wood, P. R. (1996). Phase and cycle dependence of the photospheric structure and observable properties of Mira variables. A&A, 307:481–499.

Bester, M., Danchi, W. C., Degiacomi, C. G., Greenhill, L. J., and Townes, C. H. (1992). Atmospheric fluctuations - empirical structure functions and projected performance of future instruments. ApJ, 392:357–374.

Bester, M., Danchi, W. C., Hale, D., Townes, C. H., Degiacomi, C. G., Mekarnia, D., and Geballe, T. R. (1996). Measurement at 11 Micron Wavelengths of the Diameters of alpha Orionis and alpha Scorpii: Changes in Effective Temperature of alpha Orionis and Very Recent Dust Emission. ApJ, 463:336–+.

Bieging, J. H. and Tafalla, M. (1993). The distribution of molecules in the circumstellar envelope of IRC + 10216 - HC3N, C3N, and SiS. AJ, 105:576–594.

Blazit, A. (1987). PhD thesis, Nice University.

Blazit, A., Bonneau, D., Josse, M., Koechlin, L., Labeyrie, A., and Oneto, J. L. (1977). The angular diameters of Capella A and B from two-telescope interferometry. ApJ, 217:L55–L57.

Boden, A. F., Lane, B. F., Creech-Eakman, M. J., Colavita, M. M., Dumont, P. J., Gubler, J., Koresko, C. D., Kuchner, M. J., Kulkarni, S. R., Mobley, D. W., Pan, X. P., Shao, M., van Belle, G. T., Wallace, J. K., and Oppenheimer, B. R. (1999). The Visual Orbit of 64 Piscium. ApJ, 527:360–368.

Born, M. and Wolf, E. (1965). Principles of optics. Electromagnetic theory of propagation, interf erence and diffraction of light. 3rd edition.

<!-- page 73 of 86 -->

REFERENCES

73

Bracewell, R. N. (1978). Detecting nonsolar planets by spinning infrared interferometer. Nature, 274:780–+.

Brandner, W., Rousset, G., Lenzen, R., Hubin, N., Lacombe, F., Hofmann, R., Moorwood, A., Lagrange, A.-M., Gendron, E., Hartung, M., Puget, P., Ageorges, N., Biereichel, P., Bouy, H., Charton, J., Dumont, G., Fusco, T., Jung, Y., Lehnert, M., Lizon, J.-L., Monnet, G., Mouillet, D., Moutou, C., Rabaud, D., Röhrle, C., Skole, S., Spyromilio, J., Storz, C., Tacconi-Garman, L., and Zins, G. (2002). NAOS+CONICA at YEPUN: first VLT adaptive optics system sees first light. The Messenger, 107:1–+.

Brown, R. H., Davis, J., and Allen, L. R. (1967a). The stellar interferometer at Narrabri Observatory I. A. description of the instrument and the observational procedure. MNRAS, 137:375–+.

Brown, R. H., Davis, J., Allen, L. R., and Rome, J. M. (1967b). The stellar interferometer at Narrabri Observatory-II. The angular diameters of 15 stars. MNRAS, 137:393–+.

Burns, D., Baldwin, J. E., Boysen, R. C., Haniff, C. A., Lawson, P. R., Mackay, C. D., Rogers, J., Scott, T. R., St.-Jacques, D., Warner, P. J., Wilson, D. M. A., and Young, J. S. (1998). Large-amplitude periodic variations in the angular diameter of R Leonis. MNRAS, 297:462–466.

Burns, D., Baldwin, J. E., Boysen, R. C., Haniff, C. A., Lawson, P. R., Mackay, C. D., Rogers, J., Scott, T. R., Warner, P. J., Wilson, D. M. A., and Young, J. S. (1997). The surface structure and limb-darkening profile of Betelgeuse. MNRAS, 290:L11–L16.

Buscher, D. F. (1988). Getting the most out of COAST. PhD thesis, Cambridge University, England.

Buscher, D. F. (1994). Direct maximum-entropy image reconstruction from the bispectrum. In IAU Symp. 158: Very High Angular Resolution Imaging, volume 158, pages 91–+.

Buscher, D. F., Baldwin, J. E., Warner, P. J., and Haniff, C. A. (1990). Detection of a bright feature on the surface of Betelgeuse. MNRAS, 245:7P–11P.

Cash, W., Shipley, A., Osterman, S., and Joy, M. (2000). Laboratory detection of X-ray fringes with a grazing-incidence interferometer. Nature, 407:160–162.

Chagnon, G., Mennesson, B., Perrin, G., Coude Du Foresto, V., Salome, P., Borde, P., Lacasse, M., and Traub, W. (2002). L’-band interferometric observations of evolved stars. AJ, 124:2821–2832.

Chiang, E. I. and Goldreich, P. (1997). Spectral Energy Distributions of T Tauri Stars with Passive Circumstellar Disks. ApJ, 490:368–+.

Clark, B. G. (1980). An efficient implementation of the algorithm ’clean’. A&A, 89:377+.

Colavita, M. M. (1999). Fringe Visibility Estimators for the Palomar Testbed Interferometer. PASP, 111:111–117.

Colavita, M. M., Hines, B. E., Shao, M., Klose, G. J., and Gibson, B. V. (1991). Prototype high speed optical delay line for stellar interferometry. In Active and adaptive optical systems; Proceedings of the Meeting, San Diego, CA, July 22-24, 1991 (A93-39451 15-74), p. 205-212., volume 1542, pages 205–212.

Colavita, M. M., Wallace, J. K., Hines, B. E., Gursel, Y., Malbet, F., Palmer, D. L., Pan, X. P., Shao, M., Yu, J. W., Boden, A. F., Dumont, P. J., Gubler, J., Koresko, C. D., Kulkarni, S. R., Lane, B. F., Mobley, D. W., and Van Belle, G. T. (1999). The palomar testbed interferometer. ApJ, 510:505–521.

Connes, P., Roddier, F., Shaklan, S., and Ribak, E. (1987). Fiber-linked telescope arrays on the ground and in space. In Optical Interferometry in Space, pages 73–83.

Cornwell, T. J. (1983). A method of stabilizing the clean algorithm. A&A, 121:281–285.

Cornwell, T. J. (1987). Radio-interferometric imaging of weak objects in conditions of poor phase stability - the relationship between speckle masking and phase closure methods. A&A, 180:269–274.

Cornwell, T. J. and Wilkinson, P. N. (1981). A new method for making maps with unstable radio interferometers. MNRAS, 196:1067–1086.

<!-- page 74 of 86 -->

REFERENCES

74

Coude Du Foresto, V., Ridgway, S., and Mariotti, J.-M. (1997). Deriving object visibilities from interferograms obtained with a fiber stellar interferometer. A&AS, 121:379–392.

Coude du Foresto, V. and Ridgway, S. T. (1992). Fluor - a Stellar Interferometer Using Single-Mode Fibers. In High-Resolution Imaging by Interferometry, pages 731–+.

Danchi, W. C., Bester, M., Degiacomi, C. G., Greenhill, L. J., and Townes, C. H. (1994). Characteristics of dust shells around 13 late-type stars. AJ, 107:1469–1513.

Danchi, W. C., Tuthill, P. G., and Monnier, J. D. (2001). Near-Infrared Interferometric Images of the Hot Inner Disk surrounding the Massive Young Star MWC 349A. ApJ, 562:440–445.

Davis, J. (1976). High angular resolution stellar interferometry. Proceedings of the Astronomical Society of Australia, 3:26–32.

Davis, J., Morton, D. C., Allen, L. R., and Hanbury Brown, R. (1970). The angular diameter and effective temperature of zeta Puppis. MNRAS, 150:45–54.

di Benedetto, G. P. (1985). Long baseline Michelson stellar interferometry in the near infrared. A&A, 148:169–175.

di Benedetto, G. P. and Conti, G. (1983). Stellar diameter measurements by two-aperture interferometry in the infrared. ApJ, 268:309–318.

di Benedetto, G. P. and Rabbia, Y. (1987). Accurate angular diameters and effective temperatures for eleven giants cooler than K0 by Michelson interferometry. A&A, 188:114–124.

Dullemond, C. P., Dominik, C., and Natta, A. (2001). Passive Irradiated Circumstellar Disks with an Inner Hole. ApJ, 560:957–969.

Dyck, H. M., Benson, J. A., and Ridgway, S. T. (1993). IRMA - A prototype infrared Michelson stellar interferometer. PASP, 105:610–615.

Dyck, H. M., Benson, J. A., van Belle, G. T., and Ridgway, S. T. (1996). Radii and Effective Temperatures for K and M Giants and Supergiants. AJ, 111:1705–+.

Dyck, H. M. and Howell, R. R. (1983). Seeing measurements at Mauna Kea from infrared speckle interferometry. PASP, 95:786–791.

Dyck, H. M. and Nordgren, T. E. (2002). The Effect of TiO Absorption on Optical and Infrared Angular Diameters of Cool Stars. AJ, 124:541–545.

Dyck, H. M., Zuckerman, B., Leinert, C., and Beckwith, S. (1984). Near-infrared speckle interferometry of evolved stars and bipolar nebulae. ApJ, 287:801–813.

Eggen, O. J. (1967). Masses of Visual Binary Stars. ARA&A, 5:105–+.

Eikenberry, S. S., Fazio, G. G., and Ransom, S. M. (1996). An SSPM-Based High-Speed Near-Infrared Photometer for Astronomy. PASP, 108:939–+.

Fizeau, H. (1868). Prix Borodin: Rapport sur le concours de l’année 1867. Comptes Rendus de l’Académie des Sciences, 66:932–934.

Foy, R. (1988). The Photon Counting Camera CP40. In Instrumentation for Ground-Based Optical Astronomy, Present and Future. The Ninth Santa Cruz Summer Workshop in Astronomy and Astrophysics, July 13- 24, 1987, Lick Observatory. Editor, L.B. Robinson; Publisher, Springer-Verlag, New York, NY, 1988. LC # QB856 .S26 1987. ISBN # 0-387-96730-3. P.589, 1988, pages 589–+.

Franz, O. G., Kreidl, T. J. N., Wasserman, L. W., Bradley, A. J., Benedict, G. F., Hemenway, P. D., Jefferys, W. H., McArthur, B., McCartney, J. E., Nelan, E., Shelus, P. J., Story, D., Whipple, A. L., Duncombe, R. L., Fredrick, L. W., and van Altena, W. F. (1991). Binary star observations with the Hubble Space Telescope Fine Guidance Sensors. I - ADS 11300. ApJ, 377:L17–L20.

Fried, D. L. (1965). Statistics of a geometric representation of wavefront distortion. J. Opt. Soc. Am., 55:1427–1435.

<!-- page 75 of 86 -->

REFERENCES

75

Froehly, C. (1982). Coherence and interferometry through optical fibers. In Scientific importance of high angular resolution at infrared and optical wavelengths; Proceedings of the Conference, Garching, West Germany, March 24-27, 1981. (A83-25826 10-89) Garching, West Germany, European Southern Observatory, 1982, p. 285-293; Discussion, p. 293., pages 285–293.

Gay, J. and Journet, A. (1973). Infrared Interferometry. Nature Physical Science, 241:32–33.

Ghez, A. M., Neugebauer, G., and Matthews, K. (1993). The multiplicity of T Tauri stars in the star forming regions Taurus-Auriga and Ophiuchus-Scorpius: A 2.2 micron speckle imaging survey. AJ, 106:2005–2023.

Golay, M. (1971). J. Opt. Soc. Am., 61:272+.

Goodman, J. W. (1985). Statistical optics. New York, Wiley-Interscience, 1985, 567 p.

Gull, S. F. and Skilling, J. (1983). The maximum entropy method. In Indirect Imaging. Measurement and Processing for Indirect Imaging. Proceedings o f an International Symposium held in Sydney, Australia, August 30-September 2, 1983. Editor, J.A. Roberts; Publisher, Cambridge University Press, Cambridge, England, New York, NY, 1984. LC # QB 51.3.E43 I53 1984. ISBN # 0-521-26282-8. P.267, 1983, pages 267+.

Guyon, O., Roddier, C., Graves, J. E., Roddier, F., Cuevas, S., Espejo, C., Gonzalez, S., Martinez, A., Bisiacchi, G., and Vuntesmeri, V. (1999). The Nulling Stellar Coronagraph: Laboratory Tests and Performance Evaluation. PASP, 111:1321–1330.

Haguenauer, P. and others (2002). Nulling interferometric breadboard using integrated optics beam combiners preparation for irsi/darwin mission. Proc. SPIE.

Hajian, A. R., Armstrong, J. T., Hummel, C. A., Benson, J. A., Mozurkewich, D., Pauls, T. A., Hutter, D. J., Elias, N. M., Johnston, K. J., Rickard, L. J., and White, N. M. (1998). Direct Confirmation of Stellar Limb Darkening with the Navy Prototype Optical Interferometer. ApJ, 496:484–+.

Hale, D. D. S., Bester, M., Danchi, W. C., Hoss, S., Lipman, E., Monnier, J. D., Tuthill, P. G., Townes, C. H., Johnson, M., Lopez, B., and Geballe, T. R. (1997). Multiple Dust Shells and Motions around IK Tauri as Seen by Infrared Interferometry. ApJ, 490:407–+.

Hanbury Brown, R., Davis, J., and Allen, L. R. (1974a). The angular diameters of 32 stars. MNRAS, 167:121–136.

Hanbury Brown, R., Davis, J., Allen, L. R., and Rome, J. M. (1967). The stellar interferometer at Narrabri Observatory-II. The angular diameters of 15 stars. MNRAS, 137:393–+.

Hanbury Brown, R., Davis, J., Herbison-Evans, D., and Allen, L. R. (1970). A study of gamma2 Velorum with a stellar intensity interferometer. MNRAS, 148:103–117.

Hanbury Brown, R., Davis, J., Lake, R. J. W., and Thompson, R. J. (1974b). The effects of limb darkening on measurements of angular size with an intensity interferometer. MNRAS, 167:475–484.

Hanbury Brown, R. and Twiss, R. (1956a). Correlation between photons in the two coherent beams of light. Nature, pages 27–29.

Hanbury Brown, R. and Twiss, R. (1956b). A test of a new type of stellar interferometer on sirius. Nature, pages 1046–1048.

Haniff, C. A. and Buscher, D. F. (1998). Variable sub-arcsecond structure in the circumstellar envelope of IRC+10216. A&A, 334:L5–L8.

Haniff, C. A., Buscher, D. F., Christou, J. C., and Ridgway, S. T. (1989). Synthetic aperture imaging at infrared wavelengths. MNRAS, 241:51P–56P.

Haniff, C. A., Mackay, C. D., Titterington, D. J., Sivia, D., and Baldwin, J. E. (1987a). The first images from optical aperture synthesis. Nature, 328:694–696.

Haniff, C. A., Mackay, C. D., Titterington, D. J., Sivia, D., and Baldwin, J. E. (1987b). The first images from optical aperture synthesis. Nature, 328:694–696.

<!-- page 76 of 86 -->

REFERENCES

76

Haniff, C. A., Scholz, M., and Tuthill, P. G. (1995). New Diameter Measurements of 10 Mira Variables - Implications for Effective Temperatures Atmospheric Structure and Pulsation Modes. MNRAS, 276:640–+.

Hartkopf, W. I., McAlister, H. A., and Mason, B. D. (2001). The 2001 US Naval Observatory Double Star CD-ROM. III. The Third Catalog of Interferometric Measurements of Binary Stars. AJ, 122:3480–3481.

Hartmann, L., Kenyon, S. J., and Calvet, N. (1993). The excess infrared emission of Herbig Ae/Be stars - Disks or envelopes? ApJ, 407:219–231.

Hillenbrand, L. A., Strom, S. E., Vrba, F. J., and Keene, J. (1992). Herbig Ae/Be stars - Intermediatemass stars surrounded by massive circumstellar accretion disks. ApJ, 397:613–643.

Hinz, P. M. (2001). Nulling interferometry for studying other planetary systems: Techniques and observations. PhD thesis, University of Arizona.

Hinz, P. M., Angel, J. R. P., Hoffmann, W. F., McCarthy, D. W., McGuire, P. C., Cheselka, M., Hora, J. L., and Woolf, N. J. (1998). Imaging circumstellar environments with a nulling interferometer. Nature, 395:251–253.

Hinz, P. M., Angel, J. R. P., McCarthy, D. W., Hoffmann, W. F., and Woolf, N. J. (2001a). Detecting Exo-Solar Planetary Systems With THE LBT. In Science with the Large Binocular Telescope, pages 203–+.

Hinz, P. M., Hoffmann, W. F., and Hora, J. L. (2001b). Constraints on Disk Sizes around Young Intermediate-Mass Stars: Nulling Interferometric Observations of Herbig Ae Objects. ApJ, 561:L131–L134.

Hofmann, K. e. a. (2002). Near-infrared IOTA interferometry of CH Cyg. In Proc. SPIE, Interferometry in Optical Astronomy, W. A. Traub; E d.

Hofmann, K. H. and Weigelt, G. (1993). Iterative image reconstruction from the bispectrum. A&A, 278:328–339.

Högbom, J. A. (1974). Aperture synthesis with a non-regular distribution of interferometer baselines. A&AS, 15:417–426.

Horton, A. J., Buscher, D. F., and Haniff, C. A. (2001). Diffraction losses in ground-based optical interferometers. MNRAS, 327:217–226.

Hummel, C. A., Armstrong, J. T., Buscher, D. F., Mozurkewich, D., Quirrenbach, A., and Vivekanand, M. (1995). Orbits of Small Angular Scale Binaries Resolved with the Mark III Interferometer. AJ, 110:376–+.

Hummel, C. A., Carquillat, J.-M., Ginestet, N., Griffin, R. F., Boden, A. F., Hajian, A. R., Mozurkewich, D., and Nordgren, T. E. (2001). Orbital and Stellar Parameters of Omicron Leonis from Spectroscopy and Interferometry. AJ, 121:1623–1635.

Hummel, C. A., Mozurkewich, D., Armstrong, J. T., Hajian, A. R., Elias, N. M., and Hutter, D. J. (1998). Navy Prototype Optical Interferometer Observations of the Double Stars Mizar A and Matar. AJ, 116:2536–2548.

Hutter, D. J., Johnston, K. J., Mozurkewich, D., Simon, R. S., Colavita, M. M., Pan, X. P., Shao, M., Hines, B. E., Staelin, D. H., Hershey, J. L., Hughes, J. A., and Kaplan, G. H. (1989). Angular diameter measurements of 24 giant and supergiant stars from the Mark III optical interferometer. ApJ, 340:1103–1111.

Jacob, A. P. and Scholz, M. (2002). Effects of molecular contamination of IR near-continuum bandpasses on measurements of M-type Mira diameters. MNRAS, 336:1377–1389.

Jennison, R. C. (1958). MNRAS, 118:276+.

Johnson, M. A., Betz, A. L., and Townes, C. H. (1974). 10-micron heterodyne stellar interferometer. Physical Review Letters, 33:1617–1620.

<!-- page 77 of 86 -->

REFERENCES

77

Keady, J. J. and Ridgway, S. T. (1993). The IRC + 10216 circumstellar envelope. III - Infrared molecular line profiles. ApJ, 406:199–214.

Keen, J. W., Buscher, D. F., and Warner, P. J. (2001). Numerical simulations of pinhole and singlemode fibre spatial filters for optical interferometers. MNRAS, 326:1381–1386.

Kern, P., Malbet, F., Schanen-Duport, I., and Benech, P. (1997). Integrated optics single-mode interferometric beam combiner for near infrared astronomy. In Integrated Optics for Astronomical Interferometry, pages 195–+.

Kervella, P., Coudé du Foresto, V., Perrin, G., Schöller, M., Traub, W. A., and Lacasse, M. G. (2001). The angular diameter and distance of the Cepheid ζ Geminorum. A&A, 367:876–883.

Keto, E. (1997). The Shapes of Cross-Correlation Interferometers. ApJ, 475:843–+.

Knox, K. T. and Thompson, B. J. (1974). Recovery of images from atmospherically degraded shortexposure photographs. ApJ, 193:L45–L48.

Kolmogorov, A. (1961). Turbulence, Classic Papers on Statistical Theory. Interscience, New York.

Koresko, C. D., van Belle, G. T., Boden, A. F., Colavita, M. M., Creech-Eakman, M. J., Dumont, P. J., Gubler, J., Kulkarni, S. R., Lane, B. F., Mobley, D. W., Pan, X. P., Shao, M., Wallace, J. K., and The PTI Collaboration (1998). The Visual Orbit of the 0.002” RS CVN Binary Star TZ Triangulifrom Near-Infrared Long-Baseline Interferometry. ApJ, 509:L45–L48.

Kuchner, M. and Serabyn, E. (2003). Modeling Exozodiacal Dust Detection with the Keck Interferometer. ApJ.

Kuchner, M. J. and Traub, W. A. (2002). A Coronagraph with a Band-limited Mask for Finding Terrestrial Planets. ApJ, 570:900–908.

Labeyrie, A. (1970a). Attainment of diffraction limited resolution in large telescopes by fourier analysing speckle patterns in star images. A&A, 6:85+.

Labeyrie, A. (1970b). Attainment of Diffraction Limited Resolution in Large Telescopes by Fourier Analysing Speckle Patterns in Star Images. A&A, 6:85–+.

Labeyrie, A. (1975). Interference fringes obtained on VEGA with two optical telescopes. ApJ, 196:L71– L75.

Labeyrie, A. (1996). Resolved imaging of extra-solar planets with future 10-100km optical interferometric arrays. A&AS, 118:517–524.

Labeyrie, A., Koechlin, L., Bonneau, D., Blazit, A., and Foy, R. (1977). Strong TiO-related variations in the diameters of Mira and R Leonis. ApJ, 218:L75–L78.

Lachaume, R. (2003). On marginally resolved objects in optical interferometry. A&A, 400:795–803.

Lagrange, A., Mourard, D., and Lena, P., editors (1997). High angular resolution in astrophysics.

Lane, B. F., Boden, A. F., and Kulkarni, S. R. (2001). Interferometric Measurement of the Angular Sizes of Dwarf Stars in the Spectral Range K3-M4. ApJ, 551:L81–L83.

Lane, B. F. and Colavita, M. (2003). Phase Referenced Stellar Interferometry at the Palomar Testbed Interferometer. ApJ(in press).

Lane, B. F. and Colavita, M. M. (1999). Phase Referenced Stellar Interferometry at PTI. Bulletin of the American Astronomical Society, 31:1503–+.

Lane, B. F., Colavita, M. M., Boden, A. F., and Lawson, P. R. (2000a). Palomar Testbed Interferometer: update. In Proc. SPIE Vol. 4006, p. 452-458, Interferometry in Optical Astronomy, Pierre J. Lena; Andreas Quirrenbach; Eds., volume 4006, pages 452–458.

Lane, B. F., Creech-Eakman, M. J., and Nordgren, T. E. (2002). Long-Baseline Interferometric Observations of Cepheids. ApJ, 573:330–337.

Lane, B. F., Kuchner, M. J., Boden, A. F., Creech-Eakman, M., and Kulkarni, S. R. (2000b). Direct detection of pulsations of the Cepheid star ζ Gem and an independent calibration of the periodluminosity relation. Nature, 407:485–487.

<!-- page 78 of 86 -->

REFERENCES

78

Lawson, P. (2000). Phase and group delay estimation. In Principles of Long Baseline Stellar Interferometry, page 113.

Lawson, P. R. (1994). Artifacts in PAPA camera images. Appl. Opt., 33:1146–1153.

Lawson, P. R. (2000a). Notes on the History of Stellar Interferometry. In Principles of Long Baseline Stellar Interferometry, pages 325–+.

Lawson, P. R., editor (2000b). Principles of Long Baseline Stellar Interferometry.

Lloyd, J. P., Oppenheimer, B. R., and Graham, J. R. (2002). The Potential of Differential Astrometric Interferometry from the High Antarctic Plateau. Publications of the Astronomical Society of Australia, 19:318–322.

Lopez, B., Danchi, W. C., Bester, M., Hale, D. D. S., Lipman, E. A., Monnier, J. D., Tuthill, P. G., Townes, C. H., Degiacomi, C. G., Geballe, T. R., Greenhill, L. J., Cruzalebes, P., Lefevre, J., Mekarina, D., Mattei, J. A., Nishimoto, D., and Kervin, P. W. (1997). Nonspherical Structures and Temporal Variations in the Dust Shell of O Ceti Observed with a Long Baseline Interferometer at 11 Microns. ApJ, 488:807–+.

Lopez, B. and Petrov, R. G. (2000). Direct Detection of Hot Extrasolar Planets Using Differential Interferometry. In From Extrasolar Planets to Cosmology: The VLT Opening Symposium, Proceedings of the ESO Symposium held at Antofagasta, Chile, 1-4 March 1999. Edited by Jacqueline Bergeron and Alvio Renzini. Berlin: Springer-Verlag, 2000. p. 565., pages 565–+.

Mackay, C. D., Tubbs, R. N., Bell, R., Burt, D. J., Jerram, P., and Moody, I. (2001). Subelectron read noise at MHz pixel rates. In Proc. SPIE Vol. 4306, p. 289-298, Sensors and Camera Systems for Scientific, Industrial, and Digital Photography Applications II, Morley M. Blouke; John Canosa; Nitin Sampat; Eds., volume 4306, pages 289–298.

Malbet, F., Berger, J.-P., Colavita, M. M., Koresko, C. D., Beichman, C., Boden, A. F., Kulkarni, S. R., Lane, B. F., Mobley, D. W., Pan, X. P., Shao, M., van Belle, G. T., and Wallace, J. K. (1998). FU Orionis Resolved by Infrared Long-Baseline Interferometry at a 2 AU Scale. ApJ, 507:L149–L152.

Malbet, F., Kern, P., Schanen-Duport, I., Berger, J.-P., Rousselet-Perraut, K., and Benech, P. (1999). Integrated optics for astronomical interferometry. I. Concept and astronomical applications. A&AS, 138:135–145.

Marengo, M., Sasselov, D. D., Karovska, M., Papaliolios, C., and Armstrong, J. T. (2002). Theoretical Limb Darkening for Pulsating Cepheids. ApJ, 567:1131–1139.

Mariotti, J.-M., Di Benedetto, G. P., Braun, R., Foy, R., Genzel, R., Koechlin, L., and Weigelt, G. (1992). Coherent combined instrumentation for the vlt. Technical Report VLT-65, European Southern Observatory, Garching, Germany.

Matsuura, M., Yamamura, I., Cami, J., Onaka, T., and Murakami, H. (2002). The time variation in infrared water-vapour bands in Mira variables. A&A, 383:972–986.

McAlister, H. A. (1985). High angular resolution measurements of stellar properties. ARA&A, 23:59–87.

McCarthy, D. W., Howell, R., and Low, F. J. (1978). Apparent variation in the diameter of Omicron Ceti at 10.2 microns. ApJ, 223:L113–L116.

McCarthy, D. W. and Low, F. J. (1975). Initial results of spatial interferometry at 5 microns. ApJ, 202:L37–L40.

McCarthy, D. W., Low, F. J., and Howell, R. (1977). Angular diameter measurements of Alpha Orionis, VY Canis Majoris, and IRC + 10216 at 8.3, 10.2, and 11.1 micrometers. ApJ, 214:L85–L89.

Mennesson, B., Mariotti, J. M., Coudé Du Foresto, V., Perrin, G., Ridgway, S., Ruilier, C., Traub, W. A., Carleton, N. P., Lacasse, M. G., and Mazé, G. (1999). Thermal infrared stellar interferometry using single-mode guided optics: first results with the TISIS experiment on IOTA. A&A, 346:181–189.

<!-- page 79 of 86 -->

REFERENCES

79

Mennesson, B., Perrin, G., Chagnon, G., Foresto, V. C. d., Ridgway, S., Merand, A., Salome, P., Borde, P., Cotton, W., Morel, S., Kervella, P., Traub, W., and Lacasse, M. (2002). Evidence for Very Extended Gaseous Layers around O-rich Mira Variables and M Giants. ApJ, 579:446–454.

Michelson, A. A. (1890). On the application of interference methods to astronomical measurements. Phil. Mag., 30:1–20.

Michelson, A. A. (1891). Measurement of Jupiter’s satellites by interference. Nature, 45:160–161.

Michelson, A. A. and Pease, F. G. (1921). Measurement of the diameter of α Orionis with the interferometer. ApJ, 53:249–259.

Michelson, A. A. and Pease, F. G. (1921). Measurement of the diameter of alpha Orionis with the interferometer. ApJ, 53:249–259.

Millan-Gabet, R. (1999). Investigation of Herbig Ae/Be stars in the near-infrared with a long baseline interferometer. PhD thesis, University of Massachusetts at Amherst.

Millan-Gabet, R., Schloerb, F. P., and Traub, W. A. (2001). Spatially Resolved Circumstellar Structure of Herbig AE/BE Stars in the Near-Infrared. ApJ, 546:358–381.

Millan-Gabet, R., Schloerb, F. P., Traub, W. A., and Carleton, N. P. (1999a). A NICMOS3 Camera for Fringe Detection at the IOTA Interferometer. PASP, 111:238–245.

Millan-Gabet, R., Schloerb, F. P., Traub, W. A., Malbet, F., Berger, J. P., and Bregman, J. D. (1999b). Sub-Astronomical Unit Structure of the Near-Infrared Emission from AB Aurigae. ApJ, 513:L131–L134.

Monnier, J. (2002). Astrophysics with closure phases. In Eurowinter School: Observing with the Very Large Telescope Interferometer.

Monnier, J. D. (1999). Infrared Interferometry and Spectroscopy of Circumstellar Envelopes. PhD thesis, University of California at Berkeley.

Monnier, J. D. (2000). An Introduction to Closure Phases. In Principles of Long Baseline Stellar Interferometry, pages 203–+.

Monnier, J. D. (2001). Asymmetric Beam Combination for Optical Interferometry. PASP, 113:639–645.

Monnier, J. D., Bester, M., Danchi, W. C., Johnson, M. A., Lipman, E. A., Townes, C. H., Tuthill, P. G., Geballe, T. R., Nishimoto, D., and Kervin, P. W. (1997). Nonuniform Dust Outflow Observed around Infrared Object NML Cygni. ApJ, 481:420–+.

Monnier, J. D., Danchi, W. C., Hale, D. S., Lipman, E. A., Tuthill, P. G., and Townes, C. H. (2000a). Mid-Infrared Interferometry on Spectral Lines. II. Continuum (Dust) Emission Around IRC +10216 and VY Canis Majoris. ApJ, 543:861–867.

Monnier, J. D., Danchi, W. C., Hale, D. S., Tuthill, P. G., and Townes, C. H. (2000b). Mid-Infrared Interferometry on Spectral Lines. III. Ammonia and Silane around IRC +10216 and VY Canis Majoris. ApJ, 543:868–879.

Monnier, J. D., Fitelson, W., Danchi, W. C., and Townes, C. H. (2000c). Mid-Infrared Interferometry on Spectral Lines. I. Instrumentation. ApJS, 129:421–429.

Monnier, J. D. and Millan-Gabet, R. (2002). On the Interferometric Sizes of Young Stellar Objects. ApJ, 579:694–698.

Monnier, J. D., Tuthill, P. G., and Danchi, W. C. (1999). Pinwheel Nebula around WR 98A. ApJ, 525:L97–L100.

Mourard, D., Bonneau, D., Koechlin, L., Labeyrie, A., Morand, F., Stee, P., Tallon-Bosc, I., and Vakili, F. (1997). The mean angular diameter of {delta} Cephei measured by optical long-baseline interferometry. A&A, 317:789–792.

Mourard, D., Bosc, I., Labeyrie, A., Koechlin, L., and Saha, S. (1989). The rotating envelope of the hot star Gamma Cassiopeiae resolved by optical interferometry. Nature, 342:520–522.

<!-- page 80 of 86 -->

REFERENCES

80

Mourard, D., Tallon-Bosc, I., Blazit, A., Bonneau, D., Merlin, G., Morand, F., Vakili, F., and Labeyrie, A. (1994). The GI2T interferometer on Plateau de Calern. A&A, 283:705–713.

Mozurkewich, D. (2000). Interferometer Design for Synthesis Imaging. In Principles of Long Baseline Stellar Interferometry, page 231.

Mozurkewich, D., Hutter, D. J., Johnston, K. J., Simon, R. S., Shao, M., Colavita, M. M., Staelin, D. H., Hines, B., Hershey, J. L., Hughes, J. A., and Kaplan, G. H. (1988). Preliminary measurements of star positions with the Mark III stellar interferometer. AJ, 95:1269–1277.

Mozurkewich, D., Johnston, K. J., Simon, R. S., Bowers, P. F., Gaume, R., Hutter, D. J., Colavita, M. M., Shao, M., and Pan, X. P. (1991). Angular diameter measurements of stars. AJ, 101:2207–2219.

Mueller, D., West, J. A., and Koch, K. W. (2002). Interferometric chromatic dispersion measurement of a photonic bandgap fiber. In Proc. SPIE Vol. 4870, p. 395-403, Active and Passive Optical Components for WDM Communications II, Achyut K. Dutta; Abdul Ahad S. Awwal; Niloy K. Dutta; Katsunari Okamoto; Eds., volume 4870, pages 395–403.

Narayan, R. and Nityananda, R. (1986). Maximum entropy image restoration in astronomy. ARA&A, 24:127–170.

Natta, A., Prusti, T., Neri, R., Wooden, D., Grinin, V. P., and Mannings, V. (2001). A reconsideration of disk properties in Herbig Ae stars. A&A, 371:186–197.

Nisenson, P. and Papaliolios, C. (2001). Detection of Earth-like Planets Using Apodized Telescopes. ApJ, 548:L201–L205.

Nordgren, T. E., Germain, M. E., Benson, J. A., Mozurkewich, D., Sudol, J. J., Elias, N. M., Hajian, A. R., White, N. M., Hutter, D. J., Johnston, K. J., Gauss, F. S., Armstrong, J. T., Pauls, T. A., and Rickard, L. J. (1999). Stellar Angular Diameters of Late-Type Giants and Supergiants Measured with the Navy Prototype Optical Interferometer. AJ, 118:3032–3038.

Nordgren, T. E., Sudol, J. J., and Mozurkewich, D. (2001). Comparison of Stellar Angular Diameters from the NPOI, the Mark III Optical Interferometer, and the Infrared Flux Method. AJ, 122:2707–2712.

Papaliolios, C., Nisenson, P., and Ebstein, S. (1985). Speckle imaging with the PAPA detector. Appl. Opt., 24:287–292.

Peacock, T., Verhoeve, P., Rando, N., Perryman, M. A. C., Taylor, B. G., and Jakobsen, P. (1997). Superconducting tunnel junctions as detectors for ultraviolet, optical, and near infrared astronomy. A&AS, 123:581–587.

Perley, R. A., Schwab, F., and Bridle, A. H. (1986). In Synthesis Imaging: Course Notes from an NRAO Summer School (Workshop No. 13).

Perrin, G. (2003). The calibration of interferometric visibilities obtained with single-mode optical interferometers. Computation of error bars and correlations. A&A, 400:1173–1181.

Perrin, G., Coudé du Foresto, V., Ridgway, S. T., Mennesson, B., Ruilier, C., Mariotti, J.-M., Traub, W. A., and Lacasse, M. G. (1999). Interferometric observations of R Leonis in the K band. First direct detection of the photospheric pulsation and study of the atmospheric intensity distribution. A&A, 345:221–232.

Perrin, G., Coude Du Foresto, V., Ridgway, S. T., Mariotti, J.-M., Traub, W. A., Carleton, N. P., and Lacasse, M. G. (1998). Extension of the effective temperature scale of giants to types later than M6. A&A, 331:619–626.

Perrin, G. and Malbet, F., editors (2002). EDP Sciences.

Perryman, M. A. C., Cropper, M., Ramsay, G., Favata, F., Peacock, A., Rando, N., and Reynolds, A. (2001). High-speed energy-resolved STJ photometry of the eclipsing binary UZ For. MNRAS, 324:899–909.

<!-- page 81 of 86 -->

REFERENCES

81

Petrov, R. G., Malbet, F., Richichi, A., Hofmann, K., Mourard, D., Agabi, K., Antonelli, P., Aristidi, E., Baffa, C., Beckmann, U., Berio, P., Bresson, Y., and Cassaing, F. (2000). AMBER: the nearinfrared focal instrument for the Very Large Telescope Interferometer. In Proc. SPIE Vol. 4006, p. 68-79, Interferometry in Optical Astronomy, Pierre J. Lena; Andreas Quirrenbach; Eds., volume 4006, pages 68–79.

Pina, R. K. and Puetter, R. C. (1992). Incorporation of spatial information in Bayesian image reconstruction: The maximum residual likelihood criterion. PASP, 104:1096+.

Quirrenbach, A. (2000). Observing through the turbulent atmosphere. In Principles of Long Baseline Stellar Interferometry, pages 71–+.

Quirrenbach, A. (2001). Optical Interferometry. ARA&A, 39:353–401.

Quirrenbach, A., Buscher, D. F., Mozurkewich, D., Hummel, C. A., and Armstrong, J. T. (1994). Maximum-entropy maps of the Be shell star zeta Tauri from optical long-baseline interferometry. A&A, 283:L13–L16.

Quirrenbach, A., Hummel, C. A., Buscher, D. F., Armstrong, J. T., Mozurkewich, D., and Elias, N. M. (1993a). The Asymmetric Envelope of gamma Cassiopeiae Observed with the MK III Optical Interferometer. ApJ, 416:L25+.

Quirrenbach, A., Mozurkewich, D., Armstrong, J. T., Buscher, D. F., and Hummel, C. A. (1993b). Angular diameter measurements of cool giant stars in strong TiO bands and in the continuum. ApJ, 406:215–219.

Quirrenbach, A., Mozurkewich, D., Buscher, D. F., Hummel, C. A., and Armstrong, J. T. (1996). Angular diameter and limb darkening of Arcturus. A&A, 312:160–166.

Rabbia, Y., Mekarnia, D., and Gay, J. (1990). Infrared interferometry at Observatoire de la Cote d’Azur, France. In Infrared technology XVI; Proceedings of the Meeting, San Diego, CA, July 11-13, 1990 (A92-21426 07-35). Bellingham, WA, Society of Photo-Optical Instrumentation Engineers, 1990, p. 172-182., volume 1341, pages 172–182.

Readhead, A., Nakajima, T., Pearson, T., Neugebauer, G., Oke, J., and Sargent, W. (1988). Diffractionlimited imaging with ground-based optical telescopes. AJ, 95:1278–1296.

Readhead, A. C. S., Walker, R. C., Pearson, T. J., and Cohen, M. H. (1980). Mapping radio sources with uncalibrated visibility data. Nature, 285:137–140.

Readhead, A. C. S. and Wilkinson, P. N. (1978). The mapping of compact radio sources from vlbi data. ApJ, 223:25–36.

Reynaud, F., Alleman, J. J., and Connes, P. (1992). Interferometric control of fiber lengths for a coherent telescope array. Appl. Opt., 31:3736–3743.

Ridgway, S. T. (2000). Future Ground-Based Interferometry. In Principles of Long Baseline Stellar Interferometry, pages 311–+.

Ridgway, S. T., Jacoby, G. H., Joyce, R. R., Siegel, M. J., and Wells, D. C. (1982). Angular diameters by the lunar occultation techniques. VI - Limb darkening of alpha Tauri. AJ, 87:1044–1050.

Ridgway, S. T., Joyce, R. R., White, N. M., and Wing, R. F. (1980). Effective temperatures of late-type stars - The field giants from K0 to M6. ApJ, 235:126–137.

Roddier, C. and Roddier, F. (1983). High angular resolution observations of alpha Orionis with a rotation shearing interferometer. ApJ, 270:L23–L26.

Roddier, F. (1981). The Effects of Atmospheric Turbulence in Optical Astronomy. Prog. Optics, Volume 19, p. 281-376, 19:281–376.

Roddier, F. (1986). Optics Communications, 60:145+.

Roddier, F., Cowie, L., Graves, J. E., Songaila, A., and MCKenna, D. (1990). Seeing at Mauna Kea - a joint UH-UN-NOAO-CFHT study. Proc. SPIE, 1236:485–491.

<!-- page 82 of 86 -->

REFERENCES

82

Roddier, F., Gilli, J. M., and Lund, G. (1982). On the origin of speckle boiling and its effects in stellar speckle interferometry. Journal of Optics, vol. 13, Sept.-Oct. 1982, p. 263-271., 13:263–271.

Rogstad, D. H. (1968). Applied Optics, 7:585+.

Rouan, D., Riaud, P., Boccaletti, A., Clénet, Y., and Labeyrie, A. (2000). The Four-Quadrant Phase-Mask Coronagraph. I. Principle. PASP, 112:1479–1486.

Rousselet-Perraut, K., Chesneau, O., Berio, P., and Vakili, F. (2000). Spectro-polarimetric interferometry (SPIN) of magnetic stars. A&A, 354:595–604.

Rousselet-Perraut, K., Vakili, F., Mourard, D., Morand, F., Bonneau, D., and Stee, P. (1997). An attempt to detect polarization effects in the envelope of gamma Cassiopeiae with the GI2T interferometer. A&AS, 123:173–177.

Rowan-Robinson, M. and Harris, S. (1982). Radiative transfer in dust clouds. II - Circumstellar dust shells around early M giants and supergiants. MNRAS, 200:197–215.

Sasselov, D. and Karovska, M. (1994). On Cepheid diameter and distance measurement. ApJ, 432:367–372.

Schödel, R., Ott, T., Genzel, R., Hofmann, R., Lehnert, M., Eckart, A., Mouawad, N., Alexander, T., Reid, M. J., Lenzen, R., Hartung, M., Lacombe, F., Rouan, D., Gendron, E., Rousset, G., Lagrange, A.-M., Brandner, W., Ageorges, N., Lidman, C., Moorwood, A. F. M., Spyromilio, J., Hubin, N., and Menten, K. M. (2002). A star in a 15.2-year orbit around the supermassive black hole at the centre of the Milky Way. Nature, 419:694–696.

Schwab, F. R. (1984). Relaxing the isoplanatism assumption in self-calibration; applications to lowfrequency radio interferometry. AJ, 89:1076–1081.

Schwarzschild, M. (1975). On the scale of photospheric convection in red giants and supergiants. ApJ, 195:137–144.

Segransan, D. (2002). Does the differential phase closure allow to detect photons from hot jupiters? In SF2A-2002: Semaine de l’Astrophysique Francaise.

Segransan, D., Kervella, P., Forveille, T., and Queloz, D. (2003). First radius measurements of very low mass stars with the vlti. A&A(in press).

Serabyn, E. and Colavita, M. M. (2001). Fully Symmetric Nulling Beam Combiners. Appl. Opt., 40:1668–1671.

Shaklan, S. and Roddier, F. (1988). Coupling starlight into single-mode fiber optics. Appl. Opt., 27:2334–2338.

Shaklan, S. B. (1989). Multiple Beam Correlation Using Single-Mode Fiber Optics with Application to Interferometric Imaging. Ph.D. Thesis.

Shaklan, S. B. and Roddier, F. (1987). Single-mode fiber optics in a long-baseline interferometer. Appl. Opt., 26:2159–2163.

Shao, M. and Colavita, M. M. (1992a). Long-baseline optical and infrared stellar interferometry. ARA&A, 30:457–498.

Shao, M. and Colavita, M. M. (1992b). Potential of long-baseline infrared interferometry for narrowangle astrometry. A&A, 262:353–358.

Shao, M., Colavita, M. M., Hines, B. E., Staelin, D. H., and Hutter, D. J. (1988). The Mark III stellar interferometer. A&A, 193:357–371.

Shao, M. and Staelin, D. H. (1977). Long-baseline optical interferometer for astrometry. Optical Society of America Journal, 67:81–86.

Shao, M. and Staelin, D. H. (1980). First fringe measurements with a phase-tracking stellar interferometer. Appl. Opt., 19:1519–1522.

Short, N., Fitelson, W., Hale, D., and Townes, C. (2002). Low-altitude turbulence at Mount Wilson Observatory. In Proc. SPIE Vol. 4838, Interferometry for Optical Astronomy II, Wesley A. Traub Ed., volume 4838.

<!-- page 83 of 86 -->

REFERENCES

83

Simohamed, L. M. and Reynaud, F. (1997). AA 2 M stroke optical fibre delay line. Pure Appl. Opt., Volume 6, Issue 4, p. L37-L41 (1997)., 6:L37–L41.

Sivia, D. (1987). PhD thesis, Cambridge University.

Skilling, J. and Bryan, R. K. (1984). Maximum entropy image reconstruction - general algorithm. MNRAS, 211:111+.

Spergel, D. (2002). A new pupil for detecting extra-solar planets. Applied Optics, submitted.

Stee, P., de Araujo, F. X., Vakili, F., Mourard, D., Arnold, L., Bonneau, D., Morand, F., and Tallon Bosc, I. (1995). {gamma} Cassiopeiae revisited by spectrally resolved interferometry. A&A, 300:219– +.

Stee, P., Vakili, F., Bonneau, D., and Mourard, D. (1998). On the inner envelope of the Be star gamma Cassiopeiae. A&A, 332:268–272.

Sutton, E. C., Betz, A. L., Storey, J. W. V., and Spears, D. L. (1979). The brightness distribution of IRC +10216 at 11 microns. ApJ, 230:L105–L108.

Sutton, E. C., Storey, J. W. V., Betz, A. L., Townes, C. H., and Spears, D. L. (1977). Spatial heterodyne interferometry of VY Canis Majoris, Alpha Orionis, Alpha Scorpii, and R Leonis at 11 microns. ApJ, 217:L97–L100.

Sutton, E. C., Storey, J. W. V., Townes, C. H., and Spears, D. L. (1978). Variations in the spatial distribution of 11 micron radiation from Omicron Ceti. ApJ, 224:L123–L126.

Sutton, E. C., Subramanian, S., and Townes, C. H. (1982). Interferometric measurements of stellar positions in the infrared. A&A, 110:324–331.

Swain, M. (2002). Private communication.

Tamazian, V. S., Docobo, J. ., White, R. J., and Woitas, J. (2002). Preliminary Orbits and System Masses for Five Binary T Tauri Stars. ApJ, 578:925–934.

Tango, W. J. (1990). Dispersion in stellar interferometry. Appl. Opt., 29:516–521.

ten Brummelaar, T. (1993). Visible light imaging. Technical Report Appendix-K, CHARA Array, Georgia State University, Atlanta, GA.

ten Brummelaar, T. (1994). Taking the twinkle out of the stars: An adaptive wavefront tilt cor rection servo and preliminary seeing study for SUSI. PASP, 106:915+.

ten Brummelaar, T. A. (1995). Differential path considerations in optical stellar interferometry. Appl. Opt., 34:2214–+.

Thom, C., Granes, P., and Vakili, F. (1986). Optical interferometric measurements of Gamma Cassiopeiae’s envelope in the H-alpha line. A&A, 165:L13–L15.

Thompson, A. R., Moran, J. M., and Swenson, G. W. (1986). Interferometry and synthesis in radio astronomy. Wiley-Interscience, New York.

Thompson, A. R., Moran, J. M., and Swenson, G. W. (2001). Interferometry and synthesis in radio astronomy. Interferometry and synthesis in radio astronomy by A. Richard Thompson, James M. Moran, and George W. Swenson, Jr. 2nd ed. New York : Wiley, c2001.xxiii, 692 p. : ill. ; 25 cm. ”A Wiley-Interscience publication.” Includes bibliographical references and indexes. ISBN : 0471254924.

Thompson, R. R. (2002). Spectral Angular Diameters of Mira Variables using Long-Baseline Near-Infrared Interferometry. PhD thesis, University of Wyoming.

Thompson, R. R., Creech-Eakman, M. J., and van Belle, G. T. (2002). Multiepoch Interferometric Study of Mira Variables. I. Narrowband Diameters of RZ Pegasi and S Lacertae. ApJ, 577:447–456.

Torres, G., Boden, A. F., Latham, D. W., Pan, M., and Stefanik, R. P. (2002). Testing Models of Stellar Evolution for Metal-poor Stars: An Interferometric-spectroscopic Orbit for the Binary HD 195987. AJ, 124:1716–1737.

<!-- page 84 of 86 -->

REFERENCES

84

Townes, C. H. (2002). The Potential for Atmospheric Path Length Compensation in Stellar Interferometry. ApJ, 565:1376–1380.

Traub, W. (2002). Recent progress at IOTA with 3 telescopes. In Proc. SPIE Vol. 4838, Interferometry for Optical Astronomy II, Wesley A. Traub Ed., volume 4838.

Traub, W. A. (1988). Polarization Effects in Stellar Interferometers. In NOAO-ESO Conference on High-Resolution Imaging by Interferometry: Ground-Based Interferometry at Visible and Infrared Wavelengths, Garching bei München, Germany, Mar. 15-18, 1988. Edited by F. Merkle, ESO Conference and Workshop Oroceedings No. 29, p.1029, 1988, pages 1029–+.

Treuhaft, R. N., Lowe, S. T., Bester, M., Danchi, W. C., and Townes, C. H. (1995). Vertical scales of turbulence at the Mount Wilson Observatory. ApJ, 453:522+.

Tsuji, T., Ohnaka, K., Aoki, W., and Yamamura, I. (1997). Warm molecular envelope of M giants and Miras: a new molecule forming region unmasked by the ISO SWS. A&A, 320:L1–L4.

Tubbs, R. N., Baldwin, J. E., Mackay, C. D., and Cox, G. C. (2002). Diffraction-limited CCD imaging with faint reference stars. A&A, 387:L21–L24.

Tuthill, P. and Monnier, J. (2000). Imaging and fourier coverage: Mapping with depleted arrays. Technical Report 86, CHARA Array, Georgia State University, Atlanta, GA.

Tuthill, P. G., Danchi, W. C., Hale, D. S., Monnier, J. D., and Townes, C. H. (2000a). Near- and Mid-Infrared Subarcsecond Structure of the Dusty Symbiotic Star R Aquarii. ApJ, 534:907–914.

Tuthill, P. G., Haniff, C. A., and Baldwin, J. E. (1997). Hotspots on late-type supergiants. MNRAS, 285:529–539.

Tuthill, P. G., Haniff, C. A., and Baldwin, J. E. (1999a). Surface imaging of long-period variable stars. MNRAS, 306:353–360.

Tuthill, P. G., Monnier, J. D., and Danchi, W. C. (1999b). A dusty pinwheel nebula around the massive star WR 104. Nature, 398:487–489.

Tuthill, P. G., Monnier, J. D., and Danchi, W. C. (1999c). A Menagerie of Stars: New Images from the Diffraction Limit. In ASP Conf. Ser. 194: Working on the Fringe: Optical and IR Interferometry from Ground and Space, pages 188–+.

Tuthill, P. G., Monnier, J. D., and Danchi, W. C. (2001). A dusty torus around the luminous young star LkHα101. Nature, 409:1012–1014.

Tuthill, P. G., Monnier, J. D., Danchi, W. C., Hale, D. D. S., and Townes, C. H. (2002). Imaging the Disk around the Luminous Young Star LkHα 101 with Infrared Interferometry. ApJ, 577:826–838.

Tuthill, P. G., Monnier, J. D., Danchi, W. C., and Lopez, B. (2000b). Smoke Signals from IRC +10216. I. Milliarcsecond Proper Motions of the Dust. ApJ, 543:284–290.

Tuthill, P. G., Monnier, J. D., Danchi, W. C., Wishnow, E. H., and Haniff, C. A. (2000c). Michelson Interferometry with the Keck I Telescope. PASP, 112:555–565.

Urry, W. L., Thornton, D. D., and Hudson, J. A. (1985). The Hat Creek millimeter-wave hybrid spectrometer for interferometry. PASP, 97:745–751.

Vakili, F., Chesneau, O., Delplancke, F., Jankov, S., Perraut, K., Stehle, C., and Stenflo, J. (2002). Scientific Drivers for a Future Polarimetric Mode for the VLTI: VISPER. In Scientific Drivers for ESO Future VLT/VLTI Instrumentation Proceedings of the ESO Workshop held in Garching, Germany, 11-15 June, 2001. p. 331., pages 331–+.

Vakili, F., Mourard, D., Bonneau, D., Morand, F., and Stee, P. (1997). Subtle structures in the wind of p cygni. A&A, 323:183–188.

Vakili, F., Mourard, D., Stee, P., Bonneau, D., Berio, P., Chesneau, O., Thureau, N., Morand, F., Labeyrie, A., and Tallon-Bosc, I. (1998). Evidence for one-armed oscillations in the equatorial disk of zeta Tauri from GI2T spectrally resolved interferometry. A&A, 335:261–265.

<!-- page 85 of 86 -->

REFERENCES

85

van Belle, G. T., Ciardi, D. R., Thompson, R. R., Akeson, R. L., and Lada, E. A. (2001). Altair’s Oblateness and Rotation Velocity from Long-Baseline Interferometry. ApJ, 559:1155–1164.

van Belle, G. T., Dyck, H. M., Benson, J. A., and Lacasse, M. G. (1996). Angular Size Measurements of 18 Mira Variable Stars at 2.2 (?). AJ, 112:2147–+.

van Belle, G. T., Lane, B. F., Thompson, R. R., Boden, A. F., Colavita, M. M., Dumont, P. J., Mobley, D. W., Palmer, D., Shao, M., Vasisht, G. X., Wallace, J. K., Creech-Eakman, M. J., Koresko, C. D., Kulkarni, S. R., Pan, X. P., and Gubler, J. (1999). Radii and Effective Temperatures for G, K, and M Giants and Supergiants. AJ, 117:521–533.

van Leeuwen, F., Feast, M. W., Whitelock, P. A., and Yudin, B. (1997). First results from HIPPARCOS trigonometrical parallaxes of Mira-type variables. MNRAS, 287:955–960.

Weigelt, G., Balega, Y., Bloecker, T., Fleischer, A. J., Osterbart, R., and Winters, J. M. (1998). 76mas speckle-masking interferometry of IRC+10216 with the SAO 6m telescope: Evidence for a clumpy shell structure. A&A, 333:L51–L54.

Weigelt, G., Mourard, D., Abe, L., Beckmann, U., Chesneau, O., Hillemanns, C., Hofmann, K., Ragland, S. D., Schertl, D., Scholz, M., Stee, P., Thureau, N., and Vakili, F. (2000). GI2T/REGAIN spectro-interferometry with a new infrared beam combiner. In Proc. SPIE Vol. 4006, p. 617-626, Interferometry in Optical Astronomy, Pierre J. Lena; Andreas Quirrenbach; Eds., volume 4006, pages 617–626.

Weigelt, G. P. (1977). Modified astronomical speckle interferometry ’speckle masking’. Optics Communications, 21:55–59.

Weiner, J., Danchi, W. C., Hale, D. D. S., McMahon, J., Townes, C. H., Monnier, J. D., and Tuthill, P. G. (2000). Precision Measurements of the Diameters of α Orionis and o Ceti at 11 Microns. ApJ, 544:1097–1100.

Weiner, J., Hale, D. D. S., and Townes, C. H. (2003). Interferometry on Mira in the Mid-infrared; Cyclic Variability of the Continuum Diameter and the Effect of Spectral Lines on Apparent Size. ApJ(in press).

Whitelock, P. and Feast, M. (2000). Hipparcos parallaxes for Mira-like long-period variables. MNRAS, 319:759–770.

Wiedner, M. C. (1998). Atmospheric water vapour and astronomical millimetre interferometry. PhD thesis, Cambridge University, England.

Wilson, R. W., Baldwin, J. E., Buscher, D. F., and Warner, P. J. (1992). High-resolution imaging of Betelgeuse and Mira. MNRAS, 257:369–376.

Wilson, R. W., Dhillon, V. S., and Haniff, C. A. (1997). The changing face of Betelgeuse. MNRAS, 291:819–+.

Wittkowski, M., Hummel, C. A., Johnston, K. J., Mozurkewich, D., Hajian, A. R., and White, N. M. (2001). Direct multi-wavelength limb-darkening measurements of three late-type giants with the Navy Prototype Optical Interferometer. A&A, 377:981–993.

Wizinowich, P. (1999). Private communication.

Wood, P. R. and Sebo, K. M. (1996). On the pulsation mode of Mira variables: evidence from the Large Magellanic Cloud. MNRAS, 282:958–964.

Woolf, N. J., Smith, P. S., Traub, W. A., and Jucks, K. W. (2002). The Spectrum of Earthshine: A Pale Blue Dot Observed from the Ground. ApJ, 574:430–433.

Ya’Ari, A. and Tuchman, Y. (1996). Long-Term Nonlinear Thermal Effects in the Pulsation of Mira Variables. ApJ, 456:350–+.

Young, J. S., Baldwin, J. E., Boysen, R. C., Haniff, C. A., Lawson, P. R., Mackay, C. D., Pearson, D., Rogers, J., St.-Jacques, D., Warner, P. J., Wilson, D. M. A., and Wilson, R. W. (2000a). New views of Betelgeuse: multi-wavelength surface imaging and implications for models of hotspot generation. MNRAS, 315:635–645.

<!-- page 86 of 86 -->

REFERENCES

86

Young, J. S., Baldwin, J. E., Boysen, R. C., Haniff, C. A., Pearson, D., Rogers, J., St-Jacques, D., Warner, P. J., and Wilson, D. M. A. (2000b). Cyclic variations in the angular diameter of χ Cygni. MNRAS, 318:381–386.