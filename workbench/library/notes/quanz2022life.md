<!-- page 1 of 23 -->

arXiv:2101.07500v4 [astro-ph.EP] 20 Apr 2022

Astronomy & Astrophysics manuscript no. LIFE\_paper\_1\_FINAL\_EITED April 21, 2022

©ESO 2022

# Large Interferometer For Exoplanets (LIFE):

# I. Improved exoplanet detection yield estimates for a large mid-infrared space-interferometer mission

S.P. Quanz$^{1,2,\star}$, M. Ottiger$^{1}$, E. Fontanet$^{1}$, J. Kammerer$^{3,4,22}$, F. Menti$^{1}$, F. Dannert$^{1}$, A. Gheorghe$^{1}$, O. Absil$^{5}$, V.S. Airapetian$^{6}$, E. Alei$^{1,2}$, R. Allart$^{7}$, D. Angerhausen$^{1,2}$, S. Blumenthal$^{8}$, L.A. Buchhave$^{9}$, J. Cabrera$^{10}$, Ó. Carrión-González$^{11}$, G. Chauvin$^{12}$, W.C. Danchi$^{6}$, C. Dandumont$^{13}$, D. Defrère$^{14}$, C. Dorn$^{15}$, D. Ehrenreich$^{16}$, S. Ertel$^{17,18}$ M. Fridlund$^{19,20}$, A. García Muñoz$^{11}$, C. Gascón$^{21}$, J. H. Girard$^{22}$, A. Glauser$^{1}$, J.L. Grenfell$^{10}$, G. Guidi$^{1,2}$, J. Hagelberg$^{16}$, R. Helled$^{15}$, M.J. Ireland$^{4}$, M. Janson$^{23}$, R.K. Kopparapu$^{6}$, J. Korth$^{24}$, T. Kozakis$^{9}$, S. Kraus$^{25}$, A. Léger$^{26}$, L. Leedjärv$^{27}$, T. Lichtenberg$^{8}$, J. Lillo-Box$^{28}$, H. Linz$^{29}$, R. Liseau$^{20}$, J. Loicq$^{13}$, V. Mahendra$^{30}$, F. Malbet$^{12}$, J. Mathew$^{4}$, B. Mennesson$^{31}$, M.R. Meyer$^{32}$, L. Mishra$^{33,16,2}$, K. Molaverdikhani$^{29,34}$, L. Noack$^{35}$, A.V. Oza$^{31,33}$, E. Pallé$^{36,37}$, H. Parviainen$^{36,37}$, A. Quirrenbach$^{34}$, H. Rauer$^{10}$, I. Ribas$^{21,38}$, M. Rice$^{39}$, A. Romagnolo$^{40}$, S. Rugheimer$^{8}$, E.W. Schwieterman$^{41}$, E. Serabyn$^{31}$, S. Sharma$^{42}$, K.G. Stassun$^{43}$, J. Szulágyi$^{1}$, H.S. Wang$^{1,2}$, F. Wunderlich$^{10}$, M.C. Wyatt$^{44}$, and the LIFE Collaboration$^{45}$

(Affiliations can be found after the references)

Received: &lt;date&gt; / Accepted: &lt;date&gt;

## ABSTRACT

Context. One of the long-term goals of exoplanet science is the atmospheric characterization of dozens of small exoplanets in order to understand their diversity and search for habitable worlds and potential biosignatures. Achieving this goal requires a space mission of sufficient scale that can spatially separate the signals from exoplanets and their host stars and thus directly scrutinize the exoplanets and their atmospheres.

Methods. We have developed an instrument simulator that considers all major astrophysical noise sources and coupled it with Monte Carlo simulations of a synthetic exoplanet population around main-sequence stars within 20 pc of the Sun. This allows us to quantify the number (and types) of exoplanets that our mission concept could detect. Considering single visits only, we discuss two different scenarios for distributing 2.5 years of an initial search phase among the stellar targets. Different apertures sizes and wavelength ranges are investigated.

Results. An interferometer consisting of four 2 m apertures working in the 4–18.5  $\mu$ m wavelength range with a total instrument throughput of 5% could detect up to  $\approx$ 550 exoplanets with radii between 0.5 and 6 R $_{\oplus}$  with an integrated S/N $\geq$ 7. At least  $\approx$ 160 of the detected exoplanets have radii  $\leq$ 1.5 R $_{\oplus}$ . Depending on the observing scenario,  $\approx$ 25–45 rocky exoplanets (objects with radii between 0.5 and 1.5  $\oplus$ ) orbiting within the empirical habitable zone (eHZ) of their host stars are among the detections. With four 3.5 m apertures, the total number of detections can increase to up to  $\approx$ 770, including  $\approx$ 60–80 rocky eHZ planets. With four times 1 m apertures, the maximum detection yield is  $\approx$ 315 exoplanets, including  $\leq$ 20 rocky eHZ planets. The vast majority of small, temperate exoplanets are detected around M dwarfs. The impact of changing the wavelength range to 3–20  $\mu$ m or 6–17  $\mu$ m on the detection yield is negligible.

Conclusions. A large space-based MIR nulling interferometer will be able to directly detect hundreds of small, nearby exoplanets, tens of which would be habitable world candidates. This shows that such a mission can compete with large single-aperture reflected light missions. Further increasing the number of habitable world candidates, in particular around solar-type stars, appears possible via the implementation of a multi-visit strategy during the search phase. The high median S/N of most of the detected planets will allow for first estimates of their radii and effective temperatures and will help prioritize the targets for a second mission phase to obtain high-S/N thermal emission spectra, leveraging the superior diagnostic power of the MIR regime compared to shorter wavelengths.

Key words. Telescopes – Techniques: interferometric – Infrared: planetary systems – Techniques: high angular resolution – Methods: numerical – Planets and satellites: detection – Planets and satellites: terrestrial planets

## 1. Introduction

One of the major objectives of exoplanet science is the atmospheric characterization of a statistically relevant sample of small exoplanets. Specific emphasis will be on temperate terrestrial planets to investigate whether there are other worlds similar to Earth that may harbor life. While occurrence rates of Earth-like planets around solar-type stars are still somewhat uncertain

(e.g., Bryson et al. 2021), thanks to transiting exoplanet discovery missions such as Kepler (Borucki et al. 2010) and the Transiting Exoplanet Survey Satellite (TESS; Ricker et al. 2015) and ongoing long-term radial velocity (RV) surveys, we know that, statistically, planets with radii and masses comparable to or slightly larger than those of Earth and with shorter orbital periods are very abundant (e.g., Mayor et al. 2011; Tuomi et al. 2019; Kunimoto & Matthews 2020; Bryson et al. 2021). Some major detections were even made within 20 pc of the Sun with

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">\* Correspondence: sascha.quanz@phys.ethz.ch.</span></small>

Article number,

page 1 of 23

<!-- page 2 of 23 -->

A&A proofs: manuscript no. LIFE\_paper\_1\_FINAL\_EITED

both transit searches (e.g., Berta-Thompson et al. 2015; Vander-spek et al. 2019; Gillon et al. 2017; Gillon et al. 2017) and RV surveys (e.g., Anglada-Escudé et al. 2016; Ribas et al. 2016; Jeffers et al. 2020; Astudillo-Defru et al. 2017; Díaz et al. 2019; Zechmeister et al. 2019), with RV planets typically being closer to the Sun because of the geometric bias of transiting planets.

Going forward, and focusing on the atmospheric characterization of small planets, the James Webb Space Telescope (JWST) might reveal whether some of these objects transiting nearby M dwarfs have managed to retain their atmospheres (e.g., Koll et al. 2019) despite the high level of activity of their host stars, in particular at younger ages (e.g., Ribas et al. 2016; MacGregor et al. 2018; Johnstone et al. 2019); an in-depth investigation of atmospheric constituents with JWST seems, however, rather challenging (e.g., Kreidberg & Loeb 2016; Morley et al. 2017; Krissansen-Totton et al. 2018). The Atmospheric Remote-sensing Infrared Exoplanet Large-survey mission (Ariel; Tinetti et al. 2018) of the European Space Agency (ESA) will provide transmission and emission spectra of hundreds of exoplanets, but the focus will be on objects with hot or warm hydrogen-dominated atmospheres; only a few small, relatively hot exoplanets will be studied. Upgraded or new fully optimized instruments at existing 8-meter-class ground-based telescopes may have a chance of directly detecting the nearest small exoplanet, Proxima Cen b (e.g., Lovis et al. 2017). Due to their unprecedented spatial resolution and sensitivity, the upcoming 30–40 m ground-based extremely large telescopes (ELTs) will be powerful enough to directly detect small planets around the nearest stars. Instruments working at mid-infrared (MIR) wavelengths, such as the Mid-infrared ELT Imager and Spectrograph (METIS; Brandl et al. 2018; Brandl et al. 2021), will detect the thermal emission of the planets (Quanz et al. 2015; Bowens et al. 2021). Instruments working at optical or near-infrared (NIR) wavelengths and featuring high-resolution spectrographs coupled with adaptive optics systems, such as the Planetary Camera and Spectrograph (PCS; Kasper et al. 2021) and the High Resolution Spectrograph (HIRES; Marconi 2020), aim at detection in reflected light.

Unfortunately, none of the currently planned ground-based instrument projects and approved space missions is capable of investigating in detail the atmospheres of several dozen small exoplanets, including a sizable subsample residing in or close to the so-called habitable zone (HZ) of their host stars (Kasting et al. 1993; Kopparapu et al. 2013). This is one of the reasons why, in the context of the Astrophysics Decadal Survey in the United States, new flagship missions, the Habitable Exoplanet Observatory (HabEx; Gaudi et al. 2020) and the Large UV/Optical/IR Surveyor (LUVOIR; The LUVOIR Team 2019), are currently under assessment; one of their main science drivers is the direct detection and characterization of temperate terrestrial exoplanets in reflected light $^{1}$ .

Here, we focus on a different observational approach and a new initiative that aims at developing a space-based MIR nulling interferometer capable of detecting and characterizing the thermal emission of (temperate) rocky exoplanets. The characterization of temperate exoplanets in the MIR was recently announced to be a potential science theme for a future science

mission within ESA's Voyage 2050 program$^{2}$. The idea to employ interferometric nulling for exoplanet science was originally proposed by Bracewell (1978) and later followed up in Leger et al. (1995) and Angel & Woolf (1997); in the late 1990s to mid 2000s, concept studies were carried out by both ESA and NASA: the Darwin mission and the Terrestrial Planet Finder - Interferometer (TPF-I) mission, respectively. In the end, these concepts did not go forward for implementation because of technical challenges, but also because our understanding of the exoplanet population was significantly more limited. This has, however, changed. Given the enormous scientific progress in exoplanet research since the mid 2000s and significant advances related to key technologies, it is time to reassess such a mission concept and quantify its potential scientific return. In 2018, a first such study was published (Kammerer & Quanz 2018), which investigated the exoplanet detection yield of a space-based MIR nulling interferometer based on exoplanet occurrence rates from NASA's Kepler mission; it claimed that a few hundred small exoplanets (radii between 0.5 and $6\mathrm{R}_{\oplus}$) could be within reach for such an instrument. These promising results, in combination with ongoing lab activities related to nulling interferometry, resulted in the creation of the Large Interferometer For Exoplanets (LIFE) initiative$^{3}$.

The present paper is the first in a series of papers currently in preparation. It is assumed that a mission such as LIFE would consist of two main phases: (1) a search phase to directly detect a large sample of exoplanets orbiting nearby stars and (2) a characterization phase to reobserve a subsample of these exoplanets and investigate their properties and atmospheres in detail. In the following, we focus on the search phase and quantify how many exoplanets LIFE would be able to detect depending on different mission parameters. Future work will focus more on the characterization phase of the mission, including questions related to atmospheric diversity and evolution, habitability, and the search for indications of biological activity. In this context, the MIR wavelength regime offers complementary information and even several advantages compared to studies at optical or NIR wavelengths. These include more direct constraints on the temperature and size of the objects and a large set of molecular absorption lines of main atmospheric species, including biosignatures (e.g., Schwieterman et al. 2018; Catling et al. 2018), some of which, for example  $CH_{4}$ , might be easier to detect in the MIR than at shorter wavelengths.

In comparison to previous studies that quantify the detection yield of an MIR nulling interferometer (e.g., Kammerer & Quanz 2018; Quanz et al. 2018, 2021), we have significantly updated and improved our simulation approach as further described below. Similar detection yield analyses were carried out for the reflected light missions mentioned above, enabling a direct comparison of the different mission concepts.

We note that in the ideal case, exoplanet surveys with existing and future high-precision RV instruments (e.g., CARMENES, NIRPS, ESPRESSO, MAROON-X, HARPS3, and EXPRES) will continue to uncover a significant fraction of the exoplanet population within 20 pc, including rocky, potentially habitable, planets $^{4}$ . In this case, the search phase of future direct detection exoplanet missions would be shortened and more of the limited observing time could be allotted to the char-

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">$^{1}$  We note that during the refereeing process of this paper, the Consensus Study Report “Pathways to Discovery in Astronomy and Astrophysics for the 2020s” was published by the National Academies of Sciences, Engineering, and Medicine recommending a large ( $\sim$ 6 m aperture) infrared/optical/ultraviolet (IR/O/UV) space telescope as a future flagship mission (National Academies of Sciences & Medicine 2021).</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">2 https://www.cosmos.esa.int/web/voyage-2050</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">3 www.life-space-mission.com</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">$^{4}$  As an alternative to ground-based RV searches, space-based high-precision astrometry missions could be envisioned (e.g., Malbet & Sozzetti 2018; Janson et al. 2018).</span></small>

