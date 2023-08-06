=====
About
=====

.. image:: https://enmap.git-pages.gfz-potsdam.de/sicor/doc/_static/sicor_logo_lr.png
   :width: 150px
   :alt: SICOR Logo

Sensor Independent Atmospheric Correction of optical Earth Observation (EO) data from both multispectral and
hyperspectral instruments. Currently, SICOR can be applied to Sentinel-2 and EnMAP data but the implementation of
additional space- and airborne sensors is under development. As unique features for the processing of hyperspectral
data, SICOR_ incorporates a coupled retrieval of the three phases of water and a snow and ice surface property
inversion based on a simultaneous optimization of atmosphere and surface state (Bohn et al., 2020; Bohn et al., 2021).
Both algorithms are based on Optimal Estimation (OE) including the calculation of several measures of retrieval
uncertainties. The atmospheric modeling in case of hyperspectral data is based on the MODTRAN® radiative transfer code
whereas the atmospheric correction of multispectral data relies on the MOMO code.

This project was funded by GFZ's EnMAP_ and GeoMultiSens_ activities, AgriCircle trough cooperation with Adama,
and ESA. The MODTRAN® trademark is being used with the express permission of the owner, Spectral Sciences, Inc. The
package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.


Feature overview
----------------

* Sentinel-2 L1C to L2A processing
* EnMAP L1B to L2A processing
* generic atmospheric correction for hyperspectral airborne and spaceborne data
* retrieval of the three phases of water from hyperspectral data
* 'lazy Gaussian inversion' of snow and ice surface properties
* calculation of various retrieval uncertainties
  (including a posteriori errors, averaging kernels, gain matrices, degrees of freedom, information content)
* atmospheric correction for Landsat-8: work in progress
* CH4 retrieval from hyperspectral data: work in progress


Bibliography
____________

Bohn, N., Guanter, L., Kuester, T., Preusker, R., Segl, K. (2020). Coupled retrieval of the three phases of water from
spaceborne imaging spectroscopy measurements. Remote Sens. Environ., 242, 111708,
https://doi.org/10.1016/j.rse.2020.111708.

Bohn, N., Painter, T. H., Thompson, D. R., Carmon, N., Susiluoto, J., Turmon, M. J., Helmlinger, M. C., Green, R. O.,
Cook, J. M., Guanter, L. (2021). Optimal estimation of snow and ice surface parameters from imaging spectroscopy
measurements. Remote Sens. Environ., 264, 112613, https://doi.org/10.1016/j.rse.2021.112613.

.. _SICOR: https://git.gfz-potsdam.de/EnMAP/sicor/
.. _GeoMultiSens: http://www.geomultisens.gfz-potsdam.de
.. _EnMAP: https://www.enmap.org
.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