Article number, page 2 of 23

<!-- page 3 of 23 -->

Quanz et al.: LIFE: I. Improved exoplanet detection yield estimates for a MIR space interferometer

acterization of the objects. Whether in the end the low-amplitude RV signals from Earth-like planets can be separated from astrophysical noise sources, such as stellar jitter (e.g., Oshagh et al. 2017), and to what extent, consequently, those RV surveys will be complete, remains to be seen.

In Sect. 2 we describe in detail the setup of our yield simulations. The results are presented in Sect. 3, and we discuss them in Sect. 4. We conclude and summarize our main findings in Sect. 5.

## 2. Setup of yield simulations

The general approach of our Monte Carlo-based yield simulations is described in Kammerer & Quanz (2018), but we have implemented several updates as detailed in the following.

## 2.1. Stellar target catalog

We used a new LIFE target star catalog that includes single main-sequence stars and wide separation binaries of spectral types FGKM out to 20 pc of the Sun. While the catalog includes a total of 1732 objects, only a subset was considered for the simulations of the search phase depending on the optimization strategy (see Sect. 2.6 for details). The catalog and its creation are further explained in Appendix A.

## 2.2. Exoplanet population

In our simulations we generated an artificial population of exoplanets around the stars in our target catalog and did not consider any known exoplanets. The underlying exoplanet occurrence rates as a function of the radius and orbital period follow the results from NASA's ExoPaG SAG13 (Kopparapu et al. 2018) for single FGK stars and Dressing & Charbonneau (2015) for single M stars. This allows for a comparison with the results obtained in the context of the HabEx and LUVOIR studies mentioned above, which used a very similar underlying exoplanet population. Binary stars with measured (apparent) separations greater than 50 AU were treated as single stars. For binary systems with smaller separations, the occurrence rates were scaled down by a factor of 0.3 over the entire period and radius range (cf. Kraus et al. 2016). We focused our analysis on planets with radii, $R_{\mathrm{p}}$, in the range $0.5R_{\oplus} \leq R_{\mathrm{p}} \leq 6R_{\oplus}$ for FGK stars and $0.5R_{\oplus} \leq R_{\mathrm{p}} \leq 4R_{\oplus}$ for M stars. Orbital periods, $P_{\mathrm{P}}$, in the range $0.5d \leq P_{\mathrm{P}} \leq 500d$ and $0.5d \leq P_{\mathrm{P}} \leq 200d$ were considered for FGK and M stars, respectively. Cold, Neptune-, or Jupiter-like objects with separations $\geq 3$ au, for which the SAG13 statistics cannot be applied (cf. Dulz et al. 2020) and which were included in the HabEx and LUVOIR studies, were not considered as they are typically too cold for a detection within a reasonable amount of integration time. All planets were assumed to have circular orbits and were assigned a random Bond albedo, $A_{\mathrm{B}} \in [0, 0.8)^{5}$, and a geometric albedo, $A_{\mathrm{g}} \in [0, 0.1)^{6}$, that is constant over the wavelength range we consider (cf. Kammerer & Quanz 2018). Both albedos were uniformly distributed in the considered intervals. The planets were treated as black bodies with their whole surface area radiating with an equilibrium temperature ($T_{\mathrm{eq}}$) determined by the luminosity of their host star, their Bond albedo, and their orbital separation.

In Table 1 we define two types of exoplanets that are important throughout the paper: rocky planets orbiting within the empirical habitable zone (eHZ) and exo-Earth candidates (EECs). We also provide the respective occurrence rates as provided by our exoplanet population.

## 2.3. Simulating spacecraft, instrument, and noise sources with LIFESIM

In order to estimate the signal-to-noise ratio (S/N) of our simulated exoplanets we have developed the new simulation tool LIFESIM (Dannert et al. 2022). This tool enables us to simulate the temporally modulated signal that a planetary system would leave in an observing sequence with a space-based nulling interferometer (cf. Lay 2005) and further includes the most relevant – and wavelength-dependent – astrophysical noise sources. This is an important difference from our earlier exoplanet detection yield estimates, where, instead of explicitly simulating the interferometer transmission and signal modulation for every simulated planet, constraints on the inner working angle of the instrument and sensitivity were used to assess the discovery potential (Kammerer & Quanz 2018; Quanz et al. 2018).

![Image block](doc:52385f0/tier:standard/page:3/block:13)

Fig. 1. Artist's impression of the LIFE nulling-interferometry mission, consisting of four collector spacecraft in a rectangular array configuration sending light to a beam combiner spacecraft in the center. The present analysis assumes an X-array configuration with a baseline ratio of 6:1.

In the following, we considered an interferometer consisting of four collector spacecraft in a so-called X-array configuration that feed their beams into a fifth beam combiner spacecraft located in their center (see Fig. 1).

page 3 of 23

The ratio between the long and the short baseline of the X-array was assumed to be 6:1 for the time being and a $\pi/2$ phase shift was applied between two conjugated transmission maps (cf. Defrère et al. 2010). The short baselines of the array are referred to as “nulling baselines” and are responsible for creating the central dark fringe that nulls the host star. The long baselines are referred to as “imaging baselines” and are responsible for a higher-frequency modulation of the transmission map perpendicular to the fringe pattern created by the nulling baselines. The resulting modulation map, the difference between the two conjugate transmission maps, effectively suppresses the signal coming from any centrally symmetric source (such as emission from optically thin and smooth exozodiacal dusk disks with random inclination) so that only the shot noise of the source contributes to the S/N of the observations. The 6:1 baseline ratio has been shown to be more robust against instability noise compared to a 2:1 baseline ratio (Lay 2006), but additional trade-off studies are needed to further validate this choice. A detailed description of LIFESIM is pro-

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">$^{5}$  For reference, the Bond albedos of Venus and Mercury are  $\approx0.8$  and  $\approx0.1$ , respectively, bracketing the values for the Solar System planets.</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">$^{6}$  These low values are motivated by the MIR wavelength range we are considering.</span></small>

Article number,

<!-- page 4 of 23 -->

A&A proofs: manuscript no. LIFE\_paper\_1\_FINAL\_EITED

Table 1. Types of exoplanets that are of particular importance throughout the paper. The first row shows our definition of a rocky planet orbiting within the empirical habitable zone (eHZ). The second row defines exo-Earth candidates (EECs) as used in the yield estimates for HabEx and LUVOIR. The last columns summarize the occurrence rates for these objects as provided by the assumed exoplanet population.

<table><tr><td rowspan="2">Planet type</td><td rowspan="2"> $R_{\text{P}}$  [R $_{\oplus}$ ]</td><td rowspan="2">Stellar flux range [S $_{\oplus}$ ]</td><td colspan="2">Occurrence rates $^a$ </td></tr><tr><td>M stars</td><td>FGK stars</td></tr><tr><td>Rocky eHZ</td><td>0.5 – 1.5</td><td>1.776 – 0.32 $^b$ </td><td>0.558</td><td>0.370</td></tr><tr><td>Exo-Earth Candidates (EECs)</td><td>0.82 / 0.62 $^c$  – 1.4</td><td>1.107 – 0.356 $^d$ </td><td>0.312</td><td>0.164</td></tr></table>

Notes. $^{(a)}$ Occurrence rates are values for single stars averaged over our input catalog for the given range of spectral types. Because the stellar flux range is spectral type dependent, the number of objects falling within this range, and hence the occurrence rates, varies with spectral type as well. $^{(b)}$ The flux range is given by the “recent Venus” and “early Mars” limits and is spectral type dependent (Kopparapu et al. 2014). The values given here correspond to 1 M$_{\oplus}$ planet orbiting a solar twin. We note that both limits take into account the luminosity evolution of the Sun, which was fainter during the epochs when Venus and Mars provided habitable conditions. For present-day solar luminosity, these insolation limits correspond to separations of 0.75 and 1.77 au, respectively, excluding Venus from, but including Mars in, the eHZ. $^{(c)}$ For EECs, the lower limit of the radius range depends on the separation from the star; closer to the star, planets are required to have a larger radius. This can be described by $R_{\mathrm{P}}^{\mathrm{min}} = 0.8 \cdot S^{0.25}$, where $S$ is the insolation. The $HabEx$ and $LUVOIR$ studies focused primarily on solar-type stars and used a corresponding expression based on the semimajor axis, $a$, i.e., $R_{\mathrm{P}}^{\mathrm{min}} = 0.8 \cdot a^{-0.5}$. As we are also interested in M stars, we had to convert this into an expression for $S$. $^{(d)}$ The flux range is given by the “runaway greenhouse” and “maximum greenhouse” limits and is spectral type dependent (Kopparapu et al. 2014). The values given here correspond to a 1 M$_{\oplus}$ planet orbiting a solar twin.

vided in Dannert et al. (2022), but we refer the reader to Defrère et al. (2010) for a description of the general nulling and beam combination scheme and the resulting final modulation map for an X-array interferometer.

In our simulations we assumed that for each new target star the array is reconfigured so that the center of the projected eHZ (cf. Table 1; Sect. 2.2) falls within the first transmission maximum of the nulling baselines at a reference wavelength of  $15 \mu m$ . However, we imposed a minimum separation between two adjacent collector spacecraft of at least 10 m and allow for a maximum separation of 600 m. Initial tests had shown that having the reference wavelength between 15 and  $20 \mu m$  resulted in comparable detection yields, but that shorter (e.g.,  $10 \mu m$ ) or longer (e.g.,  $25 \mu m$ ) reference wavelengths provided lower yield numbers. Keeping the baseline lengths of the configuration in mind (from a technical perspective), we decided to use  $15 \mu m$  as reference for all analyses presented in the following. The aperture diameter D of the collector spacecraft is a free parameter in our instrument model, and we discuss the impact of aperture size on the results in Sect. 3.2. For the computation of the total photon flux received by the collector spacecraft we ignored any possible obscuration from a secondary mirror. To be conservative, we assumed  $5\%^{7}$  for the optical throughput of the instrument, but will update this number when the concept for the optical layout is maturing. In earlier studies in the context of the Darwin/TPF-I missions a throughput of 10% was assumed (e.g., Lay et al. 2007; Defrère et al. 2010) and also at the Large Binocular Telescope Interferometer (LBTI) the most recent estimate for the optical throughout around  $\sim11 \mu m$  is  $\approx0.11$  (S. Ertel, private communication). For the detector quantum efficiency, we assumed 70% over the full wavelength range, which is identical to the Darwin studies mentioned above. Recent experiments with 15-micron-cutoff HgCdTe detector arrays have yielded quantum efficiencies of  $\gtrsim0.8$  between 6 and  $12 \mu m$  wavelengths (Cabrera et al. 2020) and the Si:As IBC detectors of the JWST/MIRI instrument achieve  $\gtrsim0.7$  between 12 and  $20 \mu m$  (Rieke et al. 2015).

At the moment, our S/N calculations are photon-based and include all major astrophysical noise terms. We implicitly assumed that our measurements would not be limited by instrumental effects (see Sect. 2.7 below for the definition of our de-

tection criterion). The impact of phase and/or amplitude variations as major systematic noise sources is currently being assessed. Also, thermal background from the aperture mirrors and the instrument optics, and detector-related noise sources will be included in subsequent work. For the mirrors of the collector spacecraft and the instrument optics not to contribute significantly to the measurement implies a required temperature of  $\lesssim40$  K (Defrère et al. 2010). Noise terms that were explicitly included are:

Photon noise from the simulated planets: Given the distance, radius, and equilibrium temperature of our simulated planets, their photon flux (assuming black-body emission) and related noise are fully described.

Photon noise from stellar leakage: Depending on the distance to the star, its radius, and the length of the nulling baseline, a small fraction of stellar photons may “leak” through the central dark fringe and hence contribute to the photon noise.

Photon noise from exozodi disks: For each simulated planetary system we randomly assigned a level of emission from a dusty exozodi disk following the observed (nominal) distribution from the Hunt for Observable Signatures of Terrestrial Systems (HOSTS) survey (Ertel et al. 2018, 2020). To compute the spectral energy distribution (SED) of the exozodi disk we used the publicly available code from Kennedy et al. (2015). All exozodi disks were assumed to be optically thin, smooth (i.e., without any substructure) and seen face-on. We refer the reader to Sect. 4.3.2 for a discussion about these assumptions.

Photon noise from local zodiacal light: The optically thin zodiacal dust in our Solar System is a source of significant MIR emission. In LIFESIM the surface brightness is described by a pointing-dependent 2D model originally developed for the Darwin simulator and based on data from Cosmic Background Explorer (COBE; Kelsall et al. 1998). Compared to the original COBE data, the model slightly over-predicts the flux in the $6 - 20\mu \mathrm{m}$ range and for a pointing direction with a relative latitude of more than $90^{\circ}$ from the Sun by $10 - 20\%$. For wavelengths shorter than $6\mu \mathrm{m}$ the difference increases to a factor of 2-3 at $3\mu \mathrm{m}$. However, at these shorter wavelengths the total photon noise is strongly dominated (up to several orders of magnitude) by the contribution from stellar leakage. In our simulations we assumed that we always

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">$^{7}$  This 5% throughput is applied to the modulation maps, which already contain only 50% of the incoming light.</span></small>

Article number, page 4 of 23

<!-- page 5 of 23 -->

Quanz et al.: LIFE: I. Improved exoplanet detection yield estimates for a MIR space interferometer

point in anti-sunward direction (LIFE will be launched to the Earth-Sun L2 point) but considered the true latitude of the target star.

In our S/N calculations we implicitly assumed that the combined beams are fed through single-mode fibers before the signal is spectrally dispersed. The effective field-of-view (FoV) of the fibers, and hence of each collector spacecraft, is wavelength dependent and given by  $\lambda/D$ .

In Fig. 2 we show an example of how the various noise terms compare to the incoming photon flux from a  $1 R_{\oplus}$  exoplanet with an effective temperature of 276 K orbiting at 1 au from a Sun-like star at 10 pc distance. The system is assumed to be located within the ecliptic and contains an exozodi disk with the same brightness as the zodiacal light in the Solar System.

![Chart block](doc:52385f0/tier:standard/page:5/block:5)

Fig. 2. Example illustrating the photon flux and noise contributions from the various astrophysical sources in our nulling-interferometry simulations: exoplanet flux (1 R$_{\oplus}$ and 276 K effective temperature located at 10 pc; dashed red line), flux from a Sun-like star (black line with stars), local zodiacal light (green line with ticks), and exozodi (1 zodi; solid blue line). The corresponding photon noise contributions (1-σ) are shown with the same color code, but as dotted lines.

## 2.4. Mission parameters

Assuming a total mission lifetime of 5-6 years, we assigned an available on-source observing time of 2 years to the initial search phase. This translates into 2.5 years of mission time considering 25% of general mission overhead; the remaining time of the mission is dedicated to detailed follow-up observations of a subset of the detected exoplanets and possibly an ancillary science program. The slew time from one target to the next was fixed to 10 hours, which is part of the 2 year observing time. For the moment we only considered single visits of target stars during the survey.

## 2.5. Setup of Monte Carlo simulations

To create the exoplanet population we used the freely available P-Pop Monte Carlo tool $^{8}$ , which for each star of the target catalog randomly draws exoplanets from the distributions described above (cf. Kammerer & Quanz 2018) and puts them at random

positions along their orbits. The orbital inclination was also randomly chosen for each system, but planets in multi-planet systems were assumed to be co-planar. To ensure that multi-planet systems were dynamically stable we applied a stability criterion following the approach by He et al. (2019) that is based on the mutual Hill radius of neighboring planets. Specifically, for circular orbits as assumed here, a system was considered stable if for all planet pairs within the system

$$
\Delta = \frac {a _ {o u t} - a _ {i n}}{R _ {H}} > 8,
$$

where $a_{out}$ and $a_{in}$ are the semimajor axes of the outer and inner planet, respectively, and $R_{H}$ is the mutual Hill radius given by

$$
R _ {H} = \frac {a _ {i n} + a _ {o u t}}{2} \left[ \frac {m _ {i n} + m _ {o u t}}{3 M _ {*}} \right] ^ {1 / 3},
$$

with $m_{in}$ and $m_{out}$ being the mass of the inner and outer planet, respectively, and $M_*$ being the mass of the host star. If a system or pair of planets was unstable, we re-drew the system, which happened in less than 2% of the cases. In total, we generated 500 planetary systems per target star. All planets were then run through LIFESIM in order to compute their photon fluxes as well as the photon noise from the various sources listed above.

## 2.6. Distribution of observing time: Two scenarios

We considered two scenarios that determine the distribution of the available on-source observing time of 2 years: maximizing the total number of detected exoplanets (scenario 1) or the number of rocky exoplanets orbiting within the eHZ of their host star (scenario 2; see Table 1 for definition). We note that the eHZ includes a much larger range of insolations than the “classical” HZ (Kasting et al. 1993; Kopparapu et al. 2013), but a much smaller range than the “extended hydrogen” HZ (Pierrehumbert & Gaidos 2011), which is estimated to reach  $\approx10$  au ( $\approx0.01~S_{\oplus}$ ) for a G-type star. Depending on the main science goals of LIFE, one may prefer either of the two scenarios, but, as we will see below, maximizing the number of temperate, rocky exoplanets (scenario 2) leads to a decrease in the total number of detectable planets (scenario 1).

The algorithm to distribute the observing time was similar to the one discussed in Lay et al. (2007) and considered that for each star in a given Monte Carlo run one can compute the detection efficiency (defined as number of detected planets per time interval $\delta t$). The number of detected planets depends on the threshold one puts on the S/N of the planets, which in turn depends on the assumed aperture size of the collector spacecraft and the assumed length of $\delta t$ (in our analysis we assumed $\delta t = 1\mathrm{h}$). Also, one can decide which subset of planets to focus on (i.e., scenario 1 or scenario 2). By computing the number of detectable planets for all stars and over a sufficiently large range of time intervals, one can identify the star that offers the maximum possible detection yield for the smallest time interval. This star and the corresponding planet(s) as well as the length of the required time interval were saved, and the star offering the second best detection efficiency was searched. We repeated this process until the available observing time (including the $10\mathrm{h}$ slew time from one star to the next) was used up. This yielded the total number of detectable planets per star as well as a rank-ordered list of target stars based on their expected contribution to the detection yield. We then calculated the gain (i.e., planet yield per time) as an average over all 500 Monte Carlo realizations for each star. This allowed us to construct an observing sequence,

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">8 https://github.com/kammerje/P-pop</span></small>

Article number,

page 5 of 23

<!-- page 6 of 23 -->

A&A proofs: manuscript no. LIFE\_paper\_1\_FINAL\_EDITED

![Chart block](doc:52385f0/tier:standard/page:6/block:2)

![Chart block](doc:52385f0/tier:standard/page:6/block:3)

Fig. 3. Total exoplanet detection yield from our reference case scenario simulations ($D = 2\mathrm{m}$; $\lambda = 4 - 18.5\mu m$) in the radius vs. stellar insolation plane. The plots show the number of expected planet detections per grid cell, including the statistical $1 - \sigma$ uncertainty from the Monte Carlo approach but excluding uncertainties in the exoplanet occurrence rates. Left panel: Scenario 1 (search phase optimized for maximizing the total number of exoplanets). Right panel: Scenario 2 (search phase optimized for maximizing the number of rocky eHZ exoplanets.)

which yielded the final average numbers we are quoting below. For completeness we note that in this analysis we implicitly assumed that the X-array of the collector spacecraft did an integer number of full rotations around its center irrespective of the assumed integration time. This allowed for an easier computation of the exoplanets' signals passing through the interferometer's modulation map (Dannert et al. 2022).

## 2.7. Detection criterion

In the following, we required a  $S/N \geq 7$  spectrally integrated over the full wavelength range for a planet to be considered a detection. This choice compensates for the lack of an instrumental noise model in the current simulations. Under the assumptions that the instrumental noise contribution is equal to or lower than the astrophysical noise and that the total noise can be written as the square root of the sum of the instrumental and astrophysical noise (i.e.,  $\sigma_{tot} = \sqrt{(\sigma_{inst})^{2} + (\sigma_{astro})^{2}}$ ), a total  $S/N \geq 7$  corresponds to an astrophysical signal of  $S/N_{astro} \geq 5$ .

As we were only considering photon noise, we verified that (slightly modified versions of) published signal extraction algorithms for nulling-interferometry data (e.g., Thiébaut & Mugnier 2006; Mugnier et al. 2006) actually achieve a performance close to the ideal photon-noise limited case and can also be applied to multi-planet systems (Dannert et al. 2022).

## 3. Results

For the two scenarios outlined in Sect. 2.6, we chose an aperture size of $D = 2$ m as our reference case, but we also investigated cases with $D = 1$ m and $D = 3.5$ m (the latter corresponding to the aperture of ESA's Herschel spacecraft, the largest monolithic infrared space telescope ever launched). Besides using 4–18.5 $\mu$m as wavelength range in the reference case, we also computed detection yields for 3–20 $\mu$m and 6–17 $\mu$m. We note that for determining the final wavelength range not only the expected detection yield during a 2.5-year search phase should be considered, but also the scientific importance of molecular bands for atmospheric characterization at the short and long wavelength end (Konrad et al. 2021) and technical aspects. We remind the

reader that in all cases the assumed instrument throughput is $5\%$ (see Sect. 2.3).

## 3.1. Exoplanet yield of reference case scenarios

In Fig. 3 we show the expected number of detectable exoplanets and the standard deviation resulting from our 500 Monte Carlo runs in the radius versus stellar insolation plane for the reference case setup and the two scenarios described in Sect. 2.6. Figure 4 is based on the same information, but this time we follow the exoplanet classification scheme introduced by Kopparapu et al. (2018) (see Table 2). This scheme was also used in the final study reports by the LUVOIR and HabEx teams (The LUVOIR Team 2019; Gaudi et al. 2020), which allows for an easier comparison between the different mission concepts. A current short-coming is that the scheme assumes a Sun-like host star. Variations in the host star SED could potentially alter the stellar flux condensation boundaries of the considered chemical species by a few percent. A more robust analysis with different host stellar spectral types, including M dwarfs, is needed to correct this. We note that in Fig. 4, we also show the number of terrestrial exoplanets located within the eHZ as defined in Sect. 2.6. for comparison with the other classes of exoplanets. It is important to keep in mind that in all cases the number of detectable exoplanets as a function of their radius and received insolation is influenced by both the assumed underlying exoplanet population and our technical assumptions.

These plots show that within the present simulation framework, LIFE would discover hundreds of nearby exoplanets, the vast majority of which have radii between 0.5 and $3\mathrm{R}_{\oplus}$. It also shows that the choice of observing scenario has a significant impact on the planet yield: on the one hand the number of rocky exoplanets orbiting within the eHZ can indeed be significantly increased by a factor of $\approx 1.6$ if one optimizes the observing strategy accordingly (scenario 2). For EECs (see Table 1) it is even a factor of $\approx 2$. However, this comes at a price as the resulting total number of detectable exoplanets is significantly smaller compared to scenario 1 ($\approx 350$ vs. $\approx 550$). Because of their moderate temperatures, rocky exoplanets in the eHZ are fainter than objects orbiting closer to the star and require larger amounts of

Article number, page 6 of 23

<!-- page 7 of 23 -->

Quanz et al.: LIFE: I. Improved exoplanet detection yield estimates for a MIR space interferometer

![Chart block](doc:52385f0/tier:standard/page:7/block:2)

![Chart block](doc:52385f0/tier:standard/page:7/block:3)

Fig. 4. Total exoplanet detection yield from our reference case scenario simulations ($D = 2\mathrm{m}$; $\lambda = 4 - 18.5\mu m$) using the planet classification scheme introduced by Kopparapu et al. (2018) (see Table 2). For comparison, we also plot the number of terrestrial exoplanets within the eHZ as defined in Sect. 2.6 as the leftmost bar labeled “Rocky eHZ.” The bars show the number of expected planet detections, including the statistical $1 - \sigma$ uncertainty from the Monte Carlo approach but excluding uncertainties in the exoplanet occurrence rates. Left panel: Scenario 1, i.e., the search phase is optimized for maximizing the total number of exoplanets. Right panel: Scenario 2, i.e., the search phase is optimized for maximizing the number of rocky eHZ exoplanets.

![Chart block](doc:52385f0/tier:standard/page:7/block:5)

![Chart block](doc:52385f0/tier:standard/page:7/block:6)

Fig. 5. Total exoplanet detection yield from our reference case scenario simulations ($D = 2\mathrm{m}$; $\lambda = 4 - 18.5\mu m$) shown as a function of spectral type of the host star (left panel: Scenario 1; right panel: Scenario 2). The bars show the number of expected planet detections, including the statistical $1 - \sigma$ uncertainty from the Monte Carlo approach but excluding uncertainties in the exoplanet occurrence rates. In both panels, the green bars (labeled “Rocky HZ”) show the number of rocky eHZ exoplanets, which are a subset of the planets in the $0.5 - 1.5\mathrm{R}_{\oplus}$ bin in Fig. 3.

Table 2. Exoplanet classification scheme introduced by Kopparapu et al. (2018). Together with the planet types defined in Table 1, we apply this scheme in Figs. 4, 8, 9, and 14, as well as in Figs. C.3 and C.6 in Appendix C. For reference, Venus would be classified as a “hot, rocky” planet and Earth and Mars as “warm, rocky” planets.

<table><tr><td rowspan="2">Planet type</td><td rowspan="2"> $R_{\text{P}}$  [ $R_{\oplus}$ ]</td><td colspan="3">Stellar flux range [ $S_{\oplus}$ ]</td></tr><tr><td>Hot</td><td>Warm</td><td>Cold</td></tr><tr><td>Rocky</td><td>0.5 – 1</td><td>182 – 1.0</td><td>1.0 – 0.28</td><td>0.28 – 0.0035</td></tr><tr><td>Super-Earths</td><td>1 – 1.75</td><td>187 – 1.12</td><td>1.12 – 0.30</td><td>0.30 – 0.0030</td></tr><tr><td>Sub-Neptunes</td><td>1.75 – 3.5</td><td>188 – 1.15</td><td>1.15 – 0.32</td><td>0.32 – 0.0030</td></tr><tr><td>Sub-Jovians</td><td>3.5 – 6</td><td>220 – 1.65</td><td>1.65 – 0.45</td><td>0.45 – 0.0030</td></tr></table>

integration time to be detected. While for scenario 1 the typical observing time per target is between 15 and 35 hours, it is between 50 and 130 hours for scenario 2.

In Fig. 5 we show the distribution of detectable exoplanets as a function of the spectral type of their host star. For the rocky

eHZ exoplanets there is a strong preference for M dwarfs. This is because M dwarfs are, on average, much more numerous and hence there is a larger number of M dwarfs close to the Sun. In addition, they have a higher occurrence rate of terrestrial exoplanets (cf. Dressing & Charbonneau 2015). In Fig. 6 we show

Article number,

page 7 of 23

<!-- page 8 of 23 -->

A&A proofs: manuscript no. LIFE\_paper\_1\_FINAL\_EITED

the distance distribution of the detected exoplanets for both scenarios. By maximizing the number of rocky eHZ exoplanets one exclusively observes stars within  $\sim$ 10 pc of the Sun.

![Chart block](doc:52385f0/tier:standard/page:8/block:3)

Fig. 6. Distance distribution of the detected planet populations shown in Fig. 3. The bars show the number of expected planet detections, including the statistical $1 - \sigma$ uncertainty from the Monte Carlo approach but excluding uncertainties in the exoplanet occurrence rates.

Another important parameter to look at is the detection efficiency, that is, the number of detectable rocky eHZ exoplanets relative to the total number of such exoplanets that were generated in our simulations. This is illustrated in Fig. 7, which is based on the results for scenario 2. One can see that, depending on the received stellar insolation (or, to a first approximation, the resulting equilibrium temperature), only a certain fraction of the exoplanets is detected. As indicated above, the main reason is the required sensitivity rather than the spatial resolution. Still, some of the simulated exoplanets are indeed at an orbital phase where they escape a detection with the interferometer. However, it is reassuring that  $\geq50\%$  detection efficiency is achieved for exoplanets with  $T_{eq} \geq 225$  K, or insolations within  $0.8 S_{\oplus} \leq S_{p} \leq 1.5 S_{\oplus}$ . This number could be further increased by implementing a multi-visit search phase. Work on quantifying the gain in detection efficiency (and survey completeness) as a function of number of visits in currently ongoing.

## 3.2. Impact of aperture size and wavelength range

In Figs. 8 and 9 we show the expected detection yield for apertures with D = 1 m and D = 3.5 m, respectively. The format is the same as for the reference case shown in Fig. 4; the plots corresponding to Fig. 3 are available in Appendix C, where we also show in Fig. C.3 the relative changes in yield compared to the reference case. Figure 10 provides a summary of the impact of the aperture size on the total LIFE exoplanet detection yield during the 2.5-year search phase. It shows that, as expected, aperture size strongly affects the number of detectable exoplanets and it is important to point out that the gain (loss) when going to larger (smaller) apertures is most significant for small exoplanets of all temperatures and cool exoplanets of all sizes. Specifically, Figs. 8 and 9 show that in the case of D = 3.5 m, the number of rocky eHZ exoplanets and EECs would increase to  $\approx63$  (+132%) and  $\approx28$  (+161%), respectively, in scenario 1. The corresponding numbers in scenario 2 are  $\approx78$  (+78%) and  $\approx39$  (+88%). The relative smaller gain in scenario 2 compared to sce-

![Chart block](doc:52385f0/tier:standard/page:8/block:8)

![Chart block](doc:52385f0/tier:standard/page:8/block:9)

Fig. 7. Detection efficiency for rocky eHZ exoplanets for our scenario 2. Top panel: Equilibrium temperature distribution of all exoplanets present in the surveyed sample (gray) and all detected exoplanets (blue). Bottom panel: Same as above, but as a function of stellar insolation. In both panels the detection efficiency (y axis on the right-hand side) is shown with the dashed red line.

nario 1 is explained by the higher number of exoplanets already detected with the reference aperture size of $D = 2 \, \mathrm{m}$. In case of $D = 1 \, \mathrm{m}$, the number of rocky eHZ exoplanets and EECs would decrease to $\approx 6$ (-76%) and $\approx 2$ (-81%), respectively, in scenario 1. In scenario 2, the numbers would go down to $\approx 17$ (-61%) and $\approx 7$ (-64%) for rocky eHZ exoplanets and EECs, respectively.

The effect of changing the wavelength range is much weaker by comparison, and generally the number of detectable planets only increases or decreases by a few percent. Figures C.4 and C.5 in Appendix C show the results in the same format as Fig. 3, and the changes relative to the reference case with  $\lambda = 4 - 18.5 \mu m$  are shown in Fig. C.6.

## 4. Discussion

## 4.1. Total exoplanet yields

Looking at the total number of detectable exoplanets and their properties reveals how diverse the expected LIFE exoplanet yield will be. This sample spans about four orders of magnitudes in planet insolation and about a factor of 10 in planet radius. In addition to investigations concerning the habitability of a subset of the sample, LIFE has the potential to address a number

Article number,

page 8 of 23

<!-- page 9 of 23 -->

Quanz et al.: LIFE: I. Improved exoplanet detection yield estimates for a MIR space interferometer

![Chart block](doc:52385f0/tier:standard/page:9/block:2)

Fig. 8. Same as Fig. 4, but now for $D = 1.0 \, \mathrm{m}$.

![Chart block](doc:52385f0/tier:standard/page:9/block:4)

Fig. 9. Same as Fig. 4, but now for $D = 3.5 \, \mathrm{m}$.

Total LIFE exoplanet yield (2.5-year search phase)

![Chart block](doc:52385f0/tier:standard/page:9/block:7)

Fig. 10. Total expected exoplanet detection yield as a function of aperture size and for each of the two scenarios. The numbers shown here are the sum of the mean numbers shown in the grid cells in Figs. 3, C.1, and C.2.

![Chart block](doc:52385f0/tier:standard/page:9/block:9)

![Chart block](doc:52385f0/tier:standard/page:9/block:10)

![Chart block](doc:52385f0/tier:standard/page:9/block:11)

Fig. 11. Detection yield comparison between LUVOIR A/B, HabEx, and LIFE. For LIFE we show the numbers for the $D = 2$ m reference case and for HabEx the numbers from the baseline 4-meter concept. Jovian planets are not shown, because they were not included in the LIFE simulations (cf. Sect. 2.2; see text for important details).

Article number,

page 9 of 23

<!-- page 10 of 23 -->

A&A proofs: manuscript no. LIFE\_paper\_1\_FINAL\_EITED

![Chart block](doc:52385f0/tier:standard/page:10/block:2)

![Chart block](doc:52385f0/tier:standard/page:10/block:3)

Fig. 12. Median S/N of the detected exoplanets in our reference case scenario simulations in the radius vs. stellar insolation plane (left panel: Scenario 1; right panel: Scenario 2). We note that the 1D distributions on top and to the right of the grids (as well as colored area) represent the numbers of detected exoplanets, including the $1 - \sigma$ uncertainties shown in Fig. 3, and not the marginalized distributions of the S/N.

of scientific questions related to the formation and evolution of exoplanets and their atmospheres.

In Fig. 11 we provide a comparison with the detection yields published in the HabEx and LUVOIR study reports (Gaudi et al. 2020; The LUVOIR Team 2019) $^{9}$ . This plot suggests that for exoplanets with radii up to 6 R $_{\oplus}$ , LIFE, with four times D = 2 m apertures, can achieve overall detection yields comparable to those of the LUVOIR-A (15-meter aperture) and LUVOIR-B (8-meter aperture) concepts; HabEx, with a 4-meter primary mirror, is predicted to yield fewer detections. It needs to be noted, though, that while in our simulations planets with radii >6 R $_{\oplus}$  were not included, LUVOIR A and B and HabEx are predicted to detect  $\approx$ 117,  $\approx$ 102 and  $\approx$ 31 of these Jovian planets, respectively. It is also important to mention that the numbers for LIFE are the sum of numbers for the various planet types shown in Fig. 4. The resulting overall numbers of detectable planets differ slightly from those shown in Fig. 10 because some detectable planets fall outside the insolation ranges defined in Table 2.

Overall, these results show that in principle both approaches, large, single-aperture reflected light missions and interferometric MIR missions (under the assumptions laid out in Sect. 2), offer unprecedented opportunities for the direct detection and detailed investigations of hundreds of nearby exoplanets. Going forward, it will be important to investigate possible scientific synergies between missions such as HabEx or LUVOIR and LIFE because at least a subset of the exoplanets detected by one approach is likely also detectable by the other.

The single most important parameter related to the number of detectable exoplanets is, unsurprisingly, the aperture size of the collector spacecraft. While here we focus on a 2-D array architecture for the interferometer with four collector spacecraft with aperture sizes between $D = 1$ m and $D = 3.5$ m, Dandumont et al. (2020) recently presented a similar yield analysis based on 4 different implementations of a two-aperture Bracewell interferometer: 2 CubeSat options (with a 0.5 or 1 m baseline and 0.08 m apertures), a Proba mission option (with a 5 m baseline and 0.25 m apertures), and the Fourier Kelvin Stellar Interferometer concept presented in Danchi et al. (2008) and Danchi &

Barry (2010) (with a 12 m baseline and 0.5 m apertures). The trend shown here continues down to CubeSat apertures and the detection of at least  $\approx$ 10–15 rocky eHZ exoplanets requires an aperture size of at least D = 1 m. The strong dependence of the detection yield on the aperture size results from the fact that, in the vast majority of cases, the local zodiacal dust emission is an important noise term and the effective FoV of the collector spacecraft scales with  $\lambda/D$  (cf. Sect. 2.3). In Appendix D we provide an overview of the relative contributions of the various noise terms to the total noise for planets detected in the reference case scenarios (Fig. D.1).

Another key result from our analyses is that, depending on how the observing time is distributed amongst the stellar targets, both the number of detected exoplanets and the type of detected exoplanets can vary significantly. This illustrates a strong need for the community to clearly define and prioritize the scientific objectives of such a mission in order to derive the appropriate observing strategy. An additional parameter that needs to be considered in this context is the completeness of the survey, that is, how important it is to have detected, with a certain level of confidence, all (or at least most) exoplanets from a specific subset of the exoplanet population in the solar neighborhood. Higher completeness requires more observing time per target star (including multiple visits) and hence a lower number of detectable exoplanets overall.

The results from the search phase, and also its duration, have an immediate impact on the follow-up strategy during the characterization phase of the mission. It is hence important to understand how well the fundamental properties of the detected exoplanets (such as radius and temperature, but also their orbital position) can be constrained from single-epoch data. In Fig. 12 we present some first indications by showing the median S/N of the detected exoplanets as a function of their radius and insolation. Because of the much longer average integration time per star in scenario 2 (cf. Sect. 3.1), the median S/N is, in many cases, significantly higher than in scenario 1. Interestingly, the exoplanets in most grid cells (and certainly warm and hot exoplanets with radii $>1.5R_{\oplus}$) are detected with sufficiently high S/N that some first-order estimate of their radius and effective temperature and maybe even a rough analysis of their SED based on (very) low-resolution spectroscopy appears feasible. This aspect needs to

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">$^{9}$  See Stark et al. (2019) for details on the yield calculations for the reflected light missions.</span></small>

Article number, page 10 of 23

<!-- page 11 of 23 -->

Quanz et al.: LIFE: I. Improved exoplanet detection yield estimates for a MIR space interferometer

![Chart block](doc:52385f0/tier:standard/page:11/block:2)

Fig. 13. Comparison of exoplanet detections with LIFE to known Solar System planets and exoplanets. The LIFE yield for the reference case (scenario 2) is shown in red contours using a kernel density estimate of the detected sample. Every shaded contour level corresponds to 50 exoplanets detected in the respective parameter space. Blue points represent 60 out of the 79 known exoplanets within 10 pc of the Sun for which we could estimate the radius and insolation level. Gray points represent the four rocky planets in the Solar System (E=Earth, V=Venus, Ma=Mars, and Me=Mercury).

be investigated further as the possibility to obtain spectral information already from single-epoch data allowing for a first characterization and classification of the exoplanets has an impact on the follow-up strategy during the characterization phase. For completeness we note that the largest, hottest planets receiving the highest levels of insolation do not show the highest median S/N. This is because the S/N is related to the location of the exoplanets in the transmission map of the interferometer, which maximizes the throughput for exoplanets located in the eHZ and not for close-in exoplanets (cf. Sect. 2.3).

Finally, whether or not future exoplanet imaging space missions will have to carry out a somewhat extended search phase, will also depend on the progress and results of ongoing and future ground-based RV surveys. In Fig. 13 we show a comparison between the expected LIFE detection yield (reference case; scenario 2) and currently known exoplanets within 10 pc of the Sun drawn from the NASA Exoplanet Archive $^{10}$ . If the insolation is not provided for planets in the archive, it is calculated via  $L_{\star}[L_{\odot}]/a[AU]^{2}$ , with  $L_{\star}$  the host star luminosity,  $L_{\odot}$  the solar luminosity, and a the semimajor axis of the exoplanet orbit. A missing radius measurement is estimated using forecaster $^{11}$  (Chen & Kipping 2016). This leads to 60 out of the 79 confirmed exoplanets within 10 pc for which we can assign both radius and

insolation. Fig. 13 shows on the one hand that there is an interesting sample of planets already known within 10 pc from which a preliminary target list could be compiled. On the other it demonstrates that one expect a factor of 5 more planets to be found within 10 pc with LIFE. New (or the continuation of) systematic RV exoplanet searches in the solar neighborhood will be fundamentally important to either provide future imaging missions with a predefined exoplanet target list or at least provide them with stringent constraints on the existence of nearby planetary systems. The same is true for systematic searches of exozodi disks around nearby stars. As mentioned above, already during the search phase typical integration times are easily on the order of days. This means that S/Ns >5 per spectral channel $^{12}$ are costly and knowing interesting or promising targets beforehand saves valuable observing time.

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">10 https://exoplanetarchive.ipac.caltech.edu</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">$^{11}$  https://github.com/chenjj2/forecaster</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">$R\approx 40$ (e.g.</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">$^{12}$  First science requirements for the spectral resolution and wavelength coverage of LIFE are presented im (Konrad et al. 2021). Previous works in this direction and in the context of atmospheric characterization of terrestrial exoplanets at MIR wavelengths suggested spectral resolutions of up to  $R \approx 40$  (e.g., Des Marais et al. 2002; Léger et al. 2019).</span></small>

Article number,

page 11 of 23

<!-- page 12 of 23 -->

A&A proofs: manuscript no. LIFE\_paper\_1\_FINAL\_EITED

![Chart block](doc:52385f0/tier:standard/page:12/block:2)

![Chart block](doc:52385f0/tier:standard/page:12/block:3)

![Chart block](doc:52385f0/tier:standard/page:12/block:4)

Fig. 14. Same as the right panel in Fig. 4, but ignoring all M-type dwarfs in the target catalog and spending the full search phase on FGK stars only. The panels show the results for $D = 1.0\mathrm{m}$, $D = 2.0\mathrm{m}$, and $D = 3.5\mathrm{m}$ from left to right, respectively.

## 4.2. Rocky HZ exoplanets: M-star preference and detection efficiency

As shown in Fig. 4, LIFE could detect  $\approx$ 25–45 of rocky exoplanets located within the eHZ of their host stars and  $\approx$ 10–20 EECs following the definition of Kopparapu et al. (2018). However, these numbers are strongly affected by the aperture size of the collector spacecraft. As shown in Figs. 8 and 9, decreasing (increasing) the aperture size yields a significant decrease (increase) in the number of rocky temperate exoplanets. These findings will be of great importance during upcoming trade-offs between mission cost, where aperture size will be an important parameter, and science return. We stress that this is not only important for the search phase, but it is even more relevant for the characterization phase that aims at investigating a subsample of the detected exoplanets in greater detail with high-S/N spectra (Konrad et al. 2021).

Following similar arguments presented in Stark et al. (2014, 2015), Quanz et al. (2021) argued that in order to obtain statistically robust results on the fraction of rocky HZ exoplanets that are indeed habitable, at least 30 (better 50) exoplanets in that part of parameter space need to be studied. According to the numbers presented above, this appears to be achievable with LIFE. However, the vast majority of these planets is found around M stars and at this point in time it is unknown whether exoplanets orbiting within the HZ around M stars are able to retain (secondary) atmospheres because of the high activity of M-type stars, in particular at young ages (e.g., Tian & Ida 2015; Luger & Barnes 2015; Lingam & Loeb 2018; Godolt et al. 2019; Atri & Mogan 2021). It has been shown that under certain circumstances such exoplanets, which are very likely tidally locked, may still provide habitable conditions (e.g., Leconte et al. 2015; Ribas et al. 2016; Turbet et al. 2016; Boutle et al. 2017), but empirical data are still lacking. There is, however, hope that JWST will be able to address this fundamentally important question and, for a few cases, investigate the existence of atmospheres of rocky exoplanets transiting M stars (e.g., Koll et al. 2019). Also, a deep characterization effort of the potential M-star targets should be carried out, including the high-energy radiation budget and its past history, in order to understand which stars may have provided a more quiescent environment for their expected planets. If rocky exoplanets orbiting M stars can retain atmospheres, then LIFE is in an excellent position to robustly characterize a significantly larger sample. If not, then one may want to reconsider the observing strategy and possibly de-prioritize M stars in the stellar input catalog. Figure 14 shows the results for the most extreme case, where all M stars are ignored and the full search phase is spent on FGK stars. In this case, ≈25 rocky eHZ exoplanets

can be expected assuming an aperture size of $D = 3.5 \, \mathrm{m}$; with $D = 2.0 \, \mathrm{m}$ this number would drop to $\approx 11$, limiting the statistical power of the analysis. In this context, two points are important to mention: (a) in order to further increase the number of detected rocky eHZ planets around FGK stars, it will be important to investigate how a search phase with a multi-visit strategy would affect the results. We remind the reader that a detection efficiency $\geq 50\%$ is currently achieved for exoplanets with $T_{\mathrm{eq}} \geq 225 \, \mathrm{K}$ or insolations within $0.8 \, S_{\oplus} \leq S_{\mathrm{p}} \leq 1.5 \, S_{\oplus}$. Ignoring the M stars and repeating the analysis shown in Fig. 7 for FGK stars only reveals that the overall detection efficiency is indeed lower (see Fig. C.7 in Appendix C). Hence, we can expect to gain additional detections when multiple visits per star are applied; (b) As we discuss in Sect. 4.3.3, our underlying occurrence rates for rocky, temperate planets around FGK stars may be on the rather conservative side.

Similar to the expected total detection yield, also the number of predicted EECs can be compared to those published in the HabEx and LUVOIR study reports (Gaudi et al. 2020; The LUVOIR Team 2019). HabEx, with its 4-meter baseline concept, is expected to detect  $\approx8$  EECs, while LUVOIR-A and LUVOIR-B are predicted to directly image  $\approx54$  and  $\approx28$  EECs, respectively. Considering the  $\approx20$  EECs that LIFE is expected detect (assuming D = 2 m and scenario 2), one has to keep in mind its preference for planets around M stars, while HabEx and LUVOIR have a strong detection bias for planets around solar-type stars. This suggests that there is only limited overlap in primary discovery space for EECs between the missions if they were to carry out independent search phases. Hence, it will be important to check the potential overlap assuming that one mission is following-up after the other (e.g., LIFE following after LUVOIR/HabEx). In addition, looking more carefully at the underlying EEC occurrence rates, it shows that the numbers cannot be directly compared (see Sect. 4.3.3 below).

## 4.3. Remaining limitations and uncertainties in the simulations

## 4.3.1. Treatment of noise sources

Compared to previous works the yield simulations presented here are based on a more realistic treatment of the observing technique and include all major astrophysical noise terms. One of the next crucial steps is to continue the development of an instrument concept including a noise breakdown structure so that quantitative instrumental noise estimates can be included in the simulations. The calculations from Lay (2004) indicate that the noise contributions from photon noise and instrumental noise

Article number,

page 12 of 23

<!-- page 13 of 23 -->

Quanz et al.: LIFE: I. Improved exoplanet detection yield estimates for a MIR space interferometer

may indeed not be very different. However, these calculations were done for a specific example and how the relative contributions scale with stellar and planet properties and exozodi brightness needs to be investigated. Also, recent work by Dandumont et al. (2020) and other previous analyses in the context of TPF-I (e.g., Lay 2006) or Darwin (e.g., Defrère et al. 2010) can serve as starting points. In addition to the noise budget, important instrument parameters such as overall throughput and detector quantum efficiency need to be further validated. For the interested reader we provide a summary of the status of some key technologies relevant for LIFE in Appendix B.

## 4.3.2. Treatment of exozodiacal and zodiacal dust

While we do take into account emission from potential exozodiacal dust disks using the nominal distribution from the HOSTS survey (Ertel et al. 2020), it needs to be acknowledged that there is still considerable uncertainty in the median exozodi level: while in the nominal distribution the median zodi level is $\bar{z} \approx 3.2$, Ertel et al. (2020) show that one can only be confident at the $1\sigma$ level that the median is below 9 zodis and at the $2\sigma$ level that it is below 27 zodis. In order to quantify the impact of these uncertainties on the detection yield, we did the following experiment for the reference case scenarios: the exozodi level distribution was shifted by adding multiples of the median absolute deviation (MAD) of the distribution $(\mathrm{MAD}(z) \approx 2.7)$ to each individual exozodi level in the sample. In the most extreme case we analyzed the distribution was shifted by 9-MAD, resulting in a median $\bar{z} \approx 27$ corresponding to the $2\sigma$ level mentioned above. In this case, the total number of detectable planets decreased by $\lesssim 6\%$ and the number of rocky, HZ planets changed even less. One reason for this somewhat limited impact is that, compared to noise from stellar leakage and local zodiacal dust emission, noise from exozodiacal dust disks contributes only little to the total noise budget of detected planets (see Fig. D.1). Hence, in a statistical sense, the current uncertainties may not have a strong impact on the overall results. Still, additional observational efforts determining exozodi levels would further improve upon the current statistical uncertainties and, maybe even more importantly, would also help prioritize the most promising individual targets for future space missions. In addition, at the moment, the HOSTS survey does not show a correlation between spectral type and the level of exozodi emission (Ertel et al. 2020), and hence we apply the same underlying distribution of exozodi levels to all target stars irrespective of spectral type. A larger data set would be required to further confirm this current finding.

Furthermore, the inclination of exozodiacal dust disks and possible spatial offsets and substructures (e.g., “clumps,” such as those seen in the zodiacal light; Reach 2010; Krick et al. 2012) are not considered in our simulations. As long as exozodiacal dust disks are centrally symmetric and optically thin, their contribution to the photon noise in a LIFE measurement is to first order independent from their inclination; hence, changing the inclination of the disks has no measurable impact on the results. Spatial offsets and disk substructures would, however, have an impact on the S/N calculations. Defrère et al. (2010) looked at the specific case of an Earth-Sun twin located at 15 pc. They modeled planet induced resonant structures in exozodi disks with varying dust density and inclination and investigated up to what exozodi level the planet would still be detectable. They concluded that around  $10 \mu m$  wavelength, up to  $\sim15$  and  $\sim7$  zodis are acceptable for disks with inclinations between  $0-30^{\circ}$  and up to  $60^{\circ}$, respectively. For edge-on systems this limit drops to  $\sim1.4$  zodis. In order to further refine the results presented here, analy-

ses as the ones presented in Defrère et al. (2010) could to be carried out, possibly enlarging the covered parameter space. However, as already noted by the authors, advanced signal processing approaches may further relax the constraints in terms of acceptable zodi levels mentioned above. Also, if one considers the nominal distribution of exozodi levels published by the HOSTS team, the above mentioned zodi level limits appear to be on the high-end side: about two-thirds of our simulated systems with randomly assigned zodi levels based on the nominal distribution have disks with  $\leq7$  zodis. Hence, we do not expect exozodi dust disks to be a show-stopper for LIFE. However, systems that are seen (close to) edge-on may pose a real challenge and have to be investigated in more detail, and a coordinated effort to reduce the existing uncertainties in the median exozodi level of nearby stars remains certainly important.

Defrère et al. (2010) also addressed the question of disk offsets, where the geometric center of the exozodi disk is shifted away from the center of the star, which would lead to additional flux through the modulation map of the interferometer. They focused on a Sun-like star at 15 pc and considered only face-on systems. When looking at the modulated signal covering the full wavelength range, systems with up to $\sim 50$ zodis and offsets as large as $\sim 0.5$ au were considered acceptable. As the offset increases, the level of acceptable zodis decreases, but for offsets as large as 1 au, $\sim 5$ zodis could still be tolerated. It hence seems that, apart from potentially extreme cases, disk offsets are not a major concern for LIFE. For reference: in the Solar System, the center of the zodiacal cloud is shifted by only about 0.013 AU from the Sun (Landgraf & Jehn 2001).

## 4.3.3. Occurrence rates of small, temperate exoplanets

Similarly to the exozodi disks, also our zodiacal dust model does not contain any substructures. As mentioned above, and shown in Fig. D.1, the MIR emission from the zodiacal dust is an important astrophysical noise source in a typical LIFE observation and the model should hence be further refined to correct for the current overestimation of the emission shortward of  $6 \mu m$ .

An additional uncertainty in our results is related to the underlying exoplanet population. While in some parts of the parameter space the occurrence rate of exoplanets was robustly measured by the Kepler mission, there remains significant uncertainty related to the completeness and reliability for the occurrence rates of rocky, temperate exoplanets around Sun-like stars (e.g., Bryson et al. 2020). We note that recent estimates for $\eta_{\oplus}$, which is the fraction of stars with terrestrial exoplanets within their HZ, are higher than the ones resulting from our underlying distributions: Bryson et al. (2021) provided two values, $\eta_{\oplus}^{\mathrm{o}} = 0.58_{-0.33}^{+0.73}$ and $\eta_{\oplus}^{\mathrm{o}} = 0.88_{-0.51}^{+1.28}$, for the occurrence rate of planets with radii between 0.5 and $1.5R_{\oplus}$ orbiting in the eHZ of stars with effective temperatures between 4800 and $6300\mathrm{K}^{13}$. These bounds represent two extreme assumptions about the extrapolation of completeness beyond orbital periods where the Kepler DR25 completeness data are available. For EECs around solar-type stars, Bryson et al. (2021) found a lower bound of $\eta_{\oplus}^{\mathrm{EEC}} = 0.18_{-0.28}^{+0.16}$ and an upper bound of $\eta_{\oplus}^{\mathrm{EEC}} = 0.28_{-0.09}^{+0.30}$. In our simulations, $\eta_{\oplus}^{\mathrm{o}} \approx 0.37$ and $\eta_{\oplus}^{\mathrm{EEC}} \approx 0.16$ for FGK dwarfs (and $\approx 0.56$ and $\approx 0.31$ for M dwarfs, respectively; see Table 1). Hence, in particular for solar-type stars, we might be underestimating the number of EECs and rocky, eHZ planets. Also, our value for $\eta_{\oplus}^{\mathrm{EEC}}$ is lower than the one used in the HabEx and LU-

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">$\eta_{\oplus}^{\mathrm{o}}$</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">$^{13}$  Our definition of the eHZ is identical to their “optimistic” HZ case; the superscript “o” in  $\eta_{\oplus}^{0}$  refers to the word “optimistic”.</span></small>

Article number,

page 13 of 23

<!-- page 14 of 23 -->

A&A proofs: manuscript no. LIFE\_paper\_1\_FINAL\_EDITED

VOIR concept studies, which was  $\eta_{\oplus}^{EEC}=0.24_{-0.16}^{+0.46}$ . One reason for this difference is that we did not keep this parameter constant throughout our stellar sample, but we let it vary between various spectral types (see notes in Table 1). Hence, at least for this specific subset of planets, a direct quantitative comparison between our results and the other mission studies is not immediately straightforward. In a future study, we will further investigate the impact of the various values of  $\eta_{\oplus}$  and their statistical and systematic uncertainties on the resulting detection yield (cf. Léger et al. 2015).

Overall, it is clear that reanalyses of the Kepler data, in combination with additional results from K2, TESS, and the upcoming PLAnetary Transits and Oscillations of stars (PLATO) mission (Rauer et al. 2014) are extremely important to provide a more robust empirical basis for future updates of the analyses presented here. In particular PLATO is designed to detect Earth-like planets in the HZ of solar-like stars and will improve our knowledge of the occurrence rate and formation mechanism of these targets.

## 5. Summary and conclusions

We have presented new and more realistic results for the exoplanet detection yield of a space-based MIR nulling interferometer based on the exoplanet statistics observed by the Kepler mission and targeting main-sequence FGKM stars within 20 pc of the Sun. Taking into account all major astrophysical noise terms and adding some margin for the not yet included instrumental noise effects (we require a S/N≥7 for a detection), we find that an interferometer array consisting of four 2 m apertures and covering the 4–18.5 μm wavelength range with a total throughput of 5% will yield, depending on the observing strategy, between ≈350 and ≈550 directly detected exoplanets with radii between 0.5 and 6 R$_{⊕}$ within a 2.5-year search phase. Between ≈160 and ≈190 of these exoplanets have radii between 0.5 and 1.5 R$_{⊕}$. As there is some freedom in how to assign observing time to the stellar targets, one can attempt to maximize the number of detected planets in certain areas of parameter space. We demonstrated this with two scenarios where either the total number of exoplanets or the number of rocky planets within the empirical HZ is maximized. The observing strategy must be adapted to the overall scientific objectives of the LIFE mission since it influences the number (and types) of detected exoplanets.

Keeping the instrument throughput fixed at 5%, we find the number of detectable exoplanets to be a strong function of aperture size. In our current analysis, the wavelength range has a negligible impact on the exoplanet yield. We have shown that  $\approx$ 25–45 rocky exoplanets within the empirical HZ of their host stars are expected to be detectable with four 2 m apertures, but this number could go up to  $\approx$ 60–80 if the aperture size were increased to 3.5 m. In this case, the total number of detectable planets could go up to  $\approx$ 770. With four 1 m apertures, the number of rocky exoplanets within the empirical HZ would be  $\leq$ 20 and the total detection yield <320. Irrespective of aperture size, the vast majority of rocky exoplanets orbiting within the empirical HZ are detected around M dwarfs. It will be important to further investigate if these planets could in principle possess atmospheres despite the high-energy UV flux and flaring activity these stars display. To further increase the number of detected rocky HZ planets around FGK stars, multiple visits per star during the search phase need to be considered in future work.

All numbers presented here (i.e., the total number of detected planets and the number of rocky planets within the HZ) are competitive with those predicted for current mission concepts search-

ing for exoplanets in reflected light. Further studies investigating potential scientific and operational synergies between a reflected light and a thermal emission mission should be considered. Such efforts are particularly important for small temperate planets, such as EECs, because reflected light missions have a strong bias for detecting these objects primarily around solar-type stars, while LIFE has a strong bias for planets around M stars. We note, however, that when comparing the numbers of detectable EECs with those predicted for the LUVOIR and HabEx missions, the underlying occurrence rates are not identical. The simulations presented here use lower values for EECs around FGK stars. This shows that care must be taken when comparing predicted detection yields of future missions, and additional efforts, such as obtaining new data and investigating new data analysis approaches, are needed to further refine the statistical occurrence rates that form the basis for all yield calculations.

Comparing the predicted primary discovery space of LIFE with known exoplanets within 10 pc of the Sun shows that there are >40 objects,  $\approx$ 15 of which have predicted radii <1.5 R $_{\oplus}$ , that could be added to a target list today. To minimize the time that future exoplanet imaging space missions have to devote to an initial search phase, continuing ground- and space-based detection surveys is crucial.

We note that both the overall exoplanet detection yield and the observing time required to robustly characterize the atmospheric properties of rocky, temperate exoplanets with an MIR interferometer are strong functions of apertures size, which must be considered in future trade-off studies. The MIR regime is particularly rich in molecular absorption bands of the main constituents of terrestrial exoplanet atmospheres, including major biosignatures (e.g., Schwieterman et al. 2018; Catling et al. 2018). Also, thermal emission spectra provide more information about the atmospheric structure and allow for a more direct measurement of the planetary radius than reflected light data (e.g., Line et al. 2019). The relatively high S/N (integrated over the full wavelength range) that most detectable planets in our simulations have suggests that decent estimates for their radii and effective temperatures – and in some cases even rough SEDs – seem possible. In this case, the data from a single-epoch observation obtained during the search phase will already provide crucial information for categorizing and prioritizing the planets for the follow-up characterization phase (for further details, see Dannert et al. 2022).

Our results show that when investigating and selecting future large exoplanet imaging space missions, for instance in the context of ESA's Voyage 2050 program, a concept such as LIFE should be considered a serious contender and may be required to ultimately assess the habitability of exoplanets$^{14}$. Taking into account the heritage from the Darwin and TPF-I studies and more recent progress based on various local activities, new coordinated efforts to further understand and increase the technological readiness level of key components have started as part of the LIFE initiative (e.g., Gheorghe et al. 2020).

Acknowledgements. We thank the anonymous referee for a critical and constructive review of the original manuscript which helped improve the quality of the paper. This work has been carried out within the framework of the National Centre of Competence in Research PlanetS supported by the Swiss National Science Foundation. SPQ, EA and HSW. acknowledge the financial support of the SNSF. SK acknowledges funding from an ERC Starting Grant (grant agreement No. 639889). DE acknowledges funding from the European

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">$^{14}$  See, e.g., "Exoplanet Strategy Report 2018" from the National Academies of Sciences, Engineering, and Medicine available at https://www.nap.edu/catalog/25187/exoplanet-science-strategy.</span></small>

Article number, page 14 of 23

<!-- page 15 of 23 -->

Quanz et al.: LIFE: I. Improved exoplanet detection yield estimates for a MIR space interferometer

Research Council (ERC) under the European Union's Horizon 2020 research and innovation programme (project Four Aces; grant agreement No 724427). JL-B acknowledges financial support received from “la Caixa” Foundation (ID 100010434) and the European Union’s Horizon 2020 research and innovation programme under the Marie Sklodowska-Curie grant agreement No 847648, with fellowship code LCF/BQ/PI20/11760023. RA is a Trottier Postdoctoral Fellow and acknowledges support from the Trottier Family Foundation. This work was supported in part through a grant from FRQNT. TL acknowledges funding from the Simons Foundation (SCOL award No. 611576). Part of this work was conducted at the Jet Propulsion Laboratory, California Institute of Technology, under contract with NASA. This research has made use of the SIMBAD database, operated at CDS, Strasbourg, France, and of the Washington Double Star Catalog maintained at the U.S. Naval Observatory. This research has made use of the NASA Exoplanet Archive, which is operated by the California Institute of Technology, under contract with the National Aeronautics and Space Administration under the Exoplanet Exploration Program. This research has made use of the following Python packages: astropy (Astropy Collaboration et al. 2013, 2018), matplotlib (Hunter 2007), numpy (Van Der Walt et al. 2011), and scipy (Virtanen et al. 2020).

Author contributions: SPQ initiated the project, devised the analyses and wrote the manuscript. MO and FD wrote the LIFESIM tool and created the figures. AGh and EF contributed to the LIFESIM tool. JK simulated the exoplanet populations. FM created the LIFE target star catalog. All authors discussed the results and commented on the manuscript.

## References

Angel, J. R. P. & Woolf, N. J. 1997, ApJ, 475, 373

Anglada-Escudé, G., Amado, P. J., Barnes, J., et al. 2016, Nature, 536, 1

Astropy Collaboration, Price-Whelan, A. M., Sipócz, B. M., et al. 2018, AJ, 156, 123

Astropy Collaboration, Robitaille, T. P., Tollerud, E. J., et al. 2013, A&A, 558, A33

Astudillo-Defru, N., Díaz, R. F., Bonfils, X., et al. 2017, Astronomy & Astrophysics, 605, L11

Atri, D. & Mogan, S. R. C. 2021, MNRAS, 500, L1

Berta-Thompson, Z. K., Irwin, J., Charbonneau, D., et al. 2015, Nature, 527, 204

Borucki, W. J., Koch, D., Basri, G., et al. 2010, Science, 327, 977

Boutle, I. A., Mayne, N. J., Drummond, B., et al. 2017, A&A, 601, A120

Bowens, R., Meyer, M. R., Delacroix, C., et al. 2021, A&A, 653, A8

Bracewell, R. N. 1978, Nature, 274, 780

Brandl, B., Bettonvil, F., van Boekel, R., et al. 2021, The Messenger, 182, 22

Brandl, B. R., Absil, O., Agócs, T., et al. 2018, in Proceedings of the SPIE, ed. H. Takami, C. J. Evans, & L. Simard, Leiden Univ. (Netherlands) (SPIE), 107021U

Bryson, S., Coughlin, J., Batalha, N. M., et al. 2020, AJ, 159, 279

Bryson, S., Kunimoto, M., Kopparapu, R. K., et al. 2021, AJ, 161, 36

Cabrera, M. S., McMurtry, C. W., Forrest, W. J., et al. 2020, Journal of Astronomical Telescopes, Instruments, and Systems, 6, 011004

Catling, D. C., Krissansen-Totton, J., Kiang, N. Y., et al. 2018, Astrobiology, 18, 709

Chen, J. & Kipping, D. 2016, The Astrophysical Journal, 834, 17

Colavita, M. M., Serabyn, E., Millan-Gabet, R., et al. 2009, PASP, 121, 1120

Danchi, W. C. & Barry, R. K. 2010, in Society of Photo-Optical Instrumentation Engineers (SPIE) Conference Series, Vol. 7734, Optical and Infrared Interferometry II, ed. W. C. Danchi, F. Delplancke, & J. K. Rajagopal, 77340M

Danchi, W. C., Barry, R. K., Lawson, P. R., Traub, W. A., & Unwin, S. 2008, in Society of Photo-Optical Instrumentation Engineers (SPIE) Conference Series, Vol. 7013, Optical and Infrared Interferometry, 70132Q

Dandumont, C., Defrère, D., Kammerer, J., et al. 2020, Journal of Astronomical Telescopes, Instruments, and Systems, 6, 035004

Dannert, F., Ottiger, M., Quanz, S. P., et al. 2022, arXiv e-prints, arXiv:2203.00471

Defrère, D., Absil, O., Berger, J. P., et al. 2018a, Experimental Astronomy, 46, 475

Defrère, D., Absil, O., den Hartog, R., Hanot, C., & Stark, C. 2010, A&A, 509, A9

Defrère, D., Léger, A., Absil, O., et al. 2018b, Experimental Astronomy, 46, 543

Des Marais, D. J., Harwit, M. O., Jucks, K. W., et al. 2002, Astrobiology, 2, 153

Díaz, R. F., Delfosse, X., Hobson, M. J., et al. 2019, A&A, 625, A17

Dressing, C. D. & Charbonneau, D. 2015, ApJ, 807, 45

Dulz, S. D., Plavchan, P., Crepp, J. R., et al. 2020, ApJ, 893, 122

Ertel, S., Defrère, D., Hinz, P., et al. 2020, AJ, 159, 177

Ertel, S., Defrère, D., Hinz, P., et al. 2018, AJ, 155, 194

Gaudi, B. S., Seager, S., Mennesson, B., et al. 2020, arXiv e-prints, arXiv:2001.06683

Gheorghe, A. A., Glauser, A. M., Ergenzinger, K., et al. 2020, in Optical and Infrared Interferometry and Imaging VII, ed. P. G. Tuthill, A. Merand, & S. Sallum, Vol. 11446, International Society for Optics and Photonics (SPIE), 497 – 505

Gillon, M., Demory, B.-O., Van Grootel, V., et al. 2017, Nature Astronomy, 1, 0056

Gillon, M., Triaud, A. H. M. J., Demory, B.-O., et al. 2017, Nature, 542, 456

Godolt, M., Tosi, N., Stracke, B., et al. 2019, A&A, 625, A12

He, M. Y., Ford, E. B., & Ragozzine, D. 2019, MNRAS, 490, 4575

Hinz, P., Bailey, V. P., Defrère, D., et al. 2014, in Society of Photo-Optical Instrumentation Engineers (SPIE) Conference Series, Vol. 9146, Optical and Infrared Interferometry IV, ed. J. K. Rajagopal, M. J. Creech-Eakman, & F. Malbet, 91460T

Holman, M. J. & Wiegert, P. A. 1999, AJ, 117, 621

Hunter, J. D. 2007, Computing In Science & Engineering, 9, 90

Janson, M., Brandeker, A., Boehm, C., & Martins, A. K. 2018, Future Astrometric Space Missions for Exoplanet Science, ed. H. J. Deeg & J. A. Belmonte, 87

Jeffers, S. V., Dreizler, S., Barnes, J. R., et al. 2020, Science, 368, 1477

Johnstone, C. P., Khodachenko, M. L., Lüftinger, T., et al. 2019, Astronomy & Astrophysics, 624, L10

Kammerer, J. & Quanz, S. P. 2018, A&A, 609, A4

Kasper, M., Cerpa Urra, N., Pathak, P., et al. 2021, The Messenger, 182, 38

Kasting, J. F., Whitmire, D. P., & Reynolds, R. T. 1993, Icarus, 101, 108

Kelsall, T., Weiland, J. L., Franz, B. A., et al. 1998, ApJ, 508, 44

Kennedy, G. M., Wyatt, M. C., Bailey, V., et al. 2015, ApJS, 216, 23

Koll, D. D. B., Malik, M., Mansfield, M., et al. 2019, The Astrophysical Journal, 886, 140

Konrad, B. S., Alei, E., Angerhausen, D., et al. 2021, arXiv e-prints, arXiv:2112.02054

Kopparapu, R. K., Hébrard, E., Belikov, R., et al. 2018, ApJ, 856, 122

Kopparapu, R. k., Ramirez, R., Kasting, J. F., et al. 2013, The Astrophysical Journal, 765, 131

Kopparapu, R. K., Ramirez, R. M., SchottelKotte, J., et al. 2014, ApJ, 787, L29

Kraus, A. L., Ireland, M. J., Huber, D., Mann, A. W., & Dupuy, T. J. 2016, AJ, 152, 8

Kreidberg, L. & Loeb, A. 2016, The Astrophysical Journal Letters, 832, L12

Krick, J. E., Glaccum, W. J., Carey, S. J., et al. 2012, ApJ, 754, 53

Krissansen-Totton, J., Garland, R., Irwin, P., & Catling, D. C. 2018, The Astronomical Journal, 156, 114

Kunimoto, M. & Matthews, J. M. 2020, AJ, 159, 248

Landgraf, M. & Jehn, R. 2001, Ap&SS, 278, 357

Lay, O. P. 2004, Appl. Opt., 43, 6100

Lay, O. P. 2005, Applied Optics IP, 44, 5859

Lay, O. P. 2006, in SPIE Astronomical Telescopes + Instrumentation, ed. J. D. Monnier, M. Schöller, & W. C. Danchi (SPIE), 62681A–14

Lay, O. P., Martin, S. R., & Hunyadi, S. L. 2007, in Society of Photo-Optical Instrumentation Engineers (SPIE) Conference Series, Vol. 6693, Techniques and Instrumentation for Detection of Exoplanets III, ed. D. R. Coulter, 66930A

Leconte, J., Wu, H., Menou, K., & Murray, N. 2015, Science, 347, 632

Léger, A., Defrère, D., García Muñoz, A., et al. 2019, Astrobiology, 19, 797

Léger, A., Defrère, D., Malbet, F., Labadie, L., & Absil, O. 2015, ApJ, 808, 194

Leger, A., Puget, J. L., Mariotti, J. M., Rouan, D., & Schneider, J. 1995, Ap&SS, 223, 172

Line, M., Quanz, S. P., Schwieterman, E. W., et al. 2019, BAAS, 51, 271

Lingam, M. & Loeb, A. 2018, J. Cosmology Astropart. Phys., 2018, 020

Lovis, C., Snellen, I., Mouillet, D., et al. 2017, Astronomy & Astrophysics, 599, A16

Luger, R. & Barnes, R. 2015, Astrobiology, 15, 119

MacGregor, M. A., Weinberger, A. J., Wilner, D. J., Kowalski, A. F., & Cranmer, S. R. 2018, The Astrophysical Journal Letters, 855, L2

Malbet, F. & Sozzetti, A. 2018, Astrometry as an Exoplanet Discovery Method, ed. H. J. Deeg & J. A. Belmonte, 196

Marconi, A. 2020, in Ground-based and Airborne Instrumentation for Astronomy VIII, ed. C. J. Evans, J. J. Bryant, & K. Motohara, Vol. 11447, International Society for Optics and Photonics (SPIE), 414 – 425

Martin, S., Booth, A., Liewer, K., et al. 2012, Appl. Opt., 51, 3907

Mason, B. D., Wycoff, G. L., Hartkopf, W. I., Douglass, G. G., & Worley, C. E. 2001, AJ, 122, 3466

Mayor, M., Marmier, M., Lovis, C., et al. 2011, arXiv e-prints, arXiv:1109.2497

Meixner, M., Cooray, A., Leisawitz, D., et al. 2019, arXiv e-prints, arXiv:1912.06213

Morley, C. V., Kreidberg, L., Rustamkulov, Z., Robinson, T., & Fortney, J. J. 2017, The Astrophysical Journal, 850, 121

Mugnier, L., Thiébaut, E., & Belu, A. 2006, in EAS Publications Series, Vol. 22, EAS Publications Series, ed. M. Carbillet, A. Ferrari, & C. Aime, 69–83

National Academies of Sciences, E. & Medicine. 2021, Pathways to Discovery in Astronomy and Astrophysics for the 2020s (Washington, DC: The National Academies Press)

Article number,

page 15 of 23

<!-- page 16 of 23 -->

A&A proofs: manuscript no. LIFE\_paper\_1\_FINAL\_EITED

Oshagh, M., Santos, N. C., Figueira, P., et al. 2017, A&A, 606, A107

Pecaut, M. J. & Mamajek, E. E. 2013, ApJS, 208, 9

Peñín, L. F., Scoarnec, Y., Fernández-Ibarz, J. M., et al. 2020, in Proceedings of the Small Satellite Conference, Technical Session I: Space Mission Architectures, Paper 02

Pierrehumbert, R. & Gaidos, E. 2011, ApJ, 734, L13

Quanz, S. P., Absil, O., Benz, W., et al. 2021, Experimental Astronomy

Quanz, S. P., Crossfield, I., Meyer, M. R., Schmalzl, E., & Held, J. 2015, International Journal of Astrobiology, 14, 279

Quanz, S. P., Kammerer, J., Defrère, D., et al. 2018, in Society of Photo-Optical Instrumentation Engineers (SPIE) Conference Series, Vol. 10701, Optical and Infrared Interferometry and Imaging VI, 107011I

Rauer, H., Catala, C., Aerts, C., et al. 2014, Experimental Astronomy, 38, 249

Reach, W. T. 2010, Icarus, 209, 848

Ribas, I., Bolmont, E., Selsis, F., et al. 2016, Astronomy & Astrophysics, 596, A111

Ricker, G. R., Winn, J. N., Vanderspek, R., et al. 2015, Journal of Astronomical Telescopes, Instruments, and Systems, 1, 014003

Rieke, G. H., Ressler, M. E., Morrison, J. E., et al. 2015, PASP, 127, 665

Sakon, I., Roellig, T. L., Ennico-Smith, K., et al. 2018, in Society of Photo-Optical Instrumentation Engineers (SPIE) Conference Series, Vol. 10698, Space Telescopes and Instrumentation 2018: Optical, Infrared, and Millimeter Wave, ed. M. Lystrup, H. A. MacEwen, G. G. Fazio, N. Batalha, N. Siegler, & E. C. Tong, 1069817

Schwieterman, E. W., Kiang, N. Y., Parenteau, M. N., et al. 2018, Astrobiology, 18, 663

Stark, C. C., Roberge, A., Mandell, A., et al. 2015, ApJ, 808, 149

Stark, C., Belikov, R., Bolcar, M., et al. 2019, in American Astronomical Society Meeting Abstracts, Vol. 233, American Astronomical Society Meeting Abstracts #233, 402.05

Stark, C. C., Roberge, A., Mandell, A., & Robinson, T. D. 2014, ApJ, 795, 122

The LUVOIR Team. 2019, arXiv e-prints, arXiv:1912.06219

Thiébaut, E. & Mugnier, L. 2006, in IAU Colloq. 200: Direct Imaging of Exoplanets: Science & Techniques, ed. C. Aime & F. Vakili, 547–552

Tian, F. & Ida, S. 2015, Nature Geoscience, 8, 177

Tinetti, G., Drossart, P., Eccleston, P., et al. 2018, Experimental Astronomy, 46, 135

Tuomi, M., Jones, H. R. A., Butler, R. P., et al. 2019, arXiv e-prints, arXiv:1906.04644

Turbet, M., Leconte, J., Selsis, F., et al. 2016, Astronomy & Astrophysics, 596, A112

Van Der Walt, S., Colbert, S. C., & Varoquaux, G. 2011, Computing in Science & Engineering, 13, 22

Vanderspek, R., Huang, C. X., Vanderburg, A., et al. 2019, The Astrophysical Journal Letters, 871, L24

Virtanen, P., Gommers, R., Oliphant, T. E., et al. 2020, Nature Methods, 17, 261

Wenger, M., Ochsenbein, F., Egret, D., et al. 2000, A&AS, 143, 9

Zechmeister, M., Dreizler, S., Ribas, I., et al. 2019, Astronomy & Astrophysics, 627, A49

Article number, page 16 of 23

$^{1}$  ETH Zurich, Institute for Particle Physics & Astrophysics, Wolfgang-Pauli-Str. 27, 8093 Zurich, Switzerland

$^{2}$  National Center of Competence in Research PlanetS (www.nccrplanets.ch)

$^{3}$  European Southern Observatory, Karl-Schwarzschild-Str. 2, 85748 Garching, Germany

$^{4}$  Research School of Astronomy & Astrophysics, Australian National University, ACT 2611, Australia

$^{5}$  STAR Institute, University of Liège, 19C allée du Six Août, 4000 Liège, Belgium

$^{6}$  NASA Goddard Space Flight Center, 8800 Greenbelt Rd, Greenbelt, MD, 20771, USA

$^{7}$  Department of Physics, and Institute for Research on Exoplanets, Université de Montréal, Montréal, H3T 1J4, Canada

$^{8}$  University of Oxford, Department of Atmospheric, Oceanic and Planetary Physics, Clarendon Laboratory, Sherrington Road, Oxford OX1 3PU, United Kingdom

$^{9}$  DTU Space, National Space Institute, Technical University of Denmark, Elektrovej 328, DK-2800 Kgs. Lyngby, Denmark

$^{10}$  Department of Extrasolar Planets and Atmospheres, Institute for Planetary Research, German Aerospace Centre, Rutherfordstr. 2, 12489 Berlin

$^{11}$  Zentrum für Astronomie und Astrophysik, Technische Universität Berlin, Hardenbergstrasse 36, D-10623 Berlin, Germany

$^{12}$  Univ. Grenoble Alpes, CNRS, IPAG, F-38000 Grenoble, France

$^{13}$  Centre Spatial de Liège, Université de Liège, Avenue Pré-Aily, 4031 Angleur, Belgium

$^{14}$  Institute of Astronomy, KU Leuven, Celestijnenlaan 200D, 3001, Leuven, Belgium

$^{15}$  University of Zurich, Institute of Computational Sciences, Winterthurerstrasse 190, 8057 Zurich, Switzerland

$^{16}$  Observatoire astronomique de l'Université de Genève, chemin Pegasi 51b, 1290 Versoix, Switzerland

$^{17}$  Large Binocular Telescope Observatory, 933 North Cherry Avenue, Tucson, AZ 85721, USA

$^{18}$  Steward Observatory, Department of Astronomy, University of Arizona, 993 N. Cherry Ave, Tucson, AZ, 85721, USA

$^{19}$  Leiden Observatory, Leiden University, 2333CA Leiden, The Netherlands

$^{20}$  Department of Space, Earth & Environment, Chalmers University of Technology, Onsala Space Observatory, 439 92 Onsala, Sweden

$^{21}$ Institut de Ciències de l'Espai (ICE, CSIC), Campus UAB, C/Can Magrans s/n, 08193 Bellaterra, Spain

$^{22}$  Space Telescope Science Institute, 3700 San Martin Drive, Baltimore, MD 21218, USA

$^{23}$  Department of Astronomy, Stockholm University, Alba Nova University Center, 10691 Stockholm, Sweden

$^{24}$  Department of Space, Earth and Environment, Astronomy and Plasma Physics, Chalmers University of Technology, SE-412 96 Gothenburg, Sweden

$^{25}$  University of Exeter, School of Physics and Astronomy, Stocker Road, Exeter, EX4 4QL, UK

$^{26}$  IAS, CNRS (UMR 8617), bat 121, Univ. Paris-Sud, F-91405 Orsay, France

$^{27}$  University of Tartu, Tartu Observatory, 1 Observatooriumi Str., 61602 Tōravere, Tartumaa, Estonia

$^{28}$  Centro de Astrobiología (CAB, CSIC-INTA), Depto. de Astrofísica, ESAC campus 28692 Villanueva de la Cañada (Madrid), Spain

$^{29}$  Max-Planck-Institut für Astronomie, Königstuhl 17, 69117 Heidelberg, Germany

$^{30}$  SRM Institute of Science and Technology, Chennai, India

$^{31}$  Jet Propulsion Laboratory, California Institute of Technology, 4800 Oak Grove Dr., Pasadena, CA 91109, USA

$^{32}$  Department of Astronomy, University of Michigan, Ann Arbor, MI 48109, USA

$^{33}$  Physikalisches Institut, Universität Bern, Gesellschaftsstrasse 6, 3012 Bern, Switzerland

$^{34}$  Landessternwarte, Zentrum für Astronomie der Universität Heidelberg, Königstuhl 12, 69117 Heidelberg, Germany

$^{35}$  Freie Universität Berlin, Department of Earth Sciences, Malteserstr. 74-100, 12249 Berlin, Germany

<!-- page 17 of 23 -->

Quanz et al.: LIFE: I. Improved exoplanet detection yield estimates for a MIR space interferometer

$^{36}$  Instituto de Astrofísica de Canarias (IAC), E-38200 La Laguna, Tenerife, Spain

$^{37}$  Dept. Astrofísica, Universidad de La Laguna (ULL), E-38206 La Laguna, Tenerife, Spain

$^{38}$  Institut d'Estudis Espacials de Catalunya (IEEC), C/Gran Capità 2-4, 08034 Barcelona, Spain

$^{39}$  Department of Astronomy, Yale University, New Haven, CT 06511, USA

$^{40}$  Nicolaus Copernicus Astronomical Center, Polish Academy of Sciences, ul. Bartycka 18, 00-716 Warsaw, Poland

$^{41}$  Department of Earth and Planetary Sciences, University of California, Riverside, 900 University Ave. Riverside, CA, USA 92521

$^{42}$  Deshbandhu College, University of Delhi 110019 Delhi, India

$^{43}$  Vanderbilt University, Department of Physics & Astronomy, 6301 Stevenson Center Ln., Nashville, TN 37235, USA

$^{44}$  Institute of Astronomy, University of Cambridge, Madingley Road, Cambridge CB3 0HA, UK

45 www.life-space-mission.com

Article number, page 17 of 23

<!-- page 18 of 23 -->

A&A proofs: manuscript no. LIFE\_paper\_1\_FINAL\_EITED

## Appendix A: Stellar sample

The stellar sample was compiled from querying the SIMBAD database$^{15}$ (Wenger et al. 2000) for objects within 20 pc. We removed the substellar objects (planets and brown dwarfs) using the object type parameter. For the remaining stellar objects we focused on main-sequence stars as indicated by the luminosity class of the objects (in case no luminosity class was given we assumed the objects were main-sequence objects). Based on the spectral type of the object we then assigned effective temperature, radius and mass using the relation published in Table 5 of Pecaut & Mamajek (2013), which is based on empirical data. In order to assess which objects are members of binary or multiple systems we used SIMBAD's hierarchical link. This feature connects an object with its parent and child objects. To keep the complexity of our multiple star sample low we decided to only use wide binaries where planetary orbits are possible around both components and thus are most similar to orbits around single stars. We therefore excluded all systems with more than two components and also those that had binary subtypes as SIMBAD object type. This was necessary because not all binary components had their own SIMBAD entry (for example, if the objects cannot be observed individually due to too small separations). In that case the system has no children and we cannot distinguish it from a single star. We also removed objects with incomplete information for the stellar parameters (this step also included binaries, where one component was not listed as a main-sequence star). To obtain an estimate for the separation between the remaining binary systems, we cross-matched the system position with the Washington Visual Double Star Catalog (WDS; Mason et al. 2001) by drawing a circle with a radius of 1 arcsec around the system position. If the position of a WDS object was close enough to fall within the circle we assumed that the two objects were the same physical system. In the case the WDS catalog had more components listed per system than SIMBAD (e.g., because of background stars) we took the separation between the two main components. The separation is normally given for two different observations. We kept the smaller one as the assumed physical separation of the binary system. In order to ensure that all stellar components of the remaining binary systems could harbor stable planetary systems between 0.5 and 10 AU we used the stability criterion from Holman & Wiegert (1999) that takes into account the stellar masses, their separation and the eccentricity of the binary orbit (which we assumed to be zero). Systems that did not fulfill this stability criterion were removed.

The catalog that was the basis for our simulations consists of 1732 stars in total (123 wide binary components and 1609 single stars). The distance and spectral type distributions are shown in Fig. A.1. The catalog is available upon request. We are continuously improving the catalog and plan for an updated version to include the results from Gaia data release 3.

## Appendix B: Technological readiness

The readiness of key technologies relevant for a space mission such as LIFE are summarized in Defrère et al. (2018b) and Quanz et al. (2021), but given their importance for the mission success, we discuss three aspects in the following:

Nulling interferometry: It is important to understand that the LIFE measurement principle has been demonstrated successfully in the lab at ambient temperatures (Martin et al. 2012). One of the next steps is to build a corresponding experiment,

![Chart block](doc:52385f0/tier:standard/page:18/block:8)

![Chart block](doc:52385f0/tier:standard/page:18/block:9)

Fig. A.1. Properties of target stars considered in our study. Top panel: Distance distribution of stars from the stellar input catalog in bins of 2.5 pc. Single stars are shown in orange, wide binaries (see text) in blue, and the sum in green. Bottom panel: Spectral type distribution of stars from the stellar input catalog. Colors are the same as above.

but fully under cryogenic conditions, for a broad wavelength coverage and with sensitivity as one of the key drivers (as needed for a space mission). This is underway in the form of the Nulling Interferometry Cryogenic Experiment at ETH Zurich (Gheorghe et al. 2020). In addition, new nulling instruments have been proposed for the Very Large Telescope Interferometer, including one working in the 3–5  $\mu$ m range (Defrère et al. 2018a). These efforts join previous successful projects related to N-band ground-based nulling interferometry, with the Keck Nuller (Colavita et al. 2009) and the LBTI (Hinz et al. 2014). For LIFE it will be important to leverage the experience from these projects and realize possible synergies.

Autonomous formation flying: To meet the assumptions made for our simulations, a high level of autonomous formation flying of all spacecraft will be required. Specifically, the baselines of the array should be rearranged for every new target star in order to maximize the transmission of photons from a specific distance from the star, and, during an observation, the array should rotate in order to modulate the signal from potential exoplanets. ESA's Proba-3 mission (current launch date: 2023) will demonstrate many critical aspects of formation flying for LIFE. Proba-3 will feature two cube-sized spacecraft with lengths of $\sim 1.5\mathrm{m}$ and masses of $200 - 300\mathrm{kg}$ and will maintain a virtual "rigid structure" with millimeter and arcsecond relative precision. In addition, Proba-3 aims specifically at demonstrating manoeuvres

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">15 http://simbad.cds.unistra.fr/simbad/</span></small>

Article number, page 18 of 23

<!-- page 19 of 23 -->

Quanz et al.: LIFE: I. Improved exoplanet detection yield estimates for a MIR space interferometer

relevant for LIFE, such as station-keeping at distances from 25 m up to 250 m, approaching and separating in formation without losing millimeter precision, repointing the formation, and the combination of station-keeping, resizing, and re-targeting manoeuvres. Details can be found in Peñín et al. (2020). We note that some relevant technology related to formation flying was developed in both France and Germany in the context of the Darwin mission and has been flying on the Swedish Prototype Research Instruments and Space Mission technology Advancement space experiment $^{16}$ .

High quantum-efficiency, low-noise MIR detectors: The low photon rate of exoplanets (cf. Fig. 2) and the need to integrate for many hours, if not days, will put strong requirements on the detector technology in terms of quantum efficiency (in our simulations we assumed 70%; see Sect. 2.3), low readout noise and dark current, and high stability. In addition, a wavelength coverage of at least  $\sim4-18.5\ \mu m$  is required based on atmospheric retrieval analyses quantifying the characterization potential of LIFE for Earth-like atmospheres (cf. Konrad et al. 2021). In this overall context, the technology development plan for the 5.9-meter Origins Space Telescope $^{17}$ , another mission concept proposed in the context of NASA's 2020 astrophysics decadal survey (Meixner et al. 2019), is of great importance as its proposed MISC instrument (Sakon et al. 2018) would cover the same wavelength range as LIFE. While a detailed noise budget and requirements breakdown for LIFE are still being worked on, it is clear that two types of detector technologies can be considered (and eventually traded): HgCdTe detectors (as, for instance, used in NEOCam) and Si:As detectors (as used in JWST/MIRI). Currently, the 3-11  $\mu m$  range is better covered by HgCdTe than Si:As since the latter is basically transparent below 10  $\mu m$  wavelengths. First efforts to go up to 15  $\mu m$  with HgCdTe detectors were already reported (Cabrera et al. 2020) and new arrays with cutoff wavelength >16  $\mu m$  have been grown, hybridized, and packaged and are undergoing testing (cf. OST Technology Development Plan). A key parameter for HgCdTe detectors will be the achievable dark current. For Si:As detectors, in addition to potential challenges related to dark current and 1/f noise, a general problem is the question of availability. Industrial fabricators that have built these detectors in the past (e.g., for Spitzer, WISE, and JWST) have stopped their production of low background detectors in the relevant wavelength range and it is unclear under what conditions and on what timescales restarting the production would be an option.

## Appendix C: Additional figures for non-reference cases

Figures C.1, C.2, C.3, C.4, C.5, and C.6 show the expected detection yield for the non-reference cases. Figure C.7 shows the detection efficiency for FGK-dwarf host stars (i.e., ignoring M dwarfs).

## Appendix D: Distribution of noise contributions for detected planets in the reference case scenarios

Figure D.1 summarizes the contribution of the main noise terms to the overall noise budget for detected planets orbiting FGK stars or M stars.

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">16 https://earth.esa.int/web/eoportal/</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">satellite-missions/p/prisma-prototype</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">17 https://asd.gsfc.nasa.gov/firs/docs/</span></small>

<small><span class="docvortex-page-footnote" data-block-type="page_footnote" style="color:#6b7280">OriginsVolume2TechDevelopmentPlanREDACTED.pdf</span></small>

Article number, page 19 of 23

<!-- page 20 of 23 -->

A&A proofs: manuscript no. LIFE\_paper\_1\_FINAL\_EITED

![Chart block](doc:52385f0/tier:standard/page:20/block:2)

Fig. C.1. Same as Fig. 3, but now for $D = 1.0 \mathrm{~m}$.

![Chart block](doc:52385f0/tier:standard/page:20/block:4)

![Chart block](doc:52385f0/tier:standard/page:20/block:5)

Fig. C.2. Same as Fig. 3, but now for $D = 3.5 \mathrm{~m}$.

![Chart block](doc:52385f0/tier:standard/page:20/block:7)

![Chart block](doc:52385f0/tier:standard/page:20/block:8)

![Chart block](doc:52385f0/tier:standard/page:20/block:9)

![Chart block](doc:52385f0/tier:standard/page:20/block:10)

Fig. C.3. Impact of the aperture size on the exoplanet detection yield. The numbers are relative to those shown for the reference scenarios with $D = 2 \mathrm{~m}$ in Fig. 4. Left: Scenario 1, with $D = 3.5 \mathrm{~m}$ in the top panel and $D = 1.0 \mathrm{~m}$ in the bottom panel. Right: Scenario 2, with $D = 3.5 \mathrm{~m}$ in the top panel and $D = 1.0 \mathrm{~m}$ in the bottom panel.

Article number, page 20 of 23

<!-- page 21 of 23 -->

Quanz et al.: LIFE: I. Improved exoplanet detection yield estimates for a MIR space interferometer

![Chart block](doc:52385f0/tier:standard/page:21/block:2)

Fig. C.4. Same as Fig. 3, but now for a wavelength range of 3–20 μm.

![Chart block](doc:52385f0/tier:standard/page:21/block:4)

![Chart block](doc:52385f0/tier:standard/page:21/block:5)

![Chart block](doc:52385f0/tier:standard/page:21/block:6)

Fig. C.5. Same as Fig. 3, but now for a wavelength range of 6–17 μm.

![Chart block](doc:52385f0/tier:standard/page:21/block:8)

![Chart block](doc:52385f0/tier:standard/page:21/block:9)

![Chart block](doc:52385f0/tier:standard/page:21/block:10)

![Chart block](doc:52385f0/tier:standard/page:21/block:11)

Fig. C.6. Impact of the wavelength coverage on the exoplanet detection yield. The numbers are relative to those shown for the reference scenarios with $\lambda = 4 - 18.5\mu m$ in Fig. 4. Left: Scenario 1, with $\lambda = 3 - 20\mu m$ in the top panel and $\lambda = 6 - 17\mu m$ in the bottom panel. Right: Scenario 2, with $\lambda = 3 - 20\mu m$ in the top panel and $\lambda = 6 - 17\mu m$ in the bottom panel.

Article number,

page 21 of 23

<!-- page 22 of 23 -->

A&A proofs: manuscript no. LIFE\_paper\_1\_FINAL\_EITED

![Chart block](doc:52385f0/tier:standard/page:22/block:2)

Fig. C.7. Same as Fig. 7, but ignoring M stars and only considering FGK stars.

![Chart block](doc:52385f0/tier:standard/page:22/block:4)

Article number,

page 22 of 23

<!-- page 23 of 23 -->

Article number, page 23 of 23

Quanz et al.: LIFE: I. Improved exoplanet detection yield estimates for a MIR space interferometer

Detected Planets around FGK-type stars

![Chart block](doc:52385f0/tier:standard/page:23/block:4)

Detected Planets around M-type stars

![Chart block](doc:52385f0/tier:standard/page:23/block:6)

![Chart block](doc:52385f0/tier:standard/page:23/block:7)

![Chart block](doc:52385f0/tier:standard/page:23/block:8)

Fig. D.1. Donut charts illustrating how the main noise terms considered in our simulations (stellar leakage and noise from the thermal emission of the local and exozodiacal dust disks) contribute to the overall noise budget for the detected planets. The left column shows the results for planets detected around FGK stars and the right column for planets detected around M stars. The top row is for reference case scenario 1 and the bottom row for reference case scenario 2. The numbers correspond to the mean relative contribution of the various noise terms to the total noise per detected planet averaged over all planets. The quoted uncertainties are the corresponding standard deviations (graphically indicated by the colored arcs inside and outside of the donuts). For M stars, noise from exozodiacal dust disks is basically negligible, and stellar leakage and noise from the zodiacal dust disk contribute equally to the total noise in both scenarios. This trend is generally the same for FGK stars in scenario 1, even though the relative share of exozodi noise is larger. For scenario 2, however, stellar leakage clearly dominates the noise budget of planets around FGK stars.